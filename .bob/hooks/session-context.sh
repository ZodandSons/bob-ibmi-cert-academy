#!/bin/sh
# Hook event : SessionStart — stdout is ADDED to Bob's context
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
# SessionStart hook: stdout is injected into Bob's context at the start of every session.
# Keep it short — this costs tokens on every session.

echo "## Session context (from .bob/hooks/session-context.sh)"
echo "- Project: $(basename "$PWD")"
echo "- Git branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'not a git repo')"
echo "- Build target library: ${IBMI_DEVLIB:-not set (export IBMI_DEVLIB=ORDDEVxx)}"
echo "- IBM i host: ${DB2i_HOST:-not configured (export DB2i_HOST=...)}"

# Count fixed-format vs free-format RPG sources so Bob knows the modernization state.
fixed=0; free=0
for f in $(find qrpglesrc -type f \( -iname '*.rpgle' -o -iname '*.sqlrpgle' \) 2>/dev/null); do
  if head -n 1 "$f" | grep -qi '^\*\*free'; then free=$((free+1)); else fixed=$((fixed+1)); fi
done
echo "- RPG sources: ${free} fully free, ${fixed} fixed or mixed format"

# Surface uncommitted work so Bob doesn't overwrite it.
changed=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
[ "$changed" != "0" ] && echo "- Uncommitted changes: ${changed} file(s) — check before editing"
exit 0
