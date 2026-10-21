---
id: ADR-007
version: 1
title: Ten held-out outcomes, hand-written two-tier labels, deterministic impact scoring
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
    mechanism: review, against the private labels
    ref: null
    state: manual
  - constraint: C4
    mechanism: review, against the private labels
    ref: null
    state: manual
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
  - constraint: C6
    mechanism: review; the bootstrap scripts' name check catches only some copies in this repo (see Enforcement)
    ref: null
    state: manual
  - constraint: C7
    mechanism: the scoring code itself, once written
    ref: null
    state: planned
  - constraint: C8
    mechanism: review, against the private labels
    ref: null
    state: manual
  - constraint: C9
    mechanism: review
    ref: null
    state: manual
  - constraint: C10
    mechanism: review, against the private labels
    ref: null
    state: manual
  - constraint: C11
    mechanism: review, against the private labels
    ref: null
    state: manual
backlog: [E1, E1b]
---

# ADR-007: Ten held-out outcomes, hand-written two-tier labels, deterministic impact scoring

## Context

The capability's first job on any outcome is to work out which domains it touches (T7). A domain the router misses is never consulted, unless deterministic expansion adds it: domains that consume an affected event, or that a cross-cutting ADR adds, always join the set. So impact must be scored, against labels written before the run, on outcomes the capability was never tuned on. Who writes the labels, and how they are compared, decides whether the score means anything.

Every evaluation and development outcome was checked against the eShop source and against each other (an overlap matrix, held privately) before work started (E1b).

## Decision

**Ten held-out evaluation outcomes,** used only for scored runs, plus a separate development set (DEV-1 to DEV-3) for iterating during the build. Seven are positive (one adding a new domain) and three negative (ADR conflict, decision gap, ambiguous request), spread across single-domain, multi-domain and cross-cutting.

**Andy writes the outcomes and their expected impact sets.** The outcomes, their verification against eShop and their labels are held in the private evaluation repository and published with the results.

**Impact set, defined:** for each outcome, the list of domains (and the contracts within them: APIs, events, data) that the change must modify or explicitly consider. It is an intermediate output of the capability (T7), scored for recall and precision against a label written before the run. It is not a measure of value; value measures such as time and human effort are covered in E3.

**Labels have two tiers:**

- *Must change:* domains the change must modify, written by hand at domain level, with acceptable alternatives recorded where more than one design is valid.
- *Must consider:* domains that need checking but not changing, for example a domain whose ADR constrains the change, written by hand.

**Scoring is a deterministic comparison** (recall and precision), with no LLM in the scoring. **LLMs are disagreement detectors only:** several models can label independently to flag outcomes worth a second look, never as the answer key. Split outcomes are labelled by part (A4).

## Constraints

- **C1:** There MUST be ten held-out evaluation outcomes, used only for scored runs.
- **C2:** A separate development set, DEV-1 to DEV-3, MUST be used for iterating during the build.
- **C3:** The evaluation set MUST contain seven positive outcomes, one of which adds a new domain, and three negative outcomes: an ADR conflict, a decision gap and an ambiguous request.
- **C4:** The evaluation outcomes MUST be spread across single-domain, multi-domain and cross-cutting changes.
- **C5:** Andy MUST write the outcomes and their expected impact sets.
- **C6:** The outcomes, their verification and their labels MUST be held in the private evaluation repository until they are published with the results.
- **C7:** Impact MUST be scored by a deterministic comparison (recall and precision) with no LLM in the scoring.
- **C8:** Labels MUST have two tiers, must change and must consider, both written by hand.
- **C9:** LLMs MUST be used only as disagreement detectors, never as the answer key.
- **C10:** Split outcomes MUST be labelled by part.
- **C11:** Must-change labels MUST be written at domain level, with acceptable alternatives recorded where more than one design is valid.

## Consequences

Easier:

- Impact recall and precision are reproducible: anyone with the labels and the outputs gets the same score.
- Missing a domain is visible as lost recall, not argued about.

Harder:

- The labels reflect one person's design of the system. A second reviewer on a sample would address this; it is open (E1).
- Hand labelling takes Andy's time, and "acceptable alternatives" must be anticipated before the run.

## Alternatives

### Do nothing: judge impact by reading the capability's output (added when writing this ADR)

- For: no labelling work.
- Against: unrepeatable, and open to hindsight.

### Naive: an LLM judges whether the impact analysis was right (added when writing this ADR)

- For: cheap, and copes with varied wording.
- Against: puts a probabilistic judge where a deterministic comparison works, and the judge may share the capability's blind spots.

### LLMs write the labels (added when writing this ADR)

- For: fast.
- Against: the answer key would come from the same kind of system being tested. E1's rule, "never as the answer key", rules it out.

### Hand-written two-tier labels, deterministic scoring, LLMs only to flag disagreements (chosen)

- For: a reproducible score, with an independent check on labels that look doubtful.
- Against: Andy's time, and one person's view of the system.

## Enforcement

Most constraints concern private material and can only be held by review: C3, C4, C8, C10 and C11 against the labels themselves. Under hard rule 1, Claude never reads those labels. C6 is barely checked. The bootstrap scripts (`scripts/bootstrap.ps1` and `.sh`) fail only on paths in this repository whose name contains `private-eval`, and they skip `subject/`. A copy of the evaluation repository under its real name, or under `subject/`, wouldn't be caught, and nothing checks the private repository itself. C7 becomes a property of the scoring code, testable once that code exists.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording E1's decided part (5 Oct) and E1b's development-set decision. Tier `cross-cutting` and exceptions `not-allowed` ruled by Andy in chat on 21 Oct, from review of this ADR.
