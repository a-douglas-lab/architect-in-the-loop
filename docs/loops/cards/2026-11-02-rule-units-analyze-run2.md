# Loop card: analyze, with rule units · rule-unit spike · run 2

| Field | Value |
| --- | --- |
| Stage | Analyze, run against test fixtures, with a deterministic rule-unit step before it |
| Outcome | None: project work, Step 7 item 1 (T6) |
| Run | 2 (run 1 is the constitution behaviour test) |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Constitution behaviour test, run 1](2026-11-01-constitution-behaviour-test-run1.md) |

## 1. Purpose

Tests whether loading selected rule units before `analyze` turns f8's miss (a breach no ADR title reveals) into a catch, and measures how well different translators select the units.

## 2. Trigger and inputs

- **Trigger:** Andy's go-ahead, 2 Nov: "go ahead, glossary in the spike folder for now."
- **Inputs:** fixtures f1 to f9 at `289a9db`, eight new fixtures, the glossary, seven units, and `labels.yaml`, all committed before any run (`ae25478`).
- **Context loaded:** `analyze` runs had the constitution, the skill, the feature, and the selected units' rules file. Translator runs had the glossary only; baseline runs had the constitution only; rubric runs had the rubric only. CLAUDE.md was present in every session, as in run 1.

## 3. Actor

- **Who:** fresh-context subagents for every model run; the author ran the deterministic steps and scored the results.
- **Agent setup:** Claude Opus 5.5, general-purpose subagent, default effort. `analyze` used the real `speckit-analyze` skill, with `SPECIFY_FEATURE_DIRECTORY` pointing at a neutral copy outside the repository.
- **Human role:** Andy reviewed the prior art and reshaped the spike (glossary, translator, distinct steps) before anything was built.

## 4. What happened

1. Prior art written and reviewed (run 11), shown to Andy, then reshaped after his challenges (v2).
2. Glossary, units, fixtures, labels, expectations and tests committed before any code (`ae25478`).
3. Runner and checks built; pytest 27 passed, 3 predicted misses. Alias and BM25 scored (`289a9db`).
4. 15 model runs in parallel: translator ×3, title baseline ×3, rubric ×3, `analyze` on f8 ×3, `analyze` on f1 ×3. Prompts, raw outputs and reports committed under `spikes/rule-units/runs/`.

## 5. Feedback loop

- **Signal:** for the deterministic checks, pytest against each unit's expected cases. For model runs, none inside the run: each ran once and was scored afterwards.
- **Stop condition:** each run wrote its output file.
- **Iteration cap:** one attempt per run. Not reached; none failed.
- **Iterations taken:** 1.

## 6. Output

- **Artefact:** [spikes/rule-units/results.md](../../../spikes/rule-units/results.md) and [delivery.md](../../../spikes/rule-units/delivery.md).
- **Feeds:** Andy's review; T6; Step 7 items 2 (validator and index generator) and 4 (hooks).

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| Unit tests for ADR-016@v1 C10 and hard rule 4 | Deterministic | Every non-todo case as expected; at least one case runs | 27 passed; 3 todo cases missed as predicted |
| Rubric for ADR-015@v1 C2 | Rubric, 3 runs | Verdicts as expected | 15 of 15 |
| Translator selection | Rates against labels | Reported, not gated | Constrained model 31 of 31 terms, each run |
| f8 catch | Model, 3 runs | A finding naming C10 or SARIF | 3 of 3, all CRITICAL |
| f1 control | Model, 3 runs | No CRITICAL; no finding naming hard rule 4 | No CRITICAL 3 of 3; a LOW advisory row in 1 of 3 |
| Record schema | Deterministic | Records validate | Pass, for the deterministic records |

The labels are a human judgement. They could become a check only with a second labeller, or with labels drawn from real plans and their reviews.

## 8. Gate

- **Approver:** Andy, architecture coordinator.
- **Evidence shown:** pending; this card, results.md, delivery.md and the raw runs, for local review.
- **Decision:** pending.
- **Did the approver redo any of the work to decide?** Not yet known.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | 15 model runs in parallel, longest 90 s; review run 11 about 5 minutes | Harness durations |
| Human minutes (work plus review) | Not measured: Andy's review time isn't timed | |
| Tokens / cost | About 980,000 tokens for the 15 model runs; about 114,000 for review run 11 | Harness subagent totals |
| Iterations to pass checks | 1 | |
| Leading indicator for this stage | f8 catch rate with units loaded: 3 of 3 (was 0 of 3) | results.md |
| Lagging indicator for this stage | Breaches that reach implement although a unit covered them: not known yet; needs real features | Fill in when known |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| A shell script writing fixtures broke on apostrophes | Quoting prose in bash | Wrote the fixtures with a Python script | Nowhere (author's practice) | Fill in on the next card |
| Five false selections of ADR-011@v1 C3 by the best translator | One term is too coarse for that rule's applicability | Proposed: conjunctions in `applies` | delivery.md, open items | Fill in on the next card |
| Severity predicted as HIGH; came out CRITICAL | Didn't anticipate Principle II making loaded ADR constraints binding | Recorded, not edited | results.md | n/a |
| The "(test fixture)" label and folder names would leak answers | As in run 1 | Neutral copies made by a script this time (`python -m ruleunits neutral`) | The runner | Fixed |

## 11. Ready to automate?

- [ ] Stable inputs and outputs: the rules-file shape is new
- [x] A trustworthy check: the deterministic checks are; the translator was stable across three runs
- [ ] Known failures: the conjunction fix isn't built
- [ ] An evidence-based gate: Andy hasn't reviewed yet
- [x] Known cost

**Verdict:** keep at level 1. **Why:** one spike, 17 small fixtures written by the author, and no review yet.

**Next run changes:** conjunctions in `applies`; real plans from DEV-1 to DEV-3 as fixtures; a second labeller; run the step through whichever trigger Andy chooses.
