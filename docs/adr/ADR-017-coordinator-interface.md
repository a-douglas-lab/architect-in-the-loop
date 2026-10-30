---
id: ADR-017
version: 1
title: The architecture coordinator works through a web interface, React over a C# REST API
status: accepted
date: 2026-10-29
decision-makers: [Andy Douglas]
scope: [capability]
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
    mechanism: review of the capability's project structure
    ref: null
    state: manual
  - constraint: C4
    mechanism: review of the capability's project structure
    ref: null
    state: manual
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
backlog: [P5, T5]
---

# ADR-017: The architecture coordinator works through a web interface, React over a C# REST API

## Context

Someone has to state outcomes and act at the capability's approval points. In this project that is the architecture coordinator, acting on behalf of merchant needs. Merchants are a source of business needs, not users of the capability (product.md, personas).

## Decision

**Merchants do not change the system.** The architecture coordinator states outcomes, on behalf of merchant needs, through a web interface: a **React frontend over a C# REST API**.

Still open:

- How thin the interface can be (D1 cost), and what it shows at each human approval point (P5a, A1).
- Whether agent orchestration also runs in .NET (driving Claude Code through its command-line interface), or in a small TypeScript or Python worker using the Claude Agent SDK, called from the C# API (T5).
- Where merchants configure values inside the subject system, which is a separate question (P5b).

## Constraints

- **C1:** Merchants MUST NOT change the system.
- **C2:** The architecture coordinator MUST state outcomes through a web interface.
- **C3:** The capability's API MUST be a C# REST API.
- **C4:** The capability's frontend MUST be built with React.
- **C5:** The architecture coordinator MUST state outcomes on merchants' behalf.

## Consequences

Easier:

- One clear human role at the capability's front door.

Harder:

- A web interface is extra work before any outcome can be stated; how thin it can be is open.
- If orchestration ends up in TypeScript or Python (T5), the capability spans two stacks.

## Alternatives

### Do nothing: outcomes stated as files or tickets, no interface (added when writing this ADR)

- For: no front end to build.
- Against: no place to show impact, decisions and checks at approval points.

### A command-line interface only (added when writing this ADR)

- For: cheap.
- Against: approval points need to show evidence an engineer reviewer can scan; a terminal suits that poorly.

### A merchant-facing interface (added when writing this ADR)

- For: closer to the business need.
- Against: contradicts the decision that merchants don't change the system.

### React over a C# REST API, for the coordinator (chosen)

- For: a web interface for evidence at approval points, on the subject's stack.
- Against: front-end work, and the orchestration language is still open.

The naive option (an LLM with everything in its prompt) doesn't apply to an interface choice.

## Enforcement

All five constraints rely on review. Nothing is built yet. C3 and C4 become checkable from the capability's project structure once it exists.

## History

- **v1** · 2026-10-29 · accepted · Andy Douglas: first version, recording P5a and T5's decided part (5 Oct). Tier `cross-cutting` and exceptions `not-allowed` as ruled by Andy on 29 Oct.
