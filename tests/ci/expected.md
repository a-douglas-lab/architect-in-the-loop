# Expected results: CI

Written 2026-11-04, before any code, under ADR-012@v2 C10. Never edited after a run: a wrong expectation gets a new dated expectation beside it. Results go in [results.md](results.md).

Andy's choices of 4 Nov: GitHub Actions on Ubuntu and Windows; the trailer check covers commits on `claude/*` branches; one aggregate required job named `checks`.

## T. Trailer check (ADR-010@v1 C5)

`scripts/check-trailers.py <base> <head> <branch>` reads every commit in `base..head`. On a branch whose name starts with `claude/`, each commit that isn't a merge commit must carry a trailer whose key is `Co-Authored-By`, in any case, and whose value names Claude. Merge commits are skipped: they carry no authored content, and the app's merge from `main` makes one. Each case builds a throwaway git repository in a temporary folder.

"Pass" means exit 0. "Fail" means exit 1, and the offending commit's short SHA and subject are printed.

| Case | Branch | Commits in range | Expected |
| --- | --- | --- | --- |
| T1 | `claude/x` | Two commits, both with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` | Pass |
| T2 | `claude/x` | Two commits, the second without a trailer | Fail, naming the second |
| T3 | `andy/x` | One commit without a trailer | Pass: the branch isn't checked |
| T4 | `claude/x` | One commit with `co-authored-by: Claude Sonnet 5.5 <noreply@anthropic.com>`, lower case | Pass |
| T5 | `claude/x` | One commit whose only trailer is `Co-Authored-By: Jane Doe <jane@example.com>` | Fail |
| T6 | `claude/x` | One commit with a trailer, then a merge commit without one | Pass |
| T7 | `claude/x` | "Claude" appears in the body but not in a trailer | Fail |
| T8 | `claude/x` | No commits in range | Pass |

## S. Existing suites on Ubuntu

The suites in `tests/controls/` were written and run on Windows. On Ubuntu:

| Suite | Expected |
| --- | --- |
| G, bash (`test-private-material.sh`) | 10 of 10 |
| G, PowerShell | Not run on Ubuntu: the test calls Windows PowerShell 5.1 (`powershell`) by design |
| H | 15 of 15. H8 expects "None" there, because the file system is case-sensitive (the test already encodes this) |
| K | 10 of 10, once `check_edited.py` falls back to `pwsh` when `powershell` isn't installed. Without that fix, K7 and K8 fail on Ubuntu |
| Spike (`spikes/rule-units`, `pytest -q`) | Every test passes, on both systems, with no network access |

## C. CI and bypass cases (backlog Q6, VL-6 and VL-7)

Each case is a pull request from a `claude/ci-test-*` branch. Pushing them needs Andy's approval first (ADR-013@v1 C5). Each test pull request is closed without merging, and its branch is deleted after the run.

| Case | The pull request's change | Expected `checks` result |
| --- | --- | --- |
| C1 | This branch: the workflow itself | Green on both systems |
| C2 | A script commits an empty placeholder file in a folder named `Architect-in-the-loop-evaluator`, using `git add -f` past `.gitignore` | Red: the guard step fails on both systems |
| C3 | A commit without the trailer | Red: the trailer job fails |
| C4 | A script changes `acceptance-tests.json` so H1 no longer matches, with no hook in the way | Red: the hook tests fail on both systems |
| C5 | After Andy adds the ruleset requiring a pull request and `checks`: C2's pull request is shown as blocked from merging | Blocked (`mergeStateStatus` is `BLOCKED`) |

C2 and C4 are VL-7's "change written by a script that a hook can't see". VL-7's `--no-verify` case doesn't apply: this repository has no pre-commit hook, so `--no-verify` skips nothing. VL-8's "a direct push to `main` is refused" is Andy's to run or approve, after the ruleset.
