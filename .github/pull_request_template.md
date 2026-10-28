## Summary
<!-- One or two sentences: what changes and why. Link the ticket. -->

## IBM i objects changed
| Object | Type | Source file | Change |
|---|---|---|---|
| <!-- CUSTINQ --> | <!-- *PGM --> | <!-- qrpglesrc/custinq.pgm.rpgle --> | <!-- converted to free format --> |

## Build and deployment notes
- [ ] Builds with `makei build` in a developer library
- [ ] Build order / dependencies updated in `Rules.mk`
- [ ] File layout changes: programs to recompile listed (level checks)
- [ ] Service program signature changed? Binder source updated

## Testing
- [ ] RPGUnit tests added or updated (`qtestsrc/`)
- [ ] For conversions: `verify_conversion.py` passes and report is in `conversions/`
- Manual test steps:

## Bob usage
<!-- Which mode/commands were used (e.g. /convert-to-free in Modernizer mode)
     and what a human reviewed. -->

## Risks and rollback
