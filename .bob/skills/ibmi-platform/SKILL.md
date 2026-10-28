---
name: ibmi-platform
description: IBM i platform fundamentals - objects, libraries, the library list, jobs, subsystems, activation groups, CCSIDs, messages and authority. Use when a task needs IBM i system knowledge, when explaining IBM i behaviour, or when diagnosing runtime errors such as CPF/MCH/RNX/SQL messages.
---

# IBM i platform essentials

Use this skill as background knowledge whenever code behaviour depends on the operating
system rather than the language. Load the reference files for detail:

- `reference/objects-and-libraries.md` — object types, naming, QSYS.LIB vs IFS, library list
- `reference/jobs-and-messages.md` — jobs, subsystems, activation groups, message handling,
  common message IDs and what they mean

## Key rules to apply

1. **Everything is an object** with a type (`*PGM`, `*FILE`, `*DTAARA` …) living in a library.
   Names are max 10 characters, uppercase, and must start with A–Z, `$`, `#` or `@`.
2. **The library list decides which object runs.** Unqualified references resolve through
   `*LIBL` (system portion → product → current library → user portion). Never hard-code a
   library to "fix" a not-found error — fix the job description or `ADDLIBLE` instead.
3. **Activation groups scope resources.** `*NEW` = fresh each call (slow, isolated),
   named = shared and persistent, `*CALLER` = joins the caller. Overrides, open files and
   commitment control follow the activation group.
4. **Escape messages end programs.** CL must `MONMSG`; RPG must `monitor` or use `(e)`.
   Unhandled errors in batch become inquiry messages that hang the job (`QSYSOPR`).
5. **CCSID matters** for IFS files and SQL: stream files are often 1208 (UTF-8) while
   source and data are 37/273/500 etc. Specify `CCSID` when creating IFS files.
6. **Authority**: programs run under the user profile unless compiled with
   `USRPRF(*OWNER)` (adopted authority). Flag any adoption as a review item.

## Diagnosing a failure
1. Get the job log: `DSPJOBLOG` or SQL `QSYS2.JOBLOG_INFO('job/user/name')`
   (MCP tool `recent_job_messages`).
2. Find the first escape (`*ESCAPE`) or diagnostic message — later messages are often
   consequences.
3. Look up the message ID with `DSPMSGD RANGE(CPF9801) MSGF(QCPFMSG)` or the table in
   `reference/jobs-and-messages.md`.
