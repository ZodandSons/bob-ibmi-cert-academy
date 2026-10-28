---
name: where-used
description: Impact analysis — find every program that uses a file or program
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: '<OBJECT> [LIBRARY]'
---

Find everything that uses `$1` (library: `$2`, default to the build library from the
session context).

1. Call the `where_used` tool from the `ibmi-mcp` server for the object and library.
2. Also search the repository source (`qrpglesrc/`, `qcllesrc/`, `qsqlsrc/`) for `$1`
   so uncompiled or new sources are included.
3. Present one table: program, source file in repo (if any), usage (I/O/U), language.
4. Highlight programs that **update** the object and anything that is not in git.

If the MCP server is unavailable, say so and give the source-search results only.
