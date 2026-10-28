     H*****************************************************************
     H* CUSTINQ  - Customer order total inquiry
     H* Written  - 1998-03-14 JRS
     H* Changed  - 2004-07-02 MKW Added order count
     H*****************************************************************
     H DFTACTGRP(*NO) ACTGRP(*CALLER) OPTION(*SRCSTMT:*NODEBUGIO)
     FCUSTMAST  IF   E           K DISK
     FORDHDR    IF   E           K DISK
     D wCustNo         S              7P 0
     D wTotal          S             11P 2
     D wCount          S              5S 0
     D wMsg            S             30
     C*
     C* Parameters
     C     *ENTRY        PLIST
     C                   PARM                    pCustNo           7
     C                   PARM                    pResult          30
     C                   PARM                    pTotal           11 2
     C*
     C                   MOVE      pCustNo       wCustNo
     C     wCustNo       CHAIN     CUSTMAST                           90
     C     *IN90         IFEQ      *ON
     C                   MOVEL     'NOT FOUND'   pResult
     C                   Z-ADD     0             pTotal
     C                   GOTO      EXIT
     C                   ENDIF
     C*
     C                   Z-ADD     0             wTotal
     C                   Z-ADD     0             wCount
     C     wCustNo       SETLL     ORDHDR
     C     wCustNo       READE     ORDHDR                                 91
     C     *IN91         DOWEQ     *OFF
     C                   ADD       OHAMT         wTotal
     C                   ADD       1             wCount
     C     wCustNo       READE     ORDHDR                                 91
     C                   ENDDO
     C                   EXSR      FMTRES
     C                   Z-ADD     wTotal        pTotal
     C*
     C     EXIT          TAG
     C                   SETON                                        LR
     C                   RETURN
     C*****************************************************************
     C* FMTRES - Build result text: name + order count
     C*****************************************************************
     C     FMTRES        BEGSR
     C                   MOVEL(P)  CMNAME        wMsg
     C     wCount        IFGT      0
     C                   MOVE      '*'           wMsg
     C                   ENDIF
     C                   MOVEL(P)  wMsg          pResult
     C                   ENDSR
