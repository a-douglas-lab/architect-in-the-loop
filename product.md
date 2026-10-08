# Product

Status: draft v0.2 · 8 Oct 2026 · owner: Andy Douglas

This file defines what we are building, for whom, and why. It sits at the repo root and is the reference every spec, ADR and the constitution trace back to. It deliberately avoids *how*: tools and methods are decided in [backlog.md](backlog.md) and recorded as ADRs.

Working title: Architect in the Loop. The product name is parked (backlog P1).

## Why this exists

**The problem.** AI coding agents can now write code faster than teams can govern it. In a system of many domains, the hard part was never typing code. It is keeping the whole system coherent as it changes: honouring architecture decisions, integration patterns, authentication and authorisation, event schemas and reporting needs, when change requests arrive as business outcomes rather than technical tasks. Most AI-assisted delivery today loads decisions into a prompt and hopes. Nothing proves the result honours them.

**The thesis.** Deterministic where possible, probabilistic where necessary, measured everywhere. AI does the reasoning that needs judgement; deterministic checks hold it to the decisions that have already been made; every claim the system makes about its own quality is backed by a measurement.

**How it improves.** Every claim starts as a stated direction, not a promise. Anything we need to know is tried, measured, reviewed and adapted, then the cycle repeats. Where we can't measure something (for example real-world value, without users), the repo says so rather than claiming it.

**Why this repo exists.** This is a portfolio project, built in the open to demonstrate system design, engineering judgement and strategic thinking for early-stage CTO, Chief Architect and Head of Platform roles. It is not a live service with real customers and does not claim to be. It is production-grade in its engineering and reasoning, so an interviewer can inspect, run and question any part of it.

## What it is

Two things, with a clear boundary between them.

| Part | What it is | Role in the demonstration |
| --- | --- | --- |
| **Subject system** | A multi-domain e-commerce platform, serving merchants and their shoppers. Built by extending an existing open-source reference application: dotnet/eShop (MIT licence), pinned at commit `dc7ea49` and included as a dependency, not copied | The realistic, non-trivial system that change happens *to*. It carries the domains, integrations, events and ADRs the capability must reason over |
| **Engineering capability** | An outcome-driven system builder that sits over the subject system. It takes a business outcome, works out which domains it touches, applies the architecture decisions that govern them, and coordinates AI coding agents to specify, build, test and ship the change, with humans approving at defined points | The product. It is what the portfolio is really about |

The capability reasons across the whole subject system: domain boundaries, ADRs, integration patterns, authentication and authorisation, event schemas, and intelligence and reporting. It coordinates existing coding agents (such as Claude Code) rather than reimplementing them.

The capability is generic over subject knowledge: everything it knows about a subject system comes from a declared subject contract (domains, ADRs, schemas, build and test commands), never from its own code or prompts. It is specific to one stack (.NET, Aspire, event-driven) and is built and proven against one subject system, with a second, smaller subject as a stretch goal (backlog P3).

## Who it is for

Personas fall into two groups: those who use the capability, and those who live in the subject system and generate the outcomes it works on.

### Capability personas

| Persona | Goal | What they need from the capability |
| --- | --- | --- |
| **Architecture coordinator** | Keep the whole system coherent while change arrives quickly from many directions. States outcomes on behalf of business needs, resolves conflicts and makes the decisions the capability escalates | A web interface to state outcomes and review work; decisions enforced without policing every change; early warning when a new decision conflicts with or breaks existing ones; visibility of where decisions are missing |
| **Engineer reviewer** | Approve changes with confidence and without re-deriving everything | One place showing which domains were affected, which decisions applied and why, and which checks passed |
| **Coding and coordinating agents** | Do the work correctly first time | Minimal, sufficient, correct context; precise violations to repair against |
| **Evaluator** (an interviewer or reviewer inspecting the repo) | Judge the quality of the thinking and engineering | To follow any outcome end to end, from request to impact, decisions, spec, code, tests and deployment, and to question any step |

### Subject-system personas

| Persona | Goal | Relationship to the capability |
| --- | --- | --- |
| **Merchant** | Grow and run their store | Source of the business needs behind outcomes (for example, rewarding frequent customers with points). Does not change the system; the architecture coordinator states outcomes on their behalf. Needs trade-offs explained in plain terms |
| **Shopper** | Buy things easily and safely | Indirect: experiences the result of every change. Their interests appear as constraints (privacy, security, accessibility) |

The architecture coordinator uses a web interface (React frontend, C# REST API) to state outcomes and act at approval points. Where merchants configure settings inside the subject system is open (backlog P5b).

## What success looks like

Success is defined before building, against outcomes the system has not been tuned on.

**Outcome evaluation.** Ten held-out merchant outcomes, written and labelled before the capability is built, of varying difficulty and spanning several domains: seven it should complete (one adding a new domain) and three it should stop on (an ADR conflict, a decision gap, an ambiguous request). Each is run through the capability end to end. A separate development set is used while building (backlog E1, E2).

For each outcome, the capability succeeds when:

1. **Impact is right.** The domains it identifies match the expected impact set, including the non-obvious ones.
2. **Decisions are honoured.** Every applicable ADR is applied and none is breached, and this is shown by deterministic checks rather than asserted.
3. **The change works.** The change passes acceptance tests that the coding agents did not write, including hidden examples they never saw (backlog E2).
4. **Gaps and conflicts surface.** Where no decision exists, or decisions conflict, the capability stops and asks rather than guessing.
5. **It is traceable.** An evaluator can follow the outcome through every artefact without help.

Measures to report across the set (thresholds TBD, backlog E3): impact recall and precision, missed-ADR rate, acceptance pass rate, human interventions per outcome, cost and time per outcome, and the comparison against an ungoverned baseline (backlog E4).

**Portfolio success.** The repo, a short video and a one-command run let a reviewer conclude, quickly and from evidence, that the ideas are good, the execution is strong, and the author is credible across system design, engineering and strategy. The evidence line rests on three facts (backlog P2): hidden-test pass rate against plain Claude Code, zero breaches of architecture decisions reaching main, and negative outcomes stopped for the right reason.

## Scope boundaries

Confirmed:

- **No live users.** Nothing is presented as serving real customers.
- **No hosting or availability engineering.** High availability, scaling and 24/7 operation are out of scope. Production-grade applies to design, code quality, testing, security, observability and governance.

Also confirmed (backlog P7):

- No shopper-facing AI features such as a shopping chatbot.
- No multi-tenancy in the subject system.
- The capability need not build its own coding agent; it orchestrates existing ones.

## Related documents

- [backlog.md](backlog.md): every open question and decision, with status.
- [roadmap.md](roadmap.md): the order for closing the backlog.
- [architecture-sketch.md](architecture-sketch.md): the capability's contexts, flow and walkthroughs.
- [development-outcomes.md](development-outcomes.md): DEV-1 to DEV-3, for the Ordering exemplar.
- Constitution: to follow in Phase 1, using the Spec Kit workflow (backlog T1).
- ADRs: to follow, starting with the ADR template (backlog T2).
