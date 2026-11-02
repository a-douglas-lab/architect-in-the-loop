# Loop card: review · rule-unit spike · run 12

| Field | Value |
| --- | --- |
| Stage | Review (documentation and spike change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 12 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 11](2026-11-02-rule-units-prior-art-review-run11.md) |

## Run

- **Inputs:** commits `3673c98..f9d5a0e` (prior art v2, the pre-registration, the runner and checks, the model runs, results, delivery, the analyze card, the session log and backlog T6); REVIEW.md; the raw runs under `spikes/rule-units/runs/`; Andy's three messages quoted word for word. Asked to check every number against the raw files, how missed predictions are reported, the confounds, the framing of the recommendation, and commit ordering.
- **What the reviewer re-ran itself:** pytest (27 passed, 3 expected failures), `eval-deterministic` twice, `eval-model` for the translator and the baseline. All matched results.md. It checked every rubric verdict, every f8 and f1 `analyze` row, and the neutral-name mapping.
- **Cost:** 4,063 s harness duration (much longer than run 11's 298 s; not explained), about 132,000 tokens, 21 tool calls.
- **Result:** 2 High, 5 Medium, 9 Low, 5 nits.

## What it found

- **High:** results.md said the constrained model did "better than predicted" while its unit precision (76%) missed the 85% prediction. The author's known failure mode: reporting the part of a prediction that held.
- **High:** prior-art v2 marked v1 question 6 (judgement units, deterministic or by model) as settled, citing an Andy quote about testing selection, not about that choice. It also made hard rule 4 always loaded, from a table T6 calls a proposal, and said the units were "unchanged from v1". The same silent settling run 11 flagged.
- **Medium:** delivery.md said the step before `analyze` "exists"; only alias translation and selection do. Records validated, but all had empty findings and measurements. "27 cases" counted pipeline and meta-tests. The rules file carried each check's description as well as the constraint, an unlisted confound. prior-art.md's status said "reviewed by Andy" for sections he hadn't seen.
- **Low, among others:** stability compared unlike measures (14 of 17 ADR sets against 17 of 17 units; like for like, 15 of 17); "self-reported" dropped again; the baseline's precision prediction unreported; the rubric's rule 4 not word for word; an unverifiable remark about an agent's reply; the translator prompt sharing the labels' negation convention; Andy's point widened to skills and tool search; a "trustworthy check" box ticked on stability alone.
- **Ordering verified** from commits: pre-registration before runner, runner before model outputs. Not verifiable: when the model runs happened, and whether runner code existed uncommitted before `ae25478`.

## Responses

All accepted. Fixed in results.md, prior-art.md, delivery.md, the analyze card, the session log and backlog T6:

- The unit-precision miss and the baseline's precision are stated; the "Acceptance Scenarios" remark is removed.
- prior-art.md separates what Andy's challenges settled (glossary terms from a tested translator) from what he hasn't ruled on: build versus adrkit, deterministic judgement-unit selection, hard rule 4 always loaded, and v1's other recommendations. Status line corrected.
- delivery.md says the joined step isn't built, and that the subject glossary must come from the fork's contract.
- The check-description confound and the translator-prompt confound are listed; the counts read 13 cases plus 3 predicted misses; stability compares units with units.
- The rubric's missing sentence is recorded in results.md, not edited, since the rubric is as run.
- Nits fixed, except the `feature-findings` folder name, which is recorded here as a mild hint: "findings" is a glossary alias.

Author-scored. Not independent.

## What the run showed

Re-running the evaluation, not just reading the results, confirmed every number. The faults were all in framing: a missed prediction told by its half that held, and a question Andy hadn't ruled on recorded as settled. Both are repeats from earlier runs. A pre-registered predictions table that results.md must answer row by row would catch the first mechanically.

## Measurements

Harness duration 4,063 s; about 132,000 tokens.

**Not re-reviewed:** the fixes.
