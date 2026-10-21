---
id: ADR-003
version: 2
title: Subject-side artefacts live with the subject's code, in the fork
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [capability, subject, concern:portability]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: CI check that no subject contract, subject ADR, domain spec or development acceptance test exists in this repo
    ref: null
    state: planned
  - constraint: C2
    mechanism: review
    ref: null
    state: manual
  - constraint: C3
    mechanism: CI check that the capability's code doesn't contain the subject's path
    ref: null
    state: planned
backlog: [P3]
---

# ADR-003: Subject-side artefacts live with the subject's code, in the fork

## Context

Some artefacts describe the subject system rather than the capability: the subject contract, the subject's ADRs, per-domain spec folders, and the development acceptance tests. They need one home. If they lived in this repo, the capability's repo would hold subject knowledge, making ADR-001 harder to check. It would also be unlike a real team, which keeps its decisions with its code.

## Decision

Subject-side artefacts live in the eShop fork, with the code they describe. The capability is given the contract's location and never hard-codes the subject's path.

What counts as a subject ADR, as opposed to a project ADR about the subject, is defined in ADR-000@v2.

## Constraints

- **C1:** The subject contract, subject ADRs (as defined in ADR-000), per-domain spec folders and the development acceptance tests MUST live in the eShop fork, not in this repo.
- **C2:** The capability MUST find the subject through a contract location it is given.
- **C3:** The capability MUST NOT hard-code the subject's path.

## Consequences

Easier:

- ADR-001's "no subject knowledge in the capability" rule can be checked by where files live, not only by what they say.
- The subject looks like a real team's repository, with its decisions beside its code.

Harder:

- Work often spans two repos.
- The evaluation's held-out material stays in a third, private repo, so three repos are in play.

## Alternatives

### Do nothing: keep subject artefacts wherever they are first written (added when writing this ADR)

- For: no rule to follow.
- Against: they would end up scattered between repos, and ADR-001 couldn't be checked.

### Keep everything in this repo (added when writing this ADR)

- For: one place to look.
- Against: puts subject knowledge in the capability's repo, which ADR-001 forbids.

### Subject artefacts in the fork (chosen)

- For: realistic, and makes ADR-001 checkable by location.
- Against: two repos to work across.

The naive option (an LLM with everything in its prompt) doesn't apply to where files live.

## Enforcement

C1 and C3 are planned CI checks (Step 7). Until then, C1 relies on review and CLAUDE.md hard rule 4, and C3 on review alone. C2 needs judgement and stays with review.

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · correction · written by Claude, checked by review runs 1 and 2, merged by Andy Douglas: from review run 1 (findings 7, 9, 13, 15). Removed a citation of an unmerged loop card, and the claim that the fork has its own Spec Kit set-up (true only in an unpushed local commit). C1 now refers to ADR-000's definition of a subject ADR. C2 split: "no hard-coded path" is now C3. The enforcement note no longer says hard rule 4 covers hard-coded paths. Alternatives added at write-up are marked.
