---
id: ADR-013
version: 1
title: Public repositories, MIT licence, protected main, and nothing pushed before Andy's review
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
    mechanism: GitHub rulesets "Protect main branch" in both repositories (deletion and force-push blocked, no bypass actors)
    ref: https://github.com/a-douglas-lab/architect-in-the-loop/rules/24726583
    state: enforced
  - constraint: C5
    mechanism: review; a "require a pull request" ruleset rule is planned for Step 7
    ref: null
    state: manual
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
backlog: [D7]
---

# ADR-013: Public repositories, MIT licence, protected main, and nothing pushed before Andy's review

## Context

This is a portfolio project built in the open. Its dated history is part of the evidence of authorship, and reviewers must be able to read and run it. At the same time, agents write most of the changes, and only Andy can decide what reaches GitHub under his name.

## Decision

**This repository is public on GitHub** ([a-douglas-lab/architect-in-the-loop](https://github.com/a-douglas-lab/architect-in-the-loop)), built in the open. Its dated history is part of the evidence of authorship.

**MIT licence for everything** in this repository, code and documents. Ideas can't be protected by any licence; being visibly first and able to defend the work is the practical protection.

**The eShop fork is public** (a fork of a public repository must be) and keeps eShop's MIT licence.

**Repository rulesets:** `main` in both repositories can't be force-pushed or deleted. Tags in the fork can't be moved or deleted (ADR-002@v2 C4).

**Pushes happen only after Andy's review.** *Ruled by Andy on 21 Oct:* nothing is pushed, not even a branch, until Andy has reviewed the change locally. A PR opens only after that review, and main changes only through a PR Andy merges. PRs #4 to #9 were pushed before his review, under the looser reading. Private evaluation material is kept out by `.gitignore`, the bootstrap check and, from Step 7, Claude Code hooks (ADR-011).

## Constraints

- **C1:** This repository MUST be public.
- **C2:** Everything in this repository MUST be licensed under MIT.
- **C3:** The eShop fork MUST be public and keep eShop's MIT licence.
- **C4:** `main` in both repositories MUST NOT be force-pushed or deleted.
- **C5:** A change MUST NOT be pushed to GitHub, including on a branch, until Andy has reviewed it locally.
- **C6:** Changes MUST reach `main` only through a pull request that Andy merges.

## Consequences

Easier:

- Anyone can inspect, run and question the work, and its history shows when each part was written.
- Nothing reaches GitHub under Andy's name without his review.

Harder:

- Everything is visible, including mistakes and their corrections.
- Every change waits for a local review before it can be pushed, so a PR can't be used to review it.
- Until the rulesets require pull requests, C6 is a habit, not a control.

## Alternatives

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

- For: Andy reviews in GitHub's PR view.
- Against: work reaches GitHub before Andy has seen it. Andy ruled against this on 21 Oct.

### Public, MIT, protected main, nothing pushed before review (chosen)

- For: open, simple and under Andy's control.
- Against: slower, because review comes before the PR.

"Do nothing" is the no-licence option. The naive option (an LLM with everything in its prompt) doesn't apply.

## Enforcement

C4 is enforced by the "Protect main branch" rulesets in this repository (24726583) and in the fork (24726584). Both block deletion and force-pushes and have no bypass actors. Neither requires a pull request or a review, so C6 is held only by habit. A "require a pull request before merging" rule is planned for Step 7, for Andy to add; this ADR will be updated when it is. C5 can't be enforced by GitHub, because a push is the event it would have to stop; it is held by the author's discipline and a recorded working rule. C1 to C3 are true today and checked by review.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D7 (decided 8 Oct). Rulings by Andy on 21 Oct: "pushes only after Andy's review" means nothing is pushed, even a branch, before his local review; a "require a pull request" ruleset rule is recorded for Step 7.
