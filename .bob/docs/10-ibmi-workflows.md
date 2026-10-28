# 10 · IBM i workflows: every piece working together

[Docs home](../README.md) · [← 09 Bob Shell](09-bob-shell.md) · Next: [11 Troubleshooting →](11-troubleshooting.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 2.9, 3.1, 3.3, 3.4, 3.8, 3.10, 3.11. Exam-focused notes: [Section 2](exam/section-2-core-features.md) · [Section 3](exam/section-3-use-cases.md).

Each walkthrough lists what you do, then which `.bob` pieces are involved and why.

## A. Convert a fixed-format program to free format

**You:** copy the original to `qrpglesrc/legacy/ordlist.pgm.rpgle`, then run
`/convert-to-free qrpglesrc/legacy/ordlist.pgm.rpgle` (ideally in 🔁 Fixed-to-Free Modernizer mode).

| Step | What Bob does | `.bob` piece |
|---|---|---|
| 1 | Expands your command into the full instructions | `commands/convert-to-free.md` |
| 2 | Already knows never to edit `legacy/` and never to touch PROD | `rules/03-safety…`, `rules-modernizer/01-…` |
| 3 | Activates the conversion recipe | `skills/rpg-fixed-to-free/SKILL.md` |
| 4 | Runs the inventory and shows you the risk level | `skills/…/scripts/inventory_fixed.py` |
| 5 | Converts spec by spec using the opcode table and pitfalls | `skills/…/reference/*.md`, `examples/` |
| 6 | Writes `qrpglesrc/ordlist.pgm.rpgle`; an attempt on `legacy/` is refused **twice** | mode `fileRegex` + `hooks/protect-paths.py` |
| 7 | Runs the verifier and fixes every ERROR | `skills/…/scripts/verify_conversion.py`, `rules-modernizer/02-verification.md` |
| 8 | Compiles | `skills/ibmi-build`, `makei` |
| 9 | Writes `conversions/ORDLIST.md` | `skills/…/templates/conversion-report.md` |

**You then:** read the report's `TODO-CONV` items, compile and test, and commit both files.
For many programs at once, use `batch-convert.sh` ([09](09-bob-shell.md)).

## B. Review a change before it's merged

**You:** switch to 🔍 IBM i Reviewer and run `/review-ibmi qrpglesrc/ordentry.pgm.sqlrpgle`.

| What Bob does | `.bob` piece |
|---|---|
| Can read anything but write only `reviews/*.md`, and cannot run commands | `custom_modes.yaml` (`ibmi-reviewer`) |
| Classifies findings CRITICAL…LOW in a fixed format | `rules-ibmi-reviewer/01-review-checklist.md` |
| Checks SQLSTATE handling, commitment control, locks | `commands/review-ibmi.md`, `skills/sqlrpgle-db2` |
| Lists every program affected by the change | MCP `where_used` |

In CI the same review runs automatically through `ci-review.sh` and the GitHub Actions example.

## C. Write a new program

**You:** in 🟦 RPG Developer, run `/new-rpg-program ORDPRICE "Calculate the price of an order line with customer discounts"`.

Bob copies `skills/rpgle-free-format/templates/program.pgm.rpgle`, follows
`rules-rpg-dev/01-rpgle-style.md`, uses `skills/sqlrpgle-db2` for the SQL, adds a
`Rules.mk` line (`skills/ibmi-build`), creates a test from `skills/rpgunit-testing`, and
compiles with `/build`. It can only touch RPG-type files because of the mode's `fileRegex`.

## D. Find out why last night's batch job failed

**You:** in 📊 IBM i Ops Analyst, ask *"Job 123456/QUSER/ORDNIGHT failed. Why?"*

Bob calls the MCP tool `recent_job_messages`, finds the first `*ESCAPE` message, and
explains it using the message table in `skills/ibmi-platform/reference/jobs-and-messages.md`.
The mode has no `edit` or `execute`, so it **cannot** change anything on the system,
even by accident.

## E. Build a small Python utility

**You:** in 🐍 Python Tools, ask *"Write a script that exports open orders to CSV for a date range."*

Bob follows `skills/ibmi-python` (credentials from the environment, parameter markers,
`--dry-run`), reusing patterns from `scripts/ibmi_tool.py`. The `block-secrets.py` hook
stops you from pasting a password into the chat by mistake.

---

### Which piece should I change?

| I want Bob to… | Change |
|---|---|
| always / never do something | a file in `rules/` ([03](03-rules.md)) |
| do something only in one role | `rules-{slug}/` or that mode's `customInstructions` ([03](03-rules.md), [04](04-custom-modes.md)) |
| be unable to touch certain files | the mode's `fileRegex`, a hook, and/or `.bobignore` ([04](04-custom-modes.md), [08](08-hooks.md), [02](02-agents-md-and-bobignore.md)) |
| know how to do a complex task | a skill ([05](05-skills.md)) |
| run a workflow when I type one word | a slash command ([06](06-slash-commands.md)) |
| see live IBM i data | an MCP tool ([07](07-mcp-servers.md)) |
| be stopped from doing something dangerous | a `PreToolUse` hook ([08](08-hooks.md)) |
| know facts about the system | `AGENTS.md` ([02](02-agents-md-and-bobignore.md)) |
