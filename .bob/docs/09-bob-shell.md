# 09 · Bob Shell: using `.bob` from the command line

[Docs home](../README.md) · [← 08 Hooks](08-hooks.md) · Next: [10 IBM i workflows →](10-ibmi-workflows.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 2.7, 3.5, 5.2. Exam-focused notes: [Section 2](exam/section-2-core-features.md) · [Section 3](exam/section-3-use-cases.md) · [Section 5](exam/section-5-accounts.md).

## In plain English
**Bob Shell** is Bob in your terminal. It reads **the same `.bob` folder** as the IDE,
so rules, modes, skills, commands, MCP servers and hooks all behave identically. It's
also how you put Bob into **scripts and CI pipelines**: convert 200 programs overnight,
or review every pull request automatically.

## Install and sign in
```bash
# macOS / Linux (needs Node.js 24+)
curl -fsSL https://bob.ibm.com/download/bobshell.sh | bash

bob                      # interactive session; opens the browser for IBMid sign-in
```
For scripts and CI, create an **API key** (scope *Inference*) in the Bob portal and
`export BOB_API_KEY=...`. `bob run` requires it.
[Install and setup](https://bob.ibm.com/docs/shell/getting-started/install-and-setup) ·
[API keys](https://bob.ibm.com/docs/shell/account/api-keys)

## Interactive: the everyday commands
| Type | To |
|---|---|
| `/` | see every command: built-in, ours (`/convert-to-free`…), and modes (`/modernizer`…) |
| `/mode` | pick a mode |
| `/skills` | insert a skill reference into your prompt |
| `/mcp`, `bob mcp list` | manage / list MCP servers |
| `/hooks` | view and toggle hooks |
| `/manage-secrets set KEY VALUE` | store a secret for `${KEY}` in `mcp.json` |
| `/init` | generate `AGENTS.md` and starter rules for a new repo |
| `/compact` | shrink the conversation when it gets long |
| `/resume` | go back to an earlier conversation |
| `@path/to/file` | attach a file to your prompt |

## Scripted: `bob run`
```bash
bob run "Explain @qrpglesrc/custinq.pgm.rpgle"            # one-shot
cat prompt.txt | bob run                                  # prompt from a file
bob run --mode modernizer "..."                           # start in a custom mode
bob run --format json "..." > result.json                 # machine-readable result
```

| Option | Why you want it in automation |
|---|---|
| `--mode <slug>` | Use one of the custom modes, with its file restrictions and rules |
| `--format json` / `stream-json` | Parse the result: `status`, `last_message`, `stats.session_costs`… |
| `--max-cost <bobcoins>` / `--max-turns <n>` | Hard spending and runaway limits |
| `--disable-tool-groups edit,execute` | Make a run read-only regardless of mode |
| `--disable-mcp` | Don't start MCP servers (faster, no IBM i needed) |
| `--resume <task-id>` / `--resume latest` | Continue a task |
| `--trust --accept-license` | First run on a fresh CI machine |

> ⚠️ **`bob run` pre-approves every tool call.** Nobody is there to click "Reject".
> Always combine it with `--max-cost`, `--max-turns`, a restricted `--mode` and/or
> `--disable-tool-groups`, and keep the hooks ([08](08-hooks.md)) in place.

## The automation examples in this repo
All are in [`skills/bob-shell-automation/`](../skills/bob-shell-automation/SKILL.md):

| File | What it shows |
|---|---|
| [`scripts/batch-convert.sh`](../skills/bob-shell-automation/scripts/batch-convert.sh) | One bounded `bob run --mode modernizer` **per source file**, then `verify_conversion.py` checks each result. Try `DRY_RUN=1` first |
| [`examples/prompts/convert.txt`](../skills/bob-shell-automation/examples/prompts/convert.txt) | Prompt template with `{SOURCE}`, `{TARGET}`, a required one-line final answer |
| [`scripts/ci-review.sh`](../skills/bob-shell-automation/scripts/ci-review.sh) | Read-only review of changed files (`--mode ibmi-reviewer --disable-tool-groups edit,execute`); fails the build on CRITICAL |
| [`scripts/summarize_results.py`](../skills/bob-shell-automation/scripts/summarize_results.py) | Turns the JSON results into a Markdown/CSV table with cost per file |
| [`examples/github-actions.yml`](../skills/bob-shell-automation/examples/github-actions.yml) | Pull-request pipeline: free static check, then the AI review gate |

The design rules behind them:
1. **Behaviour lives in `.bob/`, not in the script.** The prompt says "follow the
   rpg-fixed-to-free skill", so improving the skill improves the batch job.
2. **One unit of work per `bob run`.** Small contexts, per-file cost, easy retries.
3. **Verify with code, not by trusting text.** A script decides pass or fail.

## Try it
```bash
# See what would be converted, without calling Bob (no cost):
DRY_RUN=1 bash .bob/skills/bob-shell-automation/scripts/batch-convert.sh qrpglesrc/legacy

# One real, capped conversion:
bob run --mode modernizer --max-cost 1 --max-turns 30 \
  "Convert qrpglesrc/legacy/custinq.pgm.rpgle to free format. Follow the rpg-fixed-to-free skill."
```

**Docs:** [Bob Shell](https://bob.ibm.com/docs/shell) ·
[Interactive sessions](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-interactive) ·
[Non-interactive sessions (`bob run`)](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive) ·
[Usage examples](https://bob.ibm.com/docs/shell/getting-started/bobshell-examples) ·
[Best practices](https://bob.ibm.com/docs/shell/getting-started/best-practices) ·
[Slash commands](https://bob.ibm.com/docs/shell/features/slash-commands) ·
[Context window management](https://bob.ibm.com/docs/shell/core-concepts/context-window-management)
