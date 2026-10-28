# 06 · Slash commands: `commands/`

[Docs home](../README.md) · [← 05 Skills](05-skills.md) · Next: [07 MCP servers →](07-mcp-servers.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 1.1, 3.3. Exam-focused notes: [Section 1](exam/section-1-concepts.md) · [Section 3](exam/section-3-use-cases.md).

## In plain English
A **slash command** is a saved prompt. Instead of typing the same eight-line request
every time you convert a program, you type `/convert-to-free qrpglesrc/legacy/x.rpgle`.
Commands make good practice the easy path, and the whole team runs the same workflow.

## Where they live
| Folder | Scope |
|---|---|
| `.bob/commands/<name>.md` | This project |
| `~/.bob/commands/<name>.md` | You, in every project |

**The file name is the command name:** `review-ibmi.md` → `/review-ibmi`. Project
commands override global ones with the same name. Commands work the same in the IDE
and in Bob Shell.

## Anatomy of a command
```markdown
---
description: Convert a fixed-format RPG source to fully free format   <- shown in the / menu
argument-hint: <legacy-source-file>                                  <- grey hint after the name
---
Convert `$1` from fixed-format RPG to fully free-format RPG IV.      <- the prompt Bob receives
                                                                        $1 = first word you type,
Follow the `rpg-fixed-to-free` skill exactly: ...                       $2 = second word ...
```

Both front matter fields are optional. A plain Markdown file with just the prompt works too.

> ⚠️ Every `.md` file in `commands/` becomes a command, including a README. That's why
> this documentation lives in `.bob/docs/`.

## The nine commands in this repo

| Command | Arguments | What it does | Builds on |
|---|---|---|---|
| [`/convert-to-free`](../commands/convert-to-free.md) | `<source-file>` | Inventory → convert → verify → compile → report | `rpg-fixed-to-free` skill |
| [`/review-ibmi`](../commands/review-ibmi.md) | `<file-or-folder>` | Structured review, written to `reviews/` | `rules-ibmi-reviewer/`, MCP `where_used` |
| [`/new-rpg-program`](../commands/new-rpg-program.md) | `<NAME> <purpose>` | Scaffold from the template, add build rule and test | `rpgle-free-format`, `ibmi-build`, `rpgunit-testing` |
| [`/new-cl-program`](../commands/new-cl-program.md) | `<NAME> <purpose>` | Scaffold CLLE (and optional `*CMD`) | `clle-programming` |
| [`/explain-program`](../commands/explain-program.md) | `<source-file>` | Plain-English walkthrough, no changes | inventory script |
| [`/where-used`](../commands/where-used.md) | `<OBJECT> [LIBRARY]` | Impact analysis: live system plus source search | MCP `where_used` |
| [`/build`](../commands/build.md) | `<file \| all>` | Compile with `makei`, fix errors, max 3 attempts | `ibmi-build` |
| [`/plan-ibmi-change`](../commands/plan-ibmi-change.md) | `<ticket> <change>` | Plan-mode plan; written with the **five prompt components** as headings | `rules-plan/`, MCP `where_used` |
| [`/impact-analysis`](../commands/impact-analysis.md) | `<OBJECT>` | Three parallel **subagents** write findings to `tmp/impact/`, then merge | subagents, MCP |

Notice the pattern: **commands stay short and point at skills and rules.** The detailed
know-how lives in one place (the skill), and the command is just the trigger.

## Commands vs. modes vs. skills

| | Slash command | Mode | Skill |
|---|---|---|---|
| Who triggers it | You, explicitly | You (or Bob suggests) | Bob, when the task matches |
| What it changes | Sends a prompt | Who Bob is and what it may touch | What Bob knows how to do |
| Example | `/review-ibmi qrpglesrc/` | 🔍 IBM i Reviewer | `rpg-fixed-to-free` |

Custom modes also appear in the `/` menu (`/modernizer` switches mode). Those can't be
overridden by a command file with the same name.

## Try it
1. Type `/` in the chat and find the commands with their argument hints.
2. Run `/explain-program .bob/skills/rpg-fixed-to-free/examples/custinq-fixed.pgm.rpgle`.
3. Create `.bob/commands/joblog.md`:
   ```markdown
   ---
   description: Explain why a batch job failed
   argument-hint: <job-number/user/name>
   ---
   Use the recent_job_messages MCP tool for job $1. Find the first escape message,
   explain the cause in plain English, and suggest a fix.
   ```
   Then run `/joblog 123456/QUSER/ORDNIGHT`.

## Tips and common mistakes
- Use `$1`, `$2` placeholders and an `argument-hint` so people know what to type.
- Start with a clear instruction, then numbered steps. Say what the final answer should look like.
- Names are slugified: lowercase, dashes, no special characters.
- Command not showing? It must be a `.md` file directly in `commands/`
  ([11 Troubleshooting](11-troubleshooting.md)).

**Docs:** [Slash commands](https://bob.ibm.com/docs/shell/features/slash-commands)
