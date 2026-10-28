# C3000-006 cheat sheet: IBM Bob v2 Developer – Associate

[Exam home](README.md) · Read this the day before the exam.

## Weights
| § | Section | Weight |
|---|---|---|
| 1 | Concepts | 17% |
| 2 | **Bob core features** | **23%** |
| 3 | Use cases | 19% |
| 4 | Configuration | 17% |
| 5 | Accounts | 8% |
| 6 | Security | 16% |

## Where things live
| Thing | Project | Global |
|---|---|---|
| Rules | `.bob/rules/`, `.bob/rules-{slug}/` (legacy `.bobrules`, `.bobrules-{slug}`) | `~/.bob/rules/` · Windows `%USERPROFILE%\.bob\rules\` |
| AGENTS.md | workspace root; mode files in `.bob/rules-{agent\|plan\|ask}/` | — |
| Custom modes | `.bob/custom_modes.yaml` | `~/.bob/settings/custom_modes.yaml` |
| Skills | `.bob/skills/<name>/SKILL.md` | `~/.bob/skills/<name>/` |
| Slash commands | `.bob/commands/<name>.md` | `~/.bob/commands/` |
| MCP | `.bob/mcp.json` | `~/.bob/settings/mcp.json` (guide: `~/.bob/mcp.json`) |
| Hooks | `.bob/settings.json` | `~/.bob/settings/settings.json` |
| Ignore | `.bobignore` in workspace root | — |
| PR template | root → `docs/` → `.github/` → `.github/PULL_REQUEST_TEMPLATE/` → `PULL_REQUEST_TEMPLATE/` → `docs/PULL_REQUEST_TEMPLATE/` | — |

**Precedence:** project beats global (modes: project > global > built-in; skills, MCP names,
commands). **Rules load order:** global → workspace; within each, **mode-specific → AGENTS.md → general**;
alphabetical; recursive; empty files skipped; symlinks depth 5.

## How each piece activates
**Rules → always active · Modes → user · Skills → Bob (from description) · Hooks → events ·
AGENTS.md → always loaded.**
Modes = role + tool access · Skills = reusable workflows · Rules = behaviour/style ·
Hooks = lifecycle automation · AGENTS.md = durable project context.

## Modes
| Agent | Plan | Ask |
|---|---|---|
| write/modify/debug/run | design & plan, no commands | explain, **read-only** |
Workflow: **Plan → Agent → Ask**. Switch: dropdown · ⌘/Ctrl + . · `/mode` · Shift+Tab (Shell).
Custom mode parts: **slug, name, roleDefinition**, whenToUse, groups, customInstructions,
description, allowedSubagents. **No `groups` = no tools**; invalid `fileRegex` breaks loading;
slug = letters/numbers/hyphens, unique; YAML preferred (JSON auto-migrated).
Groups: `read edit execute mcp skill workflow todo subtask subagent mode`.

## Tools
Read `read_file glob grep list_files GetSymbolsOverview FindSymbol FindReferencingSymbols` ·
Write `write_file apply_diff insert_content search_and_replace` · `execute_command` ·
`spawn_subagent` (explore = read-only/lighter; general = full/default; `fork_context`) ·
`start_subtask` (title, message, todos, mode) · `use_mcp_tool` · `switch_mode` · `use_skill`
(once per conversation) · `start_workflow` · `update_todo_list` · `ask_followup_question`.
Loop: **select → present params → run approved → repeat.**

## Numbers
| | |
|---|---|
| Context cap per task | **270,000** tokens |
| Condensation begins | **~190,000** |
| Trivial-prompt baseline | **~8.5k** |
| MCP network timeout | **30 s – 5 min, default 1 min** |
| Hook timeout default | 10 s (exit **2** = block, only UserPromptSubmit & PreToolUse) |
| Bobcoin value | **$0.50** (enterprise pack 1,000 = $500, 1-year expiry) |
| Plans (Bobcoins/month) | Trial 50 · Pro 50 · Pro+ 180 · Ultra 1,000 |
| PR base-branch suggestions | **3** |

## Context window (6 categories)
**System prompt · Tool definitions · MCP tools · Rules · Skills · Messages.**
Flat: system prompt, tool definitions. Grow when added: MCP tools, rules. Mid-thread: skills.
Every turn: **messages (largest)**. Condensation is **lossy**. Every prompt **re-sends the whole
active context**, so later prompts cost more.

## @ mentions
`@file` (+`:10-20`) · `@folder` (**non-recursive**) · `@problems` · `@terminal` ·
`@<hash>` · `@git-changes` · `@https://url`. **File/folder bypass .bobignore & .gitignore.
Git mentions respect .gitignore.**

