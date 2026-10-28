# Spec → declaration mapping

## H-spec → ctl-opt
`H DFTACTGRP(*NO) ACTGRP('X')` → `ctl-opt dftactgrp(*no) actgrp('X');`
Multiple H-specs merge into one or more `ctl-opt` statements. A missing H-spec plus a
`H` data area (`DFTHSPEC`) means defaults came from there — check before assuming.

## F-spec → dcl-f
| Columns | Fixed | Free |
|---------|-------|------|
| 17 type | `I` | `usage(*input)` (default for DISK) |
| 17 type | `U` | `usage(*update:*delete)` — add `*output` if `A` in col 20 |
| 17 type | `O` | `usage(*output)` |
| 17 type | `C` (WORKSTN) | default for WORKSTN; no keyword needed |
| 20 | `A` | add `*output` to usage |
| 22 format | `E` | (default — externally described) |
| 34 | `K` | `keyed` |
| 36-42 device | `DISK` | default; `WORKSTN` / `PRINTER` / `SPECIAL` must be stated |
| keywords | `RENAME`, `PREFIX`, `INFDS`, `SFILE` … | carried over unchanged |

Example: `FCUSTMAST  UF A E           K DISK` → `dcl-f CUSTMAST usage(*update:*delete:*output) keyed;`

## D-spec → dcl-*
| Cols 24-25 | Free |
|------------|------|
| `S` | `dcl-s name type(len:dec) keywords;` |
| `C` | `dcl-c name value;` |
| `DS` | `dcl-ds name keywords; ... end-ds;` (`end-ds` omitted only with `likerec`/`extname` and no subfields) |
| `PR` | `dcl-pr name rtntype keywords; ... end-pr;` |
| `PI` | `dcl-pi name rtntype; ... end-pi;` |

Data types (col 40): `A`→`char`, `P`→`packed`, `S`→`zoned`, `I`→`int`, `U`→`uns`,
`F`→`float`, `D`→`date`, `T`→`time`, `Z`→`timestamp`, `N`→`ind`, `*`→`pointer`,
`G`→`graph`, `C`→`ucs2`. Blank type: `char` if no decimals, otherwise **packed** for
standalone fields but **zoned** for data-structure subfields.

`int` and `uns` lengths change meaning: fixed `10I 0` → free `int(10)`; `5I 0` → `int(5)`.

From/to positions in a DS (cols 26-39) → `pos(n)` plus length, or use `overlay`.

## P-spec → dcl-proc
`P name   B   EXPORT` … `P name   E` → `dcl-proc name export; ... end-proc;`

## O-spec (internally described printer)
No direct free equivalent. Prefer creating an externally described PRTF that reproduces
the layout; flag as `TODO-CONV` and keep the O-specs in a separate note for the developer.
