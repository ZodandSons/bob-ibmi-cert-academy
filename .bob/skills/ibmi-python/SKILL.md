---
name: ibmi-python
description: Write Python that connects to IBM i - Db2 for i queries with mapepire-python or pyodbc, running CL commands through QSYS2.QCMDEXC, downloading source members, object and where-used lookups, and Python running in IBM i PASE. Use for any Python script, CLI or automation that talks to IBM i.
---

# Python for IBM i

## Ready-made tool
`scripts/ibmi_tool.py` is a working CLI (standard library + one backend). Use it directly
for quick lookups, or copy its patterns into new scripts:

```bash
pip install -r .bob/skills/ibmi-python/scripts/requirements.txt
set -a; . ./.env; set +a                                 # DB2i_HOST / DB2i_USER / DB2i_PASS
python3 .bob/skills/ibmi-python/scripts/ibmi_tool.py objects ORDDEV01 --type "*PGM"
python3 .bob/skills/ibmi-python/scripts/ibmi_tool.py where-used ORDDEV01 CUSTMAST --format json
python3 .bob/skills/ibmi-python/scripts/ibmi_tool.py source ORDDEV01 QRPGLESRC CUSTINQ \
        -o qrpglesrc/legacy/custinq.pgm.rpgle
python3 .bob/skills/ibmi-python/scripts/ibmi_tool.py query "SELECT ..." --dry-run
```

## Choosing a connection method
| Method | Runs where | Install | Notes |
|--------|-----------|---------|-------|
| `mapepire-python` | Anywhere | `pip install mapepire-python` | Needs Mapepire server on IBM i (port 8076). Preferred. |
| `pyodbc` | Anywhere | `pip install pyodbc` + IBM i Access ODBC driver | Mature, fast; driver install required |
| `ibm_db` in PASE | On IBM i | `yum install python3-ibm_db` | Local, no network credentials |
| `itoolkit` | On IBM i / remote | `pip install itoolkit` | Call programs, CL, APIs via XMLSERVICE |

## Rules for new scripts

<Steps>
<Step>
Credentials from environment variables only (`DB2i_HOST`, `DB2i_USER`, `DB2i_PASS`).
Never accept a password as a command-line argument — it lands in shell history and `ps`.
</Step>
<Step>
Parameter markers (`?`) for every value. Object and library names cannot be parameters,
so validate them with the `ibmi_name()` pattern (`^[A-Z$#@][A-Z0-9$#@_]{0,9}$`) first.
</Step>
<Step>
Use one connection per run and close it in `finally`. `QTEMP` objects (aliases, work
files) only exist for the life of that connection.
</Step>
<Step>
Make scripts safe by default: read-only unless a flag says otherwise, a `--dry-run`
that prints SQL, and refusal of destructive CL (see `BLOCKED_CL` in the tool).
</Step>
<Step>
Output formats: human table by default, `--format json` for Bob Shell / CI pipelines.
</Step>
</Steps>

## Handy SQL for scripts
- Run CL: `CALL QSYS2.QCMDEXC(?)`
- Read a source member: `CREATE ALIAS QTEMP.X FOR LIB.FILE (MBR)` then `SELECT SRCDTA ... ORDER BY SRCSEQ`
- IFS file content: `SELECT LINE FROM TABLE(QSYS2.IFS_READ(PATH_NAME => ?))`
- Spool file text: `SELECT SPOOLED_DATA FROM TABLE(SYSTOOLS.SPOOLED_FILE_DATA(JOB_NAME => ?, SPOOLED_FILE_NAME => ?))`
