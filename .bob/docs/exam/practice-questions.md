# Practice questions: C3000-006 IBM Bob v2 Developer – Associate

[Exam home](README.md) · Interactive version: `python3 .bob/docs/exam/quiz/quiz.py --exam`

77 original questions, weighted like the exam. Each answer is hidden under
"Answer". Try first, then expand. *Generated from `quiz/questions.yaml`; edit that file,
then run `python3 quiz.py --export-md ../practice-questions.md`.*

## Section 1 · Concepts (17%, 13 questions)

**1-01** · Objective 1.1: Which list contains the five prompt components recommended for effective Bob prompts?

- a) System prompt, tools, MCP, rules, messages
- b) Goal, scope, budget, deadline, owner
- c) Instruction, role, context, example, cue
- d) Read, edit, execute, MCP, skill

<details><summary>Answer</summary>

**c**. The five components are instruction, role, context, example and cue. "System prompt, tools, MCP, rules, messages" is the context-window list and "read, edit, execute..." is tool groups, both common distractors. [Study](section-1-concepts.md#11-write-effective-prompts)

</details>

**1-02** · Objective 1.1: A developer wants a new CL program to follow the same error-handling structure as the team's best existing CL program. Which prompt best applies the "example" practice?

- a) Create qcllesrc/ordpurge.pgm.clle following the structure of @qcllesrc/ordnight.pgm.clle.
- b) Act as a senior IBM i systems programmer and write the program.
- c) Write a CL program with good error handling.
- d) Search the internet for good CL error-handling patterns.

<details><summary>Answer</summary>

**a**. Pointing Bob at a specific, well-written file in the codebase is the example practice. "Act as a senior..." is a role, searching the internet brings in generic outside content, and "good error handling" is vague. [Study](section-1-concepts.md#11-write-effective-prompts)

</details>

**1-03** · Objective 1.1: A prompt says "Fix the order program." Which change makes it most specific?

- a) Name the file and lines, the exact error, the expected behaviour, what must not change, and how completion is verified.
- b) Switch to Ask mode before sending the same prompt.
- c) Ask Bob to read the whole repository first so it has all the context.
- d) Add "please" and "carefully" to the request.

<details><summary>Answer</summary>

**a**. Specificity means stating the exact task, outcome and relevant constraints (file scope, expected behaviour, completion criteria). Reading the whole repo wastes tokens and can poison context. [Study](section-1-concepts.md#11-write-effective-prompts)

</details>

**1-04** · Objective 1.1: Converting a 3,000-line fixed-format RPG program, adding unit tests and updating the build in one prompt keeps producing incomplete results. Which prompting practice helps most?

- a) Pasting the full program source into the chat
- b) Asking Bob to "try harder"
- c) Task decomposition into smaller steps, each with a clear objective
- d) Adding a stronger role statement

<details><summary>Answer</summary>

**c**. Complex work should be split into manageable steps with clear objectives (e.g. inventory, convert, verify, test, build). [Study](section-1-concepts.md#11-write-effective-prompts)

</details>

**1-05** · Objective 1.1: Why should a developer use "@qrpglesrc/ordentry.pgm.sqlrpgle:120-160" instead of asking Bob to look at the whole qrpglesrc folder?

- a) Line ranges make Bob switch to Agent mode.
- b) It gives Bob precisely the relevant code without loading unnecessary repository content.
- c) It bypasses the approval prompt.
- d) Folder mentions are not supported in Bob.

<details><summary>Answer</summary>

**b**. @ context mentions point Bob at specific files or code, keeping the context window lean and the answer focused. [Study](section-4-configuration.md#43-context-mentions-)

</details>

**1-06** · Objective 1.2: What does running /init do?

- a) Installs Bob Shell and its dependencies
- b) Scans the project and generates AGENTS.md context files so Bob learns its structure, technologies, conventions and workflows
- c) Creates a new Git repository for rollback snapshots
- d) Resets all custom modes to defaults

<details><summary>Answer</summary>

**b**. /init initializes persistent project context by generating the root AGENTS.md and mode-specific AGENTS.md files. [Study](section-1-concepts.md#12-initiate-a-project-agentsmd)

</details>

**1-07** · Objective 1.2: A team wants Ask mode, in this project only, to always explain IBM i terms the first time it uses them. What is the most direct way?

- a) Built-in modes cannot be changed
- b) Create a new custom mode called ask2
- c) Add the guidance to every prompt
- d) Add the guidance to Ask mode's AGENTS.md (rules) file inside .bob

<details><summary>Answer</summary>

**d**. Built-in modes have mode-specific AGENTS.md / rules files inside .bob (rules-ask/). Editing them customizes the mode without creating a new one. [Study](section-1-concepts.md#12-initiate-a-project-agentsmd)

</details>

**1-08** · Objective 1.2: The project moved from DDS to SQL DDL and reorganized its source folders. What should the team do with AGENTS.md?

- a) Delete it; Bob reads the code directly
- b) Re-run /init, then re-add business and team conventions the scan cannot detect
- c) Nothing; AGENTS.md updates itself every session
- d) Move it into .bob/skills/

