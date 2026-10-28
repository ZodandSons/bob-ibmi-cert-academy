---
name: rpgunit-testing
description: Write and run RPGUnit (iRPGUnit) unit tests for RPG procedures and service programs - test program structure, setUp/tearDown, assertions, building with RUCRTRPG and running with RUCALLTST. Use when adding tests for RPG code, after creating an exported procedure, or to prove a fixed-to-free conversion did not change behaviour.
---

# RPGUnit (iRPGUnit) tests

Template: `templates/t_ordsrv.rpgle`. Tests live in `qtestsrc/t_<object>.rpgle`.

## How RPGUnit works
- A test is a `*SRVPGM` whose exported procedures named `test...` are run by `RUCALLTST`.
- Optional exported procedures `setUpSuite`, `setUp`, `tearDown`, `tearDownSuite` run
  around the tests.
- Assertions come from the `TESTCASE` copybook: `assert(cond : msg)`, `aEqual(exp : act)`
  (alphanumeric), `iEqual(exp : act)` (integer), `nEqual` (boolean), `fail(msg)`.

## Workflow

<Steps>
<Step>
Copy the template to `qtestsrc/t_<object>.rpgle` and `/copy` the prototypes of the
code under test.
</Step>
<Step>
Write one `test...` procedure per behaviour: happy path, not found, boundary values,
invalid input. Name them so a failure reads like a sentence:
`test_getName_returnsBlankWhenNotFound`.
</Step>
<Step>
Make tests independent of production data: insert rows in `setUp` into a test library
and delete them in `tearDown`, or use `QTEMP` copies of files.
</Step>
<Step>
Build and run (on IBM i):
```
RUCRTRPG TSTPGM(ORDDEV01/T_ORDSRV) SRCSTMF('qtestsrc/t_ordsrv.rpgle') +
         BNDSRVPGM(ORDDEV01/ORDSRV)
RUCALLTST TSTPGM(ORDDEV01/T_ORDSRV) DETAIL(*ALL)
```
Check RUCRTRPG/RUCALLTST parameters for your installed RPGUnit version (`F4` prompt);
older versions take `SRCFILE`/`SRCMBR` instead of `SRCSTMF`.
</Step>
<Step>
For conversions: write characterization tests against the **original** program first,
then run the same tests against the converted program — identical results prove the
conversion preserved behaviour.
</Step>
</Steps>
