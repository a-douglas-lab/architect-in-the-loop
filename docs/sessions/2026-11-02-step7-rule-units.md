# Step 7, item 1: rule-unit spike · 2 Nov 2026

Phase 1, Foundations. A session started from the Step 7 planning session, working in its own worktree (`claude/spike-rule-units-0fd90a`) beside the controls track (ADR-010@v1 C2). Brief: [2026-11-02-step7-brief.md](2026-11-02-step7-brief.md).

## Done

- **Prior art** ([prior-art.md](../../spikes/rule-units/prior-art.md)): ESLint, Semgrep, OPA, adrkit, Claude Code skills, rules, MCP tool search and hooks, promptfoo, Spec Kit's `before_analyze` hook, all checked against current docs. Review run 11: 1 High, 3 Medium, 11 Low ([card](../loops/cards/2026-11-02-rule-units-prior-art-review-run11.md)). Shown to Andy before building.
- **v2 after Andy's challenges:** CUE, BM25, ubiquitous language and SKOS added; selection, validation and reporting split into distinct, separately tested steps.
- **Spike built and run** ([results](../../spikes/rule-units/results.md)): a glossary, three units (ADR-016@v1 C10, ADR-015@v1 C2, hard rule 4's copy clause) and four decoys, 17 labelled fixtures, three translators against a title baseline, and the f8 re-run. Expectations committed first. Run card: [analyze with rule units, run 2](../loops/cards/2026-11-02-rule-units-analyze-run2.md).
- **Delivery recommendation** ([delivery.md](../../spikes/rule-units/delivery.md)).
- **Review run 12** on the whole spike: 2 High, 5 Medium, 9 Low, 5 nits, all fixed or answered ([card](../loops/cards/2026-11-02-rule-units-review-run12.md)).
- **Agentic DDD check** at Andy's request (agentic-ddd, Ben Johns's steward agents): neither offers a way to match text to glossary terms; borrowed the vocabulary lock, the anti-corruption layer for where subject and capability terms meet, and event triggers ([prior-art.md](../../spikes/rule-units/prior-art.md)).
- **The joined step and MCP server built** ([server-expected.md](../../spikes/rule-units/server-expected.md), committed first; [results](../../spikes/rule-units/results.md)): 52 tests pass, including the server over stdio and the generated hook config with a simulated hook payload (Claude Code not in the loop). Run card: [MCP server, run 3](../loops/cards/2026-11-02-rule-units-server-run3.md).
- **Review run 13** on the rulings and the build: 0 High, 3 Medium, 7 Low, 4 nits; all fixed but one nit in a pre-registered file ([card](../loops/cards/2026-11-02-rule-units-review-run13.md)).

## Decided

- **Andy, 2 Nov:** "go ahead, glossary in the spike folder for now." This approved the reshaped spike: a glossary as the ubiquitous language, a translator to it as its own tested step, and selection, validation and reporting as distinct steps.
- **Andy, 2 Nov, after the run:** "deterministic judgement-unit selection approved, keep hard rule 4 always loaded, make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided." My reading, for Andy to confirm: one recommendation rather than "now a step, later a server", with the server built now. delivery.md is rewritten on that reading.
- **Andy, build choices:** the Anthropic API translator with an alias fallback; the MCP Python SDK in a spike venv; a live hook run from a spike settings file, which he runs.
- **Still not ruled,** applied as the author's choices: build rather than install adrkit; SARIF version, what counts as a catch, the f1 control, results kept in the spike folder.

## Found

- **f8 is caught in 3 of 3 runs** with its unit loaded (Run B: 0 of 3), all CRITICAL, with no ADR opened (self-reported). No CRITICAL on the f1 control.
- **The constrained model translator made no term errors** (31 of 31, three runs, the same sets each run). Its unit precision, 76%, missed the 85% prediction. Alias missed every paraphrase; BM25 matched almost everything.
- **A model reading ADR titles matched the best translator on unit recall** (16 of 16). It named ADR-016 for f8 every time when asked directly. So f8's miss in Run B was the unit never reaching `analyze`, not a failure to identify the ADR. The unit carried the constraint and its check's description; the spike can't separate the two. This was a pre-registered counter-indicator, and it fired.
- **Applicability by one term is too coarse** for some rules: every false selection by the best translator was ADR-011@v1 C3.

## Proposed

- **Delivery:** an MCP server that joins the parts, called by a harness hook or the capability's orchestrator; now built. Not a skill, and not Spec Kit's `before_analyze` hook, since both leave the trigger to the model.

## Open for next step

- Andy's live hook run ([hook/README.md](../../spikes/rule-units/hook/README.md)), which also tries the model translator against the real API.
- Andy's local review, before any push or PR.
- Which trigger runs the step in this repository: a Claude Code hook belongs to the controls track and touches protected paths.
- Conjunctions in `applies`; real DEV-1 to DEV-3 plans as fixtures; a second labeller.
- Whether the glossary becomes a first-class artefact with its own ADR.
