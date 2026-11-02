# Rule units: problem, criteria and prior art

Status: draft for Andy's review · 2 Nov 2026 · Step 7, item 1 ([brief](../../docs/sessions/2026-11-02-step7-brief.md)); backlog T6, "Rule units"

This is steps 1 and 2 of the discernment method (backlog D1): the problem, the criteria, and prior art. Nothing has been built. The recommendation at the end needs Andy's go-ahead, and eight questions need his ruling. Reviewed once by the adversarial reviewer ([loop card](../../docs/loops/cards/2026-11-02-rule-units-prior-art-review-run11.md)); the fixes weren't re-reviewed.

## Problem

`speckit-analyze` checks a feature's spec, plan and tasks against the constitution only. The constitution points to ADRs but doesn't restate them (ADR-009@v2 C15), so `analyze` sees ADR titles, not constraints. A breach that no title reveals is missed: fixture f8 writes analyzer rule violations to a CSV file, which breaks ADR-016@v1 C10 ("Tools that report rule violations MUST report in SARIF"), and `analyze` missed it in 3 of 3 runs ([results.md](../../tests/constitution/results.md)). Every run reported opening no ADRs (self-reported).

The hypothesis is that the gap is selection, not reasoning: the right constraint never reaches the agent. It is unmeasured; criterion 1 tests it. Andy's T6 text says "A bigger constitution doesn't fix that". Copying constraints into the constitution would at least put C10 in front of `analyze`, but it was weighed and not chosen in ADR-009@v2, for duplication, drift and cost. The proposal is rule units: each ADR constraint as a self-contained, testable unit, selected deterministically (backlog T6).

## Criteria

