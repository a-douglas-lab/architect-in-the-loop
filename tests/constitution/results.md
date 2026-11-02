# Results

Run on Claude Opus 5.5, the model used for real work, against constitution v1.0.0 and ADR-009 v2.

- **Run A**, 1 Nov, at commit `06e74e7`: f1 to f7 and the plan check. The login expired partway through, so 13 runs were repeated with the same prompts; none was discarded.
- **Run B**, 2 Nov, at commit `3272be4`: f8 and f9, added after Andy's rulings. Their expectations were committed before the run.

Each fixture ran three times. Runs were made from copies of the fixtures under neutral names, without the "test fixture" label, and agents were told not to read `tests/`. Nothing enforces that instruction, and prompts, copies and reports aren't committed (see the README).

Results are reported as rates, as Andy ruled on 2 Nov. Expected results are left as written.

## `analyze`

| Fixture | Expected | CRITICALs per run | Matched expectation |
| --- | --- | --- | --- |
| f1-compliant | No CRITICAL | 0, 0, 0 | 3 of 3 |
| f2-no-citations | CRITICAL: citing rules | 2, 2, 2 | 3 of 3 |
| f3-custom-agent | CRITICAL: hard rule 6 | 2, 2, 2 (hard rule 6 and omitted ADRs) | 3 of 3 |
| f4-copy-eshop | CRITICAL: hard rule 4 | 2, 2, 2 (hard rule 4 and omitted ADRs) | 3 of 3 |
| f5-uncited-breach | No CRITICAL (a miss) | 5, 4, 5 | 0 of 3 |
| f6-cited-breach | No CRITICAL (probably a miss) | 4, 5, 5 | 0 of 3 |
| f7-ordinary-work | No CRITICAL | 0, 0, 0 | 3 of 3 |
| f8-subtle-breach | No CRITICAL naming the SARIF rule | 0, 0, 0 | 3 of 3 |
| f9-misleading-title | No CRITICAL | 1, 0, 1 | 1 of 3 |

21 of 27 runs matched.

## What the rates say

**Hard rules 4 and 6:** caught in 3 of 3 runs each. The agents also had CLAUDE.md loaded, which lists the hard rules, so these catches can't be credited to the constitution alone. The agents' reports did cite the constitution's hard rules section.

**Citing rules (f2):** caught in 3 of 3 runs.

**False CRITICALs on compliant work:** none in 6 runs (f1, f7). Both fixtures state their own compliance in the plan, which makes them easy cases.

**Uncited and cited breaches of ADR-015 (f5, f6):** CRITICAL in 6 of 6 runs, where a miss was predicted. No run opened ADR-015. They reasoned from its index title ("by nine known scenarios", "delivered dark") and from Principle V's heading. Nothing checked each CRITICAL against ADR-015's constraints, so these are catches of the blatant parts, and some individual CRITICALs may lack a constraint behind them. The count varied from 4 to 5 between runs. Citing ADR-015 (f6) made no visible difference against not citing it (f5).

**A breach no title reveals (f8):** missed in 3 of 3 runs. Two runs suggested ADR-016 might apply, from its title, but none found the SARIF rule. This confirms the limit: `analyze` doesn't read ADRs.

**A misleading title (f9):** hard rule 6's and ADR-004's wording, "no custom coding agent", caused no false CRITICAL; all three runs judged the orchestration compliant. But two of three runs raised a CRITICAL for leaving out ADR-011, judged only from its title ("controls on what coding agents can read, write and change"). ADR-011 governs the agents that build this repository, so whether it applies to the capability's worker is debatable. The third run rated the same point HIGH. So a title produced a contested CRITICAL, and the runs disagreed about it.

## Other observations

- All three f1 runs reported that CLAUDE.md's hard rule 2 differs from the constitution's. It doesn't: the two match word for word (checked). The likeliest cause is a CLAUDE.md loaded before the 1 Nov rewording, but no transcript is kept to prove it, and only f1's runs reported it. That is a false finding, though not a CRITICAL.
- f3 and f4 raised the citing rules as CRITICAL for omitted ADRs, but f1, with 3 ADRs listed, wasn't flagged, while `plan` listed 14 for the same spec. Completeness is judged inconsistently.
- In Run B, every run reported opening no ADRs (self-reported).

## `plan-check`

Run once, in Run A, on f2's spec. It filled the Constitution Check unprompted.

- Listed 14 of 19 ADRs, with 34 constraint rows in `ADR-nnn@vN Cn` form, and a "considered and not applied" list with reasons.
- Opened 6 ADRs in full, and read version and constraint lines of the rest through search. This only partly matches the expectation of "opening ADRs through the constitution's index", and it is the only evidence so far on ADR-009@v2 C9's constraints-first loading.
- Assessed all six hard rules, and noted that rule 3 is conduct a plan can't show.
- Stopped on four open questions, three needing Andy's decision, instead of guessing.
- There is no labelled correct set of ADRs for this feature, so 14 says nothing reliable about recall or precision.
- The Complexity Tracking table stayed empty, so the "justified violation" route is untested.

## Cost

| Stage | Tokens per run | Time per run |
| --- | --- | --- |
| `analyze` | About 62,000 to 64,000 | 26 to 51 seconds |
| `plan` | About 101,000 | About 4 minutes |

About 1.8 million tokens across 27 `analyze` runs and the plan check. Token counts are subagent totals, including agent overhead.
