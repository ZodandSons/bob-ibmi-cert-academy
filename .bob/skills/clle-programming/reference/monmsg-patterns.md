# MONMSG patterns

## 1. Expected message → handle and continue
```cl
CHKOBJ     OBJ(&LIB/&FILE) OBJTYPE(*FILE)
MONMSG     MSGID(CPF9801) EXEC(DO)
   CRTPF      FILE(&LIB/&FILE) RCDLEN(132)
ENDDO
```

## 2. Ignore a harmless message
```cl
DLTF       FILE(QTEMP/WORKFILE)
MONMSG     MSGID(CPF2105)          /* object not found - fine */
```

## 3. End-of-file on RCVF
```cl
DOWHILE    COND('1')
   RCVF
   MONMSG     MSGID(CPF0864) EXEC(LEAVE)
   /* process record */
ENDDO
```

## 4. Global handler (always present)
Right after the last `DCL`/`DCLF`:
```cl
MONMSG     MSGID(CPF0000 MCH0000) EXEC(GOTO CMDLBL(ERROR))
```
The `ERROR:` routine in the template resends the escape so the caller sees the real
cause instead of a generic CPF9999.

## 5. Object locks
```cl
ALCOBJ     OBJ((&LIB/&FILE *FILE *EXCL)) WAIT(30)
MONMSG     MSGID(CPF1002) EXEC(DO)
   SNDPGMMSG  MSGID(CPF9898) MSGF(QCPFMSG) +
                MSGDTA('File in use - try again later') MSGTYPE(*ESCAPE)
ENDDO
/* ... */
DLCOBJ     OBJ((&LIB/&FILE *FILE *EXCL))
```

## Common message IDs in CL
| ID | Meaning |
|----|---------|
| CPF0864 | End of file (RCVF) |
| CPF1002 | Cannot allocate object |
| CPF2103 | Library already in library list (ADDLIBLE) |
| CPF2104 | Library not in library list (RMVLIBLE) |
| CPF2105 | Object not found (DLTx) |
| CPF2110 | Library not found |
| CPF3141 | Member not found |
| CPF5813 | File already exists (CRTPF) |
| CPF7302 | File not created |
| CPF9801 | Object not found (CHKOBJ) |
| CPF9802 | Not authorized (CHKOBJ) |
| CPF9898 | General escape from QCPFMSG with your own text |
| CPF9897 | General informational/completion from QCPFMSG |
| MCH1210 | Receiver value too small (numeric overflow) |