<details><summary>Answer</summary>

**b**. Re-run /init after significant structural, framework or technology changes, and manually keep conventions that automated scanning misses. [Study](section-1-concepts.md#12-initiate-a-project-agentsmd)

</details>

**1-09** · Objective 1.3: What is the main benefit of MCP compared with building custom integrations?

- a) It makes Bob free to use
- b) It provides one standardized interface so Bob does not need a unique integration for every external system
- c) It encrypts all source code automatically
- d) It replaces the need for an IDE

<details><summary>Answer</summary>

**b**. MCP is a standard protocol (the "USB-C port" analogy) that extends Bob with external tools and data without modifying Bob's core. [Study](section-1-concepts.md#13-why-use-an-mcp-server)

</details>

**1-10** · Objective 1.3: A developer's global MCP config and the project's .bob/mcp.json both define a server named "ibmi-mcp" with different settings. Which is used in that project?

- a) Neither; Bob reports an error
- b) The global definition
- c) The project definition
- d) Both, merged field by field

<details><summary>Answer</summary>

**c**. Project MCP configuration takes precedence when server names conflict. [Study](section-1-concepts.md#13-why-use-an-mcp-server)

</details>

**1-11** · Objective 1.4: Which TWO items are required in a skill's SKILL.md front matter? (Select two)

- a) name
- b) author
- c) version
- d) description
- e) mode

<details><summary>Answer</summary>

**a, d**. SKILL.md needs YAML front matter with at least name and description. A skill without a description is ignored. [Study](section-1-concepts.md#14-structure-of-bob-skills)

</details>

**1-12** · Objective 1.4: How does Bob decide to activate a skill?

- a) Skills activate only from hooks
- b) The user must type /skill-name every time
- c) Bob compares the request with each skill's description and loads the relevant one
- d) All skills load at the start of every conversation

<details><summary>Answer</summary>

**c**. Bob uses the description to determine relevance, then loads the instructions (once per conversation) and can read supporting files. Rules are always active; skills are activated by Bob. [Study](section-1-concepts.md#14-structure-of-bob-skills)

</details>

**1-13** · Objective 1.3: A team wants to connect a community MCP server that can run SQL against production. What is the main security consideration?

- a) MCP servers cannot access external systems, so there is no risk
- b) MCP servers are sandboxed by .bobignore
- c) Only the server's name must be unique
- d) Adding a server expands what Bob can read or do, so it needs authentication, encryption, access controls and auditing

<details><summary>Answer</summary>

**d**. Every MCP server widens Bob's reach into the systems it can access. Trusted deployments use authentication, encryption, access controls and auditing; prefer read-only tools. [Study](section-1-concepts.md#13-why-use-an-mcp-server)

</details>

## Section 2 · Bob Core Features (23%, 18 questions)

**2-01** · Objective 2.1: Which tool group is the only file-related group available in the read-only Ask mode?

- a) subtask
- b) edit
- c) read
- d) execute

<details><summary>Answer</summary>

**c**. Ask mode uses the read group (read_file, glob, grep, list_files, symbol tools). It cannot edit files or run commands. [Study](section-2-core-features.md#21-use-bobs-file-system-to-read-create-and-modify-project-files)

</details>

**2-02** · Objective 2.2: A team wants a "Security Reviewer" persona that can read everything but can never edit source code or run commands. What should they create?

- a) A SessionStart hook
- b) A skill named security-review
- c) A custom mode with only the read group (and optionally an edit group restricted to report files)
- d) A rule saying "do not edit files"

<details><summary>Answer</summary>

**c**. Custom modes enforce tool access. A rule only asks Bob to behave; a mode without edit and execute groups cannot use them. [Study](section-2-core-features.md#22-add-a-custom-mode)

</details>

**2-03** · Objective 2.2: Where should a team keep a custom mode so every developer who clones the repository gets it?

- a) ~/.bob/settings/custom_modes.yaml
- b) .bob/skills/modes.md
- c) AGENTS.md
- d) .bob/custom_modes.yaml

<details><summary>Answer</summary>

**d**. Project modes in .bob/custom_modes.yaml are version-controlled and shared. The global file is personal. [Study](section-2-core-features.md#22-add-a-custom-mode)

</details>

**2-04** · Objective 2.3: Which statement about IBM Bob premium packages is correct?

- a) They are optional add-ons with specialized capabilities for specific platforms and modernization workflows
- b) They are free for all plans
- c) They replace Bob Shell
- d) They are required for Bob to work

<details><summary>Answer</summary>

