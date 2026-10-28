# Section 2 · Bob core features (≈23% of the exam, the largest section)

[Exam home](README.md) · [← Section 1](section-1-concepts.md) · Next: [Section 3 Use cases →](section-3-use-cases.md)

Objectives: **2.1** file system · **2.2** custom mode · **2.3** premium packages ·
**2.4** .bobignore · **2.5** three default modes · **2.6** LLM selection · **2.7** Bob Shell ·
**2.8** architecture · **2.9** SDLC partner · **2.10** Bobalytics/Bobcoins ·
**2.11** intelligent routing · **2.12** code functions · **2.13** MCP integration ·
**2.14** context window · **2.15** rules

---

## 2.1 Use Bob's file system to read, create and modify project files
- Bob reads, creates and modifies files **inside the project without leaving the IDE**.
- In the IDE you can clone a repo and check out a branch, open folders and files, and
  navigate the file panel. Bob can also find files for you.
- **Read tools** inspect without changing anything: `read_file`, `glob`, `grep`,
  `list_files`, `GetSymbolsOverview`, `FindSymbol`, `FindReferencingSymbols`. The
  **read** group is the only tool group of the read-only, least-privilege **Ask** mode
  (Ask also has MCP/skill/mode access for lookups, but nothing that changes files).
- **Write tools:** `write_file` / `write_to_file`, `apply_diff`, `insert_content`, `search_and_replace`.
- **In this repo:** the hook matchers in [`settings.json`](../../settings.json) target the
  write tools by name; see [08 Hooks](../08-hooks.md).

## 2.2 Add a custom mode
- **Why:** specialization, safety (restrict commands/files), team collaboration, experimentation.
- **Components:** slug, name, role definition, when to use (opt.), available tools (groups),
  custom instructions (opt.), description (opt.), allowed subagents (opt.).
- **Create:** Settings → **Modes** → **+** (saved as YAML), or edit the files:
  project `.bob/custom_modes.yaml` (version-controlled, team-shared), global
  `~/.bob/settings/custom_modes.yaml` (personal).
- Use **project** scope for team/repo-specific modes and **global** for personal ones.
- **In this repo:** six modes in [`custom_modes.yaml`](../../custom_modes.yaml), fully
  commented. Guide: [04 Custom modes](../04-custom-modes.md). Deeper config facts in 4.6.

## 2.3 Purpose of IBM premium packages
- **Optional add-ons** that extend Bob with specialized capabilities for **specific platforms
  and modernization workflows**: **Java Modernization**, **Z**, **i**.
- Bob checks your subscription's **entitlements at launch**. If an entitled package isn't
  installed, a notification offers **Install**.
- Update in the **Extensions** view (Update / version history) or **Install from VSIX…**
  (VSIX from the Open VSX Registry).
- The **Premium Package for i** adds direct work with QSYS source members and IFS files, an
  IBM i developer persona (RPG, COBOL, CL, DDS, SQL), a database mode, and roughly 40
  IBM i skills/workflows (including fixed-to-free conversion) plus about 30 tools. *This repo
  shows how to build similar capabilities yourself with skills, modes and MCP; the
  package delivers them ready-made.*
- Pricing page (Oct 2026): Java Modernization $20/month, IBM i $40/month, IBM Z enterprise
  only. A subscription is required to trial one.

## 2.4 Role of .bobignore
- Specifies files/directories Bob **should not access or modify**. Created in the
  **workspace root**, **same syntax as `.gitignore`**.
- Purposes: protect sensitive information, prevent accidental changes to build artifacts
  or large assets, define Bob's operational scope.
- **Limitations (frequently tested):**
  - Workspace-only: files outside the workspace root aren't affected.
  - `execute_command` is checked only for a **predefined list of file-reading commands**;
    custom scripts or unusual utilities may not be caught.
  - **The exam guide notes `insert_content` and `search_and_replace` might write to ignored
    files** due to a save-mechanism limitation.
  - **Not a full sandbox.**
- **In this repo:** [`.bobignore`](../../../.bobignore) (commented). Guide:
  [02](../02-agents-md-and-bobignore.md). Also 6.4.

