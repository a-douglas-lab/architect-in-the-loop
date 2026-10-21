---
id: ADR-nnn
version: 1                  # incremented on every change (ADR-000@v2 C8)
title: Short statement of the decision
status: proposed            # proposed | accepted | rejected | deprecated | superseded
date: YYYY-MM-DD            # date of the last status change
decision-makers: [Andy Douglas]
scope: []                   # tags, e.g. capability, subject, domain:ordering, concern:security
precedence:
  tier: domain              # cross-cutting | domain | component
  overrides: []             # ADR IDs this decision explicitly wins against
supersedes: []              # ADR IDs
superseded-by: null         # ADR ID, set only when this ADR is replaced
exceptions: allowed         # allowed | not-allowed (exception records live in docs/adr/exceptions/)
enforcement:
  - constraint: C1
    mechanism: none         # e.g. hook, architecture test, schema, analyser, CI check, grader, review
    ref: null               # path or link to the check
    state: manual           # enforced | planned | manual | withdrawn
backlog: []                 # backlog item IDs this ADR closes or relates to
---

# ADR-nnn: Short statement of the decision

## Context

What problem this decides and why now. The forces at work and the criteria used to judge the options. Make the scope explicit: what this ADR covers and what it doesn't.

## Decision

What we chose, in plain words, and why it beat the alternatives. Prose: the reasoning lives here.

## Constraints

Numbered rules that follow from the decision. Each one is a single, checkable statement that an agent or a check can act on without reading the prose above.

- **C1:** Something MUST (or MUST NOT, or SHOULD) be true.

## Consequences

What becomes easier, what becomes harder, and what we now have to do. Include the bad consequences.

## Alternatives

Each option considered, including the naive one and "do nothing", with what counted for and against it, and the evidence where a spike was run. Mark any option that wasn't weighed when the decision was taken with "(added when writing this ADR)".

### Option name

- For:
- Against:

## Enforcement

The `enforcement` list in the front matter is the record of which check covers which constraint; don't repeat it here. Use this section for what the list can't say: why a constraint is still manual or only planned, what a check misses, and what would make it deterministic.

## History

One line per version: version, date, type, approver, one-line summary. v1's type is `accepted`; later versions are `correction` or `revision` (ADR-000@v2 C8).

- **v1** · YYYY-MM-DD · accepted · Andy Douglas: first version.