## MCP
JSON-RPC 2.0, client-server, "USB-C". STDIO: `command`* args cwd env alwaysAllow disabled
(child process, local, no network, 1:1). Streamable HTTP: `url`* headers alwaysAllow disabled,
`"type":"streamable-http"` (remote, many clients). SSE = legacy remote. No servers pre-installed.
Settings → MCP: **Use MCP Servers** toggle, **Enable MCP Server Creation**, per-tool enable,
**Always allow**. Prefer local STDIO for confidential data; never hardcode credentials.

## Security
Risk: **Edit, Execute = high · MCP = medium-high · Read, Skill = medium ·
Todo, Subtask, Subagent, Mode = low.** Task permissions = **current task only.**
Suspicious approval → **deny, find what widened scope, ask for narrower.**
Secrets → approved secrets store, provided at runtime. Never in chat.
`.bobignore`: root, gitignore syntax, checked by read_file/write_file/apply_diff/symbols,
auto-reloads, implicitly ignored itself, **not a sandbox**, execute_command only for known
file-reading commands, guide: insert_content/search_and_replace may slip through.
**Rollback:** shadow Git repo; snapshots **at task start and before file edits, not before
terminal commands**; Restore files (keep chat) vs Restore files **and task** (irreversible);
misses changes outside Bob tasks; unsaved work can be overwritten.

## Accounts
API keys: **General** (instance-wide; needs **team ID**) vs **Inference** (one team, inference
only). Shown once. Users manage own keys; admins list/revoke any in their instance.
Enterprise: teams/roles, shared Bobcoin pools, spending limits, seats, Bobalytics, **SSO SAML/OIDC**.
Bobalytics: Admin → Bobalytics; Adoption rate, **Bob factor** (% committed lines by Bob), Bobcoin
spend; team views anonymized, admins can't see an individual from team charts.
Usage: hover **gauge** (top-right) · Settings → **General** · Bobalytics.
**SaaS users can't choose the LLM**: routing by complexity, capability, context size, cost.

## Architecture
**Agent** (reasoning + code generation) · **Harness** (runtime: auth, logging, telemetry, tool loop) ·
**Clients** (IDE, Shell…). One agent, one harness, many clients.

## IDE features
Code actions: lightbulb · right-click → Bob · ⌘/Ctrl + . → Add to Context, Explain, Improve,
Inline Chat (⌘/Ctrl + K), Move to Chat (⌘/Ctrl + L).
Literate coding: ⌘/Ctrl + I, write instructions, ⌘/Ctrl + Enter, inline diff accept/reject.
**Single file → literate coding; multi-file → Agent.**
Review: Review panel or `/review` → comparison branch → Include Uncommitted Changes → issue
coverage (GitHub) → Bob Findings → Fix with Bob / Dismiss → exclusions in Settings → Bob Findings.
PRs: needs commit + push access; PR icon / palette / chat command.
Premium packages: Java Modernization, Z, i. Notification → Install; Extensions → Update;
Install from VSIX…. Bob Shell companion: `/ide install|enable|disable|status`.

## Bob Shell
`bob chat` (interactive) · `bob run` (non-interactive, `BOB_API_KEY`) · `!` = shell mode ·
`--max-cost --max-turns --mode --format json --disable-tool-groups --disable-mcp --resume --team-id`.
IDE = editing, literate coding, visual review. Shell = terminal, scripts, CI/CD, logs.

## Docs vs exam guide: known wording differences
| Topic | Exam guide | Current docs | What to do |
|---|---|---|---|
| Global MCP file | `~/.bob/mcp.json` | `~/.bob/settings/mcp.json` | Know both; concept = global vs project |
| Agent mode rules folder | `.bob/rules-agent/` | `/init` tutorial: `.bob/rules-code/AGENTS-code.md` | "Code" was the v1 name for Agent |
| Skills availability | "Agent mode" (1.4) / "only Advanced mode" (4.7) | Agent, Plan, Ask list Skill group | Advanced = v1 name of the full-tool mode |
| PR chat command | `/create-pr`, "Bob: Generate PR" | `/create-pull-request`, "Bob: Create Pull Request" | Recognize either |
| Findings in chat | `@issues` | `@problems` | Recognize either |
| Bobalytics tabs | Today, Patterns | Metrics, Insights, Today, My board | Recognize either |
| Shell auto-approve key | — | Ctrl+Y (interactive page) / Ctrl+F or Alt+F (shortcuts page) | Not exam-critical |
