---
id: ADR-009
version: 2
title: Spec Kit v1.1.2, pinned and core only, with specs that flow forward
status: accepted
date: 2026-11-01
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
    mechanism: bootstrap scripts compare the installed CLI with the pin and exit with code 2 on a mismatch; nothing yet runs them as a gate
    ref: scripts/bootstrap.ps1
    state: manual
  - constraint: C3
    mechanism: review
    ref: null
    state: manual
  - constraint: C4
    mechanism: CI check that no Spec Kit preset or extension is installed (how Spec Kit records installed ones is to be confirmed; .specify/extensions.yml registers hooks, not installs)
    ref: null
    state: planned
  - constraint: C5
    mechanism: review
    ref: null
    state: manual
  - constraint: C6
    mechanism: review; a CI check needs a rule for when a folder becomes fixed, which isn't decided
    ref: null
    state: manual
  - constraint: C7
    mechanism: review
    ref: null
    state: manual
  - constraint: C8
    mechanism: the plan's Constitution Check; review
    ref: .specify/memory/constitution.md
    state: manual
  - constraint: C9
    mechanism: review
    ref: null
    state: manual
  - constraint: C10
    mechanism: ADR validator, comparing the index with the ADRs' front matter
    ref: null
    state: planned
  - constraint: C11
    mechanism: review
    ref: null
    state: manual
  - constraint: C12
    mechanism: review
    ref: null
    state: manual
  - constraint: C13
    mechanism: the plan's Constitution Check; review
    ref: .specify/memory/constitution.md
    state: manual
  - constraint: C14
    mechanism: a generator with the ADR validator; today's index came from a throwaway script
    ref: null
    state: planned
  - constraint: C15
    mechanism: review
    ref: null
    state: manual
  - constraint: C16
    mechanism: review
    ref: null
    state: manual
  - constraint: C17
    mechanism: ADR validator, comparing the quoted hard rules with CLAUDE.md
    ref: null
    state: planned
backlog: [T1, T6]
---

# ADR-009: Spec Kit v1.1.2, pinned and core only, with specs that flow forward

## Context

The project needs one workflow for turning a request into a specified, planned, built change, both for the capability itself and for the exemplar. Spec Kit provides one: constitution, specify, plan, tasks, implement. It also has a growing catalogue of presets and extensions, some official and many third-party, and a known criticism: it is spec-first but not spec-anchored, because specs aren't kept true after the change ships.

This ADR covers building this project. Whether the capability also produces Spec Kit artefacts for changes to the subject system is open (T1).

Spec Kit loads the constitution at nine stages. `plan` builds a Constitution Check from it, and `analyze` and `converge` treat it as non-negotiable: a conflict is automatically CRITICAL and requires the spec, plan or tasks to change. So a paraphrased rule in the constitution beats the ADR it summarises, and `analyze` never reads ADRs themselves. A model of ADR counts (T6) estimates that loading every full ADR passes an assumed 200,000-token window at about 115 ADRs, while an index plus the relevant Constraints sections costs about 13,000 tokens at that size. Those figures rest on assumed ADR counts and a rough token estimate.

## Decision

**Adopt the Spec Kit workflow** for building this project. Skills, subagents and hooks support its stages rather than replacing them.

**Version:** Spec Kit **v1.1.2** (released 7 Oct 2026, commit `959e866`), pinned. Installed with `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.1.2`. Upgrades are deliberate, reviewed changes.

**Workflow:** the constitution once; then, per feature, specify → plan → tasks → implement → converge, repeating implement and converge until converge reports converged. Clarify, checklist and analyze are optional quality gates.

**Initialisation (this repo):** `specify init --here --force --non-interactive --integration claude --script py --ignore-agent-tools`. Claude Code integration in skills mode (`.claude/skills/speckit-*`, invoked as `/speckit-<stage>`). Python scripts, so they behave the same on Windows, macOS, Linux and CI. `--ignore-agent-tools` only because the desktop app doesn't put a `claude` executable on PATH.

**Core only: no presets or extensions yet.** Community extensions and presets are third-party code that the Spec Kit maintainers don't review. None is installed without a source review, a pinned version and an ADR.

**Spec persistence: flow-forward, anchored on decisions.** Each feature folder in `specs/` is a fixed historical record; new requirements get a new folder. What must stay true lives in the ADRs and the constitution, enforced by deterministic checks. This is our answer to the "spec-first but not spec-anchored" criticism: the system is anchored on decisions, not on specs kept current by hand.

