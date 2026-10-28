# 03 · Rules: `rules/` and `rules-{mode}/`

[Docs home](../README.md) · [← 02 AGENTS.md and .bobignore](02-agents-md-and-bobignore.md) · Next: [04 Custom modes →](04-custom-modes.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 2.15, 3.4, 4.8. Exam-focused notes: [Section 2](exam/section-2-core-features.md) · [Section 3](exam/section-3-use-cases.md) · [Section 4](exam/section-4-configuration.md).

## In plain English
Rules are your shop's **non-negotiable standards**, written as short Markdown files. Bob
adds them to every message it sends to the model, so it never "forgets" them. Some rules
apply everywhere, and some only in one mode.

## Where they live

| Folder | Applies to | Example in this repo |
|---|---|---|
| `.bob/rules/` | **Every** mode | `01-project-context.md`, `02-ibmi-coding-standards.md`, `03-safety-and-change-control.md` |
| `.bob/rules-{slug}/` | Only the mode with that slug | `rules-rpg-dev/`, `rules-cl-dev/`, `rules-modernizer/`, `rules-ibmi-reviewer/` |
| `.bob/rules-agent/`, `rules-plan/`, `rules-ask/` | The **built-in** Agent, Plan and Ask modes | `AGENTS.md` in each (what `/init` generates) + `rules-plan/01-ibmi-planning.md` |
| `~/.bob/rules/`, `~/.bob/rules-{slug}/` | You personally, in every project | *(not in the repo)* |

Older single-file forms also work: `.bobrules` and `.bobrules-{slug}` in the workspace
root. If both a folder and a file exist, the folder wins.

## How Bob loads them
1. **Global** (`~/.bob/…`) loads before **workspace** (`.bob/…`). Workspace rules can
   override global ones.
2. Within each level: **mode-specific rules → AGENTS.md → general rules**.
3. Files in a folder load **alphabetically**. That's why they are numbered `01-`, `02-`…
4. Subfolders are read too. Empty files and temp files (`*.bak`, `*.log`, `.DS_Store`) are skipped.
5. A mode's rule files are combined with its `customInstructions` from `custom_modes.yaml`.

> ⚠️ **Everything** in a rules folder is sent to the model, including READMEs and notes.
> That's why the explanations for this example live in `.bob/docs/` and not inside `rules/`.

## The examples in this repo

| File | What it teaches | Why it's a rule (not a skill) |
|---|---|---|
| [`rules/01-project-context.md`](../rules/01-project-context.md) | Environments, file extension → object type table, 10-char names | Bob needs it for *any* IBM i task |
| [`rules/02-ibmi-coding-standards.md`](../rules/02-ibmi-coding-standards.md) | Headers, naming, `**free`, no indicators, SQLSTATE checks | Applies to all code in all modes |
| [`rules/03-safety-and-change-control.md`](../rules/03-safety-and-change-control.md) | Never touch PROD, no destructive commands, never edit `legacy/` | Must never be skipped |
| [`rules-rpg-dev/01-rpgle-style.md`](../rules-rpg-dev/01-rpgle-style.md) | RPG layout order, parameter passing, error handling | Only matters when writing RPG |
| [`rules-cl-dev/01-clle-style.md`](../rules-cl-dev/01-clle-style.md) | CLLE declarations, MONMSG, cleanup | Only matters when writing CL |
| [`rules-modernizer/01-conversion-guardrails.md`](../rules-modernizer/01-conversion-guardrails.md) | "Translate, don't redesign" | Only for conversions |
| [`rules-modernizer/02-verification.md`](../rules-modernizer/02-verification.md) | Done-checklist (verify script, compile, report) | Only for conversions |
| [`rules-ibmi-reviewer/01-review-checklist.md`](../rules-ibmi-reviewer/01-review-checklist.md) | Severity levels and report format | Only for reviews |
| [`rules-plan/01-ibmi-planning.md`](../rules-plan/01-ibmi-planning.md) | What every IBM i change plan must cover | Shows rules for a **built-in** mode |
| [`rules-agent/AGENTS.md`](../rules-agent/AGENTS.md), [`rules-plan/AGENTS.md`](../rules-plan/AGENTS.md), [`rules-ask/AGENTS.md`](../rules-ask/AGENTS.md) | Mode-specific AGENTS.md files, the way `/init` creates them | How to customize a **default** mode without a custom mode |
| [`rules/04-ddl-backward-compatibility.md`](../rules/04-ddl-backward-compatibility.md) | DB changes must be backward compatible | A project rule **scoped to subdirectories** (`qsqlsrc/`, `qddssrc/`), the monorepo pattern |

A typical rule, short and testable:

```markdown
# Safety and change control (non-negotiable)
1. Never run, generate for execution, or suggest running a command that changes
   production libraries (`ORDPRD`, `ORDDTA`) or any library ending in `PRD`.
```

## Rules vs. skills vs. AGENTS.md

| | Rules | Skills ([05](05-skills.md)) | AGENTS.md ([02](02-agents-md-and-bobignore.md)) |
|---|---|---|---|
| Loaded | Always | Only when the task matches | Always |
| Length | A few lines each | As long as needed, plus files | ~1 page |
| Content | "Always / never" | "Here's how, step by step" | "Here's the system" |
| Cost | Tokens on **every** request | Tokens only when used | Tokens on every request |

Rule of thumb: **if it's longer than a screen, or only needed sometimes, make it a skill.**

## Try it
1. Ask mode: *"What file extension should a new CL program have?"* The answer comes from `rules/01-…`.
2. Create `.bob/rules/99-test.md` containing `Always end your answers with "— Bob"`.
   Ask anything. Then delete the file.
3. Switch to **CL Developer** and ask *"What goes right after the DCLs?"* (global MONMSG,
   from `rules-cl-dev/`). Ask the same in **Ask** mode and compare.

## Tips and common mistakes
- **Be specific and checkable.** "Write good code" does nothing. "Check SQLSTATE after
  every SQL statement" works.
- **Explain the why in a few words** (e.g. "callers bind by position") so Bob can apply
  the rule to cases you didn't foresee.
- **The folder name must match the slug exactly:** `rules-rpg-dev/` for `slug: rpg-dev`.
- **Don't duplicate:** if a rule is also in `AGENTS.md` or a skill, keep one copy.

**Docs:** [Custom rules](https://bob.ibm.com/docs/ide/configuration/rules) ·
[Custom modes → mode-specific instructions](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
[Standardize Bob's behavior (tutorial)](https://bob.ibm.com/docs/ide/tutorials/standardize-bobs-behavior)
