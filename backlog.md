# Backlog: open questions

> **Public version.** Evaluation outcomes, their labels, hidden examples and anything deliberately left in eShop for evaluation are held in the private evaluation repository. Where they were discussed, this file points there instead.

Status: v0.1 · 5 Oct 2026

Every item here is an unanswered question. Nothing is cloned or coded until the items marked **Gate** are closed. Each item closes with a short ADR recording the decision, the options considered and the evidence. Items carried over from the original capabilities document keep their old ID in brackets.

**How each item is researched.** Every item follows the same method before it closes: state the problem and the criteria; list the options, including the naive one (an LLM with everything in its prompt) and "do nothing"; run a short spike where claims need evidence; then decide and record an ADR. Research depth follows value:

- **Differentiating items** (where the portfolio's originality lives: A1, A2, E2, T6, T7, T8, Q1's enforcement map, Q3's dependency map) get deep research, with measured spikes.
- **Commodity items** (for example accessibility checking or load testing) get a sensible default, checked in an hour or two, and an ADR that says so. Spending days choosing an accessibility checker adds nothing a reviewer will notice.

| Group | Items |
| --- | --- |
| Product | P1–P9 |
| Solution architecture | A1–A5 |
| Tools and methods | T1–T9 |
| Evaluation | E1–E5 |
| Quality enforcement | Q1–Q5 |
| Delivery | D1–D5 |

---

## Product

### P1. Names · Parked

**Parked (5 Oct):** not on the critical path, and the space is crowded. Use a neutral working name for the repo and revisit once the build shows what the product feels like. "Architect in the Loop" is kept as the title for the write-up.

What is the capability called? The persona name (architecture coordinator) describes a role, which is right for a persona. The capability's name must instead signal the value it brings, from the point of view of a target employer (early-stage CTO, Chief Architect, Head of Platform hiring).

Criteria:

- **Says the value, not the mechanism.** Faster change that stays architecturally sound, rather than "multi-agent orchestrator".
- **Understood in two seconds** by a screener who has never seen the repo.
- **Doesn't overclaim autonomy.** Humans approve at defined points, so "autonomous engineer" or "self-building system" would contradict the design.
- **Avoids AI hype vocabulary** that reads as trend-chasing.
- **Works in a CV line, a README title and spoken in an interview.**
- **Free to use:** no clash with an existing product, GitHub organisation or trademark (check before deciding).

Likely pattern: a short name plus a descriptive line that carries the meaning, for example "[Name]: from business outcome to governed, deployed change". Candidate directions and names to evaluate are in the 5 Oct discussion.

**Direction chosen (5 Oct):** outcome to production, as a short name plus a descriptive line.

**Shortlist and clash checks (5 Oct, web search only; repeat for GitHub organisation, domain and trademark before deciding):**

| Name | Meaning | Clash check |
| --- | --- | --- |
| **Plumbline** | A builder's tool for keeping work true to vertical: keeps fast change true to the architecture | No software development tool found; the name is used by unrelated businesses (services, ministries) |
| Throughline | The continuous thread from outcome to deployed change, which is also the traceability story | Risky: close to "Threadline", an AI engineering-context prototype from May 2026 |
| Keel | Keeps a fast boat stable | **Clash:** Keel (keel.sh) is an established open-source Kubernetes deployment automation operator |

Candidate line: *"Plumbline: from business outcome to governed, deployed change."*

**Update (5 Oct):** Plumbline dropped: risk of reading as a plumbing product. Wider shortlist reviewed; Andy's current candidates:

- **Software Factory.** Instantly understood. Concerns: a widely used generic term that can't be owned (US Department of Defense "software factories", Microsoft's 2004 "Software Factories" approach); "factory" suggests mass production of outputs, and "feature factory" is a well-known criticism of shipping outputs rather than outcomes, the opposite of this product's thesis.
- **Architect in the Loop.** Honest about human control and memorable for technical audiences. Concerns: an established framing rather than an ownable name (an InfoQ article describes architects working in, on and out of the loop with AI); and strictly, the design puts the architect *in* the loop only for higher-risk changes, *on* the loop for others.

**Loop-theme brainstorm (5 Oct):** Outcome Loop, Loopgate, On the Loop, Looped In, Decision Loop, Loopwright. Checks so far: "Loop" alone is crowded, including e-commerce apps on Shopify (returns and subscriptions), which matters because the subject system is e-commerce; no product named "Outcome Loop" found; "Loopwright" is taken by a small Android music app. Andy picked Outcome Loop for a full check.

**Outcome Loop: clash found (5 Oct).** "OutcomeLoop" is an open-source project (tinyopsstudio, July 2026, published on npm) in exactly this space: a deterministic controller that keeps a Codex coding session running until an external verifier passes. "Outcome loop" is also used as a concept by Superdense (an outcome loop and reward layer for coding agents) and Codesteward (outcome-based evaluation of merges). Not usable as the product name.

**Prior art from this check, worth reviewing:**

- *OutcomeLoop:* the agent can't write to protected paths, and protected files are fingerprinted, so it can't edit its own verifier. Relevant to E2 (hidden tests) and the G4 repair loop.
- *Superdense:* hypotheses recorded before an outcome is known, then measured. Relevant to P8.
- *Codesteward:* uses "steward" naming and learns from merge outcomes. Relevant to the stewardship context and A2.

**Prior art noted while searching:** AgentFlow CI, a hackathon project (2026) that takes a plain-English feature request through five agents to a pull request, with a human only at final approval. It confirms that "outcome to pull request" alone isn't distinctive; the differentiation is governance, measured results and pre-registration.

### P2. The evidence line · Closed

**Decided (5 Oct):** the evidence line is built on three facts:

1. **Hidden-test pass rate versus plain Claude Code** (the E4 baseline), on the ten held-out outcomes.
2. **Zero breaches of architecture decisions reaching main**, against the baseline's count.
3. **Negative outcomes stopped for the right reason** (conflict, decision gap, ambiguity).

Working shape: *"Turns business outcomes into governed, deployed changes. On 10 outcomes defined before the build, it passed [X]% of tests it never saw (plain Claude Code: [Y]%), with zero breaches of architecture decisions, and stopped correctly on all [N] it shouldn't complete."* Placeholders are filled only from the scored run.

Instrumented from the first commit: hidden and visible acceptance results per outcome and per run; ADR check results on every merge; escalation records with their reasons; the same measures for the baseline.

