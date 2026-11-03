---
id: ADR-011
version: 2
title: Deterministic controls gate what coding agents can read, write and change
status: proposed
date: 2026-11-03
decision-makers: [Andy Douglas]
scope: [project, concern:delivery, concern:security]
precedence:
  tier: cross-cutting
  overrides: []
supersedes: []
superseded-by: null
exceptions: not-allowed
enforcement:
  - constraint: C1
    mechanism: PostToolUse hook syntax-checking edited JSON, Python, shell and PowerShell files; no build, formatter or tests exist in this repository yet
    ref: .claude/hooks/check_edited.py
    state: planned
  - constraint: C2
    mechanism: permissions.ask rules in the committed .claude/settings.json; file tools only; the prompt not yet observed in an interactive session
    ref: .claude/settings.json
    state: planned
  - constraint: C3
    mechanism: PreToolUse hook reading acceptance-test globs and the stage marker .specify/stage; file tools only; the marker is set by hand
    ref: .claude/hooks/acceptance_tests.py
    state: planned
  - constraint: C4
    mechanism: permissions.blockReadsOutsideWorkingDirectories in Andy's user settings (set 3 Nov), outside this repository, with no additionalDirectories; tested with the CLI
    ref: null
    state: enforced
  - constraint: C5
    mechanism: permissions.blockWritesOutsideWorkingDirectories in the committed .claude/settings.json; needs Claude Code v2.1.314 or later
    ref: .claude/settings.json
    state: planned
  - constraint: C6
    mechanism: Read and Edit deny rules in Andy's user settings, outside this repository; untested
    ref: null
    state: manual
  - constraint: C7
    mechanism: review; the bootstrap guard and .gitignore match private-eval and Architect-in-the-loop-evaluator by name, subject/ included, and the guard checks git remote URLs
    ref: scripts/check-private-material.ps1
    state: manual
backlog: [D1]
---

# ADR-011: Deterministic controls gate what coding agents can read, write and change

## Context

Instructions in CLAUDE.md are advisory: an agent can misread them, or ignore them under pressure. The project's thesis is "deterministic where possible", so the rules that matter most must be enforced by checks the agent can't talk its way past. These rules include: never reading the private evaluation repository (hard rule 1), never editing acceptance tests to make them pass (hard rule 3), and never writing outside the project.

Claude Code offers three relevant mechanisms inside the tool. Hooks run before or after tool calls and can block them. Permission rules allow, ask or deny. And two settings refuse file-tool access outside the working directories in every permission mode: `permissions.blockReadsOutsideWorkingDirectories` (v2.1.257 or later) for reads, and `permissions.blockWritesOutsideWorkingDirectories` (v2.1.314 or later) for Write, Edit and NotebookEdit. None of these contains a script that opens files itself. Only a fourth mechanism, the OS-level sandbox, does, and it doesn't run on native Windows.

## Decision

