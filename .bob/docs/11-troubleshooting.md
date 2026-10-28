# 11 · Troubleshooting

[Docs home](../README.md) · [← 10 IBM i workflows](10-ibmi-workflows.md) · Next: [12 Glossary →](12-glossary.md)

---

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing from `.bob` seems to apply | Wrong folder opened as the workspace | Open the folder that **contains** `.bob/` (the repo root), or start `bob` there |
| Custom modes missing | YAML error, duplicate `slug`, or invalid `fileRegex` stops the file loading | Validate: `python3 -c "import yaml; yaml.safe_load(open('.bob/custom_modes.yaml'))"`. Check every slug is unique and every regex compiles |
| A mode's rules are ignored | Folder name doesn't match the slug | `slug: rpg-dev` needs `.bob/rules-rpg-dev/` exactly |
| A rule seems ignored | Too vague, or contradicted by another rule | Make it specific and testable; search `rules/`, `rules-*/` and `AGENTS.md` for conflicts |
| Skill never activates | Missing or weak `description`, or the mode lacks the `skill` group | Rewrite the description as "what + when", with the words people use. Check **Settings → Skills** |
| Skill activation keeps asking permission | Default behaviour | **Settings → Auto-Approve → Skills** |
| `/my-command` not in the menu | Not a `.md` file, or not directly in `.bob/commands/` | Rename to `my-command.md` and place it in `.bob/commands/` |
| `$1` appears literally | No argument typed after the command | Type the argument; check the `argument-hint` |
| Hook never fires | Matcher doesn't match the real tool name | Check **Settings → Hooks** / `/hooks`; test with `sh .bob/hooks/test-hooks.sh` |
| Hook blocks everything | Script crashes with exit 2, or the pattern is too broad | Run it by hand with a sample payload (see [08](08-hooks.md)); read stderr |
| `python3: not found` in a hook (Windows) | Hooks run via `cmd /c` | Use `python` or `py`, or run Bob from WSL |
| MCP server not listed or erroring | Node missing, env vars unset, Mapepire not running | Run `npx -y @ibm/ibmi-mcp-server@latest --list-toolsets --tools .bob/mcp-tools` in a terminal and read the error |
| MCP tools exist but Bob doesn't use them | Mode lacks the `mcp` group | Use Agent, Ask, `ibmi-ops`, `ibmi-reviewer`, `rpg-dev` or `cl-dev` |
| MCP connection refused / certificate error | Port 8076 blocked, or a self-signed certificate | Check the firewall; `ignore-unauthorized: true` for self-signed (dev only) |
| `bob run` authentication error | `BOB_API_KEY` not set (SSO login isn't reused) | `export BOB_API_KEY=...`; general keys also need `--team-id` |
| Bob refuses to read a file | It's in `.bobignore` | Intended for secrets; otherwise adjust `.bobignore` |
| `verify_conversion.py` reports ERRORs | Leftover fixed specs, unbalanced blocks, a lost file or subroutine | Read each line; the message names the construct and line |

Still stuck? Check the [Bob IDE FAQ](https://bob.ibm.com/docs/ide/faq),
[Bob Shell FAQ](https://bob.ibm.com/docs/shell/faq), and the changelogs
([IDE](https://bob.ibm.com/docs/ide/changelog), [Shell](https://bob.ibm.com/docs/shell/changelog)).
Features change quickly, so confirm field names against the docs for your version.
