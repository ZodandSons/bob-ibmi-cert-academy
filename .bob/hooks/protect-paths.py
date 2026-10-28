#!/usr/bin/env python3
# Hook event : PreToolUse (matcher write_to_file|apply_diff|insert_content|...) — exit 2 BLOCKS the write
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
"""PreToolUse hook: stop Bob from writing to protected paths.

- qrpglesrc/legacy/  original fixed-format sources kept for comparison
- .bob/hooks/ and .bob/settings.json  Bob must not edit its own guard rails
- .env files  credentials
"""
import json
import re
import sys

PROTECTED = [
    (r"(^|/)qrpglesrc/legacy/", "original legacy sources are read-only; write the converted file to qrpglesrc/"),
    (r"(^|/)\.bob/hooks/", "hook scripts can only be changed by a human"),
    (r"(^|/)\.bob/settings\.json$", "hook configuration can only be changed by a human"),
    (r"(^|/)\.env(\.[^/]*)?$", "credential files are off-limits"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = payload.get("input", {}) or {}
    path = str(tool_input.get("path") or tool_input.get("file_path") or "").replace("\\", "/")
    if path.endswith(".env.example"):
        return 0
    for pattern, reason in PROTECTED:
        if re.search(pattern, path):
            print(f"Blocked write to {path}: {reason}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
