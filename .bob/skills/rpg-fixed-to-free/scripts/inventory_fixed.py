#!/usr/bin/env python3
"""Inventory a fixed-format (or mixed) RPG source before converting it to free format.

Reports spec counts, opcodes, numbered indicators, risky constructs and a risk level.
Pure standard library, so it runs on a laptop or in IBM i PASE.

Usage:
    python3 inventory_fixed.py SOURCE [SOURCE ...] [--format text|markdown|json]

Exit code: 0 always (this is a report, not a gate). Use --fail-on-high in CI to exit 1
when any source is HIGH risk.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

SPEC_TYPES = set("HFDICOP")

# Opcodes that need human attention during conversion, with a weight for the risk score.
RISKY_OPCODES = {
    "MOVE": 2, "MOVEL": 2, "MOVEA": 3, "GOTO": 3, "TAG": 1, "CABEQ": 3, "CABNE": 3,
    "CABGT": 3, "CABLT": 3, "CABGE": 3, "CABLE": 3, "COMP": 2, "LOOKUP": 2, "LOKUP": 2,
    "CASEQ": 1, "CASNE": 1, "CASGT": 1, "CASLT": 1, "CASGE": 1, "CASLE": 1, "CAS": 1,
    "SUBST": 1, "CAT": 1, "MVR": 2, "XFOOT": 1, "TIME": 1, "DEBUG": 2, "FREE": 3,
}
CYCLE_FILE_TYPES = {"P", "S"}  # primary / secondary files (F-spec col 18)


@dataclass
class Inventory:
    file: str
    total_lines: int = 0
    format: str = "fixed"
    spec_counts: dict = field(default_factory=dict)
    comment_lines: int = 0
    free_block_lines: int = 0
    opcodes: dict = field(default_factory=dict)
    risky_opcodes: dict = field(default_factory=dict)
    numbered_indicators: list = field(default_factory=list)
    conditioning_indicator_lines: int = 0
    resulting_indicator_lines: int = 0
    level_break_indicators: list = field(default_factory=list)
    uses_rpg_cycle: bool = False
    has_entry_plist: bool = False
    klists: list = field(default_factory=list)
    subroutines: list = field(default_factory=list)
    files: list = field(default_factory=list)
    copybooks: list = field(default_factory=list)
    o_specs: int = 0
    risk_score: int = 0
    risk_level: str = "LOW"
    notes: list = field(default_factory=list)


def col(line: str, start: int, end: int) -> str:
    """Return RPG columns start..end (1-based, inclusive), stripped."""
    return line[start - 1:end].strip() if len(line) >= start else ""


def analyze(path: Path) -> Inventory:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    inv = Inventory(file=str(path), total_lines=len(lines))
    specs: Counter = Counter()
    ops: Counter = Counter()
    indicators: set[str] = set()
    level_breaks: set[str] = set()
    in_free = False

    if lines and lines[0].strip().lower().startswith("**free"):
        inv.format = "free"
        inv.notes.append("Source is already fully free (**free on line 1).")
        return inv

    ind_ref = re.compile(r"\*IN(\d\d)\b", re.IGNORECASE)

    for raw in lines:
        line = raw.rstrip("\n").ljust(80)
        upper = line.upper()
        directive = col(upper, 7, 80)
        if directive.startswith("/FREE"):
            in_free = True
            continue
        if directive.startswith("/END-FREE"):
            in_free = False
            continue
        if directive.startswith(("/COPY", "/INCLUDE")):
            inv.copybooks.append(directive.split(None, 1)[1] if " " in directive else directive)
            continue
        if in_free:
            inv.free_block_lines += 1
            for m in ind_ref.finditer(upper):
                indicators.add(m.group(1))
            first = upper.strip().split(" ", 1)[0].rstrip(";").split("(")[0]
            if first:
                ops[first] += 1
            continue

        spec = upper[5]
        if spec not in SPEC_TYPES:
            continue
        if upper[6] == "*":
            inv.comment_lines += 1
            continue
        specs[spec] += 1

        for m in ind_ref.finditer(upper):
            indicators.add(m.group(1))

        if spec == "F":
            name = col(line, 7, 16)
            if name:
                inv.files.append(name)
            if upper[17] in CYCLE_FILE_TYPES:
                inv.uses_rpg_cycle = True
        elif spec == "O":
            inv.o_specs += 1
        elif spec == "C":
            level = col(upper, 7, 8)
            if re.fullmatch(r"L[0-9]|LR", level):
                level_breaks.add(level)
            if col(upper, 9, 11):
                inv.conditioning_indicator_lines += 1
                cond = re.sub(r"^N", "", col(upper, 9, 11))
                if cond.isdigit():
                    indicators.add(cond)
            factor1 = col(upper, 12, 25)
            opcode = col(upper, 26, 35)
            if opcode:
                base = opcode.split("(")[0]
                ops[base] += 1
                if base == "PLIST" and factor1 == "*ENTRY":
                    inv.has_entry_plist = True
                if base == "KLIST":
                    inv.klists.append(factor1)
                if base == "BEGSR":
                    inv.subroutines.append(factor1)
            resulting = [col(upper, a, a + 1) for a in (71, 73, 75)]
            if any(resulting):
                inv.resulting_indicator_lines += 1
                for r in resulting:
                    if r.isdigit():
                        indicators.add(r)

    inv.spec_counts = dict(sorted(specs.items()))
    inv.opcodes = dict(ops.most_common())
    inv.risky_opcodes = {op: n for op, n in inv.opcodes.items() if op in RISKY_OPCODES}
    inv.numbered_indicators = sorted(indicators)
    inv.level_break_indicators = sorted(level_breaks)
    if inv.free_block_lines:
        inv.format = "mixed"

    score = sum(RISKY_OPCODES[op] * n for op, n in inv.risky_opcodes.items())
    score += len(inv.numbered_indicators) * 2
    score += inv.conditioning_indicator_lines
    if inv.uses_rpg_cycle or inv.level_break_indicators:
        score += 50
        inv.notes.append("Uses the RPG cycle / level breaks: needs a redesign, not a translation.")
    if inv.o_specs:
        score += 10
        inv.notes.append(f"{inv.o_specs} O-spec lines: internally described printer output.")
    if inv.has_entry_plist:
        inv.notes.append("*ENTRY PLIST: convert to dcl-pi; check callers for optional parameters.")
    if inv.klists:
        inv.notes.append(f"KLISTs to replace: {', '.join(inv.klists)}")
    if "GOTO" in inv.risky_opcodes or any(op.startswith("CAB") for op in inv.risky_opcodes):
        inv.notes.append("GOTO/CABxx present: control flow must be restructured carefully.")
    if any(op in inv.risky_opcodes for op in ("MOVE", "MOVEL", "MOVEA")):
        inv.notes.append("MOVE family present: apply reference/pitfalls.md items 1-3 to each one.")

    inv.risk_score = score
    inv.risk_level = "HIGH" if score >= 40 else "MEDIUM" if score >= 15 else "LOW"
    return inv


def to_markdown(inv: Inventory) -> str:
    out = [f"### Inventory: `{inv.file}`", ""]
    out.append(f"- Format: **{inv.format}**, {inv.total_lines} lines "
               f"({inv.comment_lines} comment, {inv.free_block_lines} in /free blocks)")
    out.append(f"- Risk: **{inv.risk_level}** (score {inv.risk_score})")
    if inv.format == "free":
        return "\n".join(out + ["", *[f"- {n}" for n in inv.notes]])
    out.append(f"- Specs: {', '.join(f'{k}={v}' for k, v in inv.spec_counts.items()) or 'none'}")
    out.append(f"- Files: {', '.join(inv.files) or 'none'}")
    out.append(f"- Subroutines: {', '.join(inv.subroutines) or 'none'}")
    out.append(f"- Numbered indicators: {', '.join('*IN' + i for i in inv.numbered_indicators) or 'none'}")
    out.append(f"- Lines with conditioning indicators: {inv.conditioning_indicator_lines}; "
               f"with resulting indicators: {inv.resulting_indicator_lines}")
    if inv.copybooks:
        out.append(f"- Copybooks: {', '.join(inv.copybooks)}")
    out += ["", "| Opcode | Count | Needs attention |", "|---|---|---|"]
    for op, n in inv.opcodes.items():
        out.append(f"| {op} | {n} | {'⚠️' if op in RISKY_OPCODES else ''} |")
    if inv.notes:
        out += ["", "**Notes**", *[f"- {n}" for n in inv.notes]]
    return "\n".join(out)


def to_text(inv: Inventory) -> str:
    return to_markdown(inv).replace("**", "").replace("`", "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", type=Path)
    ap.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    ap.add_argument("--fail-on-high", action="store_true", help="exit 1 if any source is HIGH risk")
    args = ap.parse_args()

    results = []
    for src in args.sources:
        if not src.is_file():
            print(f"error: {src} not found", file=sys.stderr)
            return 2
        results.append(analyze(src))

    if args.format == "json":
        print(json.dumps([asdict(r) for r in results], indent=2))
    else:
        render = to_markdown if args.format == "markdown" else to_text
        print("\n\n".join(render(r) for r in results))

    if args.fail_on_high and any(r.risk_level == "HIGH" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
