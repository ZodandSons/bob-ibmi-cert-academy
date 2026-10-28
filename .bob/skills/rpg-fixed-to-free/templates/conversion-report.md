# Conversion report — {OBJECT_NAME}

| | |
|---|---|
| Original | `qrpglesrc/legacy/{original-file}` |
| Converted | `qrpglesrc/{converted-file}` |
| Date | {YYYY-MM-DD} |
| Converted by | IBM Bob (`modernizer` mode), reviewed by {developer} |
| Risk level (inventory) | {LOW / MEDIUM / HIGH} |
| verify_conversion.py | {PASS / PASS WITH WARNINGS} |
| Compiled | {yes / no — reason} |
| RPGUnit | {n passed / not available} |

## Inventory before conversion
{paste the markdown output of inventory_fixed.py}

## Decisions
| Line (orig) | Construct | Converted to | Why |
|-------------|-----------|--------------|-----|
| {n} | `MOVEL 'NOT FOUND' pResult` | `%subst(pResult:1:9) = ...` | no (P): rest of field preserved |

## Indicators
| Indicator | Was used for | Now |
|-----------|--------------|-----|
| *IN90 | CHAIN not found | `%found(CUSTMAST)` — not referenced elsewhere |

## TODO-CONV items (need a human)
- [ ] {line} — {description}

## Behaviour notes for testers
- {e.g. non-numeric customer numbers now produce 0 instead of a garbage number}
