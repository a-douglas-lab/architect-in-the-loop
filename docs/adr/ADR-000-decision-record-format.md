---
id: ADR-000
version: 2
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
    mechanism: none
    ref: null
    state: withdrawn
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
  - constraint: C8
    mechanism: ADR validator script, comparing with the previous commit (version incremented, History line added)
    ref: null
    state: planned
  - constraint: C9
    mechanism: ADR validator script, comparing with the previous commit (no constraint ID removed or reused)
    ref: null
    state: planned
  - constraint: C10
    mechanism: review; later, checks on spec, plan and trace formats
    ref: null
    state: manual
  - constraint: C11
    mechanism: review against the History type; the reviewer checks corrections against their source
    ref: null
    state: manual
  - constraint: C12
    mechanism: review
    ref: null
    state: manual
backlog: [T2, G5, G12, Q1]
---

# ADR-000: Decision records use our own template, extending MADR 4.0.0

## Context

Every decision in this project becomes an architecture decision record (ADR). The capability also reads ADRs as data. It selects the ones that govern a change (T6), lets the arbiter apply precedence between them (G5), honours approved exceptions (G12), and reports how many ADR clauses are enforced deterministically (Q1). So an ADR has two readers: a person, who needs the reasoning, and a program, which needs fields and rules it can extract without guessing.

This ADR decides the format: the front matter, the fixed sections, how an ADR changes over time, and which repository a decision belongs in. It applies to ADRs in this repository and to the subject system's ADRs in the eShop fork. It does not decide how ADRs are selected or loaded into agent context (T6), or which mechanism enforces which rule type (Q1).

Criteria:

1. **Machine-readable:** an agent or check can extract status, scope, precedence, constraints and enforcement without reading prose.
2. **Human-readable:** the reasoning and the options considered stay in plain prose.
3. **Covers G5 and G12:** a precedence field the arbiter can apply, and a link to exceptions.
4. **Measurable enforcement:** each constraint maps to a check, so "share of constraints enforced deterministically" can be counted.
5. **Familiar:** a reviewer recognises the format, and existing tools mostly still work.
6. **Cheap:** a commodity item (backlog research method), so a sensible default, not a research project.
7. **Cheap recall (added in v2):** an agent reads one file per decision, always the current text, without following chains of superseded records.

## Decision

Use our own template, [template.md](template.md): MADR 4.0.0 extended with front matter for version, scope, precedence, supersession, exceptions and enforcement, a separate **Constraints** section, and a short **History** section.

MADR is the closest standard. It already has YAML front matter, a list of options with pros and cons, and an optional "Confirmation" section on how compliance is checked. What it lacks is what the capability needs to act on: scope tags, precedence, a link to exceptions, and constraints that a check can be mapped to one by one. The split between **Decision** (prose, for people) and **Constraints** (numbered, single checkable statements, for agents and checks) follows the proposed principle in A1: structure what the system acts on, keep prose for reasoning.

How the fields are read:

- **Precedence (G5).** When two ADRs conflict, the arbiter applies an explicit `overrides` entry first, then tier: cross-cutting binds domain, and domain binds component. If neither settles it, that is a decision gap for the architecture coordinator, never a judgement call by the arbiter.
- **Exceptions (G12).** `exceptions` says only whether exceptions to this ADR may be granted. Each exception is its own record in `docs/adr/exceptions/`, naming the ADR and constraint, the scope, the reason, the approver and the expiry date, so granting one never edits an ADR. The format of exception records is decided with Q1, when checks first read them.
- **Enforcement (Q1).** One entry per constraint, with state `enforced`, `planned`, `manual` or `withdrawn`. The share of constraints in state `enforced` with a deterministic mechanism is the published metric; withdrawn constraints don't count.

**How an ADR changes (v2).** An ADR is versioned in place. The file always holds the current, complete text of the decision; git holds every earlier version. Each change increments `version` and adds one line to History, typed as either:

- **correction:** brings the text back into line with the recorded decision or the facts. It never changes the decision. The reviewer checks each correction against its source (REVIEW.md).
- **revision:** changes the decision itself. It needs the architecture coordinator's approval, recorded in the History line.

`supersedes` and `superseded-by` are kept only for when the question itself changes: a decision split into two, or two merged into one. A changed answer to the same question is a new version, not a new ID.

Anything that cites an ADR records its version, for example `ADR-005@v2 C2`, so the rule that applied to a change can always be recovered with `git show`. Constraint IDs are never reused: a constraint that is dropped stays listed as withdrawn.

**Which repository a decision belongs in (v2).** A **subject ADR** decides something about the subject system's own design: its domains and contexts, contracts, data and code conventions. Subject ADRs live with the subject's code, in the eShop fork (ADR-003). A decision about how this project uses or treats the subject, such as which version is pinned or which features stay off, is a **project ADR** and lives here, even when its scope includes `subject`.

