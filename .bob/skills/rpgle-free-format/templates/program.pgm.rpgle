**free
// ****************************************************************
// Program  : {PGMNAME}
// Purpose  : {one line describing what the program does}
// Author   : {author}
// Created  : {YYYY-MM-DD}
// Parameters:
//   pCustomer  char(7)   in   Customer number
//   pStatus    char(1)   out  'Y' success, 'N' failure
// Change log:
//   {YYYY-MM-DD} {initials} Created
// ****************************************************************
ctl-opt main(main)
        dftactgrp(*no) actgrp(*caller)
        option(*srcstmt:*nodebugio:*noshowcpy)
        bnddir('ORDBNDDIR');

/copy qprotosrc,errors

dcl-f CUSTMAST keyed usage(*input) usropn;

dcl-c STATUS_OK 'Y';
dcl-c STATUS_ERROR 'N';

// ----------------------------------------------------------------
dcl-proc main;
  dcl-pi *n;
    pCustomer char(7) const;
    pStatus char(1);
  end-pi;

  dcl-s customerNo packed(7:0);

  pStatus = STATUS_ERROR;

  monitor;
    customerNo = %dec(pCustomer : 7 : 0);
  on-error;
    logError('Invalid customer number: ' + pCustomer);
    return;
  endmon;

  if not %open(CUSTMAST);
    open CUSTMAST;
  endif;

  if processCustomer(customerNo);
    pStatus = STATUS_OK;
  endif;

  close *all;
  return;
end-proc;

// ----------------------------------------------------------------
// processCustomer: {what it does}. Returns *on when successful.
// ----------------------------------------------------------------
dcl-proc processCustomer;
  dcl-pi *n ind;
    customerNo packed(7:0) const;
  end-pi;

  dcl-ds customer likerec(CUSTREC : *input) inz;

  chain(e) (customerNo) CUSTMAST customer;
  if %error();
    logError('I/O error reading CUSTMAST for ' + %char(customerNo));
    return *off;
  endif;
  if not %found(CUSTMAST);
    return *off;
  endif;

  // {business logic here}

  return *on;
end-proc;
