---
name: sqlrpgle-db2
description: Embedded SQL in RPG (SQLRPGLE) and Db2 for i - SET OPTION, host variables, cursors, multi-row FETCH, SQLSTATE error handling, commitment control, DDL instead of DDS, and IBM i SQL services (QSYS2). Use when writing or reviewing SQL in RPG, converting native I/O to SQL, or writing DDL for Db2 for i.
---

# SQLRPGLE and Db2 for i

Patterns are in `reference/sql-patterns.md`. Apply these rules every time:

<Steps>
<Step>
**Start every SQLRPGLE source with `SET OPTION`** before any other SQL statement:
`exec sql SET OPTION COMMIT = *NONE, NAMING = *SYS, CLOSQLCSR = *ENDMOD, DATFMT = *ISO;`
Choose `COMMIT = *CHG` when the program updates several tables that must stay consistent.
</Step>
<Step>
**Check `SQLSTATE` after every statement.** `'00000'` = success, `'02000'` = no row,
class `'01'` = warning (still check data), anything else = error. Use the
`checkSql()` helper pattern from the reference file so handling is uniform.
</Step>
<Step>
**Use host variables or parameter markers, never string concatenation** for values.
Dynamic SQL (`PREPARE` / `EXECUTE`) is only for variable table/column names — validate
those against a list before use.
</Step>
<Step>
**Fetch in blocks** for anything more than a handful of rows:
`FETCH NEXT FROM c1 FOR :max ROWS INTO :rows` with a DS array, then
`GET DIAGNOSTICS :fetched = ROW_COUNT`.
</Step>
<Step>
**Close cursors** in every path, including error paths.
</Step>
<Step>
**New tables are DDL**, not DDS: source in `qsqlsrc/<name>.table`, with a short system
name (`FOR SYSTEM NAME`), `LABEL ON` text, and a primary key.
</Step>
</Steps>

## IBM i services worth knowing
`QSYS2.OBJECT_STATISTICS`, `QSYS2.PROGRAM_REFERENCES`, `QSYS2.SYSCOLUMNS`,
`QSYS2.ACTIVE_JOB_INFO`, `QSYS2.JOBLOG_INFO`, `QSYS2.QCMDEXC` (run CL from SQL),
`QSYS2.IFS_READ` / `IFS_WRITE`, `SYSTOOLS.HTTPGETCLOB` / `QSYS2.HTTP_GET`,
`JSON_TABLE`, `JSON_OBJECT`, `JSON_ARRAYAGG`.
