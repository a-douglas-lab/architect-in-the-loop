# Results: ADR validator and index generator

Expected results are in [expected.md](expected.md), committed before any code (`0c5b00b`).

## A. Validator cases, local (Windows 11, Python 3.13.5)

Command: `python -I tests/adr/test_adr.py`.

**Before the harness ran, the author ran A0's check by hand** (`scripts/adr.py check --base origin/main`). It failed: "the index doesn't match the ADRs' front matter". The cause was a validator fault, not a finding. ADR-004's title is quoted in its YAML (`"Non-goals: …"`) because it holds a colon, and the line-pattern reader kept the quotes. Fix: quoted scalars are unquoted.

**Harness run 1:** two harness faults, then a validator fault.
- A guessed file name for ADR-005 stopped the run at A1. Fix: the harness looks the name up.
- After that, A0 to A17 matched.
- A18 crashed the harness. The validator printed "…" in its message, Windows wrote it in its code page, and the harness read UTF-8. Fix: the validator writes UTF-8 on every system.

**Harness run 2:** 20 of 20 matched.

| Case | Expected | Result |
| --- | --- | --- |
| A0 | Pass | Pass, after the unquoting fix above |
| A1, A2 | Fail, C2 | Fail, C2 |
| A3, A5 | Fail, C3 | Fail, C3 |
| A4 | Fail, C3 twice | Fail, naming both |
| A6, A7 | Fail, C5 | Fail, C5 |
| A8, A9, A19 | Fail, C8 | Fail, C8 |
| A10, A11, A13, A17 | Pass | Pass |
| A12 | Fail, C9 | Fail, C9 |
| A14, A15, A16 | Fail, C10 and C14 | Fail, C10 and C14 |
| A18 | Fail, C17 | Fail, C17 |

## On the repository's real history

- `scripts/adr.py check --base 624a523`, the commit Step 7 started from: "19 ADRs checked, 0 problems". Every ADR revision made in Step 7 passes C8 and C9. That covers ADR-010 v2, ADR-011 v2 and v3, ADR-013 v2, and ADR-016 v2 and v3, which the rule-unit spike session made.
- **Two real checks of the validator by its own enforcement update.** Setting `state` and `ref` on ADR-000 C2, C3, C5, C8 and C9 and ADR-009 C10, C14 and C17, with no version change, passed (C8's exception). Then the approved revisions, ADR-000 v4 and ADR-009 v3, passed against `origin/main`.

## K. The C1 hook on ADR edits

`python -I tests/controls/test_hooks.py`: 29 of 29. K12 was reported, and its reason names C2 (the harness checks this); K13 and K14 were silent.

## Not run yet

CI on GitHub, which needs a push with Andy's approval.
