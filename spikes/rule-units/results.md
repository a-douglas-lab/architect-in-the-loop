# Results: rule-unit spike

Run on 2 Nov 2026, on Claude Opus 5.5, the model used for real work. Expectations were committed first in `ae25478` ([expected.md](expected.md)); the runner and deterministic scores followed in `289a9db`; every model run came after that. Expectations are left as written. Where a result differs, this file says so.

Raw material is committed under [runs/](runs/): prompts, the neutral-name mapping, each model's raw output, the scored JSON, the rules files and the full `analyze` reports.

## Headline

| Question | Result |
| --- | --- |
| Does loading f8's unit turn the miss into a catch? | **Yes, 3 of 3** (Run B: 0 of 3). All three raised a CRITICAL naming ADR-016@v1 C10 |
| Does the loaded unit cause false alarms on compliant work? | **No CRITICAL in 3 of 3** on f1. One run added a LOW, advisory row naming hard rule 4 |
| Which translator selects best? | **The constrained model**: 31 of 31 terms in each run, the same sets each run. Its unit precision, 76%, missed the prediction |
| Does any translator beat a model reading ADR titles on unit recall? | **No.** Both reached 16 of 16. A counter-indicator named in expected.md fired; see below |

## The f8 re-run

The units came from the alias translator: adr-016-c10, plus hard-rule-4-copy (always loaded). A script wrote their text to a file, and the prompt told `analyze` to read it. The rules files and reports are in [runs/analyze/](runs/analyze/).

| Run | CRITICALs | Names ADR-016@v1 C10 or SARIF | Severity of that finding | ADR files opened (self-reported) |
| --- | --- | --- | --- | --- |
| 1 | 2 | Yes | CRITICAL | None |
| 2 | 2 | Yes | CRITICAL | None |
| 3 | 2 | Yes | CRITICAL | None |

- **Catch rate: 3 of 3,** as predicted.
- **Severity: CRITICAL, not the HIGH I leaned towards.** Each run reasoned that Principle II ("Decisions Are Recorded and Honoured") makes an ADR MUST binding, so breaking a loaded constraint is a constitution conflict. My prediction was wrong.
- **The second CRITICAL in every run** was that the plan doesn't list ADR-016 or cite C10 (ADR-009@v2 C8, C13). Loading the unit made the omission visible.
- **No run reported opening an ADR.** The unit's text was enough. This supports the hypothesis that the gap was the constraint not reaching the agent.
- **Confound, the check description:** the rules file gave each unit's check description as well as its rule text, so `analyze` had a detection recipe, not just the constraint. See "The counter-indicator, read straight".
- **Confound, the prompt:** the prompt's extra line changes the method in [tests/constitution/README.md](../../tests/constitution/README.md) ("read only what the skill tells it to"). Run B had no such line, so the comparison is between "constitution only" and "constitution plus selected units", not a pure A/B on one variable.

**Control, f1 with hard rule 4 loaded:**

| Run | CRITICALs | Finding naming hard rule 4 |
| --- | --- | --- |
| 1 | 0 | None. The summary notes the rule was checked |
| 2 | 0 | One LOW row, R1: "No finding under the rule's check", suggesting the plan say explicitly that the contract is read in place |
| 3 | 0 | None. A table row records "No finding" |

No CRITICAL in 3 of 3, as predicted. The stricter expectation, "no finding naming hard rule 4", held in 2 of 3: run 2's LOW row names the rule while saying it isn't broken. It is advisory, not a false alarm, but it is noise the loaded unit caused.

## Selection

Scored against [labels.yaml](labels.yaml): 17 fixtures, 31 labelled terms, 16 labelled units (hard rule 4 excluded, as always loaded). Scores are in [runs/selection/](runs/selection/).

| Selector | Term recall | Term precision | Unit recall | Unit precision | Same output in all runs |
| --- | --- | --- | --- | --- | --- |
| Alias | 24 of 31 | 24 of 24 | 14 of 16 | 14 of 17 | Deterministic (checked) |
| BM25 | 30 of 31 | 30 of 92 | 16 of 16 | 16 of 62 | Deterministic (checked) |
| Constrained model, runs 1 to 3 | 31 of 31, each run | 31 of 31, each run | 16 of 16, each run | 16 of 21, each run | 17 of 17 fixtures |
| Baseline, titles, runs 1 to 3 | n/a | n/a | 16 of 16, each run | 16 of 21, 16 of 20, 16 of 22 | 14 of 17 (ADR sets); 15 of 17 (units) |

Against the predictions:

- **Alias:** exactly as worked out by hand. It missed the two paraphrases (n1's "objections", n2's "hold back a stuck piece"), f1 and f2's "subject contract", f5 and f6's "acceptance ... checks", and h4-port's "retyped". It falsely selected ADR-011@v1 C3 on f7, s-compliant and s-four.
- **BM25:** as predicted, full recall and very low precision. Alias words such as "test", "file" and "switched" match ordinary sentences. With nine short documents, one shared word passes the cut-off. BM25 isn't a useful translator here.
- **Constrained model, terms:** better than predicted (term recall 90% or more). It made no term errors in any run, including the paraphrases, negated mentions and the hand port. The prompt told it to count a concept "whether it is asserted or negated", which is the labels' own convention, so the negated mentions were helped by the prompt.
- **Constrained model, units: the prediction missed.** expected.md predicted unit precision of 85% or more; every run scored 16 of 21 (76%).
- **Its five unit errors are all the same one,** and the translation isn't the cause. ADR-011@v1 C3 (writes to acceptance tests blocked during implement) is selected whenever acceptance tests are mentioned, but those fixtures run acceptance examples or deny touching them. The labels say the concept is present but the rule isn't relevant. A single `terms_any` term is too coarse for this rule: it needs a conjunction, such as acceptance-test together with a "write or edit" term.
- **Baseline:** recall matched the constrained model, against the prediction ("below the constrained model"). Its false selections come from ADR granularity: choosing ADR-016 brings ADR-016@v1 C2, and ADR-011 was added for f3 and f9 in some runs. It chose ADR-016 for f8 in 3 of 3 runs. Its unit precision was 16 of 21, 16 of 20 and 16 of 22 (76%, 80%, 73%), below alias's 82% as predicted; run 1 equals the constrained model's precision.

