---
id: ADR-006
version: 1
title: The evidence line rests on three facts, and results are published all or none
status: accepted
date: 2026-10-21
decision-makers: [Andy Douglas]
scope: [project, concern:evaluation]
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
    mechanism: review
    ref: null
    state: manual
  - constraint: C3
    mechanism: comparison of the published measures with the pre-registered list (ADR-008@v1 C11)
    ref: null
    state: planned
  - constraint: C4
    mechanism: review
    ref: null
    state: manual
  - constraint: C5
    mechanism: review, until the capability's instrumentation exists
    ref: null
    state: manual
backlog: [P2]
---

# ADR-006: The evidence line rests on three facts, and results are published all or none

## Context

The project's results will be summarised in a single evidence line. That line is the claim a reviewer will test first. If it is chosen after seeing the numbers, or if only the good numbers are published, it proves nothing.

## Decision

The evidence line is built on three facts:

1. **Hidden-test pass rate versus plain Claude Code** (the E4 baseline), on the ten held-out outcomes.
2. **Zero breaches of architecture decisions reaching main**, against the baseline's count.
3. **Negative outcomes stopped for the right reason** (conflict, decision gap, ambiguity).

Its working shape: *"Turns business outcomes into governed, deployed changes. On 10 outcomes defined before the build, it passed [X]% of tests it never saw (plain Claude Code: [Y]%), with zero breaches of architecture decisions, and stopped correctly on all [N] it shouldn't complete."* The placeholders are filled only from the scored run.

The measures behind it are instrumented from the capability's first commit: hidden and visible acceptance results per outcome and per run; ADR check results on every merge; escalation records with their reasons; and the same measures for the baseline.

Whether to publish is decided after seeing the results; that is Andy's call. **All or none:** if results are published, all pre-registered measures are published. The choice is whether to publish, never which numbers. The list of measures is itself pre-registered (ADR-008@v1 C11), so "all" has a fixed meaning. The development-set dry run gives an early read before the scored run, which reduces the risk of a surprise.

## Constraints

- **C1:** The evidence line MUST rest on the three facts above: hidden-test pass rate against plain Claude Code on the ten held-out outcomes; the count of breaches of architecture decisions reaching main, against the baseline's count; and negative outcomes stopped for the right reason. (Zero breaches is the target the line reports, not something a rule can require.)
- **C2:** The evidence line's numbers MUST be filled only from the scored run.
- **C3:** If results are published, all pre-registered measures MUST be published.
- **C4:** Whether to publish MUST be decided by Andy after seeing the results.
- **C5:** From the capability's first commit, hidden and visible acceptance results per outcome and per run, ADR check results on every merge, and escalation records with their reasons MUST be recorded, for the capability and for the baseline.

## Consequences

Easier:

- A reviewer can check the claim against pre-registered measures, not take it on trust.
- Publishing nothing remains an honest option, so a poor result doesn't force a misleading one.

Harder:

- A weak measure can't be dropped quietly; it is published with the rest or nothing is.
- The instrumentation has to exist before the results matter, which is work before the capability does anything useful.

## Alternatives

### Do nothing: a demo and a description, no measured claim (added when writing this ADR)

- For: no evaluation work.
- Against: an unfalsifiable claim, which the project's thesis ("measured everywhere") rules out.

### Publish whatever looks best after the run (added when writing this ADR)

- For: the most flattering result.
- Against: cherry-picking. A reviewer can't tell a real result from a selected one.

### Commit to publishing before the run, whatever the result (added when writing this ADR)

- For: the strongest guard against selection.
- Against: forces publication of a result that might mislead, for example after a broken run.

### Three fixed facts, all-or-none publication decided after the results (chosen)

- For: no selection of numbers, while keeping the option not to publish at all.
- Against: "not publishing" can still hide a bad result; the dry run reduces, but doesn't remove, that risk.

The naive option (an LLM with everything in its prompt) doesn't apply to how results are reported.

## Enforcement

C3 becomes a mechanical comparison once the pre-registered list of measures exists (ADR-008@v1 C11). The other constraints rely on review. C5 can't be met or checked until the capability has code; nothing is instrumented yet.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording P2 (decided 5 Oct). Rulings by Andy in chat on 21 Oct, from review of this ADR: C5's "first commit" is the capability's; the list of measures is pre-registered; tier `cross-cutting` and exceptions `not-allowed`.
