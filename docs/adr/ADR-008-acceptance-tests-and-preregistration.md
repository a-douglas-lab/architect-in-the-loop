---
id: ADR-008
version: 1
title: Acceptance tests are written first by a human, run red then green, and pre-registered
status: accepted
date: 2026-10-21
decision-makers: [Andy Douglas]
scope: [project, concern:evaluation]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: review
    ref: null
    state: manual
  - constraint: C2
    mechanism: review
    ref: null
    state: manual
  - constraint: C3
    mechanism: deterministic check that protocol drivers use only public APIs, events or the UI
    ref: null
    state: planned
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
  - constraint: C7
    mechanism: test runs recorded red against the subject before the change
    ref: null
    state: planned
  - constraint: C8
    mechanism: review
    ref: null
    state: manual
  - constraint: C9
    mechanism: review
    ref: null
    state: manual
  - constraint: C10
    mechanism: mutation testing tool (for example Stryker.NET)
    ref: null
    state: planned
  - constraint: C11
    mechanism: commit in the private repository before the scored run; public anchoring open (E6)
    ref: null
    state: planned
  - constraint: C12
    mechanism: review; tools chosen in Q2
    ref: null
    state: manual
  - constraint: C13
    mechanism: the evaluation runner (E6)
    ref: null
    state: planned
  - constraint: C14
    mechanism: test runs recorded red against the evaluation baseline
    ref: null
    state: planned
  - constraint: C15
    mechanism: review against the pre-registered criteria
    ref: null
    state: manual
  - constraint: C16
    mechanism: review
    ref: null
    state: manual
  - constraint: C17
    mechanism: the evaluation runner (E6)
    ref: null
    state: planned
  - constraint: C18
    mechanism: review
    ref: null
    state: manual
  - constraint: C19
    mechanism: review of the pre-registration record
    ref: null
    state: manual
  - constraint: C20
    mechanism: the evaluation runner (E6)
    ref: null
    state: planned
  - constraint: C21
    mechanism: review
    ref: null
    state: manual
  - constraint: C22
    mechanism: test runs recorded green after the change
    ref: null
    state: planned
  - constraint: C23
    mechanism: review
    ref: null
    state: manual
backlog: [E2, E1b, D6]
---

# ADR-008: Acceptance tests are written first by a human, run red then green, and pre-registered

## Context

How is "the change works" judged independently, when coding agents write both the code and its tests? If the capability writes its own acceptance tests, or sees every test it is scored on, a pass proves little. And if tests can be changed or withdrawn after the run, the score can be moved.

## Decision

**Layered acceptance, with a four-layer acceptance test model at its core:** business-language test cases and a DSL, written by a human before the run; protocol drivers built by the capability; and a deterministic check that drivers only use public APIs, events or the UI. In the D6 dry run on DEV-1, which happens before the capability exists, protocol drivers (starting with the stub driver) are built by Andy with Claude Code.

**Acceptance tests are an input,** written by Andy with Claude Code using the D6 skill, not proposed by the capability. **They come first, as the definition of done.** Reference acceptance tests are written for every outcome before the capability is built. The visible examples, plus the quality layers and ADR checks, form the definition of done the capability works to. Hidden examples are not part of the definition of done; they are used only for scoring.

**Acceptance test-driven development at system level.** Every acceptance test must fail against the subject before the change (red). For evaluation outcomes, "before" is the evaluation baseline tag (ADR-002@v2 C5). For development outcomes, every test must also pass after the change (green). For evaluation outcomes, passing is the result being measured, not a requirement on the test.

**Visible and hidden examples.** Each outcome includes a few business-language examples the capability sees (specification by example), plus hidden examples it never sees, used to check that it generalised rather than fitted to the visible ones.

**No reference implementations for evaluation outcomes.** They exist only for development outcomes on the exemplar (ADR-005@v3), to prove the test approach, the DSL and the D6 skill before any scored run. Building seven by hand roughly doubles the work. The cost is that satisfiability is only shown after the scored run; the pre-registered withdrawal criteria contain that risk.

**Test the tests** with mutation testing (for example Stryker.NET), applied to whichever implementations pass. The D6 skill is dry-run end to end on DEV-1 before any evaluation test is written, and mutation testing is proven there first.

**Quality layers beyond functional acceptance:** the number of steps for a user to achieve the outcome, measured by journey scripts (HEART is not used, because it needs real users); accessibility; REST and API contract rules; breaking-change detection; API security; architecture rules; performance budgets; and observability coverage. Tools are chosen in Q2.

**Confirmation-bias control:** the E4 baseline runs the same tests. A test that the baseline also passes isn't discriminating.

**Sequence per evaluation outcome** (decided 8 Oct):

1. Write visible and hidden acceptance tests and labels (Phase 3).
2. Freeze the evaluation baseline tag in the fork, once our baseline work is complete (end of Phase 4).
3. Confirm the tests fail against the evaluation baseline, then pre-register everything, including the baseline tag and the withdrawal criteria.
4. Run the baseline and the capability, each from the evaluation baseline. Satisfiability is shown by any run passing a test; a test nothing passes is inspected by hand against the withdrawal criteria.
5. Mutation-test whichever implementations pass.

**Pre-registration:** hidden tests, labels, thresholds and the list of measures to be published (ADR-006@v1 C3) are committed with a hash and timestamp before the scored run, and kept in the private repository until then. Whether to anchor the pre-registration publicly, so that its date doesn't rest on trust, is open (E6).

