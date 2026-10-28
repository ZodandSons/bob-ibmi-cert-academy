#!/usr/bin/env python3
# Hook event : UserPromptSubmit — exit 2 BLOCKS the prompt
# Wired up in: .bob/settings.json   Test it: sh .bob/hooks/test-hooks.sh
# Docs       : https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks
# Guide      : .bob/docs/08-hooks.md
"""UserPromptSubmit hook: block prompts that contain credentials.

stdin:  {"event": "UserPromptSubmit", "session_id": "...", "prompt": "..."}
exit 2: block the prompt (message on stderr is shown to the user)
exit 0: allow; anything on stdout is added to the model's context
"""
import json
import re
import sys

PATTERNS = [
    (r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+", "a password"),
    (r"(?i)\bDB2i_PASS\s*=\s*\S+", "the Db2 for i password"),
    (r"(?i)\bBOB_API_KEY\s*=\s*\S+", "a Bob API key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"(?i)\bSIGNON\b.*\bPASSWORD\(", "an IBM i sign-on password"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # never break Bob because of a malformed payload
    prompt = payload.get("prompt", "")
    for pattern, label in PATTERNS:
        if re.search(pattern, prompt):
            print(
                f"Prompt blocked: it appears to contain {label}. "
                "Store secrets with /manage-secrets or environment variables instead.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
