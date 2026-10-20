---
id: ADR-005
title: Ordering is the exemplar domain, brought to the preferred state first
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [project, subject, domain:ordering]
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
    mechanism: review; the overlap check is held privately
    ref: null
    state: manual
  - constraint: C3
    mechanism: existing tests stay green, plus review against the approved spec
    ref: null
    state: manual
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
  - constraint: C5
    mechanism: check that a new domain's structure matches the exemplar's template
    ref: null
    state: planned
backlog: [P9, G13]
---

# ADR-005: Ordering is the exemplar domain, brought to the preferred state first

## Context

Before the capability is built, the whole toolchain needs a dry run: Spec Kit, enforcement, quality layers and the acceptance test skill (T1, Q1, Q2, D6). New domains need a template to follow (G13). And the capability needs an example of a well-governed domain to learn conventions from, as working code rather than prose.

## Decision

Bring one existing domain to the preferred state first: a constitution and specs, ADRs with enforcement, build and CI checks, acceptance tests in the four-layer model, and instrumentation. Then apply the development outcomes DEV-1 to DEV-3 to it by hand, with Claude Code, as reference implementations.

The exemplar is **Ordering**. It is the most thorough eShop domain, with domain and infrastructure projects and domain events, and most outcomes touch it. Exactly which projects belong to Ordering, and which contexts sit next to it, are subject ADRs, written in the fork in Phase 2 (ADR-003).

The other domains stay as they are. A part-modernised, part-legacy system is realistic. Whether the capability applies the exemplar's conventions to legacy domains becomes a test in itself.

## Constraints

- **C1:** Work built into the exemplar by hand MUST come from a development outcome (DEV-1 to DEV-3).
- **C2:** Evaluation outcomes MUST NOT be applied to the exemplar, or to any other part of the subject, before the scored run.
- **C3:** Exemplar work MUST NOT change existing eShop behaviour outside an approved spec. Defects noticed MUST be reported to Andy, not fixed.
- **C4:** Domains other than Ordering MUST stay as they are, except through approved outcomes.
- **C5:** New domains MUST follow the template the exemplar produces (G13).

## Consequences

Easier:

- Tooling decisions get evidence from a real domain, not opinion.
- New-domain outcomes have a concrete template to follow and be checked against.

Harder:

- Phase 4 is a large piece of work before the capability exists.
- Some existing behaviour is deliberately left in place for evaluation (the details are private), so "fixing" it would damage the evaluation. C3 guards this.

## Alternatives

### Do nothing: build the capability against eShop as it is

- For: faster to start.
- Against: no dry run of the toolchain, no domain template, and nothing for the capability to learn conventions from.

### Naive: describe the preferred state in prose and prompts

- For: cheap.
- Against: untested conventions, which is the prompt-and-hope approach again.

### Bring every domain to the preferred state

- For: a uniform system.
- Against: far more work, and it removes the legacy-domain test.

### A different exemplar domain (Catalog or Basket)

- For: smaller, so quicker.
- Against: thinner domains, touched by fewer outcomes, so a weaker dry run.

### Ordering as the only exemplar (chosen)

- For: the richest domain, touched by most outcomes, and it leaves legacy domains to test against.
- Against: a large piece of work up front.

## Enforcement

C1 to C4 rely on review, the approved specs and CLAUDE.md hard rules 2 and 5. C2 is also checked privately against the outcome overlap matrix. C5 becomes a structural check once the exemplar's template exists (Phase 4).
