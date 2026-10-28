**free
// ****************************************************************
// Test     : T_ORDSRV - RPGUnit tests for service program ORDSRV
// Build    : RUCRTRPG TSTPGM(&DEVLIB/T_ORDSRV) SRCSTMF('qtestsrc/t_ordsrv.rpgle')
//              BNDSRVPGM(&DEVLIB/ORDSRV)
// Run      : RUCALLTST TSTPGM(&DEVLIB/T_ORDSRV)
// ****************************************************************
ctl-opt nomain option(*srcstmt:*nodebugio);

/include qinclude,TESTCASE
/copy qprotosrc,ordsrv

dcl-f CUSTMAST keyed usage(*update:*delete:*output) usropn;

dcl-c TEST_CUSTOMER 9999901;
dcl-c MISSING_CUSTOMER 9999999;

// ---- Fixtures (run against the test library on the library list) ----
dcl-proc setUpSuite export;
  open CUSTMAST;
end-proc;

dcl-proc tearDownSuite export;
  close CUSTMAST;
end-proc;

dcl-proc setUp export;
  removeCustomer(TEST_CUSTOMER);
  removeCustomer(MISSING_CUSTOMER);
  CMCUST = TEST_CUSTOMER;
  CMNAME = 'RPGUNIT TEST CUSTOMER';
  CMSTAT = 'A';
  write CUSTREC;
end-proc;

dcl-proc tearDown export;
  removeCustomer(TEST_CUSTOMER);
end-proc;

dcl-proc removeCustomer;
  dcl-pi *n;
    customerNo packed(7:0) const;
  end-pi;
  delete (customerNo) CUSTMAST;   // no-op when the record does not exist
end-proc;

// ---- Tests -----------------------------------------------------
dcl-proc test_getName_returnsTrimmedName export;
  aEqual('RPGUNIT TEST CUSTOMER' : Customer_GetName(TEST_CUSTOMER));
end-proc;

dcl-proc test_getName_returnsBlankWhenNotFound export;
  aEqual('' : Customer_GetName(MISSING_CUSTOMER));
end-proc;

dcl-proc test_isActive_trueForActiveCustomer export;
  assert(Customer_IsActive(TEST_CUSTOMER) : 'Active customer should be active');
end-proc;

dcl-proc test_isActive_falseWhenNotFound export;
  assert(not Customer_IsActive(MISSING_CUSTOMER) : 'Unknown customer must not be active');
end-proc;
