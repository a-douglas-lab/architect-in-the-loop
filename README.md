# Architect in the Loop

Status: draft · design phase, no code yet

From business outcome to governed, deployed change. *(Working title and description; the product name is parked, see [backlog.md](backlog.md) P1.)*

This repository is a portfolio project. It is not a live service with real users and does not claim to be. It is built to production-grade standards of design, code quality, testing, security, observability and governance, so that every part of it can be inspected, run and questioned.

- **What it is, who it is for and why:** [product.md](product.md)
- **Open questions and decisions, with status:** [backlog.md](backlog.md)
- **Order of work:** [roadmap.md](roadmap.md)

## What is ours and what isn't

This project extends an existing open-source application rather than building an e-commerce system from scratch. The line between the two is kept explicit.

**Built here:** the engineering capability, its architecture decisions, specifications, schemas, evaluations, infrastructure as code and all documentation in this repository.

**Used, not built:** [dotnet/eShop](https://github.com/dotnet/eShop), Microsoft's reference .NET e-commerce application, used as the subject system the capability works on.

| | |
| --- | --- |
| Licence | MIT |
| Version | Upstream commit `dc7ea49` (2 Oct 2026), tagged `upstream-dc7ea49` in our fork |
| How it is included | Our fork, [a-douglas-lab/eShop](https://github.com/a-douglas-lab/eShop), linked as a git submodule at `subject/eshop`. Our changes to eShop are commits in the fork; nothing from eShop is copied into this repository |

**eShop's own AI features are not part of this project.** eShop includes optional AI features (semantic catalogue search using embeddings, and a storefront chat assistant). They are Microsoft's work, they are switched off in this project, and nothing here builds on them.

## Getting started

```bash
git clone --recurse-submodules https://github.com/a-douglas-lab/architect-in-the-loop.git
cd architect-in-the-loop
./scripts/bootstrap.sh        # or scripts\bootstrap.ps1 on Windows
```

The bootstrap script fetches eShop at the pinned commit and checks prerequisites: the .NET SDK named in eShop's `global.json`, a container runtime for Aspire, Node.js, and the Spec Kit CLI. Run it again in every new clone or worktree.

Work is specified with [Spec Kit](https://github.com/github/spec-kit) **v1.1.2** (pinned). To install its CLI, with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.1.2
```

## Repository layout

| Path | Holds |
| --- | --- |
| `product.md`, `backlog.md`, `roadmap.md` | What we are building, every decision and open question, and the order of work |
| `docs/architecture/` | The capability's architecture sketch and walkthroughs |
| `docs/outcomes/` | Development outcomes for the Ordering exemplar |
| `docs/adr/` | Architecture decision records for this project |
| `docs/sessions/` | Short logs of each working session |
| `.specify/`, `specs/` | Spec Kit: constitution, templates and feature specs |
| `.claude/`, `CLAUDE.md` | Claude Code configuration: skills, subagents, hooks |
| `src/`, `tests/`, `rubrics/` | The capability, its tests and its runtime rubrics (as they are built) |
| `scripts/` | Bootstrap and repository tooling |
| `subject/eshop/` | The subject system (submodule). Its contract, ADRs, specs and development acceptance tests live there, with its code |

## Licence

MIT, see [LICENSE](LICENSE). eShop is © Microsoft under its own MIT licence.
