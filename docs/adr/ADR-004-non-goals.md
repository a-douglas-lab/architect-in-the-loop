---
id: ADR-004
version: 2
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
    mechanism: check of the configuration eShop is run with (UseFoundry not set to true)
    ref: null
    state: planned
  - constraint: C5
    mechanism: test that useOllama is false in the AppHost
    ref: null
    state: planned
backlog: [P7, T4]
---

# ADR-004: Non-goals: no shopper-facing AI, no multi-tenancy, no custom coding agent

## Context

The project is about governing change across a multi-domain system. Three directions would dilute that or multiply the work: AI features for shoppers, multi-tenancy in the subject system, and writing our own coding agent. eShop also ships optional AI features of its own (catalogue semantic search with embeddings, and a storefront chat), switched on through the AppHost. They are Microsoft's work, not ours.

## Decision

These are non-goals:

- **No shopper-facing AI features,** such as a shopping chatbot.
- **No multi-tenancy** in the subject system.
- **No custom coding agent.** The capability orchestrates existing coding agents, such as Claude Code (T4).

eShop's optional AI features stay switched off, and the README states they are eShop's, not ours.

## Constraints

- **C1:** Specs MUST NOT add shopper-facing AI features.
- **C2:** Specs MUST NOT add multi-tenancy to the subject system.
- **C3:** The capability MUST orchestrate existing coding agents, and MUST NOT implement its own.
- **C4:** eShop MUST NOT be run with Foundry enabled (`UseFoundry` set to true).
- **C5:** `useOllama` in eShop's AppHost MUST stay false.

## Consequences

Easier:

- Effort stays on governance, impact analysis and evaluation.

Harder:

- The capability depends on an external agent's behaviour and interfaces, which can change (T4).
- Some merchant outcomes that would naturally use AI are out of scope.

## Alternatives

### Do nothing: decide case by case (added when writing this ADR)

- For: flexible.
- Against: scope creep, one reasonable-looking feature at a time.

### Build whatever makes the best demo (added when writing this ADR)

- For: an impressive video.
- Against: neither shopper-facing AI nor a custom agent shows governance.

### Agreed non-goals (chosen)

- For: a clear scope, and a reason to say no.
- Against: rules out some appealing demonstrations.

The naive option (an LLM with everything in its prompt) doesn't apply to a choice of scope.

## Enforcement

C1 to C3 need judgement and stay with review. C4 and C5 are mechanical but not yet checked. For C4, `UseFoundry` is read from configuration at run time, and eShop's README shows setting it as an environment variable, so the check has to look at the configuration eShop is actually run with, not at the AppHost code. Upstream eShop's test `FoundryFlagUsesSafeOptInDefault` (`tests/eShop.AppHost.UnitTests/AppHostConfigurationTests.cs`) checks that Foundry is off unless configured. That covers the default only, not how eShop is run. For C5, `useOllama` is hard-coded false today.

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · correction · Andy Douglas: from review run 1 (findings 6, 8, 15, 20; nit 3). Removed an untraced claim about the E4 comparison, which is still open. C4 split into C4 (Foundry, checked at run time) and C5 (Ollama). `ref` no longer points at the subject file. The existing upstream test is noted as partial coverage. Alternatives added at write-up are marked, and the second one is no longer labelled as the naive option.
