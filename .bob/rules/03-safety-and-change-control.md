# Safety and change control (non-negotiable)

1. Never run, generate for execution, or suggest running a command that changes
   production libraries (`ORDPRD`, `ORDDTA`) or any library ending in `PRD`.
2. Never run destructive commands without explicit approval in the current conversation:
   `DLTLIB`, `CLRLIB`, `DLTF`, `CLRPFM`, `RMVM`, `DLTOBJ`, `DROP`, `DELETE` without
   `WHERE`, `TRUNCATE`, `rm -rf`. A PreToolUse hook also blocks these.
3. Never edit files in `qrpglesrc/legacy/`. Conversions write a new file and keep the
   original for side-by-side comparison.
4. Never print, log or commit credentials. Read them from environment variables or
   Bob secrets (`${KEY}` in `mcp.json`).
5. Behaviour-preserving changes (conversions, refactors) must not change business logic.
   If a fix is needed, list it separately as a recommendation — do not slip it in.
6. When unsure whether an action is reversible, stop and ask.
