/* ****************************************************************** */
/* Command  : {CMDNAME}  -> processing program {PGMNAME}               */
/* Create   : CRTCMD CMD(lib/{CMDNAME}) PGM(*LIBL/{PGMNAME})           */
/*            (TOBi / makei does this from the .cmd file)              */
/* ****************************************************************** */
             CMD        PROMPT('Process orders by date range')

             PARM       KWD(FROMDATE) TYPE(*CHAR) LEN(8) MIN(1) +
                          PROMPT('From date (YYYYMMDD)')

             PARM       KWD(TODATE) TYPE(*CHAR) LEN(8) MIN(1) +
                          PROMPT('To date (YYYYMMDD)')
