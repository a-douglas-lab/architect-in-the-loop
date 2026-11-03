# Loop card: review · ADR-016 v2 and the SARIF version check · run 19

| Field | Value |
| --- | --- |
| Stage | Review (ADR revision, spike code and documentation) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 19 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 18](2026-11-03-rule-units-review-run18.md) |

## Run

- **Inputs:** commit `6774fb8` (cases written first) and the uncommitted diff on it (ADR-016 v2, check.py, unit.yaml, backlog T6, results.md, the session log); REVIEW.md; CLAUDE.md; ADR-000; Andy's "yes, do both." and the question it answered.
- **What the reviewer re-ran:** pytest (54 passed, 3 xfailed); the old check.py from a scratch copy against the two new files (no finding, so both cases failed first).
- **Cost:** 376 s harness duration, about 78,000 tokens, 9 tool calls.
- **Result:** 0 High, 2 Medium, 4 Low, 2 nits.

## What it found

- **Medium:** the Decision prose added a rule not in C17 ("a later change of version moves every producer and the baseline together"), which Andy didn't approve. "The only approved SARIF specification" dropped the backlog's "found".
- **Low:** C10's enforcement `ref` was null while C17's pointed at the same file; a C17 finding names a rule whose text the agent never gets; "tested on … a 2.2 draft" hid that the files are hand-written or invented; expected.yaml's header doesn't say new cases may be added.
- **Nits:** "version 2.1" beside "2.1.0"; a long History line.
- **Checks that held:** ADR-000@v3 C1, C5, C6, C8, C9, C11; `date` unchanged, as the template defines it; the order of work; the harness change weakens no existing case; citation versions consistent; backlog edits inside T6.

## Responses

All accepted. The extra rule is gone from the Decision; Consequences describes a future version change as a revision of C17. "The only OASIS Standard version of SARIF found", with the 2.2 draft noted. C10's `ref` set (no version bump needed for `ref`, ADR-000@v3 C8). The Enforcement note names the three test files for what they are. results.md discloses the citation gap and how the cases were added. History line shortened; the Roslyn switch written as `version=2.1`.

Author-scored. Not independent.

## What the run showed

Reasoning recorded beside a decision travelled into the ADR as a rule. Separating the decided constraint from its reasons, as in run 18, needed doing again at the ADR stage.

## Measurements

Harness duration 376 s; about 78,000 tokens.

**Not re-reviewed:** the fixes.
