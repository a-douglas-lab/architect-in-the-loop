# Results: rule-unit spike

Run on 2 Nov 2026, on Claude Opus 5.5, the model used for real work. Expectations were committed first in `ae25478` ([expected.md](expected.md)); the runner and deterministic scores followed in `289a9db`; every model run came after that. Expectations are left as written. Where a result differs, this file says so.

Raw material is committed under [runs/](runs/): prompts, the neutral-name mapping, each model's raw output, the scored JSON, the rules files and the full `analyze` reports.

## Headline

| Question | Result |
| --- | --- |
| Does loading f8's unit turn the miss into a catch? | **Yes, 3 of 3** (Run B: 0 of 3). All three raised a CRITICAL naming ADR-016@v1 C10 |
| Does the loaded unit cause false alarms on compliant work? | **No CRITICAL in 3 of 3** on f1. One run added a LOW, advisory row naming hard rule 4 |
| Which translator selects best? | **The constrained model**: 31 of 31 terms in each run, the same sets each run. Its unit precision, 76%, missed the prediction |
| Does any translator beat a model reading ADR titles on unit recall? | **No.** Both reached 16 of 16. A counter-indicator named in expected.md fired; see below |

## The f8 re-run

The units came from the alias translator: adr-016-c10, plus hard-rule-4-copy (always loaded). A script wrote their text to a file, and the prompt told `analyze` to read it. The rules files and reports are in [runs/analyze/](runs/analyze/).

| Run | CRITICALs | Names ADR-016@v1 C10 or SARIF | Severity of that finding | ADR files opened (self-reported) |
| --- | --- | --- | --- | --- |
| 1 | 2 | Yes | CRITICAL | None |
| 2 | 2 | Yes | CRITICAL | None |
| 3 | 2 | Yes | CRITICAL | None |

- **Catch rate: 3 of 3,** as predicted.
- **Severity: CRITICAL, not the HIGH I leaned towards.** Each run reasoned that Principle II ("Decisions Are Recorded and Honoured") makes an ADR MUST binding, so breaking a loaded constraint is a constitution conflict. My prediction was wrong.
- **The second CRITICAL in every run** was that the plan doesn't list ADR-016 or cite C10 (ADR-009@v2 C8, C13). Loading the unit made the omission visible.
- **No run reported opening an ADR.** The unit's text was enough. This supports the hypothesis that the gap was the constraint not reaching the agent.
- **Confound, the check description:** the rules file gave each unit's check description as well as its rule text, so `analyze` had a detection recipe, not just the constraint. See "The counter-indicator, read straight".
- **Confound, the prompt:** the prompt's extra line changes the method in [tests/constitution/README.md](../../tests/constitution/README.md) ("read only what the skill tells it to"). Run B had no such line, so the comparison is between "constitution only" and "constitution plus selected units", not a pure A/B on one variable.

**Control, f1 with hard rule 4 loaded:**

| Run | CRITICALs | Finding naming hard rule 4 |
| --- | --- | --- |
| 1 | 0 | None. The summary notes the rule was checked |
| 2 | 0 | One LOW row, R1: "No finding under the rule's check", suggesting the plan say explicitly that the contract is read in place |
| 3 | 0 | None. A table row records "No finding" |

No CRITICAL in 3 of 3, as predicted. The stricter expectation, "no finding naming hard rule 4", held in 2 of 3: run 2's LOW row names the rule while saying it isn't broken. It is advisory, not a false alarm, but it is noise the loaded unit caused.

## Selection

Scored against [labels.yaml](labels.yaml): 17 fixtures, 31 labelled terms, 16 labelled units (hard rule 4 excluded, as always loaded). Scores are in [runs/selection/](runs/selection/).

| Selector | Term recall | Term precision | Unit recall | Unit precision | Same output in all runs |
| --- | --- | --- | --- | --- | --- |
| Alias | 24 of 31 | 24 of 24 | 14 of 16 | 14 of 17 | Deterministic (checked) |
| BM25 | 30 of 31 | 30 of 92 | 16 of 16 | 16 of 62 | Deterministic (checked) |
| Constrained model, runs 1 to 3 | 31 of 31, each run | 31 of 31, each run | 16 of 16, each run | 16 of 21, each run | 17 of 17 fixtures |
| Baseline, titles, runs 1 to 3 | n/a | n/a | 16 of 16, each run | 16 of 21, 16 of 20, 16 of 22 | 14 of 17 (ADR sets); 15 of 17 (units) |

