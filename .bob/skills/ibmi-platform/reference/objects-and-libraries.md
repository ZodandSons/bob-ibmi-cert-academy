# Objects, libraries and the library list

## Common object types
| Type | What it is | Created by |
|------|-----------|------------|
| `*PGM` | Program (OPM or ILE) | `CRTBNDRPG`, `CRTBNDCL`, `CRTPGM`, `CRTSQLRPGI OBJTYPE(*PGM)` |
| `*MODULE` | Compiled module, bound into programs | `CRTRPGMOD`, `CRTCLMOD`, `CRTSQLRPGI OBJTYPE(*MODULE)` |
| `*SRVPGM` | Service program (shared procedures) | `CRTSRVPGM` + binder source |
| `*BNDDIR` | Binding directory | `CRTBNDDIR`, `ADDBNDDIRE` |
| `*FILE` | PF / LF / table / view / index / DSPF / PRTF / SAVF | DDS (`CRTPF`) or SQL DDL |
| `*CMD` | Command | `CRTCMD` |
| `*DTAARA` | Data area | `CRTDTAARA` |
| `*DTAQ` | Data queue | `CRTDTAQ` |
| `*JOBD` | Job description (initial library list, job queue) | `CRTJOBD` |
| `*MSGF` | Message file | `CRTMSGF`, `ADDMSGD` |
| `*USRSPC` | User space | `QUSCRTUS` API |

## QSYS.LIB vs IFS
- Libraries are `/QSYS.LIB/NAME.LIB`; members are `/QSYS.LIB/LIB.LIB/FILE.FILE/MBR.MBR`.
- Modern projects keep source in git as IFS stream files and compile with `SRCSTMF`.
- SQL names (`MYLIB.MYTABLE`) vs system naming (`MYLIB/MYTABLE`) — set by the `NAMING`
  connection or `CRTSQLRPGI OPTION(*SYS|*SQL)` / `SET OPTION NAMING = *SYS`.

## Library list resolution order
1. System portion (`QSYSLIBL`) — `QSYS`, `QSYS2`, `QHLPSYS`, `QUSRSYS`
2. Product libraries (added by commands like `CRTSQLRPGI`)
3. Current library (`*CURLIB`) — where unqualified objects are **created**
4. User portion (`QUSRLIBL` or the job description's `INLLIBL`)

Change it with `ADDLIBLE`, `RMVLIBLE`, `CHGLIBL`, `CHGCURLIB`, or SQL
`SET PATH` / `SET SCHEMA` for SQL resolution.

## Useful SQL services for objects
```sql
SELECT * FROM TABLE(QSYS2.OBJECT_STATISTICS('ORDDEV01', '*PGM *SRVPGM'));
SELECT * FROM QSYS2.LIBRARY_LIST_INFO;
SELECT * FROM QSYS2.PROGRAM_REFERENCES WHERE PROGRAM_LIBRARY = 'ORDDEV01';
SELECT * FROM QSYS2.SYSPROGRAMSTAT WHERE PROGRAM_SCHEMA = 'ORDDEV01';
```
