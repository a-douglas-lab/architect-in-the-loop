---
id: ADR-010
version: 1
title: The working model is designed around Andy's review attention, and dogfoods the product
status: accepted
date: 2026-10-21
decision-makers: [Andy Douglas]
scope: [project, concern:delivery]
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
    mechanism: review
    ref: null
    state: manual
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
  - constraint: C5
    mechanism: commit-message check for the Co-Authored-By trailer on AI-authored commits
    ref: null
    state: planned
  - constraint: C6
    mechanism: loop cards record tokens per reviewer run; there is no budget or alert yet (open)
    ref: docs/loops/cards
    state: manual
backlog: [D1]
---

# ADR-010: The working model is designed around Andy's review attention, and dogfoods the product

## Context

With coding agents, typing is cheap and review is not. One person reviews everything in this project. A setup tuned for agent throughput would produce more than can be reviewed. The project also argues that governed AI delivery can be measured, so its own delivery should be governed and measured in the same way.

## Decision

**Andy's review attention is the bottleneck, not typing speed,** so the setup is designed around review capacity.

**Two or three parallel tracks, not five.** Track A is the critical path. Track B is research (prior-art reading and spikes). An optional track C covers chores (documentation and tooling). Each runs as a named session in the Claude Code desktop app, in its own git worktree.

**Configure once, commit to the repo:** a CLAUDE.md pointing to the constitution and conventions; skills for writing an ADR from the template, running a research spike using the backlog method, and writing acceptance tests (D6); an adversarial reviewer subagent; and hooks for deterministic gates (ADR-011).

**Build it the way the capability works (dogfooding).** Decisions become ADRs as backlog items close. Deterministic checks gate every change (ADR-011). AI-authored work is marked in commits with the Co-Authored-By trailer, so the project's own delivery metrics (share of AI-authored changes, review time, change failure rate) can be published alongside the product's results.

**Token use is monitored.** The budget, and how it is enforced, are open (D1).

## Constraints

- **C1:** More than three parallel tracks MUST NOT run at once.
- **C2:** Each track MUST run as a named session in its own git worktree.
- **C3:** Claude Code configuration (CLAUDE.md, skills, subagents, hooks) MUST be committed to this repository.
- **C4:** When a backlog item closes, its decision MUST be recorded as an ADR.
- **C5:** AI-authored commits MUST carry the Co-Authored-By trailer.
- **C6:** Token use MUST be monitored. What monitoring means beyond recording usage (a budget, and how it is enforced) is open (D1).

## Consequences

Easier:

- Work arrives at a pace that can be reviewed properly.
- The project's own delivery produces evidence of the same kind the product claims to produce.

Harder:

- Less parallel work than the tools allow.
- The trailer is only as reliable as the habit, until a check enforces it.

## Alternatives

### Do nothing: work in one session, as things come up (added when writing this ADR)

- For: no set-up.
- Against: no parallel research alongside the critical path, and nothing configured to repeat.

### Five or more parallel tracks

- For: more throughput.
- Against: more output than one reviewer can review (D1: "two or three parallel tracks, not five").

### A setup tuned for agent throughput, with review sampled (added when writing this ADR)

- For: fastest delivery.
- Against: unreviewed changes reach main, against the review-paced model chosen here.

### Review-paced tracks, configuration as code, dogfooding (chosen)

- For: review capacity sets the pace, and the project measures itself.
- Against: slower, and needs discipline until checks exist.

The naive option (an LLM with everything in its prompt) doesn't apply to how the work is organised.

## Enforcement

C5 becomes a commit-message check (planned with the Step 7 hooks). The rest rely on review. Two are unmet today. C2: no work has yet run in a worktree; track A runs in the main checkout (`git worktree list` shows only it). C3: so far only the Spec Kit skills are committed; the ADR, spike and acceptance-test skills, the reviewer subagent and the hooks are built in Step 7. For C6, loop cards record tokens per reviewer run; nothing sets or enforces a budget. How token use is monitored (C6) is open, so nothing enforces it yet.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D1's decisions of 5 Oct.
