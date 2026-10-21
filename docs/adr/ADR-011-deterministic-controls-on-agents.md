---
id: ADR-011
version: 1
title: Deterministic controls gate what coding agents can read, write and change
status: accepted
date: 2026-10-21
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
    mechanism: Claude Code hook running build, format and tests after edits
    ref: null
    state: planned
  - constraint: C2
    mechanism: PreToolUse hook blocking writes to protected paths
    ref: null
    state: planned
  - constraint: C3
    mechanism: PreToolUse hook blocking writes to acceptance test paths during implement
    ref: null
    state: planned
  - constraint: C4
    mechanism: permissions.blockReadsOutsideWorkingDirectories in user settings
    ref: null
    state: planned
  - constraint: C5
    mechanism: PreToolUse hook denying Edit, Write and NotebookEdit outside the allowlist
    ref: null
    state: planned
  - constraint: C6
    mechanism: Read and Edit deny rules in Andy's user settings, outside this repository; untested
    ref: null
    state: manual
  - constraint: C7
    mechanism: review; .gitignore and the bootstrap scripts guard only names containing private-eval
    ref: .gitignore
    state: manual
backlog: [D1]
---

# ADR-011: Deterministic controls gate what coding agents can read, write and change

## Context

Instructions in CLAUDE.md are advisory: an agent can misread them, or ignore them under pressure. The project's thesis is "deterministic where possible", so the rules that matter most must be enforced by checks the agent can't talk its way past. These rules include: never reading the private evaluation repository (hard rule 1), never editing acceptance tests to make them pass (hard rule 3), and never writing outside the project.

Claude Code offers three relevant mechanisms. Hooks run before or after tool calls and can block them. Permission rules allow, ask or deny. And the setting `permissions.blockReadsOutsideWorkingDirectories` refuses file-tool reads outside the working directories in every permission mode. None of these contains a script that opens files itself; only the OS-level sandbox does, and it doesn't run on native Windows.

## Decision

**Deterministic checks gate every change** (D1, dogfooding). Hooks run the build, format and tests after edits, and block writes to protected paths. **A hook blocks writes to acceptance test paths during implement,** so hard rule 3 becomes a deterministic control. The existing *gates* extension (github.com/schwichtgit/spec-gates, MIT), which enforces one policy as Claude Code hooks, git pre-commit and CI, is reviewed before we write our own hooks.

**File access is an allowlist:**

- **Reads:** `permissions.blockReadsOutsideWorkingDirectories` in user settings. It refuses Read, Grep, Glob and LSP outside the working directories, and keeps Claude Code's own files under `~/.claude/` readable. Anything else Claude needs, such as the session scratchpad or saved tool output, is added through `additionalDirectories` in user settings.
- **Writes:** a `PreToolUse` hook denies Edit, Write and NotebookEdit on any path outside the same allowlist.
- **Backstop:** a deny rule in Andy's user settings names the private evaluation repository's path. It is a backstop, not a guarantee: in one documented setup, with no managed settings and no Team or Enterprise login, a mod can approve a call that a deny rule refuses.

**Evaluation material stays out of reach.** Hidden tests and labels live in a separate private repository that is never cloned into a build worktree (hard rule 1; how it is run is E6).

The allowlist and the write hook are switched on and tested with the other hooks in Step 7. Whether to move to WSL2, so the sandbox can contain shell commands, is open.

## Constraints

- **C1:** The build, format and tests MUST run automatically after edits.
- **C2:** Writes to protected paths MUST be blocked by a hook.
- **C3:** Writes to acceptance test paths MUST be blocked by a hook during implement.
- **C4:** File-tool reads outside the working directories and the allowlist MUST be refused.
- **C5:** File-tool writes outside the allowlist MUST be refused.
- **C6:** Reads and edits of the private evaluation repository's path MUST be denied in user settings.
- **C7:** Evaluation material MUST live in a separate private repository that is never cloned into this repository or a build worktree.

## Consequences

Easier:

- The rules that matter most hold even when an agent gets them wrong.
- Each control is a counted, deterministic clause for Q1's metric.

Harder:

- Shell commands and scripts aren't contained on native Windows. Until the sandbox is available, a script that opens files itself gets past every control here.
- The allowlist's exceptions need maintaining, or the controls block Claude's own housekeeping.
- Hooks are code to write, test and keep working across worktrees.

## Alternatives

### Do nothing: rely on CLAUDE.md's instructions (added when writing this ADR)

- For: no work.
- Against: advisory only. This is the "prompt and hope" approach the product exists to replace.

### Deny rules alone, for everything outside the project (added when writing this ADR)

- For: built in.
- Against: deny beats allow, so a deny rule broad enough to fence everything also blocks the project folder.

### One hook for both reads and writes (decided 20 Oct, revised 21 Oct)

- For: one mechanism.
- Against: duplicates the built-in read block. It was chosen on the author's wrong claim that no such setting existed.

### The built-in read block, a write hook and a deny-rule backstop (chosen)

- For: uses the built-in control where one exists, and code only where it doesn't.
- Against: shell commands remain uncontained without WSL2.

The naive option (an LLM with everything in its prompt) is the "do nothing" option here.

## Enforcement

Nothing here is enforced yet, except C6, which is in place in user settings but untested and outside this repository, so it is recorded as manual. C1 to C5 are planned for Step 7. C7 is held by review. `.gitignore` and the bootstrap scripts only guard names containing `private-eval`, and the bootstrap check skips `subject/`, so a copy under the repository's real name wouldn't be caught.

## History

- **v1** · 2026-10-21 · accepted · Andy Douglas: first version, recording D1's decisions of 5 Oct (gates, protected paths, evaluation material), 20 Oct (test-path hook) and 20 Oct revised 21 Oct (file-access allowlist).
