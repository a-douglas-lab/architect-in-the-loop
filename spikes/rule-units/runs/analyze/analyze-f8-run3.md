# Specification Analysis Report

Feature: Analyzer Findings for the Repair Loop
Feature directory: `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings`

Pre-execution: `.specify/extensions.yml` does not exist, so no hooks were checked. The prerequisites script returned the feature directory and `AVAILABLE_DOCS: ["tasks.md"]`, but exited with code 2 (no stderr shown). spec.md, plan.md and tasks.md are all present, so the analysis went ahead.

Rules taken into account: the selected rules in `rules-findings.md` (ADR-016@v1 C10, SARIF for violation reports; CLAUDE.md hard rule 4, copy clause), plus the constitution.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | Constitution Alignment | CRITICAL | spec.md:L18 (FR-002), spec.md:L22 (SC-001), plan.md:L5, plan.md:L17, tasks.md:L5-6 (T003, T004) | The artefacts describe a violation report and name CSV (`findings.csv`) as its format, without naming SARIF. ADR-016@v1 C10: "Tools that report rule violations MUST report in SARIF." The selected rule's analyze-stage check fires. Principle II (Decisions Are Recorded and Honoured) makes an ADR MUST binding on the plan. | Change FR-002, SC-001, the plan design and T003/T004 to write a SARIF log (for example `findings.sarif`), mapping rule to `ruleId`, file and line to `locations[].physicalLocation`, message to `message.text`. If CSV is still wanted for the repair loop, make it a derived view of the SARIF, not the report. Do not reinterpret the ADR here; if SARIF is wrong for this case, change ADR-016 separately. |
| D2 | Constitution Alignment | CRITICAL | plan.md:L9-11 | The Constitution Check lists only ADR-001 and cites only ADR-001@v2 C1. ADR-016 (scope: capability, concern:quality) applies to a capability component that reports rule violations, and its constraint C10 governs this feature directly. Breaks "Every plan MUST list the ADRs that apply" (ADR-009@v2 C8) and "Every plan MUST cite the constraints that apply" (ADR-009@v2 C13). | Add ADR-016 to "ADRs that apply" and cite `ADR-016@v1 C10`, with how the design complies. Rerun /speckit-plan's Constitution Check. |
| C1 | Coverage Gap | MEDIUM | spec.md:L9, L13 (User Story 1, scenario 1); tasks.md | The acceptance scenario says the repair loop receives each finding. The plan says "The repair loop reads the CSV", but no task covers the repair loop's side, or a test that it receives rule, file and line. | Add a task (and a test written first) for the repair loop consuming the findings, or state in the spec that the repair-loop side is out of scope and only the file contract is delivered. |
| C2 | Coverage Gap | MEDIUM | tasks.md:L5 (T003) | Only FR-001 has a test task written first (T001). FR-002, the output format, has no test task before T003. The project requires behaviour to be tested, with expected results written first (ADR-012). | Add a failing test for the report format (SARIF schema and version fields, one result per violation) before T003. |
| B1 | Ambiguity | MEDIUM | spec.md:L17 (FR-001), plan.md:L17 | "the analyzers it runs" is not defined: which analyzers, how they are configured, and in what output format they report. The converter in the plan depends on this. | Name the analyzers (or the rule for choosing them) and their native output format in the spec or plan. |
| B2 | Ambiguity | LOW | tasks.md:L6 (T004) | "Confirm every violation appears" does not say how: a test, a count comparison, or a manual check. | Reword as a test: for a fixture with N known violations, the report holds exactly N results. |
| F1 | Inconsistency | LOW | spec.md:L13 vs spec.md:L18 | The acceptance scenario lists rule, file and line; FR-002 adds message. Minor drift in the fields the repair loop gets. | Align the scenario and the requirement on the same field list. |
| E1 | Edge Case | LOW | spec.md (no Edge Cases section) | No edge cases: no violations, analyzer failure or crash, violations with no line number, duplicate findings across analyzers. | Add an Edge Cases section covering at least zero findings and analyzer failure. |

CLAUDE.md hard rule 4 (copy clause): no sentence in the artefacts describes copying subject-system files. No finding.

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 collect-analyzer-violations | Yes | T001, T002 | Test written first. Analyzers undefined (B1). |
| FR-002 write-violations-report | Yes | T003 | Format conflicts with ADR-016@v1 C10 (D1). No test written first (C2). |
| SC-001 every-violation-reported | Yes | T004 | Verification method vague (B2). Format conflict (D1). |
| US1 repair-loop-receives-findings | Partial | none directly | Repair-loop side not covered (C1). |

## Constitution Alignment Issues

- D1: ADR-016@v1 C10 (SARIF for violation reports) is not honoured; CSV is named and SARIF is not. Principle II.
- D2: The plan omits ADR-016 from its applicable ADRs and constraint citations (ADR-009@v2 C8, C13). Principle II.

## Unmapped Tasks

None. Every task references an FR or SC.

## Metrics

- Total Requirements: 3 (FR-001, FR-002, SC-001), plus 1 user story
- Total Tasks: 4
- Coverage: 100% of FR/SC have at least one task (3 of 3); the user story's repair-loop side is uncovered
- Ambiguity Count: 2
- Duplication Count: 0
- Critical Issues Count: 2

## Next Actions

CRITICAL issues exist. Resolve them before `/speckit-implement`.

1. Run `/speckit-specify` with refinement to change FR-002 and SC-001 from `findings.csv` to a SARIF report (D1).
2. Run `/speckit-plan` to update the design to SARIF and to list ADR-016 and cite `ADR-016@v1 C10` in the Constitution Check (D1, D2).
3. Run `/speckit-tasks`, or edit tasks.md by hand, to add a failing format test before T003, a repair-loop task or an explicit scope note, and a concrete T004 (C1, C2, B2).
4. Optionally add edge cases and name the analyzers (E1, B1).

Would you like me to suggest concrete remediation edits for the top 4 issues? (None will be applied automatically.)

## Files opened

- C:\Users\adoug\Architect-in-the-loop\.claude\skills\speckit-analyze (skill loaded through the Skill tool)
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\spec.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\plan.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-findings\tasks.md
- C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-findings.md
- C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md
- Also run (not read): .specify/scripts/python/check_prerequisites.py; checked for .specify/extensions.yml (absent)
