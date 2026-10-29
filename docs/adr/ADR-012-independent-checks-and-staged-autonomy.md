---
id: ADR-012
version: 1
title: Agent work is checked independently, and autonomy is raised in stages
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
    mechanism: review; loop cards in docs/loops/cards/
    ref: docs/loops/cards
    state: manual
  - constraint: C2
    mechanism: review against the readiness criteria in docs/loops/README.md
    ref: docs/loops/README.md
    state: manual
  - constraint: C3
    mechanism: review of each loop card
    ref: null
    state: manual
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
  - constraint: C7
    mechanism: review, once there is code
    ref: null
    state: manual
  - constraint: C8
    mechanism: skill eval runs, triggered by changes to a skill, CLAUDE.md or a hook
    ref: null
    state: planned
  - constraint: C9
    mechanism: review when a stage's autonomy is raised
    ref: null
    state: manual
backlog: [D1, D8]
---

# ADR-012: Agent work is checked independently, and autonomy is raised in stages

## Context

Anthropic's AI-native SDLC playbook argues for loops in which agents check their own work before a human sees it, and for raising agent autonomy in tiers. Two risks come with that. An agent that checks its own work shares its own blind spots. And autonomy raised before a stage is understood automates mistakes. This project also has a learning goal: to understand each delivery stage by hand before automating it.

## Decision

Spec Kit stays the engine; the playbook supplies the loop around it: who acts at each stage, what each stage measures, and how autonomy is granted.

**Stages are run by hand before they are automated.** Each run of a delivery stage is recorded on a loop card ([docs/loops/](../loops/README.md)). A stage's autonomy is raised one level at a time, and only when its cards meet the readiness criteria. The cards also give each stage a leading and a lagging indicator, which feeds the delivery metrics (ADR-010). The autonomy levels (0 to 4) and the readiness criteria are a first draft, to be refined after the first DEV-1 runs. Whether low-risk stages (tasks, analyze) need a lighter loop card is open (D1). No stage goes above level 2 until ADR-013's gating rule has been revised for automated stages (ADR-013@v1 C7).

**Agent work is checked by an independent reviewer.** The adversarial reviewer runs on every documentation PR, by hand, to a written policy, [REVIEW.md](../../REVIEW.md), with findings ranked by severity and nits capped. It is a subagent with a fresh context that sees the diff and the sources, not the author's reasoning. It never approves, and Andy decides. While stages are hand-run, the review happens before anything is pushed (ADR-013@v1 C5). So its findings and the author's responses are written on that run's loop card, committed on the branch, where Andy reads them during his local review. The PR description summarises them and links the card once the branch is pushed (*ruled by Andy, 21 Oct*). Documentation PRs get four passes (fidelity, facts, constraints, honest enforcement). The playbook's three code passes (bugs, security, compliance with spec and plan) are added when there is code.

**Configuration is treated as code.** Each skill gets a small regression eval set, re-run whenever the skill, CLAUDE.md or a hook changes. Where the eval sets live and how they run is open (A5, Q2).

## Constraints

- **C1:** Each delivery stage MUST be run by hand, and each run recorded on a loop card, before the stage is automated.
- **C2:** A stage's autonomy MUST be raised only one level at a time, and only when its loop cards meet the readiness criteria.
- **C3:** Each stage's loop cards MUST record a leading and a lagging indicator.
- **C4:** Every documentation PR MUST be reviewed by the adversarial reviewer to REVIEW.md before Andy reviews it.
- **C5:** The reviewer MUST run in a fresh context that sees the diff and its sources, not the author's reasoning.
- **C6:** The reviewer MUST NOT approve a change. Its findings and the author's responses MUST be recorded on the run's loop card, and summarised in the PR description once the branch is pushed.
- **C7:** Once there is code, code PRs MUST also be reviewed for bugs, security, and compliance with the spec and plan.
- **C8:** Each skill MUST have a regression eval set, re-run whenever the skill, CLAUDE.md or a hook changes.
- **C9:** A stage MUST NOT be raised above autonomy level 2 until ADR-013 has been revised as its C7 requires.

## Consequences

Easier:

- Andy reviews findings with evidence, rather than re-reading every line.
- Automation arrives with a record of why each stage was trusted.

Harder:

- Every documentation PR costs a reviewer run: between about 98,000 and 122,000 tokens in the first five runs (loop cards).
- The reviewer is the same model as the author, so it may share some blind spots. Its precision has so far been scored by the author, not independently.
- Running stages by hand is slower than automating them straight away.

## Alternatives

### Do nothing: Andy reviews everything himself (added when writing this ADR)

- For: no tooling.
- Against: review attention is the bottleneck (ADR-010), and the author's own errors went unnoticed until the reviewer ran (loop card, run 1).

### The agent checks its own work only (added when writing this ADR)

- For: cheap and fast.
- Against: the author marks its own homework, the failure the specify loop card recorded.

### Automate each stage as soon as it works once (added when writing this ADR)

- For: speed.
- Against: one run can't show a check is trustworthy; mistakes get automated.

### Hand-run stages on loop cards, an independent reviewer, evals for configuration (chosen)

- For: trust is earned stage by stage, with evidence.
- Against: slower, and each review costs tokens.

The naive option (an LLM with everything in its prompt) is the "agent checks its own work" option here.

## Enforcement

Everything here relies on review today. The loop cards and REVIEW.md are the records review works from. C8 becomes a triggered eval run once the eval sets exist (planned).

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D1's decisions of 20 Oct (loop cards, REVIEW.md, skill evals, the adversarial reviewer). Rulings by Andy on 21 Oct: the reviewer decisions belong in this ADR; findings go on the loop card for his local review, then into the PR; no stage goes above level 2 until ADR-013 is revised (C9).
