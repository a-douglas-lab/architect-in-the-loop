---
id: ADR-018
version: 1
title: No hard deadline, milestones defined by evidence, and prior-work overlaps go to Andy
status: accepted
date: 2026-10-30
decision-makers: [Andy Douglas]
scope: [project, concern:governance]
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
    mechanism: review of roadmap.md
    ref: roadmap.md
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
    mechanism: review of README.md
    ref: README.md
    state: manual
backlog: [D2, D4]
---

# ADR-018: No hard deadline, milestones defined by evidence, and prior-work overlaps go to Andy

## Context

Two project-management questions need a recorded answer, because later work relies on them. How is the work timeboxed? And what happens when an idea overlaps with Andy's previous employment? Neither is an architecture decision. They are recorded together in one short ADR, because CLAUDE.md says every decision becomes an ADR.

## Decision

**Timebox (D2).** There is no hard deadline. Quality comes first; work continues beyond the nominal one-week date, and we see where we end up. Milestones are defined by the evidence they produce, so each phase leaves something publishable ([roadmap.md](../../roadmap.md)). Sizing at the time of the decision was about five to seven weeks for the full scope.

**Prior work (D4).** We build the best engineering solution, and don't avoid ideas because they overlap with previous work. Any overlap is flagged to Andy, who has the final say on whether and how it is used. The README carries no prior-work statement until Andy decides what it should say. Whether to take legal advice on past employment contracts is Andy's call; Claude is not a lawyer.

## Constraints

- **C1:** Work MUST NOT be cut short to meet a date: quality comes first.
- **C2:** Milestones MUST be defined by the evidence they produce.
- **C3:** An idea MUST NOT be avoided because it overlaps with previous work.
- **C4:** Any overlap with previous work MUST be flagged to Andy, who decides whether and how it is used.
- **C5:** The README MUST NOT carry a prior-work statement until Andy decides what it should say.

## Consequences

Easier:

- Each phase ends with something a reviewer can inspect, whenever it ends.
- Prior-work questions have one route and one decision-maker.

Harder:

- With no deadline, scope has to be held by the roadmap and the non-goals (ADR-004), not by the calendar.
- Spotting an overlap depends on Claude recognising one and Andy's own knowledge. Nothing can check it mechanically.

## Alternatives

### Do nothing: leave both unrecorded (added when writing this ADR)

- For: no work.
- Against: CLAUDE.md requires an ADR, and both rules would rest on memory.

### Hold to the nominal one-week date (added when writing this ADR)

- For: a fixed end.
- Against: quality would give way to the date.

### Avoid any idea that overlaps with previous work (added when writing this ADR)

- For: the most cautious on overlap.
- Against: worse engineering, and it hides the choice instead of putting it to Andy.

### No hard deadline, evidence-defined milestones, overlaps flagged to Andy (chosen)

- For: quality and evidence set the pace, and Andy keeps the decision on prior work.
- Against: no external pressure to finish, and overlap spotting relies on judgement.

The naive option (an LLM with everything in its prompt) doesn't apply to either decision.

## Enforcement

All five constraints rely on review. C2 is visible in roadmap.md, whose phases list what each leaves behind. C5 can be checked by reading the README, which carries no prior-work statement today. C3 and C4 need judgement.

## History

- **v1** · 2026-10-30 · accepted · Andy Douglas: first version, recording D2 and D4 (decided 5 Oct). One ADR for both, as Andy agreed for Step 5. Tier `cross-cutting` and exceptions `not-allowed` follow ADR-000@v3 C13.