Against the predictions:

- **Alias:** exactly as worked out by hand. It missed the two paraphrases (n1's "objections", n2's "hold back a stuck piece"), f1 and f2's "subject contract", f5 and f6's "acceptance ... checks", and h4-port's "retyped". It falsely selected ADR-011@v1 C3 on f7, s-compliant and s-four.
- **BM25:** as predicted, full recall and very low precision. Alias words such as "test", "file" and "switched" match ordinary sentences. With nine short documents, one shared word passes the cut-off. BM25 isn't a useful translator here.
- **Constrained model, terms:** better than predicted (term recall 90% or more). It made no term errors in any run, including the paraphrases, negated mentions and the hand port. The prompt told it to count a concept "whether it is asserted or negated", which is the labels' own convention, so the negated mentions were helped by the prompt.
- **Constrained model, units: the prediction missed.** expected.md predicted unit precision of 85% or more; every run scored 16 of 21 (76%).
- **Its five unit errors are all the same one,** and the translation isn't the cause. ADR-011@v1 C3 (writes to acceptance tests blocked during implement) is selected whenever acceptance tests are mentioned, but those fixtures run acceptance examples or deny touching them. The labels say the concept is present but the rule isn't relevant. A single `terms_any` term is too coarse for this rule: it needs a conjunction, such as acceptance-test together with a "write or edit" term.
- **Baseline:** recall matched the constrained model, against the prediction ("below the constrained model"). Its false selections come from ADR granularity: choosing ADR-016 brings ADR-016@v1 C2, and ADR-011 was added for f3 and f9 in some runs. It chose ADR-016 for f8 in 3 of 3 runs. Its unit precision was 16 of 21, 16 of 20 and 16 of 22 (76%, 80%, 73%), below alias's 82% as predicted; run 1 equals the constrained model's precision.

### The counter-indicator, read straight

Expected.md lists "No translator beats the baseline on unit recall" as evidence against rule units. On this set, none did: both scored 16 of 16. So:

- **Selection by title wasn't what failed f8.** Asked directly which ADRs apply, a model picked ADR-016 every time. In Run B, `analyze` wasn't asked that, read no ADRs, and two of three runs only "suggested ADR-016 might apply". What changed the outcome was the unit reaching the agent. That was more than the constraint: the rules file also carried each check's description, which works as a detection recipe ("a finding if the artefacts … name an output format other than SARIF"), and runs 2 and 3 cite the check firing. This spike can't separate the constraint text from the recipe.
- **What the units add over the baseline,** on this evidence: constraint-level delivery (the baseline picks whole ADRs, so it would also need to open them, which `analyze` doesn't do); the same units every run (17 of 17 fixtures against the baseline's 15 of 17); and a selection that can be tested and replayed.
- **Limits:** 17 small fixtures written by the author, most of them stating their own intent; labels written by the author; one model family doing both the work and the selection. The baseline may do worse on long, real plans, or across many more ADRs, where titles carry less. That is untested.

## Validation

**Deterministic units**, run by `python -m pytest` in this folder: 27 passed, 3 expected failures. Of these, 16 are unit check cases (13 passed as expected, 3 predicted misses); the other 14 passed tests are 12 pipeline tests and 2 meta-tests. The expected failures are the three cases predicted as misses, and all three missed as predicted:

- ADR-016@v1 C10: c10-unnamed (format described, not named).
- Hard rule 4: h4-port (retyped by hand), and the copy with a renamed namespace (not byte-identical).

Each unit is shown blocking (findings on f8, n1, the CSV and non-SARIF JSON files, f4 and the byte-identical copy) as well as passing (c10-sarif, f1, the SARIF file at version 2.1.0, h4-read, f8 for hard rule 4, the clean tree). A test file with no cases fails (`EmptyRun`).

**Judgement unit, ADR-015@v1 C2,** graded three times ([runs/rubric/](runs/rubric/)):

| Fixture | Expected | Verdicts | Rules failed |
| --- | --- | --- | --- |
| f5 | fail | fail, fail, fail | All five, each run |
| f6 | fail | fail, fail, fail | All five, each run |
| s-four | fail | fail, fail, fail | Rule 4 (risk rung), each run |
| s-compliant | pass | pass, pass, pass | None |
| f1 | not-applicable | not-applicable ×3 | n/a |

