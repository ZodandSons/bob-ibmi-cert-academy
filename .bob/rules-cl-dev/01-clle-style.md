# CL Developer mode — style rules

- Use CLLE (ILE CL), never OPM CLP, for new programs.
- Declare every variable with `DCL` and an explicit `TYPE` and `LEN`; use `*INT`/`*UINT`
  for counters, `STG(*DEFINED)` for overlays.
- Global `MONMSG MSGID(CPF0000 MCH0000) EXEC(GOTO CMDLBL(ERROR))` right after the
  declarations; specific `MONMSG` directly after commands where the error is expected.
- Use `DOWHILE`/`DOUNTIL`/`DOFOR`/`SELECT` instead of `GOTO` loops.
- Use `RCVF`/`DCLF` with `OPNID` when reading more than one file.
- Clean up in `ERROR:` and at normal end: `DLTOVR`, close files, remove temporary
  objects from `QTEMP`.
- Command keywords in full form (`CHKOBJ OBJ(&LIB/&OBJ) OBJTYPE(*FILE)`), not positional.
