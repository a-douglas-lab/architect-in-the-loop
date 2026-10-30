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
    mechanism: review of roadmap.md and backlog.md
    ref: roadmap.md
    state: manual
  - constraint: C2
    mechanism: review of roadmap.md; only Phase 0 records its evidence today
    ref: roadmap.md
    state: manual
  - constraint: C3
    mechanism: Andy's judgement; a dropped idea leaves no trace, so this can't be checked afterwards
    ref: null
    state: manual
  - constraint: C4
    mechanism: Andy's judgement; the reviewer has no knowledge of his previous employment
    ref: null
    state: manual
  - constraint: C5
    mechanism: review of README.md
    ref: README.md
    state: manual
  - constraint: C6
    mechanism: Andy's judgement
    ref: null
    state: manual
  - constraint: C7
    mechanism: Andy's judgement
    ref: null
    state: manual
backlog: [D2, D4]
---

# ADR-018: No hard deadline, milestones defined by evidence, and prior-work overlaps go to Andy

## Context

Two project-management questions need a recorded answer. How is the work timeboxed? And what happens when an idea may overlap with Andy's previous employment? Neither is an architecture decision. They are recorded together in one short ADR, because CLAUDE.md says every decision becomes an ADR.

## Decision

**Timebox (D2).** There is no hard deadline. Quality comes first; work continues beyond the nominal one-week date, and we see where we end up. Milestones are defined by the evidence they produce, so each phase leaves something publishable ([roadmap.md](../../roadmap.md)). Sizing at the time of the decision was about five to seven weeks for the full scope.

**Prior work (D4).** We build the best engineering solution, and don't avoid ideas because they overlap with previous work. An idea that may overlap with Andy's previous employment is flagged to him, and he has the final say on whether and how it is used. So only Andy can rule such an idea out. The README carries no prior-work statement until Andy decides what it should say. Whether to take legal advice on past employment contracts is Andy's call; Claude is not a lawyer.

## Constraints

- **C1:** The project MUST NOT set a hard deadline.
- **C2:** Milestones MUST be defined by the evidence they produce, so that each phase leaves something publishable.
- **C3:** An idea MUST NOT be dropped because it may overlap with Andy's previous employment, unless Andy decides so.
- **C4:** An idea that may overlap with Andy's previous employment MUST be flagged to him.
- **C5:** The README MUST NOT carry a prior-work statement until Andy decides what it should say.
- **C6:** Andy MUST have the final say on whether and how an overlapping idea is used.
- **C7:** Whether to take legal advice on past employment contracts MUST be left to Andy.

## Consequences

Easier:

- Progress is measured by what each phase leaves behind, not by a date.
- Prior-work questions have one route and one decision-maker.

Harder:

- With no deadline, nothing on the calendar limits scope.
- Spotting an overlap depends on Claude recognising one and on Andy's own knowledge. Nothing can check it mechanically.
- The roadmap doesn't yet record evidence for each phase, so C2 is unmet beyond Phase 0.

To do:

- Add the evidence each phase leaves behind to roadmap.md.

## Alternatives

### Do nothing: leave both unrecorded (added when writing this ADR)

- For: no work.
- Against: CLAUDE.md requires an ADR, and both rules would rest on memory.

### Hold to the nominal one-week date (added when writing this ADR)

- For: a fixed end.
- Against: quality would give way to the date.

### Avoid any idea that may overlap (added when writing this ADR)

- For: the most cautious on overlap.
- Against: worse engineering, and it hides the choice instead of putting it to Andy.

### No hard deadline, evidence-defined milestones, overlaps flagged to Andy (chosen)

- For: quality and evidence set the pace, and Andy keeps the decision on prior work.
- Against: no external pressure to finish, and overlap spotting relies on judgement.

The naive option (an LLM with everything in its prompt) doesn't apply to either decision.

## Enforcement

C1 can be read from roadmap.md and backlog.md, and C5 from the README, which carries no prior-work statement today. C2 is unmet beyond Phase 0: only that phase records its evidence in roadmap.md. C3, C4, C6 and C7 rest on Andy's judgement, because REVIEW.md doesn't cover them and the reviewer knows nothing of his previous employment. C3 can't be checked afterwards, because a dropped idea leaves no trace.

## History

- **v1** · 2026-10-30 · accepted · Andy Douglas: first version, recording D2 and D4 (decided 5 Oct). One ADR for both, as Andy agreed for Step 5. Tier `cross-cutting` and exceptions `not-allowed` follow ADR-000@v3 C13. Ruling by Andy on 30 Oct, from review: the overlap rule uses CLAUDE.md's wording ("may overlap with Andy's previous employment"), not D4's "any overlap".
