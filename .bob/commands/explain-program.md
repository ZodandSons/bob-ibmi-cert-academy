---
description: Explain what a legacy RPG or CL program does, in plain English
argument-hint: <source-file>
---
Explain `$1` for a developer who has never seen it. Do not change any files.

Cover, in this order:
1. **Purpose** — one paragraph in business terms.
2. **Interface** — parameters (`*ENTRY PLIST` / `dcl-pi` / CL `PGM PARM`), files used and
   how (input/update/output), data areas, display/printer files.
3. **Flow** — the mainline step by step; name each subroutine/procedure and what it does.
4. **Indicators** — every numbered indicator used and what it means.
5. **Calls** — programs called, and (via the `where_used` MCP tool if available) who calls this one.
6. **Risks** — anything fragile: `MOVE` truncation, `GOTO`, unmonitored I/O, locks.

If `$1` is fixed format, end with the inventory from
`python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py $1 --format markdown`.
