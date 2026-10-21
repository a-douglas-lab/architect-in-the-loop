---
id: ADR-013
version: 1
title: Public repositories, MIT licence, protected main, and review before anything is pushed while stages are hand-run
status: accepted
date: 2026-10-21
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
    mechanism: repository visibility on GitHub
    ref: https://github.com/a-douglas-lab/architect-in-the-loop
    state: manual
  - constraint: C2
    mechanism: LICENSE file; review
    ref: LICENSE
    state: manual
  - constraint: C3
    mechanism: repository visibility and licence on GitHub
    ref: https://github.com/a-douglas-lab/eShop
    state: manual
  - constraint: C4
    mechanism: GitHub rulesets "Protect main branch" in this repository (24726583) and the fork (24726584); deletion and force-push blocked, no bypass actors
    ref: https://github.com/a-douglas-lab/architect-in-the-loop/rules/24726583
    state: enforced
  - constraint: C5
    mechanism: the author's discipline, backed by a working rule in Claude Code's memory for this project (outside the repository); GitHub can't stop a push before it happens
    ref: null
    state: manual
  - constraint: C6
    mechanism: a "require a pull request before merging" rule in both main rulesets, planned for Step 7, for Andy to add; until then, habit
    ref: null
    state: planned
  - constraint: C7
    mechanism: review when a stage's autonomy is raised (ADR-012@v1 C9)
    ref: null
    state: manual
backlog: [D7, D8]
---

# ADR-013: Public repositories, MIT licence, protected main, and review before anything is pushed while stages are hand-run

## Context

This is a portfolio project built in the open. Its dated history is part of the evidence of authorship, and reviewers must be able to read and run it. Agents write many of the changes, and only Andy can decide what is published under his name. Because the repositories are public, pushing even a branch publishes it.

The project is also heading towards automated delivery loops (ADR-012), in which agents push branches, CI runs on every push, and the reviewer runs on every PR. A rule that makes Andy review before every push would put him back inside those loops, and would put his review before the deterministic checks rather than after them. The gating rule must therefore be fixed for now, while stages are run by hand, and changed deliberately before any stage is automated.

## Decision

**This repository is public on GitHub** ([a-douglas-lab/architect-in-the-loop](https://github.com/a-douglas-lab/architect-in-the-loop)), built in the open. Its dated history is part of the evidence of authorship.

**MIT licence for everything** in this repository, code and documents. Ideas can't be protected by any licence; being visibly first and able to defend the work is the practical protection.

**The eShop fork is public** (a fork of a public repository must be) and keeps eShop's MIT licence.

**Repository rulesets:** `main` in both repositories can't be force-pushed or deleted. Tags in the fork can't be moved or deleted (ADR-002@v2 C4).

**While stages are run by hand** (autonomy level 2 or below, ADR-012), pushes happen only after Andy's review. *Ruled by Andy on 21 Oct:*

- nothing is pushed, not even a branch, until Andy has reviewed the change locally;
- the reviewer's findings for that review are on the run's loop card, committed on the branch (ADR-012@v1 C6);
- main changes only through a pull request that Andy merges.

PRs #4 to #9 were pushed before his review, under a looser reading of D7.

**Before any stage is automated** (raised above level 2), this ADR is revised. The invariant then moves from pushes to `main`. Every change arrives by pull request, required checks must pass, and Andy's approval is required where the change's risk calls for it, mirroring the capability's own approval points. The revision also decides where agents push: a private mirror, so that nothing unreviewed is public, or public draft branches. That question is open (D8).

Private evaluation material is kept out by `.gitignore`, the bootstrap check and, from Step 7, Claude Code hooks (ADR-011).

## Constraints

- **C1:** This repository MUST be public.
- **C2:** Everything in this repository MUST be licensed under MIT.
- **C3:** The eShop fork MUST be public and keep eShop's MIT licence.
- **C4:** `main` in both repositories MUST NOT be force-pushed or deleted.
- **C5:** While no delivery stage is above autonomy level 2, a change MUST NOT be pushed to GitHub, including on a branch, until Andy has reviewed it locally.
- **C6:** While no delivery stage is above autonomy level 2, changes MUST reach `main` only through a pull request that Andy merges.
- **C7:** Before any delivery stage is raised above autonomy level 2, this ADR MUST be revised to set the gate for automated stages: what reaches `main` and how, and where agents push.

## Consequences

Easier:

- Anyone can inspect, run and question the work, and its history shows when each part was written.
- While stages are hand-run, nothing should reach GitHub without Andy's review. This depends on discipline (C5); PRs #4 to #9 show it can slip.
- The move to automation can't happen silently: it needs this ADR revised first.

Harder:

- Everything is visible, including mistakes and their corrections.
- While stages are hand-run, every change waits for a local review before it can be pushed, so CI can't run before Andy's review.
- Until the rulesets require pull requests, C6 is a habit, not a control.

## Alternatives

### Do nothing: no rule on pushes or merges (added when writing this ADR)

- For: no friction.
- Against: anything could reach `main` or GitHub without Andy's review.

### No licence (recorded in D7)

- For: all rights reserved.
- Against: odd for a portfolio, and deters reviewers from running it.

### Source-available, such as PolyForm Noncommercial (recorded in D7)

- For: restricts commercial reuse.
- Against: less familiar to reviewers.

### MIT for code, CC BY 4.0 for documents (recorded in D7)

- For: a licence designed for documents.
- Against: two licences to explain, for little gain.

### Private repository until finished (added when writing this ADR)

- For: mistakes stay private.
- Against: loses the dated history that evidences authorship.

### Branches pushed freely for review as PRs (added when writing this ADR; the looser reading of D7)

- For: Andy reviews in GitHub's PR view, and CI runs first.
- Against: work reaches GitHub before Andy has seen it. Andy ruled against this for the hand-run phase on 21 Oct. It may return, with a private mirror, when stages are automated (D8).

### "No push before review" as a permanent rule (added when writing this ADR)

- For: the strictest control on what is published.
- Against: it would block automated loops, and put human review before the deterministic checks. Andy chose to scope it to the hand-run phase on 21 Oct.

### Public, MIT, protected main, review before push while hand-run, revised before automation (chosen)

- For: open and under Andy's control now, with a deliberate step before automation.
- Against: slower while hand-run; the automated gate is still to be designed.

The naive option (an LLM with everything in its prompt) doesn't apply.

## Enforcement

C4 is enforced by the "Protect main branch" rulesets in this repository (24726583) and in the fork (24726584). Both block deletion and force-pushes and have no bypass actors. Neither requires a pull request or a review, so C6 is held only by habit until the "require a pull request before merging" rule is added in Step 7. C5 can't be enforced by GitHub, because a push is the event it would have to stop. It is held by the author's discipline and a working rule in Claude Code's memory for this project. C7 is checked when a stage's autonomy is raised: ADR-012@v1 C9 requires this revision first. C1 to C3 are true today and checked by review.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D7 (decided 8 Oct). Rulings by Andy in chat on 21 Oct: "No push before review", meaning nothing is pushed, even a branch, before his local review; a "require a pull request" ruleset rule is recorded for Step 7; both rules apply while stages are hand-run, and this ADR is revised before any stage goes above level 2 ("yes, scope ADR-013 that way"); main changes only through a PR he merges; the reviewer's findings go on the loop card for his local review.