**Publication: decided after seeing results** (Andy's call, 5 Oct). **All-or-none rule adopted (5 Oct):** if results are published, all pre-registered measures are published; the choice is whether to publish, never which numbers. The development-set dry run gives an early read before the scored run, which reduces the risk of a surprise.

The six-second line agreed so far is "great ideas, well executed, perfect all-rounder". That is the conclusion we want a screener to reach, but a screener won't accept it as a claim. Which one or two concrete, checkable facts make them reach it on their own? For example: "10 merchant outcomes delivered across N domains, X% of architecture decisions enforced deterministically, zero breaches reaching main." The answer shapes which metrics we instrument from day one.

### P3. Boundary between capability and subject system · Gate

Is the capability generic, working over any system that supplies a domain catalogue and ADRs in a defined format, or built specifically for this e-commerce system?

- Generic is more impressive and closer to a real platform product, but costs more and risks never finishing.
- Specific is faster but reads as a one-off demo.
- A middle option: define generic interfaces (domain catalogue format, ADR format, event-schema registry) with this subject system as the first and only implementation.

**Decided (5 Oct):** generic over subject knowledge, specific to the stack.

- The capability reads a declared subject contract and holds no subject knowledge in its own code or prompts. A CI check enforces this by failing on subject-domain terms in the capability.
- It targets a .NET, Aspire, event-driven stack and says so. Stack-specific parts sit behind small adapters.
- eShop is the only fully built subject. Automated onboarding of new subjects is out of scope; the eShop contract is authored, or extracted with human review (see T8).
- **Stretch goal:** a tiny second subject in a different domain, run with two or three outcomes, to measure portability rather than assert it. At minimum, sketch its contract on paper to test that the contract isn't shaped like eShop.
- Open consequence: the model's general knowledge (for example, that loyalty points are a liability) can't be removed. E4's baseline must separate what governance adds from what the model already knows.

To record as an ADR.

### P4. State of the subject system before the capability runs · Gate

**Partly answered (5 Oct):** most outcomes will align with the domains eShop already has; at least one outcome will add a new domain to the system. Still open: which domains exist today (verify), which new domain(s) we add, and the baseline ADRs.

The capability needs a realistic system to reason over. Which domains, ADRs, integrations and event schemas must exist *before* any outcome is run?

- **Verified (5 Oct) from the repo's src folder:** Catalog.API, Basket.API, Ordering.API (with Ordering.Domain and Ordering.Infrastructure), Identity.API, Webhooks.API, OrderProcessor and PaymentProcessor, communicating through a RabbitMQ event bus, with a Blazor storefront (WebApp), a WebhookClient and a MAUI client app. Existing tests: Basket unit tests, Catalog and Ordering functional tests, Ordering unit tests, plus Playwright end-to-end tests. No loyalty, promotions, finance ledger, fraud, notifications or analytics domains.
- **Verified (5 Oct):** the repo targets .NET 10 (global.json SDK 10.0.302); the README's .NET 9 reference is stale. Last commit 1 Oct 2026, so it is actively maintained. Pin a commit.
- **Findings from reading the source (5 Oct), to confirm by running it:** there is no merchant-facing interface (the storefront has Cart, Catalog, Checkout, Item and User pages only). Security findings are recorded in the private evaluation repository.
- B2's loyalty example touches several domains that may not exist. Does the capability create new domains, or do we build them first by hand (or with plain agent help) as part of the subject system?
- Who writes the subject system's baseline ADRs, and how many are needed for the ADR story to be credible?
- eShop currently targets .NET 9. Check its maintenance activity and whether we pin it or upgrade it.

### P5. Interfaces: who states outcomes, and where merchants configure things

**P5a. Capability interface, decided (5 Oct):** merchants do not change the system. The architecture coordinator states outcomes, on behalf of merchant needs, through a web interface: a React frontend over a C# REST API. Open: how thin it can be (D1 cost), and what it shows at each human approval point (A1).

**P5b. Merchant configuration in the subject system, still open:** eShop has no merchant interface, so outcomes that depend on merchant-set values (for example thresholds or promotion periods) need somewhere for a merchant to set them. This is separate from P5a. Options: a minimal merchant back office built into the baseline subject system, or configuration through an API or settings. Decide before labelling E1.

### P6. Architect persona definition

**Name decided (5 Oct): architecture coordinator.** They state outcomes, resolve conflicts and make decisions the capability escalates. What exactly they approve and delegate is settled by A1's use-case walk-through.

### P8. Measuring the value of an outcome · Gate

Proposal (5 Oct): treat an outcome as more than shipped code. Shipping a feature is an output; the outcome is the change in behaviour it was meant to cause. If the capability is named around outcomes, an interviewer will reasonably ask how it knows an outcome was achieved.

Design to evaluate:

- **Each outcome carries a value hypothesis and a measure**, for example loyalty: "repeat purchase rate among members rises". The architecture coordinator states or approves it.
- **Instrumentation is part of the definition of done.** The capability adds the events, metrics and dashboard the measure needs, and a deterministic check confirms they are emitted.
- **The loop is open, not closed.** Measurements are reported to the architecture coordinator, who decides whether to iterate, keep or roll back. The capability never acts on its own metrics: that would make it autonomous and invite it to optimise the metric rather than the outcome.
- **No users, so no value claims.** Synthetic traffic can prove the measurement mechanism works end to end. It proves nothing about real value, and the repo should say so plainly.

Questions: how much of this is built versus designed and documented only; whether feature flags or experiment support belong in scope; and whether the hypothesis is part of the outcome input, alongside the visible examples.

### P9. Exemplar domain · Gate

Proposal (5 Oct): bring one existing domain into the preferred state first, with everything we expect of a well-governed domain: constitution and specs, ADRs with enforcement, build and CI checks, acceptance tests in the four-layer model, and instrumentation. Then apply development-set outcomes to it by hand (with Claude Code), as reference implementations.

What it gives us:

- **A dry run of the whole toolchain** (T1, Q1, Q2, D6) on a small scale, before the capability is built. Tooling decisions get evidence instead of opinion.
- **A template for new domains**, which any new-domain outcome must follow.
- **An exemplar the capability can learn conventions from**, as working code rather than prose.

**Decided (5 Oct):**

- **Exemplar domain: Ordering.** It is the most thorough (domain and infrastructure projects, domain events) and is touched by most outcomes.
- **Other domains stay as they are.** A part-modernised, part-legacy system is realistic, and whether the capability applies the exemplar's conventions to legacy domains becomes a test in itself.
- **Each domain has its own context, ADR scope and spec folder.** product.md and the constitution stay system-wide.

Still open:

- **Which projects make up the Ordering domain?** Findings from the source (5 Oct):
  - **OrderProcessor** is a background service that queries Ordering's own database directly (raw SQL on the orders table) to find submitted orders past their grace period, then publishes an event that Ordering.API handles. It shares Ordering's data and waits for Ordering.API to run its migrations. A shared database only makes sense inside one bounded context, so **it belongs to Ordering** as a separate deployable.
  - **PaymentProcessor** has no database and depends only on the event bus. It reacts to "stock confirmed", simulates a payment using a configuration flag, and publishes payment succeeded or failed. It is a stand-in for a payment gateway with a different reason to change, so **it is likely its own thin Payments context**. Refunds would belong there.
  - Order lifecycle: Submitted, then (after the grace period) AwaitingValidation, StockConfirmed, Paid, Shipped; Cancelled is allowed until Paid.
  - **Decided (5 Oct):** Ordering = Ordering.API, Ordering.Domain, Ordering.Infrastructure and OrderProcessor. Payments (PaymentProcessor) is its own context.
- **Development-set outcomes for Ordering:** chosen so they don't pre-solve any evaluation outcome; the overlap check is held privately. Agreed set: [development-outcomes.md](development-outcomes.md).
- **Some existing eShop behaviour is deliberately left unchanged for evaluation** (details private). Consequence: exemplar work must not change existing behaviour outside its approved specs; defects noticed are reported, not fixed.

Rules:

- **Only development-set outcomes go in the exemplar.** Applying any evaluation outcome there would hand the capability the answer.

### P7. Confirm non-goals

**Decided (5 Oct):** all accepted. No shopper-facing AI features, no multi-tenancy, no custom coding agent.

Note: eShop already includes optional AI features (catalogue semantic search with embeddings and a storefront chat), switched on through the AppHost and apparently off by default. **Decided (5 Oct):** keep them switched off; the README states they are eShop's, not ours (done in the README draft).

---

## Solution architecture

### A1. Overall solution architecture · Gate

**First-pass sketch (5 Oct):** [architecture-sketch.md](architecture-sketch.md). Aligned with Andy's mental model; proof is running use cases through it. Walkthrough 1 (same file) ran seven use cases: one passed, six exposed gaps (G1 to G7). All proposed changes accepted (5 Oct).
Walkthrough 2 ran the remaining E5 scenarios: seven further gaps (G8 to G14), all accepted (5 Oct).

The end-to-end design of the capability: its components and agent roles, how work flows from outcome to deployed change, where state lives, where humans approve, and how it reads the subject contract (P3). It pulls together decisions from T4 (agent orchestration), T6 (ADR strategy), T7 (impact analysis) and T8 (subject knowledge), so it closes after them, but its shape should be sketched early so those items are decided with the whole system in view.

Decided (5 Oct):

- **Orchestrator:** deterministic code; LLMs only as workers.
- **Failure handling:** retry, then a repair loop with a fixed retry limit, then escalate to the architecture coordinator.
- **Traceability through OpenTelemetry:** every step is a span; an outcome ID correlates everything; existing distributed-tracing concepts (trace context, span links, GenAI semantic conventions) are reused rather than invented.
- **Handoffs as typed contracts:** agents exchange schema-validated messages, as services do through an API, which makes them testable, loggable and versionable.

Questions to settle:

- **Roles come from strategic domain-driven design, not guesswork.** Two levels apply. The subject system's bounded contexts (catalogue, basket, ordering) shape the domain agents. The capability itself is also a domain (outcome intake, impact analysis, governance, planning, implementation, verification), and its own context map decides which roles exist and which are LLM-driven or deterministic.
- **Human approval points, found by walking a ladder of use cases:**
  1. Happy path within one domain.
  2. Simple extension: adding a field to an existing domain.
  3. Complex happy path across several domains.
  4. Adding a sub-domain to an existing capability.
  5. Adding a completely new domain: what that means for ADRs, contracts, ownership, and a new domain agent.
  6. Negative paths: ADR conflict, decision gap, ambiguous outcome.

  For each: what the capability does alone, where the architecture coordinator must decide, and what they see when they do.
- **Typed handoffs, limits:** a schema guarantees a message's shape, not the quality of the reasoning inside its text fields. Those fields still need the runtime grader. Decide how schemas are versioned and where they are validated.
- **Structure versus prose, proposed principle (5 Oct):** structure what the system acts on; keep prose for reasoning. Decisions, domain and ADR IDs, verdicts, references and confidence go in schema fields that deterministic checks and the orchestrator consume. The reasoning behind them stays as free text inside a rationale field, because forcing reasoning into rigid formats can reduce its quality. Likely mechanism: the agent reasons freely, then emits a schema-validated result. Confirm with a spike comparing structured and free-form impact analysis on the development set.
- **Long-running traces:** an outcome may wait hours or days for human approval. One trace spanning days is awkward to store and view. Likely option: a trace per stage, linked by span links and the outcome ID. Confirm in a spike.
- **Who resolves conflicts between domain agents:** the deterministic orchestrator can't, so this is the arbiter agent (T7) or the architecture coordinator.
- **Implementation flow:** domain agents plan; an implementer (a coding agent) builds from the plan.
- **Prior art to review:** agentheim, a domain-driven-design harness for Claude Code (an orchestrator that never writes code, strict worker return formats, a knowledge layer). Check what it already solves before designing our own.

### A3. Governing cross-cutting concerns · Gate

Proposal (5 Oct): at least one further capability (a context, with its own agent or agents) governs system-wide concerns: integration patterns, logging and observability, authentication and authorisation, and similar.

eShop already has the code for this: shared projects such as ServiceDefaults (authentication, telemetry, health checks), the event bus, and the integration event log. Those projects would be owned by this context, as a platform team owns shared infrastructure.

**Decided (5 Oct): not a single agent.** One agent owning every cross-cutting concern would need too large a context and would become a bottleneck. Split by concern; the exact split is still open.

Questions to settle:

- **How to split?** A single cross-cutting agent risks becoming a catch-all that every outcome waits on. Splitting by concern (security, integration, observability) keeps each focused but adds coordination. In Team Topologies terms: a platform team, enabling teams, or both?
- **When is it involved?** On every outcome, or only when impact analysis or a cross-cutting ADR pulls it in?
- **Overlap with ADR scoping.** Cross-cutting ADRs already add domains to the impact set (T6, T7). Avoid two mechanisms doing the same job: decide whether this context *owns* those ADRs and the shared code, while the ADR mechanism does the selection.
- **Authority.** Can it veto a domain agent's plan, or only advise, with the arbiter or architecture coordinator deciding?

### A4. When an outcome splits, and who decides · Closed

From G11 (accepted): an outcome can split so that unblocked work continues. Whether a split can be automatic depends on why it happens, so the scenarios come first.

**Decided (5 Oct):** the nine scenarios below are complete. **Deliver dark is adopted:** partial features ship behind feature flags, switched off, so splitting can be automatic and switching a flag on is the human decision. Feature flags use **OpenFeature** (see Q5). The five rules for an automatic split are accepted. With delivering dark, S1, S2 and S4 also split automatically; the human decision moves to switching the flag on. **A4 closed.**

**Split scenarios (proposed, 5 Oct):**

| # | Scenario | Example | What changes for the merchant | Proposed |
| --- | --- | --- | --- | --- |
| S1 | Decision gap blocks part of the outcome | A refund rule nobody has decided yet | They get less than they asked for | Coordinator approves |
| S2 | ADR conflict blocks part | Part of an outcome needs a synchronous call to another service | They get less than they asked for | Coordinator approves |
| S3 | One part is ambiguous, the rest is clear | Loyalty: earning rules clear, redemption unclear | Nothing yet; risk of rework if the answer changes the design | Automatic for parts that don't depend on the answer |
| S4 | One independent part fails and escalates (G8) | Webhook part done, storefront part failing | They may get a part that makes no sense alone | Coordinator approves, unless delivered dark (see below) |
| S5 | Delivered part depends on the blocked part | Storefront needs a contract the blocked domain hasn't agreed (G1) | n/a | Not splittable: the dependency graph forbids it |
| S6 | Planned staging of a large outcome | Loyalty: charter, scaffold, earning, then redemption | Nothing: all of it arrives, in steps | Approved once as part of the plan; each step then automatic |
| S7 | Improvement work over budget (Q4) | Refactoring beyond the touch-radius budget | Nothing | Automatic proposal of a follow-up outcome; the follow-up needs approval |
| S8 | Out-of-scope security defect (G10) | A gap found in code next to the change | Nothing directly | Automatic proposal of a remediation outcome; flagged immediately |
| S9 | Preparatory change needed first | A calculation an outcome depends on must be corrected first | Nothing, if behaviour-preserving | Automatic if structural; approval if it changes behaviour |

**Candidate rules for an automatic split**, all checked deterministically:

1. The delivered part passes its own subset of the visible acceptance examples.
2. Nothing in the delivered part depends on the blocked part (contract dependency graph, G1).
3. The split doesn't reduce what the outcome asked for. Any reduction in what the merchant gets needs a human.
4. The delivered part's risk rung is no higher than the original outcome's.
5. The system is left consistent: no half-built feature visible to users.

**Deliver dark (adopted).** A partial feature ships behind a feature flag, switched off. Splitting can then be automatic, because nothing changes for users; switching the flag on is the human decision. This turns S1, S2 and S4 from "approve the split" into "approve the release". Cost: a feature flag capability in the subject system (checked 5 Oct: eShop has no feature flag library today).

**Consequence for evaluation (E1):** for any outcome expected to split, its visible and hidden examples must be labelled by part, so the delivered part is scored on its examples and the blocked part on escalating correctly.

### A5. Rubric catalogue for graders · Gate · deep research

**Decided (8 Oct):** add a catalogue of rubrics for the runtime grader (A2), covering domain agents, implementers and the other judgement points found in the walkthroughs. **Runtime rubrics live in this public repo**, because they define quality for the capability, as visible examples do. **Evaluation rubrics live in the private evaluation repo**, so the capability can't tune itself to them. Draft the runtime rubrics in Phase 1, because they shape what each agent must output in its typed handoffs; calibrate them in Phase 5 against real outputs.

**Starting point: Claude Managed Agents "outcomes".** Anthropic's Managed Agents (beta) lets you define an outcome as a description plus a markdown rubric; the harness provisions a grader in a separate context window, which returns per-criterion feedback, and the agent iterates until the rubric is satisfied or an iteration limit is reached (default 3, maximum 20). Sources: [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes), [cookbook: verify with an outcome grader](https://platform.claude.com/cookbook/managed-agents-cma-verify-with-outcome-grader). What to borrow:

| Outcomes concept | How it maps here |
| --- | --- |
| Rubric as a markdown document of explicit, independently gradeable criteria ("the CSV has a numeric price column", not "the data looks good") | The rubric format below; vague criteria are rejected in review |
| Grader in a separate context window, not influenced by the agent's implementation choices | A2 independence: grader sees the artefact, rubric and outcome statement, never the producer's reasoning |
| Per-criterion explanation fed back to the agent | Criterion IDs feed the repair loop, as ADR IDs and analyzer rule IDs do |
| Results: `satisfied`, `needs_revision`, `max_iterations_reached`, `failed` (rubric doesn't apply), `interrupted` | `needs_revision` → repair loop; `max_iterations_reached` → escalate with evidence (G8); `failed` → failure triage, probably a wrong rubric or a misrouted artefact (G8) |
| Iteration limit per outcome | Hierarchical budgets (G8) |
| Tip: write rubrics by having Claude analyse a known-good artefact | Derive first drafts from the Ordering exemplar's outputs for D1 to D3 |

Option to evaluate in the T4 spike: use the hosted feature itself versus adopting the pattern in our own grader. Points against the hosted feature: it is beta; it runs in Anthropic's sandbox rather than alongside Claude Code; it uses the same model family as the producer, which weakens A2's independence; and its grader reasoning is opaque, which conflicts with full traceability. Recommendation to test: adopt the pattern, implement our own grader, and use the hosted feature as a comparison baseline.

**Draft catalogue (runtime):**

| ID | Grades | Producer | When | On fail |
| --- | --- | --- | --- | --- |
| R1 | Impact set reasoning: each domain has a reason; non-obvious domains considered; nothing included without cause | Impact analysis | Before stewardship | Repair; escalate if the rung changes |
| R2 | Domain proposal: addresses the outcome within the context's boundary; cites the ADRs it relies on correctly; contract changes stated | Domain steward | Before governance | Repair |
| R3 | Intent preservation: after a repair, the proposal still delivers the outcome and its visible examples (G4) | Repair loop | After every repair | Escalate as an intent conflict |
| R4 | Arbiter ruling: applies recorded ADR precedence only; doesn't invent a decision (G5) | Arbiter | Every ruling | Convert to a decision gap |
| R5 | Domain charter: purpose, boundary, events, ownership and ADR scope coherent and consistent with the exemplar (G3) | Domain design role | Before coordinator approval | Repair, then coordinator |
| R6 | Spec: faithful to the approved proposal and outcome; acceptance criteria traceable to visible examples | Delivery (Spec Kit) | Before tasks | Repair |
| R7 | Implementation against plan: follows the plan; scope contained to the touch radius (Q4); design choices sensible. Excludes anything tests, analyzers or ADR checks already cover | Implementer (coding agent) | After deterministic checks pass | Repair; triage if the plan is at fault |
| R8 | Protocol driver honesty: thin, public interfaces only, no special-casing of examples (E2) | Implementer | Before acceptance tests run | Block |
| R9 | Trade-off explanation: clear to a non-technical reader; states what the merchant gets and doesn't | Steward or coordination | At approval points | Repair |
| R10 | Proposed ADR: decision, options and consequences stated; scope tags and precedence set (T2) | Governance | Decision gaps | Repair, then coordinator |
| R11 | Escalation record: stage, cause, attempts, options and evidence are clear enough to decide without re-investigating | Coordination | Every escalation | Repair |

**Rubric format (proposed, for Claude Code to refine with the ADR template):**

- Front matter: ID, version, artefact type, producer context, grader model tier, iteration limit, pass rule (for example all "must" criteria pass).
- Criteria: each with an ID, one checkable statement, a weight (must or should), a binary pass/fail by default (scales only where justified), and the evidence the grader must cite (a location in the artefact).
- **A deterministic test for every criterion during review:** if a schema, test or analyzer could check it, it moves out of the rubric (thesis; Q1).
- Anti-criteria for known failure modes, for example "passes by narrowing the outcome" in R3.
- Grader output as a typed message: per-criterion result, evidence, explanation, and an overall result using the statuses above. Rubric ID and version are trace attributes.

**Calibration (Phase 5):**

- Label set from exemplar and development-outcome outputs, plus **seeded flawed versions** (deliberately broken proposals, plans and drivers) to prove the grader catches what it should.
- Agreement with Andy's labels measured per rubric (for example Cohen's kappa), with a threshold set before the grader's verdicts are allowed to block.
- Re-run calibration whenever a rubric, model or prompt changes; a calibration drop blocks the change, like an eval regression.
- Report the grader's cost per outcome alongside its value (G8 budgets).

**Questions for the design session:**

1. Which rubrics are needed for the first thin slice? Likely R2, R3, R7 and R8.
2. Binary criteria only, or graded scales for some?
3. Which model tier grades, and is a different model family available and worth it?
4. Should agents see their runtime rubric while working? Proposed yes, because it defines quality as visible examples do; the evaluation rubrics stay hidden.
5. How rubrics are versioned and selected: per artefact type, with domain-specific additions from a domain's own folder?

### A2. Independent grader · part of A1

**Decided (5 Oct):** both graders, kept separate. Rubric catalogue in A5. A runtime grader checks work before a human sees it; an evaluation grader scores outcomes for E1 to E4. They use separate rubrics and are calibrated separately, and human labels remain the final check on the evaluation grader. The remaining questions below are about how, not whether.

Proposal (5 Oct): a grader role that reviews domain agents' recommendations against a rubric, independently of the agents that produced them.

Questions to settle:

- **Runtime gate, evaluation instrument, or both?** At runtime the grader checks work before a human sees it. In evaluation it scores outcomes for E1 to E4. Using the same grader for both is circular: if the capability is tuned to pass the grader, the grader's score no longer measures quality. If both roles exist, they need separate rubrics, separate calibration, or a human-labelled check on top.
- **Scope.** Under the thesis, the grader covers only what deterministic checks can't: for example, whether an impact set's reasoning is sound, whether a spec captures the outcome's intent, and whether trade-offs are explained clearly to a merchant. Anything a schema, test or constraint can check stays deterministic.
- **What it grades.** Candidates: impact sets, specs, plans, code changes, and plain-language explanations. Each needs its own rubric.
- **Independence.** The grader sees the artefacts and the rubric, not the producing agent's reasoning, so it judges the output rather than being persuaded by the argument. Options include a different model or model family to reduce self-preference bias.
- **Calibration.** Rubrics are versioned as code, and the grader's agreement with human labels (for example Cohen's kappa) is measured and published before its scores are trusted.
- **Consequences.** Does a low grade block, trigger a bounded repair loop, or only flag for the human reviewer? What is the loop limit?
- **Cost.** A grader adds model calls to every step it reviews. Decide where it earns its cost, for example only at human approval points.

