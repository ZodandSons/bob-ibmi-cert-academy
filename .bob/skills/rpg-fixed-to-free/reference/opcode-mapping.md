# Fixed opcode → free-format mapping

`F1` = factor 1, `F2` = factor 2, `R` = result field. `(E)`, `(H)`, `(N)` extenders carry over.

## Arithmetic and assignment
| Fixed | Free | Notes |
|-------|------|-------|
| `Z-ADD F2 R` | `R = F2;` | |
| `Z-SUB F2 R` | `R = -F2;` | |
| `ADD F2 R` (no F1) | `R += F2;` | Fixed truncates on overflow; free raises RNX0103 — see pitfalls |
| `F1 ADD F2 R` | `R = F1 + F2;` | |
| `SUB`, `MULT`, `DIV` | `-`, `*`, `/` | `DIV` + `MVR` → `%div()` and `%rem()` |
| `F1 DIV F2 R` then `MVR R2` | `R = %div(F1:F2); R2 = %rem(F1:F2);` | Only for integer-valued operands; otherwise compute the remainder explicitly |
| `SQRT F2 R` | `R = %sqrt(F2);` | |
| `XFOOT arr R` | `R = %xfoot(arr);` | |
| `TIME R` | `R = %time();` / `%date()` / `%timestamp()` | Depends on R's length — check |

## The MOVE family (most error-prone — read pitfalls.md)
| Fixed | Free (only when types allow) |
|-------|------------------------------|
| `MOVEL(P)` char → char | `R = F2;` |
| `MOVEL` (no P) char → char, F2 shorter | `%subst(R : 1 : %len(F2)) = F2;` |
| `MOVE(P)` char → char | `evalr R = F2;` |
| `MOVE` (no P) char → char, F2 shorter | `%subst(R : %len(R) - %len(F2) + 1) = F2;` |
| `MOVE` char → numeric | `R = %dec(F2 : len : dec);` wrapped in `monitor` (MOVE accepts blanks) |
| `MOVE` numeric → char | `evalr R = %editc(F2 : 'X');` (zero-filled, right-adjusted) |
| `MOVE` date ↔ char/num | `R = %date(F2 : *fmt);` / `R = %char(F2 : *fmt);` |
| `MOVEA` | `%subarr()` or a loop; flag `TODO-CONV` if overlapping |

## Comparison and flow
| Fixed | Free |
|-------|------|
| `F1 IFxx F2` | `if F1 op F2;` (`EQ =`, `NE <>`, `GT >`, `LT <`, `GE >=`, `LE <=`) |
| `ANDxx` / `ORxx` | `and` / `or` on the same `if` |
| `F1 DOWxx F2` / `DOUxx` | `dow` / `dou` |
| `F1 DO F2 idx` | `for idx = F1 to F2;` (F1 defaults to 1) |
| `CASxx` + `ENDCS` | `select; when ...; exsr X; endsl;` |
| `CABxx` / `GOTO` / `TAG` | Restructure with `if`/`leave`/`iter`/`leavesr`; if impossible, flag `TODO-CONV` |
| `ITER`, `LEAVE`, `LEAVESR` | same |
| `COMP` (sets indicators) | `*inXX = (F1 > F2);` etc. — or rewrite the consumer `if` |
| `SETON` / `SETOFF` | `*inXX = *on;` / `*off` |
| `EXSR`, `BEGSR`, `ENDSR` | same (lowercase) |

## File I/O
| Fixed | Free | Indicator replacement |
|-------|------|----------------------|
| `F1 CHAIN file  HI` | `chain F1 file;` | HI → `not %found(file)` |
| `F1 SETLL file  EQ` | `setll F1 file;` | EQ → `%equal(file)` |
| `READ file  EQ` | `read file;` | EQ → `%eof(file)` |
| `F1 READE file  EQ` | `reade F1 file;` | EQ → `%eof(file)` |
| `KLIST` + `KFLD`s | `chain (k1 : k2) file;` or `chain %kds(keyDs) file;` | |
| `WRITE`, `UPDATE`, `DELETE` | same | LO error → `(e)` + `%error()` |
| `EXFMT`, `READC` | same | keep display-file indicators or use `indds` |

## Strings and lookups
| Fixed | Free |
|-------|------|
| `CAT` | `R = %trimr(F1) + ' ' + F2;` (match the blank count in factor 2) |
| `SCAN` | `R = %scan(F1 : F2);` |
| `XLATE` | `R = %xlate(from : to : F2);` |
| `SUBST` | `R = %subst(F2 : start : len);` — careful: fixed SUBST does not pad R |
| `CHECK` / `CHECKR` | `%check()` / `%checkr()` |
| `LOOKUP` | `%lookup()` / `%tlookup()` — returns index, not indicator |

## Calls
| Fixed | Free |
|-------|------|
| `CALL 'PGM'` + `PARM`s | `dcl-pr Pgm extpgm('PGM');` + `Pgm(p1 : p2);` |
| `CALLB` / `CALLP` | prototyped call |
| `RETURN`, `SETON LR` | `*inlr = *on; return;` |
