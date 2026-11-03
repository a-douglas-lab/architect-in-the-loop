# Loop card: review · the separate C17 unit · run 20

| Field | Value |
| --- | --- |
| Stage | Review (spike code and documentation) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 20 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 19](2026-11-03-rule-units-review-run19.md) |

## Run

- **Inputs:** commit `aba7784` (cases written first) and the uncommitted diff on it (C17 check.py, the restored C10 unit, the runner and tests, index.yaml, ADR-016's C17 `ref`, backlog T6, results.md, the session log); REVIEW.md; CLAUDE.md; ADR-000; Andy's "add a separate C17 unit".
- **What the reviewer re-ran:** pytest (63 passed, 2 skipped, 4 xfailed); the tests on a `git archive` copy of `aba7784`; the regex on probe strings.
- **Cost:** harness duration 7,074 s, about 80,000 tokens, 9 tool calls. The reviewer estimated about 4 minutes of its own work; the gap is not explained.
- **Result:** 0 High, 1 Medium, 6 Low, 2 nits.

## What it found

- **Medium:** ADR-016's Enforcement prose ("tested on three files") and C17's mechanism are out of date; fixing them needs a new version.
- **Low:** the plan-text pattern misses common forms and `describes` overclaims; first-match gives a false finding on "convert 1.0.0 to 2.1.0", and a pre-release passes; the C17 cases failed first by a missing file, and the "none" cases can't separate checks; M4's "eight" never failed; `superseded` ignores unknown or duplicate names; the session log left out the new plan-text check.
- **Nits:** "SARIF None" in a message; the glossary's `sarif` definition names only C10.
- **Checks that held:** pytest; the todo case fails as predicted; no pre-registered expectation edited; the ADR change is `ref` only; "2.1" traced to the ADR; the selection side effect disclosed; backlog edit inside T6.

## Responses

- **Medium:** not fixed. A new ADR-016 version needs Andy; disclosed in results.md and put to him.
- **Low:** `describes` and the code comment now say what the pattern reads and misses; the misses, first-match and pre-release behaviour, what "failing first" showed, and M4 are written into results.md. `superseded` and duplicate names now stop the run, with a test. Session log reworded.
- **Nits:** the message fixed. The glossary left unchanged, because the model translator reads it; disclosed.

Author-scored. Not independent.

## What the run showed

Writing expected results first showed order, not strength: cases that expect nothing pass a check that does nothing. A case set needs at least one case per behaviour that a do-nothing check would fail.

## Measurements

Harness duration 7,074 s; about 80,000 tokens.

**Not re-reviewed:** the fixes.
