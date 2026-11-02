# Specification Analysis Report: Impact Report Export

Feature folder: `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export`

Pre-execution hooks: `.specify/extensions.yml` does not exist, so no hooks were checked.

Prerequisites script output: `FEATURE_DIR` resolved to the folder above. `AVAILABLE_DOCS` was `["tasks.md"]`. `spec.md`, `plan.md` and `tasks.md` are all present. No research.md, data-model.md, contracts/ or quickstart.md exist.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| C1 | Coverage gap | MEDIUM | plan.md:L11, L13; tasks.md | The plan cites ADR-001@v2 C1 (export code holds no subject-domain terms) and ADR-003@v2 C3 (subject path not hard-coded), but no task implements or checks either. T003 covers C2 only. | Add a task that reads the contract location from configuration, and a task (or deterministic check) that the export code holds no subject-domain terms or subject path. |
| C2 | Underspecification | MEDIUM | spec.md:L17; plan.md:L5, L20 | FR-001 says "as a file" but gives no format (CSV, JSON, Markdown, PDF), file name, or content beyond domain names. A test for T001 cannot be written without it. | State the format and the report's fields in the spec. |
| C3 | Underspecification | MEDIUM | spec.md (no Edge Cases section) | No edge cases: outcome with no impact report; unknown outcome; subject contract missing or unreadable; a domain in the impact set that the contract does not name. | Add an Edge Cases section and an FR for each failure behaviour. |
| C4 | Underspecification | MEDIUM | plan.md:L20; spec.md | The plan reads "the stored impact report", but neither spec nor plan says where impact reports are stored or what the entity holds. No Key Entities section or data-model.md. | Add Key Entities (Impact report, Impact set, Subject contract) to the spec, and the storage source to the plan. |
| C5 | Underspecification | MEDIUM | tasks.md:L3-L6 | Tasks have no file paths, no phase grouping, no [P] markers and no story labels. T002 and T003 do not name the files they change. | Regenerate with /speckit-tasks against a fuller plan, so each task names its file. |
| C6 | Underspecification | MEDIUM | tasks.md:L5-L6 | Only FR-001 has a test-first task (T001). FR-002 has no failing test, and T004 "Confirm" does not say whether it is an automated test or a manual check. | Add a failing test for FR-002 (names come from the contract, e.g. by changing a contract fixture), and make T004 an automated test written before T002/T003. |
| C7 | Underspecification | MEDIUM | plan.md (no Technical Context or Project Structure) | The plan has Summary, Constitution Check and Design only. No language version, test framework, project path for the C# API, or route for the endpoint. | Fill in Technical Context and Project Structure with /speckit-plan. |
| C8 | Ambiguity | LOW | spec.md:L9, L13; plan.md:L5 | Access control is not stated: the story names the architecture coordinator, but nothing says who may call the endpoint. | Say whether the endpoint is restricted to the coordinator, or record that authorisation is out of scope. |
| I1 | Inconsistency | LOW | spec.md:L13, L22 | Terminology drift: "impacted domains" (story) and "impact set" (SC-001) for what seems the same thing. | Define "impact set" once and use it throughout. |
| R1 | Rule alignment | LOW | plan.md:L16 | Rule check for CLAUDE.md hard rule 4 (copy clause): no sentence in spec, plan or tasks describes copying subject-system files. No finding under the rule's check. The plan says "Hard rules: none affected", yet the feature reads the subject contract, which lives in the fork. | Optional: state in the plan that the contract is read in place from the subject, not copied, to make compliance explicit. |

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 export-impact-report-as-file | Yes | T001, T002 | Format unspecified (C2) |
| FR-002 domain-names-from-subject-contract | Yes | T003 | No failing test (C6) |
| SC-001 report-lists-every-impact-set-domain | Yes | T004 | Unclear whether automated (C6) |
| Plan: ADR-001@v2 C1 no subject-domain terms | No | none | C1 |
| Plan: ADR-003@v2 C3 subject path not hard-coded | No | none | C1 |
| Plan: ADR-017@v1 C3 endpoint in C# REST API | Yes | T002 | |

## Constitution Alignment

- Principle II, "Every plan MUST list the ADRs that apply" (ADR-009@v2 C8): met. plan.md:L9 lists ADR-001, ADR-003 and ADR-017.
- Principle II, "Every plan MUST cite the constraints that apply, as `ADR-nnn@vN Cn`" (ADR-009@v2 C13): met in form. plan.md:L11-L14 use the required format. Whether these constraint IDs and versions exist, and whether other ADRs apply, was not verified: the ADR files were not opened.
- Hard Rules: "Every plan MUST comply". No conflict found. Hard rule 4 copy clause checked as above (R1).

No CRITICAL constitution conflicts.

## Unmapped Tasks

None. Every task cites an FR or SC.

## Metrics

- Total requirements: 3 (FR-001, FR-002, SC-001)
- Total tasks: 4
- Coverage: 100% (3 of 3 requirements have at least one task). Plan-cited constraints: 1 of 3 covered.
- Ambiguity count: 2 (C2, C8)
- Duplication count: 0
- Critical issues count: 0

## Next Actions

No CRITICAL issues. You may proceed to /speckit-implement, but the MEDIUM items will make the tests in T001 and T004 hard to write as things stand. Suggested order:

1. Run /speckit-clarify, or edit the spec, to settle the file format, edge cases and key entities (C2, C3, C4, C8, I1).
2. Run /speckit-plan to add Technical Context and Project Structure (C7), and the storage source (C4).
3. Run /speckit-tasks to regenerate tasks with file paths and test-first tasks for FR-002, SC-001, ADR-001@v2 C1 and ADR-003@v2 C3 (C1, C5, C6).

Would you like me to suggest concrete remediation edits for the top 5 issues? Nothing has been changed.

After-analysis hooks: `.specify/extensions.yml` does not exist, so none were checked.

## Files opened

- `C:\Users\adoug\Architect-in-the-loop\.claude\skills\speckit-analyze` (skill, loaded via the Skill tool)
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\spec.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\plan.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\tasks.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-export.md`
- `C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md`
- `C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\scripts\python\check_prerequisites.py` (run, not read)
- `.specify/extensions.yml` (existence checked; absent)
