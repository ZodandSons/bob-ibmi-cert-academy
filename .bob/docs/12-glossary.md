# 12 · Glossary

[Docs home](../README.md) · [← 11 Troubleshooting](11-troubleshooting.md) · Next: [13 Reference links →](13-reference-links.md)

---

## IBM Bob terms
| Term | Meaning |
|---|---|
| **IBM Bob** | IBM's AI coding assistant, available as Bob IDE and Bob Shell |
| **Bob IDE** | The desktop editor with the Bob chat panel |
| **Bob Shell** | The `bob` command-line tool; `bob run` for scripts and CI |
| **Workspace** | The folder opened in Bob. `.bob/`, `AGENTS.md` and `.bobignore` must be at its root |
| **Global config** | `~/.bob/...`: personal settings for every project. Project config wins on conflicts |
| **Mode** | A persona with a role and a set of allowed tools. Built in: Agent, Plan, Ask |
| **Slug** | A mode's id (`rpg-dev`). Used in `rules-{slug}/` and `/slug` |
| **Tool group** | A family of tools a mode can be granted: `read`, `edit`, `execute`, `mcp`, `skill`… |
| **fileRegex** | A regex limiting which files a mode's `edit` group may change |
| **Rule** | Always-on instruction file in `rules/` or `rules-{slug}/` |
| **AGENTS.md** | Project briefing file in the repo root, loaded every conversation |
| **Skill** | On-demand instructions plus files, in `skills/<name>/SKILL.md` |
| **Slash command** | Saved prompt in `commands/<name>.md`, run as `/name` |
| **MCP** | Model Context Protocol: the standard way to connect Bob to external tools and data |
| **MCP server** | A program exposing tools over MCP (here: IBM's IBM i MCP server) |
| **Hook** | A script Bob runs on an event; it can add context, log, or block (exit 2) |
| **`.bobignore`** | List of files Bob's file tools may not access |
| **Subagent** | A helper agent Bob spawns for a self-contained subtask |
| **Bobcoins** | Bob's usage currency; capped in scripts with `--max-cost` |
| **Auto-approve** | Settings that let Bob act without asking each time; task-level permissions apply to the current task only |
| **Agent / harness / clients** | Bob v2 architecture: the agent reasons and writes code; the harness provides auth, logging, telemetry and the tool loop; clients (IDE, Shell) are the interfaces |
| **`/init`** | Scans a project and generates `AGENTS.md` plus mode-specific AGENTS files |
| **Context window** | Everything sent to the model per prompt (270k cap): system prompt, tool definitions, MCP tools, rules, skills, messages |
| **Condensation** | Automatic, lossy summarizing of older messages from ~190k tokens |
| **Context poisoning** | Wrong or stale information that stays in the context and keeps misleading Bob; fix with a fresh task |
| **Subtask** | A visible, interactive child task thread (vs a silent subagent) |
| **Literate coding** | Writing natural-language instructions in the editor where code should go; Bob fills them in with an inline diff |
| **Code actions** | Editor shortcuts: Add to Context, Explain, Improve, Inline Chat, Move to Chat |
| **Rollback** | Task snapshots in a shadow Git repo, taken at task start and before file edits |
| **Bob Findings** | Results panel of the built-in code review (Fix with Bob / Dismiss) |
| **Bobalytics** | Enterprise usage analytics: adoption rate, Bob factor, Bobcoin spend |
| **Bob factor** | Share of committed lines of code created by Bob |
| **API key (General / Inference)** | Credentials for automation; General needs a team ID, Inference is team-scoped |
| **Premium package** | Optional paid add-on: Java Modernization, Z, or i |

## IBM i terms used in this example
| Term | Meaning |
|---|---|
| **RPGLE / RPG IV** | ILE RPG, IBM i's main business language. `.rpgle` source |
| **Fixed format** | Older RPG where meaning depends on the column (H, F, D, C, O, P specs) |
| **Free format / `**free`** | Modern RPG written like other languages; `**free` on line 1 means fully free |
| **SQLRPGLE** | RPG with embedded SQL (`exec sql`); needs the SQL precompiler |
| **CLLE** | ILE Control Language, for job control and batch drivers |
| **Service program (`*SRVPGM`)** | Shared library of procedures; exports controlled by binder source (`.bnd`) |
| **Library / library list** | IBM i's namespace for objects / the search path used to find them |
| **Activation group** | Runtime scope for a program's resources (files, overrides, commitment control) |
| **Indicator (`*IN01`–`*IN99`)** | Legacy numbered on/off flags; replaced by BIFs like `%found` in modern code |
| **BIF** | Built-in function, e.g. `%trim`, `%found`, `%dec` |
| **MONMSG** | CL's way of catching error messages |
| **Db2 for i** | The database built into IBM i |
| **QSYS2 services** | SQL views/functions for system information (`OBJECT_STATISTICS`, `JOBLOG_INFO`…) |
| **Mapepire** | IBM i database server (port 8076) used by the MCP server and `mapepire-python` |
| **TOBi (`makei`)** | *The Object Builder for i*, IBM's open-source IBM i build tool. Called *Better Object Builder* ("Bob") until 2025; renamed to avoid confusion with IBM Bob. Older articles still use the old name |
| **PASE** | The AIX-compatible runtime on IBM i where Python, Node and `makei` run |
| **RPGUnit (iRPGUnit)** | Unit-testing framework for RPG |
