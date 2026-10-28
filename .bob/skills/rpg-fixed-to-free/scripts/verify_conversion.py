#!/usr/bin/env python3
"""Verify a fixed-to-free RPG conversion.

Compares the ORIGINAL fixed/mixed source with the CONVERTED **free source and reports:

  ERROR    - must be fixed (exit code 1): not **free, leftover fixed specs or /free,
             unbalanced blocks, files or subroutines that disappeared
  WARNING  - must be fixed or explained in the conversion report: MOVE/GOTO/numbered
             indicators still present, I/O opcode counts that differ, missing fields
  INFO     - TODO-CONV markers to list in the report

This is a static check. It does not replace compiling and testing.

Usage:
    python3 verify_conversion.py ORIGINAL CONVERTED [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

IO_OPCODES = ["CHAIN", "READ", "READE", "READP", "READPE", "SETLL", "SETGT", "WRITE",
              "UPDATE", "DELETE", "EXFMT", "EXSR", "CALL", "CALLP", "RETURN", "UNLOCK"]
BLOCKS = {  # opener -> closer
    "IF": "ENDIF", "DOW": "ENDDO", "DOU": "ENDDO", "FOR": "ENDFOR", "SELECT": "ENDSL",
    "MONITOR": "ENDMON", "BEGSR": "ENDSR", "DCL-PROC": "END-PROC", "DCL-PI": "END-PI",
    "DCL-PR": "END-PR",
}


def strip_free_comment(line: str) -> str:
    """Remove a // comment that is not inside a quoted literal."""
    in_quote = False
    for i, ch in enumerate(line):
        if ch == "'":
            in_quote = not in_quote
        elif ch == "/" and not in_quote and line[i:i + 2] == "//":
            return line[:i]
    return line


# ---------------------------------------------------------------- original (fixed) parsing
def parse_original(lines: list[str]) -> dict:
    files, subrs, fields, calls = set(), set(), set(), set()
    ops: Counter = Counter()
    in_free = False
    for raw in lines:
        line = raw.ljust(80).upper()
        directive = line[6:].strip()
        if directive.startswith("/FREE"):
            in_free = True
            continue
        if directive.startswith("/END-FREE"):
            in_free = False
            continue
        if in_free:
            code = strip_free_comment(line).strip()
            word = re.split(r"[\s(;]", code, maxsplit=1)[0] if code else ""
            if word in IO_OPCODES:
                ops[word] += 1
            m = re.match(r"BEGSR\s+(\w+)", code)
            if m:
                subrs.add(m.group(1))
            continue
        spec, comment = line[5], line[6] == "*"
        if comment:
            continue
        if spec == "F":
            name = line[6:16].strip()
            if name:
                files.add(name)
        elif spec == "D":
            name = line[6:21].strip().rstrip(".")
            if name and not name.startswith("..."):
                fields.add(name)
        elif spec == "C":
            factor1, opcode = line[11:25].strip(), line[25:35].strip().split("(")[0]
            factor2, result, length = line[35:49].strip(), line[49:63].strip(), line[63:68].strip()
            if opcode in IO_OPCODES:
                ops[opcode] += 1
            if opcode == "BEGSR":
                subrs.add(factor1)
            if opcode in ("CALL", "CALLB"):
                calls.add(factor2.strip("'"))
            if result and length:          # field defined on the C-spec
                fields.add(result)
    return {"files": files, "subroutines": subrs, "fields": fields, "calls": calls, "ops": ops}


