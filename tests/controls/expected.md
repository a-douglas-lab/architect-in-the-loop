# Expected results: deterministic controls

Written before any run, under ADR-012@v2 C10. Never edited after a run: a wrong expectation gets a new dated expectation beside it. Results go in [results.md](results.md).

## G. Private-material guard (Step 7, item 6; ADR-011@v1 C7)

Written 2026-11-03. The guard is `scripts/check-private-material.ps1` and `.sh`, which both bootstrap scripts call. Each case builds a throwaway tree in a fresh temporary folder, runs the guard against it, and checks the exit code. No case touches this repository's tree or the evaluation repository: the placeholders are empty folders and files, and the URLs are text that nothing fetches.

"Caught" means exit code 1 and the offending path printed. "Clean" means exit code 0 and `none found`.

| Case | Tree | New guard | Old guard (`main` at `2732f29`) |
| --- | --- | --- | --- |
| G1 | No private material | Clean | Clean |
| G2 | Folder `Architect-in-the-loop-evaluator/` at the root | Caught | Clean: the gap |
| G3 | Folder `docs/x/architect-in-the-loop-EVALUATOR/`, other case, nested | Caught | Clean: the gap |
| G4 | Folder `subject/Architect-in-the-loop-evaluator/` | Caught | Clean: the gap |
| G5 | Folder `subject/private-eval/` | Caught | Clean: `subject/` was skipped |
| G6 | Folder `private-eval/` at the root | Caught | Caught |
| G7 | File `Architect-in-the-loop-evaluator.zip` | Caught | Clean: the gap |
| G8 | A clone under another name: `scratch/.git/config` whose remote URL names `Architect-in-the-loop-evaluator` | Caught | Clean: the gap |
| G9 | `.gitmodules` with a submodule URL naming `Architect-in-the-loop-evaluator` | Caught | Clean: the gap |
| G10 | Near misses that must not alarm: `evaluator/`, `Architect-in-the-loop/`, `grader-evaluation/`, `.git/config` with an unrelated URL | Clean | Clean |

Both implementations (PowerShell 5.1 and Git Bash) give the same result on every case. The old-guard column is run once, to show the gap the fix closes.
