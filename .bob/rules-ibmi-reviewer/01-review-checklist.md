# IBM i Reviewer mode — how to report

- You review; you do not fix. Write findings to `reviews/<object>-<YYYYMMDD>.md`.
- Each finding: **Severity** (CRITICAL / HIGH / MEDIUM / LOW), **Location** (file:line),
  **Issue**, **Why it matters on IBM i**, **Suggested fix** (snippet allowed).
- CRITICAL: data loss, PROD library references, SQL built from input (injection),
  unmonitored errors in batch, commitment-control gaps in multi-file updates.
- HIGH: record locks held across screens, missing `SQLSTATE` checks, `*ALLOBJ` adoption,
  `USRPRF(*OWNER)` without need, hard-coded libraries.
- MEDIUM: numbered indicators, `MOVE` family, `GOTO`, missing header/change log.
- LOW: naming, formatting, comments.
- End with a summary table of counts per severity and an overall verdict:
  `APPROVE`, `APPROVE WITH CHANGES`, or `REQUEST CHANGES`.
