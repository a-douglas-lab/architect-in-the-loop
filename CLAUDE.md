# CLAUDE.md

Guidance for Claude Code sessions in this repository. Keep this file short: it points to the documents that hold the detail.

## What this repo is

A portfolio project by Andy Douglas. Two parts:

- **Subject system:** an e-commerce platform, dotnet/eShop (MIT), pinned at commit `dc7ea49` and used as a dependency, never copied in.
- **The capability (the product):** an outcome-driven system builder that takes a business outcome, works out which domains it touches, applies the architecture decisions (ADRs) that govern them, and coordinates coding agents to specify, build, test and ship the change, with the architecture coordinator approving where risk requires it.

Thesis: deterministic where possible, probabilistic where necessary, measured everywhere.

## Read before acting

| Document | Holds |
| --- | --- |
| [product.md](product.md) | Who, what, why; personas; success; scope |
| [backlog.md](backlog.md) | Every open question and every decision so far, with status. The source of truth for what is decided |
| [roadmap.md](roadmap.md) | Order for closing the backlog; current phase |
| [architecture-sketch.md](architecture-sketch.md) | The capability's nine contexts, flow, approval points, and walkthroughs G1 to G14 |
| [development-outcomes.md](development-outcomes.md) | The three development outcomes (D1 to D3) for the Ordering exemplar |

**Current phase:** Phase 1, Foundations (see roadmap.md).

## How we work

- **Challenge, don't assume.** Ask Andy before deciding anything not recorded as decided in backlog.md. Offer options with trade-offs and a recommendation.
- **Spec Kit is the workflow** (constitution, specify, plan, tasks, implement). Skills, subagents and hooks support its stages; they don't replace them.
- **Every decision becomes an ADR.** When a backlog item closes, write the ADR and update the item's status in backlog.md.
- **Research method** (backlog.md, top): problem and criteria; options including the naive one and "do nothing"; a spike where evidence is needed; decision as an ADR. Depth follows value: deep for differentiating items, a sensible default for commodity ones.
- **Try, measure, review, adapt.** No claim without a measurement; where something can't be measured, say so.
- **Dogfood the product's disciplines:** deterministic checks gate changes; keep the Co-Authored-By trailer on AI-authored commits so the project's own delivery metrics can be published.
- **Prior work:** if an idea may overlap with Andy's previous employment, flag it to him; he decides.
- **Writing:** plain British English, short sentences, no hype.

## Hard rules

1. **Never access the private evaluation repository.** It holds the held-out evaluation outcomes, hidden tests and labels. Never clone it into this repo or a worktree, and never ask for its contents.
2. **Build only development outcomes by hand.** D1 to D3, and only in the Ordering exemplar. Don't add eShop features beyond an approved spec.
3. **Never edit acceptance tests to make them pass.** A failing test is reported, not changed.
4. **eShop stays pinned and separate.** Its optional AI features stay switched off.
5. **Don't change existing eShop behaviour outside an approved spec,** including defects you notice. Report them to Andy instead; some existing behaviour is deliberately left as it is.
6. **No shopper-facing AI features, no multi-tenancy, no custom coding agent** (agreed non-goals).
