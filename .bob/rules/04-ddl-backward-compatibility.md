# Database change compatibility — applies ONLY to `qsqlsrc/` and `qddssrc/`

Scope: these rules apply when creating or changing files under `qsqlsrc/` (DDL) or
`qddssrc/` (DDS). Ignore them for every other folder.

- Changes must be backward compatible: add columns, never remove, rename or retype one.
- New columns need a `DEFAULT` (or `NOT NULL WITH DEFAULT`) so existing programs keep working.
- Never change a key or the record format name of a file used by existing programs.
- List every program that uses the file (MCP `where_used`) in the change description.
