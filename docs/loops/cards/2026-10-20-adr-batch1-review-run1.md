# Loop card: review · ADR batch 1 (PR #6) · run 1

| Field | Value |
| --- | --- |
| Stage | Review (documentation PR) |
| Outcome | None: project work, Step 5 batch 1 (ADR-001 to ADR-005) |
| Run | 1 |
| Date | 2026-10-20 |
| Autonomy level | 1, drafted: the reviewer drafts findings; the author responds; Andy decides |
| Session | [Session 02 log](../../sessions/2026-10-20-session-02.md) |
| Previous card for this stage | First run |

## 1. Purpose

This stage checks a documentation PR against [REVIEW.md](../../../REVIEW.md) (fidelity, facts, constraints, honest enforcement), so that Andy reviews findings with evidence rather than re-reading every line.

**Test run.** PR #6 is already merged. The run tests whether the reviewer is worth adding before batch 2.

## 2. Trigger and inputs

- **Trigger:** Andy, asking to draft REVIEW.md and test it on batch 1.
- **Inputs:** the diff `ed10b99..ca3de68`; REVIEW.md v0.1 (uncommitted draft on `docs/review-policy`); the PR #6 description.
- **Context loaded:** REVIEW.md, backlog.md, ADR-000, the template, CLAUDE.md, and the eShop code for fact checks. The reviewer did not see the author's conversation.

### Expected result, written before the review finished

The author knows of one weakness, flagged to Andy in chat but not in the PR description, and doesn't tell the reviewer about it:

- **ADR-001, C1 Enforcement:** "the term list will itself be derived from the eShop contract". This design detail isn't in backlog P3. Under REVIEW.md pass 1 it should be flagged as **untraced**, at High severity.

A useful reviewer catches this. Missing it is a significant miss. Other findings are scored by Andy as real or not.

## 3. Actor

- **Who:** a reviewer subagent; the author (Claude, main session) responds; Andy decides.
- **Agent setup:** a general-purpose subagent with a fresh context, on the same model as the author (Claude Opus 5.5). It was told to stay read-only and not to access the evaluation repo.
- **Human role:** asked for the run; scores the findings.

## 4. What happened

1. Author drafted REVIEW.md v0.1.
2. Author started the reviewer at 16:01 with the diff range, its sources and the rules. The known weakness wasn't mentioned.
3. Reviewer returned after about 27 minutes: 20 findings (3 High, 7 Medium, 10 Low), 4 nits, one note on the decisions and a list of what it couldn't check. It stayed read-only and inside the repository, as instructed.
4. Author spot-checked two factual claims: the bootstrap script doesn't check the submodule (finding 1), and upstream eShop has a test for the Foundry default (finding 20). Both are true.
5. Author responded to each finding (section 7).

## 5. Feedback loop

- **Signal:** none inside the reviewer. It is the feedback signal for the author.
- **Stop condition:** all four passes done, and findings reported.
- **Iteration cap:** one pass per run.
- **Iterations taken:** 1.

## 6. Output

- **Artefact:** review findings, kept on this card (section 7) and in the PR description of future PRs.
- **Feeds:** the author's responses; Andy's merge decision.

## 7. Checks

**Against the expected result:** the known weakness was **caught**, as finding 14 ("untraced design details … the term list will itself be derived from the eShop contract"). It was rated **Low, not the High expected**. The reviewer treated it as enforcement prose rather than a constraint. That's arguable: REVIEW.md's severity definitions don't say how to rate untraced detail outside the constraints. **Partial hit.**

**The reviewer found three High issues the author didn't know about** (findings 1 to 3). All three are cases of the write-up claiming more than the decision or the checks support. That's exactly what REVIEW.md pass 1 and pass 4 exist for.

Author's response to each finding. **Author-scored:** Andy delegated the scoring, so it isn't an independent measure of precision.

