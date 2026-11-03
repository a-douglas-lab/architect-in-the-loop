# Loop card: review · Andy's adrkit decision · run 17

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 17 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 16](2026-11-02-rule-units-review-run16.md) |

## Run

- **Inputs:** the uncommitted diff on `9d729ed` (backlog T6, prior-art.md, the session log); REVIEW.md; the exchange word for word: Andy's "didn't you state adrkit didn't cover our requirements?", the author's question, and Andy's "yes, record it as decided".
- **Cost:** 535 s harness duration, about 67,000 tokens, 5 tool calls.
- **Result:** 0 High, 0 Medium, 3 Low, 1 nit.

## What it found

- **Low:** "Borrowed: …" listed specific shapes in the past tense, as if done and as if Andy had approved each; only the MCP server shape exists. Only ADR-009@v2 C4 was cited, where the sources also cite C5. prior-art.md's status line didn't show the file changed after run 12.
- **Nit:** the session log's sentence put the exchange out of order.
- **Checks that held:** quotes exact; the README-only caveat survives; the three gaps match prior-art.md; no adrkit contradiction left across backlog, the spike files and the session log; expected.md states every choice still listed as not ruled; backlog edits inside T6.

## Responses

All accepted and fixed: "Shapes to borrow, listed in prior-art.md … only the last is built so far"; C5 added; prior-art.md's status line notes the later rulings; the session log's exchange put in order.

Author-scored. Not independent.

## What the run showed

A list of details beside an approval reads as approved detail. Pointing to the source list, rather than restating it as done, keeps the decision at the level Andy ruled.

## Measurements

Harness duration 535 s; about 67,000 tokens.

**Not re-reviewed:** the fixes.
