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
    mechanism: review of the rubric catalogue (A5)
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
backlog: [A2, A5]
---

# ADR-014: Two graders, runtime and evaluation, kept separate

## Context

Some qualities of the capability's work can't be checked deterministically: whether an impact set's reasoning is sound, whether a spec captures the outcome's intent, whether a trade-off is explained clearly to a merchant. A grader, a model scoring work against a rubric, covers that residue. A grader is used for two different jobs. One is checking work before a human sees it, during a run. The other is scoring outcomes for the evaluation (E1 to E4). If one grader did both, tuning it to help the capability would also move the evaluation's scores.

This ADR is about the capability's graders. It is not about the adversarial reviewer that checks this project's own documentation (ADR-012).

## Decision

**Two graders, kept separate.** A **runtime grader** checks work before a human sees it. An **evaluation grader** scores outcomes for E1 to E4. They use separate rubrics and are calibrated separately, and human labels remain the final check on the evaluation grader. Rubrics are catalogued in A5.

Still open (A2; A5 proposes answers to several):

- **Scope:** under the thesis, the grader covers only what deterministic checks can't.
- **Independence:** the grader sees the artefacts, the rubric and the outcome statement, not the producing agent's reasoning. Whether a different model or model family is used, to reduce self-preference bias.
- **Calibration:** rubrics versioned as code, with agreement with human labels measured and published before scores are trusted.
- **Consequences:** whether a low grade blocks, triggers a bounded repair loop, or only flags for the human reviewer, and the loop limit.
- **Cost:** where the grader earns its cost.

## Constraints

- **C1:** A runtime grader MUST check the capability's work before a human sees it.
- **C2:** A separate evaluation grader MUST score outcomes for E1 to E4.
- **C3:** The two graders MUST use separate rubrics.
- **C4:** The two graders MUST be calibrated separately.
- **C5:** Human labels MUST remain the final check on the evaluation grader.
- **C6:** Rubrics MUST be catalogued in A5.

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
- Against: every judgement lands on the human, which review capacity can't sustain (ADR-010).

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

All six constraints rely on review today. Neither grader exists yet. C3 and C4 become checkable once the rubric catalogue and calibration records exist (A5).

## History

- **v1** · 2026-10-29 · accepted · Andy Douglas: first version, recording A2's decided part (5 Oct). Tier `cross-cutting` and exceptions `not-allowed` as ruled by Andy on 29 Oct (ADR-000@v3 C13 applies to capability ADRs).