**a**. Premium packages (Java Modernization, Z, i) are optional, entitlement-based add-ons. Install from the in-app notification; update via Extensions or Install from VSIX. [Study](section-2-core-features.md#23-purpose-of-ibm-premium-packages)

</details>

**2-05** · Objective 2.4: Which is a documented limitation of .bobignore?

- a) It only works for Python projects
- b) It cannot use wildcards
- c) Protection for execute_command is limited to a predefined list of file-reading commands
- d) It must be placed in ~/.bob/

<details><summary>Answer</summary>

**c**. .bobignore is workspace-only, not a sandbox, and execute_command is only checked for known file-reading commands. It lives in the workspace root and uses .gitignore syntax. [Study](section-2-core-features.md#24-role-of-bobignore)

</details>

**2-06** · Objective 2.5: A developer needs to design the approach for splitting a large RPG program into a service program before any code is written. Which built-in mode fits?

- a) Ask
- b) Orchestrator
- c) Agent
- d) Plan

<details><summary>Answer</summary>

**d**. Plan mode is for architecture, design and implementation planning before coding. [Study](section-2-core-features.md#25-the-three-default-modes)

</details>

**2-07** · Objective 2.5: What is the commonly recommended mode workflow?

- a) Agent only
- b) Ask → Agent → Plan
- c) Agent → Plan → Ask
- d) Plan → Agent → Ask (when needed)

<details><summary>Answer</summary>

**d**. Plan, then implement in Agent, and use Ask when you need information without risking code changes. [Study](section-2-core-features.md#25-the-three-default-modes)

</details>

**2-08** · Objective 2.6: A Bob SaaS user wants to force the most powerful model for a difficult refactor. What happens?

- a) They set it in AGENTS.md
- b) They cannot pick the model; Bob routes tasks automatically by complexity, capability, context size and cost
- c) They must buy an Ultra plan to choose models
- d) They select it from the model dropdown

<details><summary>Answer</summary>

**b**. Bob SaaS users cannot manually pick the LLM; Bob selects the appropriate model per task. [Study](section-2-core-features.md#26-how-bob-selects-llm-models)

</details>

**2-09** · Objective 2.7: Which command starts an interactive Bob Shell session?

- a) bob chat
- b) bob run
- c) bob init
- d) bob --format json

<details><summary>Answer</summary>

**a**. bob chat is interactive; bob run is non-interactive (scripts, CI/CD). [Study](section-2-core-features.md#27-use-bob-shell-from-the-command-line)

</details>

**2-10** · Objective 2.7: While in a Bob Shell session, a developer wants to re-run a failing makei command to see its error without leaving Bob. What should they use?

- a) Shell mode, toggled with ! on an empty input
- b) Plan mode
- c) A PostToolUse hook
- d) /init

<details><summary>Answer</summary>

**a**. The ! prefix toggles shell mode in Bob Shell for running and diagnosing shell commands. [Study](section-2-core-features.md#27-use-bob-shell-from-the-command-line)

</details>

**2-11** · Objective 2.8: In Bob v2's architecture, which component provides reasoning and code generation?

- a) The harness
- b) The MCP server
- c) The client
- d) The agent

<details><summary>Answer</summary>

**d**. Agent = reasoning and code generation; harness = runtime services such as authentication, logging and telemetry; clients = user interfaces (IDE, Shell). [Study](section-2-core-features.md#28-components-of-bobs-architecture)

</details>

**2-12** · Objective 2.9: Which activity best shows Bob supporting multiple parts of the SDLC?

- a) Running the company's payroll system
- b) Planning a feature, implementing it, writing tests, creating the pull request and modernizing old code
- c) Hosting the team's Git repositories
- d) Replacing the IBM i operating system

<details><summary>Answer</summary>

**b**. Bob works across planning, design, coding, testing, deployment, operations and modernization. [Study](section-2-core-features.md#29-bob-as-ai-development-partner-across-the-sdlc)

</details>

**2-13** · Objective 2.10: Where can an individual developer quickly see current Bobcoin usage in the IDE?

- a) By hovering over the gauge in the top-right corner of the Bob panel
- b) Only by asking an administrator
- c) In the Problems panel
- d) In AGENTS.md

<details><summary>Answer</summary>

**a**. Hover the gauge, or open Settings → General; Bobalytics shows patterns over time. [Study](section-2-core-features.md#210-monitor-usage-and-bobcoins-with-bobalytics)

</details>

**2-14** · Objective 2.11: How does Bob primarily reduce token cost?

- a) By compressing source files on disk
- b) By multi-model orchestration that routes each task to a suitable model instead of always the most capable one
- c) By deleting older messages after each reply
- d) By refusing long prompts

<details><summary>Answer</summary>

**b**. Intelligent routing sends simple tasks to faster, cheaper models. [Study](section-2-core-features.md#211-how-bob-optimizes-token-consumption-intelligent-routing)

</details>

**2-15** · Objective 2.12: A developer selects an RPG procedure and wants a quick explanation without opening the chat first. Which is a valid way?

- a) Lightbulb or right-click → Bob → Explain with Bob
- b) Create a new custom mode
- c) Run bob run in a terminal
- d) Add the code to .bobignore

