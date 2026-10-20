# Loop cards

Status: draft · 20 Oct 2026 · method decided in [backlog.md](../../backlog.md) D1; autonomy levels and readiness criteria are a first draft, to refine after the first DEV-1 runs

A loop card records one run of one delivery stage. It names what started the stage, who did the work, the feedback the work was checked against, who approved it, what it cost and what went wrong.

The purpose is to understand each stage by running it by hand before automating it. A stage is automated only when its cards show that it is ready (see [Ready to automate](#ready-to-automate)). The cards are also evidence: they show checks moving from judgement to deterministic, which is the capability's own thesis applied to how it is built.

Template: [loop-card-template.md](loop-card-template.md).

## How to use

1. **One card per stage per run.** Copy the template to `docs/loops/cards/` and name the copy `<date>-<outcome>-<stage>-run<n>.md`, for example `2026-10-21-dev1-specify-run1.md`.
2. **Fill it in during the run, not afterwards.** Write down timings and failures as they happen.
3. **Never invent a number.** If something wasn't measured, write "not measured" and say why. A gap is a finding.
4. **Record every fix where it landed:** CLAUDE.md, a skill, a hook, a rubric, a template, or nowhere. A fix that lives nowhere will recur.
5. **Compare runs.** The second and third runs of a stage show whether the fixes worked and whether the check is stable.

## Stages

These are the stages for the DEV-1 dry run (D6). Spec Kit provides the core; review and merge come from D1.

| Stage | Input | Output | Typical check |
| --- | --- | --- | --- |
| Outcome | Business need | Outcome entry in development-outcomes.md | Human judgement |
| Specify | Outcome | `specs/<feature>/spec.md` | Rubric; human review |
| Clarify | spec.md | Updated spec.md | Open questions resolved |
| Plan | spec.md, constitution, ADRs | plan.md | ADRs cited; human review |
| Tasks | plan.md | tasks.md | Every task traces to the plan |
| Analyze | spec, plan, tasks | Consistency report | No critical findings |
| Acceptance tests (D6) | Outcome, spec | Tests in the eShop fork | Compile; confirmed red |
| Implement | tasks.md | Code | Build, tests, analysers |
| Converge | Code, spec, plan, tasks | New tasks or "converged" | Converged |
| Mutation test | Tests, code | Mutation score | Score above threshold (E3) |
| Review | Diff, spec, plan | Review findings | Reviewer policy; no blockers |
| Merge | Approved PR | Commit on main | Branch protection; CI green |

Add a stage if a run needs one. Skip a stage only if you write down why.

## Autonomy levels

The level at which a stage was run. It follows the playbook's advice to grant autonomy in tiers, from read-only and advisory roles towards gated write access.

| Level | Name | Who does what |
| --- | --- | --- |
| 0 | Manual | A human does the work; the agent may answer questions |
| 1 | Drafted | The agent drafts; a human edits the draft before it is used |
| 2 | Approved | The agent produces the artefact; a human approves or rejects it without editing |
| 3 | Gated | The agent produces the artefact; deterministic checks gate it; a human samples |
| 4 | Autonomous | The agent produces the artefact and passes deterministic gates; no human in the loop for this stage |

Most stages start at 1. Level 4 is for stages with no risk-bearing decision in them; the capability's approval points (architecture sketch) never go above 3.

## Ready to automate

Raise a stage's autonomy level by one only when its recent cards show all of these:

- **Stable inputs and outputs.** The artefact's shape didn't change between the last two runs.
- **A trustworthy check.** It is deterministic, or a rubric that gave the same verdict on the same artefact across repeated runs.
- **Known failures.** Every failure seen has a fix that landed somewhere, and it didn't recur on the next run.
- **An evidence-based gate.** The approver decided from evidence on the card or the PR, without redoing the work.
- **Known cost.** Tokens, wall time and human minutes are measured, not estimated.

Record the decision to raise a level on the card that justified it.
