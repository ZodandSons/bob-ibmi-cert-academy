#!/usr/bin/env python3
# Hook event : PreToolUse (matcher ^execute_command$) — exit 2 BLOCKS the command
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
"""PreToolUse hook: block destructive shell / IBM i commands before Bob runs them.

stdin:  {"event": "PreToolUse", "tool": "execute_command", "input": {"command": "..."}}
exit 2: block the tool call (reason on stderr goes to Bob's log and the user)

Covers commands run locally, over SSH (`ssh ibmi system "..."`), in PASE (`system "..."`,
`cl "..."`), and SQL passed to tools such as `db2util`, `qsh -c db2`, or Python one-liners.
Customize PROTECTED_LIBS for your shop.
"""
import json
import os
import re
import sys

PROTECTED_LIBS = {"ORDPRD", "ORDDTA", "QSYS", "QGPL", "QUSRSYS"}
PROTECTED_LIBS |= {x.strip().upper() for x in os.environ.get("BOB_PROTECTED_LIBS", "").split(",") if x.strip()}

DESTRUCTIVE_CL = r"\b(DLTLIB|CLRLIB|DLTF|CLRPFM|RMVM|DLTOBJ|DLTPGM|DLTSRVPGM|RSTLIB|RSTOBJ|PWRDWNSYS|ENDSBS|ENDSYS|CHGSYSVAL)\b"
DESTRUCTIVE_SQL = [
    r"\bDROP\s+(TABLE|SCHEMA|VIEW|INDEX|PROCEDURE|FUNCTION)\b",
    r"\bTRUNCATE\b",
    r"\bDELETE\s+FROM\s+[\w./]+\s*(;|$|\")",  # DELETE without a WHERE clause
]
DESTRUCTIVE_SHELL = [
    r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\.|\*)",
    r"\bgit\s+push\s+.*--force\b",
    r"\bgit\s+reset\s+--hard\b",
]


def block(reason: str) -> int:
    print(f"Blocked by .bob/hooks/guard-dangerous-commands.py: {reason}", file=sys.stderr)
    return 2


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = str(payload.get("input", {}).get("command", ""))
    upper = command.upper()

    for lib in PROTECTED_LIBS:
        if re.search(rf"(\b{lib}/|\b{lib}\.|LIB\({lib}\)|LIBRARY\({lib}\)|\bSET\s+SCHEMA\s+{lib}\b)", upper):
            return block(f"command references protected library {lib}")

    m = re.search(DESTRUCTIVE_CL, upper)
    if m:
        return block(f"destructive CL command {m.group(1)} requires a human to run it")

    for pattern in DESTRUCTIVE_SQL:
        if re.search(pattern, upper):
            return block("destructive SQL (DROP / TRUNCATE / DELETE without WHERE)")

    for pattern in DESTRUCTIVE_SHELL:
        if re.search(pattern, command):
            return block("destructive shell command")

    return 0


if __name__ == "__main__":
    sys.exit(main())
