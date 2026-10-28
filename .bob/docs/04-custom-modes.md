# 04 · Custom modes: `custom_modes.yaml`

[Docs home](../README.md) · [← 03 Rules](03-rules.md) · Next: [05 Skills →](05-skills.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 2.2, 2.5, 4.1, 4.6, 6.3. Exam-focused notes: [Section 2](exam/section-2-core-features.md) · [Section 4](exam/section-4-configuration.md) · [Section 6](exam/section-6-security.md).

## In plain English
A **mode** is a job role for Bob: who it is, what it should focus on, and, most
importantly, **which tools it may use and which files it may change**. A reviewer that
physically cannot edit code is safer than a reviewer that is merely *asked* not to.

## Where it lives
| File | Scope |
|---|---|
| `.bob/custom_modes.yaml` | This project, shared through git |
| `~/.bob/settings/custom_modes.yaml` | You, in every project |

If two modes share a `slug`: **project beats global beats built-in.** You can even
redefine `ask`, `plan` or `agent` for one project.

You can also create modes in the IDE: **Settings → Modes → +**. Bob writes the YAML for
you. File restrictions (`fileRegex`) can only be added by editing the YAML.

## Anatomy of a mode

```yaml
customModes:
  - slug: ibmi-reviewer               # id: letters/numbers/hyphens; also /ibmi-reviewer
    name: 🔍 IBM i Reviewer           # shown in the mode picker
    description: Read-only code review...      # short picker text (optional)
    roleDefinition: >-                # WHO Bob is in this mode
      You are a meticulous IBM i code reviewer ... You report findings;
      you never change code.
    whenToUse: >-                     # helps Bob choose/suggest this mode (optional)
      Use for pull request reviews, pre-production checks and audits.
    customInstructions: ...           # extra guidance (optional) + rules-ibmi-reviewer/*.md
    groups:                           # WHAT Bob may use. Not listed = not allowed.
      - read
      - - edit                        # nested list = group with options
        - fileRegex: ^reviews/.*\.md$ # may only create/edit review reports
          description: Review reports only
      - mcp
      - skill
```

### Tool groups
| Group | Lets Bob… |
|---|---|
| `read` | read, search and list files |
| `edit` | create and change files (limit it with `fileRegex`) |
| `execute` | run terminal commands |
| `mcp` | call MCP server tools ([07](07-mcp-servers.md)) |
| `skill` | load skills ([05](05-skills.md)) |
| `todo` | keep a task list |
| `subtask` / `subagent` | split work into subtasks / spawn helper agents |
| `mode` | switch to another mode |
| `workflow` | launch predefined workflows |

## The six modes in this repo

| Mode | Edit | Execute | MCP | Teaching point |
|---|---|---|---|---|
| 🟦 `rpg-dev` | `*.rpgle, *.sqlrpgle, *.rpgleinc, *.bnd` | ✅ | ✅ | Restrict edits by **file extension** |
| 🟩 `cl-dev` | `*.clle, *.clp, *.cmd` | ✅ | ✅ | Same pattern, different language |
| 🔁 `modernizer` | `qrpglesrc/` **except** `legacy/`, plus `conversions/*.md` | ✅ | ❌ | Restrict by **folder**, with a negative look-ahead |
| 🔍 `ibmi-reviewer` | `reviews/*.md` only | ❌ | ✅ | **Read-only** for code; `allowedSubagents: [explore]` |
| 📊 `ibmi-ops` | ❌ | ❌ | ✅ | **Query-only**: the safest way to explore a live system |
| 🐍 `python-tools` | `*.py`, requirements, `.env.example` | ✅ | ❌ | A non-RPG persona |

The modernizer's regex, explained:
```
^(qrpglesrc/(?!legacy/).*\.(rpgle|sqlrpgle|rpgleinc|RPGLE|SQLRPGLE|RPGLEINC)|conversions/.*\.md)$
  └─ starts in qrpglesrc/
              └─ (?!legacy/) = "but NOT followed by legacy/"
                                                                   └─ OR any .md in conversions/
```

## How the pieces connect
```
custom_modes.yaml  slug: modernizer
        │
        ├── .bob/rules-modernizer/*.md      loaded only in this mode   (03 Rules)
        ├── /modernizer                     slash command to switch    (06 Slash commands)
        ├── customInstructions → "follow the rpg-fixed-to-free skill"  (05 Skills)
        └── bob run --mode modernizer       scripted use               (09 Bob Shell)
```

## Try it
1. Switch to **🔍 IBM i Reviewer** and say *"Fix the TODO in custinq-free.pgm.rpgle."*
   Bob explains it can't edit that file. Then say *"Review it and write the report."*
   That works, because `reviews/*.md` is allowed.
2. Switch to **📊 IBM i Ops Analyst** and ask it to run `makei`. No `execute` group, so it can't.
3. Make your own: copy the `python-tools` block, change the slug to `docs-writer`, set
   `fileRegex: .*\.md$`, save, and pick it from the mode list.

## Tips and common mistakes
- **Leaving out `groups` gives the mode no tools at all.**
- **Invalid regex or duplicate slug** can stop the whole file from loading. If your modes
  vanish, check the YAML first ([11 Troubleshooting](11-troubleshooting.md)).
- `fileRegex` is a **JavaScript** regex in a YAML string. No `(?i)`, so list both cases.
- Modes restrict **Bob's file tools**. A mode with `execute` can still change files via
  shell commands. That's why the strict modes here have no `execute`, and why hooks exist.
- Write `roleDefinition` in the second person ("You are…") and keep it focused.

**Docs:** [Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
[Modes](https://bob.ibm.com/docs/ide/features/modes) ·
[Add a custom mode (tutorial)](https://bob.ibm.com/docs/ide/tutorials/add-bob-capabilities) ·
[Tool groups](https://bob.ibm.com/docs/shell/core-concepts/tools) ·
[Subagents](https://bob.ibm.com/docs/ide/features/subagents) ·
IBM's own example: [ibmi-mcp-server/.bob/custom_modes.yaml](https://github.com/IBM/ibmi-mcp-server/blob/main/.bob/custom_modes.yaml)
