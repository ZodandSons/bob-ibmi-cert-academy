# SQLRPGLE patterns

## Uniform SQLSTATE check
```rpgle
dcl-proc checkSql;
  dcl-pi *n ind;           // *on = OK (including "no row" when allowed)
    context varchar(100) const;
    allowNotFound ind const options(*nopass);
  end-pi;

  if sqlstate = '00000' or %subst(sqlstate : 1 : 2) = '01';
    return *on;
  endif;
  if sqlstate = '02000' and %parms() >= 2 and allowNotFound;
    return *on;
  endif;
  logError(context + ' failed, SQLSTATE ' + sqlstate + ' SQLCODE ' + %char(sqlcode));
  return *off;
end-proc;
```

## Single row
```rpgle
exec sql
  SELECT CMNAME, CMSTAT INTO :name, :status
    FROM CUSTMAST
   WHERE CMCUST = :customerNo;
if not checkSql('read customer' : *on) or sqlstate = '02000';
  return *off;
endif;
```

## Cursor with multi-row fetch
```rpgle
dcl-c MAX_ROWS 100;
dcl-ds order qualified dim(MAX_ROWS);
  orderNo packed(9:0);
  amount  packed(11:2);
end-ds;
dcl-s fetched int(10);
dcl-s i int(10);

exec sql DECLARE c_orders CURSOR FOR
  SELECT OHORD, OHAMT FROM ORDHDR
   WHERE OHCUST = :customerNo
   ORDER BY OHORD
  FOR READ ONLY;

exec sql OPEN c_orders;
if checkSql('open c_orders');
  dou fetched < MAX_ROWS;
    exec sql FETCH NEXT FROM c_orders FOR :MAX_ROWS ROWS INTO :order;
    if not checkSql('fetch c_orders' : *on);
      leave;
    endif;
    exec sql GET DIAGNOSTICS :fetched = ROW_COUNT;
    for i = 1 to fetched;
      // process order(i)
    endfor;
  enddo;
endif;
exec sql CLOSE c_orders;
```

## Replacing native I/O
| Native | SQL |
|--------|-----|
| `chain` | `SELECT ... INTO ... WHERE key = :k` |
| `setll` + `reade` loop | cursor `WHERE key = :k ORDER BY ...` |
| `update` after `chain` | `UPDATE ... SET ... WHERE key = :k` (no read needed) |
| `write` | `INSERT INTO ... VALUES(...)` |
| loop + `delete` | single `DELETE ... WHERE ...` |

## DDL for a new table (`qsqlsrc/ordnote.table`)
```sql
CREATE OR REPLACE TABLE ORDER_NOTES FOR SYSTEM NAME ORDNOTE (
  ORDER_NO    DECIMAL(9, 0)  NOT NULL,
  NOTE_SEQ    INTEGER        NOT NULL,
  NOTE_TEXT   VARCHAR(500)   NOT NULL DEFAULT '',
  CREATED_AT  TIMESTAMP      NOT NULL DEFAULT CURRENT TIMESTAMP,
  CREATED_BY  VARCHAR(18)    NOT NULL DEFAULT USER,
  PRIMARY KEY (ORDER_NO, NOTE_SEQ)
) RCDFMT ORDNOTER;

LABEL ON TABLE ORDER_NOTES IS 'Order notes';
LABEL ON COLUMN ORDER_NOTES (ORDER_NO TEXT IS 'Order number',
                             NOTE_TEXT TEXT IS 'Note text');
```

## Running CL from SQL
```sql
CALL QSYS2.QCMDEXC('ADDLIBLE LIB(ORDDEV01) POSITION(*FIRST)');
```
