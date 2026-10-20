---
id: ADR-003
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
    mechanism: CI check that the capability's code doesn't contain the subject's path
    ref: null
    state: planned
backlog: [P3]
---

# ADR-003: Subject-side artefacts live with the subject's code, in the fork

## Context

Some artefacts describe the subject system rather than the capability: the subject contract, the subject's ADRs, per-domain spec folders, and the development acceptance tests. They need one home. If they lived in this repo, the capability's repo would hold subject knowledge, making ADR-001 harder to check. It would also be unlike a real team, which keeps its decisions with its code.

## Decision

Subject-side artefacts live in the eShop fork, with the code they describe. The capability is given the contract's location at run time and never hard-codes the subject's path.

## Constraints

- **C1:** The subject contract, the subject's ADRs, per-domain spec folders and the development acceptance tests MUST live in the eShop fork, not in this repo.
- **C2:** The capability MUST find the subject through a contract location it is given, and MUST NOT hard-code the subject's path.

## Consequences

Easier:

- ADR-001's "no subject knowledge in the capability" rule can be checked by where files live, not only by what they say.
- The subject looks like a real team's repository, with its decisions beside its code.

Harder:

- Work often spans two repos, each with its own Spec Kit set-up. Subject-side stages run with the fork as the project root (first noted on the DEV-1 specify loop card).
- The evaluation's held-out material stays in a third, private repo, so three repos are in play.

## Alternatives

### Do nothing: keep subject artefacts wherever they are first written

- For: no rule to follow.
- Against: they would end up scattered between repos, and ADR-001 couldn't be checked.

### Naive: keep everything in this repo

- For: one place to look.
- Against: puts subject knowledge in the capability's repo, which is what ADR-001 forbids.

### Subject artefacts in the fork (chosen)

- For: realistic, and makes ADR-001 checkable by location.
- Against: two repos to work across.

## Enforcement

C1 and C2 are planned CI checks (Step 7). Until then they rely on review and CLAUDE.md hard rule 4.
