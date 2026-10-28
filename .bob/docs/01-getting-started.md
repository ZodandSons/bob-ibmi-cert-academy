# 01 · Getting started

[Docs home](../README.md) · [← 00 What is IBM Bob](00-what-is-ibm-bob.md) · Next: [02 AGENTS.md and .bobignore →](02-agents-md-and-bobignore.md)

---

> 📝 **Certification (C3000-006):** this guide covers objectives 1.2, 2.7, 4.4. Exam-focused notes: [Section 1](exam/section-1-concepts.md) · [Section 2](exam/section-2-core-features.md) · [Section 4](exam/section-4-configuration.md).

Goal: install Bob, open a repository that contains this `.bob` folder, and **prove that
each piece is being picked up**. Plan on 30–45 minutes.

## 1. Install

| What | How | Docs |
|---|---|---|
| **Bob IDE** | Download from [bob.ibm.com/download](https://bob.ibm.com/download) and sign in with your IBMid | [Installing](https://bob.ibm.com/docs/ide/getting-started/install) |
| **Bob Shell** | macOS/Linux: `curl -fsSL https://bob.ibm.com/download/bobshell.sh \| bash`<br>Windows: see the docs. Needs **Node.js 24+** | [Install and setup](https://bob.ibm.com/docs/shell/getting-started/install-and-setup) |
| Python 3.9+ | For the helper scripts in `skills/*/scripts/` and `hooks/` | — |
| *(optional)* Mapepire on IBM i | `yum install mapepire-server` on the IBM i. Needed only for the MCP server ([07](07-mcp-servers.md)) | [mapepire-server](https://github.com/Mapepire-IBMi/mapepire-server) |
| *(optional)* TOBi (The Object Builder for i) | `yum install tobi` on the IBM i, for `makei` builds | [IBM/ibmi-tobi](https://github.com/IBM/ibmi-tobi) · [docs](https://ibm.github.io/ibmi-tobi/) |

New to Bob entirely? Do IBM's 20-minute [Quickstart](https://bob.ibm.com/docs/ide/getting-started/quickstart)
first. It uses a small demo project and shows the Ask → Plan → Agent workflow.

## 2. Put the folder in a repository

```
your-repo/                 <- open THIS folder in Bob (the workspace root)
├── AGENTS.md
├── .bobignore
└── .bob/
```

The `.bob` folder only works at the **workspace root**: the folder you open in the IDE,
or the folder you start `bob` from. Opening a parent or child folder means Bob won't see it.

## 3. Check that each piece loads

Work through this list once. Each line takes about a minute.

| # | Piece | How to check | Expected |
|---|---|---|---|
| 1 | Rules + AGENTS.md | Ask mode: *"Which libraries are you never allowed to change, and why?"* | Mentions `ORDPRD`/`ORDDTA` (from `rules/03-…` and `AGENTS.md`) |
| 2 | Custom modes | Open the mode dropdown (or `/mode` in Shell) | RPG Developer, CL Developer, Fixed-to-Free Modernizer, IBM i Reviewer, IBM i Ops Analyst, Python Tools |
| 3 | Mode rules | Switch to **Fixed-to-Free Modernizer**, ask *"What must be true before a conversion is done?"* | Lists the checklist from `rules-modernizer/02-verification.md` |
| 4 | Skills | Bob IDE: **Settings → Skills** tab. Shell: type `/skills` | Nine skills listed (`rpg-fixed-to-free`, `clle-programming`, …) |
| 5 | Slash commands | Type `/` in the chat box | `/convert-to-free`, `/review-ibmi`, `/build`, … with descriptions |
| 6 | Hooks | IDE: **Settings → Hooks**. Shell: `/hooks` | Six hooks across five events |
| 7 | Hook scripts | Terminal, repo root: `sh .bob/hooks/test-hooks.sh` | `11 passed, 0 failed` |
| 8 | MCP | IDE: MCP settings panel. Shell: `bob mcp list` | `ibmi-mcp` (enabled), `ibmi-mcp-shared` (disabled) |
| 9 | .bobignore | Create `.env` with dummy text, then ask in words (no `@` mention) *"What is in .env?"* | Bob refuses: the file is ignored |

If something is missing, see [11 Troubleshooting](11-troubleshooting.md).

## 4. Your first five tasks

Try these in order. The guide in brackets explains what is happening.

1. **Explain a program** (no changes made):
   `/explain-program .bob/skills/rpg-fixed-to-free/examples/custinq-fixed.pgm.rpgle`
   [→ 06 Slash commands](06-slash-commands.md)
2. **Run a skill script yourself** to see what Bob will see:
   ```bash
   python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py \
           .bob/skills/rpg-fixed-to-free/examples/custinq-fixed.pgm.rpgle --format markdown
   ```
   [→ 05 Skills](05-skills.md)
3. **Watch a mode restriction work.** In **IBM i Reviewer** mode, ask Bob to *"fix the
   first issue you find in custinq-free.pgm.rpgle"*. It can't: the mode may only write
   `reviews/*.md`. [→ 04 Custom modes](04-custom-modes.md)
4. **Watch a hook work.** In Agent mode, ask Bob to *"run DLTLIB ORDDEV99"*. The
   PreToolUse hook blocks it. [→ 08 Hooks](08-hooks.md)
5. **Do a real conversion** on a copy of one of your own fixed-format programs:
   put it in `qrpglesrc/legacy/` and run `/convert-to-free qrpglesrc/legacy/<file>`.
   [→ 10 IBM i workflows](10-ibmi-workflows.md)

## 5. Before you share your own `.bob` folder

- Replace the example library names (`ORDDEVxx`, `ORDPRD`, `ORDDTA`) in `rules/01-…`,
  `rules/03-…`, `AGENTS.md` and `hooks/guard-dangerous-commands.py` (`PROTECTED_LIBS`).
- Never commit passwords. `mcp.json` uses `${DB2i_PASS}`-style references ([07](07-mcp-servers.md)).
- Review hook scripts like any other code: they run on every engineer's machine.