### The counter-indicator, read straight

Expected.md lists "No translator beats the baseline on unit recall" as evidence against rule units. On this set, none did: both scored 16 of 16. So:

- **Selection by title wasn't what failed f8.** Asked directly which ADRs apply, a model picked ADR-016 every time. In Run B, `analyze` wasn't asked that, read no ADRs, and two of three runs only "suggested ADR-016 might apply". What changed the outcome was the unit reaching the agent. That was more than the constraint: the rules file also carried each check's description, which works as a detection recipe ("a finding if the artefacts … name an output format other than SARIF"), and runs 2 and 3 cite the check firing. This spike can't separate the constraint text from the recipe.
- **What the units add over the baseline,** on this evidence: constraint-level delivery (the baseline picks whole ADRs, so it would also need to open them, which `analyze` doesn't do); the same units every run (17 of 17 fixtures against the baseline's 15 of 17); and a selection that can be tested and replayed.
- **Limits:** 17 small fixtures written by the author, most of them stating their own intent; labels written by the author; one model family doing both the work and the selection. The baseline may do worse on long, real plans, or across many more ADRs, where titles carry less. That is untested.

## Validation

**Deterministic units**, run by `python -m pytest` in this folder: 27 passed, 3 expected failures. Of these, 16 are unit check cases (13 passed as expected, 3 predicted misses); the other 14 passed tests are 12 pipeline tests and 2 meta-tests. The expected failures are the three cases predicted as misses, and all three missed as predicted:

- ADR-016@v1 C10: c10-unnamed (format described, not named).
- Hard rule 4: h4-port (retyped by hand), and the copy with a renamed namespace (not byte-identical).

Each unit is shown blocking (findings on f8, n1, the CSV and non-SARIF JSON files, f4 and the byte-identical copy) as well as passing (c10-sarif, f1, the SARIF file at version 2.1.0, h4-read, f8 for hard rule 4, the clean tree). A test file with no cases fails (`EmptyRun`).

**Judgement unit, ADR-015@v1 C2,** graded three times ([runs/rubric/](runs/rubric/)):

| Fixture | Expected | Verdicts | Rules failed |
| --- | --- | --- | --- |
| f5 | fail | fail, fail, fail | All five, each run |
| f6 | fail | fail, fail, fail | All five, each run |
| s-four | fail | fail, fail, fail | Rule 4 (risk rung), each run |
| s-compliant | pass | pass, pass, pass | None |
| f1 | not-applicable | not-applicable ×3 | n/a |

15 of 15 verdicts as expected, with the same failing rules in every run. The rubric's rule 4 is introduced as word for word but leaves out ADR-015's sentence "Risk rungs are the use-case ladder in the architecture sketch, which is still a proposal (A1)". The rubric is left as run; a later version should restore the sentence. All five cases were graded in one context per run (a batch), which is a confound. f5 and f6 had already been caught from ADR-015's title in Run A, so they test the rubric, not a gap closed.

## Report

Every deterministic record validated against [report.schema.json](report.schema.json) (`runs/selection/alias.json`, `bm25.json`), but every one has `findings: []` and `measurements: {}`. So the SARIF-shaped violations part was never exercised with a real finding, against expected.md's prediction that records would carry findings and measurements. The validator is a hand-written subset of JSON Schema (type, required, properties, items, enum), since no schema library was installed. Records weren't generated for model runs or the `analyze` reports; their outputs are kept raw. The record's shape is early evidence for Q2, not a decision.

## Cost

Subagent totals as reported by the harness, including agent overhead.

| Run | Tokens per run | Time per run |
| --- | --- | --- |
| Constrained model translator, 17 fixtures | 64,400 to 64,700 | 35 to 48 s |
| Baseline, titles, 17 fixtures | 65,900 to 72,300 | 42 to 52 s |
| Rubric, 5 fixtures | 58,200 to 58,500 | 33 to 38 s |
| `analyze` on f8 with units | 65,900 to 66,700 | 57 to 68 s |
| `analyze` on f1 with units | 66,200 to 66,800 | 60 to 90 s |

Against Run B's `analyze` (about 62,000 to 64,000 tokens, 26 to 51 s), loading units added a few thousand tokens per run. Part of that is the extra file and part is the agents' longer reports, so the share due to the units isn't separable. About 980,000 tokens across the 15 model runs. The deterministic translators, selection and checks run in under a second.

## Against "what would count against rule units"

- f8 caught in fewer than 2 of 3: **no**, 3 of 3.
- A false CRITICAL from the loaded unit: **no.** One LOW advisory row.
- No translator beats the baseline on unit recall: **yes, it fired.** Read above: on this set the gain comes from delivering constraint text deterministically, not from better selection.
