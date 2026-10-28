---
description: Scaffold a new CLLE program with standard error handling
argument-hint: <PROGRAM-NAME> <what it should do>
---
Create a new CLLE program named `$1`. Purpose: $2

- Start from `.bob/skills/clle-programming/templates/program.pgm.clle`.
- Save as `qcllesrc/<lowercase $1>.pgm.clle`.
- Keep the global `MONMSG` and the `ERROR:` routine from the template.
- If the program submits work, use `SBMJOB` with an explicit `JOBD` and `JOBQ` and log
  the submitted job name with `SNDPGMMSG`.
- If it should be callable as a command, also create `qcllesrc/<lowercase $1>.cmd`.
