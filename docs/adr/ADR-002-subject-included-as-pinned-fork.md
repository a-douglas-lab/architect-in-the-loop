---
id: ADR-002
version: 2
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
    mechanism: review; the bootstrap script initialises the submodule but doesn't check it
    ref: null
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
    mechanism: GitHub repository ruleset "Immutable tags" on the fork (all tags; deletion, update and force-push blocked)
    ref: https://github.com/a-douglas-lab/eShop/rules/24726585
    state: enforced
  - constraint: C5
    mechanism: review, then the evaluation runner (E6)
    ref: null
    state: manual
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
backlog: [P4]
---

# ADR-002: eShop is included as a pinned fork submodule, with two baselines

## Context

The subject system, dotnet/eShop (MIT), must be used, not built. We change it in reviewable commits, and every result must be reproducible against a known version. Two moments matter: where we started, and the state that evaluation outcomes run from, once our own baseline work is done. If either moves, the results can't be trusted.

Criteria: the pin is visible on GitHub; our changes are reviewable code, not patches; nothing from eShop is copied into this repo; baselines can't be moved.

## Decision

Fork eShop to [a-douglas-lab/eShop](https://github.com/a-douglas-lab/eShop). Tag the upstream commit `dc7ea49` (`dc7ea499cd35…`, "Update to Aspire 13.6.0", 2 Oct 2026 UTC) as `upstream-dc7ea49`. Include the fork in this repo as the git submodule `subject/eshop`. Our changes to eShop are commits in the fork; each commit here records exactly which fork commit it was built against.

There are two baselines:

- `upstream-dc7ea49` is where we started.
- The **evaluation baseline** is a later tag in the fork, frozen after our baseline work (Phases 2 and 4). Evaluation outcomes run from it.

eShop is pinned, not upgraded. Tags in the fork are immutable.

## Constraints

- **C1:** eShop MUST be included only as the git submodule `subject/eshop`, pointing at the fork.
- **C2:** The fork MUST stay based on upstream `dc7ea49`. Upgrading eShop needs a revision of this ADR.
- **C3:** eShop files MUST NOT be copied into this repo.
- **C4:** Tags in the fork MUST NOT be moved or deleted.
- **C5:** Evaluation outcomes MUST run from the evaluation baseline tag, once it exists.
- **C6:** Changes to eShop MUST be commits in the fork.

## Consequences

Easier:

- The exact subject version behind any result is visible on GitHub.
- Our eShop changes are ordinary, reviewable commits.
- The "used, not built" boundary is physical, so it's easy to check.

Harder:

- Submodules add friction: clones need `--recurse-submodules`, and the pointer can show as modified while fork work is in progress.
- Upstream fixes don't arrive unless this ADR is revised.

To do:

- Build the C2 and C3 checks in CI (Step 7).
- Add a check that the submodule commit matches the subject contract's declared baseline, once the contract exists (Phase 2).

## Alternatives

### Do nothing: depend on upstream eShop directly (added when writing this ADR)

- For: no fork to maintain.
- Against: there's nowhere to commit our changes, and upstream moves.

### Copying eShop in

- For: one repo, simple.
- Against: breaks the "used, not built" boundary.

### A fetch script with a manifest

- For: no submodule friction.
- Against: the pin isn't visible on GitHub, and it can drift without a check.

### An upstream submodule plus patch files

- For: no fork.
- Against: our changes become patches, not reviewable code.

### A fork plus submodule, with tagged baselines (chosen)

- For: a visible pin, reviewable changes, immutable baselines.
- Against: submodule friction, and the fork needs looking after.

The naive option (an LLM with everything in its prompt) doesn't apply to how code is included.

## Enforcement

C4 is enforced by the fork's "Immutable tags" ruleset, which covers all tags and has no bypass actors. Whether organisation owners could edit the ruleset itself hasn't been checked. C1 is set up by the bootstrap script but no check reads it, so it is held by review. C2 and C3 are planned CI checks. C5 and C6 are held by review, C5 until the evaluation runner (E6) exists.

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · correction · written by Claude, checked by review runs 1 and 2, merged by Andy Douglas: from review run 1 (findings 1, 10, 11, 15; nits 1, 2, 4), plus ADR-000@v2's versioning (C2 and the matching Harder bullet now say "a revision of this ADR" instead of "a new ADR that supersedes this one"). C1's mechanism no longer claims the bootstrap script checks it. C3 split: "changes are commits in the fork" is now C6. C4 restored to all tags, as in P4, with `ref` pointing at the ruleset. Upstream date given in UTC with the full hash, and baseline timing worded as in P4. Alternatives aligned with P4's rejected options, and the added one marked.
