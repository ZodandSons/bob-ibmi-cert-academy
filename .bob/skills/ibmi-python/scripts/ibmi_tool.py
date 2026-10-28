#!/usr/bin/env python3
"""ibmi_tool.py - a small, safe CLI for talking to IBM i from Python.

Backends (chosen automatically, or with --backend):
  mapepire  pip install mapepire-python   (needs the Mapepire daemon on IBM i, port 8076)
  odbc      pip install pyodbc            (needs the IBM i Access ODBC driver)

Credentials come ONLY from environment variables (or a .env file you source yourself):
  DB2i_HOST, DB2i_USER, DB2i_PASS, DB2i_PORT (default 8076)

Subcommands:
  query      Run a read-only SELECT / VALUES / WITH statement
  cl         Run a CL command through QSYS2.QCMDEXC (destructive commands refused)
  source     Download a source member to a local stream file
  objects    List objects in a library (QSYS2.OBJECT_STATISTICS)
  where-used Programs in a library that reference an object (QSYS2.PROGRAM_REFERENCES)

Every subcommand accepts --dry-run to print the SQL without connecting.

Examples:
  python3 ibmi_tool.py query "SELECT * FROM ORDDEV01.CUSTMAST FETCH FIRST 5 ROWS ONLY"
  python3 ibmi_tool.py query "SELECT * FROM CUSTMAST WHERE CMCUST = ?" -p 1001 --format json
  python3 ibmi_tool.py cl "ADDLIBLE ORDDEV01"
  python3 ibmi_tool.py source ORDDEV01 QRPGLESRC CUSTINQ -o qrpglesrc/legacy/custinq.pgm.rpgle
  python3 ibmi_tool.py objects ORDDEV01 --type "*PGM *SRVPGM"
  python3 ibmi_tool.py where-used ORDDEV01 CUSTMAST
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

NAME = re.compile(r"^[A-Z$#@][A-Z0-9$#@_]{0,9}$")
READ_ONLY_SQL = re.compile(r"^\s*(SELECT|VALUES|WITH)\b", re.IGNORECASE)
BLOCKED_CL = re.compile(
    r"\b(DLTLIB|CLRLIB|DLTF|CLRPFM|RMVM|DLTOBJ|DLTPGM|DLTSRVPGM|RSTLIB|RSTOBJ|"
    r"PWRDWNSYS|ENDSBS|ENDSYS|CHGSYSVAL|CHGUSRPRF|CRTUSRPRF|DLTUSRPRF)\b",
    re.IGNORECASE,
)


# ------------------------------------------------------------------ helpers
def ibmi_name(value: str) -> str:
    """argparse type: validate and uppercase an IBM i object/library name."""
    up = value.strip().upper()
    if not NAME.match(up):
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid IBM i name (max 10 chars)")
    return up


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def credentials() -> dict:
    missing = [v for v in ("DB2i_HOST", "DB2i_USER", "DB2i_PASS") if not os.environ.get(v)]
    if missing:
        die(f"set environment variable(s): {', '.join(missing)}")
    return {
        "host": os.environ["DB2i_HOST"],
        "user": os.environ["DB2i_USER"],
        "password": os.environ["DB2i_PASS"],
        "port": int(os.environ.get("DB2i_PORT", "8076")),
    }


# ------------------------------------------------------------------ connection wrapper
class IBMiConnection:
    """One connection for the whole command (QTEMP objects live as long as it does)."""

    def __init__(self, backend: str = "auto"):
        creds = credentials()
        self.backend = backend
        if backend in ("auto", "mapepire"):
            try:
                from mapepire_python import connect  # type: ignore
                self.conn = connect(creds)
                self.backend = "mapepire"
                return
            except ImportError:
                if backend == "mapepire":
                    die("mapepire-python is not installed: pip install mapepire-python")
        try:
            import pyodbc  # type: ignore
        except ImportError:
            die("install a backend: pip install mapepire-python  (or pyodbc + IBM i Access ODBC)")
        self.conn = pyodbc.connect(
            driver="{IBM i Access ODBC Driver}", system=creds["host"],
            uid=creds["user"], pwd=creds["password"], naming=1,  # 1 = system naming (LIB/FILE)
        )
        self.backend = "odbc"

    def run(self, sql: str, params: Sequence[Any] = ()) -> tuple[list[str], list[tuple]]:
        """Execute SQL and return (column names, rows). Non-queries return ([], [])."""
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params)) if params else cur.execute(sql)
        if not cur.description:
            return [], []
        cols = [d[0] for d in cur.description]
        return cols, normalize_rows(cur.fetchall(), cols)

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:  # noqa: BLE001 - closing must never mask the real error
            pass


def normalize_rows(raw: Any, cols: list[str]) -> list[tuple]:
    """Mapepire versions differ: rows may be tuples, dicts, or {'data': [...]}."""
    if isinstance(raw, dict):
        raw = raw.get("data", [])
    rows = []
    for r in raw or []:
        rows.append(tuple(r.get(c) for c in cols) if isinstance(r, dict) else tuple(r))
    return rows


# ------------------------------------------------------------------ output
def emit(cols: list[str], rows: Iterable[tuple], fmt: str, out=sys.stdout) -> None:
    rows = list(rows)
    if fmt == "json":
        json.dump([dict(zip(cols, r)) for r in rows], out, indent=2, default=str)
        out.write("\n")
    elif fmt == "csv":
        w = csv.writer(out)
        w.writerow(cols)
        w.writerows(rows)
    else:
        widths = [max([len(str(c))] + [len(str(r[i]).rstrip()) for r in rows]) for i, c in enumerate(cols)]
        print("  ".join(str(c).ljust(w) for c, w in zip(cols, widths)), file=out)
        print("  ".join("-" * w for w in widths), file=out)
        for r in rows:
            print("  ".join(str(v).rstrip().ljust(w) for v, w in zip(r, widths)), file=out)
        print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})", file=out)


# ------------------------------------------------------------------ subcommands
def cmd_query(a: argparse.Namespace) -> None:
    if not READ_ONLY_SQL.match(a.sql):
        die("query only runs SELECT / VALUES / WITH statements")
    sql = a.sql.rstrip().rstrip(";")
    if a.max_rows and not re.search(r"FETCH\s+FIRST", sql, re.IGNORECASE):
        sql += f" FETCH FIRST {a.max_rows} ROWS ONLY"
    if a.dry_run:
        print(sql, "\n-- params:", a.param)
        return
    with_connection(a, lambda c: emit(*c.run(sql, a.param), a.format))


def cmd_cl(a: argparse.Namespace) -> None:
    if BLOCKED_CL.search(a.command):
        die("destructive CL command refused - run it yourself if it is really intended", 2)
    sql, params = "CALL QSYS2.QCMDEXC(?)", [a.command]
    if a.dry_run:
        print(sql, "\n-- params:", params)
        return
    with_connection(a, lambda c: (c.run(sql, params), print(f"OK: {a.command}")))


def cmd_source(a: argparse.Namespace) -> None:
    alias = "QTEMP.BOBSRC"
    steps = [
        (f"CREATE OR REPLACE ALIAS {alias} FOR {a.library}.{a.file} ({a.member})", ()),
        (f"SELECT SRCDTA FROM {alias} ORDER BY SRCSEQ", ()),
        (f"DROP ALIAS {alias}", ()),
    ]
    if a.dry_run:
        print("\n".join(s for s, _ in steps))
        return

    def work(c: IBMiConnection) -> None:
        c.run(*steps[0])
        _, rows = c.run(*steps[1])
        c.run(*steps[2])
        text = "\n".join(str(r[0]).rstrip() for r in rows) + "\n"
        target = Path(a.output or f"{a.member.lower()}.src")
        if target.exists() and not a.force:
            die(f"{target} exists - use --force to overwrite")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        print(f"Wrote {len(rows)} lines to {target}")

    with_connection(a, work)


def cmd_objects(a: argparse.Namespace) -> None:
    sql = ("SELECT OBJNAME, OBJTYPE, OBJATTRIBUTE, OBJTEXT, CHANGE_TIMESTAMP, LAST_USED_TIMESTAMP "
           "FROM TABLE(QSYS2.OBJECT_STATISTICS(?, ?)) ORDER BY OBJTYPE, OBJNAME")
    params = [a.library, a.type]
    if a.dry_run:
        print(sql, "\n-- params:", params)
        return
    with_connection(a, lambda c: emit(*c.run(sql, params), a.format))


def cmd_where_used(a: argparse.Namespace) -> None:
    sql = ("SELECT PROGRAM_NAME, PROGRAM_TYPE, OBJECT_TYPE, FILE_USAGE "
           "FROM QSYS2.PROGRAM_REFERENCES "
           "WHERE PROGRAM_LIBRARY = ? AND OBJECT_NAME = ? ORDER BY PROGRAM_NAME")
    params = [a.library, a.object]
    if a.dry_run:
        print(sql, "\n-- params:", params)
        return
    with_connection(a, lambda c: emit(*c.run(sql, params), a.format))


def with_connection(a: argparse.Namespace, fn) -> None:
    conn = IBMiConnection(a.backend)
    try:
        fn(conn)
    except Exception as exc:  # noqa: BLE001 - report any driver error cleanly
        die(f"{type(exc).__name__}: {exc}")
    finally:
        conn.close()


# ------------------------------------------------------------------ CLI
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=("auto", "mapepire", "odbc"), default="auto")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p: argparse.ArgumentParser, output: bool = True) -> None:
        p.add_argument("--dry-run", action="store_true", help="print SQL, do not connect")
        p.add_argument("--backend", choices=("auto", "mapepire", "odbc"), default=argparse.SUPPRESS)
        if output:
            p.add_argument("--format", choices=("table", "json", "csv"), default="table")

    p = sub.add_parser("query", help="run a read-only SQL query")
    p.add_argument("sql")
    p.add_argument("-p", "--param", action="append", default=[], help="parameter marker value (repeatable)")
    p.add_argument("--max-rows", type=int, default=500, help="appended FETCH FIRST n (0 = no limit)")
    common(p)
    p.set_defaults(func=cmd_query)

    p = sub.add_parser("cl", help="run a CL command via QSYS2.QCMDEXC")
    p.add_argument("command")
    common(p, output=False)
    p.set_defaults(func=cmd_cl)

    p = sub.add_parser("source", help="download a source member")
    p.add_argument("library", type=ibmi_name)
    p.add_argument("file", type=ibmi_name)
    p.add_argument("member", type=ibmi_name)
    p.add_argument("-o", "--output", help="local file to write")
    p.add_argument("--force", action="store_true", help="overwrite an existing file")
    common(p, output=False)
    p.set_defaults(func=cmd_source)

    p = sub.add_parser("objects", help="list objects in a library")
    p.add_argument("library", type=ibmi_name)
    p.add_argument("--type", default="*ALL", help='e.g. "*PGM *SRVPGM"')
    common(p)
    p.set_defaults(func=cmd_objects)

    p = sub.add_parser("where-used", help="programs referencing an object")
    p.add_argument("library", type=ibmi_name)
    p.add_argument("object", type=ibmi_name)
    common(p)
    p.set_defaults(func=cmd_where_used)
    return ap


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
