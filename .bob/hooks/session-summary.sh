#!/bin/sh
# Hook event : Stop — cannot block; output ignored
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
# Stop hook: when Bob finishes, record which files changed so the developer can review
# them (and so CI or a teammate can see what a Bob session touched).

mkdir -p .bob/logs
session=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("session_id","unknown"))' 2>/dev/null)
{
  echo "=== Bob session ${session} ended $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  git status --porcelain 2>/dev/null || echo "(not a git repository)"
  echo
} >> .bob/logs/sessions.log
exit 0
