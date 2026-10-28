# The `.bob` folder: start here

This folder configures **[IBM Bob](https://bob.ibm.com/docs)**, IBM's AI coding assistant,
for an IBM i development team. It is a complete, working **teaching example**: every
`.bob` component is used at least once, every file explains itself, and the guides in
[`docs/`](docs/) walk you through each piece with a "Try it" exercise.

**New to IBM Bob?** Read [docs/00 What is IBM Bob](docs/00-what-is-ibm-bob.md) (10 min),
then [docs/01 Getting started](docs/01-getting-started.md) (30–45 min).

> 🎓 **Preparing for IBM certification C3000-006, *IBM Bob v2 Developer – Associate*?**
> This folder is also a complete study guide. The [certification track](docs/exam/README.md)
> maps **every exam objective** to a study page and to something in this repo you can open,
> run or change. It includes a 10-day plan, a [cheat sheet](docs/exam/cheat-sheet.md),
> a [walkthrough of IBM's sample test](docs/exam/sample-test-walkthrough.md) and
> **77 practice questions** with an interactive quiz:
> `python3 .bob/docs/exam/quiz/quiz.py --exam`

---

## Learning path

| # | Guide | You'll learn | Time |
|---|---|---|---|
| 00 | [What is IBM Bob?](docs/00-what-is-ibm-bob.md) | Bob IDE vs Bob Shell, built-in modes, how a request flows through `.bob` | 10 min |
| 01 | [Getting started](docs/01-getting-started.md) | Install, open the repo, a 9-point "is it loaded?" checklist, first tasks | 45 min |
| 02 | [AGENTS.md and .bobignore](docs/02-agents-md-and-bobignore.md) | The project briefing and the "do not open" list | 10 min |
| 03 | [Rules](docs/03-rules.md) | Always-on standards, for all modes or just one | 10 min |
| 04 | [Custom modes](docs/04-custom-modes.md) | Personas with restricted tools and files | 15 min |
| 05 | [Skills](docs/05-skills.md) | On-demand recipes with templates and scripts | 15 min |
| 06 | [Slash commands](docs/06-slash-commands.md) | Saved prompts: `/convert-to-free`, `/review-ibmi`… | 10 min |
| 07 | [MCP servers](docs/07-mcp-servers.md) | Connecting Bob to a live IBM i (read-only) | 20 min |
| 08 | [Hooks](docs/08-hooks.md) | Scripts that log, add context, or block actions | 15 min |
| 09 | [Bob Shell](docs/09-bob-shell.md) | The `bob` CLI, `bob run`, batch jobs and CI | 15 min |
| 10 | [IBM i workflows](docs/10-ibmi-workflows.md) | All the pieces together on five real tasks | 15 min |
| 11 | [Troubleshooting](docs/11-troubleshooting.md) | "Why isn't my mode / skill / hook working?" | — |
| 12 | [Glossary](docs/12-glossary.md) | Bob and IBM i terms | — |
| 13 | [Reference links](docs/13-reference-links.md) | Every bob.ibm.com page and IBM GitHub repo used | — |
| 🎓 | [Certification track](docs/exam/README.md) | C3000-006: 6 section guides, cheat sheet, sample-test walkthrough, 77-question quiz | 10 days |

---

## What's in this folder

```
your-repo/
├── AGENTS.md ··························· project briefing, loaded every conversation      → docs/02
├── .bobignore ·························· files Bob may never read or edit                  → docs/02
└── .bob/
    ├── README.md ······················· you are here
    ├── docs/ ··························· the guides (our convention; Bob doesn't load it)
    │   └── exam/ ······················· C3000-006 certification track + quiz/
    │
    ├── rules/ ·························· ALWAYS loaded, every mode                         → docs/03
    │   ├── 01-project-context.md           environments, file extensions, naming
    │   ├── 02-ibmi-coding-standards.md     RPG / CL / SQL / Python standards
    │   ├── 03-safety-and-change-control.md never touch PROD, no destructive commands
    │   └── 04-ddl-backward-compatibility.md  rule scoped to qsqlsrc/ + qddssrc/ only
    ├── rules-agent/AGENTS.md ··········· built-in Agent mode (as /init creates it)         → docs/03
    ├── rules-ask/AGENTS.md ············· built-in Ask mode
    ├── rules-plan/ ····················· built-in Plan mode: AGENTS.md + 01-ibmi-planning.md
    ├── rules-rpg-dev/ ·················· loaded only in mode rpg-dev                     → docs/03
    ├── rules-cl-dev/ ··················· loaded only in mode cl-dev
    ├── rules-modernizer/ ··············· loaded only in mode modernizer
    ├── rules-ibmi-reviewer/ ············ loaded only in mode ibmi-reviewer
    │
    ├── custom_modes.yaml ··············· 6 personas with restricted tools                 → docs/04
    │
    ├── skills/ ························· loaded ON DEMAND when a task matches            → docs/05
    │   ├── ibmi-platform/                  IBM i objects, jobs, messages
    │   ├── rpgle-free-format/              writing modern RPG (templates)
    │   ├── rpg-fixed-to-free/              conversion: references, example, 2 scripts
    │   ├── clle-programming/               CL templates, MONMSG patterns
    │   ├── sqlrpgle-db2/                   embedded SQL patterns
    │   ├── ibmi-python/                    working Python CLI for IBM i
    │   ├── bob-shell-automation/           batch + CI scripts, GitHub Actions
    │   ├── ibmi-build/                     TOBi (makei) build templates
    │   └── rpgunit-testing/                RPGUnit test template
    │
    ├── commands/ ······················· /slash commands (file name = command)           → docs/06
    │   ├── convert-to-free.md  review-ibmi.md  new-rpg-program.md  new-cl-program.md
    │   ├── explain-program.md  where-used.md   build.md
    │   └── plan-ibmi-change.md (5 prompt components)  impact-analysis.md (subagents)
    │
    ├── mcp.json ························ MCP servers: IBM i via @ibm/ibmi-mcp-server       → docs/07
    ├── mcp-tools/ibmi-dev-tools.yaml ··· the read-only SQL tools that server offers
    │
    ├── settings.json ··················· hook configuration (5 events)                    → docs/08
    ├── hooks/ ·························· hook scripts + test-hooks.sh
    └── .gitignore ······················ keeps hook logs (.bob/logs/) out of git
```

### Quick reference: what loads when

| Piece | Project location | Personal (global) location | Loaded |
|---|---|---|---|
| AGENTS.md | `/AGENTS.md` | — | Every conversation |
| Rules | `.bob/rules/` | `~/.bob/rules/` | Every conversation |
| Mode rules | `.bob/rules-{slug}/` | `~/.bob/rules-{slug}/` | When that mode is active |
| Custom modes | `.bob/custom_modes.yaml` | `~/.bob/settings/custom_modes.yaml` | Mode picker, `/{slug}` |
| Skills | `.bob/skills/<name>/SKILL.md` | `~/.bob/skills/` | When the task matches the description |
| Slash commands | `.bob/commands/<name>.md` | `~/.bob/commands/` | When you type `/<name>` |
| MCP servers | `.bob/mcp.json` | `~/.bob/settings/mcp.json` | Session start |
| Hooks | `.bob/settings.json` | `~/.bob/settings/settings.json` | On their events |
| Ignore list | `/.bobignore` | — | Always |

When the same name exists in both places, **the project version wins**.

---

## Three-minute tour (no IBM i needed)

```bash
# 1. See what Bob's conversion skill sees
python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py \
        .bob/skills/rpg-fixed-to-free/examples/custinq-fixed.pgm.rpgle --format markdown

# 2. Prove the example conversion is sound (exit code 0 = pass)
python3 .bob/skills/rpg-fixed-to-free/scripts/verify_conversion.py \
        .bob/skills/rpg-fixed-to-free/examples/custinq-fixed.pgm.rpgle \
        .bob/skills/rpg-fixed-to-free/examples/custinq-free.pgm.rpgle

# 3. Watch the safety hooks allow and block sample actions
sh .bob/hooks/test-hooks.sh
```

Then open the repo in Bob and type `/` to see the commands, or open the mode picker to
see the six IBM i personas.

## Customize before using it for real

| File | Change |
|---|---|
| [`rules/01-project-context.md`](rules/01-project-context.md), [`../AGENTS.md`](../AGENTS.md) | Your libraries, environments, folder layout |
| [`rules/03-safety-and-change-control.md`](rules/03-safety-and-change-control.md) | Your production library names |
| [`hooks/guard-dangerous-commands.py`](hooks/guard-dangerous-commands.py) | `PROTECTED_LIBS`, then re-run `test-hooks.sh` |
| [`mcp.json`](mcp.json) | Set `DB2i_HOST` / `DB2i_USER` / `DB2i_PASS` in your environment (never in the file) |
| [`skills/rpg-fixed-to-free/reference/pitfalls.md`](skills/rpg-fixed-to-free/reference/pitfalls.md) | Add your shop's own conversion gotchas |

## Official documentation

- **IBM Bob docs:** [bob.ibm.com/docs](https://bob.ibm.com/docs) ·
  [IDE](https://bob.ibm.com/docs/ide) · [Shell](https://bob.ibm.com/docs/shell)
- **Each component:** [Rules](https://bob.ibm.com/docs/ide/configuration/rules) ·
  [Custom modes](https://bob.ibm.com/docs/ide/configuration/custom-modes) ·
  [Skills](https://bob.ibm.com/docs/ide/features/skills) ·
  [Slash commands](https://bob.ibm.com/docs/shell/features/slash-commands) ·
  [MCP](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-in-bob) ·
  [Hooks](https://bob.ibm.com/docs/ide/configuration/lifecycle-hooks) ·
  [.bobignore](https://bob.ibm.com/docs/ide/configuration/bobignore)
- **IBM's own `.bob` example:** [IBM/ibmi-mcp-server/.bob](https://github.com/IBM/ibmi-mcp-server/tree/main/.bob)
- **Full list:** [docs/13 Reference links](docs/13-reference-links.md)

> Bob is evolving quickly. This example matches the docs as of October 2026. If a field
> name stops working, check the [IDE changelog](https://bob.ibm.com/docs/ide/changelog).
