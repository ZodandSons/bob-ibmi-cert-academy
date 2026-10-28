# 05 · Skills: `skills/`

[Docs home](../README.md) · [← 04 Custom modes](04-custom-modes.md) · Next: [06 Slash commands →](06-slash-commands.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 1.4, 3.4, 4.7. Exam-focused notes: [Section 1](exam/section-1-concepts.md) · [Section 3](exam/section-3-use-cases.md) · [Section 4](exam/section-4-configuration.md).

## In plain English
A **skill** is a recipe binder. Bob always sees the label on the spine (the skill's
`description`) but only pulls the binder off the shelf when your task matches it. A
skill can hold step-by-step instructions plus any files Bob might need: templates,
cheat sheets, worked examples, even scripts it can run.

Rules are always loaded and must be short; skills are loaded on demand and can be long.
That's why the long fixed-to-free opcode table and pitfalls list are a skill and not rules.

## Where they live
| Folder | Scope |
|---|---|
| `.bob/skills/<skill-name>/SKILL.md` | This project, shared through git |
| `~/.bob/skills/<skill-name>/SKILL.md` | You, in every project |

The project skill wins if both have the same name.

## Anatomy of a skill
```
.bob/skills/rpg-fixed-to-free/
├── SKILL.md                       <- required: front matter + instructions
├── reference/opcode-mapping.md    <- optional supporting files, read when needed
├── reference/pitfalls.md
├── examples/custinq-fixed.pgm.rpgle
├── scripts/inventory_fixed.py     <- Bob can run these with the execute group
└── templates/conversion-report.md
```

```markdown
---
name: rpg-fixed-to-free                         <- required; matches the folder name
description: Convert fixed-format or mixed RPG  <- required; Bob decides from THIS text.
  ... to fully free-format RPG IV ... Use for       Say what it does AND when to use it.
  any fixed-to-free conversion ...                  No description = skill ignored.
---

# Fixed-format RPG → fully free RPG IV
(instructions Bob follows once the skill is active — steps, rules, which files to read)
```

## How Bob uses them
1. Bob knows every skill's **name and description** from the start.
2. When your request matches one, Bob asks to activate it (or does so automatically if
   **Settings → Auto-Approve → Skills** is on).
3. The skill's instructions are added to the conversation **once**, and Bob can read
   its supporting files.
4. In Bob Shell, `/skills` inserts a skill reference into your prompt to force one.
5. The mode needs the `skill` group (all six custom modes here have it).

## The nine skills in this repo

| Skill | Use it when… | Supporting files | Try this prompt |
|---|---|---|---|
| [`ibmi-platform`](../skills/ibmi-platform/SKILL.md) | You need IBM i system knowledge: objects, library list, jobs, messages | Object/library and job/message references | *"Why would a program get CPF4131 after a file change?"* |
| [`rpgle-free-format`](../skills/rpgle-free-format/SKILL.md) | Writing new modern RPG | Program, service program, copybook and binder templates; BIF cheat sheet | *"Create a service program to look up customer credit limits."* |
| [`rpg-fixed-to-free`](../skills/rpg-fixed-to-free/SKILL.md) | Converting fixed or mixed RPG to `**free` | Opcode and spec maps, 17 pitfalls, a worked example, **2 Python scripts**, report template | *"Convert qrpglesrc/legacy/custinq.pgm.rpgle to free format."* |
| [`clle-programming`](../skills/clle-programming/SKILL.md) | Writing or fixing CLLE / commands | Program and command templates, MONMSG patterns | *"Write a CL program that submits the nightly order purge."* |
| [`sqlrpgle-db2`](../skills/sqlrpgle-db2/SKILL.md) | Embedded SQL, DDL, Db2 services | SQL pattern library (cursors, SQLSTATE, DDL) | *"Replace the SETLL/READE loop in ORDLIST with a cursor."* |
| [`ibmi-python`](../skills/ibmi-python/SKILL.md) | Python that talks to IBM i | **Working CLI** `ibmi_tool.py`, `.env.example` | *"Write a script that exports CUSTMAST to CSV."* |
| [`bob-shell-automation`](../skills/bob-shell-automation/SKILL.md) | Scripting Bob, CI pipelines | Batch-convert and CI-review scripts, results summarizer, GitHub Actions example | *"Set up a CI job that reviews changed RPG files."* |
| [`ibmi-build`](../skills/ibmi-build/SKILL.md) | Compiling with TOBi (`makei`) | `iproj.json`, `.ibmi.json`, `Rules.mk`, `.bnddir` templates | *"Add ORDPRICE to the build."* |
| [`rpgunit-testing`](../skills/rpgunit-testing/SKILL.md) | Unit tests for RPG procedures | RPGUnit test template | *"Add tests for Customer_IsActive."* |

### The flagship: `rpg-fixed-to-free`
It shows everything a skill can do:
- **Steps** Bob must follow: inventory → dependencies → convert → pitfalls → verify → report.
- **Reference files** too long for a rule (opcode table, 17 behaviour-changing pitfalls).
- A **worked example**: `examples/custinq-fixed.pgm.rpgle` and its annotated conversion.
- **Deterministic scripts**, so correctness isn't left to the model:
  ```bash
  python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py <src> --format markdown
  python3 .bob/skills/rpg-fixed-to-free/scripts/verify_conversion.py <original> <converted>
  ```
  `verify_conversion.py` exits 1 when there are errors. Bob, the `rules-modernizer`
  checklist and the batch script all rely on that.

## Try it
1. Run the two scripts above on the example files and read the output, since Bob reads the same.
2. Ask, in Agent mode: *"How do I monitor for end-of-file on RCVF in CL?"* Bob should ask
   to activate `clle-programming`.
3. Write your own: create `.bob/skills/shop-naming/SKILL.md` with a `name`, a
   `description` like *"IBM i object naming conventions. Use when naming new programs,
   files or fields."* and a short body. Check **Settings → Skills** and it appears.

## Tips and common mistakes
- **The description is everything.** Write "what it does + when to use it", and include
  the words people actually type ("convert", "fixed format", "RPG III").
- **One job per skill.** Separate skills for writing RPG and converting RPG trigger more accurately.
- **Keep SKILL.md short and point to files.** "Use `reference/pitfalls.md`" beats pasting it in.
- **Put verification in scripts.** Bob is good at following steps, and a script that
  fails loudly is better at proving the result.
- Paths inside a skill are relative to the repo root when Bob runs them
  (`python3 .bob/skills/...`). Write them out in full.

**Docs:** [Skills (IDE)](https://bob.ibm.com/docs/ide/features/skills) ·
[Skills (Shell)](https://bob.ibm.com/docs/shell/features/skills) ·
[Auto-approve](https://bob.ibm.com/docs/ide/features/auto-approving-actions)
