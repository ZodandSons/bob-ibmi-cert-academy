# Section 6 · Bob security (≈16% of the exam)

[Exam home](README.md) · [← Section 5](section-5-accounts.md) · Next: [Cheat sheet →](cheat-sheet.md)

Objectives: **6.1** mode permissions per task · **6.2** context poisoning ·
**6.3** project permission restrictions · **6.4** .bobignore · **6.5** approval workflows ·
**6.6** security best practices · **6.7** rollback

This `.bob` folder is built around these objectives. Every guard rail is listed in the
["Defence in depth" table](#defence-in-depth-in-this-repo) at the end.

---

## 6.1 Modify mode permissions in a context/task
- The **Permissions** control **beside the mode selector** decides which actions Bob can take
  **without approval for the current task**.
- **Task-level approvals override the normal approval experience for that task only**. They
  never become global permissions.
- **Read:** view files, list directories, search without asking each time.
- **Edit / Execute:** modify files / run terminal commands without approval. IBM classes these
  as **high risk**.
- **Extended:** **MCP, Skill, Todo, Subtask, Subagent, Mode**.
- **Least-permission task setup:** enable only what the current activity needs and keep the rest approval-gated.

## 6.2 Reduce context poisoning
- **Definition:** wrong, stale or irrelevant information stays in the context window and keeps
  influencing later responses.
- **Symptoms:** drifting answers, incorrect tool use, looping multi-step work, repeated
  regressions, losing the original goal. Corrective prompts help briefly, then it returns.
- **Causes:** Bob's own earlier mistakes, outdated comments/READMEs, large noisy pastes,
  condensation leftovers, unrelated old goals in the transcript.
- **Prevent:** **narrow task scope** (one task per goal; new task when the topic changes);
  state goal, outcome, constraints, files; **lean standing context** (short AGENTS.md and rules;
  only needed MCP servers, tools, skills); **targeted evidence** (`@file`, line ranges, specific
  logs; staged investigation, not huge pastes).
- **Recover:** **start a fresh task** when bad context persists despite corrections (rules and
  files on disk are kept). For broad investigations, **use subagents** so the main task only
  receives condensed findings.

## 6.3 Identify and enable correct permission restrictions for projects
- **Project custom modes** in `.bob/custom_modes.yaml` give persistent, version-controlled tool
  restrictions and can **override a built-in mode** for that project.
- Limit a mode to the **tool groups** it needs; **omit** the rest so it can't use them.
- Constrain `edit` with **`fileRegex`** (e.g. Markdown only, or one source directory).
- **Project risk posture:** combine mode restrictions with **conservative auto-approve**.
  Sensitive or production-related work keeps **more manual approvals and narrower permissions**
  than routine local development.
- **In this repo:** `ibmi-reviewer` (edit only `reviews/*.md`, no execute), `ibmi-ops` (no edit,
  no execute), `modernizer` (edit `qrpglesrc/` but **not** `legacy/`).

## 6.4 Produce a .bobignore file
- **Purpose:** files/dirs Bob must not access through supported file operations: secrets,
  generated artifacts, large assets, out-of-scope areas.
- **Location:** workspace root. **Syntax:** `.gitignore`-compatible: `node_modules/`, `*.log`,
  `config/secrets.json`, `!important.log` (exception).
- **Enforced by** Bob file operations such as `read_file`, `write_file`, `apply_diff` and symbol
  parsing. **Not** by unrelated actions like creating tasks, switching modes or changing themes.
- Bob **monitors and reloads** it automatically. The file is **implicitly ignored**, so Bob can't
  edit its own access rules.
- **Limitation:** workspace access control, **not a system-level sandbox**.
- **Secret-bearing files** should *also* be in `.gitignore` and handled by secrets management.
  File access controls don't replace permission review.
- **In this repo:** [`.bobignore`](../../../.bobignore) + [`.gitignore`](../../../.gitignore)
  (both exclude `.env`, keys).

## 6.5 Correct permissions and approval workflows
- **Default:** before a tool runs, an **approval prompt** shows the action. Prompts appear one
  at a time; big details (diffs, command output) expand on demand.
- **Editable command approval:** change a proposed terminal command *in the prompt* before running it.
- **Global auto-approve:** selected categories run without confirmation. Smoother, but fewer
  chances to inspect.
- **Task-level approval:** grant for one task without changing global settings.
- **Risk-based approval levels (memorize):**
  | Risk | Permissions |
  |---|---|
  | **High** | **Edit, Execute** |
  | **Medium-high** | **MCP** |
  | **Medium** | **Read, Skill** |
  | **Low** | **Todo, Subtask, Subagent, Mode** |
- **When a prompt looks wrong** (e.g. a write touching three directories when you asked for one):
  **deny it, review what widened the scope (e.g. broad `@` mentions), and ask for a narrower
  proposal.** Don't "approve and roll back later", and don't overreact by removing all edit permissions.
- Bob Shell: approve once / approve group for task / always allow this command for task / reject,
  with an optional note. A keyboard toggle switches auto-approve (see the cheat sheet's
  differences table); `bob run` pre-approves everything (hence hooks).

## 6.6 Best security practices
- **Restrict file access early** with `.bobignore`.
- **Limit auto-approve:** keep human review where impact or risk isn't fully understood. Enable
  Edit/Execute auto-approval only in controlled situations.
- **Protect secrets:** never in prompts, code snippets or Bob-readable files. Use **approved
  secrets management**, least-privilege credentials, **OAuth/delegated access**, time-limited tokens.
  Provide credentials **at runtime** from the secrets store.
- **Secure MCP:** authenticate, encrypt, restrict server actions, keep audit records.
- **Human review and operational controls:** review generated content and commands, keep Bob
  and dependencies current, train users on AI risks, have an incident-response process.
- **Dedicated workspaces** for sensitive projects; scope each task to minimum permissions.

## 6.7 Rollback changes
- **Purpose:** automatic versioning of workspace files during Bob tasks so unwanted changes can
  be compared or reversed. Supports experiments, comparing approaches, recovery.
- **Mechanism:** snapshots in a **shadow Git repository, separate from your project's own repo**.
- **When snapshots are taken:** **when tasks begin** and **before file modifications**.
  **Not automatically before terminal commands.** If a command changed something, there may be
  no snapshot from just before it.
- **View differences** between the workspace and a snapshot: added, removed, modified, new, deleted files.
- **Restore files:** workspace back to the snapshot, **conversation kept** (try an alternative approach).
- **Restore files and task:** files back **and** later messages removed. Requires confirmation,
  **cannot be undone**.
- **Limitations:** unsaved work can be overwritten; **changes made outside active Bob tasks**
  aren't captured. *(Docs also note that `.gitignore`d files and built-in exclusions like
  `node_modules/` and `.env` aren't snapshotted, while `.bobignore`-only files are.)*

---

## Defence in depth in this repo
| Layer | Exam objective | File |
|---|---|---|
| Hide secrets from Bob's file tools | 6.4 | `.bobignore` |
| Keep secrets out of git | 6.4, 6.6 | `.gitignore` |
| Credentials only via env vars / secrets | 6.6, 4.5 | `mcp.json` (`${DB2i_PASS}`) |
| Least-privilege modes, fileRegex | 6.3 | `custom_modes.yaml` |
| Read-only MCP tools | 6.6, 4.5 | `mcp-tools/ibmi-dev-tools.yaml` (`security.readOnly`) |
| Block secrets typed into prompts | 6.6 | `hooks/block-secrets.py` |
| Block destructive commands / PROD | 6.5, 6.6 | `hooks/guard-dangerous-commands.py` |
| Block writes to protected paths | 6.3 | `hooks/protect-paths.py` |
| Audit trail | 6.6 | `hooks/log-activity.sh`, `session-summary.sh` |
| Always-on safety rules | 6.6 | `rules/03-safety-and-change-control.md` |
| Bounded automation | 6.5, 2.7 | `--max-cost`, `--max-turns`, `--disable-tool-groups` in scripts |

**Lab:** run `sh .bob/hooks/test-hooks.sh`, then in Bob: (1) set Read-only task permissions and
ask for an edit; watch the approval prompt. (2) Let Bob edit a file, then use rollback to
restore it. (3) Run a terminal command that changes a file and confirm there's no snapshot just
before it.

## Check yourself
<details><summary>1. Rank Edit, MCP, Skill and Mode by risk.</summary>Edit (high) > MCP (medium-high) > Skill (medium) > Mode (low).</details>
<details><summary>2. Which two operations are subject to .bobignore: creating a task, read_file, apply_diff, switching modes?</summary><code>read_file</code> and <code>apply_diff</code>.</details>
<details><summary>3. A colleague suggests pasting an API token into chat "just for this task". Recommended approach?</summary>Store it in an approved secrets solution and provide it at runtime.</details>
<details><summary>4. You restored "files and task". Can you undo it?</summary>No. It requires confirmation and cannot be undone.</details>
<details><summary>5. Bob keeps reintroducing an old wrong assumption despite corrections. Best fix?</summary>Start a fresh task with a narrow scope and targeted evidence.</details>
<details><summary>6. Task-level permissions you granted: do they apply to tomorrow's tasks?</summary>No. They apply to the current task only.</details>

**Docs:** [Auto-approve](https://bob.ibm.com/docs/ide/features/auto-approving-actions) ·
[Context poisoning](https://bob.ibm.com/docs/shell/core-concepts/context-poisoning) ·
[Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
[Ignoring files](https://bob.ibm.com/docs/ide/configuration/bobignore) ·
[Rollback](https://bob.ibm.com/docs/ide/features/rollback) ·
[Lifecycle hooks](https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks)
