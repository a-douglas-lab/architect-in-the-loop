# Loop card: review · recording Andy's T6 decision · run 15

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 15 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 14](2026-11-02-rule-units-review-run14.md) |

## Run

- **Inputs:** the uncommitted diff on `68e25e0` (backlog T6, delivery.md, the spike README, the session log); REVIEW.md; CLAUDE.md; Andy's two messages, word for word, including "yes, one recommendation with the server built now. document the decision so we don't lose track of it later." Asked to judge recording the decision as T6 "Partly decided" rather than writing an ADR now.
- **Cost:** 281 s harness duration, about 80,000 tokens, 5 tool calls.
- **Result:** 2 High, 3 Medium, 4 Low, 5 nits.

## What it found

- **High:** "a harness hook" and "not a skill or `before_analyze`" were the author's reading, filed in the Decided list; Andy wrote "a hook/orchestrator". "Not by a model" overstated the ruling: the translator into glossary terms is a model; only the selection after it is deterministic.
- **Medium:** the A1 rationale sat under delivery.md's new "Decision" heading; T6's Open list left out the rest of T6's scope (storage, referencing, keeping current, conflict detection); three T6 lines were stale ("how ADRs are selected is still open", the four-routes table "(proposed)", "awaiting Andy's review").
- **Low:** spike follow-ups missing from Open (authoring at scale, CUE, the subject glossary from the fork, a second labeller, wiring approval); the key file line didn't say a OneDrive copy may survive; the options table's tool list didn't match the built server.
- **On the choice:** defensible under the backlog legend and "each item closes with a short ADR", with A1 as precedent; but CLAUDE.md's "Every decision becomes an ADR" has no condition, and Andy should know the choice leans on the timing sentence.
- **Checks that held:** quotes exact; backlog edits inside T6 only; no "recommended, not decided" wording left; unruled items consistent across files; delivery.md keeps "intent, not yet a property".

## Responses

All High, Medium and Low findings accepted and fixed in backlog T6, delivery.md and the session log. The harness-hook reading is now its own bullet, labelled as the author's, to confirm before the ADR. Nits 1, 2 and 4 fixed; nit 3 (backlog's status date) left, as outside T6; nit 5 left, since the key line now carries an open action.

The reviewer said "docs/adr/ is protected" isn't established, citing ADR-011; backlog D1 records the protected paths as decided on 2 Nov. That reason appears in no committed file.

Author-scored. Not independent.

## What the run showed

Reading a confirmation of one point as confirming its neighbours recurred from runs 11 to 13. Splitting each Decided bullet into Andy's words and the author's reading made it visible.

## Measurements

Harness duration 281 s; about 80,000 tokens.

**Not re-reviewed:** the fixes.
