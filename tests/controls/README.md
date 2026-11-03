# Control tests

Behaviour tests for the deterministic controls in ADR-011: each one shown blocking a bad action and allowing a good one (backlog Q6, VL-3 and VL-4). Expected results are written and committed before each run (ADR-012@v2 C10), in [expected.md](expected.md). Results are in [results.md](results.md).

| Suite | Control | Run |
| --- | --- | --- |
| G | Private-material guard, `scripts/check-private-material.*` (ADR-011@v1 C7) | `powershell -File tests/controls/test-private-material.ps1` and `bash tests/controls/test-private-material.sh`. Add `-Old` / `--old` to run the guard as it was before Step 7 |

The tests build throwaway trees in a fresh temporary folder. None touches this repository's tree, and none touches the private evaluation repository (hard rule 1).
