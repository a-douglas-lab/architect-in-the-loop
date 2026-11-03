# Results: deterministic controls

Expected results are in [expected.md](expected.md), committed before each run. How to run each suite is in [README.md](README.md).

## G. Private-material guard

Run 2026-11-03 on Windows 11, PowerShell 5.1 and Git Bash, after the expected results were committed (`f5a9ea1`).

| Case | Expected | PowerShell | Bash | Old guard (both shells) |
| --- | --- | --- | --- | --- |
| G1 | Clean | exit 0 | exit 0 | exit 0 |
| G2 | Caught | exit 1 | exit 1 | exit 0 |
| G3 | Caught | exit 1 | exit 1 | exit 0 |
| G4 | Caught | exit 1 | exit 1 | exit 0 |
| G5 | Caught | exit 1 | exit 1 | exit 0 |
| G6 | Caught | exit 1 | exit 1 | exit 1 |
| G7 | Caught | exit 1 | exit 1 | exit 0 |
| G8 | Caught | exit 1 | exit 1 | exit 0 |
| G9 | Caught | exit 1 | exit 1 | exit 0 |
| G10 | Clean | exit 0 | exit 0 | exit 0 |

All 10 cases matched expectation in both shells. The old guard caught only G6, as predicted.

On this worktree with eShop checked out (1,432 entries under `subject/`), each guard takes 0.7 seconds and reports `none found`. `scripts/bootstrap.ps1` ran end to end and called the new guard. It exited 2 only because Docker is missing, which it was before this change.

**Limit:** the guard matches names and git remote URLs. A copy of the evaluation material renamed and stripped of its git metadata isn't caught. The guard never opens other files, by design (hard rule 1).
