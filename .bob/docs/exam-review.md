## Section 1: Concepts
1. Write effective prompts
```Role, Context, Examples```
```(IRCEC) Instructions, Role, Context, Examples, Cue```
2. Initiate a project (AGENTS.md)
```/init```
3. Why use an MCP server
```Extends Bob's capabilities by providing  a standardized way to interact with external tooling and services```

```Global configuration is stored in ~/.bob/settings/mcp.json, project configuration is stored in .bob/mcp.json, and project configuration takes precedence when server names conflict.```

4. Define and Illustrate the structure of  Bob Skills
```Project skills use <project>/.bob/skills/, global skills use ~/.bob/skills/. A project skill takes precedence when the same skill name exists globally.```

```.bob/skills/<skill-name>/SKILL.md```

```SKILL.md begins with YAML front matter containing at least name and description, followed by the operational instructions Bob receives when the skill is activated. ```

```Supporting resources can include checklists, templates, reference documentation, configuration examples, scripts, utilities, and style guides. ```

```(RETS) /reference, /examples, /templates, /scripts```

```Bob uses the skill description to determine when the skill is relevant and loads its instructions and supporting resources when activated. ```

```
---
name: <skill-name>
description: <skill-description>
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <OBJECT>
---

workflow steps:

<Steps>
<Step></Step>
<Step></Step>
<Step></Step>
</Steps>
```

## Section 2: Bob Core Features
1. Use Bob file's system to read, create and modify project files
```Bob's file-system capability lets it read, create, and modify files directly inside a project without leaving the IDE```

```Use Bob's read tools to inspect files and structure without changing anything: read_file, glob, grep, list_files, GetSymbolsOverview, FindSymbol, indReferencingSymbols — the only tool group available in the read-only, least-privilege Ask mode.```

2. Highlight the purpose of the IBM Premium Packages
```Upgrade either manually in the extensions view or install from a VSIX file```
```IBM Bob Premium Packages are optional, specialized add-ons that extend Bob's core AI development capabilities with platform-specific knowledge, tools, skills, modes, and automated workflows.```

```
IBM i Premium Package specifically offers:
1. Native IBM i connectivity — Work directly with QSYS source members, compile programs,execute SQL and test changes.
2. Specialized modes — IBM i Developer and Database modes.
3. Prebuilt skills — Document, generate, refactor and test IBM i applications.
4. Modernization workflows — RPG fixed-to-free conversion, DDS-to-DDL modernization and related activities.
5. IBM i knowledge — Platform-specific RAG resources to improve answers and reduce reliance on general LLM knowledge.
```

3. Define the role of .bobignore
```File in the repo root: Specify files Bob may not read or edit```
```Exact syntax as `.gitignore` ```
4. Define and differentiate between the 3 default Bob modes
```A common development workflow for modes is: Plan, Agent, Ask```
```Plan:  Planning and designing (analyzes requirements, researches and designs implementation steps)```
```Agent: Writing and modifying code (Use this mode when you need to write, modify, or refactor code.) ```
```Ask: Getting information and explanations (Use this mode when you need explanations, documentation, or answers to technical questions)```
5. Add a Custom Mode
```Go to Bob setting -> Modes to create a custom mode from the UI ```
```global-level custom mode in code by going to`~/.bob/settings/custom_modes.yaml` ```
```Manage project-level custom mode in code by going to`.bob/custom_modes.yaml` ```
```Mode specfic Rules can be created by adding a folder `.bob/rules-<mode>` ```
6. How Bob selects LLM models
```Bob automatically selects the most appropriate model for each task.```
```Factors: task complexity, required capabilities, context size, cost optimization```
7. Use Bob shell to perform AI-Assisted activities from the command line
```Bob Shell is Bob in your terminal.```
```Use Bob Shell for: CI/CD pipelines, batch processing, and unattended automation```
```It reads the same .bob folder as the IDE```
```It's also how you put Bob into scripts and CI pipelines```
```export BOB_API_KEY=.... bob run requires it.```
```bash: bob chat```
```bash: bob run```
```Shell Mode: the ! prefix allows you to execute operating-system commands directly from the Bob command-line interface, rather than asking the AI agent to interpret and execute them.```
```When you prefix a command with !, Bob treats it as a shell command instead.  Example:  !git status```
8. Define the component of Bob architecture
```Agent, Harness, Clients```
```One agent, one harness, many clients.```
```Agent (reasoning + code generation), Harness (runtime: auth, logging, telemetry, tool loop), Clients (IDE, Shell…).```
9. Explain IBM Bob as AI Development partner across the SDLC
```IBM Bob augments your existing workflows and helps you understand, plan, improve, and work confidently with real codebases while offering proactive insights that keep you in control every step.```

