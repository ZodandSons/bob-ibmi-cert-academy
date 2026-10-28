# 13 · Reference links

[Docs home](../README.md) · [← 12 Glossary](12-glossary.md)

---

The bob.ibm.com pages and GitHub repositories below were checked on 2026-10-22. The
project documentation sites (`*.github.io`) are the ones each repository's README links to.
Bob changes quickly, so if a page has moved, search from [bob.ibm.com/docs](https://bob.ibm.com/docs).

## IBM Bob documentation (bob.ibm.com)

### Start here
| Page | Use it for |
|---|---|
| [Bob IDE docs home](https://bob.ibm.com/docs/ide) | Overview of the IDE |
| [Installing the IDE](https://bob.ibm.com/docs/ide/getting-started/install) | Setup |
| [Quickstart](https://bob.ibm.com/docs/ide/getting-started/quickstart) | 20-minute hands-on intro (Ask → Plan → Agent, `/init`) |
| [Best practices (IDE)](https://bob.ibm.com/docs/ide/getting-started/best-practices) | Getting good results |
| [Download](https://bob.ibm.com/download) | IDE and Shell installers |

### `.bob` components
| Component | Docs page | Guide here |
|---|---|---|
| Rules and AGENTS.md | [Custom rules](https://bob.ibm.com/docs/ide/configuration/rules) | [03](03-rules.md), [02](02-agents-md-and-bobignore.md) |
| `.bobignore` | [Ignoring files](https://bob.ibm.com/docs/ide/configuration/bobignore) | [02](02-agents-md-and-bobignore.md) |
| Custom modes | [Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) · [Modes](https://bob.ibm.com/docs/ide/features/modes) | [04](04-custom-modes.md) |
| Skills | [Skills (IDE)](https://bob.ibm.com/docs/ide/features/skills) · [Skills (Shell)](https://bob.ibm.com/docs/shell/features/skills) | [05](05-skills.md) |
| Slash commands | [Slash commands](https://bob.ibm.com/docs/shell/features/slash-commands) | [06](06-slash-commands.md) |
| MCP | [MCP in Bob](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-in-bob) · [Understanding MCP](https://bob.ibm.com/docs/ide/configuration/mcp/understanding-mcp) · [Transports](https://bob.ibm.com/docs/ide/configuration/mcp/server-transports) · [OAuth](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-oauth) · [MCP in Bob Shell](https://bob.ibm.com/docs/shell/configuration/mcp/mcp-bobshell) | [07](07-mcp-servers.md) |
| Hooks | [Lifecycle hooks](https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks) · [Group policies](https://bob.ibm.com/docs/ide/security/group-policies) | [08](08-hooks.md) |
| Tools and tool groups | [Tools](https://bob.ibm.com/docs/shell/core-concepts/tools) | [04](04-custom-modes.md), [08](08-hooks.md) |

### Exam-relevant features
[Code reviews and Bob Findings](https://bob.ibm.com/docs/ide/features/code-reviews) ·
[Pull requests](https://bob.ibm.com/docs/ide/features/pull-requests) ·
[Rollback](https://bob.ibm.com/docs/ide/features/rollback) ·
[Literate coding](https://bob.ibm.com/docs/ide/features/literate-coding) ·
[Code actions](https://bob.ibm.com/docs/ide/features/code-actions) ·
[Bobalytics](https://bob.ibm.com/docs/ide/features/bobalytics) ·
[Bobcoins](https://bob.ibm.com/docs/ide/account/bobcoins) ·
[API keys](https://bob.ibm.com/docs/ide/account/api-keys) ·
[Premium packages](https://bob.ibm.com/docs/ide/premium-packages/pkg-index) ·
[Updating premium packages](https://bob.ibm.com/docs/ide/premium-packages/updating-premium-packages) ·
[Context poisoning](https://bob.ibm.com/docs/shell/core-concepts/context-poisoning) ·
[Shell keyboard shortcuts](https://bob.ibm.com/docs/shell/configuration/keyboard-shortcuts) ·
[Start a project with /init (tutorial)](https://bob.ibm.com/docs/ide/getting-started/tutorials/start-a-project) ·
[Pricing](https://bob.ibm.com/pricing)

Certification resources are collected in the [certification track](exam/README.md#official-ibm-resources-from-the-study-guide).

### Features worth knowing
[Subagents](https://bob.ibm.com/docs/ide/features/subagents) ·
[Context mentions (`@file`)](https://bob.ibm.com/docs/ide/features/context-mentions) ·
[Auto-approve](https://bob.ibm.com/docs/ide/features/auto-approving-actions) ·
[Keyboard shortcuts](https://bob.ibm.com/docs/ide/configuration/keyboard-shortcuts) ·
[FAQ (IDE)](https://bob.ibm.com/docs/ide/faq) ·
[Changelog (IDE)](https://bob.ibm.com/docs/ide/changelog)

### Tutorials
| Tutorial | Teaches |
|---|---|
| [Standardize Bob's behavior](https://bob.ibm.com/docs/ide/tutorials/standardize-bobs-behavior) | Creating a rules folder and rule files |
| [Add Bob capabilities (custom mode)](https://bob.ibm.com/docs/ide/tutorials/add-bob-capabilities) | Building a custom mode step by step |
| [Build MCP servers with IBM Bob](https://bob.ibm.com/docs/ide/tutorials/mcp-server-integration) | Writing and registering an MCP server in `.bob/mcp.json` |
| [MCP integration with IBM Bob](https://www.ibm.com/think/tutorials/mcp-integration-ibm-bob) | IBM Think tutorial on connecting MCP servers |

### Bob Shell
[Shell docs home](https://bob.ibm.com/docs/shell) ·
[Install and setup](https://bob.ibm.com/docs/shell/getting-started/install-and-setup) ·
[Interactive sessions](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-interactive) ·
[Non-interactive (`bob run`)](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive) ·
[Usage examples](https://bob.ibm.com/docs/shell/getting-started/bobshell-examples) ·
[Best practices](https://bob.ibm.com/docs/shell/getting-started/best-practices) ·
[API keys](https://bob.ibm.com/docs/shell/account/api-keys) ·
[Modes](https://bob.ibm.com/docs/shell/features/modes) ·
[Subagents](https://bob.ibm.com/docs/shell/features/subagents) ·
[Context window management](https://bob.ibm.com/docs/shell/core-concepts/context-window-management) ·
[FAQ](https://bob.ibm.com/docs/shell/faq) ·
[Changelog](https://bob.ibm.com/docs/shell/changelog)

## IBM GitHub repositories

| Repository | What it is | Used in this example |
|---|---|---|
| [IBM/ibmi-mcp-server](https://github.com/IBM/ibmi-mcp-server) · [docs](https://ibm-d95bab6e.mintlify.app/) | IBM i MCP server (npm `@ibm/ibmi-mcp-server`). Tool YAML schema in `tools/README.md` | `mcp.json`, `mcp-tools/` |
| [IBM/ibmi-mcp-server/.bob](https://github.com/IBM/ibmi-mcp-server/tree/main/.bob) | **IBM's own `.bob` folder**: a custom mode, mode rules, MCP config example | Compare with ours |
| [IBM/ibmi-mcp-server/tools](https://github.com/IBM/ibmi-mcp-server/tree/main/tools) | Ready-made SQL tool sets (developer, performance, security, sys-admin) | Ideas for more MCP tools |
| [IBM/ibmi-tobi](https://github.com/IBM/ibmi-tobi) · [docs](https://ibm.github.io/ibmi-tobi/) | **TOBi**, The Object Builder for i (`makei`). Formerly Better Object Builder / `ibmi-bob` | `skills/ibmi-build` |
| [IBM/ibmi-company_system](https://github.com/IBM/ibmi-company_system) | Sample IBM i application laid out for git + Better Object Builder | A realistic repo to try this `.bob` folder on |
| [IBM/ibmi-oss-examples](https://github.com/IBM/ibmi-oss-examples) | Open-source examples for IBM i (Python, Node, …) | `skills/ibmi-python` patterns |
| [IBM/python-itoolkit](https://github.com/IBM/python-itoolkit) | Python toolkit to call IBM i programs and commands (XMLSERVICE) | Alternative in `skills/ibmi-python` |
| [IBM/ibmi-oss-docs](https://github.com/IBM/ibmi-oss-docs) | Docs for open source on IBM i (yum, PASE, Python, Node) | Setting up PASE tooling |
| [IBM/ibmi-oss-resources](https://github.com/IBM/ibmi-oss-resources) | Curated list of IBM i open-source resources | Further reading |
| [IBM/vscode-ibmi-projectexplorer](https://github.com/IBM/vscode-ibmi-projectexplorer) · [docs](https://ibm.github.io/vscode-ibmi-projectexplorer) | IBM i Project Explorer for VS Code: local projects, `iproj.json`, one-click TOBi builds | `skills/ibmi-build` templates |

## Related open-source projects (IBM i community)

| Repository | What it is |
|---|---|
| [Mapepire-IBMi/mapepire-server](https://github.com/Mapepire-IBMi/mapepire-server) · [sysadmin guide](https://mapepire-ibmi.github.io/guides/sysadmin/) | Database server on IBM i that the MCP server and Python use |
| [Mapepire-IBMi/mapepire-python](https://github.com/Mapepire-IBMi/mapepire-python) | Python client (`pip install mapepire-python`), used by `ibmi_tool.py` |
| [Mapepire-IBMi/mapepire-js](https://github.com/Mapepire-IBMi/mapepire-js) | Node.js client |
| [codefori/vscode-ibmi](https://github.com/codefori/vscode-ibmi) · [docs](https://codefori.github.io/docs/) | Code for IBM i, the VS Code extension for IBM i development |
| [codefori/vscode-rpgle](https://github.com/codefori/vscode-rpgle) | RPGLE language support and linter |
| [codefori/vscode-db2i](https://github.com/codefori/vscode-db2i) | Db2 for i SQL tooling for VS Code |
| [tools-400/irpgunit](https://github.com/tools-400/irpgunit) · [docs](https://tools-400.github.io/irpgunit/) | iRPGUnit unit-testing framework, used by `skills/rpgunit-testing` |

## IBM i language references
- IBM Documentation for IBM i 7.5: [ibm.com/docs/en/i/7.5](https://www.ibm.com/docs/en/i/7.5).
  Search there for *ILE RPG Reference*, *CL command finder*, *Db2 for i SQL reference* and *IBM i services*.
