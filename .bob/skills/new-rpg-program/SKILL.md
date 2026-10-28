---
name: new-rpg-program
description: Scaffold a new free-format RPGLE program from the shop template
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <PROGRAM-NAME> <what it should do>
---

Create a new free-format RPGLE program named `$1`. Purpose: $2

- Start from `.bob/skills/rpgle-free-format/templates/program.pgm.rpgle`.
- Save as `qrpglesrc/<lowercase $1>.pgm.rpgle` (use `.pgm.sqlrpgle` if it needs SQL).
- Object name must be 10 characters or fewer; ask me if `$1` is longer.
- Fill in the header, parameters (`dcl-pi`), and the mainline. Put reusable logic in
  procedures, and add prototypes to `qprotosrc/` if they will be shared.
- Add a `Rules.mk` dependency line for the new program (see the `ibmi-build` skill).
- Add a starter RPGUnit test in `qtestsrc/` for any exported procedure.
