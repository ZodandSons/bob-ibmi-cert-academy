# Rules.mk for qrpglesrc/ — read by TOBi (makei). One line per object:
#   TARGET.TYPE: source-file dependency dependency ...
# Docs: https://ibm.github.io/ibmi-tobi/  (Prepare the project -> Rules.mk)
# Object types: .PGM .MODULE .SRVPGM .FILE .BNDDIR .CMD .DTAARA ...

# Programs
CUSTINQ.PGM: custinq.pgm.rpgle CUSTMAST.FILE ORDHDR.FILE
ORDENTRY.PGM: ordentry.pgm.sqlrpgle ORDENTRYD.FILE ORDHDR.FILE ORDDTL.FILE ORDBNDDIR.BNDDIR

# Service program: module(s) + binder source (in qsrvsrc/) + binding directory
ORDSRV.MODULE: ordsrv.sqlrpgle CUSTMAST.FILE ORDHDR.FILE
ORDSRV.SRVPGM: ordsrv.bnd ORDSRV.MODULE
ORDBNDDIR.BNDDIR: ordbnddir.bnddir ORDSRV.SRVPGM   # CL pseudo-source: see templates/ordbnddir.bnddir

# Per-target compile option overrides
CUSTINQ.PGM: private DBGVIEW := *SOURCE
ORDENTRY.PGM: private TGTRLS := V7R4M0
