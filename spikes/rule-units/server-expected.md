# Expected results: the joined step and its MCP server

Written 2 Nov 2026, before any of this code, after Andy's go-ahead: "make sure you add the step that joins the parts (MCP server called by a hook/orchestrator)". His choices for the build: the Anthropic API translator with an alias fallback, the MCP Python SDK in a spike venv, and a live hook run from a spike settings file that he runs himself. Behaviour test first, as ADR-012 requires. These expectations are not edited after a run; where a result differs, results are recorded beside them.

## What is built

- **`ruleunits/join.py`, the joined step.** One call takes a feature folder and a stage, and:
  1. translates the artefacts to glossary IDs with the constrained model (Claude Opus 5.5, structured output limited to the glossary's IDs), validates them against the glossary, and falls back to the alias translator if the model call fails, refuses or returns an ID the validator rejects; the reason is recorded;
  2. selects units deterministically (unchanged);
  3. runs the plan and analyze checks of the selected mechanical and bright-line units on the artefacts;
  4. returns one record (findings and measurements filled in), the rules text, and the hook's context text.
- **`ruleunits/server.py`, an MCP server over stdio** with three tools:
  - `rule_units_hook(skill, project_dir, hook_event_name)`: returns hook output JSON for a Claude Code `mcp_tool` hook;
  - `get_rules(feature_dir, stage)`: returns the record, for an orchestrator;
  - `index()`: returns the units' identity and applicability.
- **The feature folder is found as Spec Kit finds it:** `SPECIFY_FEATURE_DIRECTORY` first, then `feature_directory` in `.specify/feature.json`; a relative path is resolved under the project folder. The server only reads; it never writes `feature.json`.
- **`python -m ruleunits hook-files`** writes a settings file and an MCP config, with absolute paths, for the live run. Nothing under `.claude/` is edited.

Implement-stage checks (files and trees) are not joined: they need the change's files, which a hook before `analyze` doesn't have.

## Expectations, joined step (pytest, no network)

The model translator is tested with a fake client that returns recorded outputs from `runs/selection/raw/translator-run1.json`, so tests are deterministic and cost nothing.

| # | Case | Expected |
| --- | --- | --- |
| J1 | f8, alias forced | Terms include `violation-report`. Units are `adr-016-c10` and `hard-rule-4-copy`. One finding, rule ID `ADR-016@v1 C10`, naming CSV; none for hard rule 4. The record validates, with `translator` "alias" |
| J2 | f1, alias forced | Units are `hard-rule-4-copy` only. No findings |
| J3 | f4, alias forced | A finding for hard rule 4 (the plan copies subject files) |
| J4 | f8, model translator, replayed output | `translator` "model", no fallback; terms are the recorded ones; same units and finding as J1 |
| J5 | Model returns an ID not in the glossary | Falls back to alias; the fallback reason names the validator |
| J6 | Model client raises (no credentials, network) | Falls back to alias; the reason names the error type |
| J7 | Model stops with `refusal` | Falls back to alias; the reason says refusal |
| J8 | Any run | `measurements` holds the translator used, the fallback reason (or none) and a duration |
| J9 | Rules text | Carries each selected unit's citation and rule text; check findings are reported in their own section, labelled as results of deterministic checks |

## Expectations, hook contract (pytest)

| # | Case | Expected |
| --- | --- | --- |
| H1 | `speckit-analyze` on f8 | One JSON object: `hookSpecificOutput.hookEventName` is the event passed in, and `additionalContext` contains "ADR-016@v1 C10", the rule text and the finding's message, in at most 10,000 characters, written as statements, not instructions |
| H2 | A skill that isn't mapped (`speckit-specify`) | `{}`, so the hook does nothing |
| H3 | No feature folder can be found | Context saying no feature folder was found and no rules were selected, not silence |
| H4 | Resolution | `SPECIFY_FEATURE_DIRECTORY` wins over `feature.json`; a relative path resolves under the project folder; `feature.json` is unchanged after a call |
| H5 | `speckit-plan` | Stage `plan`; ADR-015@v1 C2 is selectable at plan as at analyze |

## Expectations, MCP server over stdio (pytest, real subprocess)

| # | Case | Expected |
| --- | --- | --- |
| M1 | `tools/list` | Exactly `get_rules`, `index`, `rule_units_hook` |
| M2 | `rule_units_hook` on f8, with the client in `legacy` (initialize handshake) and in `auto` mode | The text content parses as H1 in both modes |
| M3 | `get_rules` on f8 | A record that validates against `report.schema.json`, with J1's finding |
| M4 | `index` | Seven units |

## Expectations, live hook (Andy runs one session)

Run as written in `hook/README.md`: a Claude Code session started with the generated settings and MCP config, on a neutral copy of f8, asked to use the `speckit-analyze` skill.

| # | Expected | Confidence |
| --- | --- | --- |
| L1 | The hook fires once, before the skill runs, and the server's log records the call with skill `speckit-analyze` | Moderate. The docs don't name the Skill tool's input field; the settings assume `tool_input.skill`. If that is wrong, the log shows an empty skill and the hook returns `{}` |
| L2 | The session's context holds the rule-units reminder with ADR-016@v1 C10 | Follows from L1 |
| L3 | The `analyze` report raises a finding naming ADR-016@v1 C10 or SARIF | High, if L2 holds (3 of 3 in the spike) |
| L4 | No prompt text asks the model to read a rules file | By design: the hook replaces the spike's extra prompt line, which was a confound |

## What would count against this design

- L1 fails for a reason other than the field name: `mcp_tool` hooks don't reach a stdio server started from `--mcp-config`, or the hook output is ignored.
- L2 holds and L3 fails: the context arrives but `analyze` doesn't act on it.
- The joined step takes longer than the hook's timeout (600 s for `PreToolUse`), or adds more than about 30 s with the model translator.

## Dated note, 3 Nov 2026

M4's "Seven units" was the unit count on 2 Nov. Andy then asked for a separate ADR-016@v2 C17 unit ("add a separate C17 unit"), so `index` now lists eight. M4 is unchanged as a record; its test now expects eight, with a comment pointing here.
