# 00 · What is IBM Bob, and what is the `.bob` folder?

[Docs home](../README.md) · Next: [01 Getting started →](01-getting-started.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 2.5, 2.8, 2.9, 2.14, 3.4. Exam-focused notes: [Section 2](exam/section-2-core-features.md) · [Section 3](exam/section-3-use-cases.md).

## IBM Bob in one paragraph

**IBM Bob** is IBM's AI coding assistant. You describe a task in plain English
("convert CUSTINQ to free format", "why did last night's batch job fail?") and Bob
reads your code, plans, edits files and runs commands to get it done — asking your
permission along the way. It comes in two forms that share the same configuration:

| | **Bob IDE** | **Bob Shell** |
|---|---|---|
| What | A full editor (VS Code based) with a Bob chat panel | A command-line tool: `bob` |
| Good for | Day-to-day development | Terminal work, scripting, CI/CD pipelines |
| Start | Open the app, open your repo folder | `bob` (interactive) or `bob run "..."` (scripted) |
| Docs | [bob.ibm.com/docs/ide](https://bob.ibm.com/docs/ide) | [bob.ibm.com/docs/shell](https://bob.ibm.com/docs/shell) |

## The `.bob` folder in one paragraph

Out of the box, Bob knows nothing about *your* shop: your library names, your coding
standards, that `ORDPRD` must never be touched, or how you convert fixed-format RPG.
The **`.bob` folder** is where you teach it. It sits in the root of your git repository,
it is plain text, and because it is committed, **every engineer who clones the repo gets
the same Bob behaviour**. Each developer can also keep personal settings in `~/.bob/`
in their home folder; the project folder wins when both define the same thing.

## The pieces, with an analogy

Think of Bob as a capable new contractor joining your IBM i team.

| `.bob` piece | Analogy | What it does | Guide |
|---|---|---|---|
| `AGENTS.md` (repo root) | The project briefing | Big-picture map of the system, loaded every time | [02](02-agents-md-and-bobignore.md) |
| `.bobignore` (repo root) | "Do not open" drawer labels | Files Bob may not read or edit | [02](02-agents-md-and-bobignore.md) |
| `rules/` | The shop's standards manual | Short, always-on rules for every conversation | [03](03-rules.md) |
| `custom_modes.yaml` | Job roles with keycards | Personas (RPG dev, reviewer…) with limited tool access | [04](04-custom-modes.md) |
| `rules-{mode}/` | Role-specific instructions | Extra rules only for one mode | [03](03-rules.md) |
| `skills/` | Recipe binders on the shelf | Detailed how-tos Bob pulls out only when relevant | [05](05-skills.md) |
| `commands/` | Saved work orders | Reusable prompts you trigger with `/name` | [06](06-slash-commands.md) |
| `mcp.json` + `mcp-tools/` | A phone line to the system | Lets Bob query IBM i live (read-only here) | [07](07-mcp-servers.md) |
| `settings.json` + `hooks/` | Security guard at the door | Scripts that check, log or block Bob's actions | [08](08-hooks.md) |

> **Our own additions.** `docs/` (these guides), `mcp-tools/` and `hooks/` are folder
> names *we* chose. Bob does not load them by itself — they are used only because other
> files point to them (`mcp.json` → `mcp-tools/`, `settings.json` → `hooks/`).

## How a request flows through the `.bob` folder

```
 You type: "Convert qrpglesrc/legacy/custinq.pgm.rpgle to free format"
   │
   ├─ hooks: UserPromptSubmit ─ block-secrets.py checks the prompt  ── could BLOCK
   │
   ▼
 Bob builds its context (every message):
   • rules for the current mode   (.bob/rules-modernizer/*.md)
   • AGENTS.md                    (repo root)
   • general rules                (.bob/rules/*.md)
   • the mode's role + custom instructions  (custom_modes.yaml)
   • the list of skills (names + descriptions only)
   │
   ▼
 Bob decides a skill fits ──► loads .bob/skills/rpg-fixed-to-free/SKILL.md
   │                         (and reads its reference files as needed)
   ▼
 Bob uses tools — each one passes these gates:
   1. Does the MODE allow this tool group / file?  (custom_modes.yaml groups + fileRegex)
   2. Is the file hidden by .bobignore?
   3. hooks: PreToolUse ─ guard-dangerous-commands.py / protect-paths.py ── could BLOCK
   4. Your approval (unless auto-approve is on, or you're using `bob run`)
   │
   ├─ MCP tools: where_used, table_columns ... ─► IBM i MCP server ─► Db2 for i
   │
   ├─ hooks: PostToolUse ─ log-activity.sh records what happened
   ▼
 Task finished ─ hooks: Stop ─ session-summary.sh records changed files
```

## Built-in modes

Bob ships with three modes. Custom modes ([04](04-custom-modes.md)) add more.

| Mode | Slug | What it can do |
|---|---|---|
| **Agent** | `agent` | Everything: read, edit, run commands, MCP, skills, subagents |
| **Plan** | `plan` | Read, write plans, MCP, skills — no commands |
| **Ask** | `ask` | Read-only questions and explanations |

Switch modes with the dropdown next to the chat box, **⌘ + .** (macOS) or **Ctrl + .**
(Windows/Linux), or `/mode` in Bob Shell. Source: [Modes](https://bob.ibm.com/docs/ide/features/modes).

## Where to go next

1. [01 Getting started](01-getting-started.md): install Bob and check that this folder loads.
2. Read guides 02–08 in order; each is a 5–10 minute read with a "Try it" section.
3. [10 IBM i workflows](10-ibmi-workflows.md) shows the pieces working together on real tasks.
4. Preparing for **IBM certification C3000-006**? Follow the [certification track](exam/README.md).
5. Stuck? [11 Troubleshooting](11-troubleshooting.md). Unknown term? [12 Glossary](12-glossary.md).
   All links are collected in [13 Reference links](13-reference-links.md).
