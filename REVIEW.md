# Review policy

Status: v0.2 · 20 Oct 2026 (v0.2: severity rule for untraced detail; corrections checked against source) · documentation PRs only (backlog D1). Code review is added when there is code (Step 7).

The adversarial reviewer works to this policy. It is a subagent with a fresh context. It sees the diff, the repository and this file, never the author's reasoning or conversation.

**The reviewer never approves.** It reports findings. The author fixes each finding or argues against it in the PR description. Andy decides and merges.

## What to check

Work through four passes, in order. Each finding names the file and line, the pass, and the evidence.

### 1. Fidelity: is every decision one that was actually made?

The main risk in documentation PRs is the author adding, softening or strengthening a decision while writing it up.

- Every decision, constraint and "decided" statement MUST trace to text in [backlog.md](backlog.md), an earlier ADR, or an approval quoted in the PR description. Cite the source you found.
- Flag anything with no source as **untraced**: a design detail, rule, threshold or example that the source doesn't contain.
- Flag any change of strength: SHOULD in the source but MUST in the ADR, a condition or exception dropped, or scope widened or narrowed.
- Flag decisions in the source that the PR should carry but leaves out.
- **For an ADR correction** (a new version typed `correction`), check every changed line against its source. A correction that changes the decision is High (ADR-000@v2 C11).

### 2. Facts: are the claims true?

- Check every claim about eShop against the code in `subject/eshop`, and every claim about this repo against its files: paths, settings, file names, behaviour.
- Check claims about tools and standards (versions, features, licences) where the repository or the PR cites a source. Otherwise flag the claim as **unverified**.
- Check that links and paths resolve.

### 3. Constraints: can each rule be checked?

For ADRs, against [ADR-000](docs/adr/ADR-000-decision-record-format.md):

- Each constraint is one checkable statement using MUST, MUST NOT or SHOULD (C6). Flag constraints that combine several rules, or can't be checked by anyone.
- Alternatives include "do nothing" and, where it applies, the naive option (C7).
- Constraints don't contradict each other, other ADRs or CLAUDE.md's hard rules.

### 4. Honest enforcement: does anything claim more than it has?

- No enforcement entry is `enforced` unless the check exists and you can point to it.
- `ref` points at something real, or is null.
- The prose doesn't imply a check exists when the state is `planned` or `manual`.
- Claims of measurement are backed by a measurement (CLAUDE.md: no claim without a measurement).

## Out of scope

- Whether a decision is a good one. The reviewer checks the write-up against the decision, not the decision itself. If you think a decision is wrong, add it as a single note at the end, outside the findings.
- Matters of style that don't change meaning. Report at most five of these, as nits.

## Rules for the reviewer

- Read-only. Don't edit files, commit, push or comment on GitHub.
- Never access the private evaluation repository, or any path outside this repository (CLAUDE.md hard rule 1).
- Say when you couldn't check something, and why. Don't guess.

## Output

A table of findings, most severe first, then the nits (at most five), then any note on the decisions themselves.

| # | Severity | Pass | Location | Finding | Evidence |
| --- | --- | --- | --- | --- | --- |

Severity:

- **High:** a decision, constraint or enforcement claim that is wrong, untraced or overstated. It would mislead an agent or a check that reads it. Untraced detail is High wherever it appears (constraints, prose, front matter, to-do lists) if an agent or check would act on it.
- **Medium:** a factual error, an unverified claim that matters, or a constraint that can't be checked.
- **Low:** an omission or imprecision that doesn't change what anyone would do.
- **Nit:** wording only.

End with a line counting the findings at each severity, and listing what you couldn't check.
