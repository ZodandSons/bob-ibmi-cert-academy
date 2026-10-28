# Section 3 · Bob use cases (≈19% of the exam)

[Exam home](README.md) · [← Section 2](section-2-core-features.md) · Next: [Section 4 Configuration →](section-4-configuration.md)

Objectives: **3.1** plan before coding · **3.2** literate coding · **3.3** SDLC capabilities ·
**3.4** modes vs skills vs rules vs hooks vs AGENTS.md · **3.5** Shell vs IDE ·
**3.6** Bob alone vs external tools · **3.7** subagents and subtasks · **3.8** modernization ·
**3.9** build AI agents · **3.10** debugging · **3.11** code review and findings

This section is **scenario-based**: "a developer wants X, which approach?" Learn the
*decision*, not just the feature.

---

## 3.1 Create, inspect and refine a plan before coding
- Use **Plan mode** for architecture design, implementation planning and technical specs.
- **Plan mode limitations:** it designs and documents; it **doesn't run commands** and isn't
  meant for implementing code (switch to Agent for that).
- A good planning prompt states **scope, affected layers, constraints, acceptance criteria**.
- **Inspect the plan** for: scope match · decisions · implementation sequence · acceptance
  criteria · **unwanted assumptions**. **Refine** vague language, missing detail, wrong assumptions.
- **Apply the approved plan in Agent mode.**
- **In this repo:** [`/plan-ibmi-change`](../../commands/plan-ibmi-change.md) +
  [`rules-plan/`](../../rules-plan/) (required sections, explicit **Assumption:** markers,
  "Ready for Agent mode").
- **Lab:** Plan mode → `/plan-ibmi-change ORD-101 "add an order priority field to ORDHDR and the order entry screen"`.
  Check the plan against the five inspection points, ask Bob to fix one, then switch to Agent and implement step 1.

## 3.2 Literate coding: create code from comments
- Use it when the change is **local to one file or code block**.
- Write natural-language instructions, pseudocode, annotations or partial code **where the
  code should go** (toggle with **⌘/Ctrl + I**; instructions show in blue; generate with
  **⌘/Ctrl + Enter**).
- **Inspect the inline diff:** accept when it matches the required behaviour, reject when it doesn't.
- **Literate coding vs Agent mode:** in-editor · precise code location · inline diff ·
  **single-file scope**. Choose **Agent mode for multi-file or multi-step** work.
- **Lab:** [`labs/literate-coding-ordtotal.rpgle`](labs/literate-coding-ordtotal.rpgle).

## 3.3 Core SDLC capabilities: understand, generate, modify, document, automate
| Capability | IBM i example in this repo |
|---|---|
| Analyze an unfamiliar codebase | Ask mode: "explain the structure of this repo" → AGENTS.md, `/explain-program` |
| Explain logic without modifying | `/explain-program` (no edits) |
| Generate code from requirements | `/new-rpg-program`, `/new-cl-program` (functions, programs, service programs) |
| Create project artifacts | templates in `skills/*/templates/` (source, config, tests, docs, scaffolding) |
| Modify existing code | `/convert-to-free` (refactoring), repeated-pattern updates |
| Generate tests and docs | `rpgunit-testing` skill, conversion reports, README updates |
| Automate repetitive work | slash commands, `batch-convert.sh` with Bob Shell |
| Precise context | `@file`, `@folder`, `@problems`, `@terminal`, `@git-changes`, `@<url>` (4.3) |
| **Inspect output before accepting** | code diff · test results · build output · command output · manual review |

## 3.4 When to use modes, skills, rules, hooks and AGENTS.md
| Use… | When the use case needs… | Activated by | This repo |
|---|---|---|---|
| **Built-in mode** | Ask = explain, no changes · Plan = design first · Agent = write/fix/run | User | dropdown |
| **Custom mode** | a specialized role, **restricted tools**, team-specific behaviour | **User** | `custom_modes.yaml` |
| **Rules** | persistent guidance: style, docs standards, testing practice, conventions (global / workspace / mode-specific / project) | **Always active** | `rules/`, `rules-*/` |
| **AGENTS.md** | durable **project context** across conversations and modes | Always loaded | `AGENTS.md` |
| **Skill** | a reusable specialized **workflow** with instructions and supporting files | **Bob** (from description) | `skills/` |
| **Hook** | **lifecycle automation** before, during or after Bob activity | Events | `settings.json`, `hooks/` |

