# Loop card: review · ADR batch 4 · run 6

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 5 batch 4 (ADR-014 to ADR-017) |
| Run | 6 |
| Date | 2026-10-30 (review ran 29 Oct) |
| Autonomy level | 1, drafted |
| Session | [Session 04 log](../../sessions/2026-10-29-session-04.md) |
| Previous card for this stage | [Run 5](2026-10-21-adr-batch3-review-run5.md) |

## Run

- **Inputs:** the diff `main..6171ecf` (local branch `docs/adr-batch-4-capability`); REVIEW.md; four approvals quoted word for word.
- **Change from earlier runs:** the author checked for contradictions before writing, and asked Andy two questions first (C13's defaults, Q4 against hard rule 5). The brief also asked the reviewer to look for contradictions between constraints.
- **Cost:** about 5 minutes (320 s), about 127,000 tokens, 21 tool calls.
- **Result:** 4 High, 3 Medium, 9 Low, 5 nits, and a note on the decisions.

## Findings and responses

| # | Sev | Finding | Response |
| --- | --- | --- | --- |
| 1 | High | ADR-015@v1: rule 3's first part has no constraint, and C5 dropped its condition, so it contradicted S1, S2 and S4 | Accept. C13 added; C5's condition restored |
| 2 | High | ADR-015@v1 C3, C4, C6, C7 applied "rules for an automatic split" to every split | Accept. All scoped to automatic splits |
| 3 | High | ADR-015@v1 C11 required approval for S8; the source says that only for S7 | Accept. C11 now S7 only; C14 added for S8 |
| 4 | High | ADR-014@v1 C2 could send impact or test scoring to the grader, against ADR-007@v1 C7 | Accept. C2 scoped; the relationship stated in the Decision |
| 5 | Med | ADR-014@v1 C6 leaves out A5's split of runtime (public) and evaluation (private) rubrics, and overstates what can be checked | Accept. C6 and C7; the enforcement note says what only Andy can check |
| 6 | Med | ADR-016@v1 C10: the chosen tools may not emit SARIF | Verified in the Stryker.NET and coverlet docs: neither does. Andy's ruling: violations only |
| 7 | Med | ADR-015: "recorded in the fork" isn't true yet | Accept. "To be recorded" |
| 8 | Low | ADR-015@v1 C5 and C8 mechanisms wrong | Accept. Corrected |
| 9 | Low | ADR-017@v1 C1 narrowed the source and bundled two rules | Accept. C1 restored; C5 added |
| 10 | Low | ADR-016@v1 C9 dropped G10's detail | Accept. Restored from the sketch |
| 11 | Low | ADR-016 lost "the repo says so" | Accept. C16 added |
| 12 | Low | ADR-016@v1 C8's baseline may not fit the exception model | Accept as a risk. In Consequences, for Q1 |
| 13 | Low | ADR-015 ties a rule to a ladder that is only proposed | Accept. Noted |
| 14 | Low | ADR-014 cited ADR-010 for something it doesn't say | Accept. Citation removed |
| 15 | Low | ADR-015@v1 C1 bundled; C2 ambiguous | Accept. C12 added; C2 reworded |
| 16 | Low | ADR-014@v1 C1 pre-empted the open Scope and Cost questions | Accept. C1 says where it runs is open |
| Nits | — | G11 attribution; C4 and C10 overlap; backlog date; "designed as"; C15 joined two things | Fixed; C4 and C10 kept, because C10 also covers non-automatic splits |

Author-scored: 16 of 16 real. Not independent.

**The reviewer's note:** ADR-016@v1 C9 and ADR-015@v1 S9 have no defined boundary. Andy chose to record it as open under A1.

## What the run showed

- **Asking first helped, but not fully.** Asking two questions up front left only two rulings after review, against nine in batch 2. All four Highs were still the author's own transcription errors: conditions dropped when prose became rules. Decisions were not the problem this time.
- **A fact the reviewer couldn't verify was checked by the author:** the reviewer flagged SARIF as unverified, and reading the tools' docs settled it. Useful division of labour.
- **A finding led to a design question.** Andy's challenge on SARIF ("do we need to explore how we'll use the output?") turned a format rule into the evidence-record question under Q2.

## Measurements

| Run | Wall time | Tokens | High | Total findings |
| --- | --- | --- | --- | --- |
| 1 | 27 min | 114k | 3 | 20 |
| 2 | 6.5 min | 116k | 3 | 16 |
| 3 | 6 min | 98k | 4 | 13 |
| 4 | 13 min | 114k | 1 | 18 |
| 5 | 5 min | 122k | 2 | 18 |
| 6 | 5 min | 127k | 4 | 16 |

## What went wrong

| Failure | Root cause | Fix | Where the fix landed |
| --- | --- | --- | --- |
| Conditions lost when prose became constraints (four Highs) | The author writes constraints from memory of the prose, not clause by clause against the source | None yet. Candidate for the ADR-writing skill (Step 7): for each source rule, copy its condition into the constraint | Nowhere yet |

## Ready to automate?

Unchanged: keep at level 1. **Not re-reviewed:** the changes made after this review are Andy's rulings and the fixes above.