```
The SDLC is planning/discovery, design, coding, testing, deployment, operations, and
modernization.
o Bob modes support SDLC and different modes should be used for different parts of SDLC
o SDLC sets Bob apart from ‘vibe coding’
o Governance and security layer goes along side Bob SDLC
```
10. Describe Bob hybrid deployment capabilities
```IBM Bob supports hybrid AI-assisted engineering, allowing organizations to combine cloud-based AI capabilities with privately managed infrastructure while maintaining control over security, data residency, and development workflows.```
```Hybrid deployment allows organizations to introduce AI-assisted engineering without requiring every component of their development environment to move to the public cloud.```
11. Monitor Bob usage, activities, and Bobcoin consumption using Bobalytics
```Bobcoins are the consumption-based billing metric used for Bob plans. ```
```Tokens: The raw units of model usage. ```
```Bobcoins: IBM's billing metric that abstracts token usage into a predictable cost structure.```
``` One Bobcoin represents a standardized number of computational resources.```
12. Explain how Bob optimize tokens consumption (intelligent routing)
```Bob optimizes token and cost consumption primarily through multi-model orchestration.```
```Intelligent Routing = Automatic Model Selection Based on Task Complexity, Capabilities, Context, and Cost.```
```IBM Bob uses intelligent routing to automatically select the most cost-effective LLM based on **task complexity**, **optimizing token consumption** and **performance.**```
13. Identify different ways of using Code Functions (CTRL + i, CTRL + K, CTRL + L)
```Access Bob's AI-powered code actions that provide quick fixes, refactoring, and code explanations directly in the Bob IDE through lightbulb icons and context menus. ```
```Write code with AI assistance directly in your editor using natural language instructions right where the code should go. ```
```
Code Functions allow developers to invoke Bob's AI capabilities directly from the code editor.
1. Explain Code — Understand existing code, logic, and functionality.
2. Improve Code — Refactor or optimize code for readability, maintainability, and performance.
3. Fix Code — Identify and correct errors or potential defects.
4. Generate Documentation — Create documentation for selected code.
5. Generate Tests — Create unit tests for existing code.
6. Custom Code Functions — Define reusable AI actions with custom prompts.
```

14. Integrate Bob with external tools and services through MCP and supported  integrations
```.bob/mcp.json```
```~/.bob/settings/mcp.json```

Global configuration is stored in ```~/.bob/settings/mcp.json```, project configuration is stored in ```.bob/mcp.json```, and project configuration takes precedence when server names conflict.

15. Identify what components fill the context window
```
Context window is filled with (STMRSM):
o System prompts
o Tool definitions
o MCP tools
o Rules
o Skills
o Messages
```
```Each task has a certain token limit, which can be viewed in the token breakdown window```
```Start a new context window each task ```

16. Standardize Bob behavior with Rules
```Rules can be global or project level```
```Rules can cover all work or mode-specific```
```Mode specfic Rules can be created by adding a folder `.bob/rules-<mode>` ```

