# Bob Architecture — How Everything Connects

> Shows how Custom Modes, Rules, Skills, Commands, Hooks, MCP, and Bob Shell
> all relate to each other in this IBM i project.

---

## Map 1 — Interactive Session (IDE)

```mermaid
flowchart TD
    USER(["👤 Developer"])

    subgraph ENTRY["Entry Points"]
        CMD["⚡ Slash Command\n/convert-to-free\n/review-ibmi\n/where-used\n/build\n/new-rpg-program\netc."]
        MODE["🎭 Custom Mode\nrpg-dev · cl-dev\nmodernizer · ibmi-reviewer\nibmi-ops · python-tools"]
    end

    subgraph HOOKS["🪝 Hooks  (settings.json)"]
        H1["SessionStart\nsession-context.sh\n→ injects env info"]
        H2["UserPromptSubmit\nblock-secrets.py\n→ blocks credentials in prompt"]
        H3["PreToolUse · execute_command\nguard-dangerous-commands.py\n→ blocks DLTLIB, DROP, rm -rf …"]
        H4["PreToolUse · write_*\nprotect-paths.py\n→ blocks legacy/, .env, hooks/"]
        H5["PostToolUse\nlog-activity.sh\n→ appends to .bob/logs/"]
        H6["Stop\nsession-summary.sh\n→ git status snapshot"]
    end

    subgraph CONTEXT["Context Bob receives"]
        RULES_S["rules/\nShared rules\n(safety · standards · platform)"]
        RULES_M["rules-{slug}/\nMode-specific rules"]
        SKILL["🧠 Skill\nSKILL.md + templates/\nreference/ · examples/ · scripts/"]
    end

    subgraph MCP["🔌 MCP  (mcp.json + ibmi-dev-tools.yaml)"]
        TOOLS["list_objects · program_references\nwhere_used · table_columns\nrecent_job_messages · active_jobs_in_subsystem"]
        DB2["Db2 for i  QSYS2 services"]
    end

    USER -->|"types /command or switches mode"| ENTRY
    CMD -->|"carries prompt + switches mode"| MODE
    MODE --> RULES_S
    MODE -->|"rules-{slug}/"| RULES_M
    MODE -->|"customInstructions"| SKILL
    CMD -->|"references skill steps"| SKILL

    USER -->|"every prompt"| H2
    ENTRY -->|"before any tool runs"| H3
    ENTRY -->|"before any write runs"| H4
    ENTRY -->|"session opens"| H1
    ENTRY -->|"after every tool"| H5
    ENTRY -->|"session ends"| H6

    MODE -->|"groups: mcp"| MCP
    SKILL -->|"workflow step calls tool"| MCP
    TOOLS --> DB2
```

---

## Map 2 — Bob Shell (CI / Automation)

```mermaid
flowchart LR
    subgraph CI["CI Pipeline / Shell Script"]
        SCRIPT["scripts/\nbatch-convert.sh\nci-review.sh"]
        PROMPT["examples/prompts/\nconvert.txt\n(prompt template)"]
    end

    subgraph BOBRUN["bob run (non-interactive)"]
        FLAGS["--mode modernizer\n--max-cost N\n--max-turns N\n--format json\n--disable-tool-groups edit"]
        RESULT["result.json\nstatus · last_message\ntokens · tool_calls"]
    end

    subgraph BOBDOT["Same .bob/ folder"]
        RULES_S["rules/  (shared)"]
        RULES_M["rules-{slug}/"]
        SKILL2["Skills"]
        HOOKS2["🪝 Hooks\nguard-dangerous-commands.py\nprotect-paths.py\n(still active — most critical in automation)"]
        MCP2["MCP tools"]
    end

    subgraph VERIFY["Deterministic checks"]
        VFY["verify_conversion.py\n(exit 1 on errors)"]
        SUM["summarize_results.py\n→ Markdown / CSV"]
    end

    SCRIPT -->|"cat prompt.txt | bob run"| BOBRUN
    PROMPT --> SCRIPT
    FLAGS --> BOBRUN

    BOBRUN -->|"reads"| BOBDOT
    RULES_S --> BOBRUN
    RULES_M --> BOBRUN
    SKILL2 --> BOBRUN
    HOOKS2 -->|"PreToolUse still fires"| BOBRUN
    MCP2 --> BOBRUN

    BOBRUN --> RESULT
    RESULT -->|"check status == success"| VFY
    RESULT --> SUM
    SUM -->|"exit non-zero on CRITICAL"| CI
```

