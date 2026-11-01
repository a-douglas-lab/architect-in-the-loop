# Architect in the Loop Constitution

This constitution covers this repository. It points to the rules; it doesn't restate them. Constraints apply as written in their ADR (ADR-009@v2 C15). If this file and an ADR disagree, that is a decision gap for the architecture coordinator (ADR-009@v2 C12).

## Core Principles

### I. Deterministic Where Possible, Probabilistic Where Necessary, Measured Everywhere

The project's thesis. See product.md, CLAUDE.md ("How we work"), ADR-011 and ADR-012.

### II. Decisions Are Recorded and Honoured

See ADR-000, ADR-009 and ADR-010.

- Every plan MUST list the ADRs that apply (ADR-009@v2 C8).
- Every plan MUST cite the constraints that apply, as `ADR-nnn@vN Cn` (ADR-009@v2 C13).

### III. The Evaluation Stays Held Out

See ADR-006, ADR-007 and ADR-008.

### IV. The Subject Stays Pinned and Separate

See ADR-001, ADR-002, ADR-003 and ADR-005.

### V. Agent Work Is Checked Independently, and Humans Approve

See ADR-011, ADR-012 and ADR-013. Full autonomy is a stretch goal (product.md).

### VI. Scope Holds

See ADR-004.

## Hard Rules

Quoted word for word from CLAUDE.md (ADR-009@v2 C15). A plan that breaks one of these is CRITICAL.

1. **Never access the private evaluation repository.** It holds the held-out evaluation outcomes, hidden tests and labels. Never clone it into this repo or a worktree, and never ask for its contents.
2. **In eShop, build only development outcomes by hand.** DEV-1 to DEV-3, centred on the Ordering exemplar, each changing only the areas listed for it in development-outcomes.md (ADR-005). Don't add eShop features beyond an approved spec.
3. **Never edit acceptance tests to make them pass.** A failing test is reported, not changed.
4. **eShop stays pinned and separate.** It lives only in the fork, a-douglas-lab/eShop, included as the submodule `subject/eshop`; never copy eShop files into this repo. Subject-side artefacts (contract, subject ADRs, domain specs, development acceptance tests) are committed in the fork. Its optional AI features stay switched off.
5. **Don't change existing eShop behaviour outside an approved spec,** including defects you notice. Report them to Andy instead; some existing behaviour is deliberately left as it is.
6. **No shopper-facing AI features, no multi-tenancy, no custom coding agent** (agreed non-goals).

## ADR Index

Generated from the ADRs' front matter (ADR-009@v2 C10, C14). Open an ADR for its current version and constraints.

| ADR | Title | Scope |
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

See ADR-009 for the workflow and how specs relate to ADRs.

## Governance

Amendments and versioning follow ADR-009@v2 C16.

**Version**: 1.0.0 | **Ratified**: 2026-11-01 | **Last Amended**: 2026-11-01
