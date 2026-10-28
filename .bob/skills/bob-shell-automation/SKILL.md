---
name: bob-shell-automation
description: Automate IBM i work with Bob Shell (the bob CLI) - non-interactive bob run jobs, batch fixed-to-free conversion across many sources, CI/CD code review gates, JSON output parsing, cost and turn limits. Use when writing shell scripts, pipelines or scheduled jobs that run Bob, or when asked how to use Bob Shell.
---

# Bob Shell automation

Bob Shell uses the same `.bob/` folder as the IDE — rules, custom modes, skills, slash
commands and MCP servers all apply. That is what makes these scripts consistent with
what developers see interactively.

## Files
| File | Purpose |
|------|---------|
| `scripts/batch-convert.sh` | Convert every fixed-format source in a folder, one `bob run` per file, then verify |
| `scripts/ci-review.sh` | Review the RPG/CL files changed in a branch; fail the build on CRITICAL findings |
| `scripts/summarize_results.py` | Turn `bob run --format json` result files into a Markdown/CSV summary |
| `examples/github-actions.yml` | Pipeline that runs the review gate on pull requests |
| `examples/prompts/convert.txt` | Prompt template used by `batch-convert.sh` |

## Bob Shell essentials
| Need | Command |
|------|---------|
| Interactive session | `bob` (or `bob chat`) |
| One-shot, scripted | `bob run "prompt"` — requires `BOB_API_KEY` in the environment |
| Prompt from a file | `cat prompt.txt \| bob run` |
| Start in a custom mode | `bob run --mode modernizer "..."` |
| Machine-readable result | `--format json` (one object) or `--format stream-json` (NDJSON events) |
| Spending guard rails | `--max-cost <bobcoins>` and `--max-turns <n>` |
| Make a run read-only | `--disable-tool-groups edit,execute` |
| Isolate from MCP | `--disable-mcp` |
| Continue a task | `--resume <task-id>` or `--resume latest` |
| CI first run | `--trust --accept-license` |
| Reference files | `@path/to/file` inside the prompt |
| List MCP servers | `bob mcp list` |

`bob run` pre-approves all tool calls. **That is why the hooks in `.bob/settings.json`
matter most in automation** — they still block destructive commands and protected paths.
Always combine automated runs with `--max-cost`, `--max-turns` and, where possible,
`--disable-tool-groups`.

The JSON result contains `status` (`success`/`error`), `last_message`, and `stats`
(`task_id`, tokens, `session_costs`, `tool_calls`, `duration_ms`).

## Writing a new automation

<Steps>
<Step>
Put the prompt in a file under `examples/prompts/` and reference skills by name
("Follow the rpg-fixed-to-free skill…") so behaviour lives in `.bob/`, not the script.
</Step>
<Step>
Run one `bob run` per unit of work (per source file), never one giant prompt — it keeps
each context small, lets you retry failures, and gives per-file cost.
</Step>
<Step>
Always use `--format json` and save each result to a file; check `status` and verify
outputs with deterministic scripts (e.g. `verify_conversion.py`), not by trusting text.
</Step>
<Step>
Set `--mode`, `--max-cost`, `--max-turns`, and disable tool groups the job does not need.
</Step>
<Step>
Summarize with `scripts/summarize_results.py` and exit non-zero on failure so CI notices.
</Step>
</Steps>