---

## Map 3 — The Full Picture

```mermaid
flowchart TD
    subgraph A["⚡ Slash Commands\n.bob/commands/*.md"]
        direction LR
        A1["prompt template + argument-hint"]
    end

    subgraph B["🎭 Custom Mode\n.bob/custom_modes.yaml"]
        direction LR
        B1["roleDefinition\ngroups (edit · execute · mcp · skill)\nfileRegex  →  edit scope guard"]
    end

    subgraph C["📋 Rules\n.bob/rules*/"]
        C1["rules/  shared\n(always active)"]
        C2["rules-{slug}/\n(mode-specific)"]
    end

    subgraph D["🧠 Skills\n.bob/skills/*/"]
        D1["SKILL.md\n(activation + workflow)"]
        D2["templates · reference\nexamples · scripts"]
    end

    subgraph E["🪝 Hooks\n.bob/settings.json"]
        E1["SessionStart\nUserPromptSubmit\nPreToolUse\nPostToolUse · Stop"]
    end

    subgraph F["🔌 MCP\n.bob/mcp.json + mcp-tools/"]
        F1["ibmi-mcp server"]
        F2["ibmi-dev-tools.yaml\nread-only SQL tools"]
        F3["Db2 for i  QSYS2"]
    end

    subgraph G["🖥️ Bob Shell\nbob run"]
        G1["--mode · --max-cost\n--format json · --disable-tool-groups"]
    end

    A -->|"switches to / invokes"| B
    A -->|"references skill steps"| D
    B -->|"slug → rules-{slug}/"| C2
    B -->|"inherits"| C1
    B -->|"customInstructions"| D
    B -->|"groups: mcp"| F
    D1 -->|"references"| D2
    D1 -->|"workflow step"| F
    E -->|"fires on every tool & prompt\ncan BLOCK (exit 2)"| B

    G -->|"reads entire .bob/ folder\nsame rules · modes · skills · hooks · MCP"| B
    G -->|"hooks still enforce guardrails"| E
```

---

## Key Insights

| # | Insight |
|---|---|
| **1** | **Commands are thin wrappers** — they carry a user argument into a mode + skill combination. The actual logic lives in the skill, not the command file. |
| **2** | **Hooks are the safety net that cannot be bypassed** — they fire in Bob Shell automation too, which is exactly when Bob has pre-approved tool calls and the risk is highest. |
| **3** | **Bob Shell shares the entire `.bob/` folder** — rules, modes, skills, and MCP are not IDE-only features; every `bob run` in CI gets the same guardrails a developer gets interactively. |

---

## File Reference

| Layer | Location |
|---|---|
| Custom Modes | [`.bob/custom_modes.yaml`](../.bob/custom_modes.yaml) |
| Shared rules | [`.bob/rules/`](../.bob/rules/) |
| Mode-specific rules | [`.bob/rules-{slug}/`](../.bob/) |
| Skills | [`.bob/skills/`](../.bob/skills/) |
| Slash commands | [`.bob/commands/`](../.bob/commands/) |
| Hooks config | [`.bob/settings.json`](../.bob/settings.json) |
| Hook scripts | [`.bob/hooks/`](../.bob/hooks/) |
| MCP config | [`.bob/mcp.json`](../.bob/mcp.json) |
| MCP tool definitions | [`.bob/mcp-tools/ibmi-dev-tools.yaml`](../.bob/mcp-tools/ibmi-dev-tools.yaml) |
| Bob Shell scripts | [`.bob/skills/bob-shell-automation/scripts/`](../.bob/skills/bob-shell-automation/scripts/) |