**How ADRs connect to the constitution (v2).** The constitution is thin. It holds six principles that point to ADRs without restating them, the two citing rules, the six hard rules quoted word for word, and an index of ADRs. Every plan lists the ADRs that apply and cites their constraints, so the plan carries the rules forward. `analyze` sees those citations and the index, not the ADR text. It judges whether the list looks complete from the index, but doesn't verify a citation against the ADR it names. Agents load an ADR's Constraints section, and open the full ADR only when they need the reasoning. The index holds ID, title and scope, no version, and is generated from the ADRs' front matter, so revising an ADR leaves it alone unless the title or scope changes. ADR titles state the decision, so the title replaces the "one-line decision" in the original Step 6 brief. The index sits inside the constitution because `plan` loads that file automatically.

**The constitution adds no rules of its own.** Every principle cites its source. No ADR constraint is restated. If the constitution and an ADR disagree, neither wins automatically: it is a decision gap for the architecture coordinator.

**Amendments** are approved by the architecture coordinator, and versioned under Spec Kit's semantic versioning rules (the `speckit-constitution` skill).

Which ADRs "apply" is still a judgement. How to select them better is T6's question.

## Constraints

- **C1:** This project MUST be built with the Spec Kit workflow; skills, subagents and hooks MUST support its stages, not replace them.
- **C2:** Spec Kit MUST be pinned at v1.1.2. Upgrades are deliberate, reviewed changes; under ADR-000@v3 C8 and C11, an upgrade is a revision of this ADR.
- **C3:** Each feature MUST go through specify, plan, tasks, implement and converge, repeating implement and converge until converge reports converged.
- **C4:** Spec Kit MUST be used core only, with no presets or extensions installed. Changing that is a revision of this ADR (ADR-000@v3 C11).
- **C5:** A community extension or preset MUST NOT be installed without a source review, a pinned version and an ADR.
- **C6:** Each feature folder in `specs/` MUST be kept as a fixed historical record; new requirements MUST get a new folder.
- **C7:** What must stay true after a change MUST live in the ADRs and the constitution, not in specs.
- **C8:** Every plan MUST list the ADRs that apply.
- **C9:** Agents SHOULD load an ADR's Constraints section, and open the full ADR only when they need its reasoning.
- **C10:** The constitution's ADR index MUST hold ID, title and scope, no version.
- **C11:** Every principle in the constitution MUST cite its source: an ADR, a hard rule, CLAUDE.md or product.md.
- **C12:** A conflict between the constitution and an ADR MUST be treated as a decision gap for the architecture coordinator.
- **C13:** Every plan MUST cite the constraints that apply, as `ADR-nnn@vN Cn`.
- **C14:** The index MUST be generated from the ADRs' front matter.
- **C15:** The constitution MUST NOT restate ADR constraints. Its only rules are C8, C13 and the hard rules.
- **C16:** Constitution amendments MUST be approved by the architecture coordinator, and versioned under Spec Kit's semantic versioning rules.
- **C17:** The constitution MUST quote the hard rules word for word from CLAUDE.md.

## Consequences

Easier:

- A recognisable, documented workflow that reviewers know.
- Specs are honest historical records. Nobody has to keep them current, and nobody is misled when they aren't.

Harder:

- Knowing what is true now means reading ADRs and the constitution, not the latest spec. That only works if the ADRs are complete and enforced.
- Pinning means missing Spec Kit fixes until an upgrade is reviewed.
- Principles point to ADRs without versions, so ADR revisions don't touch them. The constitution's own citations of this ADR do go stale when it is revised; a PATCH amendment fixes them.
- Choosing the right ADRs is still a judgement until T6 settles selection. A missed ADR is silently not applied. The one `plan` run tested listed 14 of 19 ADRs for a small export feature, which shows selection can be broad; recall hasn't been measured. Whether a wrong but well-formed citation is noticed is untested.
- Tested behaviour ([tests/constitution/results.md](../../tests/constitution/results.md)): the citing rules (f2) and hard rules 4 and 6 (f3, f4) were caught in 3 of 3 runs each, with no false CRITICAL on the two compliant fixtures. A blatant breach of ADR-015 was also caught, whether cited or not, from its index title and a principle's heading. A breach that no title reveals (f8, ADR-016's SARIF rule) was missed in 3 of 3 runs. The agents also had CLAUDE.md, which lists the hard rules, so those catches can't be credited to the constitution alone.
- Titles and headings act as rules, though C15 says the constitution's only rules are C8, C13 and the hard rules. *Andy, 2 Nov:* accept it, and measure it. Measured on f9: the wording "no custom coding agent" caused no false CRITICAL, but ADR-011's title led two of three runs to a contested CRITICAL for leaving it out. So a title can produce a CRITICAL with no clear constraint behind it, and runs disagree.
- The hard rules keep two of the problems that sank the 22-rule draft, on a smaller scale. Rules 2, 5 and 6 overlap ADR-005 and ADR-004, and where they overlap `analyze` would side with the hard rule, so C12 doesn't hold there. Rules 1 and 3 describe conduct a plan can't show. No false CRITICAL appeared in the six runs on compliant work, but those fixtures state their own compliance, so this is weak evidence. They are accepted because they are bright lines, quoted, and rarely change.
- This constitution covers this repository only. Plans in the eShop fork won't load it, so the hard-rule safety net doesn't reach eShop work until the fork has its own. When that happens is open (T1).
- A plan template's Complexity Tracking table can record "justified" violations, while project ADRs allow no exceptions (ADR-000@v3 C13). This is untested: the table stayed empty in the plan run.
- A generated index needs a generator, which doesn't exist yet in the repository.

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

