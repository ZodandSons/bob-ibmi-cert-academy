**free
// ****************************************************************
// LAB: literate coding (exam objective 3.2)
//
// 1. Copy this file to qrpglesrc/ordtotal.rpgle and open it in Bob IDE.
// 2. Turn on literate coding: Cmd+I (macOS) / Ctrl+I (Windows/Linux),
//    or the magic-wand icon in the editor toolbar.
// 3. Replace each "INSTRUCTION:" comment below with the same text typed as a
//    literate-coding instruction (it turns blue), then press Cmd/Ctrl+Enter.
// 4. Review the INLINE DIFF. Accept (Cmd+Enter) only if it matches the intent;
//    reject (Cmd+Shift+Backspace) and refine the instruction if it doesn't.
//
// Why literate coding here? The change is LOCAL to one file and one procedure.
// If it needed new copybooks, a test program and a Rules.mk change, use Agent mode.
// ****************************************************************
ctl-opt nomain option(*srcstmt:*nodebugio);

dcl-proc Order_Total export;
  dcl-pi *n packed(11:2);
    orderNo packed(9:0) const;
  end-pi;

  dcl-s total packed(11:2) inz(0);

  // INSTRUCTION: Use embedded SQL to sum ODQTY * ODPRICE from ORDDTL for this
  // orderNo into total. Check SQLSTATE: '02000' or a null sum means total = 0;
  // any other non-'00000' state returns -1.

  return total;
end-proc;

dcl-proc Order_LineCount export;
  dcl-pi *n int(10);
    orderNo packed(9:0) const;
  end-pi;

  // INSTRUCTION: Return COUNT(*) of ORDDTL rows for orderNo using embedded SQL,
  // or -1 if SQLSTATE is not '00000'.

end-proc;