<details><summary>Answer</summary>

**a**. Code actions (lightbulb, context menu, Ctrl/Cmd + .) offer Add to Context, Explain, Improve, Inline Chat and Move to Chat. [Study](section-2-core-features.md#212-different-ways-of-using-code-functions)

</details>

**2-16** · Objective 2.14: Which list correctly names the context window categories?

- a) Read, edit, execute, MCP, skill, todo, subtask, subagent, mode
- b) System prompt, tool definitions, MCP tools, rules, skills, messages
- c) AGENTS.md, prompts, skills, MCP
- d) Agent, Plan, Ask

<details><summary>Answer</summary>

**b**. These six categories appear in the token usage breakdown. [Study](section-2-core-features.md#214-define-and-identify-the-context-window)

</details>

**2-17** · Objective 2.13: Why should a team connect only the MCP servers a task actually needs?

- a) Unused servers make Bob switch to Ask mode
- b) Every connected server's tool definitions occupy the context window and add tokens to every prompt
- c) MCP servers disable rules while connected
- d) Bob can connect to only one MCP server at a time

<details><summary>Answer</summary>

**b**. MCP uses a client-server architecture over JSON-RPC 2.0, and connected tools' definitions count in the context window (the MCP tools category). MCP can use many tokens, so the use case matters. [Study](section-2-core-features.md#213-integrate-bob-with-external-tools-through-mcp)

</details>

**2-18** · Objective 2.15: A company wants one documentation standard applied in every project its developers open, while each repository adds its own conventions. What fits best?

- a) A skill that each developer must remember to activate
- b) Pasting the standard into every prompt
- c) Global rules for the company standard plus project rules in each repository
- d) A custom mode per project

<details><summary>Answer</summary>

**c**. Custom rules can be global (all projects) or project-level, for all modes or mode-specific. Combining both is the hybrid approach for organization-wide plus repo-specific standards. [Study](section-2-core-features.md#215-standardize-bob-behaviour-with-rules)

</details>

## Section 3 · Bob Use Cases (19%, 15 questions)

**3-01** · Objective 3.1: Bob produced a plan in Plan mode. Which is NOT one of the things to inspect before implementing?

- a) The number of Bobcoins the plan text used
- b) Scope match
- c) Unwanted assumptions
- d) Acceptance criteria

<details><summary>Answer</summary>

**a**. Inspect scope match, decisions, implementation sequence, acceptance criteria and unwanted assumptions, then refine and apply the approved plan in Agent mode. [Study](section-3-use-cases.md#31-create-inspect-and-refine-a-plan-before-coding)

</details>

**3-02** · Objective 3.1: What should a good planning prompt include?

- a) Scope, affected layers, constraints and acceptance criteria
- b) Only the ticket number
- c) The full source of every program
- d) The developer's job title

<details><summary>Answer</summary>

**a**. Planning prompts should state scope, affected layers, constraints and acceptance criteria. [Study](section-3-use-cases.md#31-create-inspect-and-refine-a-plan-before-coding)

</details>

**3-03** · Objective 3.2: When is literate coding the best choice over chat-based Agent mode?

- a) When the change is local to a specific file or code block and you want an inline diff
- b) When the change spans many files and needs commands run
- c) When you need a project-wide refactor
- d) When you want Bob to create a pull request

<details><summary>Answer</summary>

**a**. Literate coding is in-editor, at a precise location, single-file, with inline diff review. [Study](section-3-use-cases.md#32-literate-coding-create-code-from-comments)

</details>

**3-04** · Objective 3.2: After literate coding generates code, the inline diff does not match the intended behaviour. What should the developer do?

- a) Commit it so rollback can restore it
- b) Accept it and fix it later
- c) Reject the generated change and refine the instructions
- d) Switch to Ask mode to accept it

<details><summary>Answer</summary>

**c**. Inspect the inline diff; accept only when it matches, otherwise reject. [Study](section-3-use-cases.md#32-literate-coding-create-code-from-comments)

</details>

**3-05** · Objective 3.3: Which TWO are part of inspecting Bob-generated output before accepting it? (Select two)

- a) Reviewing the code diff
- b) Changing the color theme
- c) Checking test and build results
- d) Restarting the IDE
- e) Counting the words in Bob's reply

<details><summary>Answer</summary>

**a, c**. Inspect code diffs, test results, build output, command output and do a manual review. [Study](section-3-use-cases.md#33-core-sdlc-capabilities-understand-generate-modify-document-automate)

</details>

**3-06** · Objective 3.4: The team wants every RPG change to check SQLSTATE after embedded SQL, in every conversation. Which mechanism fits best?

- a) A subtask
- b) A hook
- c) A skill
- d) A rule

<details><summary>Answer</summary>