**Deterministic checks gate every change** (D1, dogfooding). A hook checks each file after an edit. Today that is a syntax check, because this repository has nothing to build, format or test yet. *(The syntax check is the author's default, stated to Andy on 3 Nov and not ruled. How the build, format and tests run after edits once there is code is open.)* **A hook blocks writes to acceptance test paths during implement,** so hard rule 3 becomes a deterministic control.

**Protected paths ask Andy, in every mode** (decided 2 Nov; mechanism chosen 3 Nov). The paths are `.specify/memory/constitution.md`, `docs/adr/`, `REVIEW.md`, `CLAUDE.md`, `.claude/settings*.json`, `tests/constitution/expected.md`, `subject/` from this repository's side, and the stage marker `.specify/stage`. Each is an explicit `ask` rule in the committed `.claude/settings.json`. Claude Code never auto-approves an explicit ask rule, in any mode, including `bypassPermissions`. The rules cover the file tools. A shell redirect into a protected path wasn't asked for in `bypassPermissions` mode (tested 3 Nov). While the write block (C5) is on, Claude Code refuses edits to `.claude/settings*.json` outright, which is stricter than asking. The ask rule for them applies only where the block isn't in force, such as a desktop session on v2.1.309.

**Acceptance tests during implement** (decided 3 Nov). The hook reads gitignore-style globs from `.claude/hooks/acceptance-tests.json`. It denies a write to a matching path while the marker `.specify/stage` reads `implement`, and asks otherwise, so the skill that writes acceptance tests can still work outside implement with Andy's approval. The globs are placeholders until DEV-1 fixes the fork's test layout. The marker is a protected path. It is set by hand today; until it reads `implement`, an implement run gets "ask", not "deny". The hook sees file tools only. Anything the hook can't evaluate is blocked. *(Blocking on failure is the author's choice, not ruled: Andy approved borrowing spec-gates' "fail to ask"; this hook fails to block.)*

**File access is an allowlist:**

- **Reads:** `permissions.blockReadsOutsideWorkingDirectories` in user settings. It refuses Read, Grep, Glob and LSP outside the working directories, and the docs say it keeps Claude Code's own files under `~/.claude/` readable. Tested 3 Nov: auto memory, saved tool output and the session scratchpad stay readable, so `additionalDirectories` is empty. A user skill read with the Read tool in `default` mode still prompted, with or without the block. Anything else Claude needs is added to `additionalDirectories`. The desktop app may start a session with `~/.claude` as an extra working directory; the block then treats all of it as inside.
- **Writes:** `permissions.blockWritesOutsideWorkingDirectories` in the committed `.claude/settings.json` (decided 3 Nov, replacing the planned write hook). It refuses Write, Edit and NotebookEdit outside the working directories in every mode, with no prompt, and keeps a few of Claude Code's own files writable, such as the scratchpad and the `.md` files in auto memory. It also refuses every Claude edit to a settings file, inside the project too, so Andy edits `.claude/settings*.json` himself.
- **Backstop:** deny rules in Andy's user settings name the private evaluation repository's path, one for Read and one for Edit (added 20 Oct at Andy's request: "add the deny rules for the eval repo"). It is a backstop, not a guarantee: in one documented setup, with no managed settings and no Team or Enterprise login, a mod can approve a call that a deny rule refuses.

**Evaluation material stays out of reach.** Hidden tests and labels live in a separate private repository that is never cloned into a build worktree (hard rule 1; how it is run is E6). The bootstrap scripts refuse a tree holding it under either name.

**Prior art.** The *gates* extension (github.com/schwichtgit/spec-gates, MIT) was reviewed at v0.5.0 on 3 Nov. Its design is borrowed: fail closed, normalise the path, ignore case, resolve links, and test with planted violations. Its code isn't adopted: it needs bash, `jq` and POSIX paths, and its commit hook refuses the `Co-Authored-By` trailer this project keeps. Its path rules match `/`, and Claude Code sends backslash paths on Windows, so they would likely let those paths through (found by reading, not by running).

Open (D1): whether anything checks shell writes (the default in Step 7, not ruled, is that nothing does); whether to move to WSL2, so the sandbox can contain shell commands; wiring the stage marker into `/speckit-implement`.

## Constraints

- **C1:** The build, format and tests MUST run automatically after edits.
- **C2:** Writes to protected paths MUST ask Andy for approval, in every permission mode. *(v2: was "MUST be blocked by a hook".)*
- **C3:** Writes to acceptance test paths MUST be blocked by a hook during implement.
- **C4:** File-tool reads outside the working directories and the allowlist MUST be refused.
- **C5:** File-tool writes outside the allowlist MUST be refused, with no prompt to approve them.
- **C6:** Reads and edits of the private evaluation repository's path MUST be denied in user settings.
- **C7:** Evaluation material MUST live in a separate private repository that is never cloned into this repository or a build worktree.

## Consequences

Easier:

- The rules that matter most hold even when an agent gets them wrong.
- Each control is a counted, deterministic clause for Q1's metric.
- C2, C4, C5 and C6 use built-in settings, not code to maintain.

Harder:

- Shell commands and scripts aren't contained on native Windows. Until the sandbox is available, a script that opens files itself gets past every control here. A shell redirect into a protected path isn't asked for in `bypassPermissions` mode (tested 3 Nov).
- The allowlist's exceptions need maintaining, or the controls block Claude's own housekeeping.
- Hooks are code to write, test and keep working across worktrees.
- The write block needs Claude Code v2.1.314. The desktop app bundled v2.1.309 on 3 Nov, so desktop sessions aren't covered until the app updates.
- While the write block is on, Claude Code removes the `EnterWorktree` tool. Its effect on the desktop app's own worktrees is untested.

## Alternatives

### Do nothing: rely on CLAUDE.md's instructions (added when writing this ADR)

- For: no work.
- Against: advisory only. This is the "prompt and hope" approach the product exists to replace.

### Deny rules alone, for everything outside the project (weighed in D1, 20 Oct)

- For: built in.
- Against: deny beats allow, so a deny rule broad enough to fence everything also blocks the project folder.

### One hook for both reads and writes (decided 20 Oct, revised 21 Oct)

- For: one mechanism.
- Against: duplicates the built-in read block. It was chosen on the author's wrong claim that no such setting existed.

### The built-in read block, a write hook and a deny-rule backstop (chosen 21 Oct, revised 3 Nov)

- For: uses the built-in control where one exists, and code only where it doesn't.
- Against: shell commands remain uncontained without WSL2. Since v2.1.314 a built-in write block exists, so the write hook duplicates it.

### The built-in read and write blocks and a deny-rule backstop (chosen 3 Nov)

- For: the same principle as 21 Oct, applied to writes now the setting exists. No write hook to maintain.
- Against: needs v2.1.314, so desktop sessions wait for the app to update; settings files become editable only by Andy; shell commands remain uncontained.

### Protected paths blocked outright by a hook (v1, revised 2 Nov)

- For: no prompt to click through.
- Against: legitimate edits to the ADRs and the constitution would have to go round the control. Andy chose approval instead.

### Protected paths as a hook returning "ask" (weighed 3 Nov)

- For: one policy file with the acceptance-test hook, and clearer messages.
- Against: how a hook's "ask" behaves in `bypassPermissions` mode isn't documented; explicit ask rules are documented to prompt in every mode.

### Adopt spec-gates (weighed 3 Nov)

- For: an existing, tested policy enforced at three boundaries.
- Against: see Prior art above.

The naive option (an LLM with everything in its prompt) is the "do nothing" option here.

## Enforcement

Tests are in `tests/controls/` (3 Nov, Claude Code v2.1.317 with `claude -p`). C4 is enforced: set in Andy's user settings, outside this repository, and tested from there, refusing a read outside and allowing memory, saved tool output and the scratchpad. It is not yet observed in a desktop app session. C2 and C3 are planned, although their mechanisms exist and pass their tests. C2's ask rules refused protected writes, but under `-p` an ask can't be told from a refusal, so the prompt itself is not yet observed, and shell writes get past it. C3's hook denied during implement and asked otherwise, but the marker is set by hand and shell writes aren't seen. C1 is planned: the hook runs after every edit, but it is a syntax check, not a build, format or test run. C5 is set in the committed settings and tested on v2.1.317, but it stays planned until the desktop app runs v2.1.314 or later. C6's deny rules are in place in user settings, but they are untested and outside this repository, so C6 is recorded as manual. C7 is held by review, with the bootstrap guard as a check that runs when bootstrap runs. The guard matches names and git remote URLs, so a renamed copy stripped of its git metadata wouldn't be caught.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D1's decisions of 5 Oct (gates, protected paths, evaluation material), 20 Oct (test-path hook) and 20 Oct revised 21 Oct (file-access allowlist). C6's Read and Edit rules trace to Andy's request of 20 Oct, "add the deny rules for the eval repo".
- **v2** · 2026-11-03 · revision · proposed, not yet approved by Andy Douglas: C1's Decision text states today's syntax check; C2 asks rather than blocks, with the protected-path list (decided 2 Nov) as explicit ask rules (chosen 3 Nov); C3's globs and stage marker, with the marker added to the protected paths (chosen 3 Nov: "The marker itself is protected"); C5 by the built-in write block in project settings, replacing the write hook (chosen 3 Nov: "install the latest version of the sdk and continue from there", then "project settings"); spec-gates reviewed, design borrowed and code not adopted (chosen 3 Nov); the read block set in user settings with no additionalDirectories (approved 3 Nov: "Yes, make the change"); C1 to C5 and C7 enforcement updated.