**Withdrawal rule.** A test found defective after the run is withdrawn only with a documented reason, and the withdrawal applies to the baseline and the capability alike. What counts as defective is pre-registered, so the hand inspection in step 4 can't move the goalposts. The starting criteria, to be finalised before pre-registration: the test contradicts the outcome statement or its visible examples; it depends on behaviour outside the outcome; or it can't be satisfied through public interfaces (APIs, events or the UI).

**Publication.** Mutation scores and every withdrawal, with its reason, are published with the results, if results are published (ADR-006@v1 C3 and C4).

**Independent runs (E1b).** Evaluation outcomes run independently, each from the same baseline. E1b's "same pinned baseline" (5 Oct) is read here as the evaluation baseline tag, decided later (P4, 8 Oct).

## Constraints

- **C1:** Business-language test cases and the DSL MUST be written by a human before the run.
- **C2:** In capability and evaluation runs, protocol drivers MUST be built by the capability. In the D6 dry run, they are built by Andy with Claude Code.
- **C3:** Protocol drivers MUST use only public APIs, events or the UI.
- **C4:** Acceptance tests MUST be written by Andy with Claude Code using the D6 skill.
- **C5:** Reference acceptance tests MUST be written for every outcome before the capability is built.
- **C6:** Hidden examples MUST NOT be part of the definition of done the capability works to; they are used only for scoring.
- **C7:** Every acceptance test MUST fail against the subject before the change. For evaluation outcomes, "before" is the evaluation baseline tag.
- **C8:** Each outcome MUST include visible examples the capability sees and hidden examples it never sees.
- **C9:** Reference implementations MUST NOT be built for evaluation outcomes.
- **C10:** Implementations that pass MUST be mutation-tested.
- **C11:** Hidden tests, labels, thresholds and the list of measures to be published MUST be committed with a hash and timestamp before the scored run, and kept in the private repository until then.
- **C12:** The definition of done MUST include the visible examples, the quality layers listed above and the ADR checks.
- **C13:** The E4 baseline MUST run the same tests as the capability.
- **C14:** Evaluation tests MUST be confirmed failing against the evaluation baseline before they are pre-registered.
- **C15:** A test MUST be withdrawn only against the pre-registered criteria, with a documented reason.
- **C16:** Mutation testing MUST be proven on DEV-1 before any evaluation test is written.
- **C17:** Each evaluation outcome MUST run independently, starting from the evaluation baseline (ADR-002@v2 C5, ADR-005@v3 C7).
- **C18:** Acceptance tests MUST NOT be proposed by the capability.
- **C19:** The pre-registration MUST include the evaluation baseline tag and the withdrawal criteria.
- **C20:** A withdrawal MUST apply to the baseline and the capability alike.
- **C21:** Mutation scores and every withdrawal, with its reason, MUST be published with the results, if results are published.
- **C22:** For development outcomes, every acceptance test MUST pass after the change.
- **C23:** The D6 skill MUST be dry-run end to end on DEV-1 before any evaluation test is written.

## Consequences

Easier:

- A pass means the capability met tests it neither wrote nor fully saw.
- Once these rules are enforced, tests can't be changed or dropped after the run without a pre-registered reason. Which runs count is for E6 to settle. Today every constraint here is planned or held by review.
- Test strength is measured, not assumed.

Harder:

- All tests and labels must exist, and be confirmed red, before the scored run: a large amount of work in Phases 3 and 4.
- Satisfiability isn't known until after the run, because there are no reference implementations for evaluation outcomes.
- The labels and tests reflect one person's view. A second reviewer on a sample is open (E1, E2).
- Until the pre-registration is anchored publicly, its date rests on trust in a private repository.

## Alternatives

### Do nothing: let the coding agents write and run their own tests (added when writing this ADR)

- For: no test-writing work for Andy.
- Against: the problem this ADR exists to solve. The agents mark their own homework.

### Naive: an LLM judges whether the change meets the outcome (added when writing this ADR)

- For: cheap, and needs no tests.
- Against: probabilistic where a deterministic test works, and unrepeatable.

### Reference implementations for every evaluation outcome (recorded in E2)

- For: proves every test can be satisfied before the scored run.
- Against: roughly doubles the work. The pre-registered withdrawal criteria contain the risk instead.

### HEART metrics for the journey layer (recorded in E2)

- For: an established user-experience framework.
- Against: needs real users, which this project doesn't have. Journey scripts count steps instead.

### Human-written, red-first, pre-registered tests with visible and hidden examples (chosen)

- For: independent of the agents, fixed before the run, and measures generalisation.
- Against: a large amount of work up front, and satisfiability is only shown after the run.

## Enforcement

Nothing here is enforced yet. C3, C7, C10, C11, C13, C14, C17, C20 and C22 are mechanical and become checks as the test harness, the pre-registration and the evaluation runner are built (D6, E6). The rest concern who writes what, and when, and are held by review. Hidden tests and labels are private, and Claude never reads them (hard rule 1), so checks on their content can only run in the private repository.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording E2's decided part (5 and 8 Oct), D6's DEV-1 dry run and mutation-testing decisions (8 Oct), and E1b's independent-runs decision. Rulings by Andy in chat on 21 Oct, from review of this ADR: "pass after" applies to development outcomes only; drivers are built by Andy in the D6 dry run and by the capability in runs; mutation testing covers implementations that pass; publication is conditional on ADR-006; the list of measures is pre-registered; tier `cross-cutting` and exceptions `not-allowed`.
