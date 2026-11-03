# Loop card: review · rule-unit prior art · run 11

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 11 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | Step 7 rule-unit spike (session log to follow) |
| Previous card for this stage | [Run 10](2026-11-02-review-run10.md) |

## Run

- **Inputs:** the uncommitted [prior-art.md](../../spikes/rule-units/prior-art.md); REVIEW.md; the brief, backlog T6 and D1, ADR-009, -011, -012, -015 and -016, the constitution tests and fixtures; Andy's approvals quoted word for word; the eleven documentation URLs, which the reviewer fetched itself rather than trusting the author's summary.
- **Cost:** about 5 minutes (298 s), about 114,000 tokens, 27 tool calls.
- **Result:** 1 High, 3 Medium, 11 Low, 5 nits.

## What it found

- **High:** the ADR-015@v1 C2 rubric dropped a condition. It checked that each rule *had* a check, not that all five rules *held*. A dropped condition again, as in earlier runs.
- **Medium:** what reaches `analyze` in the f8 re-run was unclear (findings would only test repetition); the document silently settled a conflict in T6 between deterministic loading and model-selected judgement rules; "SARIF 2.1.0" was untraced.
- **Low, among others:** "self-reported" dropped from a results quote; a hypothesis stated as a finding; installing adrkit's extension means revising ADR-009, not just a new ADR; criterion 7 (an index) wasn't met by the design; uneven near misses; Spec Kit's own `before_analyze` hook point was missing from the delivery options.
- All external tool claims checked out against the current pages.

## Responses

All accepted and fixed in the document: the rubric follows both of C2's conditions; question 3 says the unit's text reaches `analyze`, not the check's findings; questions 6 and 7 put the T6 conflict and the SARIF version to Andy; an `index.yaml` is added; every unit gets a near miss; `before_analyze` is a delivery option, verified in `.claude/skills/speckit-analyze/SKILL.md` lines 24 to 56. The "small fake `subject/eshop`" now lives in the unit's fixtures, away from the protected `subject/` path.

Author-scored. Not independent.

## What the run showed

Giving the reviewer the URLs, not the author's summaries, worked: it verified every tool claim and found one option the author missed. The High was a dropped condition, the most common finding across runs. An ADR-writing skill that copies conditions clause by clause (Step 7 item 5) would address it.

## Measurements

Wall time about 5 minutes; about 114,000 tokens.

**Not re-reviewed:** the fixes.
