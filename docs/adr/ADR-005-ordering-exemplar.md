---
id: ADR-005
version: 3
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
    mechanism: review
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
  - constraint: C6
    mechanism: review of each development outcome's diff against its listed areas
    ref: null
    state: manual
  - constraint: C7
    mechanism: review, then the evaluation runner (E6)
    ref: null
    state: manual
backlog: [P9, G13]
---

# ADR-005: Ordering is the exemplar domain, brought to the preferred state first

## Context

Before the capability is built, the whole toolchain needs a dry run: Spec Kit, enforcement, quality layers and the acceptance test skill (T1, Q1, Q2, D6). New domains need a template to follow (G13). And the capability needs an example of a well-governed domain to learn conventions from, as working code rather than prose.

## Decision

Bring one existing domain to the preferred state first: a constitution and specs, ADRs with enforcement, build and CI checks, acceptance tests in the four-layer model, and instrumentation. Then apply the development outcomes DEV-1 to DEV-3 to it by hand, with Claude Code, as reference implementations.

The exemplar is **Ordering**. It is the most thorough eShop domain, with domain and infrastructure projects and domain events, and most outcomes touch it. Exactly which projects belong to Ordering, and which contexts sit next to it, are subject ADRs (ADR-000@v2), written in the fork in Phase 2.

The other domains stay as they are: they are not brought to the preferred state. Development outcomes may still change the areas listed for them in [development-outcomes.md](../outcomes/development-outcomes.md), such as the storefront checkout for DEV-1 and the webhook payload for DEV-2. Evaluation outcomes are never built by hand; only the capability applies them, in evaluation runs. A part-modernised, part-legacy system is realistic. Whether the capability applies the exemplar's conventions to legacy domains becomes a test in itself.

## Constraints

- **C1:** Work built into the exemplar by hand MUST come from a development outcome (DEV-1 to DEV-3).
- **C2:** Evaluation outcomes MUST NOT be built by hand, in the exemplar or anywhere else in the subject.
- **C3:** Exemplar work MUST NOT change existing eShop behaviour outside an approved spec. Defects noticed MUST be reported to Andy, not fixed.
- **C4:** Domains other than Ordering MUST NOT be brought to the preferred state.
- **C5:** New domains MUST follow the template the exemplar produces (G13).
- **C6:** A development outcome MUST change only the areas listed for it in development-outcomes.md (CLAUDE.md hard rule 2).
- **C7:** The capability MUST apply evaluation outcomes only in evaluation runs, from the evaluation baseline (ADR-002@v2 C5).

## Consequences

Easier:

- Tooling decisions get evidence from a real domain, not opinion.
- New-domain outcomes have a concrete template to follow and be checked against.

Harder:

- Phase 4 is a large piece of work before the capability exists.
- Some existing behaviour is deliberately left in place for evaluation (the details are private), so "fixing" it would damage the evaluation. C3 guards this.

## Alternatives

### Do nothing: build the capability against eShop as it is (added when writing this ADR)

- For: faster to start.
- Against: no dry run of the toolchain, no domain template, and nothing for the capability to learn conventions from.

### Naive: describe the preferred state in prose and prompts (added when writing this ADR)

- For: cheap.
- Against: untested conventions, which is the prompt-and-hope approach again.

### Bring every domain to the preferred state (added when writing this ADR)

- For: a uniform system.
- Against: far more work, and it removes the legacy-domain test.

### A different exemplar domain, such as Catalog or Basket (added when writing this ADR)

- For: smaller, so quicker.
- Against: thinner domains, touched by fewer outcomes, so a weaker dry run.

### Ordering as the only exemplar (chosen)

- For: the most thorough domain, touched by most outcomes, and it leaves legacy domains to test against.
- Against: a large piece of work up front.

## Enforcement

C1 to C4 and C6 rely on review, the approved specs and CLAUDE.md hard rules 2 and 5. C6 could become a check comparing each development outcome's diff with its listed areas, once domains map to paths in the subject contract. C5 becomes a structural check once the exemplar's template exists (Phase 4). C7 is held by review until the evaluation runner (E6) exists.

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · correction · written by Claude, checked by review runs 1 and 2, merged by Andy Douglas: from review run 1 (findings 2, 3, 5, 15, 16). C4 no longer adds an untraced exception. C2 restored to the source's scope (the exemplar), with no time limit. Removed the claim that the private overlap matrix checks C2. Added C6 for hard rule 2's "only in Ordering". Alternatives added at write-up are marked.
- **v3** · 2026-10-20 · revision · approved by Andy Douglas in chat: review run 2 found that restoring the source's wording made rules nobody intends. C4: other domains aren't brought to the preferred state (not "stay exactly as they are"). C6: a development outcome changes only its listed areas, matching DEV-1's storefront and DEV-2's webhook changes. C2: evaluation outcomes are never built by hand. C7 added: the capability applies them only in evaluation runs, from the baseline. Tier confirmed as `cross-cutting`, because C4 and C5 bind domains other than Ordering. CLAUDE.md hard rule 2 reworded to match.
