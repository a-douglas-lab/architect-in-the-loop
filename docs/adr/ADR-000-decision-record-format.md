---
id: ADR-000
title: Decision records use our own template, extending MADR 4.0.0
status: accepted
date: 2026-10-20
decision-makers: [Andy Douglas]
scope: [capability, subject, concern:governance]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: ADR validator script, run as a hook and in CI
    ref: null
    state: planned
  - constraint: C2
    mechanism: ADR validator script, run as a hook and in CI
    ref: null
    state: planned
  - constraint: C3
    mechanism: ADR validator script (file name matches id)
    ref: null
    state: planned
  - constraint: C4
    mechanism: ADR validator script, comparing with the previous commit
    ref: null
    state: planned
  - constraint: C5
    mechanism: ADR validator script (every listed constraint ID exists in the Constraints section, and the reverse)
    ref: null
    state: planned
  - constraint: C6
    mechanism: review
    ref: null
    state: manual
  - constraint: C7
    mechanism: review
    ref: null
    state: manual
backlog: [T2, G5, G12, Q1]
---

# ADR-000: Decision records use our own template, extending MADR 4.0.0

## Context

Every decision in this project becomes an architecture decision record (ADR). The capability also reads ADRs as data. It selects the ones that govern a change (T6), lets the arbiter apply precedence between them (G5), honours approved exceptions (G12), and reports how many ADR clauses are enforced deterministically (Q1). So an ADR has two readers: a person, who needs the reasoning, and a program, which needs fields and rules it can extract without guessing.

This ADR decides the format: the front matter, the fixed sections and the rules for changing an ADR. It applies to ADRs in this repository and to the subject system's ADRs in the eShop fork. It does not decide how ADRs are selected or loaded into agent context (T6), or which mechanism enforces which rule type (Q1).

Criteria:

1. **Machine-readable:** an agent or check can extract status, scope, precedence, constraints and enforcement without reading prose.
2. **Human-readable:** the reasoning and the options considered stay in plain prose.
3. **Covers G5 and G12:** a precedence field the arbiter can apply, and a link to exceptions.
4. **Measurable enforcement:** each constraint maps to a check, so "share of constraints enforced deterministically" can be counted.
5. **Familiar:** a reviewer recognises the format, and existing tools mostly still work.
6. **Cheap:** a commodity item (backlog research method), so a sensible default, not a research project.

## Decision

Use our own template, [template.md](template.md): MADR 4.0.0 extended with front matter for scope, precedence, supersession, exceptions and enforcement, and a separate **Constraints** section.

MADR is the closest standard. It already has YAML front matter, a list of options with pros and cons, and an optional "Confirmation" section on how compliance is checked. What it lacks is what the capability needs to act on: scope tags, precedence, a link to exceptions, and constraints that a check can be mapped to one by one. The split between **Decision** (prose, for people) and **Constraints** (numbered, single checkable statements, for agents and checks) follows the proposed principle in A1: structure what the system acts on, keep prose for reasoning.

How the fields are read:

- **Precedence (G5).** When two ADRs conflict, the arbiter applies an explicit `overrides` entry first, then tier: cross-cutting binds domain, and domain binds component. If neither settles it, that is a decision gap for the architecture coordinator, never a judgement call by the arbiter.
- **Exceptions (G12).** `exceptions` says only whether exceptions to this ADR may be granted. Each exception is its own record in `docs/adr/exceptions/`, naming the ADR and constraint, the scope, the reason, the approver and the expiry date, so granting one never edits an accepted ADR. The format of exception records is decided with Q1, when checks first read them.
- **Enforcement (Q1).** One entry per constraint, with state `enforced`, `planned` or `manual`. The share of constraints in state `enforced` with a deterministic mechanism is the published metric.

## Constraints

- **C1:** Every ADR MUST start with YAML front matter containing all the fields in the template: `id`, `title`, `status`, `date`, `decision-makers`, `scope`, `precedence` (with `tier` and `overrides`), `supersedes`, `superseded-by`, `exceptions`, `enforcement` and `backlog`.
- **C2:** Every ADR MUST contain these second-level sections, in this order and with these exact names: Context, Decision, Constraints, Consequences, Alternatives, Enforcement.
- **C3:** ADR IDs MUST be `ADR-` plus three digits, unique within the repository, and the file name MUST start with the ID (`ADR-nnn-short-title.md`). The subject system's ADRs in the eShop fork use their own sequence.
- **C4:** Once an ADR is accepted, only `status`, `date`, `superseded-by` and the `state` and `ref` of enforcement entries MAY change. Any other change MUST be a new ADR that supersedes it.
- **C5:** Every constraint in the Constraints section MUST have exactly one entry in `enforcement`, and every entry MUST name an existing constraint.
- **C6:** Each constraint SHOULD be a single checkable statement, using MUST, MUST NOT or SHOULD.
- **C7:** Alternatives MUST include "do nothing" and, where it applies, the naive option (an LLM with everything in its prompt), as the backlog's research method requires.

## Consequences

Easier:

- The capability, hooks and CI can parse every ADR the same way, in both repositories.
- "Share of constraints enforced deterministically" is a count over front matter, not a judgement.
- Precedence and exceptions have a defined home, so the arbiter's rule from G5 has data to work on.

Harder:

- More front matter than Nygard or plain MADR. Writing an ADR takes longer; the ADR-writing skill (Step 7) should fill the boilerplate.
- Two places describe enforcement: the front matter list, which is authoritative, and the Enforcement section, which holds only the notes the list can't. Writers have to keep that split.
- The enforcement `state` changes as checks are built, so accepted ADRs still get small edits. C4 limits what may change.
- MADR tools that expect MADR's exact headings won't recognise ours. None is in use yet.

To do:

- Build the ADR validator (C1 to C5) with the D1 hooks in Step 7, and run it in CI. Until then every constraint here is planned or manual, and this ADR says so.
- Decide the exception record format with Q1.
- Copy the template into the eShop fork when the subject's baseline ADRs are written (P4, Phase 2).

## Alternatives

### Do nothing: free-form markdown decisions

- For: no effort; the backlog already records decisions.
- Against: nothing for a program to parse, so selection, precedence and enforcement counts all depend on an LLM reading prose. This is the "load decisions into a prompt and hope" approach the product exists to replace.

### Naive: no records, decisions kept in CLAUDE.md and prompts

- For: decisions sit directly in agent context.
- Against: no history, no status, no supersession and no scope, and context grows with every decision. Nothing proves a decision was applied.

### Nygard (Title, Status, Context, Decision, Consequences)

- For: the best-known format, minimal, supported by adr-tools.
- Against: no metadata beyond status, no options considered, nothing for scope, precedence or enforcement. We would add all of it ourselves, ending up with our own template anyway, on a weaker base.

### MADR 4.0.0, unchanged

- For: a maintained standard with YAML front matter (status, date, decision-makers, consulted, informed), considered options with pros and cons, and an optional Confirmation section close to our Enforcement.
- Against: no scope, precedence, exceptions or per-constraint enforcement, and no separation between the reasoning and the checkable rules. Confirmation is prose, so enforcement can't be counted.

### Our own template, extending MADR 4.0.0 (chosen)

- For: meets all six criteria. Recognisable as MADR to a reviewer; adds only the fields the capability acts on.
- Against: a custom format to maintain and validate ourselves; more front matter to write.

## Enforcement

Nothing in this ADR is enforced yet. C1 to C5 are mechanical, so they are planned for a validator script run as a hook and in CI (Step 7). C6, single checkable statements, and C7, required alternatives, need judgement and stay with review. C6 is a candidate for a runtime rubric later (A5).
