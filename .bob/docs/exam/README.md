# Certification track: C3000-006 · IBM Bob v2 Developer – Associate

[Docs home](../../README.md)

This folder turns the `.bob` example into a **study guide for IBM's C3000-006 exam**. Every
exam objective in IBM's study guide is mapped below to (a) a study page with the facts and
(b) something in this repository you can open, run or change.

> IBM's own advice for each objective: *Do you know how to do the task? Why it's done?
> What happens if you do it wrong?* If you can't say yes to all three, do the lab.

## The exam at a glance
| § | Section | Weight | Study page | Practice questions |
|---|---|---|---|---|
| 1 | Concepts | 17% | [section-1-concepts.md](section-1-concepts.md) | 13 |
| 2 | Bob core features | **23%** | [section-2-core-features.md](section-2-core-features.md) | 18 |
| 3 | Bob use cases | 19% | [section-3-use-cases.md](section-3-use-cases.md) | 15 |
| 4 | Bob configuration | 17% | [section-4-configuration.md](section-4-configuration.md) | 13 |
| 5 | Bob accounts | 8% | [section-5-accounts.md](section-5-accounts.md) | 6 |
| 6 | Bob security | 16% | [section-6-security.md](section-6-security.md) | 12 |

Supporting material:
- [cheat-sheet.md](cheat-sheet.md): one page of paths, numbers and lists, plus the
  **docs-vs-exam-guide wording differences**
- [sample-test-walkthrough.md](sample-test-walkthrough.md): concepts behind IBM's 10 sample questions
- [practice-questions.md](practice-questions.md): 77 original questions with explanations, at least one per objective
- [`quiz/quiz.py`](quiz/quiz.py): the same questions as an interactive, self-scoring terminal quiz
- [labs/](labs/): hands-on lab files

IBM doesn't publish the question count or passing score in the study guide. Aim for **≥ 80%
in every section** of the practice quiz before booking the assessment test.

## Suggested 10-day plan (about 1–1.5 hours/day)
| Day | Study | Do in this repo |
|---|---|---|
| 1 | [00](../00-what-is-ibm-bob.md), [01](../01-getting-started.md); take IBM's sample test cold | Install Bob; run the 9-point load checklist |
| 2 | [Section 1](section-1-concepts.md) + guides [02](../02-agents-md-and-bobignore.md), [05](../05-skills.md) | Run `/init` in a scratch folder; read `rules-agent/AGENTS.md`; run the conversion scripts |
| 3 | [Section 2](section-2-core-features.md) §2.1–2.8 + guides [03](../03-rules.md), [04](../04-custom-modes.md) | Switch modes; try the Reviewer restriction lab |
| 4 | [Section 2](section-2-core-features.md) §2.9–2.15 + guide [09](../09-bob-shell.md) | Code actions; `bob chat`, `!` shell mode; watch the context indicator |
| 5 | [Section 3](section-3-use-cases.md) §3.1–3.5 | `/plan-ibmi-change` → Agent; literate coding lab |
| 6 | [Section 3](section-3-use-cases.md) §3.6–3.11 + guide [10](../10-ibmi-workflows.md) | `/impact-analysis` (subagents); Review panel + Findings |
| 7 | [Section 4](section-4-configuration.md) + guides [06](../06-slash-commands.md), [07](../07-mcp-servers.md) | Add an MCP tool; create a PR with the template |
| 8 | [Section 5](section-5-accounts.md) + [Section 6](section-6-security.md) + guide [08](../08-hooks.md) | `test-hooks.sh`; permissions and rollback lab |
| 9 | `python3 quiz.py --exam`; re-read weak sections | Redo labs for missed objectives |
| 10 | [Cheat sheet](cheat-sheet.md); `quiz.py --exam` again; sample test again | Book the assessment if ≥ 80% everywhere |

## Run the practice quiz
```bash
pip install pyyaml                                   # once
python3 .bob/docs/exam/quiz/quiz.py --exam           # full weighted exam, all 77, shuffled
python3 .bob/docs/exam/quiz/quiz.py --section 4      # one section
python3 .bob/docs/exam/quiz/quiz.py --count 15       # quick random 15
python3 .bob/docs/exam/quiz/quiz.py --objective 6.5  # one objective
python3 .bob/docs/exam/quiz/quiz.py --review         # read every question with answers
```
Answer with letters (`b` or `b,c` for "select two"). You get the explanation and study link
after each question, and a per-section score at the end.

