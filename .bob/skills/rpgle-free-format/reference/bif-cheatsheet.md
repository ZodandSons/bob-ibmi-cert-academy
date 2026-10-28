# Free-format RPG quick reference

## Data types
| Free | Fixed equivalent | Notes |
|------|------------------|-------|
| `char(n)` / `varchar(n)` | `nA` / `nA VARYING` | varchar for built-up strings |
| `packed(p:s)` | `pP s` | Default for numeric DB fields |
| `zoned(p:s)` | `pS s` | |
| `int(10)` / `int(20)` | `10I 0` / `20I 0` | int(3), int(5) also valid |
| `uns(10)` | `10U 0` | |
| `ind` | `N` | `*on` / `*off` |
| `date(*iso)` / `time` / `timestamp` | `D` / `T` / `Z` | |
| `pointer` / `pointer(*proc)` | `*` | |
| `like(fld)`, `likeds(ds)`, `likerec(rec)` | | |

## Most-used BIFs
| BIF | Example |
|-----|---------|
| `%trim/%triml/%trimr` | `name = %trim(CMNAME);` |
| `%subst` | `zip5 = %subst(zip : 1 : 5);` |
| `%scan` / `%scanrpl` | `pos = %scan('@' : email);` `s = %scanrpl('-' : '' : s);` |
| `%char` / `%dec` / `%int` | `txt = %char(amount);` `n = %dec(txt : 9 : 2);` |
| `%editc` / `%editw` | `out = %editc(amount : 'J');` |
| `%len` / `%size` / `%elem` | `for i = 1 to %elem(arr);` |
| `%found` / `%eof` / `%equal` / `%error` | after `chain`, `read`, `setll`, `(e)` |
| `%date` / `%time` / `%timestamp` | `d = %date(ymd : *iso);` |
| `%diff` / `+ %days(n)` | `age = %diff(%date() : birth : *years);` |
| `%lookup` / `%tlookup` | `idx = %lookup(code : codes);` |
| `%xlate` | `up = %xlate(lower : upper : s);` (or `%upper` on 7.4+) |
| `%split` (7.4+) | `for-each word in %split(line : ',');` |
| `%list` (7.4+) | `if code in %list('A' : 'B');` |
| `%kds` | `chain %kds(keys : 2) ORDDTL;` |
| `%parms` / `%passed` | optional parameters |

## Error handling
```rpgle
monitor;
  total = qty * price;
on-error 103;          // RNX0103 overflow
  total = *hival;
on-error;              // anything else
  logError('calc failed');
endmon;
```

## Embedded SQL basics
```rpgle
exec sql SET OPTION COMMIT = *NONE, NAMING = *SYS, CLOSQLCSR = *ENDMOD;
exec sql SELECT COUNT(*) INTO :count FROM ORDHDR WHERE OHCUST = :customerNo;
if sqlstate <> '00000';
  // handle
endif;
```
