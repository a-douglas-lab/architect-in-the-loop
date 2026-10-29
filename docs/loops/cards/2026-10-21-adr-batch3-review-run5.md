# Loop card: review · ADR batch 3 · run 5

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 5 batch 3 (ADR-009 to ADR-013) |
| Run | 5 |
| Date | 2026-10-21 |
| Autonomy level | 1, drafted |
| Session | [Session 03 log](../../sessions/2026-10-21-session-03.md) |
| Previous card for this stage | [Runs 3 and 4](2026-10-21-review-runs3-4.md) |

**The first run under "no push before review" (ADR-013@v1 C5).** The branch was reviewed locally, never pushed. This card is where Andy reads the findings during his local review (ADR-012@v1 C6).

## Run

- **Inputs:** the diff `main..b1915ce` (local branch `docs/adr-batch-3-ways-of-working`); REVIEW.md; six approvals quoted word for word.
- **Reviewer:** a general-purpose subagent with a fresh context, on the same model as the author. It was read-only, barred from the evaluation repo, and allowed to read three Claude Code documentation pages and `gh api`.
- **Cost:** about 5 minutes (302 s), about 122,000 tokens, 32 tool calls.
- **Result:** 2 High, 6 Medium, 10 Low, 5 nits, and a note on the decisions.

## Findings and responses

| # | Sev | Finding | Response |
| --- | --- | --- | --- |
| 1 | High | ADR-013: the planned "require a PR" rule is filed under C5, which a PR rule can't enforce; C6 has no planned mechanism | Accept. Moved to C6 (planned) |
| 2 | High | ADR-011@v1 C6: "reads and edits" and the rule types are untraced | Accept, with a trace: Andy asked on 20 Oct to "add the deny rules for the eval repo", and both rules were added. The request is now quoted in the ADR |
| 3 | Med | ADR-009: bootstrap "warns but doesn't fail" is false; it exits 2 | Accept. Verified in `bootstrap.ps1` lines 45–46 and 64–66. The author had read only the matching lines. Corrected, and the session log too |
| 4 | Med | ADR-013@v1 C6 ("only a PR Andy merges") untraced | Andy's ruling (21 Oct), recorded |
| 5 | Med | "Protected paths" is defined nowhere | Accept. Recorded as open under D1; ADR-011 says so |
| 6 | Med | ADR-010@v1 C6: "monitored" is undefined; the mechanism "none yet" is misleading | Accept. The mechanism is what exists (loop cards record tokens per run); the budget is open |
| 7 | Med | ADR-009@v1 C4 adds an untraced mechanism and overlaps C5 | Accept. C4 restated as the source ("core only"), with changes as a revision under ADR-000@v3 C11 |
| 8 | Med | ADR-009@v1 C6's "after merge" trigger is untraced | Accept. Trigger removed; the rule for when a folder becomes fixed is noted as undecided; the state is now manual |
| 9 | Low | ADR-010's "single track in one session" is inaccurate; C2 is unmet | Accept. Reworded: no work has run in a worktree yet |
| 10 | Low | ADR-009@v1 C2's "revision" not attributed | Accept. Cites ADR-000@v3 C8 and C11 |
| 11 | Low | ADR-011 misses "no prompt to click through", the D1 open items and the setting's minimum version | Accept. All added |
| 12 | Low | ADR-012 omits the lighter-card open item | Accept. Added |
| 13 | Low | ADR-013 overclaims "nothing reaches GitHub without review"; C4's ref names one repo | Accept. Consequence softened; both ruleset IDs in the mechanism |
| 14 | Low | ADR-013 has no "do nothing" option for the push rule | Accept. Added |
| 15 | Low | ADR-009@v1 C4's planned check wouldn't detect presets | Accept. Mechanism notes the detection method is to be confirmed |
| 16 | Low | ADR-010@v1 C3's configuration mostly doesn't exist yet | Accept. Stated in Enforcement |
| 17 | Low | ADR-013 "agents write most of the changes" is unmeasured | Accept. Now "many of the changes"; the working rule's location is named |
| 18 | Low | ADR-012@v1 C4 "before Andy reviews it" is inferred | Now traced: Andy's ruling puts findings on the card for his local review |
| Nits | — | Contradictory enforcement line; "three mechanisms" then a fourth; an alternative marked as added though D1 weighed it; token range; "contradicts the thesis" | All fixed |

Author-scored: 18 of 18 real (2 with an added trace or ruling). Not independent.

## The note on the decisions, and what came of it

The reviewer noted that ADR-012 put findings in the PR description, but under "no push before review" no PR exists when Andy reviews. Andy also asked whether the rule survives loop automation. It doesn't: it would put him back in every inner loop, and put his review before the deterministic checks. His rulings:

- the push rule applies **while stages are hand-run** (level 2 or below);
- ADR-013 must be revised before any stage goes higher (ADR-012@v1 C9, ADR-013@v1 C7);
- the automated gate is a new open item, **D8**;
- findings go on the loop card first, then into the PR.

## Measurements

| Run | Wall time | Tokens | High | Total findings |
| --- | --- | --- | --- | --- |
| 1 | 27 min | 114k | 3 | 20 |
| 2 | 6.5 min | 116k | 3 | 16 |
| 3 | 6 min | 98k | 4 | 13 |
| 4 | 13 min | 114k | 1 | 18 |
| 5 | 5 min | 122k | 2 | 18 |

## What went wrong

| Failure | Root cause | Fix | Where the fix landed |
| --- | --- | --- | --- |
| A second factual error by the author (bootstrap behaviour) | Read the lines that matched a search, not the surrounding control flow | Corrected | ADR-009, session log. Process fix still none; same pattern as run 3's missed setting |
| A rule written without asking whether it scales | The D7 ruling was recorded as permanent | Scoped, with a revision trigger | ADR-013@v1 C7, ADR-012@v1 C9, D8 |

## Ready to automate?

Unchanged: keep at level 1. **Not re-reviewed:** the changes made after this review are Andy's rulings and the fixes above.
