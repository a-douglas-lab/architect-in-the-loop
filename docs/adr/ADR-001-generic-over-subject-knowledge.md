---
id: ADR-001
version: 2
title: The capability is generic over subject knowledge and specific to one stack
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [capability, concern:portability]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: CI check failing on subject-domain terms in the capability's code and prompts
    ref: null
    state: planned
  - constraint: C2
    mechanism: review
    ref: null
    state: manual
  - constraint: C3
    mechanism: to be chosen with Q1
    ref: null
    state: manual
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
backlog: [P3]
---

# ADR-001: The capability is generic over subject knowledge and specific to one stack

## Context

The capability works on a subject system: today eShop. If knowledge of eShop leaks into the capability's code or prompts, two things break. Its results stop being evidence that governance works, because it may simply know the answers. And it stops being a capability, because it only works on one system.

Fully generic support for any stack would cost far more and risks never finishing. Full specificity to eShop is faster but reads as a one-off demo.

Criteria: the results must be credible as evidence; the scope must be finishable; and portability must be testable rather than asserted.

## Decision

The capability is generic over subject knowledge and specific to one stack. Everything it knows about a subject comes from a declared **subject contract**: domains, ADRs, schemas, and build and test commands. It targets a .NET, Aspire, event-driven stack and says so openly; stack-specific parts sit behind small adapters.

eShop is the only fully built subject. Automated onboarding of new subjects is out of scope: the eShop contract is written by hand, or extracted with human review (T8). A tiny second subject in a different domain, run with two or three outcomes, is a stretch goal, to measure portability rather than assert it. At minimum, its contract is sketched on paper to test that the contract isn't shaped like eShop.

## Constraints

- **C1:** The capability's code and prompts MUST NOT contain subject-domain knowledge, such as eShop's domain names, entities, events or business rules.
- **C2:** Everything the capability knows about a subject MUST come from that subject's declared contract.
- **C3:** Stack-specific behaviour (.NET, Aspire, the event bus) MUST sit behind adapters, not be spread through the capability's core.
- **C4:** Automated onboarding of new subjects is out of scope and MUST NOT be built. A subject's contract is written by hand, or extracted and then reviewed by a human.

## Consequences

Easier:

- The evaluation measures governance, not memorised knowledge of eShop.
- Portability can be tested with a second subject's contract, even on paper.

Harder:

- The subject contract must be designed and kept complete (T8). Anything missing from it is invisible to the capability.
- The model's general knowledge can't be removed. For example, it knows that loyalty points are a liability. So the E4 baseline must separate what governance adds from what the model already knows.

To do:

- Build the C1 CI check.
- Sketch a second subject's contract on paper.

## Alternatives

### Do nothing: let the capability learn eShop as it goes (added when writing this ADR)

- For: fastest start.
- Against: results become unfalsifiable, because the capability may have been tuned to eShop. Nothing would be portable.

### Naive: put eShop's architecture and decisions into the agents' prompts (added when writing this ADR)

- For: simple, and probably works well on eShop.
- Against: the "load decisions into a prompt and hope" approach the product exists to replace. It leaks subject knowledge into the capability by design.

### Fully generic across stacks

- For: the most impressive claim.
- Against: costs more, and risks never finishing.

### Fully specific to eShop

- For: the fastest to build.
- Against: reads as a one-off demo.

### Generic interfaces, with this subject as the only implementation and the stack made explicit (chosen)

- For: credible evidence, a finishable scope, and portability that can be measured.
- Against: the subject contract becomes a critical design artefact, and the stack limit has to be stated honestly.

## Enforcement

C1 is planned as a CI check that fails on subject-domain terms (P3). C2 and C4 need judgement and stay with review. C3 has no mechanism chosen yet; Q1 decides it once the capability has code. C4 states the scope exclusion as a rule so that it can be checked; its effect is the same as "out of scope".

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · correction · Andy Douglas: from review run 1 (findings 12, 14, 15, 19). Removed untraced details (the C1 term list derived from the contract; building C1 before the first code; an architecture test for C3). Restored the stretch goal's "two or three outcomes". Stated C4 as out of scope. Marked alternatives added at write-up, and aligned the others with P3's options-considered text.
