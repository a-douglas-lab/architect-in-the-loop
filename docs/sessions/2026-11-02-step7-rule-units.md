# Step 7, item 1: rule-unit spike · 2 Nov 2026

Phase 1, Foundations. A session started from the Step 7 planning session, working in its own worktree (`claude/spike-rule-units-0fd90a`) beside the controls track (ADR-010@v1 C2). Brief: [2026-11-02-step7-brief.md](2026-11-02-step7-brief.md).

## Done

- **Prior art** ([prior-art.md](../../spikes/rule-units/prior-art.md)): ESLint, Semgrep, OPA, adrkit, Claude Code skills, rules, MCP tool search and hooks, promptfoo, Spec Kit's `before_analyze` hook, all checked against current docs. Review run 11: 1 High, 3 Medium, 11 Low ([card](../loops/cards/2026-11-02-rule-units-prior-art-review-run11.md)). Shown to Andy before building.
- **v2 after Andy's challenges:** CUE, BM25, ubiquitous language and SKOS added; selection, validation and reporting split into distinct, separately tested steps.
- **Spike built and run** ([results](../../spikes/rule-units/results.md)): a glossary, three units (ADR-016@v1 C10, ADR-015@v1 C2, hard rule 4's copy clause) and four decoys, 17 labelled fixtures, three translators against a title baseline, and the f8 re-run. Expectations committed first. Run card: [analyze with rule units, run 2](../loops/cards/2026-11-02-rule-units-analyze-run2.md).
- **Delivery recommendation** ([delivery.md](../../spikes/rule-units/delivery.md)); decided by Andy on 2 Nov (below).
- **Review run 12** on the whole spike: 2 High, 5 Medium, 9 Low, 5 nits, all fixed or answered ([card](../loops/cards/2026-11-02-rule-units-review-run12.md)).
- **Agentic DDD check** at Andy's request (agentic-ddd, Ben Johns's steward agents): neither offers a way to match text to glossary terms; borrowed the vocabulary lock, the anti-corruption layer for where subject and capability terms meet, and event triggers ([prior-art.md](../../spikes/rule-units/prior-art.md)).
- **The joined step and MCP server built** ([server-expected.md](../../spikes/rule-units/server-expected.md), committed first; [results](../../spikes/rule-units/results.md)): 52 tests pass, including the server over stdio and the generated hook config with a simulated hook payload (Claude Code not in the loop). Run card: [MCP server, run 3](../loops/cards/2026-11-02-rule-units-server-run3.md).
- **Review run 13** on the rulings and the build: 0 High, 3 Medium, 7 Low, 4 nits; all fixed but one nit in a pre-registered file ([card](../loops/cards/2026-11-02-rule-units-review-run13.md)).
- **Live hook run** with Andy's API key, headless Claude Code ([results](../../spikes/rule-units/results.md), [card](../loops/cards/2026-11-02-rule-units-live-hook-run4.md)): run 1 failed on setup (project skills not loaded); in run 2 the hook fired before `speckit-analyze`, the server's API translator ran, and `analyze` raised ADR-016@v1 C10 as CRITICAL. Not blind; one run.
- **Review run 14** on the live run: 0 High, 2 Medium, 6 Low, 2 nits, all fixed ([card](../loops/cards/2026-11-02-rule-units-review-run14.md)).
- **Andy's T6 decision recorded** in backlog T6 (now Partly decided). Review run 15: 2 High, 3 Medium, 4 Low, 5 nits; all but two nits fixed ([card](../loops/cards/2026-11-02-rule-units-review-run15.md)).
- **Harness hook confirmed by Andy** and recorded. Review run 16: 0 High, 1 Medium, 1 Low, 2 nits, all fixed ([card](../loops/cards/2026-11-02-rule-units-review-run16.md)).
- **adrkit decision recorded** (build, borrow shapes, don't install). Review run 17: 0 High, 0 Medium, 3 Low, 1 nit, all fixed ([card](../loops/cards/2026-11-02-rule-units-review-run17.md)).
- **3 Nov: SARIF 2.1.0 decision recorded** (the author's, at Andy's request). Review run 18: 0 High, 3 Medium, 3 Low, 1 nit, all fixed ([card](../loops/cards/2026-11-03-rule-units-review-run18.md)).
- **3 Nov: SARIF 2.1.0 applied,** on Andy's "yes, do both.": ADR-016 v2 adds C17; the C10 unit reports other versions, cases written first ([card](../loops/cards/2026-11-03-rule-units-sarif-check-run5.md)). Review run 19: 0 High, 2 Medium, 4 Low, 2 nits, all fixed ([card](../loops/cards/2026-11-03-rule-units-review-run19.md)).

## Decided

- **Andy, 2 Nov:** "go ahead, glossary in the spike folder for now." This approved the reshaped spike: a glossary as the ubiquitous language, a translator to it as its own tested step, and selection, validation and reporting as distinct steps.
- **Andy, 2 Nov, after the run:** "deterministic judgement-unit selection approved, keep hard rule 4 always loaded, make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided." My reading: one recommendation rather than "now a step, later a server", with the server built now. delivery.md was rewritten on that reading.
- **Andy, 2 Nov, confirming:** "yes, one recommendation with the server built now. document the decision so we don't lose track of it later." Recorded as T6's Decided list in backlog.md, with T6 now Partly decided; the ADR is written when T6 closes. Delivery: an MCP server joining the parts, called by a hook or the orchestrator. That the hook is a harness hook, not a skill or `before_analyze`, was the author's reading.
- **Andy, 2 Nov, confirming the reading:** "yes, harness hook is right". Relabelled as decided in T6. The question put to him named the alternatives: not a skill or Spec Kit's `before_analyze` hook, since both leave the trigger to the model.
- **Andy, build choices:** the Anthropic API translator with an alias fallback; the MCP Python SDK in a spike venv; a live hook run from a spike settings file, which he runs.
- **Andy, 2 Nov, on adrkit:** "didn't you state adrkit didn't cover our requirements?" The author confirmed the prior art's three gaps and asked whether to record "build our own, borrowing adrkit's shapes; don't install it" as decided. Andy: "yes, record it as decided". Recorded in T6.
- **Andy, 3 Nov, on SARIF:** "you decide the sarif version". The author chose 2.1.0 for every producer of rule violations, recorded in T6 with its reasons. Andy approved applying it, 3 Nov: "yes, do both." ADR-016 v2 adds C17; the spike's C10 check reports other versions under C17. eShop's analysers would need a setting, which needs an approved spec.
- **Still not ruled,** applied as the author's choices: what counts as a catch, the f1 control, results kept in the spike folder.

## Found

- **f8 is caught in 3 of 3 runs** with its unit loaded (Run B: 0 of 3), all CRITICAL, with no ADR opened (self-reported). No CRITICAL on the f1 control.
- **The constrained model translator made no term errors** (31 of 31, three runs, the same sets each run). Its unit precision, 76%, missed the 85% prediction. Alias missed every paraphrase; BM25 matched almost everything.
- **A model reading ADR titles matched the best translator on unit recall** (16 of 16). It named ADR-016 for f8 every time when asked directly. So f8's miss in Run B was the unit never reaching `analyze`, not a failure to identify the ADR. The unit carried the constraint and its check's description; the spike can't separate the two. This was a pre-registered counter-indicator, and it fired.
- **Applicability by one term is too coarse** for some rules: every false selection by the best translator was ADR-011@v1 C3.

## Open for next step

- Hiding the server's `get_rules` and `index` from the model in a session; the live run showed it sees them.
- The API key: Andy reports he has deleted the file (2 Nov). It sat in a OneDrive-synced folder, so OneDrive's recycle bin or version history may still hold a copy; revoking the key in the Anthropic console would close that off.
- Andy's local review, before any push or PR.
- Which trigger runs the step in this repository: a Claude Code hook belongs to the controls track and touches protected paths.
- Conjunctions in `applies`; real DEV-1 to DEV-3 plans as fixtures; a second labeller.
- Whether the glossary becomes a first-class artefact with its own ADR.
