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
| **Step before `analyze`**: a script runs translate, select and check, then hands the rules file to `analyze` | Yes | **This is what the spike ran: 3 of 3** | Small, but not built yet. `python -m ruleunits rules-file` does alias translation and selection only; it doesn't call the constrained model translator or run any unit's check on a feature (checks run only on test cases) | Someone must run it. In this repository that means a hook or a wrapper, and the hook belongs to the controls track |
| **MCP server**: `get_rules(artefacts, stage)`, `check(unit, artefacts)`, `index()` | Only when called by a harness hook (`"type": "mcp_tool"`) or by the capability's orchestrator; tool search alone is model-triggered | Good, and it is the capability's own interface (A1, T4) | Medium | More to build and test; still needs the hook or orchestrator to call it |

## Recommendation

**Two stages, one core.**

1. **Now: a deterministic step before `analyze`,** built from the spike's parts: the constrained model translator with its validator, selection, the checks run against the feature, and the rules file. The spike has these parts but not the single step that joins them. Mechanical findings would be reported directly, and the rules file goes to `analyze` for judgement and explanation. In this repository the trigger would be a Claude Code hook. The hook is the controls track's area (ADR-011, D1) and `.claude/settings*.json` is a protected path, so this needs coordinating and Andy's approval, not a change from this spike.
2. **Later: the same core behind an MCP server,** called by a harness hook in Claude Code sessions and by the capability's orchestrator. That makes rule units the capability's interface for selection and checking, as A1 proposes, without changing the core.

Either stage would need the subject glossary (it holds eShop terms such as "eshop" and "ordering.domain") to come from the fork's contract, not the capability (ADR-001@v2 C1, C2).

**Not recommended:** a skill, or Spec Kit's `before_analyze` hook, as the trigger. Both leave the decision to the model.

## What the spike leaves open

- **Applicability needs conjunctions.** All five false selections by the best translator were ADR-011@v1 C3 matched on one term. Add `terms_all`, or action terms ("write", "edit"), and measure again.
- **The baseline matched recall on 17 small fixtures.** A harder set, with real plans from DEV-1 to DEV-3 and more ADRs, is needed before claiming selection gains (T6's planned spike).
- **Authoring cost.** Three units and four decoys took a glossary of nine terms. At 162 constraints, the glossary and units need a generator and a validator (Step 7 item 2), and probably model-drafted units reviewed by a person.
- **CUE** for applicability and fact records, if the Python shape holds up. That is a separate decision.
- **The glossary as a first-class artefact,** with its own ADR, if the spike earns it (Andy, 2 Nov: "glossary in the spike folder for now").
