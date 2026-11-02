# Rule units: problem, criteria and prior art

Status: v2 · 2 Nov 2026 · v1 reviewed by Andy; the v2 sections were written after his challenges and first reviewed in [run 12](../../docs/loops/cards/2026-11-02-rule-units-review-run12.md), not yet by Andy · Step 7, item 1 ([brief](../../docs/sessions/2026-11-02-step7-brief.md)); backlog T6, "Rule units"

Steps 1 and 2 of the discernment method (backlog D1): the problem, the criteria, and prior art. v1 was reviewed by the adversarial reviewer ([run 11](../../docs/loops/cards/2026-11-02-rule-units-prior-art-review-run11.md)), then by Andy, whose challenges reshaped the spike. v2 adds CUE, BM25, ubiquitous language and SKOS, and replaces v1's eight questions with the shape Andy approved and the choices still open to his ruling (see the end).

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

## Added after Andy's review (v2)

Andy's challenges, 2 Nov, quoted from chat: "Should CUE schema also be considered as part of the prior art capabilities?"; "if we're doing terms matching, this seems brittle, we'd likely need exact, near match etc. some BM25 like approach?. It feels like we need a compiler/translator to speak a consistent language."; "Feels like we need the concept of ubiquitous language/glossary as domain driven design establishes, to align everything."; "if we adopt the hook, we're relying on the LLM to run it aren't we?"; "we should run a set of tests to validate selection to see which works best, feels like we have selection, validation and reporting issues (which can be acted upon) a distinct process steps."; "i thought reporting in sarif didn't cover all aspects so we needed more than that?"

### CUE

- Types, constraints and values sit in one lattice; validating data means unifying it with a schema, and a conflict is an error. The result doesn't depend on the order of declarations or files ([the logic of CUE](https://cuelang.org/docs/concept/the-logic-of-cue/)). `cue vet` validates JSON, YAML, TOML and text files against CUE schemas, and is silent on success ([cue help vet](https://cuelang.org/docs/reference/command/cue-help-vet/)). That page documents no test runner.
- **Borrow:** selection as unification. A feature's fact record either satisfies a unit's applicability constraint or doesn't, decided by order-free merging, not by search. Also a candidate for checking structured outputs.
- **Lacks:** it reads structured data, not prose. It would be a new dependency, a Go binary. The spike writes the same idea in Python; adopting CUE would need its own decision.

### BM25 and lexical matching

- BM25 ranks documents by term frequency and rarity. It tolerates word order and repetition, but it ranks rather than decides, so it needs a cut-off, and it still works on words: "lint output" doesn't match "rule violations" unless both words are listed. (Standard information-retrieval method; not checked against a single source today.)
- **Borrow:** a cheap first pass, tested against the same labels as the other translators.
- **Lacks:** paraphrase. Andy's question, "do we need a different solution?", is answered by the translator below.

### Ubiquitous language (domain-driven design) and SKOS

- Domain-driven design's ubiquitous language is one vocabulary shared by people, documents and code within a bounded context (Evans; not re-checked today). Here it means one glossary that ADR constraints, unit applicability and the translator's output all use.
- W3C SKOS (a Recommendation, 18 Aug 2009) models such a vocabulary: `skos:prefLabel`, `skos:altLabel`, `skos:hiddenLabel` (labels kept for search, not display), `skos:definition`, `skos:broader` and `skos:narrower`, grouped in a `skos:ConceptScheme`; a resource has "no more than one value of `skos:prefLabel` per language tag" ([SKOS reference](https://www.w3.org/TR/skos-reference/)).
- **Borrow:** a term has one ID, one preferred label, a definition and aliases. The spike uses plain YAML in that shape, not RDF.
- **Bounded contexts are required here, not optional.** ADR-001@v2 C1: the capability's code and prompts "MUST NOT contain subject-domain knowledge"; C2: that knowledge comes from the subject's contract. So the spike keeps two glossaries: capability terms, and subject terms (standing in for the contract, which in the real system lives in the fork, ADR-003).

### Reporting

Andy ruled on 30 Oct that SARIF covers rule violations only, and measurement tools keep their native formats; how outputs reach the capability is open (Q2), with a proposed "small typed evidence record per change" (backlog Q2, Q4). Rubric scores, rates and translator accuracy are measurements, not violations. So the spike emits one typed record per run, with violations in a SARIF-shaped part. It is early evidence for Q2 and decides neither ADR-016 nor Q2.

### Hooks and determinism

Yes: Spec Kit's `before_analyze` hook is instructions in SKILL.md that the agent follows, so the agent decides whether it runs. Two separate questions:

- **Delivery:** does the unit reach the agent? Deterministic only if something outside the model does it: a harness hook, or a script that runs the selector and then starts `analyze`. In the capability, the orchestrator.
- **Use:** does the agent act on it? Always a model question. The f8 re-run measures this.

## The approved shape

Andy, 2 Nov: "go ahead, glossary in the spike folder for now."

Selection, validation and reporting are distinct steps, each tested on its own:

| Step | Job | Deterministic? | Measured by |
| --- | --- | --- | --- |
| Translate | Artefacts → glossary term IDs | Alias lookup and BM25: yes. Constrained model: no, but its output is validated against the glossary | Accuracy against labelled terms per fixture |
| Select | Terms and stage → units | Yes | Recall and precision against labelled units, compared with a model reading ADR titles (today's behaviour) |
| Validate | A unit's check or rubric → findings | Mechanical and bright line: yes. Judgement: no | Each unit's pass, fail and near-miss fixtures; rubric verdicts over three runs |
| Report | Findings and measurements → one typed record | Yes | A schema check on the record |

Then the f8 re-run: the selected units' text (not the check's findings) given to `analyze` by a script outside the model, three times, blind.

What Andy's challenges settled:

- **Plan-time applicability:** glossary terms from a tested translator, replacing v1's raw `terms` regular expressions (his challenge on brittleness, and the glossary he proposed).

What Andy has not ruled on. Each was applied in the spike as the author's choice, under "go ahead"; all but the first are stated in [expected.md](expected.md). It isn't clear that "go ahead" covered these, so each needs his ruling at review; overruling one would need a dated re-run:

- **Build, borrowing shapes; don't install adrkit** (v1 question 1).
- **Judgement units selected deterministically, like the others** (v1 question 6). T6's "Rule units" paragraph says units load deterministically; its four-routes table, a proposal, says judgement rules are selected by the model. The spike followed the paragraph. Andy's "we should run a set of tests to validate selection" asked for selection to be tested, not for this choice.
- **Hard rule 4 always loaded,** taken from the bright-line row of the same proposed four-routes table. This is a change from v1, which selected it by plan-stage `terms`. It shaped the f1 control: hard rule 4 was loaded on a feature that never mentions copying.
- **SARIF version, catch definition, false-alarm control and where results live** (v1's recommendations).

**Not ruled, so left out:** plans declaring their own glossary terms (it would change the plan template), and embeddings (a new dependency).

The three units are the same rules as in v1: ADR-016@v1 C10 (mechanical), ADR-015@v1 C2 (judgement, following both of its conditions), and the copy clause of hard rule 4 (bright line). Only how they are selected changed.
