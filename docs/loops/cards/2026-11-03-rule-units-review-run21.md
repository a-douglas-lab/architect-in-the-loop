# Loop card: review · ADR-016 v3 correction · run 21

| Field | Value |
| --- | --- |
| Stage | Review (ADR correction and documentation) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 21 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 20](2026-11-03-rule-units-review-run20.md) |

## Run

- **Inputs:** the uncommitted diff on `58b588c` (ADR-016 v3, results.md, the session log); REVIEW.md; ADR-000; Andy's "yes, write v3" and the question it answered.
- **What the reviewer re-ran:** nothing executable; read-only checks against the C17 unit's files, ADR-000 and the repo's citations.
- **Cost:** harness duration 169 s, about 84,000 tokens, 6 tool calls.
- **Result:** 0 High, 1 Medium, 3 Low, 2 nits.

## What it found

- **Medium:** the mechanism and History line said "plans"; the check reads spec, plan and tasks at the plan and analyze stages.
- **Low:** "plan cases are written for the spike" was wrong (one uses a constitution fixture); the file cases are four, not three (the same miscount that made v2 stale); results.md stated a citation rule no ADR records.
- **Nits:** a present-tense "is out of date" beside "fixed"; a long Enforcement paragraph.
- **Checks that held:** a correction, not a revision (no constraint changed; the plan-text check traces to backlog T6); `date` unchanged, as the template defines it; the approval quote exact; History line well formed; nothing else needs to say v3.

## Responses

All accepted, within v3 (not yet committed when found): "spec, plan and tasks" in the mechanism, the prose and the History line; four file cases named; "text cases use spike and constitution fixtures"; the citation described as the repo's practice, not a rule; past tense in results.md; the paragraph split into shorter sentences.

Author-scored. Not independent.

## What the run showed

A correction written to fix a miscount repeated a miscount. Counting from the file, not from memory, is the check.

## Measurements

Harness duration 169 s; about 84,000 tokens.

**Not re-reviewed:** the fixes.