15 of 15 verdicts as expected, with the same failing rules in every run. The rubric's rule 4 is introduced as word for word but leaves out ADR-015's sentence "Risk rungs are the use-case ladder in the architecture sketch, which is still a proposal (A1)". The rubric is left as run; a later version should restore the sentence. All five cases were graded in one context per run (a batch), which is a confound. f5 and f6 had already been caught from ADR-015's title in Run A, so they test the rubric, not a gap closed.

## Report

Every deterministic record validated against [report.schema.json](report.schema.json) (`runs/selection/alias.json`, `bm25.json`), but every one has `findings: []` and `measurements: {}`. So the SARIF-shaped violations part was never exercised with a real finding, against expected.md's prediction that records would carry findings and measurements. The validator is a hand-written subset of JSON Schema (type, required, properties, items, enum), since no schema library was installed. Records weren't generated for model runs or the `analyze` reports; their outputs are kept raw. The record's shape is early evidence for Q2, not a decision.

## Cost

Subagent totals as reported by the harness, including agent overhead.

| Run | Tokens per run | Time per run |
| --- | --- | --- |
| Constrained model translator, 17 fixtures | 64,400 to 64,700 | 35 to 48 s |
| Baseline, titles, 17 fixtures | 65,900 to 72,300 | 42 to 52 s |
| Rubric, 5 fixtures | 58,200 to 58,500 | 33 to 38 s |
| `analyze` on f8 with units | 65,900 to 66,700 | 57 to 68 s |
| `analyze` on f1 with units | 66,200 to 66,800 | 60 to 90 s |

Against Run B's `analyze` (about 62,000 to 64,000 tokens, 26 to 51 s), loading units added a few thousand tokens per run. Part of that is the extra file and part is the agents' longer reports, so the share due to the units isn't separable. About 980,000 tokens across the 15 model runs. The deterministic translators, selection and checks run in under a second.

## The joined step and its MCP server (added 2 Nov, after Andy's rulings)

Built after Andy asked for "the step that joins the parts (MCP server called by a hook/orchestrator)". Expectations and tests were committed first in `c7b89cb` ([server-expected.md](server-expected.md)); the code followed.

| Expectation | Result |
| --- | --- |
| J1 to J9, the joined step | All pass. J3 failed as first written, below |
| H1 to H5, the hook contract | All pass |
| M1 to M4, the server over stdio, real subprocess, `legacy` and `auto` client modes | All pass |
| The generated settings and MCP config, end to end (test written after the code) | Pass: the server started from the generated config outside the spike folder, called with the hook's input after `${...}` substitution from a sample `PreToolUse` payload, returned the C10 rule and finding, and logged the call |
| L1 to L4, the live hook in a Claude Code session | **All four held, in one unblind run,** L2 by inference, after a first run failed on setup. See "The live hook run" below |

pytest: 52 passed, 3 expected failures (the same three predicted misses). Five of the passing tests were written after the code: the generated config end to end; a failing client constructor (J6b), which is defensive, since anthropic 2.3.0 builds a client without credentials and fails at the request instead; and three cases of the 10,000-character limit, added after review run 13 found the shortening branch untested and able to exceed the limit (fixed).

**Misses and deviations:**

- **J3:** the test, as committed in `c7b89cb`, asked for exactly one hard rule 4 finding on f4. There are two, because f4 copies subject files in both spec.md and plan.md. The written expectation, "a finding for hard rule 4", holds, so the test was stricter than the expectation it encoded. I changed the test to match the expectation, with a comment that says so. That is an edit after a run, recorded here.
- **The model translator's tests use a fake client** with recorded outputs (J4 to J7). With no credentials, `auto` falls back to alias, and the record gives the reason: "Could not resolve authentication method". That fallback took about 3 s, mostly importing the SDK. The real API call was first made in the live run below.

**What this changes in the f8 method:** the hook puts the units into the session's context, so the spike's extra prompt line ("read this rules file"), which was a confound, isn't needed. The check descriptions are still in the context, so that confound remains.

### The live hook run

Run on 2 Nov 2026 by the author, not Andy as server-expected.md planned: Andy provided an API key in a file outside the repository, and Claude Code 2.1.316 was installed in a scratch folder and run headless (`claude -p`). Raw material is in [runs/live/](runs/live/): both transcripts, the hook log, the generated settings and MCP config, and the `analyze` report.

