# Example `.bob` folder for IBM i development with IBM Bob

A complete, documented example of how to configure **[IBM Bob](https://bob.ibm.com/docs)**
(Bob IDE and Bob Shell) for an IBM i team: RPGLE, CLLE, SQLRPGLE, fixed-to-free RPG
conversion, Python tooling, Bob Shell automation, TOBi builds and RPGUnit tests.

It is written for **engineers new to IBM Bob**. Every component is explained in plain
language, with a working example and links to the official docs and IBM's GitHub repositories.

## 👉 Start here: [`.bob/README.md`](.bob/README.md)

That page has the learning path, a map of every file, and links to the 14 guides in
[`.bob/docs/`](.bob/docs/).

## 🎓 Also a certification study guide
Working through this folder prepares you for **IBM C3000-006, *IBM Bob v2 Developer – Associate***.
The [certification track](.bob/docs/exam/README.md) maps all 51 exam objectives to study notes and
hands-on files here, with a 10-day plan, cheat sheet, sample-test walkthrough and a 77-question
interactive quiz (`python3 .bob/docs/exam/quiz/quiz.py --exam`).

## What's included

| Component | In this example | Guide |
|---|---|---|
| `AGENTS.md` | Project briefing for an order-management system | [02](.bob/docs/02-agents-md-and-bobignore.md) |
| `.bobignore` | Credentials, data extracts, save files | [02](.bob/docs/02-agents-md-and-bobignore.md) |
| Rules | 4 always-on rule files (one directory-scoped) + rules for 4 custom modes and all 3 built-in modes | [03](.bob/docs/03-rules.md) |
| Custom modes | 6 IBM i personas, each with restricted tools and files | [04](.bob/docs/04-custom-modes.md) |
| Skills | 9 skills with templates, references and tested scripts | [05](.bob/docs/05-skills.md) |
| Slash commands | 9 commands (`/convert-to-free`, `/plan-ibmi-change`, `/impact-analysis`…) | [06](.bob/docs/06-slash-commands.md) |
| PR template | `.github/pull_request_template.md` for Bob's PR generation | [exam 4.9](.bob/docs/exam/section-4-configuration.md#49-generate-pull-requests-from-the-ide) |
| MCP | IBM i MCP server with 6 read-only SQL tools | [07](.bob/docs/07-mcp-servers.md) |
| Hooks | 6 hooks across all 5 events, plus a test script | [08](.bob/docs/08-hooks.md) |
| Bob Shell | Batch conversion, CI review gate, GitHub Actions | [09](.bob/docs/09-bob-shell.md) |

## Using it in your repository

1. Copy `.bob/`, `AGENTS.md`, `.bobignore`, `.gitignore` and `.github/` into the **root** of your IBM i git repository.
2. Follow [Getting started](.bob/docs/01-getting-started.md) to check that each piece loads.
3. Replace the example library names and conventions with your own
   (see "Customize before using it for real" in [`.bob/README.md`](.bob/README.md)).

> **Two "Bobs":** *IBM Bob* is the AI assistant this folder configures. IBM's IBM i build
> tool used to be called *Better Object Builder* ("Bob") but was renamed
> **[TOBi](https://github.com/IBM/ibmi-tobi)** (The Object Builder for i) in 2025. Its
> command is still `makei`. Older articles use the old name.