**d**. Rules give persistent, always-active guidance for coding style and conventions. [Study](section-3-use-cases.md#34-when-to-use-modes-skills-rules-hooks-and-agentsmd)

</details>

**3-07** · Objective 3.4: Which mechanism is activated by Bob itself, based on the request?

- a) Custom modes
- b) AGENTS.md
- c) Skills
- d) Rules

<details><summary>Answer</summary>

**c**. Rules are always active, modes are activated by the user, and skills are activated by Bob. [Study](section-3-use-cases.md#34-when-to-use-modes-skills-rules-hooks-and-agentsmd)

</details>

**3-08** · Objective 3.4: A team wants to automatically log every tool Bob runs to an audit file. Which mechanism?

- a) AGENTS.md
- b) Plan mode
- c) A rule
- d) A PostToolUse hook

<details><summary>Answer</summary>

**d**. Hooks automate lifecycle actions before, during or after Bob activity. [Study](section-3-use-cases.md#34-when-to-use-modes-skills-rules-hooks-and-agentsmd)

</details>

**3-09** · Objective 3.5: A nightly CI job should review changed RPG files and emit JSON for the pipeline. Which is the right fit?

- a) Bob Shell interactive (bob chat)
- b) Bob IDE with literate coding
- c) Bob Shell non-interactive (bob run --format json)
- d) Code actions

<details><summary>Answer</summary>

**c**. Non-interactive Bob Shell suits CI/CD, batch processing and structured output. [Study](section-3-use-cases.md#35-bob-shell-vs-bob-ide)

</details>

**3-10** · Objective 3.6: Bob generates Terraform for a new environment. What is Terraform's role?

- a) It provisions the infrastructure; Bob is the development partner
- b) It hosts the MCP server
- c) It replaces Bob's agent
- d) It reviews Bob's code

<details><summary>Answer</summary>

**a**. Bob generates and validates; the external tool (Terraform) is the execution system. [Study](section-3-use-cases.md#36-bob-alone-vs-with-specialized-tools-or-external-applications)

</details>

**3-11** · Objective 3.7: Which statement correctly distinguishes subagents from subtasks?

- a) They are the same feature with different names
- b) Subagents appear as visible interactive threads; subtasks run silently
- c) Subagents run silently in the background and return a summary; subtasks are visible, interactive threads with their own tracking
- d) Subtasks can only read files

<details><summary>Answer</summary>

**c**. Use subagents for self-contained background work; subtasks for visible, tracked threads. [Study](section-3-use-cases.md#37-subagents-and-subtasks)

</details>

**3-12** · Objective 3.8: Which approach does Bob support for modernizing a large legacy application?

- a) Skipping builds and tests to save Bobcoins
- b) Incremental modernization: discovery, specs and plans first, then validated changes step by step
- c) Code changes first, then documentation of what was changed
- d) A big-bang rewrite generated in one prompt

<details><summary>Answer</summary>

**b**. Analyze, inspect, plan and specify before code, validate with builds and tests, and modernize incrementally. [Study](section-3-use-cases.md#38-modernize-applications-using-bob)

</details>

**3-13** · Objective 3.11: A developer wants Bob's code review to include local edits that are not yet committed. What should they do?

- a) Use literate coding
- b) Commit first; reviews never include uncommitted changes
- c) Toggle "Include Uncommitted Changes" in the Review panel
- d) Add the files to .bobignore

<details><summary>Answer</summary>

**c**. The Review workflow can include uncommitted changes (on by default when reviewing the current branch). Findings appear in Bob Findings with Fix with Bob and Dismiss. [Study](section-3-use-cases.md#311-code-review-and-bob-findings)

</details>

**3-14** · Objective 3.9: A developer used Bob to generate an MCP server with three tools for an internal API. What best demonstrates end-to-end verification?

- a) Counting the number of generated files
- b) Asking Bob in Ask mode whether the code looks correct
- c) Reading the generated code once
- d) Building an MCP client (or connecting the server to Bob) and calling each tool against the real API, then fixing errors found

<details><summary>Answer</summary>

**d**. When building agents and MCP tools with Bob, construct an MCP client to test tools end to end, modify code/config/agent YAML when validation fails, and demonstrate the working result. [Study](section-3-use-cases.md#39-build-ai-agents-using-bob)

</details>

**3-15** · Objective 3.10: A batch program fails with RNX0907 (decimal data error). The developer first wants to understand the likely cause without any file changes. Which mode?

- a) Ask mode
- b) Agent mode
- c) Plan mode with auto-approve on
- d) A custom mode with execute only

<details><summary>Answer</summary>

**a**. Use Ask mode for explanation and analysis without file changes. Switch to Agent mode when code fixes, edits or command execution are needed, then re-run tests and builds to confirm. [Study](section-3-use-cases.md#310-debug-application-problems-with-bob)

</details>

## Section 4 · Bob Configuration (17%, 13 questions)

**4-01** · Objective 4.1: Which subagent type is read-only and runs on a lighter model?

- a) orchestrator
- b) reviewer
- c) explore
- d) general

