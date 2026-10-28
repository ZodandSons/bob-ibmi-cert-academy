#!/bin/sh
# =============================================================================
# test-hooks.sh — try every hook WITHOUT starting Bob
# =============================================================================
# Hooks are ordinary programs: Bob writes a JSON payload to their stdin and
# reads their exit code (0 = allow, 2 = block). This script does the same thing
# with sample payloads so you can see, and safely change, what each hook does.
#
#   Run from the repository root:   sh .bob/hooks/test-hooks.sh
#
# Docs:  https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide: .bob/docs/08-hooks.md
# =============================================================================

pass=0; fail=0

check() {   # check <expected-exit> <hook-command> <json-payload> <label>
  expected=$1; hook=$2; payload=$3; label=$4
  printf '%s' "$payload" | $hook >/dev/null 2>/tmp/bob-hook-test.$$
  actual=$?
  if [ "$actual" = "$expected" ]; then
    pass=$((pass+1)); result="ok  "
  else
    fail=$((fail+1)); result="FAIL"
  fi
  verdict=$([ "$actual" = 2 ] && echo "BLOCK" || echo "allow")
  printf '%s %-5s %s\n' "$result" "$verdict" "$label"
  [ "$actual" = 2 ] && sed 's/^/           /' /tmp/bob-hook-test.$$
  rm -f /tmp/bob-hook-test.$$
}

echo "== PreToolUse: guard-dangerous-commands.py (matcher ^execute_command\$)"
G="python3 .bob/hooks/guard-dangerous-commands.py"
check 0 "$G" '{"tool":"execute_command","input":{"command":"makei c -f qrpglesrc/custinq.pgm.rpgle"}}' "compile one program"
check 2 "$G" '{"tool":"execute_command","input":{"command":"system \"DLTLIB LIB(ORDDEV01)\""}}' "delete a library"
check 2 "$G" '{"tool":"execute_command","input":{"command":"python3 x.py \"SELECT * FROM ORDPRD.CUSTMAST\""}}' "touch a PROD library"
check 2 "$G" '{"tool":"execute_command","input":{"command":"db2 \"DELETE FROM ORDDEV01.WORK\""}}' "DELETE without WHERE"
check 0 "$G" '{"tool":"execute_command","input":{"command":"db2 \"DELETE FROM ORDDEV01.WORK WHERE ID = 3\""}}' "DELETE with WHERE"

echo "== PreToolUse: protect-paths.py (matcher write_to_file|apply_diff|...)"
P="python3 .bob/hooks/protect-paths.py"
check 0 "$P" '{"tool":"write_to_file","input":{"path":"qrpglesrc/custinq.pgm.rpgle"}}' "write converted source"
check 2 "$P" '{"tool":"apply_diff","input":{"path":"qrpglesrc/legacy/custinq.pgm.rpgle"}}' "edit legacy original"
check 2 "$P" '{"tool":"write_to_file","input":{"path":".bob/settings.json"}}' "edit hook config"
check 2 "$P" '{"tool":"write_to_file","input":{"path":".env"}}' "write credentials file"

echo "== UserPromptSubmit: block-secrets.py"
S="python3 .bob/hooks/block-secrets.py"
check 0 "$S" '{"prompt":"Convert CUSTINQ to free format"}' "normal prompt"
check 2 "$S" '{"prompt":"connect with password=Secret123"}' "prompt containing a password"

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
