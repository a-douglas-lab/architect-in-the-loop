# Loop card: specify · DEV-1 · run 1

| Field | Value |
| --- | --- |
| Stage | Specify |
| Outcome | DEV-1, customers can add a note to their order at checkout |
| Run | 1 (practice run: see Purpose) |
| Date | 2026-10-20 |
| Autonomy level | 1, drafted: the agent drafts, Andy edits before the spec is used |
| Session | [Session 02 log](../../sessions/2026-10-20-session-02.md) |
| Previous card for this stage | First run |

## 1. Purpose

This stage turns an outcome statement into a business-language spec, so that the plan and the acceptance tests (D6) have an agreed definition of done.

**Practice run.** It runs ahead of the roadmap: the D6 dry run is Phase 2, the constitution is a blank template and no subject ADRs exist. Its aim is to learn the stage and find what's missing, not to produce the authoritative DEV-1 spec. The spec stays on an unmerged fork branch.

## 2. Trigger and inputs

- **Trigger:** Andy's message, "merged, start the first loop card on DEV-1 specify". PR #4 was in fact merged a few minutes later, at 14:25, while the fork work was under way.
- **Inputs:**
  - Outcome statement, verbatim: "Customers can add a note to their order at checkout" ([development-outcomes.md](../../outcomes/development-outcomes.md) at `b68aac2`; unchanged in `b52abd5`).
  - Spec Kit v1.1.2 spec template, `.specify/templates/spec-template.md` in the fork, from `specify init` on the run's branch.
- **Context loaded:** the `speckit-specify` skill (`.claude/skills/speckit-specify/SKILL.md` in this repo at `b68aac2`) and the spec template. The constitution file was present but is the blank template, so it added nothing.
- **Context needed and not available:**
  - Subject ADRs (P4, Phase 2). Nothing told the spec which decisions apply: for example, how personal data in free text is handled, or the rule that business rules live in the owning domain.
  - A fork constitution.
  - Any knowledge of current eShop behaviour. The skill doesn't ask the agent to read the code, and it didn't. One assumption about existing behaviour ("only signed-in customers can check out today") is unchecked.
  - Persona and domain context. The skill doesn't load product.md, so the merchant persona didn't shape the spec. The merchant question only came up because the agent asked it.

## 3. Actor

- **Who:** agent drafted; Andy answered the clarification question and approves at the gate.
- **Agent setup:** Claude Code desktop app, Claude Opus 5.5. Effort and permission mode weren't recorded. The `speckit-specify` skill was followed by hand, because the skill lives in this repo's `.claude/` while the spec belongs in the fork. Tools: file read and write, the shell (for `specify init` and git).
- **Human role:** chose the run type (practice run in the fork). Answered one scope question.

## 4. What happened

1. Checked preconditions and found the run would jump ahead of the roadmap (above). Asked Andy: run now in the fork, run in this repo, or wait. **Andy: practice run in the fork.**
2. Created the fork branch `practice/dev-1-specify` from `dc7ea49`. Initialised Spec Kit core with the same options as this repo (`--integration claude --script py --ignore-agent-tools`). It added `.specify/` and `.claude/skills/` only.
3. Followed the skill: short name `order-note`, sequential numbering, `specs/001-order-note/`. `.specify/feature.json` was written, but Spec Kit's own `.gitignore` keeps it out of the commit. No extension hooks were registered.
4. Drafted the spec from the outcome statement alone: three user stories, edge cases, 10 functional requirements, 5 success criteria, assumptions. One `[NEEDS CLARIFICATION]` marker (FR-008: who reads the note beyond the customer). Only the final spec was committed, so these draft counts can't be checked. The committed spec has two stories.
5. Validation, iteration 1: two checklist items failed, both caused by the marker (open clarification, unbounded scope).
6. Asked Andy the clarification as three options with their implications. **Andy: customer only, for now.** Removed Story 3 (merchant reads the note), restricted FR-008, and recorded merchant and shipping visibility as a likely follow-up.
7. Validation, iteration 2: all items pass.
8. Committed in the fork, local only: `af47ded`.

## 5. Feedback loop

- **Signal:** the skill's spec-quality checklist (16 items), assessed by the same agent that wrote the spec. No deterministic check and no independent grader.
- **Stop condition:** all checklist items pass, or 3 iterations.
- **Iteration cap:** 3; not reached.
- **Iterations taken:** 2. The second was triggered by the human answer, not by self-correction.

The agent is marking its own homework here. The checklist mostly asks about form ("no implementation details", "success criteria measurable"). It doesn't ask whether the spec is right about the subject system or covers what a domain expert would expect.

## 6. Output