<details><summary>Answer</summary>

**c**. explore is read-only on a lighter model; general has full tool access on the default model. [Study](section-4-configuration.md#41-tools-read-command-subtask-mcp)

</details>

**4-02** · Objective 4.1: Which tool runs CLI commands such as builds and tests in the workspace?

- a) apply_diff
- b) use_skill
- c) update_todo_list
- d) execute_command

<details><summary>Answer</summary>

**d**. execute_command belongs to the execute (command) group. [Study](section-4-configuration.md#41-tools-read-command-subtask-mcp)

</details>

**4-03** · Objective 4.2: What is the per-task context window cap, and around when does automatic condensation begin?

- a) 128,000 cap; condensation at 100,000
- b) 270,000 cap; condensation around 190,000
- c) 1,000,000 cap; no condensation
- d) 270,000 cap; condensation at 260,000

<details><summary>Answer</summary>

**b**. Each task has a 270,000-token cap; condensation typically starts around 190,000. [Study](section-4-configuration.md#42-utilize-context-window-management)

</details>

**4-04** · Objective 4.2: Which context category usually becomes the largest once Bob starts reading files and running tools?

- a) Tool definitions
- b) Skills
- c) Messages
- d) System prompt

<details><summary>Answer</summary>

**c**. Messages grow every turn and with repo exploration. System prompt and tool definitions stay flat. [Study](section-4-configuration.md#42-utilize-context-window-management)

</details>

**4-05** · Objective 4.3: A developer mentions @qrpglesrc/ in a prompt. What does Bob include?

- a) All files in qrpglesrc/ and every subfolder
- b) Only files directly in qrpglesrc/ (non-recursive)
- c) Nothing; folders cannot be mentioned
- d) Only the folder name

<details><summary>Answer</summary>

**b**. Folder mentions are non-recursive. [Study](section-4-configuration.md#43-context-mentions-)

</details>

**4-06** · Objective 4.3: Which context mentions still respect .gitignore?

- a) File mentions
- b) Git mentions such as @git-changes and @<commit-hash>
- c) Folder mentions
- d) URL mentions

<details><summary>Answer</summary>

**b**. File and folder mentions bypass .bobignore and .gitignore; Git mentions use Git, so they respect .gitignore. [Study](section-4-configuration.md#43-context-mentions-)

</details>

**4-07** · Objective 4.4: How do you install the Bob Shell companion extension manually when Bob Shell runs in Bob IDE's terminal?

- a) /init
- b) bob run --install
- c) /ide install
- d) Add it to mcp.json

<details><summary>Answer</summary>

**c**. Use /ide install; /ide enable, /ide disable and /ide status manage the connection. [Study](section-4-configuration.md#44-download-extensions)

</details>

**4-08** · Objective 4.5: Which parameter is required for a STDIO MCP server, and which for a Streamable HTTP server?

- a) env for both
- b) url for STDIO; command for HTTP
- c) alwaysAllow for both
- d) command for STDIO; url for HTTP

<details><summary>Answer</summary>

**d**. STDIO needs command (plus optional args, cwd, env, alwaysAllow, disabled); remote needs url (plus headers...). [Study](section-4-configuration.md#45-develop-and-add-mcp-tools)

</details>

**4-09** · Objective 4.5: A project handles confidential customer data. Which MCP transport keeps traffic off the network?

- a) Streamable HTTP
- b) STDIO (Bob spawns the server as a local child process)
- c) Any transport, as long as alwaysAllow is empty
- d) SSE

<details><summary>Answer</summary>

**b**. STDIO is local, low latency and has no network exposure. Prefer local servers for confidential projects. [Study](section-4-configuration.md#45-develop-and-add-mcp-tools)

</details>

**4-10** · Objective 4.6: A custom mode defined in YAML has no groups key. What tool access does it get?

- a) All tools
- b) No grouped tools
- c) The same as Agent mode
- d) Read only

<details><summary>Answer</summary>

**b**. Omitting groups grants no grouped tools. Unknown group names also grant nothing. [Study](section-4-configuration.md#46-create-custom-modes)

</details>

**4-11** · Objective 4.8: In what order are rules loaded within one level (global or workspace)?

- a) General rules → AGENTS.md → mode-specific rules
- b) AGENTS.md → general → mode-specific
- c) Random order
- d) Mode-specific rules → AGENTS.md → general rules

<details><summary>Answer</summary>

**d**. Global loads before workspace; within each level, mode-specific → AGENTS.md → general, alphabetically. [Study](section-4-configuration.md#48-custom-rules-global-vs-project)

</details>

**4-12** · Objective 4.9: What is required before Bob can generate and create a pull request from the IDE?

- a) A PR template in .github/
- b) An MCP server for GitHub
- c) An Enterprise plan
- d) Changes committed to a branch and push access to the remote repository

