#!/bin/sh
# Hook event : PostToolUse (no matcher = every tool) — cannot block; output ignored
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
# PostToolUse hook: append each tool call as one JSON line to .bob/logs/activity.jsonl.
# The payload includes tool name, input and output. Output is trimmed to keep the log small.
# .bob/logs/ is listed in .bobignore and should be in .gitignore.

mkdir -p .bob/logs
python3 -c '
import json, sys, datetime
p = json.load(sys.stdin)
p["output"] = str(p.get("output", ""))[:500]
p["logged_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps(p))
' >> .bob/logs/activity.jsonl 2>/dev/null
exit 0