- **Artefact:** `specs/001-order-note/spec.md` and `specs/001-order-note/checklists/requirements.md`, eShop fork, branch `practice/dev-1-specify`, commit `af47ded` (not pushed).
- **Feeds:** clarify (optional), then plan; acceptance tests (D6) from the acceptance scenarios.

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| Spec-quality checklist | Rubric, self-assessed | All 16 items pass | Pass (iteration 2) |
| No `[NEEDS CLARIFICATION]` markers left | Deterministic in principle (text search); done by eye here | Zero markers | Pass |
| At most 3 clarification markers | Deterministic in principle | ≤ 3 | Pass (1) |
| Mandatory template sections present | Deterministic in principle | All present | Pass |
| Spec matches current eShop behaviour | Human judgement | Assumptions about existing behaviour are true | Not run |
| Scope matches the outcome's listed areas (Ordering, storefront checkout) | Human judgement | Nothing outside them | Agent's own check: pass, after FR-008 was answered. Human check: Andy reviewed the spec on 30 Oct and made no edits |

Ways to move checks out of judgement:

- The marker count and mandatory sections are a simple script. Spec Kit runs them as instructions to the model, but they could be a hook.
- "Matches current behaviour" could become a step that runs before drafting and records the code the agent read.
- "Scope matches the listed areas" is an early form of impact analysis (T7). Here the agent raised the question and set out that showing the note to the merchant or to shipping systems would pull in more areas; Andy chose the narrow scope. Since the run, this has become a recorded rule, ADR-005@v3 C6 (a development outcome changes only its listed areas). It is enforced by review today (state `manual`). An automated check of the diff against those areas is only a possibility, once domains map to paths in the subject contract.

## 8. Gate

- **Approver:** Andy, as architecture coordinator, editing then approving the spec (level 1).
- **Evidence shown:** the spec, the checklist with its notes, and this card.
- **Decision:** reviewed by Andy, 30 Oct, and he said to proceed. He made no edits: the fork's working tree is clean at `af47ded`. This is a practice spec, so the review doesn't make it the authoritative DEV-1 spec.
- **Did the approver redo any of the work to decide?** Not recorded.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | About 5 minutes from branching the fork to the commit (14:22 to about 14:27), including one wait for Andy's clarification answer. The earlier run-type question came before 14:22 | Shell clock at the start; fork commit time 14:27:33. Waits not timed separately |
| Human minutes (work plus review) | Not measured | Andy's review wasn't timed |
| Tokens / cost | Not measured | The session doesn't expose per-stage token counts. Gap to fix before cost can be compared across runs |
| Iterations to pass checks | 2 | Checklist notes |
| Leading indicator: spec accepted without rework | No edits at the gate | Fork working tree compared with `af47ded` |
| Lagging indicator: rework found in a later stage | Unknown | Fill in after plan and D6 |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| Stage started ahead of the roadmap, without a constitution or subject ADRs | The roadmap puts D6 in Phase 2; the request came before the gates closed | Treated as a practice run, labelled on the card and in the fork commit | Card, not yet anywhere durable | |
| The skill couldn't be run as a normal skill call: it lives in this repo, the spec belongs in the fork | Two repos, with Spec Kit in each, and the session rooted in this one | Followed the skill by hand with the fork as the project root | Possibly resolved by the tool, not by us: after the run, the author's session listed the fork's own skills as a scoped set (`subject/eshop:speckit-*`, 20 Oct). A reviewer session on 21 Oct didn't show them, so this is unconfirmed. Try it on the next run; if it doesn't work, root the session in the fork | |
| Line-ending warnings on the Spec Kit files in the fork | The fork's `.gitattributes` has `* text=auto`. This repo had a related problem, fixed in `1bb2b3c` (a CRLF rule on `*.ps1` broke Spec Kit's file hashes). The fork's cause may differ, and may touch the `.py` and `.md` files Spec Kit hashes | Not fixed (practice branch) | Nowhere yet. Find the fork's cause before Spec Kit goes in properly; don't copy `1bb2b3c` blindly | |
| Spec drafted with no knowledge of current eShop behaviour; one unchecked assumption | The skill only asks for the outcome and the constitution | Flagged in the checklist notes | Checklist notes. Candidate fix: a pre-drafting step that reads the affected code | |
| Self-assessed checklist: the producer grades its own work | Spec Kit design | None | Nowhere yet. Relevant to A2 (independent grader) and A5 (rubrics) | |

The failures didn't send work back to an earlier stage. The clarification answer narrowed scope inside this stage.

## 11. Ready to automate?

- [ ] Stable inputs and outputs: one run only.
- [ ] A trustworthy check: self-assessed checklist, no independent grader.
- [ ] Known failures: five found, none fixed durably (one possibly resolved by the tool, unconfirmed).
- [ ] An evidence-based gate: run once, with no edits; whether Andy had to redo any work isn't recorded.
- [ ] Known cost: tokens and human time not measured.

**Verdict:** keep at level 1. **Why:** first run, no trustworthy check and no cost data.

**Next run changes:**

- Run it as a real run once the constitution and baseline ADRs exist (Phase 2).
- Try the fork's scoped skill (`subject/eshop:speckit-specify`). If it doesn't work, root the session in the fork.
- Read the affected eShop code before drafting, and record what was read.
- Time Andy's review.
- Find a way to capture tokens per stage.