<details><summary>Answer</summary>

**d**. Commit to a branch and have push access. Templates are optional; without one Bob uses a default template (title, summary, implementation details, testing, links). [Study](section-4-configuration.md#49-generate-pull-requests-from-the-ide)

</details>

**4-13** · Objective 4.7: A developer has a global skill named code-review and the project also contains .bob/skills/code-review/. Which one does Bob use in that project, and how can they confirm it?

- a) The global skill; check AGENTS.md
- b) Both are merged; check the Problems panel
- c) Neither; duplicate names disable both
- d) The project skill; check the Skills settings tab, which shows loaded skills and their location

<details><summary>Answer</summary>

**d**. Project skills take precedence over global skills with the same name. The Skills settings tab shows which skills are loaded and from where. Settings → Auto-Approve → Skills removes the activation prompt. [Study](section-4-configuration.md#47-develop-bob-skills)

</details>

## Section 5 · Bob Accounts (8%, 6 questions)

**5-01** · Objective 5.1: What does the Bob factor metric in Bobalytics represent?

- a) The percentage of committed code created by Bob
- b) The number of MCP servers
- c) The number of prompts per user
- d) The Bobcoin price

<details><summary>Answer</summary>

**a**. Bob factor = Bob's contribution to the codebase (share of committed lines Bob created). [Study](section-5-accounts.md#51-administer-bobalytics)

</details>

**5-02** · Objective 5.1: What can an administrator see about an individual developer from a team-level Bobalytics chart?

- a) Their source code
- b) Their full prompt history
- c) Nothing individually identifiable; team charts are anonymized
- d) Their Bobcoin spend by name

<details><summary>Answer</summary>

**c**. Bobalytics gives team-level insights without exposing individual user data to admins. [Study](section-5-accounts.md#51-administer-bobalytics)

</details>

**5-03** · Objective 5.2: A CI pipeline runs Bob Shell with a General API key and fails authentication for inference. What is missing?

- a) An MCP server
- b) A team ID (--team-id)
- c) Plan mode
- d) A PR template

<details><summary>Answer</summary>

**b**. General keys are instance-wide and need a team ID for inference. Inference keys are already team-scoped. [Study](section-5-accounts.md#52-authenticate-with-api-keys)

</details>

**5-04** · Objective 5.3: Which capability is specific to the Enterprise plan?

- a) Running /init
- b) SSO with SAML or OIDC identity providers and shared Bobcoin pools with spending limits
- c) Using Ask mode
- d) Writing custom rules

<details><summary>Answer</summary>

**b**. Enterprise adds team management, shared Bobcoin allocation, spending limits, Bobalytics and SSO (SAML/OIDC). [Study](section-5-accounts.md#53-enterprise-plan-features)

</details>

**5-05** · Objective 5.4: What is the relationship between tokens and Bobcoins?

- a) Tokens are raw model usage units; Bobcoins abstract token usage into a predictable billing metric
- b) They are identical units
- c) Tokens are billed in USD, Bobcoins are free
- d) Bobcoins count only output tokens

<details><summary>Answer</summary>

**a**. Bobcoins combine token usage across models and operations into one consumption metric. [Study](section-5-accounts.md#54-bobcoins)

</details>

**5-06** · Objective 5.5: Late in a long task, a developer's one-line question uses far more tokens than the same question did at the start. Why?

- a) Short prompts are billed at a minimum size
- b) The system prompt grows after each response
- c) Bob switches to a more expensive model after 10 messages
- d) The full active context, including all accumulated messages, is processed again with each prompt

<details><summary>Answer</summary>

**d**. Every prompt re-sends the whole active context, so a growing Messages category raises the cost of later prompts. [Study](section-5-accounts.md#55-token-usage-for-prompting)

</details>

## Section 6 · Bob Security (16%, 12 questions)

**6-01** · Objective 6.1: A developer enables auto-approval for Edit using the Permissions control beside the mode selector for the current task. What is the scope?

- a) Until the IDE restarts
- b) All users in the organization
- c) All future tasks for that user
- d) The current task only; it does not become a global permission

<details><summary>Answer</summary>

**d**. Task-level approvals override the normal approval experience for that task only. [Study](section-6-security.md#61-modify-mode-permissions-in-a-contexttask)

</details>

**6-02** · Objective 6.2: Bob keeps building on an earlier wrong assumption even after several corrective prompts. What is the most reliable fix?

- a) Enable auto-approve so Bob works faster
- b) Add the correction to every prompt
- c) Add more MCP servers
- d) Start a fresh task with a narrow scope and only targeted evidence

<details><summary>Answer</summary>

**d**. That's context poisoning. Bad content persists in Messages; a new task with lean, targeted context is the reliable recovery. [Study](section-6-security.md#62-reduce-context-poisoning)

</details>

**6-03** · Objective 6.2: Which practice helps PREVENT context poisoning during a broad codebase investigation?