One-liners to memorize: **modes shape role and tool access · skills teach reusable workflows ·
rules guide behaviour and output style · hooks automate lifecycle actions · AGENTS.md gives
durable project context.** Real solutions often combine them (see the "Which piece should I
change?" table in [10 IBM i workflows](../10-ibmi-workflows.md)).

## 3.5 Bob Shell vs Bob IDE
- **IDE:** editor-based development, project navigation, file changes, **literate coding**,
  visual review panels, interactive coding.
- **Shell:** terminal-based work, command execution, script automation, **CI/CD**,
  troubleshooting, **log analysis**, non-interactive automation.
- Shell **interactive** (`bob chat`) = conversational terminal problem-solving. Shell
  **non-interactive** (`bob run`) = one-shot prompts, scripting, batch, structured output
  (`--format json`) for pipelines.
- **Lab:** compare `/review-ibmi` in the IDE with `scripts/ci-review.sh` (Shell, CI).

## 3.6 Bob alone vs with specialized tools or external applications
- First decide the objective: explain, plan, generate, modify, automate, or coordinate
  work across external tools.
- Use **MCP tools** for external systems, documentation, APIs, databases, SDKs or
  platform-specific commands.
- **Bob is the development partner; the external application is the execution/runtime system:**
  - Bob generates and validates **Terraform**; Terraform provisions infrastructure.
  - Bob generates streaming artifacts; **Confluent Cloud** hosts Kafka resources.
  - Bob generates/modifies integration artifacts; **webMethods Hybrid Integration** deploys and governs.
  - Bob creates agents; **watsonx Orchestrate** runs and manages them.
  - *IBM i analogue in this repo:* Bob writes RPG/CL and `Rules.mk`; **TOBi + the IBM i**
    compile and run them. Bob queries Db2 for i through MCP; **Db2** executes the SQL.

## 3.7 Subagents and subtasks
- **Subagent** when work is **self-contained**: read-only exploration, searching code,
  summarizing files, finding components, understanding structure.
- Types: **explore** (read-only, lighter model) and **general** (full tool access, default model).
- Pattern for large jobs: **instruct subagents to write results to a temporary directory,
  then collect them** (with another subagent or the main agent). Writing needs *general*
  subagents, because explore is read-only.
- **Subagents:** silent, background, return a **summary**. **Subtasks:** separate **visible**,
  interactive conversation threads with their own tracking.
- Use **subtasks** when the work needs its own visible, interactive thread.
- When several subagents run together, watch them in the **parallel subagents panel**.
- **In this repo:** [`/impact-analysis`](../../commands/impact-analysis.md) (three parallel
  general subagents → `tmp/impact/` → merge) and the `ibmi-reviewer` mode's
  `allowedSubagents: [explore]`.

## 3.8 Modernize applications using Bob
1. **Analyze** the existing app: opportunities, constraints, architecture issues, risk areas.
2. **Inspect** source, config, APIs, schemas, docs, integrations *before* proposing work.
3. **Generate discovery outputs:** structure, business capabilities, dependencies, integration points, candidates.
4. **Create specifications, design artifacts and implementation plans** before code changes.
5. **Pick the pattern:** Java version upgrade · UI modernization · **Liberty replatforming**
   (WebSphere traditional → Liberty) · *(IBM i: fixed → free RPG, DDS → DDL, native I/O → SQL)*.
6. **Inspect** generated specs, plans and proposals before allowing code changes.
7. **Validate** with builds, tests, deployment checks, runtime verification, tool-assisted debugging.
8. Prefer **incremental modernization over big-bang rewrites.**
- **In this repo:** the whole `rpg-fixed-to-free` skill (inventory → convert → verify → report),
  `modernizer` mode, `batch-convert.sh` (one program at a time, verified).

## 3.9 Build AI agents using Bob
- Create the project structure for agents, MCP tools or agentic workflows.
- Generate MCP server code, tool definitions, helpers, tests, docs *(optional)*. **Build an MCP
  client to test tools end to end.**
- Configure Bob to use MCP servers that provide documentation, SDK commands or platform tooling.
- Use **skills across the agent lifecycle:** architecture → implementation → documentation → evaluation.
- Create agentic workflow artifacts from approved specs. **Fix** code, config, tools or **agent
  YAML** when validation finds errors. **Demonstrate end-to-end verification.**
- **In this repo:** `mcp-tools/ibmi-dev-tools.yaml` is a set of agent tools defined in YAML;
  verify them with `npx @ibm/ibmi-mcp-server --list-toolsets`. IBM tutorial:
  [Build agents and MCP tools for watsonx Orchestrate using Bob](https://developer.ibm.com/tutorials/build-agents-mcp-tools-watsonx-orchestrate-using-bob).

## 3.10 Debug application problems with Bob
1. Analyze errors, failed tests, logs, command output or unexpected behaviour.
2. Locate related files, components, functions or services. 3. Diagnose the likely root cause.
4. **Ask mode** to explain/analyze **without file changes**. **Agent mode** for fixes, edits, commands.
5. Modify code/tests/config/docs. 6. **Re-run tests, builds, commands** to confirm.
7. **Inspect after the fix:** test output · build output · logs · runtime behaviour · code diff.
8. Ask Bob to **document the defect, correction and validation**.
- Compare chat-based debugging in Bob IDE with **tool-assisted debugging** (e.g. **Liberty Tools**).
- **In this repo:** workflow D in [10 IBM i workflows](../10-ibmi-workflows.md) (job log via MCP),
  `/build` (compile → read errors → fix → rebuild, max 3 attempts).

## 3.11 Code review and Bob Findings
- Use the **Review workflow** before committing or opening a PR. Start it from the **Review
  panel** or **`/review`**. Pick the **comparison target** (branch dropdown) → **Start Review**.
- Toggle **Include Uncommitted Changes** for local modifications (on by default when
  reviewing your current branch).
- **Issue coverage:** select a GitHub issue to validate the change against it (needs GitHub).
- Inspect results in the **Bob Findings** panel. Click a finding to open the file at the annotated location.
- Reference findings in chat (the exam guide says **`@issues`**; the current docs show
  `@problems` for resolving several at once).
- **Fix with Bob** (Bob creates a fix task) or **Dismiss** irrelevant findings.
- **Review exclusions:** Settings → **Bob Findings** tab → **Review Exclusions** glob patterns
  (e.g. `qrpglesrc/legacy/**`).
- **Combine Bob review with human review** for architecture, intent and final approval.
- **In this repo:** the `ibmi-reviewer` mode and `/review-ibmi` are a *custom* review
  workflow; the built-in Review panel is the product feature tested here.

---

## Check yourself
<details><summary>1. A one-procedure change in a single RPG module: literate coding or Agent mode?</summary>Literate coding: local, single file, inline diff. Multi-file or multi-step → Agent.</details>
<details><summary>2. "Every RPG program must check SQLSTATE." Mode, skill, rule, hook or AGENTS.md?</summary>Rule: persistent coding guidance that is always active.</details>
<details><summary>3. You need a separate, visible thread to track a long migration step. Subagent or subtask?</summary>Subtask. Subagents are silent and return a summary.</details>
<details><summary>4. Bob wrote Terraform. Who provisions the infrastructure?</summary>Terraform. Bob is the development partner, not the runtime.</details>
<details><summary>5. Name the five things to inspect in a generated plan.</summary>Scope match, decisions, implementation sequence, acceptance criteria, unwanted assumptions.</details>
<details><summary>6. How do you stop the built-in review from analyzing generated files?</summary>Settings → Bob Findings → Review Exclusions (glob patterns).</details>

**Docs:** [Modes](https://bob.ibm.com/docs/ide/features/modes) ·
[Literate coding](https://bob.ibm.com/docs/ide/features/literate-coding) ·
[Context mentions](https://bob.ibm.com/docs/ide/features/context-mentions) ·
[Subagents](https://bob.ibm.com/docs/ide/features/subagents) ·
[Code reviews](https://bob.ibm.com/docs/ide/features/code-reviews) ·
[Bob Shell non-interactive](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive) ·
[Java Modernization package](https://bob.ibm.com/docs/ide/premium-packages/java-modernization/java-modernization-index)