---

## Tools and methods

The original document assumed Spec Kit, ADRs and CUE. These may no longer be the best choices for a capability that orchestrates existing coding agents. Each is reopened here.

### T1. Planning and specification tooling · Gate

**Decided (5 Oct): adopt the Spec Kit workflow** (constitution, specify, plan, tasks, implement) for building this project. Still open within T1: which presets and extensions to use (for example the brownfield bootstrap extension for eShop, and whether the Model Driven Engineering preset fits); whether the capability also produces Spec Kit artefacts for changes to the subject system (the second layer); and how ADRs and the constitution's ADR index connect to Spec Kit's constitution.

What drives specification and planning, and at which layer?

There are two layers: building the capability itself, and the capability producing specs for changes to the subject system. They may use the same tool or different ones.

Options to evaluate:

- Spec Kit (now at v1.0.x, with presets and extensions), including the community Model Driven Engineering preset, which already produces impact-driven change specs. If we use Spec Kit, we must state what we add beyond that preset.
- Spec Kit's brownfield bootstrap extension, since eShop is existing code.
- Alternatives: other spec-driven tools, or plain markdown specs plus Claude Code's own mechanisms (CLAUDE.md, skills, subagents, hooks).

Criteria: fit with orchestrating Claude Code, support for existing code, support for impact-scoped changes, how much it constrains us, and how well a reviewer will recognise it. Also note the published criticism that Spec Kit is spec-first but not spec-anchored over time; our design should answer it.

