---
name: ibmi-build
description: Build and compile IBM i objects from git stream-file source with TOBi, The Object Builder for i (formerly Better Object Builder; command makei) - iproj.json, .ibmi.json, Rules.mk dependencies, compiling one file or the whole project, and reading compile errors. Use when compiling, adding a new object to the build, or fixing build/compile failures.
---

# Building with TOBi (`makei`)

> Naming note: **TOBi (The Object Builder for i)** was called *Better Object Builder*, or
> "Bob", until 2025, when IBM renamed it to avoid confusion with IBM Bob, the AI assistant.
> Older articles still say "Bob" or `yum install bob`. The command is still `makei`.
> Install on IBM i with `yum install tobi`. Docs: https://ibm.github.io/ibmi-tobi/

## Files
| Template | Goes to | Purpose |
|----------|---------|---------|
| `templates/iproj.json` | repo root | Project definition: object library, library list, build commands |
| `templates/.ibmi.json` | repo root or any source folder | Per-folder target CCSID / object library overrides |
| `templates/Rules.mk` | each source folder | Which objects to build from which source, and dependencies |
| `templates/Rules.root.mk` | repo root (as `Rules.mk`) | Lists the source folders in build order |
| `templates/ordbnddir.bnddir` | a source folder | CL *pseudo-source* that creates a binding directory (`&O` = object library, `&N` = object name) |

## Commands
| Task | Command |
|------|---------|
| Build everything that changed | `makei build` |
| Compile one source file | `makei compile -f qrpglesrc/custinq.pgm.rpgle` (short: `makei c -f …`) |
| Build one target and its dependencies | `makei build -t CUSTINQ.PGM` |
| Create the project files | `makei init` |
| See all options | `makei --help` |

Run `makei` **on IBM i** (PASE, via SSH) or let VS Code *Code for IBM i* / IBM Bob run it
through the deploy-and-build action. The target object library comes from `&DEVLIB`
(set in `.env` or the environment: `export DEVLIB=ORDDEV01`).

## Adding a new object to the build

<Steps>
<Step>
Name the source with the object name and type: `custinq.pgm.rpgle` → `CUSTINQ.PGM`,
`ordsrv.sqlrpgle` → `ORDSRV.MODULE`, `ordsrv.bnd` → binder source for `ORDSRV.SRVPGM`.
</Step>
<Step>
Add a target line to the folder's `Rules.mk` listing the source and every object it
depends on (files it opens, service programs it binds to, copybooks are tracked automatically):
`CUSTINQ.PGM: custinq.pgm.rpgle CUSTMAST.FILE ORDHDR.FILE ORDSRV.SRVPGM`
</Step>
<Step>
For a service program add both the module and the service program targets, and add the
service program to the binding directory target (see `templates/Rules.mk`).
</Step>
<Step>
Build. If the compile fails, read the listing: `.logs/` holds the joblog and spool,
`.evfevent/` holds machine-readable errors (one file per source). Fix the source, rebuild.
</Step>
</Steps>

## Reading compile errors
- RPG: `RNF` messages. Severity 30+ stops the compile. `RNF7030` undefined name,
  `RNF7503` expression type mismatch, `RNF5410` unbalanced block, `RNF0637` not in
  free-format, `RNS9308` compilation stopped (look above it for the real error).
- CL: `CPD` messages, e.g. `CPD0712` undeclared variable, `CPD0791` no labels for GOTO.
- SQL precompile: `SQL` messages, e.g. `SQL0312` host variable not declared.
- Level checks at runtime (`CPF4131`) mean a dependency is missing from `Rules.mk`.
