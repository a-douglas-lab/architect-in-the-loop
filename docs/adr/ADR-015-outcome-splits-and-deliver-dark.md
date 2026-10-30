---
id: ADR-015
version: 1
title: Outcomes may split by nine known scenarios; partial work is delivered dark
status: accepted
date: 2026-10-29
decision-makers: [Andy Douglas]
scope: [capability, concern:delivery]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: review against the scenario table
    ref: null
    state: manual
  - constraint: C2
    mechanism: the capability's split check
    ref: null
    state: planned
  - constraint: C3
    mechanism: the capability's split check (visible acceptance examples for the delivered part)
    ref: null
    state: planned
  - constraint: C4
    mechanism: the capability's split check (contract dependency graph, G1)
    ref: null
    state: planned
  - constraint: C5
    mechanism: the capability's approval points; for work delivered dark, the flag switch
    ref: null
    state: planned
  - constraint: C6
    mechanism: the capability's split check (risk rung)
    ref: null
    state: planned
  - constraint: C7
    mechanism: the capability's split check
    ref: null
    state: planned
  - constraint: C8
    mechanism: the capability's split check, confirming the delivered feature's flag is off
    ref: null
    state: planned
  - constraint: C9
    mechanism: the capability's approval points
    ref: null
    state: planned
  - constraint: C10
    mechanism: the capability's split check (contract dependency graph, G1)
    ref: null
    state: planned
  - constraint: C11
    mechanism: the capability's approval points
    ref: null
    state: planned
  - constraint: C12
    mechanism: review against the scenario table
    ref: null
    state: manual
  - constraint: C13
    mechanism: the capability's split check
    ref: null
    state: planned
  - constraint: C14
    mechanism: the capability's split logic
    ref: null
    state: planned
backlog: [A4, G11]
---

# ADR-015: Outcomes may split by nine known scenarios; partial work is delivered dark

## Context

An outcome can be blocked in part: a decision gap, an ADR conflict, an ambiguous request, or a failing part (scenarios S1 to S4 below). Splitting lets unblocked work continue (G11). But a split changes what the merchant gets, so whether it can happen automatically depends on why it happens.

## Decision

**The nine scenarios below are complete.**

| # | Scenario | Example | What changes for the merchant | Decision |
| --- | --- | --- | --- | --- |
| S1 | Decision gap blocks part of the outcome | A refund rule nobody has decided yet | They get less than they asked for | Automatic, delivered dark; switching on needs the coordinator |
| S2 | ADR conflict blocks part | Part of an outcome needs a synchronous call to another service | They get less than they asked for | Automatic, delivered dark; switching on needs the coordinator |
| S3 | One part is ambiguous, the rest is clear | Loyalty: earning rules clear, redemption unclear | Nothing yet; risk of rework if the answer changes the design | Automatic for parts that don't depend on the answer |
| S4 | One independent part fails and escalates (G8) | Webhook part done, storefront part failing | They may get a part that makes no sense alone | Automatic, delivered dark; switching on needs the coordinator |
| S5 | Delivered part depends on the blocked part | Storefront needs a contract the blocked domain hasn't agreed (G1) | n/a | Not splittable: the dependency graph forbids it |
| S6 | Planned staging of a large outcome | Loyalty: charter, scaffold, earning, then redemption | Nothing: all of it arrives, in steps | Approved once as part of the plan; each step then automatic |
| S7 | Improvement work over budget (Q4) | Refactoring beyond the touch-radius budget | Nothing | Automatic proposal of a follow-up outcome; the follow-up needs approval |
| S8 | Out-of-scope security defect (G10) | A gap found in code next to the change | Nothing directly | Automatic proposal of a remediation outcome; flagged immediately |
| S9 | Preparatory change needed first | A calculation an outcome depends on must be corrected first | Nothing, if behaviour-preserving | Automatic if structural; approval if it changes behaviour |

