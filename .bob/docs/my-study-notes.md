# What is IBM Bob?

IBM Bob is an AI SDLC (Software Development Lifecycle) assistant — IBM's AI coding assistant.

| Interface | Description | Best for |
|-----------|-------------|----------|
| **Bob IDE** | A full editor (VS Code based) with a Bob chat panel | Day-to-day development |
| **Bob Shell** | A command-line tool (`bob`, `bob run…`) | Terminal work, scripting, CI/CD pipelines |

> **The `.bob` folder** — Bob knows nothing about your shop or project: the `.bob` folder is where you teach it.

---

## AGENTS.md (repo root) — The project briefing

`AGENTS.md` is a short "welcome to the project" document written for AI agents. Bob reads it at the start of every conversation. It answers the questions a new engineer would ask on day one.

- **Generate a first draft** — Run `/init`. Bob writes a root `AGENTS.md` and starter rule files for the Agent, Plan and Ask modes.
- **Tip:** Keep it under about 100 lines. It is sent on every request, and longer means slower and costlier. Update it in the same pull request that changes the layout or build.

---

## .bobignore (repo root) — Files Bob may not read or edit

A list of files Bob is not allowed to read or change: credentials, customer data extracts, save files. Same syntax as `.gitignore`.

---

## rules/ — Shop Standards

Rules are your shop's non-negotiable standards, written as short Markdown files. Bob adds them to every message it sends to the model, so it never "forgets" them. Some rules apply everywhere, and some only in one mode.

| Location | Scope |
|----------|-------|
| `.bob/rules/` | Every mode |
| `.bob/rules-{slug}/` | Only the mode with that slug |
| `.bob/rules-agent/`, `rules-plan/`, `rules-ask/` | The built-in Agent, Plan and Ask modes |
| `~/.bob/rules/`, `~/.bob/rules-{slug}/` | You personally, in every project |

**How Bob loads rules:** Global (`~/.bob/…`) loads before workspace (`.bob/…`). Workspace rules can override global ones. Files in a folder load alphabetically — that's why they are numbered `01-`, `02-`…

A mode's rule files are combined with its `customInstructions` from `custom_modes.yaml`.

> **Rule of thumb:** if it's longer than a screen, or only needed sometimes, make it a skill.

You can override default Bob modes (such as Agent, Ask, or Plan) by creating a custom mode with the same slug — `(rules-<slug-name>/)`.

---

## Modes

A mode is a job role for Bob: who it is, what it should focus on, and — most importantly — which tools it may use and which files it may change.

**Config locations:**

- `.bob/custom_modes.yaml`
- `~/.bob/settings/custom_modes.yaml`

If two modes share a slug: project beats global beats built-in.

**Default modes:**

| Mode | Purpose |
|------|---------|
| **Plan** | Analyzes requirements, researches and designs implementation steps |
| **Agent** | Use when you need to write, modify, or refactor code |
| **Ask** | Use when you need explanations, documentation, or answers to technical questions |

**Key rules for custom modes:**

- `custom_modes.yaml` — Personas (RPG dev, reviewer…) with limited tool access.
- File restrictions (`fileRegex`) can only be added by editing the YAML:
  ```yaml
  - fileRegex: ^reviews/.*\.md$   # may only create/edit review reports
  ```
- Leaving out permission groups gives the mode no tools at all.

---

## skills/ — Reusable instruction sets

