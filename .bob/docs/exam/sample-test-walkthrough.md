# IBM sample test: walkthrough

[Exam home](README.md)

IBM publishes a 10-question **sample test** for C3000-006 (*IBM Bob v2 Developer – Associate*),
available with the study guide from the IBM Professional Certification Program. Take it
**first, cold**, then read this page. It explains the concept behind each question and where
this repo teaches it. The questions themselves aren't reproduced here; use IBM's PDF.

| # | Section | Concept being tested | Answer | Why the others are wrong | Learn it here |
|---|---|---|---|---|---|
| 1 | 1 Concepts | The **example** prompt component means pointing Bob at a concrete good model in *your* codebase | d | "Act as…" is a *role*; generic docs or "find examples" don't give Bob a specific model | [1.1](section-1-concepts.md#11-write-effective-prompts), [`/plan-ibmi-change`](../../commands/plan-ibmi-change.md) |
| 2 | 2 Core features | Built-in modes **can** be customized: edit the mode's **AGENTS.md** (rules file) in `.bob` | d | There's no `custom_modes.md` or `RULES.md`; "can't be edited" is false | [1.2](section-1-concepts.md#12-initiate-a-project-agentsmd), [`rules-agent/AGENTS.md`](../../rules-agent/AGENTS.md) |
| 3 | 2 Core features | **SDLC partner**: planning, implementing, commits/PRs, modernization | d | Repo hosting and HR/payroll aren't Bob's job | [2.9](section-2-core-features.md#29-bob-as-ai-development-partner-across-the-sdlc) |
| 4 | 2 Core features | **Six context-window categories** | d | Modes, prompt pieces and tool groups are different lists | [2.14](section-2-core-features.md#214-define-and-identify-the-context-window), [cheat sheet](cheat-sheet.md#context-window-6-categories) |
| 5 | 3 Use cases | **Rollback snapshots are taken before file changes, not before terminal commands** | d | Snapshots don't wait for commits, aren't disabled by Agent mode, aren't manual | [6.7](section-6-security.md#67-rollback-changes) |
| 6 | 4 Configuration | A rule for one subdirectory → **scope it to that subdirectory in project rules** | d | Global rules apply everywhere; "tell others to ignore it" or repeating it in prompts is fragile | [4.8](section-4-configuration.md#48-custom-rules-global-vs-project), [`rules/04-…`](../../rules/04-ddl-backward-compatibility.md) |
| 7 | 5 Accounts | Later prompts cost more because the **full active context is processed again each prompt** | d | System prompt and MCP definitions don't grow per response; reserved space is fixed | [5.5](section-5-accounts.md#55-token-usage-for-prompting) |
| 8 | 6 Security | `.bobignore` is checked by **file operations**: `read_file` and `apply_diff` (two answers) | b, c | Creating tasks, switching modes and changing themes don't touch files | [6.4](section-6-security.md#64-produce-a-bobignore-file) |
| 9 | 6 Security | Suspicious approval scope → **deny, review what widened it (e.g. @ mentions), ask for narrower** | c | "Approve then roll back" is risky; writes aren't irreversible; removing all edit permissions overreacts | [6.5](section-6-security.md#65-correct-permissions-and-approval-workflows) |
| 10 | 6 Security | Credentials → **approved secrets solution, provided at runtime** | a | Pasting "temporarily", "don't write files" or "short prompts are fine" all still expose the secret | [6.6](section-6-security.md#66-best-security-practices) |

## Patterns in IBM's questions
- **Scenario first.** Most questions describe a developer situation and ask for the *best*
  action. Eliminate options that are unsafe, overreact, or ignore a Bob feature built for the job.
- **"Select two"** appears. Read the stem for the count.
- **Distractors reuse real Bob words** (modes vs tool groups vs context categories). Know which
  list is which; the [cheat sheet](cheat-sheet.md) separates them.
- The sample is **not** representative of full coverage. IBM recommends the paid assessment
  test (Pearson VUE) as the readiness check. Use this repo's [practice questions](practice-questions.md)
  to cover every objective.
