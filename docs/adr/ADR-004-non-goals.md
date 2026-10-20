---
id: ADR-004
title: "Non-goals: no shopper-facing AI, no multi-tenancy, no custom coding agent"
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [capability, subject, project]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: review of every spec against this ADR
    ref: null
    state: manual
  - constraint: C2
    mechanism: review of every spec against this ADR
    ref: null
    state: manual
  - constraint: C3
    mechanism: review
    ref: null
    state: manual
  - constraint: C4
    mechanism: test that the AppHost starts with Foundry and Ollama disabled
    ref: subject/eshop/src/eShop.AppHost/AppHost.cs
    state: planned
backlog: [P7, T4]
---

# ADR-004: Non-goals: no shopper-facing AI, no multi-tenancy, no custom coding agent

## Context

The project is about governing change across a multi-domain system. Three tempting directions would dilute that or multiply the work: AI features for shoppers, multi-tenancy in the subject system, and writing our own coding agent. eShop also ships optional AI features of its own (catalogue semantic search, and a storefront chat), which are Microsoft's work, not ours.

## Decision

These are non-goals:

- **No shopper-facing AI features,** such as a shopping chatbot.
- **No multi-tenancy** in the subject system.
- **No custom coding agent.** The capability orchestrates existing coding agents, such as Claude Code (T4).

eShop's optional AI features stay switched off, and the README says they are eShop's.

## Constraints

- **C1:** Specs MUST NOT add shopper-facing AI features.
- **C2:** Specs MUST NOT add multi-tenancy to the subject system.
- **C3:** The capability MUST orchestrate existing coding agents, and MUST NOT implement its own.
- **C4:** eShop's AI features MUST stay disabled: `UseFoundry` not enabled, and `useOllama` false in the AppHost.

## Consequences

Easier:

- Effort stays on governance, impact analysis and evaluation, where the portfolio's originality is.
- The evaluation compares governance with plain Claude Code, not one agent with another.

Harder:

- The capability depends on an external agent's behaviour and interfaces, which can change (T4).
- Some merchant outcomes that would naturally use AI are out of scope.

## Alternatives

### Do nothing: decide case by case

- For: flexible.
- Against: scope creep, one reasonable-looking feature at a time.

### Naive: build whatever makes the best demo

- For: an impressive video.
- Against: shopper-facing AI and a custom agent are both crowded spaces, and neither shows governance.

### Agreed non-goals (chosen)

- For: a clear scope, and a reason to say no.
- Against: rules out some appealing demonstrations.

## Enforcement

C1 to C3 need judgement and stay with review. C4 is mechanical: a planned test that the AppHost configuration keeps both AI switches off. Today `useOllama` is hard-coded false and Foundry is off unless configured.