## 2.5 The three default modes
| Mode | Primary purpose | Changes files? |
|---|---|---|
| **Agent** | Writing and modifying code (also debugging, refactoring, running commands) | Yes |
| **Plan** | Planning and designing (architecture, implementation plans) | Writes plans/docs; no command execution |
| **Ask** | Information and explanations | **No**: read-only |

- Common workflow: **Plan → Agent → Ask** (Ask when needed, e.g. to understand something
  without risking code changes).
- **Permissions can be changed per context window / task** for the workflow. They reset when
  a new context window (task) is opened. See 6.1.
- Switch with the mode dropdown, **⌘/Ctrl + .**, `/mode` in Bob Shell, or let Bob suggest a switch.
- **In this repo:** rules for each built-in mode in `rules-agent/`, `rules-plan/`, `rules-ask/`.

## 2.6 How Bob selects LLM models
- **Bob SaaS users cannot manually pick the LLM.** Bob automatically selects the most
  appropriate model for each task.
- Factors: **task complexity** (simple → faster, cheaper models), **required capabilities**
  (specialized tasks → models with those strengths), **context size** (large codebases →
  extended context windows), **cost optimization**.

## 2.7 Use Bob Shell from the command line
- Interactive: **`bob chat`** (or `bob`). Non-interactive: **`bob run "…"`** (needs `BOB_API_KEY`).
- **Interactive** for exploratory/debugging work where you review changes. **Non-interactive**
  for CI/CD, batch processing and unattended automation.
- **Cost control in automated runs:** `--max-cost <bobcoins>`, `--max-turns <n>`, plus
  restricted `--mode` / `--disable-tool-groups`.
- **Shell mode `!`:** pressing `!` on an empty input toggles shell mode so you can run
  shell commands from inside Bob Shell, e.g. to reproduce and diagnose a failing command.
- **In this repo:** [09 Bob Shell](../09-bob-shell.md) and
  [`skills/bob-shell-automation/`](../../skills/bob-shell-automation/SKILL.md).

## 2.8 Components of Bob's architecture
Bob v2 is built on **one agent, one harness, many clients**:

| Component | Role |
|---|---|
| **Agent** | Reasoning and code generation: the "brain" that plans and decides which tools to use |
| **Harness** | The runtime around the agent that handles ancillary capabilities such as authentication, logging and telemetry (and runs the tool loop) |
| **Clients** | The user interfaces (Bob IDE, Bob Shell, and more planned) that all share the same agent and harness |

Why it matters: the agent behaves **consistently across clients**, and improvements ship
once instead of twice. That's why `.bob/` works identically in the IDE and Shell.

## 2.9 Bob as AI development partner across the SDLC
- Bob works across the **whole SDLC**: planning/discovery, design, coding, testing,
  deployment, operations, modernization. Not just autocomplete or "vibe coding".
- Different modes fit different phases (Plan → design, Agent → code/test, Ask → understand).
- A **governance and security layer** goes alongside (modes, permissions, rules, hooks, Bobalytics).
- Exam-style example: planning and implementing complex features, creating commits and
  pull requests, and modernizing applications. **Not** hosting repos or HR/payroll.
- **In this repo:** [10 IBM i workflows](../10-ibmi-workflows.md) walks plan → code →
  review → build → operate.

## 2.10 Monitor usage and Bobcoins with Bobalytics
- **Bobcoins** = Bob's consumption-based billing metric (individual and enterprise tiers).
- **Tokens** = raw model usage units. **Bobcoins** abstract tokens into a predictable cost
  (1 Bobcoin = a standardized amount of compute; billed at **$0.50 USD**).
- Monitor: **hover the gauge** (top-right of the Bob panel) · **Settings → General** ·
  **Bobalytics** for patterns over time.
