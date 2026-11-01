# Architect in the Loop Constitution

This constitution covers this repository: the capability and how it is built. The eShop fork will have its own in Phase 2, indexing the subject's ADRs. This one summarises rules recorded elsewhere and adds none of its own (ADR-009@v2 C11). If it disagrees with an ADR, that is a decision gap for the architecture coordinator (ADR-009@v2 C12).

## Core Principles

### I. Deterministic Where Possible, Probabilistic Where Necessary, Measured Everywhere

- Deterministic checks MUST gate changes wherever a rule can be checked mechanically (ADR-011@v1).
- A claim MUST be backed by a measurement. Where something can't be measured, the repo MUST say so (CLAUDE.md, "How we work").

Rationale: this is the project's thesis, in product.md.

### II. Decisions Are Recorded and Honoured

- When a backlog item closes, its decision MUST be recorded as an ADR (ADR-010@v1 C4).
- Every plan MUST list the ADRs whose scope applies, and cite their constraints as `ADR-nnn@vN Cn` (ADR-009@v2 C8).
- Where no decision exists, or decisions conflict, the work MUST stop and ask the architecture coordinator (CLAUDE.md, "How we work"; product.md, success criterion 4).

Rationale: nothing else proves a decision was applied.

### III. The Evaluation Stays Held Out

- The private evaluation repository MUST NOT be accessed, or cloned into this repository or a worktree (hard rule 1; ADR-011@v1 C7).
- Acceptance tests MUST NOT be edited to make them pass; a failing test is reported (hard rule 3).
- Evaluation outcomes MUST NOT be built by hand (ADR-005@v3 C2).

Rationale: the results mean nothing if the capability was tuned on them.

### IV. The Subject Stays Pinned and Separate

- Work built by hand MUST come from a development outcome, and each outcome MUST change only its listed areas (hard rule 2; ADR-005@v3 C1, C6).
- eShop MUST be included only as the submodule `subject/eshop`, and its files MUST NOT be copied into this repository (hard rule 4; ADR-002@v2 C1, C3).
- Subject-side artefacts MUST live in the fork (ADR-003@v2 C1).
- Existing eShop behaviour MUST NOT change outside an approved spec; defects noticed are reported (hard rule 5; ADR-005@v3 C3).
- The capability's code and prompts MUST NOT contain subject-domain knowledge (ADR-001@v2 C1).

Rationale: keeps the "used, not built" boundary, and keeps the capability portable.

### V. Agent Work Is Checked Independently, and Humans Approve

- Every documentation PR MUST be reviewed by the adversarial reviewer to REVIEW.md, which MUST NOT approve a change (ADR-012@v1 C4, C6).
- Each delivery stage MUST be run by hand, and recorded on a loop card, before it is automated (ADR-012@v1 C1).
- A stage's autonomy MUST be raised one level at a time, and not above level 2 until ADR-013 is revised (ADR-012@v1 C2, C9).
- While stages are hand-run, a change MUST NOT be pushed until Andy has reviewed it, and MUST reach `main` only through a pull request he merges (ADR-013@v1 C5, C6).

Rationale: autonomy is earned with evidence, one stage at a time. Full autonomy is a stretch goal, which may prove impossible or ineffective (product.md).

### VI. Scope Holds

- Shopper-facing AI features, multi-tenancy and a custom coding agent MUST NOT be built (hard rule 6; ADR-004@v2 C1, C2, C3).

Rationale: effort stays on governance, impact analysis and evaluation.

## ADR Index

Generated from the ADRs' front matter (ADR-009@v2 C10). Open an ADR for its current version and constraints.

