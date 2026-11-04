# CUE demo: expected results

Written 2026-11-04, before CUE is downloaded or any CUE is written. Andy approved the test: "Yes, download and run it". It tests the claim in [results.md](results.md): that clauses written as CUE constraints on a shared outcome request can be checked against a request before code, and that unification catches a clash between ADRs.

## Setup

- **The tool:** CUE v0.17.1, `cue_v0.17.1_windows_arm64.zip` from the github.com/cue-lang/cue release. Its SHA-256 is checked against the release's checksums file before use. The binary sits in a temporary folder outside the repository.
- **The model:** `model/`, one CUE package. Each ADR whose clauses apply gets its own file, which adds constraints to the shared definitions `#OutcomeRequest` and `#PlanCitations`. A CUE package unifies all its files, so loading the package loads every ADR's clauses at once. Each constraint carries a comment citing it, `ADR-nnn@vN Cn`.
- **The clauses modelled:** 8, from five ADRs.
  - `#OutcomeRequest`:
    - ADR-005@v3 C1: hand-built work comes from DEV-1 to DEV-3.
    - ADR-005@v3 C6: the areas touched are within the outcome's listed areas.
    - ADR-008@v1 C8: visible and hidden examples are both present.
    - ADR-016@v3 C15: ADR-016 isn't applied to development outcomes.
    - ADR-017@v1 C5: the architecture coordinator states the outcome.
  - `#PlanCitations`:
    - ADR-009@v3 C8: the plan lists the ADRs that apply.
    - ADR-009@v3 C13 and ADR-000@v4 C10: each citation is `ADR-nnn@vN Cn`.

  ADR versions are as on this branch.
- **The data:** `data/dev1.yaml`, DEV-1 from development-outcomes.md written as an outcome request and a plan. The areas are DEV-1's listed areas. The examples are placeholders, because DEV-1's examples aren't written yet.
- **The command:** `cue vet -c ./model <data file>`, run by `run_demo.py`, which records each case's exit code and first error lines.

## Cases

| Case | Change | Expected |
| --- | --- | --- |
| Q1 | DEV-1 as written | Pass |
| Q2 | `areas_touched` adds `basket` | Fail, and the error points at the ADR-005 C6 constraint |
| Q3 | `id: EVAL-3` with `kind: development` | Fail, pointing at ADR-005 C1 |
| Q4 | No hidden examples | Fail, pointing at ADR-008 C8 |
| Q5 | A plan citation without a version, `ADR-005 C6` | Fail, pointing at the citation format (ADR-009 C13, ADR-000 C10) |
| Q6 | A test file `adr099.cue` adds `#OutcomeRequest: stated_by: "merchant"`, clashing with ADR-017 C5, with DEV-1's data unchanged | Fail, naming both values and both files. Unification catches the clash between two ADRs |
| Q7 | `adr099.cue` adds `#OutcomeRequest: stated_by: string`, which is compatible | Pass |
| Q8 | As Q6, checked with no data at all (`cue vet -c ./model`) | Fail: the clash shows in the definitions alone, before any request exists |

Q8 is a prediction with low confidence. CUE may report the conflict only when the field is evaluated, and `vet` with no data may not evaluate the definition's fields.

## Measures

For each case: exit code, the first error lines, and whether they name the clause's file and line. For the model: lines of CUE per clause. The run time is recorded but not judged.

## Dated expectation, 2026-11-04, after review run 2

Review run 2 found that Q8 had no control: `cue vet -c` fails on any model with no data, because `request` and `plan` are incomplete, so Q8's exit code proved nothing. Tried by hand on 4 Nov, `cue vet -c=false ./model`, which allows incomplete values, passed on the model alone and failed once the planted clash was added. From this date:

| Case | Change | Expected |
| --- | --- | --- |
| Q8 | As before, run with `cue vet -c=false ./model` | Fail, with "conflicting values" naming `adr017.cue` and `adr099.cue` |
| Q9 (control, new) | The model as committed, no clash, `cue vet -c=false ./model` | Pass |

The clash in Q6 and Q8 is a planted test clause (`adr099.cue`), not a conflict between real ADRs.