---

## Objective coverage map
**Study** = where the facts are. **Practice** = something in this repo to open, run or change.

### Section 1 · Concepts (17%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 1.1 | Write effective prompts (5 components, specificity, context, decomposition, examples) | [S1](section-1-concepts.md#11-write-effective-prompts) | [`commands/plan-ibmi-change.md`](../../commands/plan-ibmi-change.md) (role / instruction / context / example / cue) |
| 1.2 | Initiate a project: `/init`, root and mode AGENTS.md, maintenance | [S1](section-1-concepts.md#12-initiate-a-project-agentsmd), [02](../02-agents-md-and-bobignore.md) | [`AGENTS.md`](../../../AGENTS.md), [`rules-agent/`](../../rules-agent/AGENTS.md), [`rules-plan/`](../../rules-plan/AGENTS.md), [`rules-ask/`](../../rules-ask/AGENTS.md) |
| 1.3 | Why use an MCP server (standard, extension, local/remote, scope, security) | [S1](section-1-concepts.md#13-why-use-an-mcp-server), [07](../07-mcp-servers.md) | [`mcp.json`](../../mcp.json) |
| 1.4 | Structure of Bob skills (folder, SKILL.md, front matter, resources, activation) | [S1](section-1-concepts.md#14-structure-of-bob-skills), [05](../05-skills.md) | [`skills/rpg-fixed-to-free/`](../../skills/rpg-fixed-to-free/SKILL.md) |

### Section 2 · Bob core features (23%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 2.1 | File system: read, create, modify; read tools | [S2](section-2-core-features.md#21-use-bobs-file-system-to-read-create-and-modify-project-files) | Hook matchers in [`settings.json`](../../settings.json) |
| 2.2 | Add a custom mode (why, components, global vs project) | [S2](section-2-core-features.md#22-add-a-custom-mode), [04](../04-custom-modes.md) | [`custom_modes.yaml`](../../custom_modes.yaml) |
| 2.3 | Premium packages | [S2](section-2-core-features.md#23-purpose-of-ibm-premium-packages) | Compare with this repo's DIY skills/modes |
| 2.4 | Role of .bobignore (+ limitations) | [S2](section-2-core-features.md#24-role-of-bobignore), [02](../02-agents-md-and-bobignore.md) | [`.bobignore`](../../../.bobignore) |
| 2.5 | Three default modes, Plan→Agent→Ask, per-task permissions | [S2](section-2-core-features.md#25-the-three-default-modes) | `rules-agent/`, `rules-plan/`, `rules-ask/` |
| 2.6 | How Bob selects LLMs | [S2](section-2-core-features.md#26-how-bob-selects-llm-models) | — (concept) |
| 2.7 | Bob Shell: `bob chat`, `bob run`, cost control, `!` | [S2](section-2-core-features.md#27-use-bob-shell-from-the-command-line), [09](../09-bob-shell.md) | [`batch-convert.sh`](../../skills/bob-shell-automation/scripts/batch-convert.sh) |
| 2.8 | Architecture: agent, harness, clients | [S2](section-2-core-features.md#28-components-of-bobs-architecture) | Same `.bob` works in IDE and Shell |
| 2.9 | Bob across the SDLC | [S2](section-2-core-features.md#29-bob-as-ai-development-partner-across-the-sdlc), [10](../10-ibmi-workflows.md) | Workflows A–E |
| 2.10 | Bobcoins and Bobalytics monitoring | [S2](section-2-core-features.md#210-monitor-usage-and-bobcoins-with-bobalytics), [S5](section-5-accounts.md) | `summarize_results.py` (cost per run) |
| 2.11 | Intelligent routing | [S2](section-2-core-features.md#211-how-bob-optimizes-token-consumption-intelligent-routing) | — (concept) |
| 2.12 | Code actions and literate coding | [S2](section-2-core-features.md#212-different-ways-of-using-code-functions) | [`labs/literate-coding-ordtotal.rpgle`](labs/literate-coding-ordtotal.rpgle) |
| 2.13 | MCP integration (JSON-RPC, client-server, token cost) | [S2](section-2-core-features.md#213-integrate-bob-with-external-tools-through-mcp), [07](../07-mcp-servers.md) | [`mcp-tools/ibmi-dev-tools.yaml`](../../mcp-tools/ibmi-dev-tools.yaml) |
| 2.14 | Context window (6 categories, monitoring) | [S2](section-2-core-features.md#214-define-and-identify-the-context-window), [S4](section-4-configuration.md#42-utilize-context-window-management) | Short rules; skills on demand |
| 2.15 | Standardize behaviour with rules | [S2](section-2-core-features.md#215-standardize-bob-behaviour-with-rules), [03](../03-rules.md) | [`rules/`](../../rules/) |

### Section 3 · Bob use cases (19%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 3.1 | Plan before coding; inspect and refine the plan | [S3](section-3-use-cases.md#31-create-inspect-and-refine-a-plan-before-coding) | [`/plan-ibmi-change`](../../commands/plan-ibmi-change.md), [`rules-plan/`](../../rules-plan/) |
| 3.2 | Literate coding | [S3](section-3-use-cases.md#32-literate-coding-create-code-from-comments) | [`labs/literate-coding-ordtotal.rpgle`](labs/literate-coding-ordtotal.rpgle) |
| 3.3 | SDLC capabilities: understand, generate, modify, document, automate | [S3](section-3-use-cases.md#33-core-sdlc-capabilities-understand-generate-modify-document-automate) | `/explain-program`, `/new-rpg-program`, `/convert-to-free` |
| 3.4 | Modes vs skills vs rules vs hooks vs AGENTS.md | [S3](section-3-use-cases.md#34-when-to-use-modes-skills-rules-hooks-and-agentsmd), [10](../10-ibmi-workflows.md) | All of them, side by side |
| 3.5 | Bob Shell vs Bob IDE | [S3](section-3-use-cases.md#35-bob-shell-vs-bob-ide) | `/review-ibmi` vs `ci-review.sh` |
| 3.6 | Bob alone vs external tools | [S3](section-3-use-cases.md#36-bob-alone-vs-with-specialized-tools-or-external-applications) | Bob writes code; TOBi/IBM i build and run it |
| 3.7 | Subagents and subtasks | [S3](section-3-use-cases.md#37-subagents-and-subtasks) | [`/impact-analysis`](../../commands/impact-analysis.md), `allowedSubagents` |
| 3.8 | Modernize applications | [S3](section-3-use-cases.md#38-modernize-applications-using-bob) | [`skills/rpg-fixed-to-free/`](../../skills/rpg-fixed-to-free/SKILL.md), `modernizer` mode |
| 3.9 | Build AI agents | [S3](section-3-use-cases.md#39-build-ai-agents-using-bob) | MCP tool YAML; `--list-toolsets` |
| 3.10 | Debug and correct defects | [S3](section-3-use-cases.md#310-debug-application-problems-with-bob) | `/build`, workflow D |
| 3.11 | Code review and Bob Findings | [S3](section-3-use-cases.md#311-code-review-and-bob-findings) | `ibmi-reviewer` mode, `/review-ibmi` |

### Section 4 · Bob configuration (17%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 4.1 | Tools (read, write, command, subagent, subtask, MCP, mode, skill, workflow, todo, question) | [S4](section-4-configuration.md#41-tools-read-command-subtask-mcp) | `settings.json` matchers; mode `groups` |
| 4.2 | Context window management (270k, 190k, 8.5k, best practices) | [S4](section-4-configuration.md#42-utilize-context-window-management) | Lean rules; subagent command |
| 4.3 | Context mentions | [S4](section-4-configuration.md#43-context-mentions-) | `@` mentions in `/plan-ibmi-change` |
| 4.4 | Extensions (premium packages, Shell companion `/ide`) | [S4](section-4-configuration.md#44-download-extensions) | — (product UI) |
| 4.5 | Develop and add MCP tools (config, transports, security) | [S4](section-4-configuration.md#45-develop-and-add-mcp-tools), [07](../07-mcp-servers.md) | [`mcp.json`](../../mcp.json), add-a-tool exercise in 07 |
| 4.6 | Create custom modes (validation, override, YAML) | [S4](section-4-configuration.md#46-create-custom-modes) | [`custom_modes.yaml`](../../custom_modes.yaml) |
| 4.7 | Develop skills (approval, settings tab, precedence) | [S4](section-4-configuration.md#47-develop-bob-skills) | Write the `shop-naming` skill (guide 05) |
| 4.8 | Custom rules global vs project (load order, scoping) | [S4](section-4-configuration.md#48-custom-rules-global-vs-project) | [`rules/04-ddl-backward-compatibility.md`](../../rules/04-ddl-backward-compatibility.md) |
| 4.9 | Generate PRs (prereqs, flow, template order) | [S4](section-4-configuration.md#49-generate-pull-requests-from-the-ide) | [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) |

### Section 5 · Bob accounts (8%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 5.1 | Administer Bobalytics | [S5](section-5-accounts.md#51-administer-bobalytics) | — (admin console) |
| 5.2 | Authenticate with API keys (General vs Inference) | [S5](section-5-accounts.md#52-authenticate-with-api-keys) | `BOB_API_KEY` in [`github-actions.yml`](../../skills/bob-shell-automation/examples/github-actions.yml) |
| 5.3 | Enterprise plan features | [S5](section-5-accounts.md#53-enterprise-plan-features) | — (concept) |
| 5.4 | Bobcoins (plans, packs, vs tokens) | [S5](section-5-accounts.md#54-bobcoins) | `--max-cost` in the scripts |
| 5.5 | Token usage for prompting | [S5](section-5-accounts.md#55-token-usage-for-prompting) | Compare weak vs strong prompts (S1 lab) |

### Section 6 · Bob security (16%)
| Obj | Topic | Study | Practice in this repo |
|---|---|---|---|
| 6.1 | Mode permissions per task | [S6](section-6-security.md#61-modify-mode-permissions-in-a-contexttask) | Permissions lab in S6 |
| 6.2 | Reduce context poisoning | [S6](section-6-security.md#62-reduce-context-poisoning) | One task per goal; subagents |
| 6.3 | Project permission restrictions | [S6](section-6-security.md#63-identify-and-enable-correct-permission-restrictions-for-projects) | `ibmi-reviewer`, `ibmi-ops`, `modernizer` modes |
| 6.4 | Produce a .bobignore | [S6](section-6-security.md#64-produce-a-bobignore-file) | [`.bobignore`](../../../.bobignore), [`.gitignore`](../../../.gitignore) |
| 6.5 | Approval workflows, risk levels | [S6](section-6-security.md#65-correct-permissions-and-approval-workflows) | Hooks block what approvals might miss |
| 6.6 | Security best practices | [S6](section-6-security.md#66-best-security-practices) | Defence-in-depth table in S6; [`hooks/`](../../hooks/) |
| 6.7 | Rollback | [S6](section-6-security.md#67-rollback-changes) | Rollback lab in S6 |

## Official IBM resources (from the study guide)
- Docs: [bob.ibm.com/docs/ide](https://bob.ibm.com/docs/ide) · [bob.ibm.com/docs/shell](https://bob.ibm.com/docs/shell) ·
  [interactive Shell](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-interactive) ·
  [non-interactive Shell](https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive)
- [IBM Developer tutorials](https://developer.ibm.com/tutorials/) ·
  [Architecture modernization with IBM Bob](https://developer.ibm.com/articles/architecture-modernization-ibm-bob/)
- Blog: [Bob v2 release announcement](https://bob.ibm.com/blog/bob-v2-release-announcement/#one-agent-one-harness-many-clients) ·
  [Premium Package for Java announcement](https://bob.ibm.com/blog/pp_for_java_announcement/)
- Videos: [1](https://www.youtube.com/watch?v=qdAozfL1mXw) · [2](https://www.youtube.com/watch?v=10RzLWvGO2w) ·
  [3](https://www.youtube.com/watch?v=g9JIUM0MHgQ) · [4](https://www.youtube.com/watch?v=JOOCmaFAmcs) ·
  [playlist](https://www.youtube.com/playlist?list=PL-aWPAFzESis6waeGnNqVLLS7cpROtTe3)
- Schedule the exam: [Pearson VUE (IBM)](https://home.pearsonvue.com/ibm). The assessment test
  reports your score per section, which is the best readiness signal.
