---
id: ADR-014
version: 1
title: Two graders, runtime and evaluation, kept separate
status: accepted
date: 2026-10-29
decision-makers: [Andy Douglas]
scope: [capability, concern:evaluation]
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
    mechanism: review; evaluation rubrics are private, so only Andy can compare the two sets
    ref: null
    state: manual
  - constraint: C4
    mechanism: review of the calibration records
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
    mechanism: review
    ref: null
    state: manual
backlog: [A2, A5]
---

# ADR-014: Two graders, runtime and evaluation, kept separate

## Context

Some qualities of the capability's work can't be checked deterministically: whether an impact set's reasoning is sound, whether a spec captures the outcome's intent, whether a trade-off is explained clearly to a merchant. A grader, a model scoring work against a rubric, covers that residue. A grader is used for two different jobs. One is checking work before a human sees it, during a run. The other is scoring outcomes for the evaluation (E1 to E4). If one grader did both, tuning it to help the capability would also move the evaluation's scores.

This ADR is about the capability's graders. It is not about the adversarial reviewer that checks this project's own documentation (ADR-012).

## Decision

**Two graders, kept separate.** A **runtime grader** checks work before a human sees it. An **evaluation grader** scores outcomes for E1 to E4. They use separate rubrics and are calibrated separately, and human labels remain the final check on the evaluation grader. Rubrics are catalogued in A5. Runtime rubrics live in this public repository, because they define quality for the capability, as visible examples do. Evaluation rubrics live in the private evaluation repository, so the capability can't tune itself to them.

The evaluation grader doesn't replace deterministic scoring: impact is scored by a deterministic comparison with no LLM (ADR-007@v1 C7), and acceptance by tests (ADR-008@v1).

Still open (A2; A5 proposes answers to several):

- **Scope:** under the thesis, the grader covers only what deterministic checks can't. For impact scoring, ADR-007 has already settled this. Where else it applies, and at which points the runtime grader runs, is open.
- **Independence:** the grader sees the artefacts, the rubric and the outcome statement, not the producing agent's reasoning. Whether a different model or model family is used, to reduce self-preference bias.
- **Calibration:** rubrics versioned as code, with agreement with human labels measured and published before scores are trusted.
- **Consequences:** whether a low grade blocks, triggers a bounded repair loop, or only flags for the human reviewer, and the loop limit.
- **Cost:** where the grader earns its cost.

## Constraints

- **C1:** The capability MUST have a runtime grader that checks work before a human sees it. Which work, and at which points, is open.
- **C2:** A separate evaluation grader MUST score outcomes for E1 to E4, only where deterministic scoring doesn't apply (ADR-007@v1 C7).
- **C3:** The two graders MUST use separate rubrics.
- **C4:** The two graders MUST be calibrated separately.
- **C5:** Human labels MUST remain the final check on the evaluation grader.
- **C6:** Runtime rubrics MUST live in this public repository, catalogued in A5.
- **C7:** Evaluation rubrics MUST live in the private evaluation repository.

## Consequences

Easier:

- The runtime grader can be tuned to help the capability without moving the evaluation's scores.
- The evaluation grader stays answerable to human labels.

Harder:

- Two sets of rubrics, and two calibrations, to write and maintain.
- The open questions (independence, consequences, cost) must be settled before either grader is trusted.

## Alternatives

### Do nothing: no grader; humans judge what checks can't (added when writing this ADR)

- For: no grader to build or calibrate.
- Against: every judgement lands on the human reviewer, and nothing screens work before they see it.

### Naive: one LLM judges everything, including what checks could cover (added when writing this ADR)

- For: simple.
- Against: probabilistic where deterministic checks work, against the thesis.

### One grader for both jobs (added when writing this ADR)

- For: one rubric set and one calibration.
- Against: tuning it for the capability moves the evaluation's scores.

### Two separate graders (chosen)

- For: run-time help and evaluation scoring can't contaminate each other.
- Against: double the rubric and calibration work.

## Enforcement

All seven constraints rely on review today. Neither grader exists yet. The runtime side of C4 becomes checkable once calibration records exist (A5). Evaluation rubrics and their calibration are private, and Claude never reads them (hard rule 1), so C3, C5, C7 and the evaluation side of C4 can only be checked by Andy.

## History

- **v1** · 2026-10-29 · accepted · Andy Douglas: first version, recording A2's decided part (5 Oct). Tier `cross-cutting` and exceptions `not-allowed` as ruled by Andy on 29 Oct (ADR-000@v3 C13 applies to capability ADRs).
