---
id: ADR-002
title: eShop is included as a pinned fork submodule, with two baselines
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [subject, project, concern:reproducibility]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: git submodule configuration, checked by the bootstrap script
    ref: scripts/bootstrap.ps1
    state: manual
  - constraint: C2
    mechanism: CI check that the submodule commit descends from the pinned upstream tag
    ref: null
    state: planned
  - constraint: C3
    mechanism: CI check that no eShop source files exist outside subject/eshop
    ref: null
    state: planned
  - constraint: C4
    mechanism: GitHub repository ruleset on the fork (tags cannot be moved or deleted)
    ref: https://github.com/a-douglas-lab/eShop
    state: enforced
  - constraint: C5
    mechanism: review, then the evaluation runner (E6)
    ref: null
    state: manual
backlog: [P4]
---

# ADR-002: eShop is included as a pinned fork submodule, with two baselines

## Context

The subject system, dotnet/eShop (MIT), must be used, not built. We change it in reviewable commits, and every result must be reproducible against a known version. Two moments matter: where we started, and the state that evaluation outcomes run from, once our own baseline work is done. If either moves, the results can't be trusted.

Criteria: the pin is visible on GitHub; our changes are reviewable code, not patches; nothing from eShop is copied into this repo; baselines can't be moved.

## Decision

Fork eShop to [a-douglas-lab/eShop](https://github.com/a-douglas-lab/eShop). Tag the upstream commit `dc7ea49` ("Update to Aspire 13.6.0", 2 Oct 2026) as `upstream-dc7ea49`. Include the fork in this repo as the git submodule `subject/eshop`. Our changes to eShop are commits in the fork; each commit here records exactly which fork commit it was built against.

There are two baselines:

- `upstream-dc7ea49` is where we started.
- The **evaluation baseline** is a later tag in the fork, frozen once our baseline work is complete (end of Phase 4). Evaluation outcomes run from it.

eShop is pinned, not upgraded.

## Constraints

- **C1:** eShop MUST be included only as the git submodule `subject/eshop`, pointing at the fork.
- **C2:** The fork MUST stay based on upstream `dc7ea49`. Upgrading eShop needs a new ADR that supersedes this one.
- **C3:** eShop files MUST NOT be copied into this repo. Changes to eShop MUST be commits in the fork.
- **C4:** Baseline tags in the fork MUST NOT be moved or deleted.
- **C5:** Evaluation outcomes MUST run from the evaluation baseline tag, once it exists.

## Consequences

Easier:

- The exact subject version behind any result is visible on GitHub.
- Our eShop changes are ordinary, reviewable commits.
- The "used, not built" boundary is physical, so it's easy to check.

Harder:

- Submodules add friction: clones need `--recurse-submodules`, and the pointer can show as modified while fork work is in progress.
- Upstream fixes don't arrive unless we supersede this ADR.

To do:

- Build the C2 and C3 checks in CI (Step 7).
- Add a check that the submodule commit matches the subject contract's declared baseline, once the contract exists (Phase 2).

## Alternatives

### Do nothing: depend on upstream eShop directly

- For: no fork to maintain.
- Against: there's nowhere to commit our changes, and upstream moves.

### Naive: copy eShop into this repo

- For: one repo, simple.
- Against: breaks the "used, not built" boundary, and blurs which code is ours.

### A fetch script with a manifest

- For: no submodule friction.
- Against: the pin isn't visible on GitHub, and it can drift without a check.

### An upstream submodule plus patch files

- For: no fork.
- Against: our changes become patches rather than reviewable code.

### A fork plus submodule, with tagged baselines (chosen)

- For: a visible pin, reviewable changes, immutable baselines.
- Against: submodule friction, and the fork needs looking after.

## Enforcement

C4 is enforced by the fork's repository ruleset. C1 is set up by the bootstrap script but not yet checked, so it is recorded as manual. C2 and C3 are planned CI checks. C5 is held by review until the evaluation runner (E6) exists.
