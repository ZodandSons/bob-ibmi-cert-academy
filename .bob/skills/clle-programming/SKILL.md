---
name: clle-programming
description: Write and maintain ILE CL (CLLE) programs and command definitions with proper variable declarations, MONMSG error handling, structured loops, file processing, overrides and job submission. Use for any CL program, *CMD source, batch job stream or CL error-handling question.
---

# ILE CL (CLLE)

## Files
- `templates/program.pgm.clle` — standard program skeleton with global error handling
- `templates/command.cmd` — command definition matching the template program
- `reference/monmsg-patterns.md` — error handling patterns and common message IDs

## Workflow

<Steps>
<Step>
Copy `templates/program.pgm.clle` to `qcllesrc/<name>.pgm.clle` and fill in the header.
</Step>
<Step>
Declare every parameter and variable with `DCL` (explicit `TYPE` and `LEN`). Parameters
come first and must match the caller exactly — CL passes by reference, and a length
mismatch corrupts storage silently.
</Step>
<Step>
Keep the global `MONMSG` directly after the declarations. Add specific `MONMSG`s after
individual commands where a message is *expected* (e.g. `CPF9801` after `CHKOBJ`).
</Step>
<Step>
Use structured control flow: `IF/ELSE/DO/ENDDO`, `SELECT/WHEN/OTHERWISE/ENDSELECT`,
`DOWHILE`, `DOUNTIL`, `DOFOR`, `LEAVE`, `ITERATE`. Use subroutines (`SUBR`/`CALLSUBR`)
instead of `GOTO` for repeated logic. The only `GOTO` allowed is the jump to `ERROR`.
</Step>
<Step>
Clean up at both normal end and in `ERROR:` — `DLTOVR FILE(*ALL)`, delete `QTEMP`
work objects, release locks (`DLCOBJ`).
</Step>
<Step>
If users should call it as a command, create `qcllesrc/<name>.cmd` from
`templates/command.cmd` with `PROMPT` text and validity checks.
</Step>
</Steps>

## Reminders
- Numeric literals passed with `CALL ... PARM(5)` are `*DEC(15 5)`; character literals
  shorter than 32 bytes are padded to 32. Prefer `CALLPRC` or declared variables.
- `%SST`, `%TRIM`, `%CHECK`, `%SCAN`, `%DEC`, `%CHAR`, `%UPPER`, `%LEN` exist in CL (7.2+).
- `RTVJOBA`, `RTVSYSVAL`, `RTVDTAARA`, `RTVOBJD` retrieve values into variables.
- Use `SNDPGMMSG MSGTYPE(*COMP)` to report success to the caller and `*ESCAPE` to fail.