### T2. Decision records · Gate

ADR format (Nygard, MADR, or our own template with front matter for ID, status, scope, supersedes and enforcement links), where ADRs live, and how they are versioned. The template becomes ADR-000.

### T3. Deterministic constraint enforcement

Moved to Q1, which treats enforcement as a map of rule types to mechanisms rather than a single tool choice.

### T4. Orchestrating coding agents · Gate

Decided: orchestrate existing agents such as Claude Code rather than build our own. Still open:

- Mechanism: Claude Code headless mode, the Claude Agent SDK, or another harness.
- Shape: how many agents, what each does, how they hand off, where humans approve.
- Safety: sandboxing, least-privilege tokens, what agents can and cannot touch.
- Cost: budget per outcome and how it is enforced.

### T5. Language and stack for the capability itself · Gate

The subject system is .NET. Should the capability also be .NET? This is a real tension: the agent orchestration ecosystem (including the Claude Agent SDK) is strongest in TypeScript and Python, and writing the capability in .NET may mean fighting the grain. Options: all .NET; capability in TypeScript or Python with the subject in .NET; or a .NET capability that shells out to agent CLIs. Criteria: delivery speed, how it reads to your target employers, and fit with your CV story.

**Partly answered (5 Oct):** the capability's API is C# with a React frontend (P5a). Still open: whether agent orchestration also runs in .NET (driving Claude Code through its command-line interface) or in a small TypeScript or Python worker using the Claude Agent SDK, called from the C# API.