## Section 3:Bob Use Cases
1. Create, inspect, and refine a solution architecture and implementation plan before coding
```Agent Plan Mode```
2. Use literate code to create code from comments
```CTRL + i```
3. Apply Bob core SDLC capabilities to understand, generate, modify, document, and automate development workflows
Bob covers the full SDLC by using:  (Plan, Agent, Ask)
- Ask mode to understand unfamiliar code,
- slash commands (/new-rpg-program) to generate code,
- Agent mode to modify it,
- rpgunit-testing skill and Code Functions to document and test it
- Bob Shell (bob run / batch-convert.sh) to automate repetitive workflows in scripts and CI/CD pipelines.
4. Distinguish when to use Modes, Skills, Rules, Hooks, and AGENTS.md
- Modes — Shape Bob's role and tool access (Ask = explain, Plan = design, Agent = write/fix/run).
- Skills — Teach Bob a reusable, specialized workflow with instructions and supporting files, activated automatically by Bob from the description.
- Rules — Provide persistent, always-active guidance on style, standards, and conventions (global, project, or mode-specific).
- Hooks — Automate lifecycle actions triggered by events before, during, or after Bob activity.
- AGENTS.md — Gives Bob durable project context (what the system is, layout, key objects) that persists across every conversation and mode.
5. Evaluate when to use Bob Shell versus Bob IDE
- Bob IDE — interactive editor-based development: writing, modifying, reviewing, and navigating code.
- Bob Shell — terminal automation: CI/CD pipelines, batch processing, scripts, and non-interactive one-shot tasks (bob run).
6. Evaluate when Bob should work alone versus with specialized tools or external applications
- Bob alone when the task is pure AI reasoning (explain, generate, modify, document);
- Specialized tools/MCP when the task requires executing against an external system (database, platform API, infrastructure) — Bob is the development partner, the external tool is the execution engine.
7. Use subagents and subtasks to divide complex development work into focused parallel workstreams
- Subagents for silent, self-contained background work (explore codebases, summarize files) that returns a summary;
- Subtasks for visible, interactive conversation threads that need their own tracking and user involvement.
8. Modernize applications using Bob
- Bob modernizes applications by using specialized skills and modes (e.g., fixed-to-free RPG conversion, DDS-to-DDL migration) to systematically refactor legacy code into modern standards while preserving business logic — with side-by-side comparison and RPGUnit tests to verify no behaviour changed.
9. Build AI agents using Bob
- Use Bob to generate the project structure, MCP server code, tool definitions, and agent YAML from approved specs, then configure Bob to consume those MCP tools end-to-end
- Bob builds the agent artifacts while a platform like watsonx Orchestrate runs and manages them at runtime.
10. Debug application problems and correct code defects with Bob debugging and documenting code
- Use Bob's Fix Code function (Ctrl+i) with @problems, @terminal, or @git-changes context to identify and correct defects, then use Generate Documentation to document the fix — keeping diagnosis, correction, and documentation in one AI-assisted workflow.
11. Utilize Code Review and Bob Findings
- Run the Review panel (or /review) against a comparison branch to generate Bob Findings, then inspect annotated issues in the Findings panel, fix them with "Fix with Bob" or dismiss them, and combine with human review for final approval before committing or opening a PR.

## Section 4: Bob Configuration
1. Familiarize self with tools: Read, command, subtask, MCP
- Read tools — read_file, glob, grep, list_files, GetSymbolsOverview, FindSymbol, FindReferencingSymbols — let Bob inspect files and code structure without making any changes.
- Command tools — slash commands like /review or /new-rpg-program — invoke predefined, reusable AI workflows stored in ```.bob/commands/``` or ```~/.bob/commands/```.
- Subtask tool — ```start_subtask``` — opens a new, visible, interactive conversation thread so complex work can be tracked and broken into focused steps.
- MCP tools — tools registered via ```.bob/mcp.json``` or ```~/.bob/settings/mcp.json``` — extend Bob's capabilities by connecting it to external systems and services (databases, APIs, IBM i) through the Model Context Protocol.
2. Configure task limits for Bob coins
- Bob's task limits for Bobcoins are configured in Settings → Bob → Task Limits, where you can set a maximum Bobcoin budget per task to prevent runaway consumption.  (Max Turns and Max Cost/Coins)
3. Utilize context mentions @ file
- @file context mentions let you pin specific files, symbols, or resources directly into Bob's context window so it reasons against the exact content you choose rather than whatever it happens to find.
4. Download extensions from marketplace
- Bob extensions (including premium packages like the IBM i Premium Package) are installed from the VS Code / IDE marketplace via the Extensions view, or offline from a VSIX file.
5. Distinguish between local and remote MCP server deployment / transport options
- STDIO: Local MCP servers run as a child process on your machine (stdio transport)
- SSE or HTTP: Remote MCP servers run elsewhere and are reached over the network (SSE or HTTP transport), configured respectively
6. Develop and add MCP tools to environment
- You build a custom MCP server (using the registerTool API), then register it in .bob/mcp.json (project) or ~/.bob/settings/mcp.json (global) so Bob discovers and exposes its tools in every conversation.
7. Create a custom Bob Modes
- A custom Bob mode is defined in .bob/custom_modes.yaml (project-level) or ~/.bob/settings/custom_modes.yaml (global), specifying a name, id, roleDefinition, allowedTools, and optional permission groups to shape Bob's role and tool access for a specific workflow.
8. Develop Bob skills
- A Bob skill is created by adding a SKILL.md file under ```.bob/skills/<skill-name>/``` or ```~/.bob/skills/<skill-name>/``` with a YAML front matter block (containing at least name and description) followed by the operational instructions Bob receives when that skill is activated.
9. Create custom Bob rules global vs project
- Global rules live in ```~/.bob/rules/``` and apply to every workspace, while project rules live in ```.bob/rules/``` (or ```.bob/rules-<mode>/``` for mode-specific rules) and apply only to that project — with project rules taking precedence when both exist.
10. Generate pull requests and PR descriptions directly from your IDE
- Bob's Create Pull Request workflow (/create-pr or the PR workflow) generates a PR description from your git diff using any configured PR templates, lets you review and edit it, then creates the pull request on GitHub directly from the IDE.

