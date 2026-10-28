# Jobs, activation groups and messages

## Jobs
- Qualified job name: `number/user/name` (e.g. `123456/QUSER/ORDNIGHT`).
- Interactive jobs run in `QINTER`, batch in `QBATCH` (or your own subsystem).
- `SBMJOB CMD(CALL PGM(X)) JOB(NAME) JOBD(LIB/JOBD) JOBQ(LIB/JOBQ)` — always name the
  job and pass a job description so the library list is predictable.
- QTEMP is per job. Objects there vanish when the job ends.

## Activation groups
| Setting | Behaviour | Use for |
|---------|-----------|---------|
| `DFTACTGRP(*YES)` | OPM compatibility; no procedures | Never in new code |
| `ACTGRP(*NEW)` | New AG each call, destroyed on return | Rarely — expensive |
| `ACTGRP('APPNAME')` | Named, persists for the job | Application entry programs |
| `ACTGRP(*CALLER)` | Runs in the caller's AG | Service programs, called programs |

Reclaim a named AG with `RCLACTGRP ACTGRP(APPNAME)`.

## Message types
`*ESCAPE` ends the program that receives it unless monitored. `*DIAG` precedes an escape
with detail. `*INFO` / `*COMP` are informational. `*INQ` waits for a reply.

## Messages you will meet
| ID | Meaning | Usual cause |
|----|---------|-------------|
| CPF9801 | Object not found | Library list, typo, object not built |
| CPF9802 | Not authorized to object | Authority; check `DSPOBJAUT` |
| CPF9810 | Library not found | Library list / JOBD |
| CPF4131 | Level check | File changed, program not recompiled (`LVLCHK`) |
| CPF5032 | Record already locked | Another job holds the record; see `WRKOBJLCK` |
| CPF3142 | File not found | Override or library list |
| MCH1210 | Receiver too small | Numeric overflow in CL / MI |
| MCH3601 | Pointer not set | Parameter not passed (*nopass / missing parm) |
| RNX1211 | I/O on closed file | `*INLR` set then file used, or USROPN not opened |
| RNX1218 | Record locked | Same as CPF5032 from RPG |
| RNX0100 | Array index out of range | Index 0 or > dim |
| RNX0103 | Result too large (overflow) | Free-format arithmetic overflow |
| RNX0105 | Invalid character in numeric conversion | `%dec`/`%int` on non-numeric |
| RNX0907 | Decimal data error | Blanks/garbage in packed or zoned field |
| SQL0204 | Object not found | SQL path / schema |
| SQL0913 | Row or object in use | Lock — check commitment control |