### T6. ADR strategy across the system [B1]

Carried over in full from the original document: how ADRs are stored, selected, referenced by agents and kept current, including the personas, nine use cases and evaluation criteria listed there. The progressive-disclosure approach remains a hypothesis. Depends on T1, T2 and T3.

### T7. From outcome to impacted domains [B2] · Gate · deep research

**Status (5 Oct):** central to the capability and likely the first thing an interviewer probes. The working proposal below is a hypothesis only. Research must start from prior art (how change impact analysis is done in industry and literature, software catalogues, dependency graphs) before evaluating our own design, and the chosen option is recorded in an ADR explaining why it beat the alternatives.

Carried over in full: how the capability identifies which domains an outcome touches, using the loyalty worked case. Options include a domain catalogue classified by an LLM, deterministic expansion through events, cross-cutting ADR rules, embeddings as a safety net and human confirmation. Depends on P4, because impact analysis needs the domains to exist.

**Proposed mental model (5 Oct):** a classifier or router identifies the impacted domains; each domain has a knowledge base (embeddings or similar, indexed by domain); queries are routed to domain agents backed by their domain's knowledge. How knowledge reaches each agent (whole-domain context, retrieval, or a mix) is to be determined.

Challenges to resolve in research:

- **The router is a single point of failure for recall.** A domain it misses is never consulted, so its ADRs are never applied. Compare against a broadcast option: every domain agent screens the outcome with a cheap model and claims or declines it. With around seven domains, broadcast may be affordable. Measure router, broadcast and a hybrid on recall, precision and cost.
- **Deterministic expansion still applies.** Domains that consume an affected event, or are added by a cross-cutting ADR, join the set regardless of what the router decides.
- **Why per-domain agents?** Decided rationale (5 Oct): domain agents are proxies for domain experts and engineering domain owners. Supporting reasons: context isolation, parallel work, and negotiating cross-domain contracts. Still test against a single agent with domain-scoped retrieval, and publish the ablation.
- **Retrieval may be unnecessary at eShop's size.** Each eShop domain may be small enough for its whole knowledge to fit in context with prompt caching. Decide from data: model each domain's knowledge (ADRs, contracts, code summaries, docs), measure its size in tokens today, and project it at larger scales (for example the 10, 50 and 200 ADR test in T6) to find where retrieval starts to pay off.
- **Who resolves disagreement between domain agents** when their proposals conflict? Two options: the orchestrator, or a separate arbiter agent. An arbiter fits model tiering: routing is a simple job for a small model, while resolving conflicts needs a larger context and stronger reasoning. Settle in A1.

### T9. Durable workflow engine · Gate

Outcomes wait hours or days at approval points (confirmed by walkthrough W3), so the deterministic orchestrator needs durable state that survives restarts. Options in .NET include Dapr Workflow, the Durable Task framework and Temporal's .NET SDK, or a hand-built state machine over a database. Criteria: durability, visibility of workflow state, testability, fit with OpenTelemetry tracing, and operational weight for a demo that is deployed only on demand.

### T8. Subject knowledge: sources, extraction and retrieval · Gate

Proposal (5 Oct): an ADR embedding pipeline as a generic mechanism for extracting project knowledge, usable for any subject.

Questions to settle:

