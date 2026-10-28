---
name: rpg-fixed-to-free
description: Convert fixed-format or mixed RPG III / RPG IV source (H, F, D, C, P, O specs, /free blocks) to fully free-format RPG IV (**free) without changing behaviour. Use for any fixed-to-free conversion, modernization, or "convert this RPG" request.
---

# Fixed-format RPG → fully free RPG IV

The goal is a **translation, not a redesign**. The converted program must compile to the
same behaviour as the original. Refactoring comes later, as a separate change.

## Files in this skill
| File | Use it for |
|------|-----------|
| `reference/opcode-mapping.md` | Every fixed opcode → free equivalent, incl. the `MOVE` family |
| `reference/spec-mapping.md` | H/F/D/P/O specs → `ctl-opt`, `dcl-f`, `dcl-s`, `dcl-ds`, `dcl-pr`, `dcl-proc` |
| `reference/pitfalls.md` | Semantics that silently change if converted naively |
| `examples/custinq-fixed.pgm.rpgle` → `custinq-free.pgm.rpgle` | A worked, annotated example |
| `scripts/inventory_fixed.py` | Pre-conversion inventory and risk score |
| `scripts/verify_conversion.py` | Post-conversion checks (exit code 1 on errors) |
| `templates/conversion-report.md` | The report every conversion must produce |

## Workflow

<Steps>
<Step>
**Inventory.** Run:
`python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py <source> --format markdown`

It reports spec counts, every opcode used, numbered indicators, `MOVE`-family usage,
`GOTO`/`TAG`/`CABxx`, `*ENTRY PLIST`, `KLIST`s, and a risk level. If the risk level is
**HIGH**, show the inventory to the user and agree on an approach before converting.
</Step>

<Step>
**Understand dependencies.** Identify display/printer files (their indicators must be
kept or moved to an `indds`), copybooks (`/COPY`), and called programs. If the IBM i MCP
server is available, check `where_used` for the program.
</Step>

<Step>
**Convert specs in order.** Line 1 is `**free`. Then:
1. H-specs → `ctl-opt` (keep every keyword; add `dftactgrp(*no)` only if it was there or
   the program uses procedures — changing activation group changes behaviour).
2. F-specs → `dcl-f` (see `reference/spec-mapping.md` for usage/keyed/device rules).
3. Fields defined in C-spec result columns → explicit `dcl-s` (numeric = **packed**).
4. D-specs → `dcl-s` / `dcl-c` / `dcl-ds` / `dcl-pr` / `dcl-pi`.
5. `*ENTRY PLIST` → `dcl-pi *n` (or the program's name). `KLIST` → `%kds(ds)` or a key list.
6. C-specs → free statements using `reference/opcode-mapping.md`.
7. P-specs → `dcl-proc` / `end-proc`. O-specs: keep the printer file externally described
   if possible; otherwise convert to a PRTF and flag `TODO-CONV`.
</Step>

<Step>
**Apply the pitfalls list.** Walk through `reference/pitfalls.md` line by line against
this source. Every `MOVE`/`MOVEL`/`MOVEA` gets a `// CONV:` comment explaining the choice.
</Step>

<Step>
**Verify.** Run:
`python3 .bob/skills/rpg-fixed-to-free/scripts/verify_conversion.py <original> <converted>`

Fix every ERROR. Review every WARNING and either fix it or explain it in the report.
Then compile (`makei c -f <converted>`) and run RPGUnit tests if they exist.
</Step>

<Step>
**Report.** Fill in `templates/conversion-report.md` and save it as `conversions/<NAME>.md`.
</Step>
</Steps>

## Naming during conversion
Keep every existing field, file, record-format and subroutine name exactly as is — other
programs, DDS and debug sessions depend on them. Only newly introduced names (e.g. a key
data structure replacing a `KLIST`) follow the modern naming standard.
