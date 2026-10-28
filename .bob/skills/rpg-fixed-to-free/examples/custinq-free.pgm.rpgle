**free
// ****************************************************************
// CUSTINQ  - Customer order total inquiry
// Written  - 1998-03-14 JRS
// Changed  - 2004-07-02 MKW Added order count
// Changed  - 2026-10-10 BOB Converted to fully free format (behaviour-preserving)
// ****************************************************************
ctl-opt dftactgrp(*no) actgrp(*caller) option(*srcstmt:*nodebugio);

dcl-f CUSTMAST keyed usage(*input);
dcl-f ORDHDR keyed usage(*input);

// CONV: *ENTRY PLIST -> dcl-pi. Numeric fields defined in C-spec result columns are
//       PACKED, so pTotal is packed(11:2), not zoned.
dcl-pi *n;
  pCustNo char(7);
  pResult char(30);
  pTotal packed(11:2);
end-pi;

dcl-s wCustNo packed(7:0);
dcl-s wTotal packed(11:2);
dcl-s wCount zoned(5:0);
dcl-s wMsg char(30);

// CONV: MOVE char(7) -> packed(7:0). MOVE silently accepted blanks/non-digits;
//       %dec() raises an error instead, so the conversion is monitored.
monitor;
  wCustNo = %dec(pCustNo : 7 : 0);
on-error;
  wCustNo = 0;   // TODO-CONV: confirm callers always pass a numeric customer number
endmon;

// CONV: *IN90 (CHAIN not-found, HI position) is not used elsewhere -> %found().
chain wCustNo CUSTMAST;
if not %found(CUSTMAST);
  // CONV: MOVEL without (P) only overwrites the leftmost 9 bytes; the rest of
  //       pResult keeps the caller's value. Preserved with %subst().
  %subst(pResult : 1 : 9) = 'NOT FOUND';
  pTotal = 0;
  // CONV: GOTO EXIT -> the code at TAG EXIT inlined here.
  *inlr = *on;
  return;
endif;

wTotal = 0;
wCount = 0;
setll wCustNo ORDHDR;
// CONV: *IN91 (READE EOF, EQ position) is not used elsewhere -> %eof().
reade wCustNo ORDHDR;
dow not %eof(ORDHDR);
  // CONV: fixed-format ADD truncated silently on overflow; free-format raises RNX0103.
  //       wTotal is 11,2 and OHAMT is 9,2 per CUSTMAST/ORDHDR, so overflow needs >100 orders
  //       at maximum value - accepted, listed in the conversion report.
  wTotal += OHAMT;
  wCount += 1;
  reade wCustNo ORDHDR;
enddo;
exsr FMTRES;
pTotal = wTotal;

*inlr = *on;
return;

// ****************************************************************
// FMTRES - Build result text: name + order count
// CONV: kept as a subroutine. Converting to a procedure is a separate refactor.
// ****************************************************************
begsr FMTRES;
  wMsg = CMNAME;                         // CONV: MOVEL(P) char->char == assignment
  if wCount > 0;
    // CONV: MOVE '*' (no P) replaces only the rightmost byte of wMsg.
    %subst(wMsg : %len(wMsg) : 1) = '*';
  endif;
  pResult = wMsg;                        // CONV: MOVEL(P) same length == assignment
endsr;
