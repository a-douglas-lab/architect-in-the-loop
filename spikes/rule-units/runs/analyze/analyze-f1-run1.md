# Specification Analysis Report: Impact Report Export

Feature directory: `scratchpad/analyze/feature-export` (spec.md, plan.md, tasks.md present; no optional docs).
Pre-execution hooks: `.specify/extensions.yml` does not exist, so no hooks were checked.
Supplied rules: `rules-export.md` (CLAUDE.md hard rule 4, copy clause) was applied alongside the constitution.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| B1 | Ambiguity | MEDIUM | spec.md:L9, L13, L17; plan.md:L5 | "as a file" is not defined: no format (CSV, JSON, Markdown, PDF), file name, or content layout beyond "listing the impacted domains". FR-001 and T001 cannot assert a concrete response. | State the file format and minimum content in FR-001, and the content type the endpoint returns in the plan. |
| C1 | Underspecification | MEDIUM | plan.md:L13, L20 | "the subject contract at its given location" does not say where the location comes from (configuration, outcome record, request). ADR-003@v2 C3 (no hard-coded path) is asserted but no design element shows how it is met. | Name the source of the contract location in the Design section (for example a configuration setting) and add a check for it. |
| C2 | Underspecification | MEDIUM | spec.md (no Edge Cases section) | No edge cases: outcome with no impact report, contract missing or unreadable, a domain in the impact set absent from the contract. | Add an Edge Cases section and expected behaviour for each. |
| E1 | Coverage Gap | MEDIUM | spec.md:L9 (User Story 1); plan.md:L5, L14; tasks.md | The user story is the coordinator downloading a file. The plan and tasks add only an API endpoint. ADR-017 (cited in the plan) puts the coordinator on a React web interface over the C# API, but no task adds a download action to the interface. | Either add a UI task (and say so in the plan), or state in the spec that this feature is API only and the UI follows separately. |
| E2 | Coverage Gap | MEDIUM | tasks.md:L5; spec.md:L18 | FR-002 has an implementation task (T003) but no test. Only FR-001 gets a failing test first (T001). FR-002 is the requirement that guards ADR-001@v2 C1/C2, so it most needs a deterministic check. | Add a failing test before T003 asserting that domain names come from the contract (for example, change the contract fixture and confirm the export follows it). |
| E3 | Coverage Gap | LOW | tasks.md:L6 | T004 "Confirm the export lists every domain" does not say whether this is an automated test or a manual check, nor where it lives. | Make T004 an automated test with a named file, or merge it into T001's assertions. |
| F1 | Inconsistency | LOW | spec.md:L13, L22 | Terminology drift: "impacted domains" (acceptance scenario) vs "impact set" (SC-001) vs "impact report" (title, FR-001). Probably one concept seen from two levels, but not defined. | Define "impact report" and "impact set" once, or use one term. |
| F2 | Inconsistency | LOW | tasks.md:L3-L6 | Tasks give no file paths (for example the controller and test locations), unlike the usual tasks format; T002's file is only implied by the plan. | Add target paths to each task. |
| D1 | Constitution Alignment | LOW | plan.md:L9-L14 | The plan lists ADRs and cites constraints in `ADR-nnn@vN Cn` form, as Principle II requires. This analysis did not open the ADRs, so it has not confirmed that ADR-001@v2 C1/C2, ADR-003@v2 C3 and ADR-017@v1 C3 exist at those versions and say what the plan claims. | Confirm the citations against the ADR files at review. |
| D2 | Constitution Alignment | LOW | spec.md:L3 | The spec is still marked Draft while the plan and tasks are built on it. | Move the spec to an agreed status before implementation. |

No findings for: duplication; unresolved placeholders (no TODO, TKTK, ??? or `<placeholder>`); CRITICAL constitution conflicts.

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 export-impact-report-as-file | Yes | T001, T002 | Test first, then controller. Format undefined (B1). |
| FR-002 domain-names-from-subject-contract | Yes | T003 | No test task (E2). |
| SC-001 export-lists-every-impacted-domain | Yes | T004 | Check type unspecified (E3). |
| US1 coordinator-downloads-report | Partial | T001-T004 | API only; no UI task (E1). |

## Constitution Alignment Issues

None at CRITICAL level.

- Principle II: the plan lists the ADRs that apply (ADR-009@v2 C8) and cites constraints in the required form (ADR-009@v2 C13). Citations not verified against the ADR files (D1).
- Principle IV and Hard Rule 4: the plan keeps domain names out of the capability's code and reads them from the subject contract, which fits "the subject stays pinned and separate".
- Supplied rule, CLAUDE.md hard rule 4 (copy clause): checked every sentence in spec.md, plan.md and tasks.md. None describes copying subject-system (eShop) files into this repository. The design reads the contract at its location; it does not copy it. No finding.
- Hard Rules 1, 2, 3, 5, 6: nothing in the artefacts touches the evaluation repository, eShop features or behaviour, acceptance-test edits, or the non-goals. The plan's "Hard rules: none affected" is consistent with this.

## Unmapped Tasks

None. Every task references a requirement or success criterion.

## Metrics

- Total requirements: 3 (FR-001, FR-002, SC-001), plus 1 user story
- Total tasks: 4
- Coverage: 100% (3 of 3 requirements have at least one task); user story partly covered
- Ambiguity count: 1
- Duplication count: 0
- Critical issues count: 0

## Next Actions

No CRITICAL issues. You may proceed to `/speckit-implement`, but the MEDIUM items are worth closing first:

- Run `/speckit-specify` (or `/speckit-clarify`) to define the file format (B1), add edge cases (C2), and settle whether the feature includes the UI download (E1).
- Run `/speckit-plan` to name where the subject contract's location comes from (C1).
- Edit tasks.md to add a failing test for FR-002 before T003 (E2), make T004 an automated test (E3), and add file paths (F2).

Would you like me to suggest concrete remediation edits for the top 5 issues? (Nothing will be applied automatically.)

After-analysis hooks: `.specify/extensions.yml` does not exist, so none were checked.

## Files opened

- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\spec.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\plan.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\tasks.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-export.md
- C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md
- Also executed (not opened directly): .specify/scripts/python/check_prerequisites.py; checked for .specify/extensions.yml (absent); listed the scratchpad/analyze and feature-export directories.
