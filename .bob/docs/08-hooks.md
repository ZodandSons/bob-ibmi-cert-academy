# 08 · Hooks: `settings.json` and `hooks/`

[Docs home](../README.md) · [← 07 MCP servers](07-mcp-servers.md) · Next: [09 Bob Shell →](09-bob-shell.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 3.4, 4.1, 6.5, 6.6. Exam-focused notes: [Section 3](exam/section-3-use-cases.md) · [Section 4](exam/section-4-configuration.md) · [Section 6](exam/section-6-security.md).

## In plain English
Rules *ask* Bob to behave. **Hooks make sure.** A hook is a small script that Bob runs
automatically at set moments: when a session starts, when you send a prompt, before or
after it uses a tool, and when it finishes. A hook can **add information**, **record what
happened**, or **block an action** by exiting with code `2`.

## Where it lives
| File | Scope |
|---|---|
| `.bob/settings.json` → `"hooks"` | This project. Merged **on top of** global hooks |
| `~/.bob/settings/settings.json` → `"hooks"` | You, in every project. Always run |
| Group policy `EnforcedHooks` | Your organisation; admins can force hooks on everyone |

The scripts themselves can live anywhere. We keep them in `.bob/hooks/`. View and toggle
hooks in **Settings → Hooks** (IDE) or `/hooks` (Bob Shell).

## The five events

| Event | When | Can block? (exit 2) | What happens to stdout |
|---|---|---|---|
| `SessionStart` | Once, when a session begins | No | **Added to Bob's context** |
| `UserPromptSubmit` | Each prompt, before it's sent | **Yes**: prompt not sent | Added to Bob's context |
| `PreToolUse` | Before a matching tool runs | **Yes**: tool not run | Ignored |
| `PostToolUse` | After a matching tool ran | No | Ignored |
| `Stop` | When Bob finishes | No | Ignored |

**Exit codes:** `0` = OK · `2` = block (only the two events above) · anything else =
logged and ignored. **stderr** goes to Bob's log; for a block, it's the reason shown.

## How a hook receives information
Bob writes JSON to the script's **stdin**. For `PreToolUse`:
```json
{ "event": "PreToolUse", "session_id": "ses_01abc123",
  "tool": "execute_command",
  "input": { "command": "system \"DLTLIB LIB(ORDDEV01)\"" } }
```
`UserPromptSubmit` adds `"prompt"`. `PostToolUse` adds `"output"`.

## Anatomy of `settings.json`
```jsonc
{
  "hooks": {
    "PreToolUse": [                                     // event name
      {
        "matcher": "^execute_command$",                 // regex on the TOOL NAME (Pre/PostToolUse only)
        "hooks": [                                      // omit matcher = every tool
          {
            "type": "command",                          // the only type supported
            "command": "python3 .bob/hooks/guard-dangerous-commands.py",  // run from the repo root
            "timeout": 5                                // seconds (default 10, 0 = none)
          }
        ]
      }
    ]
  }
}
```
Tool names you'll match most: `execute_command` (shell), `write_to_file`, `apply_diff`,
`insert_content` (edits), `read_file`, `use_mcp_tool`. Full list: [Tools](https://bob.ibm.com/docs/shell/core-concepts/tools).

## The six hooks in this repo

| Event | Script | What it does |
|---|---|---|
| `SessionStart` | [`session-context.sh`](../hooks/session-context.sh) | Prints branch, target library, host, and how many RPG sources are fixed vs free. Bob starts every session knowing this |
| `UserPromptSubmit` | [`block-secrets.py`](../hooks/block-secrets.py) | Blocks prompts containing `password=…`, API keys or private keys |
| `PreToolUse` `^execute_command$` | [`guard-dangerous-commands.py`](../hooks/guard-dangerous-commands.py) | Blocks `DLTLIB`, `CLRPFM`, `DROP TABLE`, `DELETE` without `WHERE`, `rm -rf`, and anything naming a protected library (`PROTECTED_LIBS`, or the `BOB_PROTECTED_LIBS` env var) |
| `PreToolUse` edits | [`protect-paths.py`](../hooks/protect-paths.py) | Blocks writes to `qrpglesrc/legacy/`, `.bob/hooks/`, `.bob/settings.json`, `.env` |
| `PostToolUse` (all) | [`log-activity.sh`](../hooks/log-activity.sh) | Appends every tool call to `.bob/logs/activity.jsonl` (audit trail) |
| `Stop` | [`session-summary.sh`](../hooks/session-summary.sh) | Records `git status` to `.bob/logs/sessions.log` |

Why hooks matter most in **Bob Shell automation**: `bob run` pre-approves every tool
call. Hooks are the safety net that still applies ([09](09-bob-shell.md)).

Notice `protect-paths.py` stops Bob from editing its own hooks. Guard rails that the
guarded party can switch off aren't guard rails.

## Try it: no Bob needed
```bash
sh .bob/hooks/test-hooks.sh          # runs 11 sample payloads through the hooks
```
Or test one by hand, exactly as Bob would:
```bash
echo '{"tool":"execute_command","input":{"command":"CLRPFM ORDDEV01/WORK"}}' \
  | python3 .bob/hooks/guard-dangerous-commands.py; echo "exit=$?"
# Blocked by .bob/hooks/guard-dangerous-commands.py: destructive CL command CLRPFM ...
# exit=2
```
Then in Bob (Agent mode) ask it to *"run CLRPFM ORDDEV01/WORK"* and watch it get blocked.

**Exercise:** add your test library to `PROTECTED_LIBS` in `guard-dangerous-commands.py`,
add a matching line to `test-hooks.sh`, and run it.

## Tips and common mistakes
- **Hooks run with your full permissions.** Review them like production code.
- **Keep them fast:** they run on every prompt or tool call. The default timeout is 10s.
- **Fail open on bad input:** our scripts `return 0` if the JSON can't be parsed, so a
  hook bug never bricks Bob. Decide deliberately if you want the opposite.
- **Check tool names** in **Settings → Hooks** if a matcher never fires; they can differ between versions.
- `SessionStart` output costs tokens every session, so keep it to a few lines.
- Hooks can't rewrite the prompt or tool input. They can only add context, log, or block.

**Docs:** [Lifecycle hooks](https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks) ·
[Group policies (EnforcedHooks)](https://bob.ibm.com/docs/ide/security/group-policies) ·
[Tools and tool groups](https://bob.ibm.com/docs/shell/core-concepts/tools)