| ADR | Decision | Scope |
| --- | --- | --- |
| [ADR-000](../../docs/adr/ADR-000-decision-record-format.md) | Decision records use our own template, extending MADR 4.0.0 | capability, subject, concern:governance |
| [ADR-001](../../docs/adr/ADR-001-generic-over-subject-knowledge.md) | The capability is generic over subject knowledge and specific to one stack | capability, concern:portability |
| [ADR-002](../../docs/adr/ADR-002-subject-included-as-pinned-fork.md) | eShop is included as a pinned fork submodule, with two baselines | subject, project, concern:reproducibility |
| [ADR-003](../../docs/adr/ADR-003-subject-artefacts-live-with-subject.md) | Subject-side artefacts live with the subject's code, in the fork | capability, subject, concern:portability |
| [ADR-004](../../docs/adr/ADR-004-non-goals.md) | Non-goals: no shopper-facing AI, no multi-tenancy, no custom coding agent | capability, subject, project |
| [ADR-005](../../docs/adr/ADR-005-ordering-exemplar.md) | Ordering is the exemplar domain, brought to the preferred state first | project, subject, domain:ordering |
| [ADR-006](../../docs/adr/ADR-006-evidence-line-and-publication.md) | The evidence line rests on three facts, and results are published all or none | project, concern:evaluation |
| [ADR-007](../../docs/adr/ADR-007-outcome-set-and-impact-scoring.md) | Ten held-out outcomes, hand-written two-tier labels, deterministic impact scoring | project, concern:evaluation |
| [ADR-008](../../docs/adr/ADR-008-acceptance-tests-and-preregistration.md) | Acceptance tests are written first by a human, run red then green, and pre-registered | project, concern:evaluation |
| [ADR-009](../../docs/adr/ADR-009-spec-kit-workflow.md) | Spec Kit v1.1.2, pinned and core only, with specs that flow forward | project, concern:delivery |
| [ADR-010](../../docs/adr/ADR-010-working-model.md) | The working model is designed around Andy's review attention, and dogfoods the product | project, concern:delivery |
| [ADR-011](../../docs/adr/ADR-011-deterministic-controls-on-agents.md) | Deterministic controls gate what coding agents can read, write and change | project, concern:delivery, concern:security |
| [ADR-012](../../docs/adr/ADR-012-independent-checks-and-staged-autonomy.md) | Agent work is checked independently, and autonomy is raised in stages | project, concern:delivery |
| [ADR-013](../../docs/adr/ADR-013-public-repo-licence-and-review.md) | Public repositories, MIT licence, protected main, and review before anything is pushed while stages are hand-run | project, concern:governance |
| [ADR-014](../../docs/adr/ADR-014-two-separate-graders.md) | Two graders, runtime and evaluation, kept separate | capability, concern:evaluation |
| [ADR-015](../../docs/adr/ADR-015-outcome-splits-and-deliver-dark.md) | Outcomes may split by nine known scenarios; partial work is delivered dark | capability, concern:delivery |
| [ADR-016](../../docs/adr/ADR-016-improving-legacy-code-the-capability-touches.md) | When the capability changes a legacy domain, it improves the code it touches, within a budget | capability, subject, concern:quality |
| [ADR-017](../../docs/adr/ADR-017-coordinator-interface.md) | The architecture coordinator works through a web interface, React over a C# REST API | capability |
| [ADR-018](../../docs/adr/ADR-018-timebox-and-prior-work.md) | No hard deadline, milestones defined by evidence, and prior-work overlaps go to Andy | project, concern:governance |

## Development Workflow

- Work MUST follow Spec Kit v1.1.2, core only: specify, plan, tasks, implement and converge (ADR-009@v2 C2, C3, C4).
- Agents SHOULD load an ADR's Constraints section, and open the full ADR only when they need its reasoning (ADR-009@v2 C9).
- What must stay true MUST live in the ADRs and this constitution, not in specs (ADR-009@v2 C7).

## Governance

- Amendments MUST be approved by the architecture coordinator.
- A new principle MUST cite its source ADR or hard rule (ADR-009@v2 C11).
- Versions follow Spec Kit's semantic versioning: MAJOR for a principle removed or redefined, MINOR for one added or materially expanded, PATCH for wording, a refreshed citation or a regenerated index.
- Compliance is checked at each plan's Constitution Check, and by review.

**Version**: 1.0.0 | **Ratified**: 2026-11-01 | **Last Amended**: 2026-11-01
