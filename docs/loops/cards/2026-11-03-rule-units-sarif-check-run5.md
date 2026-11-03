# Loop card: implement · SARIF 2.1.0 check and ADR-016 v2 · rule-unit spike · run 5

| Field | Value |
| --- | --- |
| Stage | Implement (spike check) and ADR revision |
| Outcome | None: project work, Step 7 item 1 (T6) |
| Run | 5 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Live hook run, run 4](2026-11-02-rule-units-live-hook-run4.md) |

## 1. Purpose

Apply the SARIF 2.1.0 decision: pin it in ADR-016, and make the spike's C10 unit report other versions.

## 2. Trigger and inputs

- **Trigger:** Andy, 3 Nov: "yes, do both."
- **Inputs:** the decision in backlog T6; ADR-016@v1; the C10 unit and its tests.

## 3. Actor

The author (Claude Opus 5.5), in this worktree. Andy approved the revision in chat.

## 4. What happened

1. Two cases added to the unit's `tests/expected.yaml`, with fixture files (a 1.0.0 file in Roslyn's shape, an invented 2.2 file), and an optional `rule` field in the test harness. Run: 2 failed, 52 passed, 3 expected failures. Committed first (`6774fb8`).
2. check.py reports a SARIF version other than 2.1.0 as a finding citing ADR-016@v2 C17; unit.yaml's description updated. Run: 54 passed, 3 expected failures.
3. ADR-016 v2: C17 added, with its enforcement entry, the reasons in the Decision, a Consequences line, the Enforcement note and a History line.

## 5. Feedback loop

- **Signal:** pytest. **Stop condition:** all cases as expected. **Iterations:** 1.

## 6. Output

- check.py, unit.yaml, ADR-016 v2; results in [results.md](../../../spikes/rule-units/results.md), "SARIF version check".

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| New cases fail first | Deterministic | Both fail against the old check | Pass (and confirmed by the reviewer from a scratch copy) |
| All cases after the change | Deterministic | 54 passed, 3 xfailed | Pass |
| ADR-000@v3 rules | Review | C1, C5, C8, C9, C11 | Pass (review run 19) |

## 8. Gate

- **Approver:** Andy. **Decision:** pending his local review.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Tests | 54 passed, 3 expected failures (was 52 and 3) | pytest |
| Wall time | Not measured | |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| A C17 finding names a rule whose text the agent never gets | The unit carries one citation | Not fixed; a separate C17 unit would close it | results.md | Fill in on the next card |

## 11. Ready to automate?

- [ ] Real producer output: the 1.0.0 file is hand-written, the 2.2 file invented

**Verdict:** keep at level 1.
