# Loop card: implement · Step 7 ADR validator · run 1

| Field | Value |
| --- | --- |
| Stage | Implement, with research and behaviour tests (project tooling, no Spec Kit feature folder) |
| Outcome | None: project work, Step 7 item 2 |
| Run | 1 |
| Date | 2026-11-04 |
| Autonomy level | 1, drafted: the agent built; Andy ruled three times, approved three ADR texts and the ADR-000 mechanism texts, asked for CUE's reach to be measured, and approved the CUE download |
| Session | Same session as the [CI card](2026-11-04-step7-ci-run1.md) |
| Previous card for this stage | [Step 7 CI, run 1](2026-11-04-step7-ci-run1.md) |

## 1. Purpose

This run turns ADR-000's and ADR-009's mechanical rules into a check that CI and the C1 hook run, so ADR mistakes are caught by a program and not only by review (backlog Q6, VL-9).

## 2. Trigger and inputs

- **Trigger:** Andy, "We can start 2, but don't we also need to consider cue schema too as i thought the index would bloat and not solve the search problem we'll have for specific clauses inside the ADRs?"
- **Inputs:** ADR-000@v3, ADR-009@v2, the template, the constitution, CLAUDE.md, backlog Q1, Q6 and T6, at `67b1bd4` (`main` after PR #18).

## 3. Actor

- **Who:** an agent (Claude Opus 5.5, desktop app), with Andy deciding.
- **Human role:** raised the CUE and index questions; ruled "Code checks now; CUE question researched first", "Record for the T6 ADR", "JSON Schema; record CUE finding in Q1"; approved ADR-000 v4 and ADR-009 v3 ("Approve as shown"), then the amended v4.

## 4. What happened

1. Measured the index (about 45 tokens per ADR) and recorded the bloat point for the T6 ADR.
2. Wrote the expected results (`0c5b00b`), built the validator, and ran A0 by hand: it failed on a validator fault (a quoted YAML title).
3. Harness runs: one harness fault (a guessed file name) and a Windows encoding fault in the validator, then 20 of 20.
4. Checked every ADR revision made in Step 7 against the commit Step 7 started from: 0 problems.
5. Wired the per-file checks into the C1 hook (K12 to K14) and the full check into CI.
6. Andy approved ADR-000 v4 and ADR-009 v3's Enforcement text. The validator accepted both, and its own state and ref update.
7. CUE desk research: the author counted 1 of 171 constraints as data-shaped, later corrected (173 constraints; see step 9). Andy chose JSON Schema. Its expectations were committed (`687b1e6`), then F passed 11 of 11.
8. Amended ADR-000 v4 for C1, with Andy's approval.
9. At Andy's request ("yes measure CUEs real reach"), classified all 173 constraints, predictions first: 22 (13%) share a field, 69 (40%) are checkable as data today. Then a CUE demo ("Yes, download and run it"): 8 clauses from six ADRs against DEV-1, 8 of 9 cases matched, a planted clash caught. Review run 2 corrected an overstated headline (32%) and a misattributed quote.

## 5. Feedback loop

- **Signal:** test runners against expectations committed first; the validator on the real ADRs and their history.
- **Iterations taken:** A: 3 (hand run, harness run 1, run 2); F: 1; K: 1.

## 6. Output

- **Artefacts:** `scripts/adr.py`, `scripts/adr-front-matter.schema.json`, `requirements.txt`, `tests/adr/`, the hook and CI wiring, ADR-000 v4, ADR-009 v3, backlog Q1, Q6 and T6, on `claude/step7-adr-validator`.
- **Feeds:** every later ADR change; the T6 ADR; item 5's ADR-writing skill, which can run the validator.

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| A0–A25 | Deterministic | Match expected | 20 of 20 on run 2; A0–A25 37 of 37 with F, after review runs 1 and 2 |
| F0–F10 | Deterministic | Match expected | 11 of 11 |
| Hook units with K12–K14 | Deterministic | Match expected | 29 of 29 |
| The validator on Step 7's real revisions | Deterministic | 0 problems | 0 problems |
| CI on GitHub | Deterministic | Green | Not run: needs a push |
| Adversarial review | Rubric (REVIEW.md) | No unresolved High | See below |

## 8. Gate

- **Approver:** Andy. **Decision:** pending his local review.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | Not measured | |
| Tokens / cost | Not measured | |
| Leading indicator | First-run match: A 0 of 1 by hand (validator fault), then harness faults; F 11 of 11 | results.md |
| Index cost | About 850 tokens for 19 ADRs | Characters of the index rows divided by 4 |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed |
| --- | --- | --- | --- |
| A0 failed by hand | Line parser kept YAML quotes | Unquote scalars | `scripts/adr.py` |
| A18 crashed the harness | Windows code page on stderr | UTF-8 output | `scripts/adr.py` |
| A1 stopped the run | The harness guessed a file name | Look it up | `tests/adr/test_adr.py` |
| An approved ADR text went stale within the hour | The schema was decided after the text was approved | Amended v4, with approval | ADR-000 |
| PowerShell quoting broke two commands | Inline scripts in PowerShell 5.1 | Scripts written to files | Nowhere: habit |

## 11. Ready to automate?

Keep at level 1: CI hasn't run the validator on GitHub yet.
