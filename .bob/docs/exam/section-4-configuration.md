# Section 4 · Bob configuration (≈17% of the exam)

[Exam home](README.md) · [← Section 3](section-3-use-cases.md) · Next: [Section 5 Accounts →](section-5-accounts.md)

Objectives: **4.1** tools · **4.2** context window management · **4.3** context mentions ·
**4.4** extensions · **4.5** MCP tools · **4.6** custom modes · **4.7** skills ·
**4.8** rules (global vs project) · **4.9** pull requests

This section rewards **exact facts**: names, paths, numbers. Use the
[cheat sheet](cheat-sheet.md) for last-minute review.

---

## 4.1 Tools: read, command, subtask, MCP…
**The tool loop:** Bob **selects a tool → presents its parameters for review → runs the
approved tool → repeats** until the task is complete.

| Group | Tools | Notes |
|---|---|---|
| **Read** | `read_file`, `glob`, `grep`, `list_files`, `GetSymbolsOverview`, `FindSymbol`, `FindReferencingSymbols` | No changes |
| **Edit (write)** | `write_file`, `apply_diff`, `insert_content`, `search_and_replace` | Create/modify files |
| **Command** | `execute_command` | Install deps, run tests, build |
| **Subagent** | `spawn_subagent` | Isolated context; **explore** (read-only, lighter model) or **general** (full tools, default model); use sparingly; `fork_context: true` passes parent history |
| **Subtask** | `start_subtask` | New **named, visible** task thread: title, message, initial todo list, optional starting mode |
| **MCP** | `use_mcp_tool` | Tools from connected MCP servers |
| **Mode** | `switch_mode` | Agent, Plan, Ask, or custom |
| **Skill** | `use_skill` | Loads a skill's full instructions **once per conversation** |
| **Workflow** | `start_workflow` | Predefined multi-step process (e.g. PR creation, code review) |
| **Todo** | `update_todo_list` | Visible checklist for multi-step tasks |
| **Question** | `ask_followup_question` | Clarify before proceeding |

Subagents are used **only** when a task is self-contained, would pollute the main context,
and can't be done in one or two direct tool calls.

**In this repo:** hook matchers on `execute_command` and the write tools
([`settings.json`](../../settings.json)); modes granting/withholding groups
([`custom_modes.yaml`](../../custom_modes.yaml)).

## 4.2 Utilize context window management
**Numbers to memorize**

| Fact | Value |
|---|---|
| Hard cap per task | **270,000 tokens** |
| Automatic condensation starts | **~190,000 tokens** |
| Baseline for a trivial prompt (sample project) | **~8.5k tokens** (mostly tool definitions, system prompt, rules, skills) |
| Reserved for the model's reply (Shell report) | ~20k |

**Six categories** in the token-usage breakdown: **system prompt · tool definitions · MCP tools ·
rules** (AGENTS.md, `.bob/rules-*`) **· skills · messages** (prompts, replies, tool activity,
`@` mentions, command output; file contents have no separate line).

**How each grows**
- System prompt and tool definitions: set at task start, **stay flat**.
- MCP tools and rules: grow when servers/tools or rule files are **added**, not from prompting.
- Skills: can grow **mid-thread** when Bob activates a new skill.
- Messages: grow every turn and with repo exploration. **Usually the largest category.**

**Monitoring:** the token-usage indicator shows percent-full and used/total. Click it for
the breakdown.

**Condensation:** keeps recent/relevant context plus system instructions, tool definitions,
rules and skills. Summarizes or removes older segments. It is **lossy**: early details in
Messages may not survive. Start a new task when changing topics or when quality degrades.

**Bobcoins impact:** input **and** output tokens count, and **every message re-sends the full
active context** (including fixed overhead). Later prompts in a long thread cost more, even
if they are short.

**Best practices**
- **Scope:** one task per work goal; state goal, outcome, constraints up front; name files.
  Start a new task (**+**) when the topic changes.
- **Lean standing context:** short rules and AGENTS.md; connect only needed MCP servers,
  tools and skills; prefer **project-scoped** MCP config.
