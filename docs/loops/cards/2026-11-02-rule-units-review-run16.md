# Loop card: review · Andy's harness-hook confirmation · run 16

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 16 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 15](2026-11-02-rule-units-review-run15.md) |

## Run

- **Inputs:** the uncommitted diff on `32df293` (backlog T6, delivery.md, the session log); REVIEW.md; Andy's reply, word for word: "yes, harness hook is right".
- **Cost:** 281 s harness duration, about 64,000 tokens, 2 tool calls.
- **Result:** 0 High, 1 Medium, 1 Low, 2 nits.

## What it found

- **Medium:** delivery.md dropped the "author's reading" label from "not by the model's choice" as well as from "harness hook"; Andy confirmed only the second.
- **Low:** removing "on the author's reading" from "Not chosen" holds only if the question to Andy named the skill and `before_analyze`. It did: the question said "not a skill or Spec Kit's `before_analyze` hook, since both of those leave it to the model to decide whether to run it".
- **Nits:** "Moved into T6's Decided list" (it was already there, labelled); a hard-to-parse sentence in delivery.md.
- **Checks that held:** the quote is exact in all three files; the only backlog change is inside T6; no leftover "to confirm" on the hook point; the A1 rationale and the adrkit and SARIF choices are still marked not ruled.

## Responses

All accepted. delivery.md labels "not by the model's choice" as the author's wording of the intent and splits the sentence; the session log says "relabelled" and records the question's wording.

Author-scored. Not independent.

## What the run showed

Removing a label when one of two labelled points is confirmed took the other point with it. The label should cover one claim, so it can be removed one claim at a time.

## Measurements

About 64,000 tokens; 2 tool calls.

**Not re-reviewed:** the fixes.