## Constraints

- **C1:** Every ADR MUST start with YAML front matter containing all the fields in the template: `id`, `version`, `title`, `status`, `date`, `decision-makers`, `scope`, `precedence` (with `tier` and `overrides`), `supersedes`, `superseded-by`, `exceptions`, `enforcement` and `backlog`.
- **C2:** Every ADR MUST contain these second-level sections, in this order and with these exact names: Context, Decision, Constraints, Consequences, Alternatives, Enforcement, History.
- **C3:** ADR IDs MUST be `ADR-` plus three digits, unique within the repository, and the file name MUST start with the ID (`ADR-nnn-short-title.md`). The subject system's ADRs in the eShop fork use their own sequence.
- **C4:** *Withdrawn in v2, replaced by C8 to C11.* (Was: only status, date, superseded-by and enforcement state and ref may change once an ADR is accepted.)
- **C5:** Every constraint in the Constraints section MUST have exactly one entry in `enforcement`, and every entry MUST name an existing constraint.
- **C6:** Each constraint SHOULD be a single checkable statement, using MUST, MUST NOT or SHOULD.
- **C7:** Alternatives MUST include "do nothing" and, where it applies, the naive option (an LLM with everything in its prompt), as the backlog's research method requires. Alternatives that weren't recorded when the decision was taken MUST be marked as added when the ADR was written.
- **C8:** Any change to an accepted ADR, other than to an enforcement entry's `state` or `ref`, MUST increment `version` and add one History line giving the version, date, type (correction or revision), approver and a one-line summary.
- **C9:** A constraint ID MUST NOT be removed or reused. A dropped constraint stays in the list, marked withdrawn, with enforcement state `withdrawn`.
- **C10:** Anything that cites an ADR constraint (specs, plans, traces, evaluation records) MUST record the ADR's version, as `ADR-nnn@vN Cn`.
- **C11:** A revision MUST be approved by the architecture coordinator. A correction MUST NOT change the decision.
- **C12:** A subject ADR, as defined above, MUST live in the subject's repository. A project ADR MUST live in this repository.

## Consequences

Easier:

- The capability, hooks and CI can parse every ADR the same way, in both repositories.
- "Share of constraints enforced deterministically" is a count over front matter, not a judgement.
- Precedence and exceptions have a defined home, so the arbiter's rule from G5 has data to work on.
- Recall reads one current file per decision. Selection (T6) never loads retired text or follows chains.

Harder:

- More front matter than Nygard or plain MADR. Writing an ADR takes longer; the ADR-writing skill (Step 7) should fill the boilerplate.
- The file is no longer an immutable record. What applied to a past change has to be recovered from git, which only works if every citation records the version (C10).
- "Correction" could become a way to change a decision quietly. C11, the History type and the reviewer's check against the source are the guard.
- Two places describe enforcement: the front matter list, which is authoritative, and the Enforcement section, which holds only the notes the list can't.
- MADR tools that expect MADR's exact headings won't recognise ours. None is in use yet.

To do:

- Build the ADR validator (C1 to C3, C5, C8, C9) with the D1 hooks in Step 7, and run it in CI. Until then every constraint here is planned or manual, and this ADR says so.
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

### Immutable ADRs, changed only by superseding (v1's rule)

- For: the file itself is the audit record; the usual ADR practice.
- Against: every correction creates a new ID and a chain to follow, so recall gets slower and dearer. The first review showed the rule biting within hours of acceptance, on write-up errors rather than changes of mind.

### Our own template, extending MADR 4.0.0, versioned in place (chosen)

- For: meets all seven criteria. Recognisable as MADR to a reviewer; adds only the fields the capability acts on; one current file per decision.
- Against: a custom format to maintain and validate ourselves; more front matter; history depends on git and on versioned citations.

## Enforcement

Nothing in this ADR is enforced yet. C1 to C3, C5, C8 and C9 are mechanical, so they are planned for a validator script run as a hook and in CI (Step 7). C6, C7, C11 and C12 need judgement and stay with review. C10 becomes checkable once spec, plan and trace formats exist. C6 is a candidate for a runtime rubric later (A5).

## History

- **v1** · 2026-10-20 · accepted · Andy Douglas: first version.
- **v2** · 2026-10-20 · revision · approved by Andy Douglas in chat: ADRs are versioned in place instead of superseded (C4 withdrawn; C8 to C11 added); `version` field and History section added; withdrawn state added; alternatives added at write-up must be marked (C7); subject and project ADRs defined (C12). Bootstrapping note: v1's C4 forbade this edit. Strictly, the change should have been a new ADR. It was made as v2, under the rule it introduces, with Andy's explicit approval.