**Deliver dark:** partial features ship behind feature flags, switched off, so nothing changes for users and splitting can be automatic. Switching a flag on is the human decision. The cost is a feature flag capability in the subject system, which eShop has none of today. The flag mechanism itself (OpenFeature, Q5) is a subject decision, to be recorded in the fork in Phase 2 (ADR-000@v3 C12).

**Rules for an automatic split,** all checked deterministically:

1. The delivered part passes its own subset of the visible acceptance examples.
2. Nothing in the delivered part depends on the blocked part (contract dependency graph, G1).
3. The split doesn't reduce what the outcome asked for. Any reduction in what the merchant gets needs a human; with deliver dark, that happens when the flag is switched on.
4. The delivered part's risk rung is no higher than the original outcome's. Risk rungs are the use-case ladder in the architecture sketch, which is still a proposal (A1).
5. The system is left consistent: no half-built feature visible to users.

For evaluation, outcomes expected to split are labelled by part (ADR-007@v1 C10).

**Open (A1):** which rule applies when a security defect is in touched code (ADR-016@v1 C9, fixed with a test and flagged) and also needed first (S9, approval if it changes behaviour).

## Constraints

- **C1:** Every split MUST fall under one of the scenarios S1 to S9.
- **C2:** A split MUST NOT be made automatically unless all five rules hold, each checked deterministically.
- **C3:** In an automatic split, the delivered part MUST pass its own subset of the visible acceptance examples.
- **C4:** In an automatic split, the delivered part MUST NOT depend on the blocked part.
- **C5:** A reduction in what the merchant gets MUST be approved by a human. For work delivered dark, that happens when the flag is switched on.
- **C6:** In an automatic split, the delivered part's risk rung MUST NOT be higher than the original outcome's.
- **C7:** An automatic split MUST leave no half-built feature visible to users.
- **C8:** Partial features MUST be delivered behind feature flags, switched off.
- **C9:** Switching a feature flag on MUST be a human decision.
- **C10:** A split where the delivered part depends on the blocked part (S5) MUST NOT be made, automatically or otherwise.
- **C11:** A follow-up outcome proposed for over-budget improvement work (S7) MUST be approved.
- **C12:** A split MUST follow the decision recorded for its scenario.
- **C13:** An automatic split MUST NOT reduce what the outcome asked for.
- **C14:** An out-of-scope security defect (S8) MUST be flagged immediately, and a remediation outcome proposed automatically.

## Consequences

Easier:

- Unblocked work continues without waiting on every open question.
- Nothing a merchant sees changes until a human switches it on.

Harder:

- The subject system needs a feature flag capability first.
- Every split needs the contract dependency graph (G1, Q3) to be right; a wrong graph allows a bad split.
- Flags left on or off too long become debt (Q5's lifecycle question).

## Alternatives

### Do nothing: never split; the whole outcome waits (added when writing this ADR)

- For: simple, and nothing partial ever ships.
- Against: one open question blocks everything else.

### Naive: the agent decides when and how to split (added when writing this ADR)

- For: flexible.
- Against: no deterministic check that a split is safe, and the merchant can get less than asked without anyone deciding.

### Every split needs human approval (added when writing this ADR)

- For: full control.
- Against: makes every blocked part a human interruption, even when delivering dark changes nothing for users.

### Nine scenarios, five deterministic rules, deliver dark (chosen)

- For: automatic where nothing changes for users; a human wherever the merchant would get less.
- Against: needs feature flags and a trustworthy dependency graph.

## Enforcement

Nothing here is enforced yet: the capability doesn't exist. C2 to C4, C6 to C8, C10, C13 and C14 are intended as deterministic checks in the capability's split logic. C5, C9 and C11 are approval points. C1 and C12 are held by review until the split logic records which scenario applies.

## History

- **v1** · 2026-10-29 · accepted · Andy Douglas: first version, recording A4 (decided 5 Oct). Tier `cross-cutting` and exceptions `not-allowed` as ruled by Andy on 29 Oct.
