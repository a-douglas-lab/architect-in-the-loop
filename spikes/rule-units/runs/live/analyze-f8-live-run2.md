## Specification Analysis Report

**Feature:** Analyzer Findings for the Repair Loop. The prerequisite script found this feature in a scratchpad directory, `…\scratchpad\live\x02`, not under `specs/`. It may be a fixture for the rule-unit spike rather than a real feature. Please confirm it's the one you meant.

No `.specify/extensions.yml` exists, so no hooks ran before or after the analysis.

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | Constitution / ADR | CRITICAL | spec.md:18, spec.md:22, plan.md:5, plan.md:17, tasks.md:5-6 | ADR-016@v1 C10 says: "Tools that report rule violations MUST report in SARIF." The feature reports rule violations as `findings.csv` and never mentions SARIF. The rule-unit server's deterministic check flagged the same thing. | Replace the CSV output with a SARIF file, for example `findings.sarif`. Rule, file and line map to `ruleId` and `locations[].physicalLocation`; message maps to `message.text`. Update FR-002, SC-001, the plan's Design section, T003 and T004. |
| D2 | Constitution | CRITICAL | plan.md:9-11 | Principle II says every plan MUST list the ADRs that apply and cite their constraints (ADR-009@v2 C8, C13). The plan lists only ADR-001. It leaves out ADR-016, whose scope covers the capability and which governs this exact behaviour. | Add ADR-016 and cite `ADR-016@v1 C10` in the Constitution Check. |
| C1 | Coverage | MEDIUM | spec.md:13, tasks.md | The acceptance scenario says "the repair loop receives each finding". No task covers the repair loop reading the output. Only the write side is covered. | Add a task that checks the repair loop can consume the output, or state that the reading side is out of scope. |
| C2 | Underspecification | MEDIUM | spec.md:17, plan.md:17 | "The analyzers it runs" is never defined: which analyzers, and in what output format. The plan's `FindingsCollector` "runs the analyzers" but names none. | Name the analyzers, or the contract they must meet, for example SARIF-emitting .NET analyzers. If they already emit SARIF, D1 becomes mostly a pass-through. |
| U1 | Underspecification | LOW | spec.md | There are no edge cases: zero findings, an analyzer that fails, findings with no line number. | Add an Edge Cases section. |
| I1 | Consistency | LOW | tasks.md:3-6 | Only FR-001 has a test-first task (T001). T003 has no failing test written before it, so ADR-012's "expected results first" is only partly followed. | Add a failing-test task before T003. |

**Coverage Summary**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 collect-violations | Yes | T001, T002 | |
| FR-002 write-violations-file | Yes | T003 | Format conflicts with ADR-016 C10 (D1) |
| SC-001 every-violation-recorded | Yes | T004 | Inherits D1 |

**Constitution alignment issues:** D1 and D2. The rule-unit server also selected ADR-011@v1 C3 and hard rule 4's copy clause. Neither is triggered: the feature doesn't write to acceptance test paths and doesn't copy eShop files. ADR-001@v2 C1 is cited at its current version.

**Unmapped tasks:** none.

**Metrics**
- Requirements: 3 (2 functional requirements, 1 success criterion)
- Tasks: 4
- Coverage: 100% (every requirement has at least one task)
- Ambiguities: 1 (C2)
- Duplications: 0
- Critical issues: 2

### Next actions

- Don't run `/speckit-implement` until D1 and D2 are fixed.
- Run `/speckit-specify` to change FR-002 and SC-001 to SARIF output.
- Run `/speckit-plan` to add ADR-016@v1 C10 to the Constitution Check and update the Design section.
- Run `/speckit-tasks` to regenerate T003 and T004, add a test-first task for the output, and decide whether the repair loop's reading side is in scope (C1).

Would you like me to suggest concrete edits for the top 4 issues (D1, D2, C1, C2)? I won't apply anything without your approval.
