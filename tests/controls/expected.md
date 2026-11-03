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

## H. Acceptance-test hook, unit cases (ADR-011@v1 C3)

Written 2026-11-03, after Andy's choice the same day: "Policy globs + stage marker". The hook is `.claude/hooks/acceptance_tests.py`, a `PreToolUse` hook on Edit, Write, NotebookEdit and MultiEdit. It reads globs from `.claude/hooks/acceptance-tests.json` and the stage from the marker `.specify/stage`. Each case copies the hook and its policy into a throwaway root, pipes one hook input on stdin, and reads the decision.

"Deny" and "ask" mean exit 0 with that `permissionDecision` in the JSON output. "None" means exit 0 and no output, so the call goes on through the normal permission flow. "Blocked" means exit 2.

Placeholder globs until DEV-1 fixes the fork's layout: `**/tests/acceptance/**` and `**/*.AcceptanceTests/**`.

| Case | Input | Stage marker | Expected |
| --- | --- | --- | --- |
| H1 | Write `tests/acceptance/OrderTests.cs` | `implement` | Deny |
| H2 | Edit, same path | `implement` | Deny |
| H3 | NotebookEdit, `notebook_path` `tests/acceptance/n.ipynb` | `implement` | Deny |
| H4 | Write, same path as H1 | absent | Ask |
| H5 | Write, same path as H1 | `specify` | Ask |
| H6 | Write `src/Ordering/Order.cs` | `implement` | None |
| H7 | Write, absolute Windows path with backslashes, `<root>\subject\eshop\tests\Ordering.AcceptanceTests\X.cs` | `implement` | Deny |
| H8 | Write `Tests/Acceptance/x.cs`, other case | `implement` | Deny on Windows (case-insensitive file system) |
| H9 | Write `src/../tests/acceptance/x.cs` | `implement` | Deny |
| H10 | Write `acceptance/x.cs` with `cwd` set to `<root>/tests` | `implement` | Deny |
| H11 | Not valid JSON on stdin | `implement` | Blocked |
| H12 | Write as H1, policy file missing | `implement` | Blocked |
| H13 | Write to a path outside the root | `implement` | None: outside the root is C5's job |
| H14 | Write as H1, marker reads `Implement` plus a newline | `Implement\n` | Deny |
| H15 | MultiEdit, same path as H1 | `implement` | Deny |

Not run: a symlink into an acceptance path. Creating symlinks on Windows needs Developer Mode or admin rights. The hook resolves symlinks with `os.path.realpath`, but that is untested here.

## K. Check-after-edit hook, unit cases (ADR-011@v1 C1)

Written 2026-11-03. The hook is `.claude/hooks/check_edited.py`, a `PostToolUse` hook on the same tools. It syntax-checks the edited file by type. The repository has no build or formatter yet, so this is as far as C1 goes for now. "Reported" means exit 0 with `"decision": "block"` and a reason naming the file, which Claude sees next to the tool result. "Silent" means exit 0 and no output.

| Case | Edited file | Expected |
| --- | --- | --- |
| K1 | Valid `.json` | Silent |
| K2 | Invalid `.json` | Reported |
| K3 | Valid `.py` | Silent |
| K4 | `.py` with a syntax error | Reported |
| K5 | Valid `.sh` (`bash -n`) | Silent |
| K6 | `.sh` with a syntax error | Reported |
| K7 | Valid `.ps1` (PowerShell parser) | Silent |
| K8 | `.ps1` with a parse error | Reported |
| K9 | `.md` | Silent: no check for this type |
| K10 | A path that no longer exists | Silent |

## L. Live cases with Claude Code v2.1.317 (ADR-011@v1 C2, C3, C4, C5)

Written 2026-11-03. Each case runs `claude -p` (v2.1.317, installed with npm on 3 Nov at Andy's request) in a throwaway git repository. The repository holds a copy of this branch's `.claude/settings.json` and hooks. The read and write blocks are passed with `--settings`, so Andy's user settings are not touched. The model only drives the tool call. Each case is judged by what is on disk and by `permission_denials` in the JSON output, not by what the model says. A case where the model never calls the tool counts as not run, and is retried once.

"Refused" means the file is not written (or the read returns nothing) and the call appears in `permission_denials`. "Done" means the file is written (or its content is returned).

| Case | Action | Mode | Expected | Why |
| --- | --- | --- | --- | --- |
| L1 | Write to a file outside the repository, with the write block | `bypassPermissions` | Refused | The block holds in every mode (settings reference) |
| L2 | Write `docs/notes.md` | `acceptEdits` | Done | Inside, not protected |
| L3 | Write `docs/adr/ADR-999.md` (ask rule) | `bypassPermissions` | Refused | Ask rules are never auto-approved; with no one to answer, `-p` denies |
| L4 | Write `docs/adr/ADR-999.md` | `acceptEdits` | Refused | Same |
| L5 | Bash `echo x > docs/adr/x.md` | `bypassPermissions` | Done: a gap | The docs say redirects are checked against Edit allow and deny rules; ask rules aren't named |
| L6 | Write `tests/acceptance/x.cs`, marker `implement` | `bypassPermissions` | Refused | A hook's deny holds in every mode |
| L7 | Write `tests/acceptance/x.cs`, no marker | `bypassPermissions` | Done | A hook's ask is a prompt, and bypass skips prompts; the exceptions listed don't include it |
| L8 | Read a file outside the repository, with the read block | `bypassPermissions` | Refused | The block holds in every mode |
| L9 | Read `docs/notes.md` | `default` | Done | Inside |
| L10 | Write invalid `config/bad.json` | `acceptEdits` | Done, and the check-after-edit reason reaches the model | `PostToolUse` runs after the write |
| L11 | Write `.claude/settings.local.json`, with the write block | `bypassPermissions` | Refused | The write block refuses settings files everywhere |
