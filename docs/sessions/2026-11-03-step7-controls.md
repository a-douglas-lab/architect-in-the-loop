# Session log · Step 7, second track · 2–3 Nov 2026

Phase 1, Foundations. Step 7, items 4 (Claude Code controls) and 6 (bootstrap guard), carried in their own worktree (`claude/step7-controls-cc0237`), in parallel with the rule-unit spike (ADR-010@v1 C2). Started from the [Step 7 brief](2026-11-02-step7-brief.md). All work is local and awaits Andy's review; nothing is pushed.

## Done

- **Prior art reviewed before building:** spec-gates at v0.5.0 (tag `78b2d6c`), its `protect-files.sh` and `settings.fragment.json` read in full; Claude Code's hooks, permissions, permission-modes and settings-reference pages, fetched 3 Nov. Findings and options went to Andy before any hook was written.
- **Bootstrap guard (item 6):** `scripts/check-private-material.ps1` and `.sh` match `private-eval` and `Architect-in-the-loop-evaluator` in any case, search `subject/` too, and check git remote URLs. Both bootstrap scripts call them, and `.gitignore` gained the real name. Ten cases pass in both shells; the old guard caught one of them.
- **Hooks:** `.claude/hooks/acceptance_tests.py` (C3) and `check_edited.py` (C1), wired in a new committed `.claude/settings.json` with `onFailure: "block"` on the first. 25 unit cases pass. Run 1 found a crash on `.sh` files (no bash on PATH), fixed.
- **Protected paths (C2)** as ask rules, and the **write block (C5)** in the same project settings.
- **Read block (C4)** set in Andy's user settings, after he saw the exact change and approved it.
- **Live tests** with `claude -p` v2.1.317, which Andy asked to have installed: 11 control cases, 8 read cases and 4 user-settings cases. Each miss is explained in [results](../../tests/controls/results.md).
- **ADR-011 v2 drafted,** pending Andy's approval. Backlog D1 and Q6 updated.

## Decided (Andy, 3 Nov)

- Protected paths are `permissions.ask` rules.
- Acceptance tests: policy globs and a stage marker.
- spec-gates: borrow the design, not the code.
- The write block is the built-in setting, on the latest CLI ("install the latest version of the sdk and continue from there"), installed as the npm CLI pinned at 2.1.317, and set in project settings.
- The read block goes in user settings as shown ("Yes, make the change").

## Found

- **A built-in write block now exists** (`blockWritesOutsideWorkingDirectories`, v2.1.314). This is the second time a planned hook has turned out to duplicate a setting; the first was the read block on 21 Oct.
- **The desktop app bundles its own CLI,** v2.1.309 on 3 Nov, separate from the npm CLI and signed in separately. Controls tested on the CLI aren't yet observed in a desktop session.
- **spec-gates' path rules would let Windows paths through:** its matches use `/`, and Claude Code sends backslashes on Windows. Found by reading, not by running.
- **Shell writes get past the ask rules** in `bypassPermissions` mode (L5).
- **The read block keeps more readable than the docs say:** saved tool output and the scratchpad, as well as memory.
- **This desktop session was started with `~/.claude` as an extra working directory,** so the read block treats all of it as inside, `.credentials.json` included.
- **Test runs leave folders behind** in `~/.claude/projects/` (one per throwaway repository, named `C--Users-adoug-AppData-Local-Temp-tmp…-repo`). They were not deleted; Andy decides.

## Open for next step

- Andy's local review of this branch, and his approval of ADR-011 v2.
- Observe the controls in a desktop session: a new session for the read block now, and the write block once the app runs v2.1.314 or later.
- Questions raised (backlog D1): wiring the stage marker into `/speckit-implement`; protecting `.claude/hooks/`; `EnterWorktree` under the write block; shell writes.
