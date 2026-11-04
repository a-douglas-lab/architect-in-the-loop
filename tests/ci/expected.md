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

## Dated expectations, 2026-11-04, after review run 1 and Andy's rulings

Andy's rulings: "C1 check + guard; C3 reported"; "Skip merge commits"; "Drop the C3 test PR" and "Protect .github/". The expectations above stay as written. Where one is replaced, the new one is stated here.

### D. Checks on the pull request's changed files (new)

`scripts/check-changed.py <base> <head>` runs the C1 hook's own check (`check()` in `.claude/hooks/check_edited.py`, one definition, VL-1) on every file added or changed in `base..head` that still exists. It fails if any check fails. It lists changed files matching the C3 globs in `.claude/hooks/acceptance-tests.json`, and doesn't fail on them: CI can't tell implement from the stage that writes tests. Each case builds a throwaway git repository holding a copy of the hooks.

| Case | Change in range | Expected |
| --- | --- | --- |
| D1 | A valid `.json` and a valid `.py` | Pass |
| D2 | An invalid `.json` | Fail, naming the file |
| D3 | A new file under `tests/acceptance/` | Pass, and the path is listed as an acceptance-test change |
| D4 | A deleted `.json` | Pass |
| D5 | A `.md` file | Pass |

### T. Trailer check, replaced and added

- **Merge commits stay skipped,** now by Andy's ruling, not the author's default.
- **T9 (new):** a commit whose only trailer is `Co-Authored-By: Claudette Smith <c@example.com>` gives **Fail**. The value must name Claude as a word.
- **The range (replaces "every commit in `base..head`" in CI):** CI passes `origin/<base branch>` as the base, not the pull request's recorded base commit. That excludes everything already on `main` at the time of the run, even when the recorded base is stale.
- **T2:** the failure output names the commit's short SHA as well as its subject. The harness now checks both.

### K. Check-after-edit hook (addition to tests/controls/expected.md section K)

- **K11 (new):** a `.ps1` file, with neither `powershell` nor `pwsh` on PATH: **Reported**, with "no PowerShell found".

### P. `.github/` is a protected path (addition to tests/controls/expected.md section L)

- **P1 (new):** with `Edit(/.github/**)` in the ask rules, `claude -p` in `bypassPermissions` mode writing `.github/workflows/x.yml` in a throwaway repository: **Refused**, by the ask rule, with the message "Claude requested permissions to write to …".

### S. Clarified

"Every test passes" means no test fails: skips and expected failures are allowed. "No network access" means no model or API calls; `pip install` needs the network.

H8 gives "None" on Ubuntu because `os.path.normcase` doesn't fold case on POSIX, not because the hook asks the file system.

### C. Replaced

- **C3 is dropped** (Andy, 4 Nov). It would publish a commit that breaks ADR-010@v1 C5. T2 covers the script, and C1 covers the job in CI.
- **C5 runs on C2's pull request before it is closed;** C2 is closed and its branch deleted after C5.
- **Out of scope here:** the fork's ruleset (VL-8 covers both repositories; Andy adds both) and VL-7's `--no-verify` case, which skips nothing while no pre-commit hook exists. ADR-013@v1 C6 ("changes MUST reach `main` only through a pull request that Andy merges") becomes enforced by the ruleset Andy adds, not by this workflow.
