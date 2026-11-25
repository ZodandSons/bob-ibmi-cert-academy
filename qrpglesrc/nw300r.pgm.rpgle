**free
// *****************************************************************
// *  PROGRAM  : NW300R
// *  TITLE    : SUPPLIER MASTER FILE MAINTENANCE
// *  AUTHOR   : B. J. THOMAS                     DATE: 05/20/96
// *             (COPIED FROM NW100R CUSTOMER MAINTENANCE)
// *
// *  MODIFICATION LOG
// *  05/20/96 BJT         NEW - SCREEN FIELDS NOW REFERENCE SUPMST SO
// *                       NO MORE MOVE STATEMENTS NEEDED
// *  04/10/03 TPK  TPK03  CONVERTED TO RPG IV
// *  2026-11-02 BOB        CONVERTED TO FULLY FREE FORMAT
// *
// *  INDICATORS - SAME AS NW100R
// *  *IN03  = F3 (exit)
// *  *IN06  = F6 (add)
// *  *IN12  = F12 (cancel)
// *  *IN31  = SFLNXTCHG / subfile has records (display subfile)
// *  *IN32  = SFLDSPCTL
// *  *IN33  = SFLCLR
// *  *IN34  = SFLDSP
// *  *IN40  = protect all input fields
// *  *IN41  = protect supplier number field
// *  *IN50  = edit error on detail screen
// *  *IN51  = SMNAME blank error
// *  *IN53  = SMCNTY blank error
// *  *IN54  = SMPHON invalid character error
// *  *IN57  = SMFAX invalid character error (removed 1997)
// *  *IN90  = general no-record / EOF indicator
// *  *IN91  = READC no changed records
// *  *IN92  = CHAIN not found
// *****************************************************************
ctl-opt datedit(*mdy) option(*srcstmt:*nodebugio) dftactgrp(*no);

// ---- Files -------------------------------------------------------
dcl-f NW300D    workstn sfile(SFLREC:RRN) indds(wkInds);
dcl-f SUPMST    usage(*update:*delete:*output) keyed;
dcl-f SUPMSTL1  usage(*input) keyed rename(SUPMSTR:SUPMST1);

