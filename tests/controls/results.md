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

**Limit (G):** the guard matches names and git remote URLs. A copy of the evaluation material renamed and stripped of its git metadata isn't caught. The guard never opens other files, by design (hard rule 1).

## H and K. Hook unit cases

Run 2026-11-03 with Python 3.13.5 on Windows 11, after the expected results were committed (`e678923`). Command: `python -I tests/controls/test_hooks.py`.

**Run 1:** 23 of 25 matched. K5 and K6 failed: `check_edited.py` exited 1 on `.sh` files instead of checking them. Root cause: only Git's `cmd` folder is on PATH, so the hook found no `bash`. Fix: the hook looks for Git Bash beside `git`, and reports "no bash found" rather than crashing when there is none.

**Run 2, after the fix:** 25 of 25 matched.

| Case | Expected | Run 1 | Run 2 |
| --- | --- | --- | --- |
| H1 to H3 | Deny | deny | deny |
| H4, H5 | Ask | ask | ask |
| H6 | None | none | none |
| H7 to H10 | Deny | deny | deny |
| H11, H12 | Blocked | blocked | blocked |
| H13 | None | none | none |
| H14, H15 | Deny | deny | deny |
| K1, K3, K7, K9, K10 | Silent | silent | silent |
| K2, K4, K8 | Reported | reported | reported |
| K5 | Silent | exit 1 | silent |
| K6 | Reported | exit 1 | reported |

Not run: H8 on a case-sensitive file system, where the expectation is "None"; and symlinks (see expected.md).