- a) Use subagents so the main task receives only condensed findings
- b) Keep one task open for all work this week
- c) Load every available skill at the start
- d) Paste the entire repository into the chat

<details><summary>Answer</summary>

**a**. Subagents keep intermediate reads out of the main context; keep standing context lean and evidence targeted. [Study](section-6-security.md#62-reduce-context-poisoning)

</details>

**6-04** · Objective 6.3: A documentation mode must only be able to edit Markdown files. How is this enforced?

- a) Adding source files to .gitignore
- b) A SessionStart hook
- c) An edit group with a fileRegex such as .*\.md$ in the mode definition
- d) A rule that says "only edit .md files"

<details><summary>Answer</summary>

**c**. fileRegex on the edit group restricts which files a mode can change. [Study](section-6-security.md#63-identify-and-enable-correct-permission-restrictions-for-projects)

</details>

**6-05** · Objective 6.4: Which TWO statements about .bobignore are true? (Select two)

- a) Bob monitors it and reloads changes automatically
- b) It blocks mode switching
- c) It is a full system-level sandbox
- d) The .bobignore file itself is implicitly ignored, so Bob cannot change its own access rules
- e) It must be named .bob/ignore.json

<details><summary>Answer</summary>

**a, d**. It auto-reloads and is implicitly ignored itself. It is not a sandbox, lives in the workspace root as .bobignore, and doesn't affect mode switching. [Study](section-6-security.md#64-produce-a-bobignore-file)

</details>

**6-06** · Objective 6.4: Which pattern in .bobignore re-allows a file excluded by a broader rule?

- a) #important.log
- b) !important.log
- c) +important.log
- d) allow: important.log

<details><summary>Answer</summary>

**b**. .gitignore syntax uses ! for exceptions (e.g. !.env.example). [Study](section-6-security.md#64-produce-a-bobignore-file)

</details>

**6-07** · Objective 6.5: Which permissions does IBM classify as high risk?

- a) Edit and Execute
- b) Read and Skill
- c) Subtask and Subagent
- d) Todo and Mode

<details><summary>Answer</summary>

**a**. Edit and Execute are high; MCP is medium-high; Read and Skill medium; Todo, Subtask, Subagent, Mode low. [Study](section-6-security.md#65-correct-permissions-and-approval-workflows)

</details>

**6-08** · Objective 6.5: Bob proposes a terminal command that is almost right but targets the wrong library. What can the developer do?

- a) Only approve or reject; commands cannot be changed
- b) Disable the execute group globally
- c) Restart the task
- d) Edit the command directly in the approval prompt before running it

<details><summary>Answer</summary>

**d**. Terminal commands proposed by Bob can be edited in the approval prompt before execution. [Study](section-6-security.md#65-correct-permissions-and-approval-workflows)

</details>

**6-09** · Objective 6.6: Bob needs a token to call an internal test-results service. What is the recommended approach?

- a) Hard-code it in mcp.json and commit it
- b) Put it in AGENTS.md so Bob always has it
- c) Paste it in the chat and delete the message afterwards
- d) Store it in an approved secrets solution and provide it at runtime

<details><summary>Answer</summary>

**d**. Never place secrets in prompts or Bob-readable files. Use secrets management and runtime injection. [Study](section-6-security.md#66-best-security-practices)

</details>

**6-10** · Objective 6.7: When does Bob create rollback snapshots?

- a) Only when the developer commits
- b) Before every terminal command
- c) When a task begins and before file modifications, but not automatically before terminal commands
- d) Only when requested manually

<details><summary>Answer</summary>

**c**. Snapshots are stored in a shadow Git repo at task start and before file edits; terminal commands don't trigger them. [Study](section-6-security.md#67-rollback-changes)

</details>

**6-11** · Objective 6.7: A developer wants to undo Bob's file changes but keep the conversation to try another approach. Which option?

- a) Restore files
- b) git reset --hard
- c) Restore files and task
- d) Delete the task

<details><summary>Answer</summary>

**a**. Restore files keeps conversation history. Restore files and task also removes later messages, needs confirmation, and cannot be undone. [Study](section-6-security.md#67-rollback-changes)

</details>

**6-12** · Objective 6.3: A project contains scripts that deploy to production libraries. What is the appropriate permission posture?

- a) Restricted project modes plus conservative auto-approve, keeping more manual approvals and narrower permissions than routine local work
- b) Remove the project from version control
- c) Rely on .bobignore alone, since it sandboxes commands
- d) Enable auto-approve for Edit and Execute to avoid slowing developers down

<details><summary>Answer</summary>

**a**. Combine custom-mode restrictions (tool groups, fileRegex) with conservative auto-approve. Sensitive or production-related work keeps more manual approvals. .bobignore is not a sandbox. [Study](section-6-security.md#63-identify-and-enable-correct-permission-restrictions-for-projects)

</details>
