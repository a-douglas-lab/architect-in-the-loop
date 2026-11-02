# Loop card: review · constitution · runs 8 and 9

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 6 |
| Runs | 8 (first draft, 22 restated MUSTs) and 9 (thin rewrite, option D) |
| Date | 2026-11-01 |
| Autonomy level | 1, drafted |
| Session | [Session 05 log](../../sessions/2026-11-01-session-05.md) |
| Previous card for this stage | [Run 7](2026-10-30-adr-018-review-run7.md) |

## Runs

| | Run 8 | Run 9 |
| --- | --- | --- |
| Commit | `0b59ab7` | `df67913` |
| Wall time | About 22 minutes (1,332 s) | About 11 minutes (638 s) |
| Tokens | About 128,000 | About 129,000 |
| Tool calls | 17 | 22 |
| Findings | 10 High, 10 Medium, 9 Low, 5 nits | 1 High, 8 Medium, 8 Low, 4 nits |

## Run 8: the review that changed the design

Most Highs shared one cause. The draft restated ADR rules as constitution MUSTs. Five dropped conditions, and `analyze` treats the constitution as non-negotiable, so a paraphrase would beat its ADR: "no automatic winner" wouldn't hold. The reviewer's note named this.

Andy declined to choose from the options offered, and asked for each to be modelled against use cases. Four were modelled, and he then asked whether parallel problems (tool discovery, progressive disclosure) applied. Both steps changed the outcome: option D appeared during the modelling, and T6 was reframed as a retrieval problem. He chose D.

Run 8's other findings were either resolved by the rewrite or fixed with it: untraced sources, overclaims in the scaling note (including the author's false claim that stewards are cheaper in total), and T6 and session log inconsistencies.

## Run 9: findings and responses

| # | Sev | Finding | Response |
| --- | --- | --- | --- |
| 1 | High | "A plan that breaks one of these is CRITICAL" was a new rule | Accept. Replaced with a compliance MUST, sourced to ADR-009@v2 C17 |
| 2 | Med | adrkit's "below 1.1.0" is false, and was repeated under "checked in their docs" | Accept. Verified: `>=0.13.0,<1.2.0`. Both backlog lines corrected |
| 3 | Med | ADR-009 implied `analyze` catches hard-rule breaches | Accept. Now stated as unproven |
| 4 | Med | Hard rules keep two problems of the rejected draft | Accept. Stated in Consequences, and C15 reworded |
| 5 | Med | The hard-rule benefit doesn't reach eShop until the fork has a constitution | Accept. Stated in ADR-009; open under T1 |
| 6 | Med | The constitution's opening restated C12 | Accept. Now a pointer |
| 7 | Med | PATCH for "a regenerated index" had no source, and MINOR narrowed | Accept. C16 now defers to Spec Kit's rules |
| 8 | Med | C8, C10, C13 and C14 can't be traced to quoted words | Option C's text to be quoted in the PR. The change from "one-line decision" to title is stated |
| 9 | Med | "Eight stages" is wrong: nine load it | Accept. Corrected |
| 10 | Low | `analyze`'s effect stated too narrowly; `converge` omitted | Accept |
| 11 | Low | C15 and C16 bundled | Partly. C17 split out; C16 left |
| 12 | Low | C9 and C13 are weakly checkable | Accept. Stated |
| 13 | Low | No "chosen" entry for option D; no "do nothing" | Accept. Added |
| 14 | Low | Hard rule 2's rewording missing from the backlog | Accept. Added to T1 and History |
| 15 | Low | A proposal listed as decided; skill scope merged | Accept. Moved; backlog softened |
| 16 | Low | Fork path-rules idea goes beyond the approved spike | Accept. Separated |
| 17 | Low | Governance has no compliance expectation | Accept. Added |
| Nits | — | Terminology, a vague citation, product.md's description, "117" | Fixed; now "about 115" |

Author-scored: 17 of 17 real. Not independent.

**The reviewer's note:** Andy may want to decide when the fork constitution is written. Recorded as open under T1.

## What the runs showed

- **A design fault can look like many writing errors.** Run 8's 10 Highs mostly fell away with one change of shape, where fixing them singly would have kept the fault.
- **A human challenge did what the reviewer can't.** The reviewer checks text against sources. Andy's two questions changed the design itself.
- **A fourth factual error by the author** (adrkit): this one repeated stale text under a heading claiming it had been checked. "Open every file a claim names" needs extending: re-check facts copied from older text.
- **In chat, "eight stages" was also wrong,** in the option table: per-feature totals there were understated by one load.

## Measurements

| Run | Wall time | Tokens | High | Total findings |
| --- | --- | --- | --- | --- |
| 1 | 27 min | 114k | 3 | 20 |
| 2 | 6.5 min | 116k | 3 | 16 |
| 3 | 6 min | 98k | 4 | 13 |
| 4 | 13 min | 114k | 1 | 18 |
| 5 | 5 min | 122k | 2 | 18 |
| 6 | 5 min | 127k | 4 | 16 |
| 7 | 9 min | 93k | 2 | 10 |
| 8 | 22 min | 128k | 10 | 29 |
| 9 | 11 min | 129k | 1 | 17 |

## Ready to automate?

Unchanged: keep at level 1. **Not re-reviewed:** the changes made after run 9 are the fixes above and the proposed validation layers under Q1.
