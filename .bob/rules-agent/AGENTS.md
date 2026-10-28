# Agent mode context — IBM i order management

You are making real changes. Before editing:

- Work in small, reviewable steps: one program or one concern per change.
- Write converted or new sources to `qrpglesrc/`, `qcllesrc/`, `qsqlsrc/`; never `qrpglesrc/legacy/`.
- After every change: compile with `makei c -f <file>` and run related RPGUnit tests.
- Name files `<object>.<type>.<lang>` (see rules/01). The object name is max 10 characters.
- When a request touches more than three objects, stop and suggest Plan mode first.
- Report what you changed, how you verified it, and anything left for a human.