- **Which knowledge, from which source?** The subject contract holds at least three kinds of knowledge: decisions (ADRs), structure (domains, APIs, events, dependencies) and domain facts (for example, that unredeemed points are a liability). ADRs hold only the first, and only where someone wrote one down.
- **Extraction versus retrieval.** Embeddings retrieve relevant passages; they don't produce a structured domain catalogue. Structure can be extracted deterministically from code and contracts (project references, OpenAPI documents, integration event types), which is generic per stack and exact.
- **Guaranteed versus likely.** Selecting the ADRs that bind a change must be guaranteed, which similarity search can't promise. Candidate role for embeddings: recall safety net alongside deterministic selection, and answering "has this been decided before?"
- **Where domain facts live.** Options: in ADRs, in the domain catalogue (for example a glossary or invariants section per domain), or left to the model's general knowledge. The choice affects E4.
- **Evaluation.** Recall of embedding-based selection versus deterministic selection against a hand-labelled set; extraction accuracy of the catalogue against a hand-written one.

Depends on T6 and T7; closes jointly with them.

---

## Evaluation

Success is defined before building. These items turn product.md's success criteria into something measurable.

### E1. The outcome set · Gate

**Decided (5 Oct):** ten held-out evaluation outcomes, used only for scored runs, plus a separate development set ([development-outcomes.md](development-outcomes.md)) for iterating during the build. Seven positive outcomes (one adding a new domain) and three negative (ADR conflict, decision gap, ambiguous request). The outcomes, their verification against eShop and their labels are held in the private evaluation repository and published with the results.

**Impact-set labelling, decided (5 Oct):** Andy writes the expected impact sets as part of the eval set; the capability runs the set and scoring is a deterministic comparison (recall and precision), with no LLM in the scoring. Refinements:

- **Two-tier labels (accepted 5 Oct).** *Must change*: domains the change must modify, written by hand at domain level, with acceptable alternatives recorded where more than one design is valid. (Earlier proposal to derive these from reference implementations dropped on 5 Oct; see the revised sequence in E2.) *Must consider*: domains that need checking but not changing (for example a domain whose ADR constrains the change), written by hand.
- **Second reviewer on a sample (optional, not yet decided)** (for example three of ten outcomes) by an experienced engineer, to show the labels aren't shaped by the same person's design of the system. Optional but adds credibility.
- **LLMs as disagreement detectors only.** Several models can label independently to flag outcomes worth a second look, never as the answer key.

**Impact set, defined:** for each outcome, the list of domains (and the contracts within them: APIs, events, data) that the change must modify or explicitly consider. It is an intermediate output of the capability (T7), scored for recall and precision against a label written before the run. It is not a measure of value; value measures such as time and human effort are covered in E3.

At least ten merchant outcomes. Still to decide:

- **Authoring.** Who writes them, and are expected impact sets labelled by a second reviewer to limit bias?
- **Spread.** A mix of difficulty: single-domain, multi-domain, and cross-cutting.
- **Negative cases.** Outcomes the capability should *not* simply complete: one that conflicts with an ADR, one with a decision gap, one that is ambiguous and should prompt a question. Without these, every case is a happy path and the evaluation proves little.
- **Held-out split.** Which outcomes are used during development and which are kept unseen until the final run, so the capability isn't tuned to the test.
- **Publication.** Outcomes and labels published in the repo for scrutiny.

### E1b. Validate outcomes and overlaps before starting · Closed

**Closed (5 Oct).** Every evaluation and development outcome was checked against the eShop source and against each other (overlap matrix), held privately. Public decisions from it: the storefront is its own context (a composition of the other domains plus the features that stitch them together); evaluation outcomes run independently, each from the same pinned baseline; business rules live in the owning domain (baseline ADR); times are stored in UTC and business time periods follow UK local time (Europe/London); development set D1 to D3.

### E2. Acceptance tests · Gate

**Decided (5 Oct):** layered acceptance, with a four-layer acceptance test model at its core (business-language test cases and DSL written by a human before the run; protocol drivers built by the capability; a deterministic check that drivers only use public APIs, events or the UI). Refinements, all accepted:

- **Acceptance tests first, as the definition of done (5 Oct).** Reference acceptance tests are written for every outcome before the capability is built. The visible examples, plus the E2 quality layers and ADR checks, form the definition of done the capability works to. Hidden examples are not part of the definition of done; they are used only for scoring.
- **Revised sequence (5 Oct), awaiting confirmation.** No reference implementations for evaluation outcomes. Per evaluation outcome: (1) write visible and hidden acceptance tests and labels; (2) confirm the tests fail against unmodified eShop; (3) pre-register everything; (4) run the baseline and the capability. Satisfiability is shown by any run passing a test; a test nothing passes is inspected by hand. (5) Mutation-test whichever implementations pass, and publish the score as a measure of test strength. A pre-registered rule governs defects found in tests after the run: a test is withdrawn only with a documented reason, and the withdrawal applies to the baseline and the capability alike.
- **Reference implementations only on the exemplar domain (P9)**, applied to development-set outcomes, to prove the test approach, the DSL and the D6 skill before any scored run.

- **Acceptance test-driven development at system level.** Every acceptance test must fail against unmodified eShop before the run (red), and pass after (green).
- **Visible and hidden examples.** Each outcome includes a few business-language examples the capability sees (specification by example), plus hidden examples it never sees, used to check it generalised rather than fitted to the visible ones.
- **Test the tests.** Mutation testing (for example Stryker.NET) on a reference implementation proves the tests catch real defects.
- **Pre-registration.** Hidden tests, labels and thresholds committed with a hash and timestamp before the scored run; kept in a private repo until then.
- **Quality layers beyond functional acceptance:** number of steps for a user to achieve the outcome, measured by journey scripts (HEART is not used, because it needs real users), accessibility, REST and API contract rules, breaking-change detection, API security, architecture rules, performance budgets and observability coverage.
- **Confirmation-bias controls:** the E4 baseline runs the same tests; a test that the baseline also passes isn't discriminating. Second reviewer on a sample of labels and tests.

Original question:

If coding agents write both the code and its tests, passing tests prove little. How is "the change works" judged independently?

Options to explore:

- Human-written executable acceptance tests per outcome, written before the capability runs (for example Gherkin with Reqnroll, or Playwright end-to-end tests, which eShop already uses).
- Hidden tests the agents never see, run only at evaluation.
- Contract tests at domain boundaries (API and event schemas).
- Property-based tests for business rules such as point balances never going negative.
- A rubric-graded LLM judge only for what can't be tested, such as the quality of plain-language trade-off explanations, calibrated against human labels.

Also decide: are acceptance tests part of the input a merchant or architect provides, or something the capability proposes and a human approves? That changes what the capability is.

### E5. Architecture design scenarios · Gate

An evaluation set for the capability's *architecture*, separate from E1's outcomes, which measure its results. Each scenario tests how the design behaves; walk through them on paper to shape A1 and A3, then turn them into executable scenario tests. Prior art: quality attribute scenarios from the Architecture Tradeoff Analysis Method (ATAM).

Candidate scenarios:

- A cross-cutting concern is part of the change set (for example, an outcome that needs a new authorisation scope).
- Two cross-cutting contexts disagree (for example, security wants synchronous token checks while integration requires asynchronous messaging).
- A domain agent's plan conflicts with a cross-cutting context.
- A cross-cutting ADR is superseded while an outcome is in flight.
- A new domain must adopt platform conventions (the loyalty outcome).
- A change to a legacy domain that doesn't follow the exemplar's conventions.
- An agent times out or returns invalid output, and retries are exhausted.