### Do nothing: leave the constitution as Spec Kit's blank template (added when writing v2)

- For: no work.
- Against: `plan` and `analyze` would have nothing to check, and no route to the ADRs.

### Naive: load every full ADR into every stage (added when writing v2)

- For: nothing can be missed.
- Against: an estimated 204,000 tokens per load at 117 ADRs.

### Copy every ADR constraint into the constitution (weighed 1 Nov)

- For: `analyze` would see every constraint.
- Against: duplicates more than 160 rules, drifts, and costs an estimated 28,000 tokens per load at 117 ADRs.

### An index with no citing rule (weighed 1 Nov)

- For: small.
- Against: nothing makes an agent open an ADR, or carry its rules into a plan.

### Restate 22 selected rules as constitution MUSTs (drafted, then rejected 1 Nov)

- For: `analyze` sees 21 of 167 rules directly.
- Against: five paraphrases drifted in the first draft, and `analyze` sides with the paraphrase, so no automatic winner wouldn't hold. Seven of the nine ADR revisions to date would have needed an amendment. Several rules can't be shown in a plan, which risks false CRITICALs.

### Quote the same rules word for word (weighed 1 Nov)

- For: no paraphrase.
- Against: the same seven amendments, and stale text is enforced until each one lands.

### Thin, pointing to ADRs, with no hard rules (weighed 1 Nov)

- For: smallest, with no drift.
- Against: predicted to miss a bright-line breach. Not tested separately: the hard rules were in place for every test run.

### Thin, pointing to ADRs, plus the six hard rules (chosen for v2)

- For: no ADR paraphrased, no drift from ADR revisions, and the bright lines stay visible.
- Against: the limits listed under Consequences.

### Spec Kit core, pinned, flow-forward specs anchored on ADRs (chosen)

- For: a standard workflow, reproducible, with truth kept where checks can enforce it.
- Against: depends on ADRs being complete, and upgrades need deliberate work.

T1 also records three extensions as deferred, not rejected: *Brownfield Bootstrap*, deferred to the eShop fork; the official `git` extension, to try on the first spec; and the official `assess` extension, to consider for the research-spike skill.

## Enforcement

C2 is checked by the bootstrap scripts, which compare the installed CLI's version with the pin and exit with code 2 on a mismatch. Nothing runs them as a gate yet (no CI, no hook), so the state is manual. C4 is a planned CI check, once it is confirmed how Spec Kit records installed presets and extensions. C6 needs a rule for when a feature folder becomes fixed (for example, when its feature is merged) before a check can enforce it; until then it is held by review. C8 and C13 are held by the plan's Constitution Check, and `tests/constitution/` tests them against `analyze` and `plan`. It is a model following instructions, so its results are evidence, not enforcement. The comparison of rejected options is predicted from Spec Kit's skill text, not observed. C13's "that apply" has no deterministic test yet, and review can't see what an agent loaded (C9). C10, C14 and C17 are planned for the ADR validator; today's index was generated by a throwaway script. The rest rely on review.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording T1's decided part (5 and 8 Oct).
- **v2** · 2026-11-01 · revision · approved by Andy Douglas in chat: closes T1's open question on how ADRs connect to the constitution. A thin constitution: pointers to ADRs, citing rules for plans, the hard rules word for word, a generated index, constraints-first loading, no automatic winner in a conflict, and amendments approved by Andy (C8 to C17). CLAUDE.md hard rule 2 reworded to "In eShop, build only development outcomes by hand".
