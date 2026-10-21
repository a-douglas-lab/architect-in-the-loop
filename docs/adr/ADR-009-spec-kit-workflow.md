---
id: ADR-009
version: 1
title: Spec Kit v1.1.2, pinned and core only, with specs that flow forward
status: accepted
date: 2026-10-21
decision-makers: [Andy Douglas]
scope: [project, concern:delivery]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: review
    ref: null
    state: manual
  - constraint: C2
    mechanism: bootstrap scripts compare the installed CLI with the pin; they warn on a mismatch but don't fail
    ref: scripts/bootstrap.ps1
    state: manual
  - constraint: C3
    mechanism: review
    ref: null
    state: manual
  - constraint: C4
    mechanism: CI check that no Spec Kit preset or extension is installed (no .specify/extensions.yml)
    ref: null
    state: planned
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
  - constraint: C6
    mechanism: CI check that a merged feature folder under specs/ isn't changed later
    ref: null
    state: planned
  - constraint: C7
    mechanism: review
    ref: null
    state: manual
backlog: [T1]
---

# ADR-009: Spec Kit v1.1.2, pinned and core only, with specs that flow forward

## Context

The project needs one workflow for turning a request into a specified, planned, built change, both for the capability itself and for the exemplar. Spec Kit provides one: constitution, specify, plan, tasks, implement. It also has a growing catalogue of presets and extensions, some official and many third-party, and a known criticism: it is spec-first but not spec-anchored, because specs aren't kept true after the change ships.

This ADR covers building this project. Whether the capability also produces Spec Kit artefacts for changes to the subject system, and how ADRs connect to Spec Kit's constitution, are open (T1).

## Decision

**Adopt the Spec Kit workflow** for building this project. Skills, subagents and hooks support its stages rather than replacing them.

**Version:** Spec Kit **v1.1.2** (released 7 Oct 2026, commit `959e866`), pinned. Installed with `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.1.2`. Upgrades are deliberate, reviewed changes.

**Workflow:** the constitution once; then, per feature, specify → plan → tasks → implement → converge, repeating implement and converge until converge reports converged. Clarify, checklist and analyze are optional quality gates.

**Initialisation (this repo):** `specify init --here --force --non-interactive --integration claude --script py --ignore-agent-tools`. Claude Code integration in skills mode (`.claude/skills/speckit-*`, invoked as `/speckit-<stage>`). Python scripts, so they behave the same on Windows, macOS, Linux and CI. `--ignore-agent-tools` only because the desktop app doesn't put a `claude` executable on PATH.

**Core only: no presets or extensions yet.** Community extensions and presets are third-party code that the Spec Kit maintainers don't review. None is installed without a source review, a pinned version and an ADR.

**Spec persistence: flow-forward, anchored on decisions.** Each feature folder in `specs/` is a fixed historical record; new requirements get a new folder. What must stay true lives in the ADRs and the constitution, enforced by deterministic checks. This is our answer to the "spec-first but not spec-anchored" criticism: the system is anchored on decisions, not on specs kept current by hand.

## Constraints

- **C1:** This project MUST be built with the Spec Kit workflow; skills, subagents and hooks MUST support its stages, not replace them.
- **C2:** Spec Kit MUST be pinned at v1.1.2. Upgrading needs a revision of this ADR.
- **C3:** Each feature MUST go through specify, plan, tasks, implement and converge, repeating implement and converge until converge reports converged.
- **C4:** A Spec Kit preset or extension MUST NOT be installed without a revision of this ADR.
- **C5:** A community extension or preset MUST NOT be installed without a source review, a pinned version and an ADR.
- **C6:** A feature folder in `specs/` MUST NOT be changed after its feature is merged; new requirements MUST get a new folder.
- **C7:** What must stay true after a change MUST live in the ADRs and the constitution, not in specs.

## Consequences

Easier:

- A recognisable, documented workflow that reviewers know.
- Specs are honest historical records. Nobody has to keep them current, and nobody is misled when they aren't.

Harder:

- Knowing what is true now means reading ADRs and the constitution, not the latest spec. That only works if the ADRs are complete and enforced.
- Pinning means missing Spec Kit fixes until an upgrade is reviewed.

## Alternatives

### Do nothing: no specification workflow (added when writing this ADR)

- For: no ceremony.
- Against: nothing for agents or reviewers to work to, and no definition of done before coding.

### Naive: describe each change in a prompt and let the agent plan it (added when writing this ADR)

- For: fastest.
- Against: no reviewable artefacts between the request and the code.

### Model Driven Engineering preset (`mde` 0.5.1) (recorded in T1: rejected)

- For: a fuller modelling flow.
- Against: replaces the recognisable core flow with `specify → next`, needs its own extension, and treats proposed answers as approved when the user says `next`, which conflicts with our approval discipline. Small and little-used (one release, May 2026).

### Official `agent-context` extension (recorded in T1: no)

- For: keeps agent context files up to date automatically.
- Against: CLAUDE.md is curated by hand.

### Specs kept current (spec-anchored) (added when writing this ADR)

- For: the spec always describes the system.
- Against: specs drift unless someone keeps them current by hand, and the drift is silent.

### Spec Kit core, pinned, flow-forward specs anchored on ADRs (chosen)

- For: a standard workflow, reproducible, with truth kept where checks can enforce it.
- Against: depends on ADRs being complete, and upgrades need deliberate work.

T1 also records three extensions as deferred, not rejected: *Brownfield Bootstrap*, deferred to the eShop fork; the official `git` extension, to try on the first spec; and the official `assess` extension, to consider for the research-spike skill.

## Enforcement

C2 is checked by the bootstrap scripts, which compare the installed CLI's version with the pin. They only warn on a mismatch and don't fail, so the state is manual. C4 and C6 are planned CI checks. The rest rely on review.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording T1's decided part (5 and 8 Oct).