- **Add context when needed:** `@file` or line ranges instead of pasting or whole
  directories. Work in stages: **find → inspect → plan → change → validate**. Use
  **subagents** for broad repo reads.
- **Reset/condense** when Messages fills up: keep constraints, evidence, open questions.

**In this repo:** rules are deliberately short; long know-how lives in on-demand skills;
`/impact-analysis` uses subagents so only summaries land in Messages; `SessionStart` hook
output is kept to a few lines.

## 4.3 Context mentions (@)
| Mention | Includes |
|---|---|
| `@/path/to/file` | Full file contents **with line numbers** (text, PDF, DOCX). Line range: `@/src/app.js:10-20` |
| `@/path/to/folder` | Files **directly** in the folder (**non-recursive**) |
| `@problems` | All errors/warnings from the Problems panel, grouped by file |
| `@terminal` | Most recent command + its full output (doesn't clear the terminal) |
| `@<commit-hash>` | That commit: message, author, date, diff |
| `@git-changes` | Uncommitted changes |
| `@https://…` | Web page fetched and converted to Markdown (headless browser) |

- **File/folder mentions bypass `.bobignore` and `.gitignore`.** **Git mentions respect
  `.gitignore`** (they use Git commands).
- Combine mentions: "Fix `@problems` in `@/qrpglesrc/ordentry.pgm.sqlrpgle`".
- Bob Shell limits: 100 KB per file, 500 KB total; `@server:resource` for MCP resources.

## 4.4 Download extensions
- **Premium packages** (Java Modernization, Z, i): installed via an **in-app notification**
  when an entitlement is detected (**Install**); updated from **Extensions** or **Install from VSIX…**.
- **Bob Shell companion extension:** when Bob Shell runs in Bob IDE's integrated terminal,
  Bob offers to install it, or run **`/ide install`**. Manage with **`/ide enable`**,
  **`/ide disable`**, **`/ide status`**.
- The exam guide itself notes that a general-purpose marketplace inside Bob IDE is
  unconfirmed. Know the two mechanisms above.

## 4.5 Develop and add MCP tools
**Configuration**
- Global (`~/.bob/settings/mcp.json`; the exam guide writes `~/.bob/mcp.json`) vs project
  `.bob/mcp.json` (version-controlled). **Project wins on name conflicts.**
- Edit from **Settings → MCP → Edit Global MCP / Edit Project MCP**.
- Bob ships with **no pre-installed MCP servers.** Build your own (MCP SDK) or use community servers.
- **Settings → MCP → Use MCP Servers** toggle: whether Bob can connect to *any* server.
- **Settings → MCP → Enable MCP Server Creation**: whether Bob can scaffold new servers on request.
- Enable/disable **individual tools** in a server to save context.
- Per server: delete, restart, enable/disable, **network timeout 30 s–5 min (default 1 min)**,
  manage tools. **Always allow** per tool (gated by the global MCP auto-approve setting).
- **Create a server with Bob:** ask in natural language ("Build an MCP server for the GitHub
  Gist API"). Bob scaffolds it, implements the tool, prompts for credentials and connects it.

**Parameters**
| Transport | Parameters |
|---|---|
| **STDIO** | `command` (**required**), `args`, `cwd`, `env`, `alwaysAllow`, `disabled` |
| **Streamable HTTP / SSE** | `url` (**required**), `headers`, `alwaysAllow`, `disabled`; `"type": "streamable-http"` |

**Transports**
| | STDIO (local) | Streamable HTTP (modern remote) | SSE (legacy remote) |
|---|---|---|---|
| How | Bob spawns the server as a **child process**; newline-delimited **JSON-RPC 2.0** over stdin/stdout | Single HTTP endpoint (POST + GET), optional SSE streaming | GET event stream + separate POST endpoint |
| Traits | Same machine, very low latency, **no network exposure**, one-to-one | Remote, many concurrent clients, needs network security | Superseded by Streamable HTTP |
| Deploy | Per-user install; updates on every machine; local file permissions | Install once, shared; central updates; auth-based access | same as HTTP |

Hybrids: a local STDIO proxy to remote services, or a local gateway fanning out to remote servers.

**Good tool descriptions:** clear names, purpose and use-case descriptions, detailed parameter
specs (type, format, examples, required vs optional).

**Security:** prefer **local/STDIO** servers for confidential data (external servers may send
data to third parties); local servers run **with Bob's permissions**, so install only from
trusted sources; keep an **approved-server inventory** and audit (GDPR, HIPAA…); **never hardcode
credentials** (env vars/secrets vault; keep secret-bearing config out of git).

**In this repo:** [`mcp.json`](../../mcp.json) has one STDIO server (`command`/`args`/`cwd`/`env`,
`${VAR}` credentials) and one disabled `streamable-http` server.
[`mcp-tools/ibmi-dev-tools.yaml`](../../mcp-tools/ibmi-dev-tools.yaml) shows well-described,
read-only tools with typed, required parameters. Guide: [07](../07-mcp-servers.md).

## 4.6 Create custom modes
- Components: **slug, name, role definition**, when to use (opt.), **available tools**, custom
  instructions (opt.), description (opt.), allowed subagents (opt.).
- Create: Settings → Modes → create → fill in → Save (stored as YAML). Or edit
  `~/.bob/settings/custom_modes.yaml` (global) / `.bob/custom_modes.yaml` (project).
- Tool groups: `read`, `edit` (optionally `fileRegex`), `execute`, `mcp`, `skill`, `workflow`,
  `todo`, `subtask`, `subagent`, `mode`.
- **Validation:** slug = letters/numbers/hyphens, unique · unknown group names grant no access ·
  **omitting `groups` grants no grouped tools** · invalid `fileRegex` can stop the mode loading.
- Mode instructions: `.bob/rules-{slug}/` (preferred, alphabetical) or `.bobrules-{slug}`;
  both combine with `customInstructions`.
- **Override a built-in mode** (agent/ask/plan) with a custom mode of the same slug:
  **project > global > defaults**.
- **YAML preferred**; legacy `custom_modes.json` auto-migrates and is still supported.
- **In this repo:** [`custom_modes.yaml`](../../custom_modes.yaml) (six modes, `fileRegex`
  with negative look-ahead, `allowedSubagents`). Guide: [04](../04-custom-modes.md).

## 4.7 Develop Bob skills
- Reusable, **versionable** instruction sets (e.g. review checklist, documentation standard).
- Bob loads a skill's instructions and supporting files **once per conversation** and decides
  activation from the **description**.
- Setup: folder under `.bob/skills/` or `~/.bob/skills/` with `SKILL.md` (YAML front matter:
  required **name** and **description**). **No description → ignored.**
- Supporting files: checklists, templates, reference docs, style guides, scripts in subfolders.
- **Project overrides global** on name collision.
- **Approval:** Bob asks before activating by default; **Settings → Auto-Approve → Skills** skips it.
- **Skills settings tab:** see which skills are loaded and from where (project vs global).
- Effective skills: activation-driving descriptions, focused SKILL.md (move detail to files),
  structured actionable steps.
- *Mode wording:* guide 4.7 says "only in Advanced mode" (Bob v1 wording); 1.4 says Agent mode.
- **In this repo:** nine skills; guide [05](../05-skills.md).

## 4.8 Custom rules: global vs project
- Rules = preferences, constraints, guidelines that steer default behaviour.
- **UI:** Modes → select mode → Edit → **Mode-specific custom instructions** → Save.
- **Files:** `.bob/rules/` (all modes) and `.bob/rules-agent/` or any `rules-{slug}/`;
  global `~/.bob/rules/` (Linux/macOS) or `%USERPROFILE%\.bob\rules\` (Windows).
- **Priority:** global loads first, then workspace. Within each level **mode-specific → AGENTS.md →
  general**. Workspace can override global.
- **AGENTS.md:** workspace root, auto-loaded, version-controlled; disable with
  `"bob-code.useAgentRules": false`.
- **File behaviour:** recursive subfolders, alphabetical order, filters `.DS_Store`, `*.bak`,
  `*.cache`, `*.log`, `*.tmp`, `Thumbs.db`; symlinks to depth 5; empty files skipped.
- **Team standardization:** commit `.bob/rules/`; distribute a shared global-rules repo for
  org standards; or combine both (hybrid).
- **Scoping in a monorepo:** a rule that should apply to one area belongs in **project rules,
  scoped to that subdirectory**, not in global rules or repeated in prompts. Example:
  [`rules/04-ddl-backward-compatibility.md`](../../rules/04-ddl-backward-compatibility.md)
  applies *only* to `qsqlsrc/` and `qddssrc/`.
- Guide: [03 Rules](../03-rules.md).

## 4.9 Generate pull requests from the IDE
- Bob analyzes **branch changes, commit history and branch name** to write a PR title and
  description. You review and edit before submitting.
- **Prerequisites:** changes **committed to a branch** + **push access** to the remote.
- **Start:** PR icon in **Source Control**, the Command Palette (docs: "Bob: Create Pull Request";
  guide: "Bob: Generate PR"), or chat (docs: `/create-pull-request`; guide: `/create-pr`).
- **Flow:** choose **base branch** (Bob suggests the **three most likely**) → remote (if several) →
  review title/description → create → **PR link in chat**.
- **Template search order** (first match wins; several → Bob asks you to choose):
  1. `pull_request_template.md` (root) 2. `docs/` 3. `.github/`
  4. `.github/PULL_REQUEST_TEMPLATE/` 5. `PULL_REQUEST_TEMPLATE/` 6. `docs/PULL_REQUEST_TEMPLATE/`
- **Default template** (none found): branch-derived title, summary, key implementation details,
  testing information, relevant links.
- Iterate in chat as many times as needed before confirming. Use **descriptive branch names**
  and clear template headings and placeholders.
- **In this repo:** [`.github/pull_request_template.md`](../../../.github/pull_request_template.md)
  (position 3 in the search order), with IBM i sections (objects changed, build order, level checks).

---

## Check yourself
<details><summary>1. Which tool group is Ask mode's only file-related group?</summary>Read.</details>
<details><summary>2. At roughly what usage does condensation begin, and what is the cap?</summary>~190,000 tokens; 270,000 hard cap.</details>
<details><summary>3. Does <code>@qrpglesrc/</code> include files in subfolders?</summary>No. Folder mentions are non-recursive.</details>
<details><summary>4. Does an @file mention respect .bobignore?</summary>No. File/folder mentions bypass .bobignore and .gitignore. Git mentions respect .gitignore.</details>
<details><summary>5. Which MCP transport keeps confidential data off the network and runs as a child process?</summary>STDIO.</details>
<details><summary>6. What's required in an STDIO server entry? In a remote one?</summary><code>command</code>; <code>url</code>.</details>
<details><summary>7. A custom mode has no <code>groups</code>. What can it do?</summary>Nothing that needs grouped tools. No access is granted.</details>
<details><summary>8. You have templates in both <code>.github/</code> and <code>docs/</code>. What does Bob do?</summary>It finds more than one and asks you to choose.</details>

**Docs:** [Tools](https://bob.ibm.com/docs/shell/core-concepts/tools) ·
[Context window management](https://bob.ibm.com/docs/shell/core-concepts/context-window-management) ·
[Context mentions](https://bob.ibm.com/docs/ide/features/context-mentions) ·
[MCP in Bob](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-in-bob) ·
[Server transports](https://bob.ibm.com/docs/ide/configuration/mcp/server-transports) ·
[Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
[Skills](https://bob.ibm.com/docs/ide/features/skills) ·
[Custom rules](https://bob.ibm.com/docs/ide/configuration/rules) ·
[Pull requests](https://bob.ibm.com/docs/ide/features/pull-requests) ·
[Updating premium packages](https://bob.ibm.com/docs/ide/premium-packages/updating-premium-packages)
