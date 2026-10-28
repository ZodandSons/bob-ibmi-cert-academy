# Section 1 · Concepts (≈17% of the exam)

[Exam home](README.md) · Next: [Section 2 Core features →](section-2-core-features.md)

Objectives: **1.1** Write effective prompts · **1.2** Initiate a project (AGENTS.md) ·
**1.3** Why use an MCP server · **1.4** Structure of Bob skills

---

## 1.1 Write effective prompts

### Know this
- A strong prompt = **clear instruction + the information Bob needs** to interpret it.
- **Five prompt components:** **instruction** (what to do), **role** (who Bob should act as),
  **context** (project/code facts), **example** (a model of the desired output), **cue**
  (how to start or shape the answer).
- **Specificity:** state the exact task and outcome. Include constraints that matter:
  language, framework, file scope, expected behaviour, output format, completion criteria.
- **Context:** use `@` mentions to point at *specific* files or code instead of loading
  broad repository content (cheaper, less confusing; see 4.2 and 4.3).
- **Task decomposition:** split complex work into smaller steps, each with a clear objective.
- **Examples:** the strongest form is pointing Bob at a *real, good example in your own
  codebase* ("make it like `@qrpglesrc/custinq.pgm.rpgle`"), not a generic instruction
  to "find examples" or "act as an expert".

### In this repo
[`commands/plan-ibmi-change.md`](../../commands/plan-ibmi-change.md) is a working prompt
with each of the five components as a heading: **Role**, **Instruction**, **Context**
(with `@` mentions), **Constraints**, **Example**, **Cue**. Every other command in
[`commands/`](../../commands/) is a short, specific, decomposed prompt too.

### Weak vs strong (IBM i)
| Weak | Strong |
|---|---|
| "Fix the order program." | "In `@qrpglesrc/ordentry.pgm.sqlrpgle`, the SQL INSERT at lines 140–155 fails with SQLSTATE 23505 when an order is re-submitted. Make it detect the duplicate and show message ORD0012 instead. Don't change other procedures. Done when the program compiles and `t_ordentry` passes." |
| "Write a CL program like the others." | "Create `qcllesrc/ordpurge.pgm.clle` following the structure of `@qcllesrc/ordnight.pgm.clle` (global MONMSG, ERROR routine)." |

### Lab
In Ask mode, send the weak prompt above, then the strong one. Compare how many files
Bob reads and how specific the answer is (watch the context-usage indicator, 4.2).

### Exam traps
- "Tell Bob to act as a senior developer" is a **role**, not an example.
- "Tell Bob to find good examples in the codebase" ≠ giving an example. *Pointing at one
  specific good file* is the example practice.

---

## 1.2 Initiate a project (AGENTS.md)

### Know this
- **`/init`** scans the project and generates **AGENTS.md** context files, giving Bob
  persistent project context. Run it when you start work on a project (in Agent mode).
- **Root `AGENTS.md`**: concise, actionable project summary used in new conversations.
  Typical content: purpose, directory structure, tech stack, architectural patterns,
  conventions, development workflows.
- **Mode-specific AGENTS.md files** inside `.bob/`, one each for **Agent, Plan and Ask**,
  give each built-in mode guidance suited to how it operates. **To add custom rules to a
  default mode, edit that mode's AGENTS.md file in `.bob`** (or add any file to its
  `rules-{slug}/` folder).
- **Maintenance:** re-run `/init` after significant structural, module, framework or
  technology changes (and when onboarding people). Manually add business or team
  conventions the scan can't detect.
- AGENTS.md loads automatically (disable with `"bob-code.useAgentRules": false`), after
  mode-specific rules and before general workspace rules.

### In this repo
- Root: [`AGENTS.md`](../../../AGENTS.md)
- Mode files: [`rules-agent/AGENTS.md`](../../rules-agent/AGENTS.md),
  [`rules-plan/AGENTS.md`](../../rules-plan/AGENTS.md),
  [`rules-ask/AGENTS.md`](../../rules-ask/AGENTS.md)
- Guide: [02 AGENTS.md and .bobignore](../02-agents-md-and-bobignore.md)

> **Naming note.** The current rules docs and the exam guide use `rules-agent/`. IBM's
> older `/init` tutorial shows `.bob/rules-code/AGENTS-code.md`, `rules-plan/AGENTS-plan.md`
> and `rules-ask/AGENTS-ask.md`. Agent mode was called *Code* mode before Bob v2. The
> idea is identical: a mode's folder `rules-{slug}/` holds that mode's AGENTS file.

