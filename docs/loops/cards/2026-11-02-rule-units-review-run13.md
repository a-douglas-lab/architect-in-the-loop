# Loop card: review · rule-unit MCP server · run 13

| Field | Value |
| --- | --- |
| Stage | Review (documentation and spike change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 13 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 12](2026-11-02-rule-units-review-run12.md) |

## Run

- **Inputs:** commits `c7b89cb` (Andy's rulings, the agentic-DDD check, the pre-registration) and `5da0081` (the joined step, the MCP server, results, the build card); REVIEW.md; CLAUDE.md; Andy's message and his three build choices, quoted word for word. The reviewer fetched the two agentic-DDD sources, the codebook's glossary and the hooks reference itself.
- **What the reviewer re-ran:** pytest (49 passed, 3 expected failures, as reported); `anthropic.Anthropic()` with no credentials; a diff over every protected path (empty).
- **Cost:** 592 s harness duration, about 106,000 tokens, 15 tool calls.
- **Result:** 0 High, 3 Medium, 7 Low, 4 nits.

## What it found

- **Medium:** the agentic-DDD section borrowed the codebook's "translation token table" as a map between contexts; it maps internal terms to customer-facing wording, and the cross-context map is its anti-corruption layer. The build card blamed a bug the SDK can't produce (2.3.0 builds a client without credentials). The session log filed the author's reading of "this feels like a roadmap you decided" under Decided.
- **Low:** the backlog's four-routes table still said the model selects judgement rules; "end to end" unqualified in the session log; the run instructions didn't flag `tool_input.skill` as assumed, nor warn that typing `/speckit-analyze` bypasses `PreToolUse`; the context's shortening branch was untested and could exceed 10,000 characters; "two misses" listed one; a paraphrase of the steward article; "never by the model's choice" claimed of a server whose other tools the model can call.
- **Checks that held:** ordering (expectations and tests before code; J3's change legitimate and disclosed), test counts, protected paths, no key in a file, feature resolution matching Spec Kit's script, the hook-doc claims.

## Responses

All accepted. Fixed in prior-art.md, delivery.md, results.md, hook/README.md, the build card, the session log, backlog T6's table, `join.py` and its tests:

- The borrow is now the vocabulary lock and the anti-corruption layer, quoted from the codebook's glossary.
- The card's row says the bug was a misreading; J6b is kept and labelled defensive.
- The roadmap reading is labelled as mine, for Andy to confirm, in the session log and delivery.md.
- The shortening branch is fixed and has three tests; pytest is now 52 passed, 3 expected failures.
- delivery.md says "not by the model's choice" is intent until the wiring hides `get_rules` and `index` from the model.
- **Not fixed:** the unversioned "ADR-012" in server-expected.md, because that file is pre-registered and isn't edited after a run. It is ADR-012@v2 C10.

Author-scored. Not independent.

## What the run showed

Fetching the source behind the author's summary caught a misread borrowing, as in run 11. An interpretation of Andy's words filed as a decision recurred from runs 11 and 12; a rule to quote and label any reading of an approval, rather than restate it, would catch it.

## Measurements

Harness duration 592 s; about 106,000 tokens.

**Not re-reviewed:** the fixes.
