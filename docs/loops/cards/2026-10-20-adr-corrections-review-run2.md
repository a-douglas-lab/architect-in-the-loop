# Loop card: review · ADR v2 corrections · run 2

| Field | Value |
| --- | --- |
| Stage | Review (documentation PR) |
| Outcome | None: project work. ADR-000 v2 (revision) and ADR-001 to ADR-005 v2 (corrections) |
| Run | 2 |
| Date | 2026-10-20 |
| Autonomy level | 1, drafted |
| Session | [Session 02 log](../../sessions/2026-10-20-session-02.md) |
| Previous card for this stage | [Run 1](2026-10-20-adr-batch1-review-run1.md) |

## 1. Purpose

This stage checks the corrections from run 1 against their sources, before merge. It is the first run under REVIEW.md v0.2.

## 2. Trigger and inputs

- **Trigger:** the corrections were committed on `docs/review-policy` (1364ff6, 5e18e11).
- **Inputs:** the diff `main..HEAD`; REVIEW.md v0.2; Andy's four approvals, quoted word for word in the reviewer's brief.
- **Changes from run 1:** the brief asked the reviewer to focus on changed lines and their sources, and quoted the approvals, because REVIEW.md pass 1 accepts only quoted approvals. No weakness was planted.

## 3. Actor

Same as run 1: a general-purpose subagent with a fresh context, on the same model as the author (Claude Opus 5.5). Read-only, and barred from the evaluation repo.

## 4. What happened

1. Reviewer ran from 16:57: 16 findings (3 High, 5 Medium, 8 Low), 2 nits, a list of claims it checked and found correct, and a list of what it couldn't check.
2. The author fixed the mechanical findings: unversioned citations, P9's status, History wording and approvers, enforcement mechanisms, and the template nit.
3. Seven findings needed Andy. He chose the recommended option on all seven: ADR-005 C4, C6 and hard rule 2 ("listed areas only"); C2 ("never by hand"); tier `cross-cutting`; and four additions confirmed. These became ADR-005 v3, a revision, plus updates to CLAUDE.md and D1.
4. No third review run. The post-review changes are Andy's own decisions, written up and listed in the PR description.

## 5. Feedback loop

- **Signal:** none inside the reviewer.
- **Iterations taken:** 1.

## 6. Output

Findings, the author's responses (section 7) and Andy's decisions, all carried into the PR description.

## 7. Checks

| # | Sev | Summary | Response |
| --- | --- | --- | --- |
| 1 | High | ADR-005 C4 "stay as they are" blocks DEV-1 and DEV-2 | Andy: listed areas only (ADR-005 v3) |
| 2 | High | Tier changed inside a correction | Accept. Removed from v2; Andy confirmed cross-cutting in v3 |
| 3 | High | REVIEW.md's four passes conflict with D1's recorded three | Andy: four for documentation PRs now, three code passes later (D1 revised) |
| 4 | Med | C7 "mark added alternatives" not explicitly approved | Andy confirmed |
| 5 | Med | ADR-005 C2 would block the scored run | Andy: never by hand; C7 added |
| 6 | Med | The PR breaks C10 (unversioned citations) | Accept. Fixed |
| 7 | Med | P9 status wrong under the legend | Accept. Decided (ADR pending) |
| 8 | Med | "Withdrawn constraints don't count" changes the Q1 metric | Andy confirmed |
| 9 | Low | Hard rule 2 itself conflicts with DEV-1 and DEV-2 | Andy: reworded with finding 1 |
| 10 | Low | ADR-004 History gives the wrong reason for a removal | Accept. Fixed |
| 11 | Low | ADR-002 History misses two changes | Accept. Fixed |
| 12 | Low | Corrections name Andy as approver, but he didn't review the text | Accept. Now "written by Claude, checked by review runs 1 and 2, merged by Andy Douglas" |
| 13 | Low | `manual` state with no mechanism | Accept. Mechanism set to review |
| 14 | Low | `useOllama` is a local, so a unit test can't see it | Accept. Source check |
| 15 | Low | P9's per-domain layout classed as a subject ADR without a ruling | Andy confirmed |
| 16 | Low | "Untrue" too strong for the Spec Kit claim | Accept. Reworded |

Author-scored: 16 of 16 real. Not independent (see run 1).

**The pattern worth keeping:** findings 1 and 5 show that a correction can't fix an ambiguous decision. Matching the source word for word only moved the problem. The reviewer named this itself, and said it needs a revision.

## 8. Gate

- **Approver:** Andy.
- **Decision:** seven rulings made in chat, all as recommended; merge decision pending on the PR.
- **Did the approver redo any of the work to decide?** No. He chose from options with the evidence summarised.

## 9. Measurements

| Measure | Run 2 | Run 1 | How measured |
| --- | --- | --- | --- |
| Wall time | About 6.5 minutes (387 s) | About 27 minutes | Subagent report |
| Tokens | About 116,000 | About 114,000 | Subagent report |
| Tool calls | 15 | 24 | Subagent report |
| Findings | 16 + 2 nits | 20 + 4 nits | Count |
| High | 3 | 3 | Count |
| Needed Andy | 7 | 0 (all fixable by the author) | Count |

Run 2 was four times faster for the same tokens. The focused brief is the likely cause, but this is one comparison, not a measurement of cause.

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| The corrections introduced new problems (tier, unversioned citations) | The author fixed findings without re-reading the rules the fix introduced | None yet. The validator could check C10 citations mechanically | Nowhere yet (Step 7) | |
| Ambiguous decisions surfaced only after write-up | P9's text was ambiguous; the backlog records decisions in prose | Revisions approved by Andy | ADR-005 v3 | |
| Approver overstated in History lines | C8 asks for an approver, but corrections don't need one | Name who wrote, checked and merged | ADR History lines; the template could say so | |

## 11. Ready to automate?

- [ ] Stable inputs and outputs: two runs, with a brief that changed between them.
- [ ] A trustworthy check: no independent scoring yet.
- [ ] Known failures: severity calibration untested since v0.2.
- [x] An evidence-based gate: Andy decided from options, without redoing the work.
- [x] Known cost: about 115,000 tokens per run; wall time varies.

**Verdict:** keep at level 1. **Next run changes:** use the focused brief as standard. Start the planted test set for the reviewer's regression eval.
