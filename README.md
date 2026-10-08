# [Name TBD]

Status: draft · design phase, no code yet

From business outcome to governed, deployed change. *(Working description; the name and line are being decided, see [backlog.md](backlog.md) P1.)*

This repository is a portfolio project. It is not a live service with real users and does not claim to be. It is built to production-grade standards of design, code quality, testing, security, observability and governance, so that every part of it can be inspected, run and questioned.

- **What it is, who it is for and why:** [product.md](product.md)
- **Open questions and decisions in progress:** [backlog.md](backlog.md)

## What is ours and what isn't

This project extends an existing open-source application rather than building an e-commerce system from scratch. The line between the two is kept explicit.

**Built here:** the engineering capability, its architecture decisions, specifications, schemas, evaluations, infrastructure as code and all documentation in this repository.

**Used, not built:** [dotnet/eShop](https://github.com/dotnet/eShop), Microsoft's reference .NET e-commerce application, used as the subject system the capability works on.

| | |
| --- | --- |
| Licence | MIT |
| Version | Pinned to commit `dc7ea49` (1 Oct 2026); to be confirmed when the subject system is set up |
| How it is included | As a pinned dependency, not copied into this repository |

**eShop's own AI features are not part of this project.** eShop includes optional AI features (semantic catalogue search using embeddings, and a storefront chat assistant). They are Microsoft's work, they are switched off in this project, and nothing here builds on them.
