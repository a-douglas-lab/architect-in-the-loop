# Results: CUE reach

Method and predictions: [README.md](README.md), committed before any clause was classified (`6256ca3`). Data: [clauses.csv](clauses.csv), written by [classify.py](classify.py). The script checks that its 173 rows are exactly the active constraints at `67b1bd4`. One rater, the author, with seven corrections from review run 2 adopted (below). The CUE demo is reported separately: [demo-results.md](demo-results.md).

## Measures

| Measure | Predicted | First write-up | After review run 2 |
| --- | --- | --- | --- |
| V | 3% | 82 (47%) | 77 (45%) |
| R, process witnessed by a record | 40% | 59 (34%) | 59 (34%) |
| J, judgement | 40% | 27 (16%) | 32 (18%) |
| X, no witness | 17% | 5 (3%) | 5 (3%) |
| Checkable as data today (V or R, witness exists or partly) | 25% | 71 (41%) | 69 (40%) |
| Of those, the witness exists fully | | 33 (19%) | 31 (18%) |
| Checkable as data once its record exists (V or R) | | 141 (82%) | 136 (79%) |
| Checkable against an outcome request, before code | 20% | 27 (16%) | 26 (15%) |
| Of those, V or R | | 22 (13%) | 19 (11%) |
| **Constrains the same field as another clause** (README's measure) | 5% | not measured | **22 (13%)** |
| Falls in a definition another clause also constrains | | 55 (32%) | 55 (32%) |

**Corrections, from review run 2.**
- **The wrong measure was headlined.** The first write-up reported definition-level sharing (32%), said "unification could compare them", and called the predictions "badly wrong". The README predicted field-level sharing, which is what unification compares. Measured, that is 22 clauses (13%), against a prediction of 5%. Most clauses in a shared definition constrain different fields of it. The six `#OutcomeRequest` clauses, for example, constrain six different fields, so unification has nothing to compare among them.
- **V was widened after the predictions.** The README defines V as fixing "a value or range". The classification also counted structure: sections, file locations, record shapes. So the predicted 3% and the measured 45% aren't like for like. The V-or-R total doesn't depend on that boundary.
- **The reviewer re-checked 47 rows and changed seven.** ADR-001 C3, ADR-005 C5, ADR-000 C12, ADR-015 C12 and ADR-018 C5 move from V to J. ADR-008 C7's `pre_code` becomes no. ADR-009 C8 gains a judgement note. All are adopted, and the figures in the last column include them.

## What the numbers mean

- **"Checkable as data" isn't "needs CUE".** Python, JSON Schema or OPA can check any V or R clause once its record is data. 40% is the reach of data-based checking, of which CUE is one option. CUE's distinctive parts are one declarative definition run at every layer, and conflict detection by unification.
- **Unification's field is 13%,** the 22 clauses that constrain a field another clause also constrains. They include the split scenario (3), front matter (5), the evaluation baseline (3), the evaluation set (3), citation format (2), publication contents (2), flag state (2) and SARIF version (2). These clauses are written to agree, so a conflict among them would come from a later change, which is what the demo planted.
- **Most witnesses aren't data yet.** Only 31 clauses (18%) have a witness that exists fully as data today. The outcome request and the split record, where most plan-time clauses fall, don't exist as records at all.
- **Judgement is 18%,** including clauses that matter most at plan time: ADR-004's non-goals in specs, and ADR-015 C13.

## Limits

- **One rater, plus one reviewer's spot-check of 47 rows.** The field assignments behind the 13% are also one rater's.
- **The V class is broader than the README defined it** (above).
