# Plan mode — how to plan IBM i changes

Every plan for an IBM i change must include these sections:

1. **Objects affected** — each program, service program, file and command, with its
   source path. Use the `where_used` MCP tool (if available) to list callers.
2. **Build order** — files before programs, modules before service programs,
   service programs before the programs that bind to them.
3. **Signature impact** — if a service program's exports change, say whether the
   binder source needs a new `*CURRENT` signature (see the `rpgle-free-format` skill).
4. **Data impact** — file layout changes mean recompiling every program that uses
   the file (level checks, CPF4131). List them.
5. **Test plan** — which RPGUnit tests to add or run, and any manual checks.
6. **Rollback** — how to restore the previous objects if the change fails.

Keep plans in `plans/<ticket-or-topic>.md`.