### Lab
In an empty test folder, run `/init` in Agent mode and compare what it generates with this
repo's `AGENTS.md` and mode files. Note what the scan could *not* know (e.g. "never touch ORDPRD").

---

## 1.3 Why use an MCP server

### Know this
- **MCP (Model Context Protocol)** is a **standardized** way for Bob to interact with
  external tools and services. One standard interface replaces a unique integration per system
  (the "USB-C port" analogy).
- **Capability extension without modifying Bob's core**: databases, APIs, developer tools,
  operational systems.
- **Local or remote** servers, depending on integration and security needs (transports in 4.5).
- **Scope:** global vs project (`.bob/mcp.json`). **Project wins on name conflicts.**
- **Security boundary:** adding a server expands what Bob can read or do. Trusted
  deployments need authentication, encryption, access controls and auditing.

### In this repo
[`mcp.json`](../../mcp.json) adds IBM's IBM i MCP server with **read-only** SQL tools from
[`mcp-tools/ibmi-dev-tools.yaml`](../../mcp-tools/ibmi-dev-tools.yaml). Bob gains live
"where used" and job-log analysis without any change to Bob itself.
Guide: [07 MCP servers](../07-mcp-servers.md).

> **Path note.** The exam guide writes the global file as `~/.bob/mcp.json`. The current
> docs show `~/.bob/settings/mcp.json` (Windows `%APPDATA%\Bob\settings\mcp.json`). Know
> both; the exam tests the *concept*: global vs project, project wins.

---

## 1.4 Structure of Bob skills

### Know this
- **Skill** = reusable instruction set teaching a specialized workflow. Goals: reusability,
  consistency, specialization, collaboration, repeatability.
- **Location:** each skill in its own folder: `<project>/.bob/skills/<name>/` or
  `~/.bob/skills/<name>/`. **Project skill wins** if the same name exists globally.
- **`SKILL.md`** is required: YAML front matter with at least **`name`** and
  **`description`**, then the instructions. **No description → skill ignored.**
- **Supporting resources** beside SKILL.md: checklists, templates, reference docs, config
  examples, scripts, style guides.
- **Activation:** Bob uses the **description** to decide when a skill is relevant, then
  loads its instructions (once per conversation) and can read its supporting files.
  Rules are always active, modes are activated by the user, **skills are activated by Bob**.

### In this repo
Nine skills in [`skills/`](../../skills/). The richest is
[`rpg-fixed-to-free/`](../../skills/rpg-fixed-to-free/SKILL.md): SKILL.md + `reference/`
+ `examples/` + `scripts/` + `templates/`. Guide: [05 Skills](../05-skills.md).

> **Mode note.** The exam guide says skills are available in **Agent** mode (1.4) and,
> elsewhere, "only in **Advanced** mode" (4.7, wording from Bob v1). In the current
> docs, Agent, Plan and Ask all list the Skill tool group. If asked, associate skills with
> the full-tool mode (Agent; formerly Advanced).

---

## Check yourself
<details><summary>1. Which practice is "using examples": "act as a senior RPG developer" or "follow the structure of @qcllesrc/ordnight.pgm.clle"?</summary>
The second. Pointing at a concrete, good example in your codebase. The first is a <b>role</b>.
</details>
<details><summary>2. You want Plan mode to always include a rollback section. Where do you put that?</summary>
In Plan mode's rules: its AGENTS.md (or another file) in <code>.bob/rules-plan/</code>. Built-in modes can be customized; you don't need a custom mode.
</details>
<details><summary>3. The team adopted a new framework and reorganized folders. What should you do with AGENTS.md?</summary>
Re-run <code>/init</code>, then re-add manual conventions the scan can't detect.
</details>
<details><summary>4. A SKILL.md has a name but no description. What happens?</summary>
The skill is ignored. The description drives activation.
</details>
<details><summary>5. Global and project mcp.json both define "ibmi-mcp". Which is used?</summary>
The project one.
</details>

**Docs:** [Quickstart (`/init`)](https://bob.ibm.com/docs/ide/getting-started/quickstart) ·
[Start a project with /init](https://bob.ibm.com/docs/ide/getting-started/tutorials/start-a-project) ·
[Custom rules](https://bob.ibm.com/docs/ide/configuration/rules) ·
[Understanding MCP](https://bob.ibm.com/docs/ide/configuration/mcp/understanding-mcp) ·
[Skills](https://bob.ibm.com/docs/ide/features/skills) ·
[Context mentions](https://bob.ibm.com/docs/ide/features/context-mentions)
