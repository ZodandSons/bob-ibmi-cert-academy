**free
// ****************************************************************
// Module   : {MODNAME}  (service program {SRVPGM})
// Purpose  : {what this group of procedures is for}
// Exports  : see qsrvsrc/{srvpgm}.bnd — keep signature order stable!
// Change log:
//   {YYYY-MM-DD} {initials} Created
// ****************************************************************
ctl-opt nomain option(*srcstmt:*nodebugio:*noshowcpy);

/copy qprotosrc,{srvpgm}

// ----------------------------------------------------------------
// Customer_GetName: return the customer name, or '' when not found.
// ----------------------------------------------------------------
dcl-proc Customer_GetName export;
  dcl-pi *n varchar(50);
    customerNo packed(7:0) const;
  end-pi;

  dcl-s name varchar(50);

  exec sql
    SELECT TRIM(CMNAME) INTO :name
      FROM CUSTMAST
     WHERE CMCUST = :customerNo;

  if sqlstate <> '00000';
    return '';
  endif;
  return name;
end-proc;

// ----------------------------------------------------------------
// Customer_IsActive: *on when the customer exists and is active.
// ----------------------------------------------------------------
dcl-proc Customer_IsActive export;
  dcl-pi *n ind;
    customerNo packed(7:0) const;
  end-pi;

  dcl-s status char(1);

  exec sql
    SELECT CMSTAT INTO :status
      FROM CUSTMAST
     WHERE CMCUST = :customerNo;

  return sqlstate = '00000' and status = 'A';
end-proc;
