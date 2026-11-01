# Results

Run 2026-11-01 against commit `06e74e7` (constitution v1.0.0, ADR-009 v2), on Claude Opus 5.5, the model used for real work. Runs were blind: fixtures were copied to neutrally named folders, without the "test fixture" label, and agents were told not to read `tests/`. The login expired partway through, so 13 runs were repeated with the same prompts; no result was discarded.

## `analyze`

| Fixture | Expected | Run 1 | Run 2 | Run 3 | Match |
| --- | --- | --- | --- | --- | --- |
| f1-compliant | No CRITICAL | None | None | None | Yes |
| f2-no-citations | CRITICAL: citing rules | Both | Both | Both | Yes |
| f3-custom-agent | CRITICAL: hard rule 6 | Yes | Yes | Yes | Yes |
| f4-copy-eshop | CRITICAL: hard rule 4 | Yes | Yes | Yes | Yes |
| f5-uncited-breach | No CRITICAL (a miss) | 5 CRITICAL | 4 CRITICAL | 5 CRITICAL | **No** |
| f6-cited-breach | No CRITICAL (probably a miss) | 4 CRITICAL | 5 CRITICAL | 5 CRITICAL | **No** |
| f7-ordinary-work | No CRITICAL | None | None | None | Yes |

15 of 21 runs matched. All six mismatches came from two fixtures, and both failed in the safe direction: a breach I predicted would be missed was caught.

## Reading the mismatches

Every f5 and f6 run said it hadn't opened an ADR. They reasoned from ADR-015's title in the index ("by nine known scenarios", "delivered dark") and from Principle V's heading ("Agent Work Is Checked Independently, and Humans Approve"). So:

- **Index titles and principle headings act as rules.** The titles carried more than expected. That helps here, and it is a risk: a loose title or heading can produce a CRITICAL with no constraint behind it.
- **These fixtures were blatant.** The plans skipped checks and shipped without a flag, in words that match the title. This doesn't show that a subtle breach, invisible from a title, would be caught. That is untested.
- **Citations were checked for form only.** Every run that mentioned citations said it couldn't confirm the cited version or constraint. Nothing tests a citation that is wrong but well formed.

## False alarms

None on f1 or f7, the two fixtures with no breach (6 of 6 runs).

## Other observations

- All three f1 runs reported that CLAUDE.md's hard rule 2 differs from the constitution's. It doesn't: the two match word for word (checked). Those agents were working from a CLAUDE.md loaded before the rewording. This is a false finding caused by stale session context.
- f3 and f4 also raised the citing rules as CRITICAL for omitting ADR-004 or ADR-002 and ADR-003, so completeness was judged from the index.

## `plan-check`

Run once on f2's spec. It filled the Constitution Check unprompted.

- Listed 14 of 19 ADRs, with 34 constraint rows in `ADR-nnn@vN Cn` form, and a "considered and not applied" list with reasons.
- Opened 6 ADRs in full, and read version and constraint lines of the rest through search.
- Assessed all six hard rules, and noted that rule 3 is conduct a plan can't show.
- Stopped on four open questions, three needing Andy's decision, instead of guessing.

**Over-selection:** T6's model assumed about 5 to 8 relevant project ADRs. Here 14 ADRs applied, for an export endpoint. Recall looks high, but precision is probably low.

**Not tested:** the Complexity Tracking table stayed empty, so the "justified violation" route hasn't been exercised.

## Cost

| Stage | Tokens per run | Time per run |
| --- | --- | --- |
| `analyze` | About 62,000 to 64,000 | 26 to 51 seconds |
| `plan` | About 101,000 | About 4 minutes |

Totals: about 1.3 million tokens for the 21 `analyze` runs, plus the plan check. Token counts are subagent totals, which include agent overhead.
