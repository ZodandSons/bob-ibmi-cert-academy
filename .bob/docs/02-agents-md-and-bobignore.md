# 02 · `AGENTS.md` and `.bobignore`

[Docs home](../README.md) · [← 01 Getting started](01-getting-started.md) · Next: [03 Rules →](03-rules.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 1.2, 2.4, 4.3, 6.4. Exam-focused notes: [Section 1](exam/section-1-concepts.md) · [Section 2](exam/section-2-core-features.md) · [Section 4](exam/section-4-configuration.md) · [Section 6](exam/section-6-security.md).

These two files live in the **repository root**, next to `.bob/`, not inside it.

## AGENTS.md: the project briefing

### In plain English
`AGENTS.md` is a short "welcome to the project" document written for AI agents. Bob reads
it at the start of every conversation, so it always knows what the system is, how the
repository is laid out, and how things are built. The name is a cross-tool convention, so
other coding agents read the same file.

### Where it lives and how Bob uses it
| | |
|---|---|
| Location | `AGENTS.md` in the workspace root |
| Loaded | Automatically, every conversation, every mode |
| Load order | After mode-specific rules, before general rules in `.bob/rules/` |
| Turn off | Setting `"bob-code.useAgentRules": false` |
| Generate a first draft | Run `/init`. Bob writes a root `AGENTS.md` and starter rule files for the Agent, Plan and Ask modes |

### The example in this repo → [`../../AGENTS.md`](../../AGENTS.md)
It answers the questions a new engineer would ask on day one:

```markdown
## Repository layout          <- where each kind of source lives (qrpglesrc/, qcllesrc/ ...)
## Build                      <- makei build / makei c -f <file>
## Environments               <- DEV / TEST / PROD libraries and who may change them
## Key business objects       <- CUSTMAST, ORDHDR ... and their keys
## How to work here           <- which modes, skills and commands to use
```

### AGENTS.md or rules?
| Put it in **AGENTS.md** | Put it in **`.bob/rules/`** |
|---|---|
| Facts: what, where, how it's built | Instructions: always / never do X |
| "Orders live in ORDHDR keyed by customer and order" | "Never hard-code library names" |
| One file, easy to read top to bottom | Many small files, easy to change one at a time |

### Tips
- Keep it under about 100 lines. It is sent on every request, and longer means slower and costlier.
- Update it in the same pull request that changes the layout or build.

**Docs:** [Custom rules → Using AGENTS.md files](https://bob.ibm.com/docs/ide/configuration/rules) ·
[Quickstart (`/init`)](https://bob.ibm.com/docs/ide/getting-started/quickstart) ·
[Standardize Bob's behavior (tutorial)](https://bob.ibm.com/docs/ide/tutorials/standardize-bobs-behavior)

---

## .bobignore: "do not open"

### In plain English
A list of files Bob is not allowed to read or change: credentials, customer data
extracts, save files. Same syntax as `.gitignore`.

### Where it lives and how Bob uses it
| | |
|---|---|
| Location | `.bobignore` in the workspace root |
| Syntax | `.gitignore` patterns: `dir/`, `*.ext`, `path/file`, `**/`, `!exception` |
| Blocks | Bob's file tools (read, write, apply diff, insert, search), and common file-reading commands such as `cat` and `grep` |
| Hides | Matching files are omitted from (or shown with a 🔒 in) Bob's file listings |
| Reload | Automatic on save. Bob can never edit `.bobignore` itself |

### The example in this repo → [`../../.bobignore`](../../.bobignore)
```gitignore
.env                 # credentials ...
.env.*
!.env.example        # ... but the template stays readable
**/*.savf            # save files
data/extracts/**     # production data extracts may contain customer data
.bob/logs/**         # hook output: noise for Bob
```

Note what is **not** ignored: `.logs/` and `.evfevent/` (build output). The `/build`
command needs Bob to read compile errors there. Ignore too much and Bob can't do its job.

### Important limitations
- **`@` mentions bypass it.** If *you* type `@.env` in a prompt, the file's contents are
  sent anyway. `.bobignore` stops Bob from reaching for a file, not you from attaching it.
  (The `block-secrets.py` hook catches passwords typed into a prompt, but not attached files.)
- **It is not a sandbox.** A shell command such as `python3 dump.py .env` is not checked.

For real protection, combine it with:
- **modes** without the `execute` group ([04](04-custom-modes.md)), and
- **hooks** that block writes to sensitive paths ([08](08-hooks.md); see `protect-paths.py`).

### Try it
1. Create `.env` containing `DB2i_PASS=dummy`.
2. Ask Bob: *"What is in .env?"* It should refuse.
3. Ask: *"What is in .bob/skills/ibmi-python/scripts/.env.example?"* That one is allowed by the `!` exception.

**Docs:** [Ignoring files](https://bob.ibm.com/docs/ide/configuration/bobignore) ·
[Context mentions (`@`)](https://bob.ibm.com/docs/ide/features/context-mentions)
