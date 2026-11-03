# Loop card: implement · a separate ADR-016@v2 C17 unit · rule-unit spike · run 6

| Field | Value |
| --- | --- |
| Stage | Implement (spike unit) |
| Outcome | None: project work, Step 7 item 1 (T6) |
| Run | 6 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [SARIF 2.1.0 check, run 5](2026-11-03-rule-units-sarif-check-run5.md) |

## 1. Purpose

Give C17 its own unit, so a C17 finding comes with the rule's text, and return the C10 unit to C10 only.

## 2. Trigger and inputs

- **Trigger:** Andy, 3 Nov: "add a separate C17 unit".
- **Inputs:** ADR-016@v2 C17; the C10 unit and its tests; run 5's open failure.

## 3. Actor

The author (Claude Opus 5.5), in this worktree.

## 4. What happened

1. The C17 unit's identity (`unit.yaml`), nine cases and three plan fixtures written and committed first (`aba7784`). All C17 cases failed there, because `check.py` didn't exist yet.
2. `check.py` written: plan and analyze text naming a SARIF version other than 2.1.0, and SARIF files whose `version` isn't 2.1.0.
3. The C10 check and description restored to C10 only. Its two C17 cases kept, marked `superseded` with a dated note; two new C10 cases expect the 1.0.0 and 2.2 files to pass C10. The harness gained `superseded`, with a test.
4. M4's "seven units" test changed to eight, with a dated note in server-expected.md. index.yaml regenerated. ADR-016's C17 `ref` moved to the new check (no version bump, ADR-000@v3 C8).
5. After review run 20: `superseded` names that match no case, and duplicate names, now stop the run; the plan-text pattern's misses written into `describes`, the code comment and results.md.

## 5. Feedback loop

- **Signal:** pytest. **Stop condition:** all cases as expected. **Iterations:** 2 (M4's count, then review fixes).

## 6. Output

- `units/adr-016-c17/`; results in [results.md](../../../spikes/rule-units/results.md), "A separate C17 unit".

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| C17 cases fail first | Deterministic | All fail at `aba7784` | Pass, but by a missing file, not a mismatched result (review run 20) |
| All cases after the change | Deterministic | Pass, todo as xfail, superseded as skip | 65 passed, 2 skipped, 4 xfailed |
| ADR change is `ref` only | Review | ADR-000@v3 C8 | Pass (review run 20) |

## 8. Gate

- **Approver:** Andy. **Decision:** pending his local review.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Tests | 65 passed, 2 skipped, 4 xfailed (was 54 and 3 xfailed at run 5) | pytest |
| Wall time | Not measured | |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| Run 5's gap: a C17 finding named a rule whose text the agent never got | One unit, one citation | Separate C17 unit | `units/adr-016-c17/` | No |
| M4 asserted seven units | M4 was pre-registered before C17 | Dated note; test says eight | server-expected.md, test_server.py | Fill in on the next card |
| The plan-text pattern misses common forms and gives one false finding | Pattern written to the cases, not to how people write versions | Recorded, not fixed | results.md, `describes` | Fill in on the next card |
| ADR-016's Enforcement prose is out of date | Changing it needs a new version | Not fixed; needs Andy | results.md | Fill in on the next card |

## 11. Ready to automate?

- [ ] Real producer output and real plans as fixtures
- [ ] Plan-text pattern tested on how versions are actually written

**Verdict:** keep at level 1.
