# Expected results: ADR validator and index generator

Written 2026-11-04, before any code, under ADR-012@v2 C10. Never edited after a run: a wrong expectation gets a dated expectation beside it. Results go in [results.md](results.md).

Step 7, item 2 (backlog Q6, VL-9). Andy's ruling of 4 Nov: "Code checks now; CUE question researched first". So this validator holds the checks that need git and plain code. The front-matter schema (ADR-000@v3 C1: every field present, with the right shape) waits for the CUE versus JSON Schema research. It is not checked here.

## What the validator checks

`scripts/adr.py check [--base <ref>]`, over `docs/adr/ADR-*.md`:

| Rule | Check |
| --- | --- |
| ADR-000@v3 C2 | The second-level sections are exactly Context, Decision, Constraints, Consequences, Alternatives, Enforcement, History, in that order |
| ADR-000@v3 C3 | `id` is `ADR-` plus three digits, unique, and the file name starts with it |
| ADR-000@v3 C5 | Every constraint in Constraints has exactly one `enforcement` entry, and every entry names an existing constraint |
| ADR-000@v3 C8 | With `--base`: an ADR whose text changed, apart from an enforcement entry's `state` or `ref`, has a higher `version` and one more History line. Each new History line reads `- **vN** · YYYY-MM-DD · <type> · …`, with type `revision` or `correction` and N equal to the new version. ADRs new since the base aren't compared |
| ADR-000@v3 C9 | With `--base`: no constraint ID present at the base is missing |
| ADR-009@v2 C10, C14 | The constitution's ADR Index rows equal the rows generated from front matter: `\| [ADR-nnn](../../docs/adr/<file>) \| <title> \| <scope, comma-separated> \|`, in ID order, with no version |
| ADR-009@v2 C17 | Each numbered hard rule under CLAUDE.md's "Hard rules" appears word for word in the constitution |

`scripts/adr.py index --write` rewrites the constitution's index rows from front matter. A failure prints the file, the rule and what is wrong, and exits 1. A pass exits 0.

The C1 hook (`check_edited.py`) and CI's changed-files check run the per-file rules (C2, C3's file-name rule and C5) on any edited `docs/adr/ADR-*.md`, using the same functions. CI also runs `scripts/adr.py check --base origin/<base>` on pull requests.

## A. Validator cases

Each case copies this repository's `docs/adr/`, constitution and CLAUDE.md into a throwaway git repository, commits that as the base, applies one change, commits it, and runs `check --base` against the base.

| Case | Change | Expected |
| --- | --- | --- |
| A0 | None: the repository as it is at `origin/main` | Pass. A prediction: the ADRs were written by hand to these rules and twice reviewed, but never checked by a program, so a fail here is plausible and would be a finding, not a fault in the case |
| A1 | Remove the Alternatives section from ADR-005 | Fail, C2 |
| A2 | Swap Consequences and Alternatives in ADR-005 | Fail, C2 |
| A3 | Rename ADR-005's file so it starts `ADR-050-` | Fail, C3 |
| A4 | Set ADR-006's `id` to `ADR-005` | Fail, C3 (duplicate), and C3 (file name) |
| A5 | Set ADR-005's `id` to `ADR-5` | Fail, C3 |
| A6 | Add a constraint C99 to ADR-005's Constraints, with no enforcement entry | Fail, C5 |
| A7 | Add an enforcement entry for C99 to ADR-005, with no such constraint | Fail, C5 |
| A8 | Change a word in ADR-005's Decision, version unchanged | Fail, C8 |
| A9 | As A8, version incremented, no new History line | Fail, C8 |
| A10 | As A8, version incremented and a well-formed `revision` History line added | Pass |
| A11 | Change only an enforcement entry's `state` in ADR-005, version unchanged | Pass |
| A12 | As A10, and ADR-005's last constraint deleted, with its enforcement entry | Fail, C9 |
| A13 | As A10, and ADR-005's last constraint marked withdrawn, its entry's state `withdrawn` | Pass |
| A14 | Change one title in the constitution's index | Fail, C10 and C14 |
| A15 | Delete one row from the constitution's index | Fail, C10 and C14 |
| A16 | Add a new ADR-099, valid, not in the index | Fail, C10 and C14; no C8 comparison for it |
| A17 | As A16, then `index --write` | Pass |
| A18 | Change one word in hard rule 3 in the constitution | Fail, C17 |
| A19 | As A10, but the History line's type is `update` | Fail, C8 |

## F. Front-matter schema, dated expectation 2026-11-04

Written after Andy's ruling of 4 Nov ("JSON Schema; record CUE finding in Q1"), before the schema exists. `scripts/adr.py check` validates each ADR's front matter, parsed with PyYAML, against `scripts/adr-front-matter.schema.json` (JSON Schema 2020-12, through the `jsonschema` library), for ADR-000@v3 C1. The fields and their allowed values come from `docs/adr/template.md`: `status` in proposed, accepted, rejected, deprecated, superseded; `precedence.tier` in cross-cutting, domain, component; `exceptions` in allowed, not-allowed; each enforcement `state` in enforced, planned, manual, withdrawn; `id`, `overrides`, `supersedes` and `superseded-by` as ADR IDs; `date` as YYYY-MM-DD. Fields beyond the template's are allowed (the author's default: C1 requires the template's fields, and doesn't forbid others). The two libraries are pinned in `requirements.txt` and installed in CI. The C1 hook keeps to the per-file checks, which need no libraries.

Each case changes ADR-005's front matter in a throwaway repository and runs `check` (no `--base`).

| Case | Change | Expected |
| --- | --- | --- |
| F0 | None | Pass |
| F1 | Remove the `backlog` field | Fail, C1 |
| F2 | `status: approved` | Fail, C1 |
| F3 | `version: two` | Fail, C1 |
| F4 | `date: 4 Nov 2026` | Fail, C1 |
| F5 | One enforcement entry's `state: done` | Fail, C1 |
| F6 | Remove `overrides` from `precedence` | Fail, C1 |
| F7 | `superseded-by: ADR-5` | Fail, C1 |
| F8 | `scope: project`, a string, not a list | Fail, C1 |
| F9 | Front matter that isn't valid YAML (an unclosed `[`) | Fail, C1, with no crash |
| F10 | An extra field, `owner: Andy Douglas` | Pass |

## K. The C1 hook on ADR edits (addition to tests/controls/expected.md section K)

| Case | Edited file | Expected |
| --- | --- | --- |
| K12 | A copy of ADR-005 named `docs/adr/ADR-005-x.md` with its Alternatives section removed | Reported, naming C2 |
| K13 | An unchanged copy of ADR-005 at `docs/adr/ADR-005-x.md` | Silent |
| K14 | `docs/adr/template.md` | Silent: the template isn't an ADR |