For each: expected behaviour, which role decides, and when the architecture coordinator is involved.

### E6. Running the private evaluation · Gate

Hidden tests and labels live in a separate private repository (D1). How is an evaluation triggered and run without exposing them?

Options to evaluate:

- **Manual trigger in the private repo:** a GitHub Actions workflow started by hand, given a commit of the public repo to evaluate. Simple, and nothing in the public repo can start it.
- **Triggered from the public repo:** a release or tag in the public repo sends a dispatch event to the private repo. Automatic, but the public repo then holds a credential that can start evaluations, so it must be scoped narrowly.

Either way: the workflow checks out the public repo at the given commit, runs the hidden tests against it, and stores results in the private repo. Agents in build sessions never hold credentials for the private repo. Development-set runs can be frequent; the scored held-out run happens once, at a pre-registered commit, and results follow the all-or-none rule (P2).

### E3. Success thresholds

What score on each measure in product.md (impact recall and precision, missed-ADR rate, acceptance pass rate, interventions, cost and time per outcome) counts as good enough? Thresholds set before the final run are credible; thresholds set after are not.

### E4. Baseline comparison · Gate

What are results compared against? The strongest evidence is an ablation: the same outcomes run through plain Claude Code with the ADRs simply placed in context, versus through the governed capability. If governance doesn't measurably beat that baseline, we need to know early.

---

## Quality enforcement

### Q1. Enforcement map: which mechanism enforces which kind of rule · Gate

No single tool covers every kind of rule. This item maps each rule type to a mechanism and checks the gaps.

| Rule type | Example | Candidate mechanisms | Notes |
| --- | --- | --- | --- |
| Code structure inside a service | Domain layer doesn't reference infrastructure | NetArchTest, ArchUnitNET | Works on compiled .NET code only. Blind to HTTP calls, events, data and anything before code exists |
| Service-to-service dependencies | Loyalty must not call Ordering synchronously | Aspire app model (service references declared in the AppHost), architecture tests on client types | An HTTP call built from a URL string is invisible to NetArchTest. The Aspire app model is a machine-readable dependency graph and may be the better check |
| Event and API contracts | Events carry an idempotency key | AsyncAPI or JSON Schema, Spectral for OpenAPI, OpenAPI diff for breaking changes | eShop already has a Spectral configuration |
| Proposals before code | Impact record lists every domain consuming an affected event | CUE, JSON Schema, OPA/Rego | Where CUE came from: the original document chose it to validate specs, impact records, agent messages and ADR front matter *before* code is written, and to detect conflicting ADRs because contradictory constraints fail to unify |
| Business policy | Refund within policy limit; price above margin floor | CUE, OPA/Rego, domain code with property-based tests | |
| Security | Users act only on their own orders | Authorisation tests, API security test suites | |
| Infrastructure and deployment | No public endpoints except the storefront | OPA/Rego, IaC policy tools | |
| Judgement residue | Trade-off explanation is clear to a merchant | Runtime and evaluation graders (A2) | Only what no deterministic check can cover |

Questions: does CUE earn its learning curve over JSON Schema plus OPA for the proposal and policy rows? Is NetArchTest or ArchUnitNET better maintained and more expressive today? Can the Aspire app model be checked reliably in tests? Output: the enforcement section of the ADR template (T2), plus the published "share of ADR clauses enforced deterministically" metric.

### Q2. Quality layer tooling

Choose a default tool for each E2 quality layer: journey step counts, accessibility, REST rules (stricter Spectral ruleset), breaking-change detection, API security, performance budgets and observability coverage. Commodity research: pick, check briefly, record.

### Q4. Improving legacy code a change touches · Gate

**Decided (5 Oct):** when a change touches a legacy domain, it should also improve the code it touches. The approach below is accepted, with these additions:

