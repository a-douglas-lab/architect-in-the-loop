# Specification Analysis Report: Analyzer Findings for the Repair Loop

Feature directory: `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings`

Prerequisites script output: `AVAILABLE_DOCS: ["tasks.md"]`. spec.md and plan.md are both present in the feature directory and were loaded. No `.specify/extensions.yml` exists, so no before or after hooks were checked or run.

Rules taken into account (from rules-findings.md): ADR-016@v1 C10 (violation reports MUST be SARIF; mechanical) and CLAUDE.md hard rule 4, copy clause (bright-line).

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | Constitution Alignment | CRITICAL | spec.md:L18 (FR-002), spec.md:L22 (SC-001), plan.md:L5, plan.md:L17, tasks.md:L5-L6 (T003, T004) | The artefacts describe a violation report and name CSV (`findings.csv`) as its output format, without naming SARIF. This breaks ADR-016@v1 C10: "Tools that report rule violations MUST report in SARIF." Under Principle II (Decisions Are Recorded and Honoured), an applicable ADR MUST constraint cannot be set aside by a spec. | Change FR-002, SC-001, the plan's Summary and Design, and T003/T004 to write a SARIF log (for example `findings.sarif`) with rule ID, file, line and message mapped to SARIF `ruleId`, `locations` and `message`. If CSV is still wanted for the repair loop, make it a derived view of the SARIF log, not the report. If SARIF is not wanted, that needs an ADR-016 change, outside this analysis. |
| D2 | Constitution Alignment | CRITICAL | plan.md:L9-L11 (Constitution Check) | The plan lists only ADR-001 as applying and cites only ADR-001@v2 C1. ADR-016 (scope: capability, concern:quality) governs tools that report rule violations, which is exactly this feature. Constitution Principle II: "Every plan MUST list the ADRs that apply (ADR-009@v2 C8)" and "MUST cite the constraints that apply, as `ADR-nnn@vN Cn` (ADR-009@v2 C13)." | Add ADR-016 to "ADRs that apply" and cite `ADR-016@v1 C10` in the Constitution Check, with how the design complies. |
| C1 | Underspecification | MEDIUM | spec.md:L17 (FR-001), plan.md:L17 | "The analyzers it runs" are not named, nor is their output format. The plan says the collector "converts their output to rows" without saying from what. Conversion and test fixtures cannot be designed without this. | Name the analyzers (or the input contract, for example SARIF already emitted by them) in the plan's Design. |
| C2 | Underspecification | MEDIUM | spec.md (whole), plan.md (whole) | No Edge Cases section. Unhandled cases: no violations (empty report), an analyzer that fails or crashes, findings without a line number, duplicate findings across analyzers, findings outside the changed code (US1 says "code the capability changed"). | Add an Edge Cases section to the spec and matching behaviour to the plan. |
| C3 | Underspecification | MEDIUM | spec.md:L9, plan.md:L17 | US1 says findings are limited to "code the capability changed", but no requirement or plan element filters findings to the change. FR-001 collects all violations. | Either add a requirement that scopes findings to changed files/lines, or drop the restriction from US1. |
| E1 | Coverage Gap | MEDIUM | spec.md:L13 (US1 scenario 1), tasks.md | No task covers the repair loop receiving the findings (the user story's actual outcome). Tasks stop at writing the file. The plan says "The repair loop reads the CSV" but no task makes or checks that hand-off. | Add a task for the repair-loop hand-off (read and act on the report), or state in the plan that the repair loop's reader is out of scope and owned elsewhere. |
| E2 | Coverage Gap | MEDIUM | tasks.md:L3-L6 | Only FR-001 has a test-first task (T001). FR-002 (output format and columns) has no failing test written before T003. T004 is a confirmation step with no stated test, fixture or expected result. Project practice (CLAUDE.md, ADR-012) is behaviour tested with expected results written first. | Add a failing test for the report format before T003 (once D1 is fixed, a SARIF schema validation test). Make T004 a concrete test with a fixture of known violations and the expected count. |
| E3 | Coverage Gap | LOW | plan.md:L11, tasks.md | The plan cites ADR-001@v2 C1 ("the collector holds no subject-domain terms") but no task checks it. | Add a check task (for example, a test or lint that the collector code contains no subject-domain terms). |
| F1 | Inconsistency | LOW | spec.md:L13 vs spec.md:L18, plan.md:L17 | The acceptance scenario lists rule, file and line; FR-002 and the plan add message. Minor drift. | Add message to the acceptance scenario so the fields agree. |
| F2 | Inconsistency | LOW | spec.md, plan.md, tasks.md | Terminology drift: "findings" (title, US1), "violations" (FR-001, FR-002, SC-001), "rule violations", "rows". | Pick one term (for example "finding" for a reported rule violation) and define it once. |
| B1 | Ambiguity | LOW | spec.md:L22 (SC-001) | "Every violation an analyzer reports" has no stated test set, so the criterion is measurable only once the analyzers and a fixture are named (see C1, E2). | Tie SC-001 to a named fixture with a known violation count. |
| C4 | Underspecification | LOW | plan.md (whole) | The plan has no technical context (language, stack, where the collector lives, where the report is written). | Add a Technical Context section. |

CLAUDE.md hard rule 4 (copy clause): no sentence in spec.md, plan.md or tasks.md describes copying subject-system files. No finding. The plan's "Hard rules: none affected" is consistent with this.

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 collect-analyzer-violations | Yes | T001, T002 | Analyzers unnamed (C1) |
| FR-002 write-violations-report | Yes | T003 | Format conflicts with ADR-016@v1 C10 (D1); no test-first task (E2) |
| SC-001 every-violation-reported | Yes | T004 | Format conflict (D1); no fixture or expected result (E2, B1) |
| US1 repair-loop-receives-findings | No | none | Hand-off not covered (E1) |

## Constitution Alignment Issues

- D1: the report format (CSV) conflicts with ADR-016@v1 C10 (SARIF required), so the decision is not honoured (Principle II).
- D2: the plan's Constitution Check omits ADR-016 and its constraint citation (Principle II, ADR-009@v2 C8 and C13).

## Unmapped Tasks

None. Every task references an FR or SC.

## Metrics

- Total Requirements: 3 (FR-001, FR-002, SC-001), plus 1 user story
- Total Tasks: 4
- Coverage: 100% of requirements have at least one task (3 of 3); user story outcome not covered
- Ambiguity Count: 1 (B1)
- Duplication Count: 0
- Critical Issues Count: 2

## Next Actions

- CRITICAL issues exist: resolve D1 and D2 before `/speckit-implement`.
- Run `/speckit-specify` with refinement to change FR-002 and SC-001 to a SARIF report and to add Edge Cases (C2) and the scope question (C3).
- Run `/speckit-plan` to list ADR-016 and cite ADR-016@v1 C10 in the Constitution Check, name the analyzers and their input format (C1), and add Technical Context (C4).
- Run `/speckit-tasks` (or edit tasks.md manually) to add a failing format test before T003, a concrete fixture-based test for SC-001, a repair-loop hand-off task, and an ADR-001@v2 C1 check (E1 to E3).

## Remediation

Would you like me to suggest concrete remediation edits for the top 5 issues? (Nothing has been changed.)

## Files opened

- C:\Users\adoug\Architect-in-the-loop\.claude\skills\speckit-analyze (skill loaded via the Skill tool)
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\spec.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\plan.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\tasks.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-findings.md
- C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md
- Run, not read: .specify/scripts/python/check_prerequisites.py; checked for .specify/extensions.yml (absent)
