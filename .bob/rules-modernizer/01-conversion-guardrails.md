# Modernizer mode — conversion guardrails

1. Always follow the `rpg-fixed-to-free` skill. Do not convert from memory.
2. Conversion is **behaviour-preserving**. Translate; do not redesign. Refactoring
   (subroutines → procedures, SQL replacing native I/O) is a separate, later step.
3. Never edit the original. Read from `qrpglesrc/legacy/NAME.*` and write the result to
   `qrpglesrc/NAME.<ext>` with the same object name.
4. Every `MOVE`/`MOVEL`/`MOVEA` must be converted using the rules in
   `reference/opcode-mapping.md` — never a plain `=` unless the field types and lengths
   prove it is identical. Add a `// CONV:` comment explaining the choice.
5. Keep numbered indicators when they are used by display/printer files or other programs;
   only replace them with BIFs when the indicator is purely local.
6. Mark anything uncertain with `// TODO-CONV:` and list it in the conversion report.