- **Measure with existing tools, not bespoke metrics.** Roslyn analyzers (.NET's built-in code quality rules, with severities versioned in .editorconfig), Microsoft's code metrics (complexity, maintainability, coupling), and SonarAnalyzer.CSharp (Sonar's rules as a NuGet package that runs in a normal build, so it works headlessly for agents and CI). SonarLint, now SonarQube for IDE, is IDE-only and can't analyse a whole project, so it suits Andy's own editing, not the pipeline. Coverage via coverlet; mutation score via Stryker.NET. Check the Sonar analyzer's licence before adopting.
- **One output format.** All tools report in SARIF (the standard static-analysis results format, which the .NET build can emit). The ratchet, the repair loop and GitHub code scanning then consume one format, and any tool can be swapped without changing the capability.
- **Rule IDs feed the repair loop**, as ADR IDs do: a violation names its rule, and the agent repairs against it.
- **Review burden is accepted for now** and measured over time. Making agents handle more on their own, so that review burden falls, is an improvement goal to iterate on, not a launch requirement.

Approach:

- **Scope by touch radius.** Improve only the code the change already modifies (files or methods in the diff), not the whole domain. Deterministic: computed from the diff.
- **Separate structural from behavioural change.** Improvements go in their own commits, which must not change behaviour: existing tests stay green before and after, and the mutation score doesn't fall. Prior art: Kent Beck's "Tidy First?" separation of structural and behavioural changes. This also keeps review manageable.
- **Budget, not target.** Cap improvement effort as a share of the outcome, for example structural diff relative to behavioural diff, or a share of the token budget. Lines changed is used only as a budget proxy, never as a measure of value, because it rewards churn. Thresholds pre-registered, like E3.
- **Measure value by what got better:**
  - Primary: the ratchet delta from G7, meaning violations of the exemplar's rules removed in the touched code.
  - Secondary: complexity of touched methods, test coverage and mutation score of touched code, coupling and duplication.
  - Prioritisation: hotspots (code that changes often and is complex), after Adam Tornhill's code-as-a-crime-scene approach, so effort goes where it pays back most.
- **Over budget becomes a follow-up.** Improvements beyond the budget are proposed as a separate improvement outcome for the architecture coordinator, rather than done inline.
- **Report review burden.** Improvements enlarge the diff a human reviews, so report the reviewable size of each change alongside the improvement it bought.
- **No outcome claims.** Fewer defects or faster future changes would need real history, which we won't have. The repo says so.

### Q5. Feature flags with OpenFeature · Gate

**Decided (5 Oct):** feature flags in the subject system use OpenFeature, the vendor-neutral feature flag standard, through its .NET SDK. OpenFeature is an API, not a flag store, so a provider must be chosen.

Questions to settle:

- **Provider.** Likely flagd, OpenFeature's own flag daemon, which reads flag definitions from files and has a .NET provider and an Aspire Community Toolkit integration. The provider package has been renamed (OpenFeature.Contrib.Providers.Flagd to OpenFeature.Providers.Flagd), and Aspire's documentation still shows the old name: confirm the current package and SDK versions when pinning. Alternatives: an in-memory provider for tests; a hosted flag service (unnecessary for a demo).
- **Ownership.** Feature flags are a cross-cutting concern (A3): which steward owns the flag conventions, and which ADR governs them?
- **Flag definitions as code.** Flags defined in versioned files, validated by schema, so the capability creates and changes them through the same governed path as code.
- **Consistency across services.** A partly delivered feature may span the storefront and Ordering; both must evaluate the same flag the same way (shared flag key, shared evaluation context such as the user).
- **Testing.** Acceptance tests run with the flag off (nothing visible changes) and on (the feature works). Decide whether both states are part of the definition of done.
- **Lifecycle.** Flags become debt if never removed. Give each flag an owner and an expiry, like exceptions (G12), and propose a removal outcome once it has been fully on for a set period.
- **Link to P8.** Flags also make it possible to measure an outcome's value hypothesis by comparing groups. Decide whether experiments are in scope or only on/off release.

### Q3. Validate the system dependency map · Gate

Impact analysis and service-dependency ADRs both rely on knowing which services depend on which. Where does that map come from, and how do we know it's right?

Candidate sources, each seeing only part of the picture:

- Aspire AppHost service references (declared intent).
- Configuration: appsettings service URLs and connection strings.
- Container definitions: Dockerfiles and compose files.
- Code: HTTP client registrations and event subscriptions (eShop registers subscriptions explicitly, for example in the storefront's startup extensions).
- Runtime: OpenTelemetry traces from a running system show the dependencies that actually happen.

Questions: which sources do we combine; how do we reconcile them; and can declared dependencies be compared with observed ones from traces, so drift between what the system says and what it does is detected automatically? Output: a validated dependency map consumed by T7 and Q1.

---

## Delivery

### D1. Speeding up development · Gate

**Decided (5 Oct):** points 1 to 3 below accepted; the private evaluation repo accepted, with how it is triggered and run still to design (E6). Andy works in the Claude Code desktop app, which runs parallel sessions, each in its own worktree. Token use is monitored, with a budget decided later. The Spec Kit workflow (T1) sits at the centre: skills and hooks support its stages rather than replacing them.

Original proposal. Principle: Andy's review attention is the bottleneck, not typing speed, so the setup is designed around review capacity.

- **Two or three parallel tracks, not five.** Track A: the critical path. Track B: research (prior-art reading, spikes). Optional track C: chores (documentation, tooling). Each runs as a named Claude Code session in its own git worktree, which Claude Code supports natively. Parallel sessions multiply token use, so set a budget.
- **Configure once, commit to the repo:** a CLAUDE.md pointing to the constitution and conventions; skills for writing an ADR from the template, running a research spike using the backlog method, and writing acceptance tests (D6); an adversarial reviewer subagent; hooks for deterministic gates (build, format and tests after edits; blocking writes to protected paths).
- **Build it the way the capability works (dogfooding).** Decisions become ADRs as backlog items close; deterministic checks gate every change; AI-authored work is marked in commits so the project's own delivery metrics (share of AI-authored changes, review time, change failure rate) can be published alongside the product's results.
- **Keep evaluation material out of reach.** Hidden tests and labels live in a separate private repository that is never cloned into a build worktree.
- **Daily loop:** pick from the roadmap, run the tracks, review at the gates, close backlog items as ADRs, publish progress.


Cost to plan for: E2's mutation testing needs a reference implementation for each positive outcome (seven), and these also supply the must-change impact labels (E1). Decide whether you write them, or Claude Code writes them under your review, separately from the capability.

Full-time effort plus Claude Code and Spec Kit will be faster than the original six-week estimate assumed, but agent speed produces more code to review, not less, and scope tends to grow to fill the time saved. Options to evaluate:

- Use existing tools wherever they cover a need (Spec Kit presets, agent SDKs, eShop as-is) and build only the differentiating parts.
- Parallel Claude Code sessions on separate git worktrees, each with a narrow task.
- Subagents, skills and hooks configured once and reused.
- Build the evaluation harness first, so every later change is measured automatically.
- Cut subject-system scope: fewer domains, done properly.
- Decide which components are fine as thin stubs (for example, the merchant interface) versus which must be deep.

### D2. Timebox and milestones · Closed

**Decided (5 Oct):** no hard deadline. Quality comes first; work continues beyond the nominal one-week date, and we see where we end up. Milestones are still defined by the evidence they produce, so each phase leaves something publishable. Sizing at the time: about five to seven weeks for the full scope.

What is the target date for something you can put in front of employers? Define milestones by evidence produced, not features, and decide what "good enough to apply with" means versus the full vision. Applying with an early milestone while continuing to build may serve the job search better than waiting.

### D3. Demonstration package

Carried over: public repo, short video of a recorded run, and a one-command deploy. Decide what the video shows (likely one outcome in depth plus the scoreboard across all ten) and its length.

### D4. Prior-work IP check

**Decided (5 Oct, revised):** we build the best engineering solution and do not avoid ideas because they overlap with previous work. Any overlap is flagged to Andy, who has the final say on whether and how it is used. The README carries no prior-work statement until Andy decides what it should say.

Original question: you've said nothing is off limits from an engineering view. The legal view may differ: designs or code created while employed (for example the Quality CLI, risk scoring and governance work) may belong to the employer under your contract. Rebuilding ideas from scratch is usually different from reusing material, but check your employment contracts or take advice before publishing anything derived from past work. I'm not a lawyer.

### D6. System-level acceptance test skill · Gate

**Decided (5 Oct):** Andy writes the reference acceptance tests with Claude Code, guided by a purpose-built skill. Search found generic test-driven development skills (unit-level red, green, refactor) but nothing for system-level acceptance tests in the four-layer model, so we build our own, using Anthropic's skill-creator and the existing TDD skills as reference. The skill is itself a portfolio artefact showing disciplined use of AI.

What the skill covers:

- **Business-language test cases** per outcome, in the four-layer model: test cases, DSL, protocol drivers, system under test.
- **Extending the DSL** as new outcomes need new steps.
- **A stub protocol driver**, so the tests compile and run before any implementation exists.
- **Splitting visible from hidden examples.** Visible examples go into the outcome request and are the definition of done. Hidden examples cover cases the outcome didn't spell out (edge cases, failure paths, interactions) and check that the capability understood the outcome rather than satisfying a checklist. This mirrors what a domain expert does, which is what domain agents stand in for.
- **Keeping hidden examples hidden:** they live in a separate private evaluation repo the capability can't access, and are published after the scored run.
- **Red first:** confirming every test fails against unmodified eShop.
- **Pre-registration:** committing tests and labels with a hash before the scored run.

**Reference implementations, revised (5 Oct):** none for the ten evaluation outcomes; the capability and the baseline produce those implementations, and building seven more by hand would double the work for little gain. Reference implementations exist only for development-set outcomes on the exemplar domain (P9), where they validate the test approach and this skill.

**Open (narrowed): who builds the exemplar's reference implementations.** Proposal from 5 Oct: an implementer, building from a domain agent's plan. Caution: if that plan comes from the capability's own domain agents, the reference is produced by the system under test. Its diff would then supply the must-change labels, so impact scoring would agree with the capability by construction. The reference implementations must also exist before the capability is built (E2 sequence). To decide: an independent plan and implementation, made by Andy with Claude Code in a separate session using this skill; or another arrangement that keeps the reference independent.

### D5. Rework the original document [B4]

Retire the sections written for earlier vehicle candidates (merchant ops agents, issue triage, incident investigation, Astronomy Shop hosting). Keep what carries over: own repo with upstream code pinned, deploy only on demand, replay for repeatable evals where relevant, and the video. Map the original in-product and SDLC capability tables onto the new two-part product, and drop rows with no natural home.
