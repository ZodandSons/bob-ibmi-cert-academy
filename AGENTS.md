# AGENTS.md — Order Management (IBM i)

This file gives Bob (and any other coding agent) the big picture of this repository.
Bob's rules in `.bob/rules/` hold the detailed standards; this file is the map.

## What this system is
Order management for a wholesale distributor running on IBM i 7.5.
Green-screen and batch programs written in RPG IV (mixed fixed and free format),
CL drivers, Db2 for i tables (DDS physical files being migrated to DDL),
and a growing set of Python utilities that run in PASE or on developer laptops.

## Repository layout
| Path | Contents |
|------|----------|
| `qrpglesrc/` | RPGLE / SQLRPGLE programs (`*.pgm.rpgle`, `*.pgm.sqlrpgle`) and modules |
| `qrpglesrc/legacy/` | Original fixed-format sources — **read-only reference, never edit** |
| `qcllesrc/` | CL programs (`*.pgm.clle`) and command sources (`*.cmd`) |
| `qprotosrc/` | Prototypes / copybooks (`*.rpgleinc`) |
| `qsrvsrc/` | Binder source (`*.bnd`) for service programs |
| `qddssrc/` | Legacy DDS (`*.pf`, `*.lf`, `*.dspf`, `*.prtf`) |
| `qsqlsrc/` | DDL (`*.table`, `*.view`, `*.index`, `*.sqlprc`) |
| `qtestsrc/` | RPGUnit tests (`t_*.rpgle`) |
| `python/` | Python utilities (Mapepire / ODBC) |
| `scripts/` | Bob Shell automation and CI scripts |

## Build
TOBi (The Object Builder for i, formerly Better Object Builder): `makei build` (whole project) or `makei c -f <file>` (one file).
Objects build into the developer's library `&DEVLIB` (set via `iproj.json` / `.env`).

## Environments
| Name | Library | Who may change it |
|------|---------|-------------------|
| DEV  | `ORDDEVxx` (per developer) | Developer + Bob |
| TEST | `ORDTST` | CI pipeline only |
| PROD | `ORDPRD`, `ORDDTA` | Change management only — **Bob never touches PROD** |

## Key business objects
- `CUSTMAST` customer master, key `CMCUST` (7,0)
- `ORDHDR` order header, key `OHCUST`, `OHORD`
- `ORDDTL` order lines, key `ODORD`, `ODLINE`
- `ITEMMAST` item master, key `IMITEM` (char 15)

## How to work here
1. Prefer the custom modes in `.bob/custom_modes.yaml` (RPG Developer, CL Developer,
   Fixed-to-Free Modernizer, IBM i Reviewer, IBM i Ops Analyst, Python Tools).
2. Skills in `.bob/skills/` load automatically when a task matches them.
3. Slash commands in `.bob/commands/` wrap the common workflows.
