# Results: CUE reach

Method and predictions: [README.md](README.md), committed before any clause was classified (`6256ca3`). Data: [clauses.csv](clauses.csv), written by [classify.py](classify.py). The script checks that its 173 rows are exactly the active constraints at `67b1bd4`. One rater, the author. No CUE was run.

## Measures

| Measure | Predicted | Measured |
| --- | --- | --- |
| V, a value or structure in an artefact | 3% | 82 (47%) |
| R, process witnessed by a record | 40% | 59 (34%) |
| J, judgement | 40% | 27 (16%) |
| X, no witness | 17% | 5 (3%) |
| CUE can check it today (V or R, witness exists or partly) | 25% | 71 (41%) |
| Of those, the witness exists fully | | 33 (19%) |
| CUE could check it once its record exists (V or R) | | 141 (82%) |
| Checkable against an outcome request, before code | 20% | 27 (16%) |
| Of those, V or R | | 22 (13%) |
| Constrains a definition another clause also constrains | 5% | 55 (32%) |

The predictions were badly wrong in the direction that favours CUE. The author's earlier "1 of 171" counted only clauses whose text names a value. It missed every clause about the *structure* of an artefact (front matter, settings, labels, split records) and every clause witnessed by a record. That earlier figure, and the Q1 note built on it, understated CUE's reach.

## What the numbers mean, and don't

- **"Checkable as data" isn't "needs CUE".** Every V or R clause can be checked by any program once its record is data: Python, JSON Schema, OPA. 41% is the reach of *data-based checking*, of which CUE is one option. What is distinctive to CUE is narrower: one declarative definition run at every layer (VL-1), and conflict detection by unification.
- **Many witnesses aren't data yet.** Some are Markdown, such as development-outcomes.md, plans, loop cards and the backlog. Some are code, which needs a dependency graph exported. Some are records the capability will create but hasn't. Only 33 clauses (19%) have a witness that exists as data today.
- **Unification has a real field, at plan time.** 55 clauses (32%) fall into 14 shared definitions. The largest are at the point Andy asked about, loading clauses against an outcome request:
  - `#SplitRecord`: 8 clauses, all from ADR-015. Scenario, the five rules, dependency between parts, risk rungs and approvals.
  - `#OutcomeRequest`: 6 clauses, from ADR-005, 007, 008, 016 and 017. Which outcome, its listed areas, its example sets, who stated it, its type.
  - `#PlanCitations`: 3 clauses (ADR-000 C10, ADR-009 C8 and C13).

  Today none of these records exists as data. If they were defined as CUE, a request or plan could be checked against every clause on it at once, before any code. Clauses from different ADRs that constrain the same field would then be compared by unification: a conflict between them would show as a failure, not go unnoticed.
- **Judgement is smaller than predicted (16%),** but it includes clauses that matter most at plan time: ADR-004's non-goals in specs, and ADR-015 C13 "MUST NOT reduce what the outcome asked for". Those stay with rubrics and graders.

## Limits

- **One rater.** Several calls are close: V or J for ADR-001 C3 and ADR-005 C4, R or X for ADR-012 C5. A blind second rater would give agreement, and isn't done.
- **The V class is broad by the method's definition.** It includes Markdown structure (ADR-000 C2) that needs parsing before any data check.
- **No CUE was run.** Whether CUE's errors are usable, and what it costs in CI, is untested.

## What would test the claim

A small CUE model of `#OutcomeRequest` and `#PlanCitations`. DEV-1, written as data, would be loaded against the 9 clauses those two definitions carry. A deliberately conflicting clause would then be added, to see unification catch it. This needs the CUE binary: `cue_v0.17.1_windows_arm64.zip`, 8.85 MB, from github.com/cue-lang/cue releases. Andy's approval is needed for the download.
