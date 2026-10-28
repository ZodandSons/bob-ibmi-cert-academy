---
name: rpgle-free-format
description: Write new modern fully free-format RPGLE (RPG IV) programs, modules, procedures, service programs and copybooks following shop standards. Use when creating or substantially rewriting RPG code, designing procedures or service programs, or asking how to do something in modern RPG.
---

# Modern free-format RPG IV

## Templates (copy, then fill in)
| Template | Becomes |
|----------|---------|
| `templates/program.pgm.rpgle` | A bound program with parameters and error handling |
| `templates/service.sqlrpgle` | A NOMAIN module (with embedded SQL) for a service program |
| `templates/service.rpgleinc` | The matching prototype copybook |
| `templates/service.bnd` | Binder source with signature |

Quick reference for built-in functions and data types: `reference/bif-cheatsheet.md`.

## Steps for a new program

<Steps>
<Step>
Decide the object type: **program** (one entry point, called by CL/menu) or
**service program** (reusable procedures called from many programs).
</Step>
<Step>
Copy the matching template into the right folder with the right extension
(`qrpglesrc/name.pgm.rpgle`, `qrpglesrc/name.sqlrpgle` + `qprotosrc/name.rpgleinc` +
`qsrvsrc/name.bnd`). The object name is the part before the first dot.
</Step>
<Step>
Declare the interface first: `dcl-pi` for the program, prototypes for procedures.
Use `const` for input parameters, `value` for small scalars, and return values
instead of output parameters where possible.
</Step>
<Step>
Write the mainline as a short sequence of procedure calls. Keep each procedure
under ~60 lines with one responsibility.
</Step>
<Step>
Add error handling: `monitor` around I/O and conversions, `%error` after `(e)`
opcodes, `SQLSTATE` checks after SQL (see the `sqlrpgle-db2` skill).
</Step>
<Step>
Add the build dependency (see `ibmi-build`) and a test (see `rpgunit-testing`), then compile.
</Step>
</Steps>

## Patterns to prefer
- `dcl-ds customer likerec(CUSTREC : *all);` (likerec is implicitly qualified) + `chain (custNo) CUSTMAST customer;`
- `for-each item in items;` (7.3 TR9 / 7.4 TR3 and later) or `for i = 1 to %elem(arr);`
- `select; when ...; other; endsl;` instead of nested `if` chains.
- `%char`, `%dec`, `%editc`, `%trim`, `%scanrpl`, `%split` (7.4+) for strings.
- `data-into` / `data-gen` with YAJL for JSON; SQL `JSON_TABLE` for parsing in SQL.
- Varying-length fields (`varchar`) for anything built up by concatenation.
- `ctl-opt main(main);` + `dcl-proc main;` for programs that should not use the RPG cycle.

## Patterns to avoid
Numbered indicators, `GOTO`, `MOVE` family, `*ENTRY PLIST`, global variables used to pass
data between procedures, and `/copy` of anything other than prototypes and constants.
