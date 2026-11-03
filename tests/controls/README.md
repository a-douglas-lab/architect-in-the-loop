# Control tests

Behaviour tests for the deterministic controls in ADR-011: each one shown blocking a bad action and allowing a good one (backlog Q6, VL-3 and VL-4). Expected results are written and committed before each run (ADR-012@v2 C10), in [expected.md](expected.md). Results are in [results.md](results.md).

| Suite | Control | Run |
| --- | --- | --- |
| G | Private-material guard, `scripts/check-private-material.*` (ADR-011@v1 C7) | `powershell -File tests/controls/test-private-material.ps1` and `bash tests/controls/test-private-material.sh`. Add `-Old` / `--old` to run the guard as it was before Step 7 |
| H, K | Acceptance-test hook (C3) and check-after-edit hook (C1), in `.claude/hooks/` | `python -I tests/controls/test_hooks.py` |
| L | The controls in a real session: ask rules (C2), hooks, and the built-in read and write blocks (C4, C5) | `python -I tests/controls/run_live.py [case ...]`. Needs a signed-in `claude` CLI, v2.1.314 or later; uses the model, so it costs tokens |
| R, U | The read block and housekeeping reads (C4, VL-4); U takes the block from user settings only | `python -I tests/controls/run_live.py R1 … R8` or `U1 U3 U4 U7`. Same needs as L |

G, H, K and L build throwaway trees in a fresh temporary folder. R and U run in this worktree, under its own settings and hooks, and only read: memory, a skill, a saved tool output, a file in the session's scratchpad, an ADR, and a file in a temporary folder. No suite touches the private evaluation repository (hard rule 1).
