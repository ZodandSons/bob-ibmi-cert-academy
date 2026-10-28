# Shared coding standards

## All languages
- Every source starts with a header comment: object name, purpose, author, date, and a
  change log line for each modification (`YYYY-MM-DD initials description`).
- Names: meaningful mixed case in RPG and Python (`customerNumber`), uppercase in CL
  (`&CUSTNO`). No single-letter names except loop counters.
- No hard-coded library names in code. Rely on the library list, or a single named
  constant/parameter when a qualified name is unavoidable.
- No hard-coded user IDs, passwords, IP addresses or host names anywhere.

## RPG
- New code is fully free format: `**free` on line 1, `ctl-opt` not H-specs.
- Required: `ctl-opt option(*srcstmt:*nodebugio) dftactgrp(*no)`; programs that use
  procedures from service programs also specify `bnddir`.
- Never use numbered indicators (`*IN01`–`*IN99`) in new logic. Use `%found`, `%eof`,
  `%error` and named indicators. Display/printer files use an `indds` data structure.
- No `GOTO`, `TAG`, `CABxx`, `MOVE`, `MOVEL`, `MOVEA` or `*ENTRY PLIST` in new code.
- Prefer SQL for set-based data access; native I/O is fine for single-record keyed access.

## CL
- `PGM` with typed `DCL`s, a global `MONMSG CPF0000 EXEC(GOTO ERROR)` and an `ERROR:`
  label that resends the escape message. See the `clle-programming` skill.

## SQL
- Always check `SQLSTATE` (not just `SQLCODE`) after every statement in SQLRPGLE.
- Use parameter markers / host variables. Never build SQL by concatenating user input.

## Python
- Python 3.9+, type hints, `argparse` for CLIs, credentials only from environment variables.
