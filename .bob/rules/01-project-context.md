# Project context (applies to every mode)

- Platform: IBM i 7.5, Db2 for i, CCSID 37. Source is stored in git as stream files and
  built with TOBi, The Object Builder for i (`makei`; formerly Better Object Builder). Do not assume source physical files exist.
- Build target is the developer's own library (`&DEVLIB`, e.g. `ORDDEV01`). Never build
  into `ORDTST`, `ORDPRD` or `ORDDTA`.
- File extensions identify object type and language. Always use them when creating files:

| Extension | Meaning |
|-----------|---------|
| `.pgm.rpgle` / `.pgm.sqlrpgle` | Program (bound, single module) |
| `.rpgle` / `.sqlrpgle` | Module (for service programs) |
| `.rpgleinc` | Copybook / prototypes |
| `.pgm.clle` | CL program |
| `.cmd` | Command definition |
| `.bnd` | Binder source |
| `.table`, `.view`, `.index`, `.sqlprc`, `.sqludf` | DDL |
| `.pf`, `.lf`, `.dspf`, `.prtf` | DDS (legacy — do not create new PF/LF) |

- Object names are max 10 characters, uppercase in commands, and the source file name
  (before the first dot) is the object name.
- `qrpglesrc/legacy/` holds the original fixed-format sources and is read-only.
