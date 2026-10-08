# Roadmap: order for closing the backlog

Status: proposal · 5 Oct 2026

Ranks the open items in [backlog.md](backlog.md) by what they unblock. Closed or decided items are not listed. Phases overlap where nothing blocks them; with Claude Code, two tracks can run in parallel.

## Ranking principles

1. **Unblock the most first.** An item that many others depend on goes early, however small.
2. **Decide cheaply what can be decided cheaply.** Strategic choices that need no research shouldn't wait behind research.
3. **Evidence early.** The job search is the point. Each phase should leave something a reviewer can see.
4. **Research depth follows value** (backlog method): commodity items get a default and a short ADR; differentiating items get spikes.

## Critical path

The longest chain of dependencies, which sets the earliest possible scored run:

ADR template (T2) → baseline ADRs (P4) → outcome labels (E1) → acceptance tests via the skill (D6, E2) → pre-registration → capability build → scored run

Everything not on this chain can run alongside it.

## Phases

### Phase 0. Frame · decisions only, no research

| Item | Why now |
| --- | --- |
| ~~D2 Timebox and milestones~~ | Closed: no hard deadline, quality first, each phase leaves something publishable |
| ~~P2 Evidence line~~ | Decided: hidden-test pass rate vs baseline, zero ADR breaches, negative outcomes stopped correctly |
| P1 Name | Needed for the repo, README and any early publication |
| D1 Ways of working | Parallel tracks, worktrees, skills and hooks set up once and reused |

Evidence at the end: product.md, backlog, outcome validation and the architecture sketch with its walkthroughs are already portfolio material. Consider publishing them as a "design complete" milestone, since written reasoning is what senior roles are judged on.

### Phase 1. Foundations · tool choices with short spikes

| Item | Depth | Why now |
| --- | --- | --- |
| T2 ADR template (ADR-000) | Commodity plus our front matter (scope, precedence, enforcement links) | On the critical path; everything references ADRs |
| T1 Planning and spec tooling, and the constitution | Spike | Decides how both the capability and the exemplar are specified |
| T5 Stack for the capability | Short | Decides how T4 and T9 are built |
| T4 Orchestrating coding agents | Spike | Core of delivery; judged against the sketch's delivery context |
| T9 Durable workflow engine | Spike | Core of coordination; judged against walkthroughs W3, W8 and W9 |
| Q2 Quality layer tools | Commodity | Defaults only (Roslyn and Sonar analyzers, SARIF, Playwright, axe, Stryker.NET) |
| Q5 Feature flag provider | Commodity | Needed before the exemplar |
| A5 Runtime rubrics, first drafts | Deep, drafting only | Shapes each agent's typed output; calibration waits for Phase 5 |

### Phase 2. Subject baseline

| Item | Why now |
| --- | --- |
| A3 Cross-cutting split | Decides who owns the cross-cutting baseline ADRs |
| P4 Baseline ADRs | On the critical path; the negative evaluation outcomes need ADRs to collide with. Includes "business rules live in the owning domain" |
| P5b Merchant configuration | Some evaluation outcomes need somewhere for the merchant to set values; blocks their labels |
| Q1 Enforcement map | Fills the enforcement section of each baseline ADR |

### Phase 3. Evaluation assets

| Item | Why now |
| --- | --- |
| D6 Acceptance test skill | On the critical path; every test is written with it |
| E1 Labels (two-tier, per part where an outcome may split; held privately) | Needs baseline ADRs and merchant configuration |
| E2 Tests written and confirmed red | In the private evaluation repo; then pre-registered |
| E4 Baseline comparison design | Must be fixed before the scored run |
| E3 Thresholds | Last step before pre-registration |

### Phase 4. Exemplar (Ordering)

| Item | Why now |
| --- | --- |
| P9 Ordering to preferred state, development outcomes D1 to D3, reference implementations | Dry run of the whole toolchain; produces the domain template (G13) |
| Q4 Ratchet baseline for legacy domains | Recorded as exceptions (G12) |

### Phase 5. Deep research, with spikes on the exemplar · can start earlier as paper research

| Item | Why here |
| --- | --- |
| T7 Impact analysis (prior art first) | Most likely interview topic; spikes need the domain catalogue |
| T6 ADR strategy | Needs baseline ADRs to test selection |
| T8 Subject knowledge | Needs the exemplar to size knowledge per domain |
| Q3 Dependency map | Needs a running system for observed dependencies |
| A2 and A5 Graders and rubric calibration | Calibration needs real outputs |
| P8 Value measurement | Design only; built on Q5's flags |

Prior-art reading for T7, T6 and A1 (including agentheim) can start in Phase 1 as a second track.

### Phase 6. Build, run, publish

A1 finalised from the research, capability built against the development set, scored run against the ten held-out outcomes, then D3 (repo, video, one-command deploy). D5 (rework the original document) is likely unnecessary: product.md and backlog.md supersede it, so the original can be archived.