**Setup:** the prompt was exactly "Use the speckit-analyze skill on the current feature.", on Claude Opus 5.5, from the repository root, with the generated settings and MCP config (`--strict-mcp-config`). To keep the repository's broad local allow rules (`git push`, `gh pr`) out of an unattended session, the run loaded only user and project settings, offered only Skill, Read, Glob, Grep, Bash and PowerShell, allowed the prerequisites script as a shell command, and capped spend at $2. In practice the permission system also accepted two read-only `ls` commands and denied one Bash command (a variable it couldn't check); your user-level settings were loaded too, so any allow rules there applied. The command, with paths shortened:

```powershell
claude -p "Use the speckit-analyze skill on the current feature." --model claude-opus-5-5 --setting-sources "user,project" --settings live\settings.json --mcp-config live\mcp.json --strict-mcp-config --tools "Skill,Read,Glob,Grep,Bash,PowerShell" --allowedTools "Skill" "Read" "Glob" "Grep" "Bash(python .specify/scripts/python/check_prerequisites.py *)" "PowerShell(python .specify/scripts/python/check_prerequisites.py *)" --max-budget-usd 2 --no-session-persistence --output-format stream-json --verbose
```

The key was read from Andy's `.env` file into that process's environment only. `SPECIFY_FEATURE_DIRECTORY` pointed at the neutral copy, with `SPECIFY_FEATURE_NO_PERSIST=1`.