- **Bobalytics** (admin settings; Enterprise): KPIs, **Adoption rate**, token/consumption use,
  **Bob factor** (Bob's contribution to committed code), **Bobcoin spend**. Helps justify AI
  use to stakeholders.
- **Privacy:** team-level insights **without exposing individual user data**. Admins cannot
  access a specific user's data from team-level charts. Details in [Section 5](section-5-accounts.md).

## 2.11 How Bob optimizes token consumption (intelligent routing)
- **Multi-model orchestration:** each task is dynamically routed to a *suitable* model
  instead of always the most capable (most expensive) one → lower cost, faster simple tasks.

## 2.12 Different ways of using code functions
- **Code actions** in the editor: **lightbulb icon**, **right-click → Bob**, **⌘/Ctrl + .**,
  Command Palette ("Bob: …"). Actions: **Add to Bob Context**, **Explain with Bob**,
  **Improve with Bob**, **Inline Chat** (⌘/Ctrl + K), **Move to Chat** (⌘/Ctrl + L).
- **Literate coding:** write natural-language instructions *in the editor where the code
  should go* and Bob generates it (details in 3.2).

## 2.13 Integrate Bob with external tools through MCP
- MCP is the standardized **client-server** protocol Bob uses to reach external tools,
  using **JSON-RPC 2.0**. Bob (host/client) connects to MCP servers that expose tools.
- Managed **globally or per project**.
- **MCP can use a lot of tokens:** every connected tool's definition sits in the context
  window, so connect only what the use case needs (2.14, 4.2).
- **In this repo:** [07 MCP servers](../07-mcp-servers.md).

## 2.14 Define and identify the context window
- Filled with **six categories:** **system prompt, tool definitions, MCP tools, rules,
  skills, messages.**
- Monitor usage in the indicator **above the agentic chat**; open the **context window
  breakdown** to see each category.
- Each task has a token limit (270,000) visible in the breakdown. **Start a new context
  window (task) for each new task.**
- Full detail in [Section 4.2](section-4-configuration.md#42-utilize-context-window-management).

## 2.15 Standardize Bob behaviour with rules
- **Custom rules** = persistent plain-text instructions. **Global or project** level;
  **all modes or mode-specific**. Bob reads and follows them. They enforce best practices
  and corporate/development patterns.
- **In this repo:** [`rules/`](../../rules/) and five `rules-{slug}/` folders.
  Guide: [03 Rules](../03-rules.md). Deeper config facts in 4.8.

---

## Check yourself
<details><summary>1. A colleague wants Bob to explain a legacy RPG program with zero risk of edits. Which mode?</summary>Ask: read-only, least privilege.</details>
<details><summary>2. Can a Bob SaaS user force a specific LLM for a hard refactor?</summary>No. Bob selects models automatically (complexity, capabilities, context size, cost).</details>
<details><summary>3. Name the three parts of Bob v2's architecture and one job of each.</summary>Agent: reasoning and code generation. Harness: authentication, logging, telemetry, tool execution. Clients: the user interfaces (IDE, Shell).</details>
<details><summary>4. List the six context window categories.</summary>System prompt, tool definitions, MCP tools, rules, skills, messages.</details>
<details><summary>5. Your nightly script calls <code>bob run</code>. Name two cost controls.</summary><code>--max-cost</code> and <code>--max-turns</code> (plus a restricted <code>--mode</code> or <code>--disable-tool-groups</code>).</details>
<details><summary>6. Where do you install an IBM premium package from a file?</summary>Extensions panel → "…" → Install from VSIX….</details>

**Docs:** [Modes](https://bob.ibm.com/docs/ide/features/modes) ·
[Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
[Premium packages](https://bob.ibm.com/docs/ide/premium-packages/pkg-index) ·
[Updating premium packages](https://bob.ibm.com/docs/ide/premium-packages/updating-premium-packages) ·
[Ignoring files](https://bob.ibm.com/docs/ide/configuration/bobignore) ·
[Bobcoins](https://bob.ibm.com/docs/ide/account/bobcoins) ·
[Bobalytics](https://bob.ibm.com/docs/ide/features/bobalytics) ·
[Code actions](https://bob.ibm.com/docs/ide/features/code-actions) ·
[Understanding MCP](https://bob.ibm.com/docs/ide/configuration/mcp/understanding-mcp) ·
[Bob Shell keyboard shortcuts (`!`)](https://bob.ibm.com/docs/shell/configuration/keyboard-shortcuts) ·
[Bob 2.0 architecture (IT Jungle)](https://www.itjungle.com/2026/07/13/big-blue-ships-bob-2-0-and-premium-package-for-ibm-i/)