| # | Sev | Summary | Author response |
| --- | --- | --- | --- |
| 1 | High | ADR-002 C1 front matter says the bootstrap script checks the submodule; it doesn't | Accept. Verified |
| 2 | High | ADR-005 C4 adds an untraced "except through approved outcomes" | Accept |
| 3 | High | ADR-005 claims the overlap matrix checks C2; it can't | Accept |
| 4 | Med | P9 marked Closed, but "each domain has its own context, ADR scope and spec folder" is in no ADR and no deferral list | Accept |
| 5 | Med | ADR-005 C2 widens the scope and adds an untraced "before the scored run" | Accept |
| 6 | Med | ADR-004 asserts the E4 comparison, which is still Open | Accept |
| 7 | Med | ADR-003 cites a loop card that isn't on main, and says the fork has Spec Kit when that commit isn't pushed | Accept |
| 8 | Med | ADR-004 C4 bundles two rules; `ref` points at the subject file, not a check | Accept |
| 9 | Med | ADR-003 C1 ("subject ADRs live in the fork") has no definition of a subject ADR, and ADR-002, 004 and 005 have `subject` scope | Accept. A real gap in ADR-000 and ADR-003 |
| 10 | Med | ADR-002 C3 bundles two rules | Accept |
| 11 | Low | ADR-002 C4 narrows "all tags" to "baseline tags"; `ref` should be the ruleset | Accept |
| 12 | Low | ADR-001 C4 hardens "out of scope" into "MUST NOT be built" | Partly. A constraint has to be stated as a rule to be checkable; the effect is the same. Worth a note in the ADR |
| 13 | Low | ADR-003 C2 bundles two rules, and hard rule 4 doesn't cover it | Accept |
| 14 | Low | ADR-001 untraced details; the backlog's P3 still says "a CI check enforces this" in the present tense | Accept (the known weakness) |
| 15 | Low | Alternatives not in the backlog are presented as options considered | Partly. ADR-000 C7 requires them. Mark which alternatives were added when writing the ADR |
| 16 | Low | Hard rule 2's "only in Ordering" isn't a constraint | Accept |
| 17 | Low | ADR-005 `tier: cross-cutting` on a domain-scoped ADR | Accept |
| 18 | Low | PR description overstates "P4's decided part" | Accept |
| 19 | Low | Stretch-goal detail dropped | Accept |
| 20 | Low | "Throwaway check passes" leaves no artefact; ADR-004 misses an existing upstream test | Accept. Verified |

## 8. Gate

- **Approver:** Andy.
- **Evidence shown:** this card, with the findings and the author's responses.
- **Decision:** adopt the reviewer for every documentation PR, run by hand (Andy, 20 Oct). Correct batch 1 by **versioning ADRs in place** (Andy's proposal), not by superseding them: ADR-000 v2, then ADR-001 to ADR-005 v2 as corrections.
- **Did the approver redo any of the work to decide?** No. He decided from the summary of findings and options.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | About 27 minutes (1,619 s) | Subagent report |
| Tokens | About 114,000 | Subagent report |
| Tool calls | 24 | Subagent report |
| Findings | 20, plus 4 nits | Count |
| Known weakness caught | 1 of 1, at a lower severity than expected | Expectation written before the run |
| Author accepts | 18 in full, 2 in part | Section 7 |
| Real findings | 18 real, 2 partly real (author-scored, not independent) | Section 7 |
| Human minutes | Not measured | — |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| Batch 1 merged with 3 High findings | No review besides Andy's before merge, and the author can't see their own overreach | Run the reviewer before every documentation PR | REVIEW.md, if adopted | |
| Severity of the known weakness under-rated | REVIEW.md doesn't say how to rate untraced detail in prose outside the constraints | Untraced detail is High wherever it appears, if a check or agent would act on it | REVIEW.md v0.2 | |
| Fixing batch 1 collides with ADR-000 C4 | C4 lets only status and enforcement state change, but these errors are in the constraints | ADRs are versioned in place, with corrections and revisions typed in a History section | ADR-000 v2 (C8 to C11) | |
| A gap in the format itself: no definition of a "subject ADR" | ADR-000 and ADR-003 didn't define it | Subject and project ADRs defined | ADR-000 v2 (C12) | |
| The run is slow and costly for 5 short ADRs | One fresh-context agent reading everything, with no focus | Try scoping the reviewer's reading list on the next run, and compare | Nowhere yet | |

## 11. Ready to automate?

- [ ] Stable inputs and outputs: one run.
- [ ] A trustworthy check: one blind seed caught, at the wrong severity; findings not yet scored by Andy.
- [ ] Known failures: severity calibration open.
- [ ] An evidence-based gate: pending.
- [x] Known cost: about 27 minutes and 114,000 tokens per batch of five ADRs.

**Verdict:** keep at level 1, and run it by hand on every documentation PR. **Why:** the first run found real problems the author missed, but it is one run, with one seed.

**Next run changes:** fix the severity rule; build a small seeded test set (copies of ADRs with known weaknesses planted, kept out of the real record) as the reviewer's regression eval (D1); time Andy's scoring; try a narrower reading list to cut cost.
