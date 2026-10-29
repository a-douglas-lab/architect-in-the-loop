---
id: ADR-016
version: 1
title: When the capability changes a legacy domain, it improves the code it touches, within a budget
status: accepted
date: 2026-10-29
decision-makers: [Andy Douglas]
scope: [capability, subject, concern:quality]
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
    mechanism: touch radius computed from the diff
    ref: null
    state: planned
  - constraint: C3
    mechanism: commit classification (structural or behavioural)
    ref: null
    state: planned
  - constraint: C4
    mechanism: existing tests run before and after each structural commit; mutation score compared
    ref: null
    state: planned
  - constraint: C5
    mechanism: budget check on each outcome, against pre-registered thresholds
    ref: null
    state: planned
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
  - constraint: C7
    mechanism: the capability's split logic (ADR-015@v1, S7)
    ref: null
    state: planned
  - constraint: C8
    mechanism: differential checks against a recorded baseline of exceptions (ratchet)
    ref: null
    state: planned
  - constraint: C9
    mechanism: review; security findings in touched code flagged
    ref: null
    state: manual
  - constraint: C10
    mechanism: tool configuration
    ref: null
    state: planned
  - constraint: C11
    mechanism: review of violation reports
    ref: null
    state: manual
  - constraint: C12
    mechanism: per-change report
    ref: null
    state: planned
  - constraint: C13
    mechanism: review
    ref: null
    state: manual
  - constraint: C14
    mechanism: review
    ref: null
    state: manual
  - constraint: C15
    mechanism: review
    ref: null
    state: manual
backlog: [Q4, G7, G10, G12]
---

# ADR-016: When the capability changes a legacy domain, it improves the code it touches, within a budget

## Context

Only Ordering is brought to the preferred state (ADR-005@v3). The other domains are legacy. When an outcome changes a legacy domain, there are three tempting answers: leave the code as it is, apply every rule absolutely, or refactor the whole domain. The first lets quality decay. The second fails changes on problems they didn't cause (G7). The third turns every outcome into a rewrite.

This ADR governs the capability, when it changes a legacy domain during an outcome. Hand-built development outcomes (DEV-1 to DEV-3) stay under CLAUDE.md hard rule 5: defects noticed are reported to Andy, not fixed (*ruled by Andy, 29 Oct*).

## Decision

**When a change touches a legacy domain, it also improves the code it touches:**

- **Scope by touch radius.** Improve only the code the change already modifies (files or methods in the diff), not the whole domain. This is deterministic: computed from the diff.
- **Separate structural from behavioural change.** Improvements go in their own commits, which must not change behaviour: existing tests stay green before and after, and the mutation score doesn't fall. Prior art: Kent Beck's "Tidy First?".
- **Budget, not target.** Improvement effort is capped as a share of the outcome, for example structural diff relative to behavioural diff, or a share of the token budget. Lines changed is used only as a budget proxy, never as a measure of value, because it rewards churn. Thresholds are pre-registered, like E3's.
- **Over budget becomes a follow-up.** Improvements beyond the budget are proposed as a separate improvement outcome for the architecture coordinator, rather than done inline (ADR-015@v1, S7).
- **Checks on legacy domains are differential** (G7). A baseline of existing violations is recorded as exceptions (G12), with a ratchet: the count can fall, but never rise.
- **Security defects in touched code are never ratcheted silently** (G10). They are fixed as their own behavioural change with a test and flagged, or escalated.

**Measure with existing tools, not bespoke metrics:**

- Roslyn analyzers, with severities versioned in `.editorconfig`.
- Microsoft's code metrics: complexity, maintainability and coupling.
- SonarAnalyzer.CSharp, which runs in a normal build, so it works headlessly for agents and CI. Its licence must be checked before it is adopted. SonarQube for IDE (formerly SonarLint) is IDE-only, so it suits Andy's own editing, not the pipeline.
- Coverage via coverlet; mutation score via Stryker.NET.

**One output format: SARIF.** The ratchet, the repair loop and GitHub code scanning consume one format, so any tool can be swapped without changing the capability. **Rule IDs feed the repair loop,** as ADR IDs do: a violation names its rule, and the agent repairs against it.