**Run 1 failed on setup** ($0.10; 14 s by the transcript's `duration_ms`). Loading only user settings also dropped the project's skills, so the Skill call returned "Unknown skill", and the hook didn't fire (no log file existed after it). Two facts came out of it: the Skill tool's input is `{"skill": "speckit-analyze"}`, which confirms the assumed `tool_input.skill`; and the model could see the server's `get_rules` tool and offered to call it, which is review run 13's point that the other tools aren't hidden. It also named "the rule-units hook on that tool (`rule_units_hook`)" although the hook never fired: it knew of the hook from the server's tool names, not from the hook's output.

**Run 2** ($0.19 for the session; 54 s by `duration_ms`; the translator's own API call isn't in the cost):

| # | Expected | Result |
| --- | --- | --- |
| L1 | Hook fires once, before the skill; log records `speckit-analyze` | **Held.** One log line: skill `speckit-analyze`, `PreToolUse`, context returned, 8.0 s |
| L2 | The context reaches the session | **Held, inferred.** The stream transcript doesn't carry `additionalContext` text (no match for its first line). The report quotes C10 word for word ("Tools that report rule violations MUST report in SARIF.") although the session never opened ADR-016 (the only ADR it read was ADR-001), says "The rule-unit server's deterministic check flagged the same thing", and names the other units the server selected |
| L3 | A finding naming ADR-016@v1 C10 or SARIF | **Held.** D1, CRITICAL, quoting C10. D2, CRITICAL, says the plan doesn't list ADR-016, as in all three spike runs |
| L4 | No prompt line asks the model to read a rules file | **Held.** The prompt was the single sentence above |

**The real translator differed from the recorded one.** The server's call to the API returned `acceptance-test`, `subject-system` and `violation-report` for f8; the labels, and the recorded spike run used in J4, have `violation-report` only. So ADR-011@v1 C3 was selected, and `analyze` judged it "not triggered". This is a different failure from the spike's: there, the translation was right and one-term applicability was too coarse (f7, s-compliant, s-four); here, the translator added `acceptance-test` (and `subject-system`), which the labels don't have. f8's spec has the template heading "Acceptance Scenarios", a likely cause, not confirmed. One call, with a different prompt layout and effort setting from the spike's subagent runs, so it says nothing about the translator's rate, only that it isn't the recorded output.

**Confounds:** not blind. The session ran in this worktree, whose folder name is "spike-rule-units-0fd90a", so every path it saw carried the spike's name: the working folder, the skill's folder, the constitution and the feature (in this session's scratch folder, whose name also contains it). The report said the feature "may be a fixture for the rule-unit spike". The hook's context names "the rule-unit MCP server", and the server's tool names are visible. A blind run needs a checkout whose path doesn't name the spike. One run only. CLAUDE.md was loaded, as in every earlier run. The check description is still in the context.

## SARIF version check (added 3 Nov)

Andy asked the author to choose the SARIF version ("you decide the sarif version"); the author chose 2.1.0 for every producer (backlog T6). Andy then approved applying it: "yes, do both." ADR-016 v2 adds C17, "SARIF reports of rule violations MUST use SARIF version 2.1.0"; C10 is unchanged.

Two cases were added to the C10 unit's `tests/expected.yaml` and committed first (`6774fb8`), failing against the old check: a SARIF 1.0.0 file shaped like Roslyn's default error log, and a file claiming a 2.2 draft version. Each expects a finding citing ADR-016@v2 C17. The test harness gained an optional `rule` field, because these findings cite a different constraint from the unit's own. The check now reports any SARIF version other than 2.1.0 under C17; the 2.1.0 file still passes. pytest: 54 passed, 3 expected failures (was 52 and 3).

Limits: the 1.0.0 file is hand-written to Roslyn's shape, not produced by Roslyn; the 2.2 file is invented, since no 2.2 schema was checked. The check reads only the `version` field, not the `$schema` URL. The analyze-stage check is unchanged: a plan naming "SARIF" without a version passes. The unit now checks two constraints but carries only C10's citation and text, so a C17 finding names a rule whose text the rules file and `get_rules` never give the agent; a separate C17 unit would close that. (Closed later on 3 Nov; see below.) The expected-results file's header allows a new dated entry for a wrong expectation; the two cases are new expectations, appended with a dated note, and no existing case changed.

**A separate C17 unit (later on 3 Nov).** Andy: "add a separate C17 unit". `units/adr-016-c17/` carries C17's citation and text, applies at plan, analyze and implement when the artefacts carry the glossary term `sarif`, and has its own nine cases, committed first (`aba7784`) and failing before its check existed. At plan and analyze it reports a SARIF version other than 2.1.0 named in the artefacts ("SARIF 1.0" is a finding; "SARIF v2.1" and SARIF with no version pass); at implement, a SARIF file whose `version` isn't 2.1.0. A version given in words is a predicted miss (todo). The C10 unit is back to C10 only: any SARIF version passes it. Its two C17 cases are kept, marked superseded with a dated note, and skipped; two new C10 cases expect the 1.0.0 and 2.2 files to pass C10. The test harness gained `superseded` (with its own test) and kept `rule`. M4's pre-registered "Seven units" gets a dated note in server-expected.md; the index now lists eight. pytest: 63 passed, 2 skipped, 4 expected failures.

Effect on the recorded selection results: none were re-run. With the labels' terms, the C17 unit is now also selected for c10-sarif, which the labels (written before C17 existed) don't list. The selection figures above were computed with seven units.

Limits of the C17 unit (from review run 20):

- **What "failing first" showed.** At `aba7784` every C17 case failed because `check.py` didn't exist, not on a mismatched result. The five "none" cases would pass a check that never reports anything, so they show the expectations came first, not that they separate a good check from a bad one; the four "finding" cases do.
- **M4's count never failed.** `index` reads the units folder, not index.yaml, so the M4 test with "eight" already passed at `aba7784`. The change to eight wasn't tested first and then fixed.
- **The plan-text pattern is narrow.** It reads "SARIF", optionally "v" or "version", then a dotted number. It misses "SARIF version 2", "SARIF: 1.0", "SARIF (2.2)", "SARIF2.1.0" and schema URLs such as `sarif-1.0.0.json`; only the version in words was predicted. It takes the first non-2.1.0 version, so "convert SARIF 1.0.0 to SARIF 2.1.0" is a false finding, and a pre-release "2.1.0-rtm.5" passes as 2.1.0. None of these has a case; they are recorded, not fixed.
- **ADR-016's Enforcement prose was out of date.** It said C17's check "is tested on three files", and its mechanism named only the version field of each file. The unit has nine cases, five of them on spec, plan and tasks text. Changing that prose needed a new ADR-016 version under ADR-000@v3 C8, which needed Andy; at first only the `ref` was changed. (Fixed later on 3 Nov: ADR-016 v3, a correction, on Andy's "yes, write v3". The unit still cites ADR-016@v2 C17, whose text v3 leaves unchanged. That follows the repo's practice, not a written rule: the C10 unit, index and glossary still cite ADR-016@v1 C10.)
- **The glossary's `sarif` definition still names only C10.** Still true, but the C17 unit now selects on that term. Left unchanged, since the definition is part of what the model translator reads.

`superseded` names that match no case, and duplicate case names, now stop the run (with a test). pytest after these fixes: 65 passed, 2 skipped, 4 expected failures.

## Against "what would count against rule units"

- f8 caught in fewer than 2 of 3: **no**, 3 of 3.
- A false CRITICAL from the loaded unit: **no.** One LOW advisory row.
- No translator beats the baseline on unit recall: **yes, it fired.** Read above: on this set the gain comes from delivering constraint text deterministically, not from better selection.
