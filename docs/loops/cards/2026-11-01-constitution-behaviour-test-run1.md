# Loop card: analyze and plan · constitution behaviour test · run 1

| Field | Value |
| --- | --- |
| Stage | Analyze and plan, run against test fixtures |
| Outcome | None: project work, Step 6 |
| Run | 1 |
| Date | 2026-11-01 |
| Autonomy level | 1, drafted |
| Session | [Session 05 log](../../sessions/2026-11-01-session-05.md) |
| Previous card for this stage | First run |

## Purpose

This run checks that the constitution makes Spec Kit behave as ADR-009 intends. Andy asked for it before any PR: "as with any capability shouldn't we add tests, validate the behaviour".

## What happened

1. Author wrote seven fixtures and the expected results, and committed them before any run (`06e74e7`).
2. Author noticed that folder names would give away the answers, so copied the fixtures to neutral names without the "test fixture" label.
3. 22 fresh-context agents ran. Nine `analyze` runs finished, then the login expired and 13 failed. After sign-in, those 13 ran again with the same prompts.
4. Author recorded the results in [results.md](../../../tests/constitution/results.md), and updated ADR-009 from predictions to observations.

## Result

Run A: 15 of 21 `analyze` runs matched expectation. The six mismatches were f5 and f6, where blatant breaches were caught when a miss was predicted. No false CRITICAL on compliant work, but all three f1 runs raised one false finding. `plan` filled the Constitution Check unprompted, listing 14 of 19 ADRs.

Run B (2 Nov), after the review and Andy's rulings: f8, a breach no title reveals, was missed 3 of 3 as predicted. f9, a misleading title, matched 1 of 3: ADR-011's title produced a contested CRITICAL in two runs.

Full results: [results.md](../../../tests/constitution/results.md).

## What the run showed

- **Testing replaced guesses.** ADR-009's "unproven" and "predicted" lines now state what was seen. Two predictions were wrong.
- **The surprise matters more than the pass.** Index titles and principle headings act as rules. Nothing tested this before the run, and it cuts both ways.
- **The fixtures have a gap.** f5 and f6 are blatant. Subtle breaches, wrong citations and the Complexity Tracking route are untested.
- **Agents can trust stale context.** All three f1 runs reported a false mismatch from a CLAUDE.md loaded before the rewording.

## Measurements

About 63,000 tokens and under a minute per `analyze` run; about 101,000 tokens and 4 minutes for `plan`. About 1.4 million tokens in total.

## What went wrong

| Failure | Root cause | Fix | Where the fix landed |
| --- | --- | --- | --- |
| Fixture names leaked the answers | Named for the author's convenience | Copied to neutral names for the run | The README's method |
| 13 runs lost to an expired login | Long batch, no check before starting | Re-run | Nowhere yet |
| The first write-up claimed more than the runs showed | Author summarised from memory of the reports | Review run 10 (15 High); rewritten as rates | results.md, ADR-009, backlog |

This card leaves out several template sections, including the leading and lagging indicators ADR-012@v2 C3 asks for. Earlier review cards lack them too. To fix when the stage cards are next revised.

## Ready to automate?

Not yet. It needs a script that makes the neutral copies, and fixtures for the gaps above. It is a model following instructions, so results are evidence, not a gate.

**Next run changes:** add wrong-citation and justified-violation fixtures (Step 7, VL-2); commit prompts and reports; re-run when the constitution, CLAUDE.md or the skills change.
