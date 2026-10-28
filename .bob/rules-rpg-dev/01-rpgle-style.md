# RPG Developer mode — style rules

- Layout: `ctl-opt` → `dcl-f` → copybooks (`/copy qprotosrc,xxx`) → `dcl-pi` →
  constants → standalone fields → data structures → mainline → procedures.
- Indent 2 spaces. One statement per line. Keywords lowercase (`dcl-s`, `if`, `endif`).
- Every procedure has a `dcl-pi` and, if exported, a prototype in a `.rpgleinc` copybook.
- Parameters: pass by `const` or `value` unless the procedure must change the caller's
  variable. Use `options(*nopass)` / `%parms()` for optional parameters.
- Data structures that mirror a file use `likerec` or `extname(...: *all)` with `qualified`.
- Error handling: wrap I/O and conversions in `monitor` / `on-error`; never let a
  program end with an unhandled `RNX`/`RNQ` inquiry message in batch.
- Programs end with `return;` (and `*inlr = *on;` only when the program must close files).
- Every new exported procedure gets an RPGUnit test in `qtestsrc/` (see `rpgunit-testing`).
