# Results: CI

Expected results are in [expected.md](expected.md), committed before any code (`9b3575d`), with dated expectations added after review run 1 (`cd85508`).

## T. Trailer check, local (Windows 11, Python 3.13.5)

Command: `python -I tests/ci/test_trailers.py`.

**Run 1:** 7 of 8 matched. T6 failed, which was a harness fault, not a script fault. The test passed the original branch point as `base`, so after the merge the main-side commit, which has no trailer, fell inside the range. CI passes the tip of `main`, which excludes it. Fix: the test passes `main` as the base.

**Run 2, after the fix:** 8 of 8 matched.

## S. Existing suites, local (Windows) before CI

- `tests/controls/test_hooks.py`, after `check_edited.py` gained its `pwsh` fallback: 25 of 25 on Windows. The Ubuntu run is in CI, not yet run.
- Spike, `pytest -q` in a fresh venv from `requirements.txt`: 65 passed, 2 skipped, 4 xfailed, in 14 seconds.

## After review run 1 and Andy's rulings (4 Nov), local (Windows)

Run after the dated expectations were committed (`cd85508`).

| Suite | Expected | Result |
| --- | --- | --- |
| T1 to T9, with the SHA checked in T2 | As expected.md | 9 of 9 |
| D1 to D5 | As expected.md | 5 of 5 |
| K11, no PowerShell on PATH | Reported | Reported. `test_hooks.py`: 26 of 26 |
| P1, `.github/` ask rule, `claude -p` v2.1.317, `bypassPermissions` | Refused | Refused: "Claude requested permissions to write to …\.github\workflows\x.yml, but you haven't granted it yet" |

P1's refusal comes from the new ask rule. `.github/` isn't one of Claude Code's built-in protected paths, and those are allowed in bypass mode anyway.

This branch checked itself: `check-changed.py origin/main HEAD` checked 7 changed files with 0 failures, and `check-trailers.py` found every commit carrying the trailer.

## C. CI and bypass cases

Not run yet: each needs a push, which needs Andy's approval first (ADR-013@v1 C5).
