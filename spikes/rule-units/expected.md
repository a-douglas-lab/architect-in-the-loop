# Expected results: rule-unit spike

Written 2026-11-02, before any translator, selector, check, rubric or `analyze` run, and committed before running. Never edited after a run: a wrong expectation gets a new dated entry below it (as in [tests/constitution/expected.md](../../tests/constitution/expected.md)). Results go in [results.md](results.md), as rates.

Labels for the selection comparison are in [labels.yaml](labels.yaml); per-unit expectations are in each unit's `tests/expected.yaml`. Both are author-written, so they are subjective; contested labels carry a reason.

## Method, fixed before running

**Fixtures.** f1 to f9 from `tests/constitution/fixtures/`, unchanged, and eight new ones in [fixtures/](fixtures/): paraphrased near misses, compliant variants and decoy bait. 17 in all.

**Translators** (artefacts → glossary term IDs, from [glossary/](glossary/)):

1. **Alias:** case-insensitive match of each alias on word boundaries.
2. **BM25:** each glossary term is a document made of its label and aliases; each sentence of the artefacts (split on line breaks and on `. `) is a query. Tokens are lower-cased words, with a crude stem (trailing `ing`, `ed`, `es`, `s` removed, in that order, keeping at least three letters), and these stopwords removed: a, an, the, of, to, in, on, off, for, and, or, by, is, it, its, as, at, be, with. k1 = 1.5, b = 0.75. A term is detected if any sentence scores 1.5 or more against it. With nine documents, one matching word that occurs in only one document scores about 1.9, so in practice the cut-off means "one distinctive word". The cut-off was chosen by that reasoning, not tuned.
3. **Constrained model:** a fresh subagent, given the glossary (IDs, definitions, aliases) and each fixture's three artefacts under a neutral name, returns term IDs only. A validator rejects any ID not in the glossary. Three runs, each covering all 17 fixtures in one context (a batch, so fixtures may influence each other; stated as a confound).

**Baseline: a model reading titles,** today's behaviour. A fresh subagent gets the constitution's ADR index (ID, title, scope) and each fixture, and lists the ADRs that apply. ADRs map to units by ADR: ADR-004 → adr-004-c3; ADR-011 → adr-011-c3; ADR-015 → adr-015-c2 and adr-015-c9; ADR-016 → adr-016-c10 and adr-016-c2. ADR-level selection can't tell constraints apart, and that is part of what is measured. Three runs, batched like translator 3.

**Selection:** deterministic. A unit is selected if the stage is in its `applies.stages` and any of its `applies.terms_any` was detected, or if `applies.always` is true. Stage `analyze` throughout. `hard-rule-4-copy` is always loaded and left out of scoring.

**Scoring.** Term level: recall and precision over (fixture, term) pairs against `labels.yaml`. Unit level: recall and precision over (fixture, unit) pairs, six scored units. Model runs: per-run figures and the range; stability is the share of fixtures with the same output in all three runs.

**Neutral copies** for every model run: fixtures copied to the scratchpad as `x01` to `x17` (order shuffled with a fixed seed), with the "(test fixture)" label removed. Agents are told not to read `tests/` or `spikes/`. Nothing enforces that. Prompts, the name mapping and raw outputs are committed under `runs/` this time, which the constitution tests' README names as a gap.

## Predictions: translate and select

Worked by hand from the alias lists before running.

| Translator | Term recall | Term precision | Unit recall | Unit precision |
| --- | --- | --- | --- | --- |
| Alias | 24 of 31 (77%) | 24 of 24 (100%) | 14 of 16 (88%) | 14 of 17 (82%) |
| BM25 | At least alias | Clearly below alias | At least alias | Below 70% |
| Constrained model | 90% or more | 85% or more | 15 or 16 of 16 | 85% or more |
| Baseline, titles | n/a | n/a | Below the constrained model | Below alias |

- **Alias, misses predicted:** subject-system in f1 and f2 ("subject contract"); acceptance-test in f5 and f6 ("acceptance ... checks"); violation-report in n1 ("objections"); outcome-split in n2 ("hold back a stuck piece"); file-copy in h4-port ("retyped"). At unit level, adr-016-c10 on n1 and adr-015-c2 on n2. **False selections predicted:** adr-011-c3 on f7 (a negated mention), s-compliant and s-four (acceptance examples run, not written).
- **BM25:** aliases contain common words ("test", "rule", "code", "part"), which will match unrelated sentences; that is the reason for predicting low precision.
- **Constrained model:** predicted to catch both paraphrases (n1, n2) and the hand port; its likeliest errors are negated mentions (f7, h4-read) and labels that could be argued.
- **Stability:** constrained model, same output on at least 15 of 17 fixtures across the three runs. Alias and BM25 are deterministic: identical on a second run, checked by a test.

## Predictions: validate

Per unit, in each `tests/expected.yaml`:

- **ADR-016@v1 C10, mechanical:** finding on f8 (CSV), n1 (spreadsheet), the CSV file and the non-SARIF JSON file; none on c10-sarif, f1 and the SARIF file, whose version is reported as 2.1.0. **Predicted miss (todo):** c10-unnamed, whose format is described but not named.
- **Hard rule 4, copy clause, bright line:** finding on f4 and on the byte-identical copy; none on h4-read, f1, f8 and the clean tree. **Predicted misses (todo):** h4-port (retyped by hand) and the copy with a renamed namespace.
- **ADR-015@v1 C2, judgement, graded three times:** fail on f5, f6 and s-four; pass on s-compliant; not-applicable on f1. Predicted in 3 of 3 runs each.

Every unit's test run must execute at least one case; a run that executes none fails (after OPA's `--fail-on-empty`).

## Predictions: report

Every run writes one record per fixture: translator, terms, selected units, findings and measurements. Violations take a SARIF-shaped form (`ruleId`, `level`, `message.text`, `locations`). A test validates every record against [report.schema.json](report.schema.json). The record is early evidence for Q2; it doesn't decide Q2.

## Predictions: the f8 re-run

**Setup.** A neutral copy of f8, as in Run B. The units come from the **alias** translator, fixed now so the expectation can't depend on which translator wins: adr-016-c10, and hard-rule-4-copy (always loaded). A script writes the selected units' text (citation, rule word for word, source, kind and the check's description; not the check's findings) to a file outside the feature folder. The prompt runs the real `speckit-analyze` skill and adds one line telling the agent to read that file as rules that apply to the feature. That line departs from the README's method ("read only what the skill tells it to"). Three runs, fresh contexts, on the model used for real work.

**Catch:** a finding at any severity that names ADR-016@v1 C10 or SARIF.

| Fixture | Run B | Expected now |
| --- | --- | --- |
| f8 with its units | Missed, 0 of 3 | Caught in 3 of 3. Severity not predicted firmly: likely HIGH, because `analyze` makes constitution conflicts automatically CRITICAL and a loaded unit isn't the constitution |
| f1 with its units (hard rule 4 only), false-alarm control | No CRITICAL, 3 of 3 (Run A) | No CRITICAL, and no finding naming hard rule 4, in 3 of 3 |

Only f1 is re-run as a control, because hard rule 4 is always loaded, so every fixture's input changes. That is a cost limit, stated.

## What would count against rule units

- The f8 re-run catches C10 in fewer than 2 of 3 runs, which would mean selection isn't the only gap.
- The control raises a false CRITICAL from the loaded unit.
- No translator beats the baseline on unit recall.
