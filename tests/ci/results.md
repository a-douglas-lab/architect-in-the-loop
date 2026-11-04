# Results: CI

Expected results are in [expected.md](expected.md), committed before any code (`9b3575d`).

## T. Trailer check, local (Windows 11, Python 3.13.5)

Command: `python -I tests/ci/test_trailers.py`.

**Run 1:** 7 of 8 matched. T6 failed, which was a harness fault, not a script fault. The test passed the original branch point as `base`, so after the merge the main-side commit, which has no trailer, fell inside the range. CI passes the pull request's base commit, the tip of `main`, which excludes it. Fix: the test passes `main` as the base.

**Run 2, after the fix:** 8 of 8 matched.

## S. Existing suites, local (Windows) before CI

- `tests/controls/test_hooks.py`, after `check_edited.py` gained its `pwsh` fallback: 25 of 25 on Windows. The Ubuntu run is in CI (below).
- Spike, `pytest -q` in a fresh venv from `requirements.txt`: 65 passed, 2 skipped, 4 xfailed, in 14 seconds.

## C. CI and bypass cases

Not run yet: each needs a push, which needs Andy's approval first (ADR-013@v1 C5).
