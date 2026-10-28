---
name: review-ibmi
description: 'Review RPG, CL or SQL source against the shop checklist'
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <file-or-folder>
---

Review `$1` as a senior IBM i reviewer.

- Apply `.bob/rules-ibmi-reviewer/01-review-checklist.md` for severities and format.
- Check the shop standards in `.bob/rules/02-ibmi-coding-standards.md`.
- For RPG also check: commitment control on multi-file updates, record locks held across
  `EXFMT`, `%error` / `monitor` around I/O, `SQLSTATE` after every SQL statement.
- For CL also check: global `MONMSG`, `ERROR:` handling, overrides removed, `QTEMP` cleanup.
- If the IBM i MCP server is available, use `where_used` to note the blast radius of
  any changed file or program.

Write the report to `reviews/<object>-<today as YYYYMMDD>.md` and give me the verdict and
the CRITICAL/HIGH findings in chat.