// ---- Standalone variables ----------------------------------------
dcl-s MSG       char(50)  dim(8) ctdata perrcd(1);
dcl-c VALID     '0123456789()-. ';
dcl-s WSUP      like(SMSUP#);
dcl-s RRN       packed(4:0);
dcl-s SVPOS     like(C1POS);
dcl-s POSKEY    char(40);
dcl-s POS       packed(3:0);

// ---- Indicator data structure (maps *INxx to named fields) -------
dcl-ds wkInds   len(99);
  in03          ind   pos(3);   // F3 exit
  in06          ind   pos(6);   // F6 add
  in12          ind   pos(12);  // F12 cancel
  in31          ind   pos(31);  // SFLNXTCHG
  in32          ind   pos(32);  // SFLDSPCTL
  in33          ind   pos(33);  // SFLCLR
  in34          ind   pos(34);  // SFLDSP
  in40          ind   pos(40);  // protect all
  in41          ind   pos(41);  // protect supplier#
  in50          ind   pos(50);  // edit error
  in51          ind   pos(51);  // SMNAME blank
  in53          ind   pos(53);  // SMCNTY blank
  in54          ind   pos(54);  // SMPHON invalid char
  in57          ind   pos(57);  // SMFAX invalid (unused since 1997)
  in90          ind   pos(90);
  in91          ind   pos(91);
  in92          ind   pos(92);
end-ds;

// ---- Prototype forward declarations for local subprocedures ------
dcl-pr LODSFL end-pr;
dcl-pr PRCOPT end-pr;
dcl-pr CHGREC end-pr;
dcl-pr ADDREC end-pr;
dcl-pr DLTSUP end-pr;
dcl-pr DSPREC end-pr;
dcl-pr EDTCHK end-pr;
dcl-pr OLDCHK end-pr;

// ---- Mainline ----------------------------------------------------
LODSFL();

dow *on;
  write FMT01;
  // CONV: MOVE *BLANKS MSGLIN — MSGLIN is a char field; = *blanks clears fully (P behaviour ok)
  MSGLIN = *blanks;
  exfmt SFLCTL;

  if in03 or in12;
    leave;
  endif;

  if in06;
    ADDREC();
    LODSFL();
    iter;
  endif;

  if C1POS <> SVPOS;
    LODSFL();
    iter;
  endif;

  PRCOPT();
  LODSFL();
enddo;

*inlr = *on;
return;

// *****************************************************************
// *  LODSFL - LOAD SUBFILE
// *****************************************************************
dcl-proc LODSFL;
  dcl-pi *n end-pi;

  in33 = *on;
  write SFLCTL;
  in31 = *off;
  in32 = *off;
  in33 = *off;
  RRN  = 0;
  // CONV: MOVE C1POS SVPOS — same type/length; full assignment ok (target fully overwritten)
  SVPOS = C1POS;
  // CONV: MOVE *BLANKS POSKEY — full clear, then MOVEL C1POS POSKEY (left-aligned partial fill)
  POSKEY = *blanks;
  // CONV: MOVEL C1POS POSKEY without (P) — only bytes 1..%len(C1POS) are set; rest stays blank
  %subst(POSKEY:1:%len(C1POS)) = C1POS;
  setll POSKEY SUPMST1;
  read SUPMST1;

  dow not %eof(SUPMSTL1);
    RRN += 1;
    // CONV: MOVE *BLANK S1OPT — single-char field, full assignment ok
    S1OPT = *blank;
    S1SUP = SMSUP#;
    // CONV: MOVEL SMNAME S1NAME without (P) — both are likely same length (externally described);
    //        if lengths differ, only bytes 1..%len(SMNAME) are written; rest stays.
    %subst(S1NAME:1:%len(SMNAME)) = SMNAME;
    // CONV: MOVEL SMCITY S1CITY without (P) — same reasoning
    %subst(S1CITY:1:%len(SMCITY)) = SMCITY;
    // CONV: MOVEL SMCNTY S1CNTY without (P) — same reasoning
    %subst(S1CNTY:1:%len(SMCNTY)) = SMCNTY;
    write SFLREC;
    if RRN = 500;
      leave;   // CONV: CABEQ 500 LODEND → leave (exit inner loop)
    endif;
    read SUPMST1;
  enddo;

  // LODEND:
  in32 = *on;
  if RRN > 0;
    in31 = *on;
  else;
    // CONV: MOVEL MSG(6) MSGLIN without (P) — if MSGLIN >= MSG element length, bytes beyond are
    //        unchanged. MSG elements are 50 chars and MSGLIN is also 50; full overwrite ok.
    MSGLIN = MSG(6);
  endif;
  in34 = *on;
end-proc;

// *****************************************************************
// *  PRCOPT - PROCESS OPTIONS
// *****************************************************************
dcl-proc PRCOPT;
  dcl-pi *n end-pi;

  readc SFLREC;

  dow not %eof(NW300D);
    WSUP = S1SUP;
    // CONV: CASxx → select/when
    select;
      when S1OPT = '2';
        CHGREC();
      when S1OPT = '4';
        DLTSUP();
      when S1OPT = '5';
        DSPREC();
    endsl;
    readc SFLREC;
  enddo;
end-proc;

// *****************************************************************
// *  CHGREC - CHANGE (FILE FIELDS ARE THE SCREEN FIELDS)
// *****************************************************************
dcl-proc CHGREC;
  dcl-pi *n end-pi;

  chain WSUP SUPMSTR;
  if not %found(SUPMST);
    // CONV: MOVEL MSG(1) MSGLIN — see LODSFL note; same lengths, full assignment ok
    MSGLIN = MSG(1);
  else;
    // CONV: MOVEL 'CHANGE' D1MODE — D1MODE is char; if D1MODE > 6 bytes, remaining bytes
    //        are NOT cleared (no P). Assign with %subst to preserve original behaviour.
    %subst(D1MODE:1:6) = 'CHANGE';
    in40 = *off;
    in41 = *on;
    // CONV: CHG1 TAG + CABEQ *IN50 CHG1 → dou not in50 (repeat until no edit errors)
    // CONV: GOTO CHGX on F3/F12 → leave
    dou not in50;
      exfmt DTLREC;
      if in12 or in03;
        leave;
      endif;
      EDTCHK();
    enddo;
    if not in12 and not in03;
      update SUPMSTR;
      // CONV: MOVEL MSG(2) MSGLIN — full assignment ok (see LODSFL note)
      MSGLIN = MSG(2);
    endif;
  endif;
end-proc;

// *****************************************************************
// *  ADDREC - ADD (NEXT NUMBER LOGIC COPIED FROM NW200R)
// *****************************************************************
dcl-proc ADDREC;
  dcl-pi *n end-pi;

  // CONV: MOVEL 'ADD' D1MODE — see CHGREC note; assign with %subst
  %subst(D1MODE:1:3) = 'ADD';
  in40 = *off;
  in41 = *off;
  setgt *hival SUPMSTR;
  readp SUPMSTR;
  WSUP = 1;
  if not %eof(SUPMST);
    WSUP = SMSUP# + 1;
  endif;
  clear SUPMSTR;
  SMSUP# = WSUP;
  // CONV: ADD1 TAG + CABEQ *IN50 ADD1 → dou not in50
  // CONV: GOTO ADDX on F3/F12 → leave
  dou not in50;
    exfmt DTLREC;
    if in12 or in03;
      leave;
    endif;
    EDTCHK();
  enddo;
  if not in12 and not in03;
    // CONV: MOVE *BLANK SMSTAT — SMSTAT is likely char(1); full assignment ok
    SMSTAT = *blank;
    write SUPMSTR;
    // CONV: MOVEL MSG(3) MSGLIN — full assignment ok (see LODSFL note)
    MSGLIN = MSG(3);
  endif;
end-proc;

// *****************************************************************
// *  DLTSUP - DELETE (PHYSICAL - PRODUCTS ARE NOT CHECKED)
// *****************************************************************
dcl-proc DLTSUP;
  dcl-pi *n end-pi;

  chain WSUP SUPMSTR;
  if not %found(SUPMST);
    // CONV: MOVEL MSG(1) MSGLIN — full assignment ok (see LODSFL note)
    MSGLIN = MSG(1);
    // CONV: GOTO DLTX → leavesr replaced by if/else restructure below
  else;
    D2SUP  = SMSUP#;
    // CONV: MOVEL SMNAME D2NAME — see CHGREC note; assign with %subst if lengths differ
    %subst(D2NAME:1:%len(SMNAME)) = SMNAME;
    // CONV: MOVE 'N' D2CONF — single char, full assignment ok
    D2CONF = 'N';
    exfmt DLTREC;
    if not in12;
      if D2CONF = 'Y';
        delete SUPMSTR;
        // CONV: MOVEL MSG(4) MSGLIN — full assignment ok (see LODSFL note)
        MSGLIN = MSG(4);
      endif;
    endif;
  endif;
end-proc;

// *****************************************************************
// *  DSPREC - DISPLAY
// *****************************************************************
dcl-proc DSPREC;
  dcl-pi *n end-pi;

  chain WSUP SUPMSTR;
  if not %found(SUPMST);
    MSGLIN = MSG(1);
  else;
    // CONV: MOVEL 'DISPLAY' D1MODE — see CHGREC note; assign with %subst
    %subst(D1MODE:1:7) = 'DISPLAY';
    in40 = *on;
    in41 = *on;
    exfmt DTLREC;
  endif;
end-proc;

// *****************************************************************
// *  EDTCHK - EDIT (SAME AS NW100R)
// *****************************************************************
dcl-proc EDTCHK;
  dcl-pi *n end-pi;

  in50 = *off;
  in51 = *off;
  in53 = *off;
  in54 = *off;
  in57 = *off;
  if SMNAME = *blanks;
    in50 = *on;
    in51 = *on;
  endif;
  if SMCNTY = *blanks;
    in50 = *on;
    in53 = *on;
  endif;
  // CONV: CHECK VALID SMPHON POS — %check returns 0 when all chars are valid
  POS = %check(VALID:SMPHON);
  if POS > 0;
    in50 = *on;
    in54 = *on;
  endif;
  // FAX CHECK REMOVED 1997 - FOREIGN FAX NUMBERS HAVE LETTERS BJT
  // *C    VALID         CHECK     SMFAX         POS                      57
  // *C  57               SETON                                        50
end-proc;

// *****************************************************************
// *  OLDCHK - NOT USED SINCE 1997 - DO NOT DELETE (BJT)
// *****************************************************************
dcl-proc OLDCHK;
  dcl-pi *n end-pi;

  if SMPOST = *blanks and SMCNTY = 'USA';
    in50 = *on;
  endif;
end-proc;

**CTDATA MSG
Customer not found
Supplier changed
Supplier added
Supplier deleted
Customer has products - not deleted
No suppliers found
Record in use by another user
Unexpected error - call I.S. dept x4357
