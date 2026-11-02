# Loop card: review · rule-unit live hook run · run 14

| Field | Value |
| --- | --- |
| Stage | Review (documentation change and raw evidence) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 14 |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 13](2026-11-02-rule-units-review-run13.md) |

## Run

- **Inputs:** commit `9e2c508` (the live hook run: results, delivery, the hook README, the run 4 card, the session log, backlog T6, and the raw files under `spikes/rule-units/runs/live/`); REVIEW.md; CLAUDE.md; Andy's two messages, word for word; the pre-registered L1 to L4. Told not to read the key file.
- **What the reviewer did:** scored L1 to L4 from the raw JSONL itself, checked every number against the transcripts, searched the committed files for key-like strings (none), and diffed the protected paths (empty).
- **Cost:** 209 s harness duration, about 107,000 tokens, 12 tool calls.
- **Result:** 0 High, 2 Medium, 6 Low, 2 nits.

## What it found

- **Medium:** the blindness confound was understated: the worktree's folder name is in every path the session saw, so the proposed fix (move the feature folder) wouldn't make the run blind. The translator's extra terms were called "the same false selection the spike found"; the cause differs (wrong terms here, coarse applicability there).
- **Low:** two `ls` commands also ran and one Bash call was denied, against "the only allowed shell command"; summary lines dropped "inferred", "unblind" and "one run"; durations didn't match `duration_ms`; the README still said the key never goes in a file; run 1's model knew the hook's name from the tool list; "known cost" ticked without the translator's cost.
- **Checks that held:** L1 timing (the hook's 8.04 s fits the gap between the Skill call and "Launching skill"); L2's inference, which it found stronger than stated (C10 quoted word for word with ADR-016 never opened); costs, terms, units and the finding; run 1 fairly called a setup failure; no key in any committed file; no protected path changed.

## Responses

All accepted and fixed in results.md, the run 4 card, the hook README and backlog T6. The exact command is recorded; L2 now cites the word-for-word quote; durations use `duration_ms`; the next run needs a checkout whose path doesn't name the spike.

Author-scored. Not independent.

## What the run showed

Scoring from the raw transcripts found what the prose summary hid: commands the permission system let through, and a confound bigger than the one written down. Raw evidence committed beside the summary made both checkable.

## Measurements

Harness duration 209 s; about 107,000 tokens.

**Not re-reviewed:** the fixes.
