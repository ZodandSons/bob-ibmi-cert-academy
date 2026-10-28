#!/usr/bin/env bash
# batch-convert.sh — convert every fixed-format RPG source in a folder with Bob Shell.
#
#   BOB_API_KEY=... ./batch-convert.sh [SOURCE_DIR] [TARGET_DIR]
#   defaults: qrpglesrc/legacy  ->  qrpglesrc
#
# Env:  MAX_COST (bobcoins per file, default 2)   MAX_TURNS (default 40)
#       DRY_RUN=1 to list what would be converted without calling Bob
#
# For each source: inventory -> bob run (modernizer mode) -> verify_conversion.py.
# Results land in .bob/logs/batch-<timestamp>/ and a summary.md is printed at the end.
set -euo pipefail

SRC_DIR="${1:-qrpglesrc/legacy}"
DST_DIR="${2:-qrpglesrc}"
MAX_COST="${MAX_COST:-2}"
MAX_TURNS="${MAX_TURNS:-40}"
SKILL_DIR=".bob/skills/rpg-fixed-to-free"
PROMPT_TEMPLATE=".bob/skills/bob-shell-automation/examples/prompts/convert.txt"
OUT_DIR=".bob/logs/batch-$(date +%Y%m%d-%H%M%S)"

[[ -d "$SRC_DIR" ]] || { echo "No such folder: $SRC_DIR" >&2; exit 2; }
if [[ -z "${DRY_RUN:-}" ]]; then
  command -v bob >/dev/null || { echo "Bob Shell (bob) is not installed" >&2; exit 2; }
  [[ -n "${BOB_API_KEY:-}" ]] || { echo "BOB_API_KEY must be set for bob run" >&2; exit 2; }
fi
mkdir -p "$OUT_DIR" conversions

shopt -s nullglob nocaseglob
converted=0; skipped=0; failed=0
for src in "$SRC_DIR"/*.rpgle "$SRC_DIR"/*.sqlrpgle; do
  file="$(basename "$src")"
  name="${file%%.*}"
  target="$DST_DIR/$file"

  if head -n 1 "$src" | grep -qi '^\*\*free'; then
    echo "skip  $file (already free)"; continue
  fi
  if [[ -f "$target" ]]; then
    echo "skip  $file (target exists: $target)"; continue
  fi

  python3 "$SKILL_DIR/scripts/inventory_fixed.py" "$src" --format json > "$OUT_DIR/$name.inventory.json"
  risk=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[0]["risk_level"])' "$OUT_DIR/$name.inventory.json")
  echo "----  $file  (risk: $risk)"
  [[ -n "${DRY_RUN:-}" ]] && continue

  sed -e "s|{SOURCE}|$src|g" -e "s|{TARGET}|$target|g" -e "s|{NAME}|$name|g" \
      "$PROMPT_TEMPLATE" > "$OUT_DIR/$name.prompt.txt"

  # One bounded, non-interactive Bob run per file. Hooks in .bob/settings.json still apply.
  if ! bob run --mode modernizer \
                --max-cost "$MAX_COST" --max-turns "$MAX_TURNS" \
                --disable-mcp --format json --trust --accept-license \
                < "$OUT_DIR/$name.prompt.txt" > "$OUT_DIR/$name.result.json"; then
    echo "FAIL  bob run failed for $file"; failed=$((failed+1)); continue
  fi

  # Never trust the model's word: verify deterministically.
  if [[ -f "$target" ]]; then
    if python3 "$SKILL_DIR/scripts/verify_conversion.py" "$src" "$target" > "$OUT_DIR/$name.verify.txt"; then
      echo "ok    $target"; converted=$((converted+1))
    else
      echo "FAIL  verification errors in $target (see $OUT_DIR/$name.verify.txt)"; failed=$((failed+1))
    fi
  else
    echo "skip  $file (Bob did not produce $target — see conversions/$name.md)"; skipped=$((skipped+1))
  fi
done

python3 .bob/skills/bob-shell-automation/scripts/summarize_results.py "$OUT_DIR" > "$OUT_DIR/summary.md" || true
echo
echo "Converted: $converted  Skipped: $skipped  Failed: $failed"
echo "Details:   $OUT_DIR/summary.md"
[[ $failed -eq 0 ]]
