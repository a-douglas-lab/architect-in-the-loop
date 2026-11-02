# Expected results

Written 2026-11-01, before any run.

| Fixture | The plan | Expected from `analyze` | Tests |
| --- | --- | --- | --- |
| f1-compliant | Lists the ADRs that apply, and cites constraints | No CRITICAL | No false alarm on compliant work |
| f2-no-citations | Has no ADR list and no citations | CRITICAL for the citing rules | ADR-009@v2 C8, C13 |
| f3-custom-agent | Builds an in-house coding agent; cites only an unrelated ADR | CRITICAL for hard rule 6 | The hard-rule safety net |
| f4-copy-eshop | Copies eShop source into this repository; cites only an unrelated ADR | CRITICAL for hard rule 4 | The hard-rule safety net |
| f5-uncited-breach | Splits outcomes automatically without the checks ADR-015 requires; doesn't cite ADR-015 | No CRITICAL (a miss) | The admitted limit: a rule outside the constitution, uncited |
| f6-cited-breach | Cites ADR-015@v1 C2, then skips those checks | No CRITICAL (probably a miss) | Whether citing alone helps |
| f7-ordinary-work | Hand-built capability change, updating a unit test the change touches | No CRITICAL | False CRITICAL risk from hard rules 2 and 3 |

## Added 2026-11-02, before any run of these fixtures

Ruled by Andy after the first run: the earlier expectations stay as written, and results are reported as rates, not pass or fail.

| Fixture | The plan | Expected from `analyze` | Tests |
| --- | --- | --- | --- |
| f8-subtle-breach | Writes analyzer rule violations to a custom CSV file; cites only ADR-001. This breaks ADR-016@v1 C10 (SARIF), which nothing in ADR-016's title reveals | No CRITICAL naming the SARIF rule (a miss). A CRITICAL for omitted ADRs is possible | Whether a breach invisible from a title is caught |
| f9-misleading-title | Drives Claude Code through the Agent SDK, with custom prompts and tool settings; cites ADR-004@v2 C3 | No CRITICAL | Whether hard rule 6's or ADR-004's wording ("no custom coding agent") causes a false CRITICAL on compliant orchestration |

## Plan check

`plan-check`: expected to fill the Constitution Check with a list of ADRs that apply and `ADR-nnn@vN Cn` citations, opening ADRs through the constitution's index.
