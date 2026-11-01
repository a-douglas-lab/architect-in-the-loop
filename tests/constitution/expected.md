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

`plan-check`: expected to fill the Constitution Check with a list of ADRs that apply and `ADR-nnn@vN Cn` citations, opening ADRs through the constitution's index.
