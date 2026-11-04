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

### C1, first run on GitHub (PR #16, run 41865805616, 4 Nov)

Pushed with Andy's approval ("saved, push and open the PR"). The run started at 16:17 UTC, during a GitHub Actions partial outage ("Incident with Actions and Pages", githubstatus.com).

All four jobs passed. C1 matches its expectation: green on both systems.

- `suites (windows-latest)`: passed, 1m24s.
- `suites (ubuntu-latest)`: passed, 29s. This is the first Ubuntu run of every suite (S), and all matched: guard 10 of 10 (bash), hooks 0 failures (H8 "None", K7 and K8 through `pwsh`), trailer and changed-files tests 0 failures, spike "65 passed, 2 skipped, 4 xfailed".
- `pull request`: passed, 6s: "every commit carries the trailer"; "15 changed files checked, 0 failed".
- `checks`: passed at 16:19, in 3s, with `results: success success`.

**A misdiagnosis, corrected.** For several minutes GitHub's jobs API and `gh pr checks` reported `suites (ubuntu-latest)` and `pull request` as queued, with no runner, after `checks` had passed. The author read this as `checks` passing without its inputs, and told Andy so. The job logs show both jobs ran at 16:18, before `checks` started: the status display was lagging during the outage, and `checks` received real results. On that wrong reading, Andy ruled "require the leaf checks too". The ruleset now requires all four checks (set by the author through the API at Andy's instruction, then read back). While the lagging status still showed `pull request` as queued, PR #16 showed `BLOCKED`, then `CLEAN` once all four reported. Told of the correction, Andy ruled "Back to `checks` only". The leaf checks were removed through the API and the ruleset read back: it requires `checks` alone, from GitHub Actions.

### C2 and C5 (PR #17, 4 Nov)

Pushed with Andy's approval ("Push the C2 test branch"). The branch was `claude/step7-ci` plus one commit adding an empty `Architect-in-the-loop-evaluator/.keep`, force-added past `.gitignore`.

| Case | Expected | Result | Match |
| --- | --- | --- | --- |
| C2 | Red: the guard step fails on both systems | `suites (ubuntu-latest)` and `suites (windows-latest)` failed at "Private-material guard on this tree", each logging "found private evaluation material in this working tree" with the placeholder's path; `checks` failed; `pull request` passed, which is correct because it doesn't run the guard | Yes |
| C5 | Blocked (`mergeStateStatus` is `BLOCKED`) | `BLOCKED` (`mergeable` was `MERGEABLE`, meaning no conflicts). In the web page this shows as a greyed-out merge button, with no separate "blocked" banner | Yes |

The PR was closed without merging, and `gh pr close --delete-branch` deleted the branch locally and on GitHub. This is VL-7's "a change written by a script that a hook can't see … caught at CI", for the guard's rule, and VL-6's "a deliberately failing pull request can't merge".

### V. Direct push to `main` (VL-8, 4 Nov)

Run after the expectation was committed (`9ba4297`), with Andy's approval ("Yes, test with a no-op push"). An empty commit carrying the trailer, pushed from a throwaway branch at `origin/main` with `git push origin HEAD:main`.

| Expected | Result | Match |
| --- | --- | --- |
| Refused, citing the repository rule; `main` unchanged | Refused: "GH013: Repository rule violations found for refs/heads/main", listing "Changes must be made through a pull request" and "Required status check "checks" is expected". `main` was `a239768` before and after. The probe branch was deleted locally; it never reached GitHub | Yes |

Not tested: a direct push to the fork's `main`. Its ruleset requires a pull request (read through the API), but no push was tried there.

C2 and C5 have not run: each needs a push with Andy's approval, and they wait until Actions is healthy.
