# Specification Analysis Report: Impact Report Export

Feature directory: `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export`

Pre-execution: `.specify/extensions.yml` does not exist, so no `before_analyze` hooks were checked.

Prerequisites script output: `FEATURE_DIR` resolved to the folder above; `AVAILABLE_DOCS` listed `tasks.md` only. `spec.md` and `plan.md` are both present in the folder (the script lists only optional docs beyond the plan), so all three core artefacts were analysed.

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| B1 | Ambiguity | MEDIUM | spec.md:L9, L13, L17; plan.md:L5 | "as a file" never says which format (CSV, JSON, Markdown, PDF) or what the file contains beyond the domain list. FR-001 is not testable as written. | Name the format and the minimum content (outcome id, domains) in FR-001. |
| C1 | Underspecification | MEDIUM | plan.md:L20; spec.md | The plan reads "the stored impact report", but the spec never says where impact reports are stored or what happens when an outcome has none. | Add an edge case to the spec ("outcome with no impact report") and name the source of the stored report in the plan. |
| C2 | Underspecification | MEDIUM | plan.md:L13, L20; tasks.md:L5 | ADR-003@v2 C3 (subject path not hard-coded) is cited, and the design resolves the contract "at its given location", but nothing says how the location is given (configuration, request parameter, environment). No task covers it. | State the mechanism in the plan; add a task to read the contract location from configuration, and a test that fails if the path is hard-coded. |
| C3 | Underspecification | MEDIUM | spec.md | No Edge Cases section: missing report, unknown outcome, contract unreadable, domain in report absent from contract. | Add edge cases and matching acceptance scenarios. |
| E1 | Coverage Gap | MEDIUM | plan.md:L11; tasks.md | ADR-001@v2 C1 (export code holds no subject-domain terms) is cited in the Constitution Check but has no task or deterministic check enforcing it. | Add a task for a check (test or lint) that the export code contains no subject-domain terms. |
| E2 | Coverage Gap | MEDIUM | tasks.md:L3-L5 | Only FR-001 has a test-first task (T001). FR-002 (names from the subject contract) has an implementation task (T003) but no failing test written before it. | Add a failing test for FR-002 before T003, e.g. a test using a stub contract with names that differ from any in code. |
| E3 | Coverage Gap | MEDIUM | spec.md:L9; plan.md:L14; tasks.md | The user story is the coordinator downloading the report, and ADR-017 (cited) has the coordinator working through a React web interface over the C# REST API. Tasks cover only the API endpoint; there is no task for how the coordinator triggers the download. | Either add a UI task, or state in the spec that this feature is API-only and the UI is out of scope. |
| E4 | Coverage Gap | LOW | tasks.md:L6 | T004 "Confirm the export lists every domain" does not say how (automated test or manual check). SC-001 is a measurable criterion that should be an automated test. | Reword T004 as an automated test, with the fixture it uses. |
| F1 | Inconsistency | LOW | tasks.md | Tasks have no phase grouping, no [P] markers, and no file paths (e.g. where `ExportController` and its tests live). | Add phases and file paths so tasks are executable without inference. |
| F2 | Inconsistency | LOW | spec.md:L9; plan.md:L5 | Terminology varies between "download" (story) and "export" (requirement, plan, tasks). Minor. | Use "export" throughout, or define download as the coordinator-facing action. |
| A1 | Duplication | LOW | spec.md:L13, L18 | The acceptance scenario restates FR-002 ("read from the subject contract"). Harmless but redundant. | Keep FR-002 as the requirement; let the scenario reference it. |
| C4 | Underspecification | LOW | spec.md | No access control is stated: who may export, and whether the report may contain anything sensitive. | Add a line on who may export, or state that the existing API's authorisation applies. |

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 export-impact-report-as-file | Yes | T001, T002 | Format unspecified (B1) |
| FR-002 domain-names-from-subject-contract | Yes | T003 | No test-first task (E2); location mechanism unspecified (C2) |
| SC-001 export-lists-every-impacted-domain | Yes | T004 | Verification method unclear (E4) |

## Constitution Alignment

No constitution MUST violated.

- Principle II, ADR-009@v2 C8: the plan lists applicable ADRs (ADR-001, ADR-003, ADR-017). Satisfied.
- Principle II, ADR-009@v2 C13: the plan cites constraints in `ADR-nnn@vN Cn` form. Satisfied.
- Hard Rules (ADR-009@v2 C17): the plan states "none affected". Nothing in spec, plan or tasks touches the evaluation repository, eShop code, acceptance tests, or the non-goals. Satisfied.
- Cited constraints that lack enforcing tasks are reported as coverage gaps (E1, C2), not violations: the plan itself honours them.

## Rules Applied (rules-export.md)

| Rule | Kind | Result | Evidence |
|------|------|--------|----------|
| CLAUDE.md hard rule 4, copy clause: "never copy eShop files into this repo" | bright-line | No finding | No sentence in spec.md, plan.md or tasks.md describes copying subject-system files. The only subject-related actions are reading the subject contract and resolving names through it (spec.md:L13, L18; plan.md:L12, L20; tasks.md:L5), which are reads, not copies. Implement-stage check (byte-identical files outside `subject/`) is not applicable at analyse stage. |

## Unmapped Tasks

None. Every task references a requirement or success criterion.

## Metrics

- Total requirements: 3 (FR-001, FR-002, SC-001)
- Total tasks: 4
- Coverage: 100% (3 of 3 requirements have at least one task)
- Ambiguity count: 1
- Duplication count: 1
- Critical issues count: 0

## Next Actions

No CRITICAL issues. You may proceed to `/speckit-implement`, but the MEDIUM findings are worth closing first because they affect testability:

- Refine the spec (`/speckit-specify` or `/speckit-clarify`): file format (B1), edge cases (C1, C3), UI scope (E3).
- Adjust the plan (`/speckit-plan`): how the subject contract location is supplied (C2).
- Edit tasks.md manually or rerun `/speckit-tasks`: add a failing test for FR-002 (E2), a subject-terms check for ADR-001@v2 C1 (E1), reword T004 as an automated test (E4), and add phases and paths (F1).

Would you like me to suggest concrete remediation edits for the top 5 issues? (No edits will be applied automatically.)

After reporting: `.specify/extensions.yml` does not exist, so no `after_analyze` hooks were checked.

## Files opened

- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\spec.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\plan.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\feature-export\tasks.md`
- `C:\Users\adoug\AppData\Local\Temp\claude\C--Users-adoug-Architect-in-the-loop--claude-worktrees-spike-rule-units-0fd90a\8e9b8dfe-d2c0-4c7f-b8af-9fc1549bdf40\scratchpad\analyze\rules-export.md`
- `C:\Users\adoug\Architect-in-the-loop\.claude\worktrees\spike-rule-units-0fd90a\.specify\memory\constitution.md`

Also used, not opened with a read: the speckit-analyze skill (loaded through the Skill tool); `.specify/scripts/python/check_prerequisites.py` (run, not read); a directory listing of the `analyze` and `feature-export` folders; an existence check for `.specify/extensions.yml` (absent). CLAUDE.md was supplied in the session context automatically.
