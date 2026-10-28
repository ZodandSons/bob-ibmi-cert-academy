# Modernizer mode — verification is mandatory

A conversion is not done until all of these are true:

- [ ] `python3 .bob/skills/rpg-fixed-to-free/scripts/verify_conversion.py <original> <converted>`
      exits with code 0.
- [ ] The program compiles: `makei c -f qrpglesrc/<file>` (or the user confirms they compiled it).
- [ ] A conversion report exists at `conversions/<NAME>.md` listing: opcode counts before,
      every `TODO-CONV`, every `MOVE`-family decision, and indicator changes.
- [ ] If RPGUnit tests exist for the program, they pass.