1. **Closes the measured gap.** f8's breach is caught when its unit is loaded, measured as a rate over three blind runs.
2. **Deterministic selection.** The same artefacts and stage always select the same units. No model reads titles to choose. T6's "Rule units" paragraph says units load deterministically, while its proposed four-routes table says judgement rules are selected by the model; question 6 asks Andy which holds for the judgement unit.
3. **Works before code exists.** At specify and plan there are no changed files, so applicability can't rest on paths alone (backlog T6, "Spike").
4. **Each unit is testable on its own,** with fixtures that must pass and fixtures that must fail, expected results written first (ADR-012@v2 C10).
5. **No drift from the source.** A unit carries its citation (`ADR-nnn@vN Cn`, or the hard rule's number) and the rule's text word for word, so a validator can compare it with the source.
6. **Fits ADR-009.** Spec Kit stays core only (ADR-009@v2 C4); changing that is a revision of ADR-009, and a community extension also needs a source review and a pinned version (C5).
7. **Scales.** An index is always present; unit bodies load on demand (backlog T6, "Rule units"; the scaling model gives the costs).
8. **Small.** A spike in Python that doesn't decide the capability's stack (T5).

## Options, including the naive one and doing nothing

| Option | For | Against |
| --- | --- | --- |
| Do nothing | No work | f8-type breaches stay invisible: 0 of 3 caught |
| Naive: load every full ADR into `analyze` | Nothing missed today | About 33,000 tokens at 19 ADRs, passing an assumed 200,000-token window at about 115 ADRs (T6 model); still no tests per rule |
| Copy constraints into the constitution | `analyze` sees them | Weighed and not chosen in ADR-009@v2: duplication, drift and cost |
| Install adrkit | Already built (pre-1.0; maintenance activity not checked) | See below: whole-ADR granularity, selection by files, no per-decision tests described, and installing its extension means revising ADR-009 |
| Build rule units, borrowing shapes from prior art | Meets the criteria if the spike shows it | Authoring cost per constraint; keyword triggers have limited recall |

The naive figure is 19 × about 1,750 tokens, using T6's average, measured before ADR-009 v2 (which has since grown); it is an estimate at 4 characters a token.

## Prior art

Checked against current documentation on 2 Nov 2026. Each entry says what the tool does, what to borrow, and what it lacks for this problem.

### ESLint: rule plus `RuleTester`

- A rule is an object with `meta` (fields include `type`, `docs.description`, `docs.url`, `messages`, `schema`, `fixable` and `deprecated`) and a `create` function ([custom rules](https://eslint.org/docs/latest/extend/custom-rules)).
- `RuleTester.run(name, rule, { valid, invalid })` tests it. An invalid case must state `errors`, as a count or as objects with `message` or `messageId`. `RuleTester` "is used internally for the bundled rules that come with ESLint" ([Node.js API](https://eslint.org/docs/latest/integrate/nodejs-api#ruletester)). The docs don't require plugin rules to ship tests.
- **Borrow:** identity and metadata in the unit; `valid` and `invalid` cases run by one runner; an invalid case states which finding it expects, not just "fails".
- **Lacks:** nothing in the rule itself says where it applies; that is left to the user's configuration (not checked in detail).

### Semgrep: rule, `paths`, annotated tests

- Required fields: `id`, `message`, `severity`, `languages`, and a pattern. Optional `paths` takes `include` and `exclude` globs relative to the project root; exclusion wins. Optional `metadata` is free data that doesn't affect matching ([rule syntax](https://docs.semgrep.dev/writing-rules/rule-syntax)).
- `semgrep --test` pairs a rule file with a target file of the same name. Comments mark lines: `ruleid:` must match, `ok:` must not, and `todoruleid:` and `todook:` record known gaps without failing the run ([testing rules](https://docs.semgrep.dev/writing-rules/testing-rules)).
- **Borrow:** `include` and `exclude` for applicability; tests paired to the rule by name; `todo` markers, so a known miss is recorded honestly instead of hidden.
- **Lacks:** patterns match code, not prose plans.

### OPA: `opa test` and METADATA

- Tests are Rego rules named `test_…`; `with` replaces `input`, `data` or functions; `--coverage` reports uncovered lines; `--fail-on-empty` fails a run where no test executes ([policy testing](https://www.openpolicyagent.org/docs/policy-testing)).
- METADATA annotations give `title`, `description`, `related_resources`, `scope`, `custom` and more, readable with `rego.metadata.rule()` or `opa inspect -a` ([annotations](https://www.openpolicyagent.org/docs/policy-language#annotations)).
- **Borrow:** fail on empty, so a unit with no tests, or a selector that selects nothing, can't pass silently; `related_resources` as the link back to the ADR; tests that substitute inputs, which here are fixture artefacts.
- **Lacks:** a policy evaluates structured input. Plans are prose, so judgement rules don't fit Rego.

### adrkit

From its README ([github.com/mbeacom/adrkit](https://github.com/mbeacom/adrkit)), Apache-2.0, pre-1.0, `v0.20.0` named as the current pin for its GitHub Action:

- **`affects`:** a front-matter list of typed entries, `type: path` with a glob or `type: package` with a version range. "Match resolution is a pure function."
- **`@adr` markers:** a comment such as `@adr 0012` in any source file opts that code in; `adr explain` reports it as "declared by" a file and line.
- **Selection:** `adr explain <path>` (with `--as-of`) and `adr check <files...>` list the accepted decisions governing files. A read-only MCP server offers `search_decisions`, `get_decision`, `get_decision_context(files[])` and `list_superseded`.
- **`adr evaluate`:** deterministic and model-free; it routes a *proposal* ADR through rubric rules and escalates to a named human. It doesn't check plans against decisions.
- **Spec Kit extension:** `/speckit.adrkit.context`, `.check` and `.draft`, with an `after_plan` hook. Pinned to Spec Kit `>=0.13.0,<1.2.0`. The README names a `decision-checker` agent that "reconciles a plan or diff against the corpus, one verdict per decision", without saying how.
- The README describes no tests or fixtures for individual decisions.
- **Borrow:** typed `affects`; markers as an opt-in beside globs; `--as-of`, which matches our versioned citations; a read-only MCP server as the delivery shape.
- **Lacks, for this problem:** the unit is a whole decision, not a constraint; selection is by files, which don't exist at plan time; no per-decision tests are described. Installing its extension would mean revising ADR-009 (C4), with a source review and a pinned version (C5).
- **What we add beyond it:** constraint-level units, applicability by stage and by terms in the artefacts, tests for every unit, and rubrics for judgement rules.

### Claude Code skills and path-scoped rules

- **Skills:** the description is always in context (description plus `when_to_use` truncated at 1,536 characters); the body loads when invoked. `paths` makes Claude load the skill "automatically only when working with files matching the patterns". `disable-model-invocation: true` keeps the description out of context and stops Claude invoking it ([skills](https://code.claude.com/docs/en/skills)).
- **Rules in `.claude/rules/`:** a rule without `paths` loads at launch; a path-scoped rule "loads when Claude uses the Read, Write, or Edit tool on a matching file" ([memory](https://code.claude.com/docs/en/memory)).
- **Borrow:** progressive loading; path triggers for the "known area" route, once code exists.
- **Lacks:** without `paths`, loading is the model's choice, which is the same failure as reading titles. With `paths`, every feature's plan lives at `specs/<feature>/plan.md`, so a path doesn't tell f8 from f1.

### MCP tool search, and hooks that call MCP tools

- **Tool search** is on by default: "Only tool names and server instructions load at session start", and definitions load when Claude searches ([MCP](https://code.claude.com/docs/en/mcp), "Scale with MCP tool search"). Whether to search is the model's choice.
- **Hooks** can call an MCP tool directly: `"type": "mcp_tool"` with `server`, `tool` and `input`, on events including `UserPromptSubmit`, `PreToolUse` and `PostToolUse`. A hook can return `additionalContext`, inserted as a system reminder, capped at 10,000 characters ([hooks](https://code.claude.com/docs/en/hooks)).
- **Borrow:** the index-then-fetch shape. A hook calling the server makes delivery deterministic, where tool search alone isn't.
- **Lacks:** nothing in tool search selects by the artefact's content.

### Spec Kit's own hook point before `analyze`

- Found by the review, not in the brief's list. `speckit-analyze` checks `.specify/extensions.yml` for entries under `hooks.before_analyze` and tells the agent it "MUST actually invoke the hook" before continuing ([SKILL.md](../../.claude/skills/speckit-analyze/SKILL.md), lines 24 to 56). The file doesn't exist in this repository.
- **Borrow:** the natural place for a step before `analyze`, inside Spec Kit's flow.
- **Lacks:** the hook is run by the agent following instructions, so it isn't strictly deterministic. Whether registering a hook counts as an extension under ADR-009@v2 C4 is open; ADR-009's enforcement entry for C4 says the file "registers hooks, not installs".

### Testing judgement rules: promptfoo `llm-rubric`

- A model grades output against a natural-language rubric and returns `pass`, `score` and `reason`; `not-llm-rubric` inverts it, which expresses an expected failure ([llm-rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/)).
- **Borrow:** a judgement unit carries a rubric plus fixtures expected to pass and to fail, graded several times and reported as rates (matching Andy's 2 Nov ruling on rates). Not proposed as a dependency.

## What the prior art says about the problem

1. **The rule systems examined pair a rule with its tests in one runner:** ESLint's `RuleTester`, `semgrep --test` and `opa test`. None of their docs requires tests, and adrkit describes none per decision. That supports the "tests" part of the unit.
2. **In the tools examined, applicability is declared, not inferred:** Semgrep by `paths`, adrkit by typed `affects` and markers, Claude Code by `paths`. Nothing found selects by the content of a prose plan. That part is ours to design, and it is the part f8 needs.
3. **Deterministic delivery needs something other than the model to trigger it:** a path match, a hook, or a step in the flow. Skills and tool search on their own leave the choice to the model.

## Recommendation

**Build, borrowing shapes; don't install adrkit.** A unit is a folder in `spikes/rule-units/units/`:

- `unit.yaml`: the citation (`ADR-016@v1 C10`, or `hard rule 4`), the rule text word for word, a link to its source, `kind` (`mechanical`, `judgement` or `bright-line`), and `applies` (stages; scope; `include` and `exclude` globs, after Semgrep; and `terms`, regular expressions over the artefacts' text, the plan-time trigger). The kinds take three of T6's four routes. The fourth, "applies to a known area", is the `include` globs, which matter only once code exists.
- `check.py` for a mechanical or bright-line unit, or `rubric.md` for a judgement unit.
- `tests/`: `pass/` and `fail/` fixtures, and `expected.yaml` naming the finding each failing fixture must raise. A `todo` list records known misses, after Semgrep.
- An `index.yaml` lists every unit's citation, kind and `applies`, generated from the units. It is the always-present part (criterion 7); bodies are read only when selected.

A small runner in Python (size not estimated): `select(artefacts, stage)` returns units, in a fixed order; `check(unit, artefacts)` returns findings; `test` runs every unit's fixtures and fails on empty, after OPA.

**Honest limit:** `terms` is keyword matching. It is deterministic, but its recall is only as good as the terms. Each unit's tests include a near miss, recorded as a `todo` where the unit doesn't catch it.

**The three units:**

| Unit | Kind | Check | Fixtures |
| --- | --- | --- | --- |
| ADR-016@v1 C10 | Mechanical | Plan stage: an artefact names a violation output format other than SARIF. Implement stage: a violations file is SARIF, judged by its `$schema` and `version` fields (no version is named in ADR-016; question 7) | f8 (fail); a SARIF variant of f8 (pass); a near miss that describes the format without naming it |
| ADR-015@v1 C2 | Judgement | Rubric, following C2's two conditions: where the plan splits automatically, all five rules must hold, and each must be checked deterministically. A plan that checks every rule but breaks one fails | f5 and f6 (fail); a compliant split plan (pass); a near miss that checks four of the five rules |
| Hard rule 4, "never copy eShop files into this repo" clause | Bright line | Plan stage: copying eShop files into this repository. Diff: a file outside `subject/` identical to one in a fake eShop tree kept in the unit's own fixtures, not under `subject/` | f4 (fail); a plan that reads eShop through the submodule (pass); a near miss that vendors one eShop file under another name |

f5 and f6 were already raised as CRITICAL in 6 of 6 runs, from ADR-015's title, so they test the rubric, not a gap the unit closes. Only the copy clause of hard rule 4 is covered; its other clauses (pinned, fork only, AI features off) are out of the spike. Hard rule 4 rather than hard rule 3, because the parallel track is building the acceptance-test hook for hard rule 3 (ADR-011@v1 C3).

## Questions for Andy

1. **Build or borrow.** Recommended: build, borrowing the shapes above. Alternative: review and install adrkit, which means revising ADR-009 and doesn't solve plan-time selection.
2. **Plan-time applicability.** Recommended: `terms` over artefact text, plus stage and scope, with recall measured and known misses recorded. Alternative: map impact-set domains to units (T7), which doesn't exist yet.
3. **What reaches `analyze` in the f8 re-run.** Recommended: the selected units' text (citation, rule word for word, and the check's description), not the deterministic check's findings. Passing findings would only test whether `analyze` repeats them; passing the unit tests whether loading it closes the gap, as the brief asks. The deterministic check is run on f8 separately and reported on its own.
4. **How the unit reaches `analyze`.** Recommended: the prompt tells the agent to read the selector's output file as well, with no change to the skill. This departs from the README's method ("read only what the skill tells it to"), and the results will say so. Alternatives: a `before_analyze` entry in `.specify/extensions.yml`, which is Spec Kit's own hook point but run by the agent and possibly an extension under ADR-009@v2 C4; or a `UserPromptSubmit` hook adding the units as `additionalContext`, closer to the MCP option but more to build now.
5. **What counts as a catch, and false alarms.** Recommended: a finding at any severity that names ADR-016@v1 C10 or SARIF, with severity reported separately; `analyze` makes constitution conflicts automatically CRITICAL, and a loaded ADR unit may come out as HIGH. Also recommended: run the selector on f1 to f9. Where it selects nothing, the earlier results stand, since the only change is a prompt line pointing at an empty file (a small confound, stated). Where it selects something unexpected, run that fixture three times as a false-alarm check.
6. **Judgement units: selected deterministically or by the model?** T6's "Rule units" paragraph and its four-routes table differ. Recommended for the spike: deterministic, by `terms`, so all three units are tested the same way; the four-routes table stays a proposal.
7. **SARIF version.** ADR-016@v1 C10 says only "SARIF". Recommended: the check accepts any `version` field naming SARIF and reports which, rather than fixing 2.1.0, which no ADR names.
8. **Where expectations and results live.** `tests/constitution/expected.md` is a protected path (2 Nov). Recommended: the spike keeps its own `expected.md` and `results.md` in `spikes/rule-units/`, and adds `spikes/` to the README's layout table.