A skill is a reusable instruction set that teaches Bob a specialized, repeatable workflow — like a recipe binder. Bob always sees the label on the spine (the skill's description) but only pulls the binder off the shelf when your task matches it.

A skill can hold step-by-step instructions plus any files Bob might need: templates, cheat sheets, worked examples, even scripts it can run.

> **Rules** are always loaded and must be short; **skills** are loaded on demand and can be long.
> (That's why the long fixed-to-free opcode table and pitfalls list are a skill and not rules.)

**Skill file locations:**

- `.bob/skills/<skill-name>/SKILL.md`
- `~/.bob/skills/<skill-name>/SKILL.md`
- Supporting sub-folders: `/reference`, `/examples`, `/templates`, `/scripts`

**How skills activate:**

- Bob knows every skill's name and description from the start.
- When your request matches one, Bob asks to activate it (or does so automatically if **Settings → Auto-Approve → Skills** is on).
- The skill's instructions are added to the conversation once, and Bob can read its supporting files.
- In Bob Shell, `/skills` inserts a skill reference into your prompt to force one.
- *The mode needs the skill group (all six custom modes here have it).*

**Best practices:**

- The description is everything. Write "what it does + when to use it", and include the words people actually type ("convert", "fixed format", "RPG III").
- One job per skill. Separate skills for writing RPG and converting RPG trigger more accurately.
- Keep `SKILL.md` short and point to files. "Use reference/pitfalls.md" beats pasting it in.
- Put verification in scripts. Bob is good at following steps, and a script that fails loudly is better at proving the result.
- Paths inside a skill are relative to the repo root when Bob runs them (`python .bob/skills/...`). Write them out in full.

---

## slash commands/ — Reusable prompts you trigger with `/name`

A slash command is a saved prompt. Instead of typing the same eight-line request every time you convert a program, you type:

```
/convert-to-free qrpglesrc/legacy/x.rpgle
```

Commands make good practice the easy path, and the whole team runs the same workflow.

**File locations:**

- `.bob/commands/<name>.md`
- `~/.bob/commands/<name>.md`

The file name is the command name: `review-ibmi.md` → `/review-ibmi`

**Front matter fields** (both optional):

```yaml
description: Convert a fixed-format RPG source to fully free format, with verification
argument-hint: <legacy-source-file>
```

**Argument placeholders:** `$1` = first word you type, `$2` = second word.

**Best practices:**

- Use `$1`, `$2` placeholders and an `argument-hint` so people know what to type.
- Start with a clear instruction, then numbered steps. Say what the final answer should look like.
- Names are slugified: lowercase, dashes, no special characters.
- Custom modes also appear in the `/` menu (`/modernizer` switches mode). Those can't be overridden by a command file with the same name.

---

## MCP (Model Context Protocol) server

MCP lets Bob talk to outside systems through small helper programs called MCP servers. An MCP server acts as a bridge between Bob and external services like databases, APIs, or custom scripts. With MCP, you can extend Bob's capabilities beyond its built-in features.

> **Example:** Which programs use `CUSTMAST`?

**Key files:**

| File/Folder | Purpose |
|-------------|---------|
| `.bob/mcp.json` | MCP Server Registry — defines which MCP servers are available to Bob |
| `mcp-tools/` | Tool definitions for a specific MCP server |

### 1. `.bob/mcp.json` — MCP Server Registry

This file tells IBM Bob:
- Which MCP servers are configured
- How to start or connect to each server
- What arguments and environment variables to provide
- Which servers are available within the project

### 2. `mcp-tools/` — Tool Definitions

For an MCP server that supports file-based tool definitions, a directory such as `mcp-tools/` contains the definitions of operations that server can expose.

**Credentials — managing secrets:**

Set `DB2i_HOST`, `DB2i_USER`, `DB2i_PASS` in your shell profile before starting Bob.

| Command | Action |
|---------|--------|
| `/manage-secrets set DB2i_PASS` | Set a new secret |
| `/manage-secrets list` | List existing keys |
| `/manage-secrets rm KEY` | Remove a key |

> `.env` works — but with an important caveat: Bob does not natively inject `.env` into MCP config the way `/manage-secrets` does.
> **Bottom line:** use `.env` for your scripts and Python tools; use `/manage-secrets` for anything referenced in `mcp.json`.

---

## Hooks — `settings.json` and `hooks/`

> **Rules** ask Bob to behave. **Hooks** make sure.

A hook is a small script that Bob runs automatically at set moments: when a session starts, when you send a prompt, before or after it uses a tool, and when it finishes.

**Config locations:**

- `.bob/settings.json` → `"hooks"`
- `~/.bob/settings/settings.json` → `"hooks"`
- **Group policy `EnforcedHooks`** — your organisation's admins can force hooks on everyone.

The scripts themselves can live anywhere; convention is `.bob/hooks/`. View and toggle hooks in **Settings → Hooks** (IDE) or `/hooks` (Bob Shell).

### The five hook events

| Event | When it fires |
|-------|--------------|
| `SessionStart` | Once, when a session begins |
| `UserPromptSubmit` | Each prompt, before it's sent |
| `PreToolUse` | Before a matching tool runs |
| `PostToolUse` | After a matching tool ran |
| `Stop` | When Bob finishes |

**Exit codes:** `0` = OK · `2` = block (`PreToolUse` / `PostToolUse` only) · anything else = logged and ignored. `stderr` goes to Bob's log; for a block, it's the reason shown.

Bob writes JSON to the script's `stdin`.

### What `SessionStart` can do

Adding context is one of its primary purposes, but `SessionStart` can do more:

| Action | Example |
|--------|---------|
| **Inject context** | Tell Bob the project name, Git branch, IBM i development library |
| **Initialize environment** | Create temporary directories or prepare workspace files |
| **Validate prerequisites** | Check whether Git, Node.js, or other required tools are installed |
| **Gather dynamic information** | Inspect RPGLE sources, Git status, or project configuration; generate temporary metadata or diagnostic reports |
| **Log activity** | Record session initialization for troubleshooting |

Side effects such as creating files or writing logs happen independently of context injection.

---

## Bob Shell — Using `.bob` from the command line

Bob Shell is Bob in your terminal. It reads the same `.bob` folder as the IDE — so rules, modes, skills, commands, MCP servers, and hooks all behave identically. It's also how you put Bob into scripts and CI pipelines: convert 200 programs overnight, or review every pull request automatically.

For scripts and CI, create an API key (scope **Inference**) in the Bob portal and export `BOB_API_KEY=…`. `bob run` requires it.

---

## Context Window Management

Each session in Bob Shell — and each task in the chat panel — has a context window: the token budget for that conversation. The cap is **270,000 tokens**. Everything Bob loads counts against it.

**What fills the context window:**

| Component | Description |
|-----------|-------------|
| **System prompt** | Bob's core instructions for the session |
| **Tool definitions** | Built-in tool schemas and connected MCP tool definitions |
| **MCP tools** | Instructions and descriptions for tools provided by connected MCP servers |
| **Rules** | Custom instructions from project and mode rule files (e.g. `AGENTS.md` or `.bob/rules-*`) |
| **Skills** | Instructions from skills Bob loaded for the conversation |
| **Messages** | Your prompts, Bob's replies, and tool activity in the conversation (the transcript counted as tokens) |

`@` mentions, command output, and tool results all count toward Messages. File contents do not appear as a separate line.

---

## Context Poisoning

Context poisoning is when wrong or irrelevant information gets into the context window and stays in the transcript. Bob treats the information as fact on follow-up prompts. Replies drift. Tool calls become inaccurate. The work goal gets lost.

### Symptoms

- **Worse output** — Suggestions repeat, wander, or stop matching the repo.
- **Wrong tool use** — Tool steps in the transcript no longer match what you asked for.
- **Stuck multi-step work** — Long multi-prompt flows loop or stall.
- **Short-lived fixes** — A corrective prompt helps once, but then the problem returns.
- **Tool confusion** — Bob misuses tools even though tool definitions did not change.

> If Messages is already large, check your token usage first. Poisoning and an overfull window often occur together.

### Common causes

| Cause | Description |
|-------|-------------|
| **Bad facts in the session** | Bob states something incorrect; later exchanges treat it as ground truth in Messages |
| **Stale or wrong repo text** | Outdated comments, README fragments, or generated docs mislead file reads |
| **Oversized pastes** | Logs or snippets with noise, truncation, or hidden characters land in Messages |
| **Compaction** | Bob compacts older Messages; useful detail disappears, and what remains can dominate the session |
| **Irrelevant context** | Unrelated files, old plans, or a prior work goal still exist in the transcript |

### Recovery

1. **Start a new session** — Exit and run `bob` again. This clears poisoned Messages while keeping Rules and project files on disk.
2. **Paste less** — Send only the log lines or errors Bob needs. Large dumps increase Messages and introduce more risk.
3. **Split the work goal** — Use separate sessions for unrelated steps so that a stale transcript does not carry over.
4. **Check tool output** — If a tool returns garbage, stop and start a new session rather than letting Bob build on it in Messages.
5. **Trust tests over text** — When comments and code disagree, point Bob at runnable checks. (Same guidance as context window best practices.)

---

## IBM i Workflows — Every piece working together

### Progress checklist

- [x] **01 Getting started** — Install Bob and check that this folder loads.
- [x] **02–05** — Read guides in order; each is a 5–10 minute read with a "Try it" section.
- [x] **06–08** — Read guides in order; each is a 5–10 minute read with a "Try it" section.
- [ ] **10 IBM i workflows** — Shows the pieces working together on real tasks.
- [ ] **Certification track** — Preparing for IBM certification C3000-006? Follow the certification track.
- [ ] **Stuck?** — See guide 11 Troubleshooting. Unknown term? Guide 12 Glossary. All links in guide 13 Reference links.

---

## Exercises

### Conversions & modes

- [x] Do a real conversion on a copy of one of your own fixed-format programs: put it in `qrpglesrc/legacy/` and run `/convert-to-free qrpglesrc/legacy/<file>`. → *10 IBM i workflows*
- [x] Ask mode: "What file extension should a new CL program have?" The answer comes from `rules/01-…`.
- [x] Create `.bob/rules/common/99-test.md` containing `Always end your answers with "— Bob"`. Ask anything. Then delete the file.
- [x] Switch to CL Developer and ask "What goes right after the DCLs?" (global `MONMSG`, from `rules-cl-dev/`). Ask the same in Ask mode and compare.
- [x] Switch to 🔍 IBM i Reviewer and say "Fix the TODO in `custinq-free.pgm.rpgle`." Bob explains it can't edit that file. Then say "Review it and write the report." That works, because `reviews/*.md` is allowed.
- [x] Switch to 📊 IBM i Ops Analyst and ask it to run `makei`. No execute group, so it can't.
- [ ] Make your own: copy the `python-tools` block, change the slug to `docs-writer`, set `fileRegex: .*\.md$`, save, and pick it from the mode list.

### Skills

Try each of these prompts and observe which skill Bob activates:

- [ ] "Create a service program to look up customer credit limits."
- [ ] "Convert `qrpglesrc/legacy/custinq.pgm.rpgle` to free format."
- [ ] "Write a CL program that submits the nightly order purge."
- [ ] "Replace the SETLL/READE loop in ORDLIST with a cursor."
- [ ] "Write a script that exports CUSTMAST to CSV."
- [ ] "Set up a CI job that reviews changed RPG files."
- [ ] "Add ORDPRICE to the build."
- [ ] "Add tests for `Customer_IsActive`."
- [ ] Run the two scripts on the example files and read the output, since Bob reads the same.
- [ ] Ask, in Agent mode: "How do I monitor for end-of-file on RCVF in CL?" Bob should ask to activate `clle-programming`.
- [ ] Write your own: create `.bob/skills/shop-naming/SKILL.md` with a name, a description like "IBM i object naming conventions. Use when naming new programs, files or fields." and a short body. Check **Settings → Skills** — it appears.

---

## Bob Study — Quick Reference

| Concept | One-line definition |
|---------|---------------------|
| **Slash command** | Sends a saved prompt |
| **Mode** | Who Bob is and what it may touch |
| **Skill** | What Bob knows how to do |

**Effective prompt** — names the task, a role, context, and an example.  
An effective prompt combines: **Instruction · Role · Context · Example · Cue**

You can save your prompts as custom slash commands to reuse and share with your team.  
**Tips:** Be specific · Provide context · Break down tasks · Include examples

A skill is a reusable instruction set that teaches Bob a specialized, repeatable workflow.  
You can use the UI, or use the `/create-skill` command in the Bob chat for a guided setup.  
**Skill fields:** Skill Name · Description · Allow Bob to use this skill · Scope & Location

A custom mode combines a role definition, behavioral instructions, and a deterministic set of permitted tools.  
**Steps:** Define the application requirements → Refine the plan → Review the plan

### Reference links

- <https://bob.ibm.com/docs/ide/features/slash-commands#creating-custom-commands>
- <https://bob.ibm.com/docs/ide/tutorials/use-skills>
- <https://bob.ibm.com/docs/ide/tutorials/ai-pair-programming-with-ibm-bob>
- <https://bob.ibm.com/docs/ide/tutorials/modernize-nodejs-express-api>
- <https://bob.ibm.com/docs/ide/tutorials/mcp-server-integration>
