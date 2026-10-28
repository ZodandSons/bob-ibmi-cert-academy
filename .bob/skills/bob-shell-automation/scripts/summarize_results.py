#!/usr/bin/env python3
"""Summarize a folder of `bob run --format json` results (from batch-convert.sh).

Usage:
    python3 summarize_results.py RESULTS_DIR [--csv]

Reads <name>.result.json (Bob's final JSON object), <name>.inventory.json and
<name>.verify.txt when present, and prints a Markdown table (or CSV) with status,
risk, verification result, cost, tokens and duration per source.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def summarize(folder: Path) -> list[dict]:
    rows = []
    names = sorted({p.name.split(".")[0] for p in folder.glob("*.inventory.json")} |
                   {p.name.split(".")[0] for p in folder.glob("*.result.json")})
    for name in names:
        result = load_json(folder / f"{name}.result.json") or {}
        inventory = load_json(folder / f"{name}.inventory.json") or [{}]
        verify_file = folder / f"{name}.verify.txt"
        verify = "-"
        if verify_file.exists():
            m = re.search(r"Result: (.+?)\s+\(", verify_file.read_text(encoding="utf-8"))
            verify = m.group(1) if m else "?"
        stats = result.get("stats", {})
        last = (result.get("last_message") or "").strip().splitlines()
        rows.append({
            "source": name,
            "risk": inventory[0].get("risk_level", "-"),
            "bob_status": result.get("status", "not run"),
            "outcome": last[-1][:80] if last else "-",
            "verify": verify,
            "cost": stats.get("session_costs", ""),
            "tokens": stats.get("total_tokens", ""),
            "tool_calls": stats.get("tool_calls", ""),
            "seconds": round(stats["duration_ms"] / 1000) if stats.get("duration_ms") else "",
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--csv", action="store_true")
    args = ap.parse_args()
    if not args.folder.is_dir():
        print(f"error: {args.folder} is not a folder", file=sys.stderr)
        return 2

    rows = summarize(args.folder)
    if not rows:
        print("No results found.")
        return 0
    cols = list(rows[0].keys())
    if args.csv:
        w = csv.DictWriter(sys.stdout, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
        return 0

    print(f"# Batch results: {args.folder}\n")
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r[c]).replace("|", "/") for c in cols) + " |")
    total = sum(float(r["cost"]) for r in rows if str(r["cost"]).replace(".", "", 1).isdigit())
    passed = sum(1 for r in rows if r["verify"].startswith("PASS"))
    print(f"\n**{passed}/{len(rows)} passed verification. Total cost: {total:.2f} Bobcoins.**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
