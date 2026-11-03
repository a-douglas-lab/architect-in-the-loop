# Control tests

Behaviour tests for the deterministic controls in ADR-011: each one shown blocking a bad action and allowing a good one (backlog Q6, VL-3 and VL-4). Expected results are written and committed before each run (ADR-012@v2 C10), in [expected.md](expected.md). Results are in [results.md](results.md).

| Suite | Control | Run |
| --- | --- | --- |
| G | Private-material guard, `scripts/check-private-material.*` (ADR-011@v1 C7) | `powershell -File tests/controls/test-private-material.ps1` and `bash tests/controls/test-private-material.sh`. Add `-Old` / `--old` to run the guard as it was before Step 7 |
| H, K | Acceptance-test hook (C3) and check-after-edit hook (C1), in `.claude/hooks/` | `python -I tests/controls/test_hooks.py` |
| L | The controls in a real session: ask rules (C2), hooks, and the built-in read and write blocks (C4, C5) | `python -I tests/controls/run_live.py [case ...]`. Needs a signed-in `claude` CLI, v2.1.314 or later; uses the model, so it costs tokens |

The tests build throwaway trees in a fresh temporary folder. None touches this repository's tree, and none touches the private evaluation repository (hard rule 1).
