---
name: convert-to-free
description: 'Convert a fixed-format RPG source to fully free format, with verification'
metadata:
  user-invocable: true
  disable-model-invocation: true
  argument-hint: <legacy-source-file>
---

Convert `$1` from fixed-format RPG to fully free-format RPG IV.

Follow the `rpg-fixed-to-free` skill exactly:

1. Run `python3 .bob/skills/rpg-fixed-to-free/scripts/inventory_fixed.py $1 --format markdown`
   and show me the inventory before changing anything. Stop and ask if the risk level is HIGH.
2. Convert spec by spec (H → F → D → P/C → O) into a new file under `qrpglesrc/`
   with the same object name. Never modify `$1`.
3. Run `python3 .bob/skills/rpg-fixed-to-free/scripts/verify_conversion.py $1 <new-file>`
   and fix every ERROR it reports.
4. Compile with `makei c -f <new-file>` if the build environment is available.
5. Write the conversion report to `conversions/<NAME>.md` using the template in the skill.

Finish with a short summary: files written, TODO-CONV items, and anything I must check by hand.
