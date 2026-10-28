---
description: Repo-wide impact analysis of a file or program using parallel subagents
argument-hint: <OBJECT>
---
Find everything in this repository that depends on `$1`, without filling this
conversation with every file you read.

1. Spawn three **general** subagents in parallel, one per area. (General, not explore:
   explore subagents are read-only and cannot write the result files.)
   - `qrpglesrc/` and `qprotosrc/`: RPG programs, modules and copybooks referencing `$1`
   - `qcllesrc/`: CL programs and commands referencing `$1`
   - `qsqlsrc/` and `qddssrc/`: files, views, indexes and logical files over `$1`

   Each subagent must only read source and write ONE file,
   `tmp/impact/$1-<area>.md`, containing a table (source file, line, how it uses `$1`).
   It returns only a 3-line summary to this conversation.
2. If the `ibmi-mcp` server is available, call `where_used` for `$1` to add compiled
   objects that are not in git.
3. Read the three result files and merge them into one table, highlighting programs
   that **update** `$1`.
4. Finish with: number of affected objects, highest-risk items, and suggested test order.
