# Delivery: how rule units should reach the agents

Status: recommendation for Andy · 2 Nov 2026 · from the spike's [results](results.md). Not decided; adopting any option closes part of T6 and needs an ADR.

## What the evidence says delivery must do

1. **Put the unit in front of the agent.** f8 went from 0 of 3 to 3 of 3 when the unit was loaded, with no ADR opened (self-reported). Asked directly, a model could name ADR-016 from its title every time. What `analyze` lacked was the constraint, though the rules file also carried the check's description, and the spike can't separate the two ([results.md](results.md)).
2. **Be triggered by something other than the model.** Andy's point about Spec Kit's `before_analyze` hook, confirmed by the docs; the docs show the same for skills without `paths` and for MCP tool search. All three leave the decision to run to the agent ([prior-art.md](prior-art.md)).
3. **Keep the probabilistic part narrow and validated.** The constrained model translator made no term errors in three runs, and its output is checked against the glossary. Selection, mechanical checks and reporting are deterministic.
4. **Run mechanical checks without the agent.** The C10 and hard rule 4 checks found the f8 and f4 breaches on their own, as test cases, in under a second. The agent is needed for judgement units and for explaining findings, not for detecting mechanical breaches.

## Options

| Option | Deterministic trigger? | Fits the evidence | Cost now | Against |
| --- | --- | --- | --- | --- |
| Skill | No: model-invoked, or `paths`, which can't tell features apart at plan time | Poor | Small | The failure mode it is meant to fix |
| Spec Kit `before_analyze` hook | No: the agent follows SKILL.md's instruction to run it | Partial | Small | Possibly an extension under ADR-009@v2 C4 |
| **Step before `analyze`**: a script runs translate, select and check, then hands the rules file to `analyze` | Yes | **This is what the spike ran: 3 of 3** | Small. Now built as `join.py`, the core the MCP server calls; on its own it still needs something to run it | Someone must run it. In this repository that means a hook or a wrapper, and the hook belongs to the controls track |
| **MCP server**: `get_rules(artefacts, stage)`, `check(unit, artefacts)`, `index()` | Only when called by a harness hook (`"type": "mcp_tool"`) or by the capability's orchestrator; tool search alone is model-triggered | Good, and it is the capability's own interface (A1, T4) | Medium | More to build and test; still needs the hook or orchestrator to call it |

## Recommendation

An earlier version split this into "now, a step before `analyze`" and "later, an MCP server". Andy, 2 Nov: "make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided." I read that as asking for one recommendation rather than stages, and for the server to be built now. That reading is mine and needs Andy's confirmation:

**An MCP server that joins the parts, called by a harness hook or by the capability's orchestrator, not by the model's choice.** One call translates the feature's artefacts, validates the terms, selects units, runs the mechanical and bright-line checks against the feature, and returns the selected units' text and any findings. A hook returns these to the session as `additionalContext`; the orchestrator would read the same result. That makes rule units the capability's interface for selection and checking, as A1 proposes.

In this repository, wiring the hook is the controls track's area (ADR-011@v1, D1), and `.claude/settings*.json` is a protected path. So the spike tests the hook's contract without editing settings, and the wiring needs Andy's approval.

**Built:** `ruleunits/join.py` (the joined step) and `ruleunits/server.py` (the MCP server, tools `rule_units_hook`, `get_rules` and `index`), with tests against [server-expected.md](server-expected.md). The server passes over stdio, and from the generated hook config with a simulated hook payload. **Live run, 2 Nov:** in a headless Claude Code session, the hook fired before `speckit-analyze`, the server called the API translator, and `analyze` raised C10 as CRITICAL; one run, not blind ([results.md](results.md)). The run also showed the model can see the server's other tools. "Not by the model's choice" is the intent, not yet a property: the server's `get_rules` and `index` tools are also offered to the model in a session, and nothing stops it calling them. Hiding them from the model (a permission deny rule, or a hook-only server) is part of the wiring.

The server would need the subject glossary (it holds eShop terms such as "eshop" and "ordering.domain") to come from the fork's contract, not the capability (ADR-001@v2 C1, C2).

**Not recommended:** a skill, or Spec Kit's `before_analyze` hook, as the trigger. Both leave the decision to the model.

## What the spike leaves open

- **Applicability needs conjunctions.** All five false selections by the best translator were ADR-011@v1 C3 matched on one term. Add `terms_all`, or action terms ("write", "edit"), and measure again.
- **The baseline matched recall on 17 small fixtures.** A harder set, with real plans from DEV-1 to DEV-3 and more ADRs, is needed before claiming selection gains (T6's planned spike).
- **Authoring cost.** Three units and four decoys took a glossary of nine terms. At 162 constraints, the glossary and units need a generator and a validator (Step 7 item 2), and probably model-drafted units reviewed by a person.
- **CUE** for applicability and fact records, if the Python shape holds up. That is a separate decision.
- **The glossary as a first-class artefact,** with its own ADR, if the spike earns it (Andy, 2 Nov: "glossary in the spike folder for now").
