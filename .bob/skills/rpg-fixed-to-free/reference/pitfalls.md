# Conversion pitfalls — behaviour that silently changes

Check every item against the source before declaring a conversion complete.
Add your shop's own discoveries at the bottom.

1. **MOVEL / MOVE without (P) does not clear the target.** `MOVEL 'ABC' FLD10` changes only
   bytes 1–3. `FLD10 = 'ABC'` blanks bytes 4–10. Use `%subst()` to preserve behaviour.
2. **MOVE is right-aligned.** `MOVE 'X' FLD5` changes byte 5 only. Use `evalr` or `%subst`.
3. **MOVE char → numeric accepts blanks and letters** (uses the digit portion of each byte).
   `%dec()` raises RNX0105. Wrap in `monitor` and decide the fallback explicitly.
4. **Numeric fields defined in C-spec result columns are packed**, not zoned.
5. **Arithmetic overflow:** fixed `ADD`/`SUB`/`MULT`/`Z-ADD` truncate high-order digits silently;
   free-format expressions raise RNX0103. Either prove it cannot overflow, or keep truncation
   with `%rem(value : 10 ** digits)` and say so.
6. **Half-adjust:** `ADD(H)` → `eval(h)`. Missing the `(h)` changes results.
7. **Resulting indicators set *and* used elsewhere.** If `*IN90` from a `CHAIN` is also
   tested later, by a subroutine, by a display file, or passed to another program, keep
   the indicator: `chain key file; *in90 = not %found(file);`
8. **Conditioning indicators (cols 9–11)** wrap the statement in an `if`. `N` means `not`.
   Lines with several conditioning indicators across consecutive specs are AND-ed / OR-ed
   via `AN`/`OR` in cols 7–8 — convert the whole group together.
9. **Level-break indicators (L1–L9) and the RPG cycle** (primary files, `IP`/`UP`, matching
   records `M1`–`M9`) have no free equivalent. Stop and agree on a redesign; flag HIGH.
10. **`GOTO` into or out of a subroutine or loop.** Restructure only when every path is
    clear; otherwise flag `TODO-CONV` and leave a note for a human.
11. **`*ENTRY PLIST` with fewer parameters passed by some callers.** Add `options(*nopass)`
    and check `%parms()` exactly where the old code relied on the field being untouched.
12. **`KLIST` reused for different files** with different key layouts — create one key DS
    per file.
13. **`SUBST` without (P)** leaves the rest of the result unchanged, like `MOVEL`.
14. **`LOOKUP` sets the array index in factor 1 and an indicator.** `%lookup()` returns 0
    when not found and does not change the index variable unless you assign it.
15. **`DO` loop index after the loop** is limit + increment in fixed format; same with `for`,
    but verify if the code reads the index after `enddo`.
16. **Changing `dftactgrp`/`actgrp`** changes file sharing, overrides and commitment
    control scope. Never change them during conversion.
17. **Date fields with `DATFMT`** on the H-spec affect `MOVE` to/from dates. Carry
    `datfmt`/`timfmt` over to `ctl-opt` and use explicit formats in `%date()`/`%char()`.

## Shop-specific (add yours)
- _Example:_ Programs that call `QCMDEXC` with a length field defined as `15 5` must keep
  `packed(15:5)` for that parameter.
