#!/usr/bin/env bash
# ci-review.sh — AI code review gate for IBM i sources changed on a branch.
#
#   BOB_API_KEY=... ./ci-review.sh [BASE_REF]        (default BASE_REF: origin/main)
#
# Runs Bob in the read-only ibmi-reviewer mode (edit and execute tool groups disabled),
# writes reviews/ci-review.md, and exits 1 if any CRITICAL finding is reported.
set -euo pipefail

BASE_REF="${1:-origin/main}"
MAX_COST="${MAX_COST:-3}"
OUT_DIR="reviews"
mkdir -p "$OUT_DIR"

mapfile -t files < <(git diff --name-only --diff-filter=ACMR "$BASE_REF"...HEAD -- \
  '*.rpgle' '*.sqlrpgle' '*.rpgleinc' '*.clle' '*.cmd' '*.sql' '*.table' '*.view' |
  grep -v '^qrpglesrc/legacy/' || true)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No IBM i sources changed — nothing to review."
  exit 0
fi

refs=""
for f in "${files[@]}"; do refs+=" @$f"; done

prompt="Review these changed IBM i sources:$refs

Use the shop checklist in .bob/rules-ibmi-reviewer/01-review-checklist.md.
Do not modify any files and do not run commands. Return the full review as Markdown in your final message.
The first line of your final message must be exactly: VERDICT: <APPROVE|APPROVE WITH CHANGES|REQUEST CHANGES> CRITICAL=<n> HIGH=<n>"

bob run --mode ibmi-reviewer \
        --disable-tool-groups edit,execute \
        --max-cost "$MAX_COST" --max-turns 30 \
        --format json --trust --accept-license \
        "$prompt" > "$OUT_DIR/ci-review.json"

python3 - "$OUT_DIR/ci-review.json" "$OUT_DIR/ci-review.md" <<'PY'
import json, re, sys
result = json.load(open(sys.argv[1]))
if result.get("status") != "success":
    print("Bob review did not complete:", result.get("last_message", "")[:500]); sys.exit(2)
text = result.get("last_message", "")
open(sys.argv[2], "w").write(text)
m = re.search(r"VERDICT:\s*(.+?)\s+CRITICAL=(\d+)\s+HIGH=(\d+)", text)
if not m:
    print("Could not find the VERDICT line; failing safe."); sys.exit(1)
verdict, critical, high = m.group(1), int(m.group(2)), int(m.group(3))
cost = result.get("stats", {}).get("session_costs")
print(f"Verdict: {verdict}  CRITICAL={critical}  HIGH={high}  cost={cost}")
sys.exit(1 if critical > 0 else 0)
PY
