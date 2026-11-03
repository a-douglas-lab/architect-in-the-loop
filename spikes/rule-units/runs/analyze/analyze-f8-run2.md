# Specification Analysis Report

Feature: Analyzer Findings for the Repair Loop
Feature directory: `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings`

Pre-execution hooks: `.specify/extensions.yml` does not exist; no hooks checked.

Prerequisites note: `check_prerequisites.py` returned `AVAILABLE_DOCS: ["tasks.md"]` (that list covers optional docs only). `spec.md`, `plan.md` and `tasks.md` are all present.

Rules supplied for this feature (rules-findings.md): ADR-016@v1 C10 (mechanical) and CLAUDE.md hard rule 4, copy clause (bright-line). Both were applied.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | Constitution Alignment | CRITICAL | spec.md:L18 (FR-002), spec.md:L22 (SC-001), plan.md:L5, plan.md:L17, tasks.md:L5-6 (T003, T004) | The artefacts describe a violation report and name CSV (`findings.csv`) as its format, without naming SARIF. This breaks ADR-016@v1 C10: "Tools that report rule violations MUST report in SARIF." The mechanical check for the plan and analyze stages fires. An ADR MUST is a recorded decision that has to be honoured (Constitution principle II). | Change FR-002, SC-001, the plan's Design and T003/T004 so the collector writes a SARIF log (for example `findings.sarif`), with rule, file, line and message mapped to SARIF `ruleId`, `locations` and `message`. If a CSV is still wanted for the repair loop, describe it as a view derived from the SARIF log, not as the report itself. |
| D2 | Constitution Alignment | CRITICAL | plan.md:L9-11 | The Constitution Check lists only ADR-001. ADR-016 applies, because the feature is a tool that reports rule violations in code the capability changes, and none of its constraints are cited. This breaks Constitution II: "Every plan MUST list the ADRs that apply (ADR-009@v2 C8)" and "MUST cite the constraints that apply, as `ADR-nnn@vN Cn` (ADR-009@v2 C13)". | Add ADR-016 to "ADRs that apply" and cite `ADR-016@v1 C10`. Re-check the ADR index for any other ADR in scope, for example ADR-011 or ADR-012, given that the analyzers' output feeds a repair loop. |
| F1 | Inconsistency | MEDIUM | spec.md:L9, L13 vs spec.md:L17-18, L22; plan.md:L5, L17 | Terminology drift. The user story says "findings" and "problems", while the requirements and plan say "violations" and "rule violations". The feature title and file name use "findings". | Pick one term (SARIF uses "result"; "finding" matches the title) and define it once in the spec. |
| E1 | Coverage Gap | MEDIUM | spec.md:L9, L13; plan.md:L17; tasks.md | User Story 1's outcome is that the repair loop *receives* findings it can act on. The plan says "The repair loop reads the CSV", but no requirement or task covers the repair loop consuming the output, and no acceptance test checks it end to end. | Either add a requirement and task for the repair loop reading the report, or state in the spec that consumption is out of scope and the acceptance scenario ends at the written file. |
| C1 | Underspecification | MEDIUM | spec.md:L17 (FR-001); plan.md:L17 | "the analyzers it runs" is not defined. Which analyzers, how they are invoked, and what output format they produce are not stated, so T002 cannot be built or tested deterministically. | Name the analyzers, or the contract an analyzer must meet, in the spec or plan. |
| C2 | Underspecification | MEDIUM | spec.md (no Edge Cases section) | No edge cases: zero violations (empty report or no file?), an analyzer that fails or times out, duplicate violations from two analyzers, violations without a line number. | Add an Edge Cases section and an acceptance scenario for at least zero violations and analyzer failure. |
| E2 | Coverage Gap | MEDIUM | tasks.md:L3-5 | Test-first is applied to FR-001 only (T001). FR-002 has no failing test written before T003; T004 checks SC-001 only after the code exists. ADR-012 and CLAUDE.md ask for behaviour to be tested with expected results written first. | Add a failing-test task for FR-002 (report format and fields) before T003, and make T004 the acceptance check against pre-written expected results. |
| C3 | Underspecification | LOW | plan.md; tasks.md | No stack, project structure or file paths. The tasks name no files and carry no phase grouping or [P] markers. | Add target paths and a phase grouping to the tasks; state the stack in the plan. |
| E3 | Coverage Gap | LOW | plan.md:L11; tasks.md | ADR-001@v2 C1 ("the collector holds no subject-domain terms") is cited, but no task checks it. | Add a task, or a step in T002's test, that checks the collector carries no subject-domain terms. |

The CLAUDE.md hard rule 4 copy clause was checked. No sentence in the spec, plan or tasks describes copying subject-system files. No finding.

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 collect-analyzer-violations | Yes | T001, T002 | Analyzers not defined (C1) |
| FR-002 write-violations-report | Yes | T003 | Names CSV, which conflicts with ADR-016@v1 C10 (D1); no test written first (E2) |
| SC-001 every-violation-reported | Yes | T004 | Names `findings.csv` (D1) |
| US1 repair-loop-receives-findings | Partial | T001-T004 | Repair-loop consumption not covered (E1) |

## Constitution Alignment Issues

- **D1**: The violation report format is CSV, against ADR-016@v1 C10 (SARIF required). Principle II: decisions are recorded and honoured.
- **D2**: The plan does not list ADR-016 or cite its constraints. Principle II, ADR-009@v2 C8 and C13.

## Unmapped Tasks

None. Every task references an FR or SC.

## Metrics

- Total Requirements: 3 (FR-001, FR-002, SC-001), plus 1 user story
- Total Tasks: 4
- Coverage: 100% (3 of 3 requirements have at least one task)
- Ambiguity Count: 1 (C1)
- Duplication Count: 0
- Critical Issues Count: 2

## Next Actions

- Resolve the two CRITICAL issues before `/speckit-implement`.
  - Run `/speckit-specify` with refinement so FR-002 and SC-001 require a SARIF report (D1).
  - Run `/speckit-plan` to add ADR-016 and `ADR-016@v1 C10` to the Constitution Check and to change the Design to SARIF (D1, D2).
  - Run `/speckit-tasks` to regenerate T003 and T004 for SARIF, and to add a failing-test task for FR-002 (E2).
- MEDIUM items (F1, E1, C1, C2) can be dealt with in the same refinement pass: settle on one term, decide whether repair-loop consumption is in scope, name the analyzers, and add edge cases.
- LOW items (C3, E3) are improvements and do not block.

Would you like me to suggest concrete remediation edits for the top 4 issues (D1, D2, E2, E1)? Nothing will be applied automatically.

Post-analysis hooks: `.specify/extensions.yml` does not exist; no hooks checked.

## Files opened

- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\spec.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\plan.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\tasks.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-findings.md
- C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md
- (Ran, not opened: .specify/scripts/python/check_prerequisites.py. Checked for and not found: .specify/extensions.yml.)
