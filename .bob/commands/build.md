---
description: Compile with TOBi (makei) and fix any compile errors
argument-hint: <source-file | all>
---
Build `$1` using the `ibmi-build` skill.

- If `$1` is `all`, run `makei build`. Otherwise run `makei c -f $1`.
- Read errors from the compile listing / `.evfevent` files under `.logs/` and `.evfevent/`.
- Fix errors in the source (respecting the current mode's edit permissions) and rebuild.
  Stop after 3 attempts and summarize what is still failing.
- Never change `iproj.json`, `.ibmi.json` or `Rules.mk` to make a build pass without
  telling me why.