**Measure value by what got better.** Primary: the ratchet delta, meaning violations of the exemplar's rules removed in the touched code. Secondary: complexity, coverage and mutation score of the touched code, plus coupling and duplication. Hotspots, code that changes often and is complex, are prioritised, after Adam Tornhill.

**Report the review burden:** the reviewable size of each change, alongside the improvement it bought. The burden is accepted for now; reducing it is an improvement goal, not a launch requirement.

**No outcome claims.** Fewer defects or faster future changes would need real history, which we won't have. The repo says so.

## Constraints

- **C1:** When the capability changes a legacy domain, it MUST also improve the code the change touches.
- **C2:** Improvement MUST be limited to the code the change already modifies (files or methods in the diff).
- **C3:** Improvements MUST be made in their own commits, separate from behavioural changes.
- **C4:** An improvement commit MUST NOT change behaviour: existing tests stay green before and after, and the mutation score doesn't fall.
- **C5:** Improvement effort MUST be capped by a budget, with thresholds pre-registered.
- **C6:** Lines changed MUST NOT be used as a measure of value.
- **C7:** Improvements beyond the budget MUST be proposed as a separate improvement outcome, not done inline.
- **C8:** Checks on legacy domains MUST be differential: existing violations recorded as exceptions, with a count that may fall but MUST NOT rise.
- **C9:** A security defect in touched code MUST NOT be ratcheted silently; it MUST be fixed as its own behavioural change with a test and flagged, or escalated.
- **C10:** Analysis tools MUST report in SARIF.
- **C11:** Each violation MUST name the rule it breaks, for the repair loop.
- **C12:** The reviewable size of each change MUST be reported alongside the improvement it bought.
- **C13:** The project MUST NOT claim fewer defects or faster future changes from these improvements.
- **C14:** SonarAnalyzer.CSharp MUST NOT be adopted until its licence has been checked.
- **C15:** This ADR MUST NOT be applied to hand-built development outcomes; for them, defects are reported, not fixed (hard rule 5).

## Consequences

Easier:

- Legacy code gets better where change happens, without rewrites.
- Changes aren't failed for problems they didn't cause.
- Tools can be swapped behind SARIF.

Harder:

- Every legacy domain needs a recorded baseline of violations before the ratchet works (Q4, Phase 4; the exception record format is decided with Q1).
- Budgets and thresholds must be set and pre-registered.
- Changes get bigger to review; the burden is reported, not reduced.

## Alternatives

### Do nothing: leave legacy code as it is (added when writing this ADR)

- For: smallest changes.
- Against: quality decays wherever change happens.

### Naive: tell the agent to "clean up as you go" (added when writing this ADR)

- For: no rules to build.
- Against: unbounded scope, structural and behavioural change mixed, and nothing measurable.

### Absolute checks on every domain (recorded in G7)

- For: one rule everywhere.
- Against: fails changes on violations they didn't cause.

### Improve the whole domain when it's touched (recorded in Q4: "not the whole domain")

- For: the domain reaches the preferred state.
- Against: every outcome becomes a rewrite.

### Bespoke quality metrics (recorded in Q4: "existing tools, not bespoke metrics")

- For: fit exactly what we want to measure.
- Against: unfamiliar to reviewers, and more to build and defend.

### Touch radius, separate commits, budget, differential ratchet, SARIF (chosen)

- For: improvement that is bounded, measurable and reviewable.
- Against: needs baselines, budgets and tool set-up before it works.

## Enforcement

Nothing here is enforced yet: the capability, the tool set-up and the baselines don't exist. C2 to C5, C7, C8, C10 and C12 are designed as checks in the capability and its pipeline. The rest rely on review.

## History

- **v1** · 2026-10-29 · accepted · Andy Douglas: first version, recording Q4 (decided 5 Oct). Rulings by Andy on 29 Oct: the ADR governs the capability only, and hand-built work stays under hard rule 5 (C15); tier `cross-cutting` and exceptions `not-allowed`.
