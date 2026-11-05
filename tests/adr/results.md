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

## F. Front-matter schema, local (Windows 11, Python 3.13.5, fresh venv from `requirements.txt`)

Run after the dated expectation was committed (`687b1e6`). 11 of 11 matched on the first run: F0 and F10 passed, and F1 to F9 failed on C1 (F9 without a crash). The A cases were re-run in the same venv: 20 of 20. F0 passing means all 19 ADRs already conform to the schema.

The harness compares F cases with the change itself (`--base HEAD`), because a front-matter-only edit of an accepted ADR also breaks C8 against the original. That isolates C1.

Without the libraries, `check` reports "C1: not checked: install requirements.txt" for each ADR and fails. CI installs them first.

## On the repository's real history

- `scripts/adr.py check --base 624a523`, the commit Step 7 started from: "19 ADRs checked, 0 problems". Every ADR revision made in Step 7 passes C8 and C9. That covers ADR-010 v2, ADR-011 v2 and v3, ADR-013 v2, and ADR-016 v2 and v3, which the rule-unit spike session made.
- **Two real checks of the validator by its own enforcement update.** Setting `state` and `ref` on ADR-000 C2, C3, C5, C8 and C9 and ADR-009 C10, C14 and C17, with no version change, passed (C8's exception). Then the approved revisions, ADR-000 v4 and ADR-009 v3, passed against `origin/main`.

## K. The C1 hook on ADR edits

`python -I tests/controls/test_hooks.py`: 29 of 29. K12 was reported, and its reason names C2 (the harness checks this); K13 and K14 were silent.

## Not run yet

CI on GitHub, which needs a push with Andy's approval.

## After review run 1 (4 Nov)

Run after the dated expectations were committed (`6d83ffe`), in the venv with `requirements.txt`.

**Run 1 hung.** The new pattern for enforcement states nested a repeated `\s+`, which also matches newlines, and it backtracked without end. Two processes used 940 and 600 CPU-seconds before they were stopped. Fix: the entries are read line by line (`entry_states()`).

**Run 2:** 37 of 37. A0 to A25 and F0 to F10 matched in 116 seconds.
- A20 and A21 fail on C9's withdrawn consistency.
- A22 and A23 fail on C8's one-line-per-version and who-and-summary rules.
- A24 fails on C17 with no rules found.
- A25 fails on C14 when scope is a block list.
- F1 to F9 failed on the schema itself, not on missing libraries.
- A16 shows no C8 problem for the new ADR.

Every existing History line already matched the stricter C8 format, so nothing in the repository was rejected. `check --base origin/main` and `check --base 624a523`: 0 problems. Hook tests: 29 of 29.

**Corrections to the record above.** Harness run 1 had one harness fault, the guessed file name, not two; the A18 crash was a validator fault (encoding). Review run 1 also found that the earlier "0 problems on the real history" was checked by the reviewer without the schema libraries; with them installed it is still 0.

## After review run 2 (5 Nov)

- **A25 didn't test what it claimed.** Without the schema libraries it still failed on "C14", because the old index-mismatch message contains "C14". So the new YAML cross-check was untested. Fix, in the harness only: A25 regenerates the index after its change, so only the cross-check can catch it, and the harness requires its message ("reads differently as YAML").
- **The C9 withdrawn check moved out of the per-file checks,** so the C1 hook does exactly what ADR-000 v4's Enforcement section says (C2, C3's file-name rule and C5). `check()` still runs it, so A20 and A21 are unchanged.
- **C8's "who" is checked by format only:** text, a colon, then a summary. A line with no approver passes if its summary has a colon in it. Whether the named person approved is still review's job (ADR-000 C11).

Run: 37 of 37 in 123 seconds, in the venv with `requirements.txt`. Hook tests: 29 of 29. `check --base origin/main`: 0 problems.