# ---------------------------------------------------------------- converted (free) checks
def check_converted(lines: list[str], findings: list[tuple[str, int, str]]) -> dict:
    files, subrs, declared = set(), set(), set()
    ops: Counter = Counter()
    stack: list[tuple[str, int]] = []
    text_upper = []

    if not lines or not lines[0].strip().lower().startswith("**free"):
        findings.append(("ERROR", 1, "Line 1 must be **free"))

    fixed_spec = re.compile(r"^[ 0-9]{5}[HFDICOP][ *A-Z]")
    for n, raw in enumerate(lines, 1):
        if n == 1:
            continue
        code = strip_free_comment(raw).strip()
        up = code.upper()
        text_upper.append(up)
        if raw.strip().upper().startswith(("/FREE", "/END-FREE")):
            findings.append(("ERROR", n, "/free or /end-free directive in a **free source"))
        if fixed_spec.match(raw) and not raw.strip().startswith("//"):
            findings.append(("ERROR", n, f"looks like a fixed-format {raw[5]}-spec"))
        if not up:
            continue

        if re.match(r"(MOVE|MOVEL|MOVEA)\b", up):
            findings.append(("WARNING", n, "MOVE-family opcode remains (not valid in **free)"))
        if re.match(r"(GOTO|TAG|CAB(EQ|NE|GT|LT|GE|LE))\b", up):
            findings.append(("WARNING", n, "GOTO/TAG/CABxx remains"))
        for ind in re.findall(r"\*IN(\d\d)\b", up):
            findings.append(("WARNING", n, f"numbered indicator *IN{ind} still used — confirm it must be kept"))
        if "TODO-CONV" in raw.upper():
            findings.append(("INFO", n, "TODO-CONV: " + raw.split("TODO-CONV", 1)[1].strip(" :")))

        word = re.split(r"[\s(;]", up, maxsplit=1)[0]
        if word in IO_OPCODES:
            ops[word] += 1
        elif re.match(r"\w+\s*\(", up) and not up.startswith(("DCL-", "IF", "DOW", "DOU", "WHEN", "FOR")):
            ops["CALLP"] += 1   # prototyped call written without CALLP
        m = re.match(r"DCL-F\s+(\w+)", up)
        if m:
            files.add(m.group(1))
        m = re.match(r"BEGSR\s+(\w+)", up)
        if m:
            subrs.add(m.group(1))
        m = re.match(r"DCL-(S|C|DS|PR|PROC)\s+(\w+)", up)
        if m:
            declared.add(m.group(2))
        elif stack and stack[-1][0] in ("DCL-PI", "DCL-PR") or re.match(r"(\w+)\s+(CHAR|VARCHAR|PACKED|ZONED|INT|UNS|IND|DATE|TIME|TIMESTAMP|LIKE|LIKEDS|POINTER|FLOAT)\b", up):
            m2 = re.match(r"(\w+)\s+\w", up)
            if m2:
                declared.add(m2.group(1))

        # block balance
        if word in BLOCKS and not re.search(r"\b" + BLOCKS[word] + r"\b", up):
            stack.append((word, n))
        elif word in BLOCKS.values():
            if not stack:
                findings.append(("ERROR", n, f"{word} without a matching opener"))
            else:
                opener, line_no = stack.pop()
                if BLOCKS[opener] != word:
                    findings.append(("ERROR", n, f"{word} closes {opener} opened on line {line_no}"))
    for opener, line_no in stack:
        findings.append(("ERROR", line_no, f"{opener} is never closed with {BLOCKS[opener]}"))

    return {"files": files, "subroutines": subrs, "declared": declared, "ops": ops,
            "text": "\n".join(text_upper)}


def compare(orig: dict, conv: dict, findings: list) -> None:
    for f in sorted(orig["files"] - conv["files"]):
        findings.append(("ERROR", 0, f"file {f} is declared in the original but has no dcl-f"))
    for s in sorted(orig["subroutines"] - conv["subroutines"]):
        if not re.search(rf"DCL-PROC\s+{s}\b", conv["text"]):
            findings.append(("ERROR", 0, f"subroutine {s} disappeared (not a begsr or dcl-proc)"))
    for fld in sorted(orig["fields"] - conv["declared"]):
        if not re.search(rf"\b{re.escape(fld)}\b", conv["text"]):
            findings.append(("WARNING", 0, f"field {fld} from the original is not declared or used"))
    for call in sorted(orig["calls"]):
        if call and call not in conv["text"]:
            findings.append(("WARNING", 0, f"CALL target {call} not found (expected an extpgm prototype)"))
    for op in ("CHAIN", "READ", "READE", "READP", "SETLL", "SETGT", "WRITE", "UPDATE",
               "DELETE", "EXFMT", "EXSR"):
        a, b = orig["ops"].get(op, 0), conv["ops"].get(op, 0)
        if a != b:
            findings.append(("WARNING", 0, f"{op} appears {a}x in the original but {b}x converted"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original", type=Path)
    ap.add_argument("converted", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    for p in (args.original, args.converted):
        if not p.is_file():
            print(f"error: {p} not found", file=sys.stderr)
            return 2

    read = lambda p: p.read_text(encoding="utf-8", errors="replace").splitlines()  # noqa: E731
    findings: list[tuple[str, int, str]] = []
    orig = parse_original(read(args.original))
    conv = check_converted(read(args.converted), findings)
    compare(orig, conv, findings)

    order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1]))
    counts = Counter(f[0] for f in findings)
    status = "FAIL" if counts["ERROR"] else ("PASS WITH WARNINGS" if counts["WARNING"] else "PASS")

    if args.json:
        print(json.dumps({"status": status, "counts": counts,
                          "findings": [{"level": l, "line": n, "message": m} for l, n, m in findings]},
                         indent=2))
    else:
        print(f"Verifying {args.converted} against {args.original}")
        for level, n, msg in findings:
            where = f"line {n}" if n else "overall"
            print(f"  {level:<7} {where:<9} {msg}")
        print(f"\nResult: {status}  ({counts['ERROR']} errors, {counts['WARNING']} warnings, "
              f"{counts['INFO']} TODO-CONV)")
    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
