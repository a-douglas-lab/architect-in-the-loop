# CI tests

Behaviour tests for the CI workflow, [`.github/workflows/checks.yml`](../../.github/workflows/checks.yml), and the trailer check it runs (backlog Q6, VL-6 to VL-8; ADR-010@v1 C5). Expected results are written and committed before each run (ADR-012@v2 C10), in [expected.md](expected.md). Results are in [results.md](results.md).

| Suite | What | Run |
| --- | --- | --- |
| T | `scripts/check-trailers.py` | `python -I tests/ci/test_trailers.py` |
| D | `scripts/check-changed.py`: the C1 check on a pull request's changed files, and acceptance-test changes reported | `python -I tests/ci/test_changed.py` |
| S | The `tests/controls/` suites and the spike's tests on Ubuntu | In CI |
| C | Pull requests that must turn `checks` red, and the ruleset blocking them | By hand, with Andy's approval for each push |

The workflow runs, on Ubuntu and Windows: the private-material guard on the tree, its tests, the hook tests, the trailer-check and changed-files tests, and the rule-unit spike's tests. On pull requests it also runs, on Ubuntu, the trailer check and the changed-files check. The job named `checks` fails if any of them fails. It is the one check Andy is to require in the ruleset; until he adds the ruleset, nothing blocks a merge.