## Section 5: Bob Accounts
1. Administer Bobalytics
- Bobalytics is Bob's usage dashboard where you monitor and administer AI consumption — tracking Bobcoin spend, token usage, and developer activity metrics across your organization's Bob account.
2. Authenticate with API
- Authenticating with the API means providing your BOB_API_KEY environment variable (or configuring it in Bob's settings) so that Bob Shell and CI/CD pipelines can make authenticated requests to the Bob service without interactive login.
3. Determine the features of enterprise plan
- The Enterprise plan gives your organization a centralized admin dashboard (at bob.ibm.com) with user/team management, SSO/SAML/OIDC identity provider integration, per-team Bobcoin budget allocation with overage limits, Bobalytics analytics (adoption rate, Bob Factor, spend), API key management for all users, data residency controls, and priority IBM support — all features not available on individual plans.
4. Define Bob Coins
- Bobcoins are IBM's consumption-based billing metric that abstracts raw LLM token usage into a predictable cost unit — one Bobcoin represents a standardized amount of computational resources, letting organizations budget and track AI spend without dealing with model-specific token counts directly.
5. Understand Token Usage for Prompting
- Token usage for prompting refers to how every element placed in Bob's context window — system prompts, tool definitions, MCP tools, rules, skills, and conversation messages — consumes tokens from the task's limit, so understanding what fills the context window helps you write efficient prompts and avoid hitting the token ceiling.
6. Understand the Bob Factor Metric
- The Bob Factor is a metric that measures the percentage of committed lines of code attributed to IBM - Bob's AI-assisted development.
It helps organizations quantify IBM Bob's contribution to their software development activities based on actual Git commits rather than simply measuring how frequently developers use Bob.
\[
\text{Bob Factor}=\frac{\text{Committed lines created by Bob}}{\text{Total committed lines}}\times100
\]

## Section 6: Bob Security
1. Modify mode permissions in a context/task
- You modify mode permissions within an active context/task by clicking the Permissions button in the chat panel and toggling the Read, Edit, Execute, Skill, and MCP checkboxes — changes made this way apply only to that task, while global defaults are set under Settings → Tool Auto-approval.
2. Reduce content poisoning
- Context poisoning occurs when wrong or irrelevant information enters the context window and corrupts all subsequent responses; you reduce it by starting a new task (+), pasting only the specific content Bob needs, splitting unrelated steps into separate tasks, and trusting runnable tests over stale comments or log dumps.
3. Identify and enable correct Permissions restrictions for projects
- Project-level permission restrictions are configured in .bob/settings.json using allowedTools to whitelist tool groups (read, edit, execute, mcp, skill) per mode, and enforced at the task level via the Permissions button in the chat panel — ensuring Bob only has the access each project and workflow actually requires.
4. Produce .bobignore file
- A .bobignore file sits in the repo root, uses the exact same syntax as .gitignore, and lists paths that Bob may never read or edit — for example, blocking credentials, private keys, and generated build artifacts from ever entering Bob's context.

Example:
```
# Secrets and credentials
.env
*.pem
*.key
secrets/

# Build artifacts
target/
*.class

secrets/        # ignore the entire secrets/ folder
!secrets/docs/  # but allow Bob to read secrets/docs/
```
5. Apply correct permissions and understand approval workflows
- Bob's approval workflow requires explicit confirmation before each tool action (read, edit, execute, MCP) unless auto-approved — you apply correct permissions by enabling only the tool groups a task genuinely needs via the Permissions button (task-scoped) or Settings → Tool Auto-approval (global default), keeping execute and MCP off by default to minimize risk.
6. List the best security practices and capabilities for developing with Bob
- Bob's security best practices:
  - Use .bobignore to block sensitive files from Bob's context
  - Start with minimal permissions — only enable Read, Edit, Execute, MCP as each task actually requires
  - Never auto-approve Execute or MCP in production environments
  - Review all generated content before implementing it
  - Use AGENTS.md, rules, and hooks (e.g. guard-dangerous-commands.py) to enforce project guardrails
  - Store secrets in environment variables — never hard-code credentials in source
  - Use dedicated workspaces for sensitive projects
  - Keep Bob and dependencies up to date
  - Train team members to recognize AI-assisted security risks
  - Prepare an incident response process for AI-assisted workflows
7. Rollback changes
- Rolling back changes with Bob means using standard git commands (git revert, git checkout, git reset) since Bob writes directly to your working tree — Bob's own checkpoint is the git history, so every AI-assisted change is reversible as long as you commit regularly and review Bob's changes before committing.