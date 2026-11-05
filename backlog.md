# Backlog: open questions and decisions

> **Public version.** Evaluation outcomes, their labels, hidden examples and anything deliberately left in eShop for evaluation are held in the private evaluation repository. Where they were discussed, this file points there instead.

Status: v0.2 · updated 3 Nov 2026

Every open question and every decision so far, with its status. This file is the source of truth for what is decided. **Gate rule (8 Oct):** an item marked **Gate** must close before the [roadmap](roadmap.md) phase that depends on it starts. Each item closes with a short ADR recording the decision, the options considered and the evidence. Items carried over from the original capabilities document keep their old ID in brackets.

**Statuses.** Each item heading carries one status:

| Status | Meaning |
| --- | --- |
| **Open** | No decision yet |
| **Partly decided** | Some decisions made; what is still open is listed under "Open" |
| **Decided (ADR pending)** | Fully decided; the ADR is not yet written |
| **Closed (ADR-nnn)** | Decided and recorded in the named ADR |
| **Parked** | Deliberately deferred; the item says when to revisit |
| **Merged into X** | Handled by another item |

Two further markers may follow the status: **Gate** (see the rule above) and **Deep research** (see the method below).

**How each item is researched.** Every item follows the same method before it closes: state the problem and the criteria; list the options, including the naive one (an LLM with everything in its prompt) and "do nothing"; run a short spike where claims need evidence; then decide and record an ADR. Research depth follows value:

- **Differentiating items** (where the portfolio's originality lives: A1, A2, E2, T6, T7, T8, Q1's enforcement map, Q3's dependency map) get deep research, with measured spikes.
- **Commodity items** (for example accessibility checking or load testing) get a sensible default, checked in an hour or two, and an ADR that says so. Spending days choosing an accessibility checker adds nothing a reviewer will notice.

**IDs.** Backlog items use a group letter and number (P1, A1, T1, E1, Q1, D1). Development outcomes use DEV-1 to DEV-3 ([development-outcomes.md](docs/outcomes/development-outcomes.md)); walkthrough gaps use G1 to G14 ([architecture-sketch.md](docs/architecture/architecture-sketch.md)).

| Group | Items |
| --- | --- |
| Product | P1–P9 |
| Solution architecture | A1–A5 |
| Tools and methods | T1–T9 |
| Evaluation | E1–E6 |
| Quality enforcement | Q1–Q6 |
| Delivery | D1–D8 |

---

## Product

### P1. Names · Parked

**Parked (5 Oct):** not on the critical path, and the space is crowded. Revisit once the build shows what the product feels like. "Architect in the Loop" is the working title for the repo and the write-up (repo created as `architect-in-the-loop`, 8 Oct).

What is the capability called? The persona name (architecture coordinator) describes a role, which is right for a persona. The capability's name must instead signal the value it brings, from the point of view of a target employer (early-stage CTO, Chief Architect, Head of Platform hiring).

Criteria:

- **Says the value, not the mechanism.** Faster change that stays architecturally sound, rather than "multi-agent orchestrator".
- **Understood in two seconds** by a screener who has never seen the repo.
- **Doesn't overclaim autonomy.** Humans approve at defined points, so "autonomous engineer" or "self-building system" would contradict the design.
- **Avoids AI hype vocabulary** that reads as trend-chasing.
- **Works in a CV line, a README title and spoken in an interview.**
- **Free to use:** no clash with an existing product, GitHub organisation or trademark (check before deciding).

**Direction chosen (5 Oct):** outcome to production, as a short name plus a descriptive line, for example "[Name]: from business outcome to governed, deployed change".

**Names checked and rejected (5 Oct, web search only):**

| Name | Reason rejected |
| --- | --- |
| Plumbline | Risk of reading as a plumbing product |
| Throughline | Close to "Threadline", an AI engineering-context prototype from May 2026 |
| Keel | Keel (keel.sh) is an established open-source Kubernetes deployment operator |
| Outcome Loop | "OutcomeLoop" is an open-source project in exactly this space (tinyopsstudio, July 2026); "outcome loop" is also used by Superdense and Codesteward |
| Loopwright | Taken by a small Android music app |
| Software Factory | Generic and unownable; "factory" suggests output over outcome, the opposite of the thesis |

"Loop" alone is crowded, including e-commerce apps on Shopify. "Architect in the Loop" is an established framing rather than an ownable name, and strictly the design puts the architect *in* the loop only for higher-risk changes, *on* the loop for others. Any final candidate is checked for GitHub organisation, domain and trademark before deciding.

**Prior art found during the name search, worth reviewing:**

- *OutcomeLoop:* the agent can't write to protected paths, and protected files are fingerprinted, so it can't edit its own verifier. Relevant to E2 (hidden tests) and the G4 repair loop.
- *Superdense:* hypotheses recorded before an outcome is known, then measured. Relevant to P8.
- *Codesteward:* uses "steward" naming and learns from merge outcomes. Relevant to the stewardship context and A2.
- *AgentFlow CI:* a hackathon project (2026) that takes a plain-English feature request through five agents to a pull request, with a human only at final approval. It confirms that "outcome to pull request" alone isn't distinctive; the differentiation is governance, measured results and pre-registration.

### P2. The evidence line · Closed (ADR-006)

**Decided (5 Oct):** the evidence line is built on three facts:

1. **Hidden-test pass rate versus plain Claude Code** (the E4 baseline), on the ten held-out outcomes.
2. **Zero breaches of architecture decisions reaching main**, against the baseline's count.
3. **Negative outcomes stopped for the right reason** (conflict, decision gap, ambiguity).

Working shape: *"Turns business outcomes into governed, deployed changes. On 10 outcomes defined before the build, it passed [X]% of tests it never saw (plain Claude Code: [Y]%), with zero breaches of architecture decisions, and stopped correctly on all [N] it shouldn't complete."* Placeholders are filled only from the scored run.

Instrumented from the first commit: hidden and visible acceptance results per outcome and per run; ADR check results on every merge; escalation records with their reasons; the same measures for the baseline.

**Publication: decided after seeing results** (Andy's call, 5 Oct). **All-or-none rule (5 Oct):** if results are published, all pre-registered measures are published; the choice is whether to publish, never which numbers. The development-set dry run gives an early read before the scored run, which reduces the risk of a surprise.

**Decided (21 Oct, Andy), from review of ADR-006:** "instrumented from the first commit" means from the capability's first commit. The list of measures that all-or-none publication covers is pre-registered (E2).

### P3. Boundary between capability and subject system · Closed (ADR-001, ADR-003) · Gate

**Decided (5 Oct):** generic over subject knowledge, specific to the stack.

- The capability reads a declared subject contract and holds no subject knowledge in its own code or prompts. A CI check is to enforce this by failing on subject-domain terms in the capability (planned, ADR-001@v2 C1).
- It targets a .NET, Aspire, event-driven stack and says so. Stack-specific parts sit behind small adapters.
- eShop is the only fully built subject. Automated onboarding of new subjects is out of scope; the eShop contract is authored, or extracted with human review (see T8).
- **Subject-side artefacts live with the subject's code (8 Oct):** the subject contract, the subject's ADRs, per-domain spec folders and the development acceptance tests live in the eShop fork, not in this repo. The capability is given the contract's location and never hard-codes the subject's path. A real team keeps its decisions with its code, and keeping subject knowledge physically outside the capability's repo makes the "no subject knowledge in the capability" rule easy to check.
- **Stretch goal:** a tiny second subject in a different domain, run with two or three outcomes, to measure portability rather than assert it. At minimum, sketch its contract on paper to test that the contract isn't shaped like eShop.

Options considered: fully generic (more impressive, costs more, risks never finishing); fully specific (faster, reads as a one-off demo); generic interfaces with this subject as the only implementation (chosen, with the stack made explicit).

Consequence carried to E4: the model's general knowledge (for example, that loyalty points are a liability) can't be removed, so the baseline must separate what governance adds from what the model already knows.

### P4. State of the subject system before the capability runs · Partly decided · Gate

The capability needs a realistic system to reason over. Which domains, ADRs, integrations and event schemas must exist *before* any outcome is run?

**Decided (5 Oct):**

- Most outcomes align with the domains eShop already has; at least one evaluation outcome adds a new domain.
- **New domains are created by the capability, not built by hand beforehand.** Impact analysis returns "unowned capability", a domain design role drafts the charter, and the domain is scaffolded from the exemplar's template (G3, G13).
- **eShop is pinned, not upgraded:** upstream commit `dc7ea49` (`dc7ea499cd35…`, "Update to Aspire 13.6.0", 2 Oct 2026 UTC). Confirmed 8 Oct.
- **How it is included (8 Oct):** a fork, [a-douglas-lab/eShop](https://github.com/a-douglas-lab/eShop), with the upstream commit tagged `upstream-dc7ea49`, linked from this repo as a git submodule at `subject/eshop`. Our changes to eShop (exemplar, DEV-1 to DEV-3, baseline ADRs, feature flags, merchant configuration, and later the capability's own changes) are commits in the fork, never copies in this repo. Each commit here records exactly which subject commit it was built against. Options rejected: a fetch script with a manifest (pin not visible on GitHub, can drift without a check); an upstream submodule plus patch files (changes become patches, not reviewable code); copying eShop in (breaks the "used, not built" boundary).
- **Two baselines (8 Oct).** `upstream-dc7ea49` is where we started. The **evaluation baseline** is a later tag in the fork, frozen after our baseline work (Phases 2 and 4); evaluation outcomes run from it. Tags in the fork are immutable (repository ruleset).
- **Recorded (20 Oct):** the pin, the fork and submodule, and the two baselines are [ADR-002](docs/adr/ADR-002-subject-included-as-pinned-fork.md).

**Verified (5 Oct) from the source:**

- Projects: Catalog.API, Basket.API, Ordering.API (with Ordering.Domain and Ordering.Infrastructure), Identity.API, Webhooks.API, OrderProcessor and PaymentProcessor, communicating through a RabbitMQ event bus, with a Blazor storefront (WebApp), a WebhookClient and a MAUI client app.
- Existing tests: Basket unit tests, Catalog and Ordering functional tests, Ordering unit tests, plus Playwright end-to-end tests.
- No loyalty, promotions, finance ledger, fraud, notifications or analytics domains.
- Targets .NET 10 (global.json SDK 10.0.302); the README's .NET 9 reference is stale. Actively maintained (last commit 1 Oct 2026).
- No merchant-facing interface: the storefront has Cart, Catalog, Checkout, Item and User pages only (see P5b). To confirm by running it.
- Security findings are recorded in the private evaluation repository.

**Open:**

- Who writes the subject system's baseline ADRs, and how many are needed for the ADR story to be credible? (Roadmap Phase 2.)

### P5. Interfaces: who states outcomes, and where merchants configure things · Partly decided

**P5a. Capability interface, decided (5 Oct)** and recorded in [ADR-017](docs/adr/ADR-017-coordinator-interface.md): merchants do not change the system. The architecture coordinator states outcomes, on behalf of merchant needs, through a web interface: a React frontend over a C# REST API.

**P5b. Merchant configuration in the subject system:** eShop has no merchant interface, so outcomes that depend on merchant-set values (for example thresholds or promotion periods) need somewhere for a merchant to set them. This is separate from P5a.

**Open:**

- P5a: how thin the interface can be (D1 cost), and what it shows at each human approval point (A1).
- P5b: a minimal merchant back office built into the baseline subject system, or configuration through an API or settings. Decide before labelling E1.

### P6. Architect persona definition · Partly decided

**Decided (5 Oct):** the persona is called the **architecture coordinator**. They state outcomes, resolve conflicts and make the decisions the capability escalates.

**Open:** exactly what they approve and what is delegated. The use-case ladder in [architecture-sketch.md](docs/architecture/architecture-sketch.md) proposes the answer; it closes with A1.

### P7. Confirm non-goals · Closed (ADR-004)

**Decided (5 Oct):** no shopper-facing AI features, no multi-tenancy, no custom coding agent.

eShop's own optional AI features (catalogue semantic search with embeddings, and a storefront chat), switched on through the AppHost, **stay switched off**. The README states they are eShop's, not ours.

### P8. Measuring the value of an outcome · Open · Gate

Proposal (5 Oct): treat an outcome as more than shipped code. Shipping a feature is an output; the outcome is the change in behaviour it was meant to cause. If the capability is named around outcomes, an interviewer will reasonably ask how it knows an outcome was achieved.

Design to evaluate:

- **Each outcome carries a value hypothesis and a measure**, for example loyalty: "repeat purchase rate among members rises". The architecture coordinator states or approves it.
- **Instrumentation is part of the definition of done.** The capability adds the events, metrics and dashboard the measure needs, and a deterministic check confirms they are emitted.
- **The loop is open, not closed.** Measurements are reported to the architecture coordinator, who decides whether to iterate, keep or roll back. The capability never acts on its own metrics: that would make it autonomous and invite it to optimise the metric rather than the outcome.
- **No users, so no value claims.** Synthetic traffic can prove the measurement mechanism works end to end. It proves nothing about real value, and the repo should say so plainly.

**Open:** how much of this is built versus designed and documented only; whether experiments (comparing groups through Q5's flags) are in scope or only on/off release; and whether the hypothesis is part of the outcome input, alongside the visible examples.

### P9. Exemplar domain · Decided (ADR pending) · Gate

The exemplar approach is recorded in [ADR-005](docs/adr/ADR-005-ordering-exemplar.md).

**Decided, still to record as subject ADRs in the fork (Phase 2, ADR-000@v2 C12):** the projects that make up Ordering (including OrderProcessor); Payments as its own thin context; and "each domain has its own context, ADR scope and spec folder", with product.md and the constitution staying system-wide. P9 closes when these are written.

Bring one existing domain into the preferred state first, with everything we expect of a well-governed domain: constitution and specs, ADRs with enforcement, build and CI checks, acceptance tests in the four-layer model, and instrumentation. Then apply development outcomes to it by hand (with Claude Code), as reference implementations.

What it gives us:

- **A dry run of the whole toolchain** (T1, Q1, Q2, D6) on a small scale, before the capability is built. Tooling decisions get evidence instead of opinion.
- **A template for new domains**, which any new-domain outcome must follow (G13).
- **An exemplar the capability can learn conventions from**, as working code rather than prose.

**Decided (5 Oct):**

- **Exemplar domain: Ordering.** It is the most thorough (domain and infrastructure projects, domain events) and is touched by most outcomes.
- **Ordering = Ordering.API, Ordering.Domain, Ordering.Infrastructure and OrderProcessor.** OrderProcessor queries Ordering's own database directly (raw SQL on the orders table) and waits for Ordering.API's migrations; a shared database only makes sense inside one bounded context, so it belongs to Ordering as a separate deployable.
- **Payments (PaymentProcessor) is its own thin context.** It has no database, depends only on the event bus, reacts to "stock confirmed", simulates a payment and publishes success or failure. It stands in for a payment gateway with a different reason to change; refunds would belong there.
- **Other domains stay as they are.** A part-modernised, part-legacy system is realistic, and whether the capability applies the exemplar's conventions to legacy domains becomes a test in itself.
- **Each domain has its own context, ADR scope and spec folder.** product.md and the constitution stay system-wide.
- **Development outcomes: DEV-1 to DEV-3** ([development-outcomes.md](docs/outcomes/development-outcomes.md)), chosen so they don't pre-solve any evaluation outcome; the overlap check is held privately.

Reference: Ordering's order lifecycle is Submitted, then (after the grace period) AwaitingValidation, StockConfirmed, Paid, Shipped; Cancelled is allowed until Paid.

Rules:

- **Only development outcomes go in the exemplar.** Applying any evaluation outcome there would hand the capability the answer.
- **Some existing eShop behaviour is deliberately left unchanged for evaluation** (details private). Exemplar work must not change existing behaviour outside its approved specs; defects noticed are reported to Andy, not fixed.

---

## Solution architecture

### A1. Overall solution architecture · Partly decided · Gate

The end-to-end design of the capability: its components and agent roles, how work flows from outcome to deployed change, where state lives, where humans approve, and how it reads the subject contract (P3). It pulls together T4 (agent orchestration), T6 (ADR strategy), T7 (impact analysis) and T8 (subject knowledge), so it closes after them, but its shape is sketched early so those items are decided with the whole system in view.

**Sketch:** [architecture-sketch.md](docs/architecture/architecture-sketch.md). Walkthrough 1 ran seven use cases (gaps G1 to G7); walkthrough 2 ran the remaining E5 scenarios (gaps G8 to G14). All proposed changes accepted (5 Oct).

**Decided (5 Oct):**

- **Orchestrator:** deterministic code; LLMs only as workers.
- **Failure handling:** retry, then a repair loop with a fixed retry limit, then escalate to the architecture coordinator. Failures are triaged and routed back to the stage that caused them; budgets are hierarchical (G8).
- **Traceability through OpenTelemetry:** every step is a span; an outcome ID correlates everything; existing distributed-tracing concepts (trace context, span links, GenAI semantic conventions) are reused rather than invented.
- **Handoffs as typed contracts:** agents exchange schema-validated messages, as services do through an API, which makes them testable, loggable and versionable.
- **Domain agents (stewards) stand in for domain experts and engineering domain owners.**
- **The arbiter resolves conflicts between stewards, applying recorded ADR precedence only;** anything else is a decision gap for the coordinator (G5).
- **Implementation flow:** stewards plan; an implementer (a coding agent) builds from the plan.

**Decided (1 Nov, Andy): full autonomy is the eventual goal, as a stretch goal.** The path runs through exercising the capability with the architecture coordinator in the loop. As use cases and features are added, it may prove impossible or ineffective. Nothing is claimed beyond the evidence, and P1's "doesn't overclaim autonomy" still applies.

**Open:**

- **Rule units as the capability's core interface (proposed 2 Nov, T6).** Selecting the decisions that govern a change and checking it against them is the capability's job; the rule-unit spike in Step 7 is an early prototype of it.
- **How autonomy rises: escalations become rules (proposed 1 Nov).** Log every escalation and its cause. When the same kind recurs, the coordinator decides once and it becomes a rule or precedence, which the system then applies. Autonomy grows because a human turns decisions into rules, not because the agent starts deciding. `product.md` already lists human interventions per outcome as a measure to report. DEV-1 to DEV-3 plus ten evaluation outcomes are too few samples to automate a class with confidence: this project can demonstrate the mechanism, not prove the numbers.
- **Roles from strategic domain-driven design.** The subject system's bounded contexts shape the stewards; the capability's own context map (nine contexts in the sketch) decides which roles exist and which are LLM-driven or deterministic. Confirm the context map, including whether Evidence is its own context and where risk scoring lives.
- **Human approval points.** The sketch's use-case ladder proposes them, scaled by risk. Confirm. Include which rule applies when a security defect is in touched code (ADR-016@v1 C9: fixed with a test and flagged) and also needed first (ADR-015@v1 S9: approval if it changes behaviour).
- **Typed handoff limits.** A schema guarantees a message's shape, not the quality of the reasoning inside its text fields; those fields still need the runtime grader. Decide how schemas are versioned and where they are validated.
- **Structure versus prose, proposed principle:** structure what the system acts on; keep prose for reasoning. Decisions, domain and ADR IDs, verdicts, references and confidence go in schema fields; the reasoning stays as free text in a rationale field. Likely mechanism: the agent reasons freely, then emits a schema-validated result. Confirm with a spike comparing structured and free-form impact analysis on the development set.
- **Long-running traces.** An outcome may wait days for approval. Likely option: a trace per stage, linked by span links and the outcome ID. Confirm in a spike.
- **Prior art to review:** agentheim, a domain-driven-design harness for Claude Code (an orchestrator that never writes code, strict worker return formats, a knowledge layer). Check what it already solves before designing our own.
- **Prior art reviewed (20 Oct):** Anthropic's AI-native SDLC playbook (intent → spec → plan → build → test → deploy → maintain, each stage committing an artefact). It has no impact analysis across domains, no selection of the decisions that govern a change, and no stop when decisions conflict or are missing; its design stage applies generic organisational skills. That gap is this capability's differentiator (product.md). Its evals have no held-out set, and its headline figures are unmeasured vendor claims.

### A2. Independent grader · Partly decided

The decided part is recorded in [ADR-014](docs/adr/ADR-014-two-separate-graders.md).

**Decided (5 Oct):** two graders, kept separate. A **runtime grader** checks work before a human sees it; an **evaluation grader** scores outcomes for E1 to E4. They use separate rubrics and are calibrated separately, and human labels remain the final check on the evaluation grader. Rubrics are catalogued in A5.

**Open (A5 proposes answers to several):**

- **Scope.** Under the thesis, the grader covers only what deterministic checks can't: for example, whether an impact set's reasoning is sound, whether a spec captures the outcome's intent, and whether trade-offs are explained clearly to a merchant.
- **Independence.** The grader sees the artefacts, the rubric and the outcome statement, not the producing agent's reasoning. Whether a different model or model family is used to reduce self-preference bias.
- **Calibration.** Rubrics versioned as code; agreement with human labels (for example Cohen's kappa) measured and published before scores are trusted.
- **Consequences.** Whether a low grade blocks, triggers a bounded repair loop, or only flags for the human reviewer, and the loop limit.
- **Cost.** Where the grader earns its cost, for example only at human approval points.

### A3. Governing cross-cutting concerns · Partly decided · Gate

At least one further context governs system-wide concerns: integration patterns, logging and observability, authentication and authorisation, and similar. eShop already has the code for this: shared projects such as ServiceDefaults (authentication, telemetry, health checks), the event bus, and the integration event log. Those projects would be owned here, as a platform team owns shared infrastructure.

**Decided (5 Oct): not a single agent.** One agent owning every cross-cutting concern would need too large a context and would become a bottleneck. Split by concern. Cross-cutting stewards are triggered by what proposals touch, as well as by impact analysis (G9).

**Open:**

- **How to split?** By concern (security, integration, observability) keeps each focused but adds coordination. In Team Topologies terms: a platform team, enabling teams, or both?
- **Overlap with ADR scoping.** Cross-cutting ADRs already add domains to the impact set (T6, T7). Decide whether this context *owns* those ADRs and the shared code, while the ADR mechanism does the selection.
- **Authority.** Can it veto a steward's plan, or only advise, with the arbiter or architecture coordinator deciding?

### A4. When an outcome splits, and who decides · Closed (ADR-015)

From G11: an outcome can split so that unblocked work continues. Whether a split can be automatic depends on why it happens.

**Decided (5 Oct):**

- The nine scenarios below are complete.
- **Deliver dark:** partial features ship behind feature flags, switched off, so nothing changes for users and splitting can be automatic. Switching a flag on is the human decision. Feature flags use **OpenFeature** (Q5). Cost: a feature flag capability in the subject system (eShop has none today).
- The five rules for an automatic split below apply.

**Split scenarios:**

| # | Scenario | Example | What changes for the merchant | Decision |
| --- | --- | --- | --- | --- |
| S1 | Decision gap blocks part of the outcome | A refund rule nobody has decided yet | They get less than they asked for | Automatic, delivered dark; switching on needs the coordinator |
| S2 | ADR conflict blocks part | Part of an outcome needs a synchronous call to another service | They get less than they asked for | Automatic, delivered dark; switching on needs the coordinator |
| S3 | One part is ambiguous, the rest is clear | Loyalty: earning rules clear, redemption unclear | Nothing yet; risk of rework if the answer changes the design | Automatic for parts that don't depend on the answer |
| S4 | One independent part fails and escalates (G8) | Webhook part done, storefront part failing | They may get a part that makes no sense alone | Automatic, delivered dark; switching on needs the coordinator |
| S5 | Delivered part depends on the blocked part | Storefront needs a contract the blocked domain hasn't agreed (G1) | n/a | Not splittable: the dependency graph forbids it |
| S6 | Planned staging of a large outcome | Loyalty: charter, scaffold, earning, then redemption | Nothing: all of it arrives, in steps | Approved once as part of the plan; each step then automatic |
| S7 | Improvement work over budget (Q4) | Refactoring beyond the touch-radius budget | Nothing | Automatic proposal of a follow-up outcome; the follow-up needs approval |
| S8 | Out-of-scope security defect (G10) | A gap found in code next to the change | Nothing directly | Automatic proposal of a remediation outcome; flagged immediately |
| S9 | Preparatory change needed first | A calculation an outcome depends on must be corrected first | Nothing, if behaviour-preserving | Automatic if structural; approval if it changes behaviour |

**Rules for an automatic split**, all checked deterministically:

1. The delivered part passes its own subset of the visible acceptance examples.
2. Nothing in the delivered part depends on the blocked part (contract dependency graph, G1).
3. The split doesn't reduce what the outcome asked for. Any reduction in what the merchant gets needs a human (with deliver dark, at the point the flag is switched on).
4. The delivered part's risk rung is no higher than the original outcome's.
5. The system is left consistent: no half-built feature visible to users.

**Consequence for evaluation (E1):** for any outcome expected to split, its visible and hidden examples are labelled by part, so the delivered part is scored on its examples and the blocked part on escalating correctly.

### A5. Rubric catalogue for graders · Partly decided · Gate · Deep research

**Decided (8 Oct):** add a catalogue of rubrics for the runtime grader (A2), covering stewards, implementers and the other judgement points found in the walkthroughs. **Runtime rubrics live in this public repo**, because they define quality for the capability, as visible examples do. **Evaluation rubrics live in the private evaluation repo**, so the capability can't tune itself to them. Draft the runtime rubrics in Phase 1, because they shape what each agent must output in its typed handoffs; calibrate them in Phase 5 against real outputs.

**Starting point: Claude Managed Agents "outcomes".** Anthropic's Managed Agents (beta) lets you define an outcome as a description plus a markdown rubric; the harness provisions a grader in a separate context window, which returns per-criterion feedback, and the agent iterates until the rubric is satisfied or an iteration limit is reached (default 3, maximum 20). Sources: [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes), [cookbook: verify with an outcome grader](https://platform.claude.com/cookbook/managed-agents-cma-verify-with-outcome-grader). What to borrow:

| Outcomes concept | How it maps here |
| --- | --- |
| Rubric as a markdown document of explicit, independently gradeable criteria ("the CSV has a numeric price column", not "the data looks good") | The rubric format below; vague criteria are rejected in review |
| Grader in a separate context window, not influenced by the agent's implementation choices | A2 independence: grader sees the artefact, rubric and outcome statement, never the producer's reasoning |
| Per-criterion explanation fed back to the agent | Criterion IDs feed the repair loop, as ADR IDs and analyzer rule IDs do |
| Results: `satisfied`, `needs_revision`, `max_iterations_reached`, `failed` (rubric doesn't apply), `interrupted` | `needs_revision` → repair loop; `max_iterations_reached` → escalate with evidence (G8); `failed` → failure triage, probably a wrong rubric or a misrouted artefact (G8) |
| Iteration limit per outcome | Hierarchical budgets (G8) |
| Tip: write rubrics by having Claude analyse a known-good artefact | Derive first drafts from the Ordering exemplar's outputs for DEV-1 to DEV-3 |

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

**Rubric format (proposed, to refine alongside the ADR template):**

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

**Open:**

0. Whether judgement rules from ADRs become rubrics inside rule units (T6, proposed 2 Nov), so each rubric carries its own test fixtures.
1. Which rubrics are needed for the first thin slice? Likely R2, R3, R7 and R8.
2. Binary criteria only, or graded scales for some?
3. Which model tier grades, and is a different model family available and worth it?
4. Should agents see their runtime rubric while working? Proposed yes, because it defines quality as visible examples do; the evaluation rubrics stay hidden.
5. How rubrics are versioned and selected: per artefact type, with domain-specific additions from a domain's own folder?

---

## Tools and methods

The original document assumed Spec Kit, ADRs and CUE. Each was reopened here for a capability that orchestrates existing coding agents.

### T1. Planning and specification tooling · Partly decided · Gate

There are two layers: building the capability itself (and the exemplar), and the capability producing specs for changes to the subject system. They may use the same tool or different ones.

The decided part is recorded in [ADR-009](docs/adr/ADR-009-spec-kit-workflow.md).

**Decided (5 Oct): adopt the Spec Kit workflow** for building this project. Skills, subagents and hooks support its stages rather than replacing them.

**Decided (8 Oct), from the Spec Kit v1.1.2 documentation:**

- **Version:** Spec Kit **v1.1.2** (released 7 Oct 2026, commit `959e866`), pinned. Installed with `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.1.2`. Upgrades are deliberate, reviewed changes.
- **Workflow:** constitution once; per feature, specify → plan → tasks → implement → **converge** (repeat implement and converge until it reports converged). Clarify, checklist and analyze are optional quality gates.
- **Initialisation (this repo):** `specify init --here --force --non-interactive --integration claude --script py --ignore-agent-tools`. Claude Code integration in skills mode (`.claude/skills/speckit-*`, invoked as `/speckit-<stage>`). Python scripts, so they behave the same on Windows, macOS, Linux and CI. `--ignore-agent-tools` only because the desktop app does not put a `claude` executable on PATH.
- **Core only: no presets or extensions yet.**
  - *Model Driven Engineering preset* (`mde` 0.5.1): **rejected.** It replaces the recognisable core flow with `specify → next`, needs its own extension, and treats proposed answers as approved when the user says `next`, which conflicts with our approval discipline. Small and little-used (one release, May 2026).
  - *Brownfield Bootstrap* extension: **deferred to the eShop fork** (Phase 2), the only place with existing code. Try the core existing-projects guide first; the extension has not changed since April 2026, before Spec Kit 1.x.
  - Official `git` extension (numbered feature branches): not yet; it may clash with the desktop app's worktree branches. Try it on the first spec.
  - Official `agent-context` extension: no; CLAUDE.md is curated by hand.
  - Official `assess` extension: consider in Step 7 as the base for the research-spike skill.
- **Community extension policy:** community extensions and presets are third-party code that the Spec Kit maintainers do not review. None is installed without a source review, a pinned version and an ADR.
- **Spec persistence: flow-forward, anchored on decisions.** Each feature folder in `specs/` is a fixed historical record; new requirements get a new folder. What must stay true lives in the ADRs and the constitution, enforced by deterministic checks. This is our answer to the criticism that Spec Kit is spec-first but not spec-anchored: the system is anchored on decisions, not on specs kept current by hand.

**Decided (1 Nov, Andy):** the constitution is thin. Principles point to ADRs without restating them; every plan cites the constraints that apply; the six hard rules are quoted word for word; the index (ID, title, scope, no version) is generated. Agents should load Constraints sections, opening a full ADR only when they need its reasoning. The constitution adds no rules of its own, and a conflict with an ADR is a decision gap. CLAUDE.md hard rule 2 now reads "In eShop, build only development outcomes by hand". Recorded in [ADR-009](docs/adr/ADR-009-spec-kit-workflow.md) (v2).

**Open:**

- When the eShop fork gets its own constitution. This one covers this repository only, so fork plans won't load it, and the hard-rule safety net doesn't reach eShop work until then. P9 says the constitution stays system-wide; reconcile that.
- Whether the capability also produces Spec Kit artefacts for changes to the subject system (the second layer; with A1 and T4). Spec Kit will be initialised separately in the eShop fork for subject-side specs (P3).

### T2. Decision records · Closed (ADR-000) · Gate

ADR format (Nygard, MADR, or our own template), where ADRs live, and how they are versioned. The template becomes ADR-000. Its front matter needs at least: ID, status, scope tags, precedence (G5), supersedes, enforcement links (Q1) and exceptions (G12).

**Decided (20 Oct), [ADR-000](docs/adr/ADR-000-decision-record-format.md):** our own template ([docs/adr/template.md](docs/adr/template.md)), extending MADR 4.0.0 with front matter for scope, precedence, supersession, exceptions and per-constraint enforcement, and a numbered Constraints section separate from the Decision prose.

- **Precedence (G5):** an explicit `overrides` wins first, then tier (cross-cutting binds domain, domain binds component); anything else is a decision gap.
- **Exceptions (G12):** separate records in `docs/adr/exceptions/`; the ADR says only whether exceptions are allowed. Record format decided with Q1.
- **Accepted ADRs:** only status, date, superseded-by and enforcement state and link may change; anything else is a new, superseding ADR.
- **Both repositories use the same template;** the eShop fork's ADRs have their own ID sequence.
- **Not yet enforced:** an ADR validator (constraints C1 to C5) is built with the D1 hooks in Step 7.

### T3. Deterministic constraint enforcement · Merged into Q1

Q1 treats enforcement as a map of rule types to mechanisms rather than a single tool choice.

### T4. Orchestrating coding agents · Partly decided · Gate

**Decided:** orchestrate existing agents such as Claude Code rather than build our own (P7, [ADR-004](docs/adr/ADR-004-non-goals.md)).

**Open:**

- Mechanism: Claude Code headless mode, the Claude Agent SDK, or another harness.
- Shape: how many agents, what each does, how they hand off, where humans approve.
- Safety: sandboxing, least-privilege tokens, what agents can and cannot touch.
- Cost: budget per outcome and how it is enforced.

### T5. Language and stack for the capability itself · Partly decided · Gate

**Decided (5 Oct):** the capability's API is C# with a React frontend (P5a; [ADR-017](docs/adr/ADR-017-coordinator-interface.md)).

**Open:** whether agent orchestration also runs in .NET (driving Claude Code through its command-line interface) or in a small TypeScript or Python worker using the Claude Agent SDK, called from the C# API. The tension: the subject is .NET, but the agent orchestration ecosystem is strongest in TypeScript and Python. Criteria: delivery speed, how it reads to target employers, and fit with the CV story.

### T6. ADR strategy across the system [B1] · Partly decided

How ADRs are stored, selected, referenced by agents and kept current, including the personas, nine use cases and evaluation criteria in the original document. Depends on T1, T2 and Q1. ADR-009@v2 C9 adopts constraints-first loading; selection of judgement rules is decided (below), selection in general (by domain, path or impact set) is still open, and the wider progressive-disclosure approach remains a hypothesis.

**Decided (2 Nov), by Andy after the rule-unit spike** ([spikes/rule-units/](spikes/rule-units/README.md)). The ADR is written when T6 closes.

- **Judgement units are selected deterministically from glossary terms:** "deterministic judgement-unit selection approved". The step that turns artefacts into terms may use a model, as the spike's translator does, with its output validated against the glossary; the selection after it is deterministic.
- **Hard rule 4 stays always loaded:** "keep hard rule 4 always loaded".
- **Delivery: an MCP server that joins the parts, built now, called by a hook or by the capability's orchestrator.** Andy: "make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided", then, asked to confirm that this meant one recommendation rather than "now a step, later a server": "yes, one recommendation with the server built now."
- **The hook is a harness hook,** such as Claude Code's `PreToolUse`, not a skill or Spec Kit's `before_analyze` hook, which leave the trigger to the model ([delivery.md](spikes/rule-units/delivery.md)). The author's reading, confirmed by Andy, 2 Nov: "yes, harness hook is right".
- **Build our own; borrow adrkit's shapes, don't install it.** adrkit's unit is a whole decision, not a constraint; it selects by files, which don't exist at plan time; and its README describes no per-decision tests. Installing its extension would also mean revising ADR-009@v2 C4, with a source review and a pinned version (C5). Shapes to borrow, listed in [prior-art.md](spikes/rule-units/prior-art.md): typed `affects`, `@adr` markers, `--as-of` and a read-only MCP server; only the last is built so far. The assessment is from its README, not a source review. The author's recommendation; Andy, 2 Nov: "yes, record it as decided".

**Decided (3 Nov), by the author at Andy's request:** "you decide the sarif version".

- **SARIF 2.1.0, one version for every producer of rule violations.** 2.1.0 is the only approved SARIF specification found (an OASIS Standard since March 2020; a 2.2 draft exists in the OASIS sarif-spec repository, status not confirmed). GitHub code scanning "only supports SARIF version 2.1.0" ([docs](https://docs.github.com/en/enterprise-server@3.15/code-security/reference/code-scanning/sarif-files/sarif-support-for-code-scanning)). One version, on the author's reasoning: ADR-016@v1 C10's consumers (the ratchet, the repair loop and code scanning) each read one format, and the ratchet compares results across runs, so a version change must move every producer and the baseline together. Roslyn's error log writes SARIF 1.0.0 by default and 2.1.0 only when asked (`SarifVersion.cs` in Roslyn's source), so eShop's analysers would need that setting, which is an eShop change and needs an approved spec (CLAUDE.md hard rules 2 and 5). **Applied, 3 Nov, approved by Andy:** "yes, do both." [ADR-016](docs/adr/ADR-016-improving-legacy-code-the-capability-touches.md) v2 adds C17 (SARIF 2.1.0), and the spike has a separate C17 unit (Andy, 3 Nov: "add a separate C17 unit") that reports a SARIF version other than 2.1.0, named in a plan or set in a file, with the cases written first.

**Open:** the rest of T6's scope (how ADRs are stored, referenced and kept current; selection by domain, path or impact set; conflict detection; enforcement and human attention, as listed under the limits below); the spike's other choices (what counts as a catch, the f1 control, where results live); hiding the server's `get_rules` and `index` from the model, and which trigger runs it in this repository (both part of the hook wiring, with the controls track, D1); wiring needs Andy's approval; conjunctions in applicability; selection recall on real plans (the spike below), with a second labeller; the subject glossary coming from the fork's contract (ADR-001@v2 C1, C2); a generator and validator for authoring units at scale; CUE for applicability; and whether the glossary becomes a first-class artefact.

**Scaling model (1 Nov).** Measured on the 19 ADRs before ADR-009 v2: 162 constraints; about 1,750 tokens per full ADR and about 240 per Constraints section, estimated at 4 characters a token. ADR counts and relevant sets below are assumptions, not measurements.

| Scenario | ADRs | Relevant | All full | All constraints | Index + relevant full | Index + relevant constraints | One domain steward |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Phase 2 baseline | 52 | 17 | 91k | 12k | 31k | 6k | 3k |
| Mature eShop | 117 | 38 | 204k | 28k | 70k | 13k | 5k |
| Large estate, 30 domains | 520 | 95 | 908k | 123k | 182k | 39k | 8k |

The model has no pass or fail test. Against an assumed 200,000-token window, loading every full ADR passes it at about 115 ADRs. Each steward's own context stays small, but stewards aren't cheaper in total: across every touched domain they cost about the same as or more than index plus relevant constraints. So this isn't evidence for T7's per-domain decision. The figures assume one combined index; in practice this repo's index stays small because subject ADRs live in the fork, and the fork's would need splitting by domain at large sizes. The relevant sets may be too low: 12 ADRs carry the `project` tag, so "scope applies" read literally selects far more.

**The limits that matter more than context:**

1. **Selection recall.** A missed ADR is silently not applied. Index titles and scope tags may not be enough. Not yet measured.
2. **Conflict detection.** All-pairs comparison reaches 6,786 pairs at 117 ADRs and 134,940 at 520. It needs filtering by scope, or machine-checkable constraints (Q1).
3. **Enforcement.** On 1 Nov, before ADR-009 v2, 2 of 161 active constraints were enforced. If constraints grow faster than checks, ADRs become prose again.
4. **Human attention.** ADR acceptance is human, so ADR volume is review volume.

**The index's cost, measured (4 Nov), for the T6 ADR.** Andy asked whether the index would bloat without solving the search for specific clauses. It doesn't solve that search, and isn't meant to: ADR-009@v2 C10 makes it ID, title and scope, and clause-level selection is the rule units' job (glossary terms select units; the MCP server returns them). It does grow with the estate, and it is always loaded, because it lives in the constitution. Today it is 19 rows and 3,407 characters: about 850 tokens, or 45 per ADR, at 4 characters a token. At the scaling model's sizes that is about 5,000 tokens at 117 ADRs and about 23,000 at 520. Proposed for the T6 ADR: at scale, the index moves behind the rule-unit server as a lookup, instead of living in the constitution. That would revise ADR-009. Andy, 4 Nov: "Record for the T6 ADR". Item 2's generator writes the index wherever it lives.

**Parallel problems (1 Nov).** Where constraints live is a retrieval problem, and tool discovery and progressive disclosure solve the same one. Checked in their docs: skills keep descriptions in context and load bodies on invocation, or by a `paths` pattern; MCP tool search keeps tool names in context and loads definitions on search; path-scoped rules in `.claude/rules/` load when matching files are touched; adrkit selects decisions deterministically, by an `affects` glob or a `@adr` marker, with no embeddings. Its design is worth borrowing; installing it would need a source review and an ADR (ADR-009@v2 C4, C5).

**Four routes, by kind of rule (proposed; the judgement row decided by Andy, 2 Nov):**

| Kind of rule | Route | Selected by |
| --- | --- | --- |
| Bright line | Always loaded | Nothing needed |
| Mechanically checkable | Not loaded; a check fires, and the violation feeds the repair loop | The check |
| Applies to a known area | Loaded by domain or path | A deterministic match |
| Judgement | Selected at plan time, then graded | A deterministic match on glossary terms (was "The model"; Andy, 2 Nov, after the rule-unit spike) |

**First evidence ([tests/constitution/results.md](tests/constitution/results.md)).** One `plan` run on a small export feature listed 14 of this repository's 19 ADRs, for about 101,000 tokens. With no labelled correct set, that shows only that selection can be broad; it says nothing reliable about recall or precision. The table above models whole-system scenarios, so it isn't directly comparable. `analyze` caught a blatant breach of an uncited ADR in 3 of 3 runs, working from its index title and a principle's heading. One feature and one plan run is a very small sample.

**Spike:** on DEV-1 to DEV-3, compare model-selected ADRs with deterministic matching on an `affects` field, and measure recall. Paths don't exist at specify and plan, so test impact-set domains mapping to ADRs (with T7). Selection recall hasn't been measured.

**A further idea, not part of the spike:** generate ADR constraints into path-scoped rules in the fork, so a domain's constraints load when an agent touches its code.

**Rule units (proposed by Andy, 2 Nov).** The constitution test showed `analyze` misses a breach buried in ADR text (f8, 3 of 3), because it reads only the constitution. A bigger constitution doesn't fix that; a different shape might. Each ADR constraint becomes a self-contained, testable unit:

- **identity:** ID, version, constraint text, a link to its ADR;
- **applicability:** which stages, domains or paths it governs (the `affects` idea above);
- **check:** deterministic for mechanical rules (run at the Q6 layers), or a rubric for judgement rules (graded at plan time, A2 and A5);
- **tests:** fixtures that must pass and must fail, with expected results written first (ADR-012@v2 C10).

Units load deterministically, selected by impact set or touched paths, not by a model reading titles: an index is always present, and units are fetched on demand. Delivery options: an MCP server (`get_rules`, `check`; deterministic, and it is the capability's own interface), skills (progressive loading, but model-triggered), or a step before `analyze` (smallest, but changing Spec Kit's flow needs an ADR, ADR-009@v2 C4). Prior art: ESLint and Semgrep rules ship with their own tests; OPA policies use `opa test`; adrkit pairs `affects` with `evaluate`.

**Spike, first item of Step 7:** build three units of different kinds, each with tests: ADR-016@v1 C10 (mechanical), ADR-015@v1 C2 (judgement), and one hard rule. Re-run f8 with its unit loaded, and measure whether the miss becomes a catch. Run it through the discernment step (D1) before choosing to build or borrow. This is also an early prototype of the capability's own selection and checking (A1, T7).

**Spike run (2 Nov); Andy's decisions are listed under Decided above; the branch awaits his local review** ([spikes/rule-units/](spikes/rule-units/README.md)). After the prior art, Andy reshaped it: "Feels like we need the concept of ubiquitous language/glossary as domain driven design establishes, to align everything", and selection, validation and reporting as distinct steps. Approved: "go ahead, glossary in the spike folder for now." Built: a glossary (capability and subject terms kept apart, ADR-001@v2 C1), three units (ADR-016@v1 C10, ADR-015@v1 C2, hard rule 4's copy clause) and four decoys, 17 labelled fixtures, expectations committed first. Results ([results.md](spikes/rule-units/results.md)):

- **f8 caught in 3 of 3** runs with its unit loaded (was 0 of 3), all CRITICAL, with no ADR opened (self-reported). No CRITICAL on the f1 control; one LOW advisory row naming the loaded hard rule.
- **Translators:** a constrained model mapping artefacts to glossary IDs scored 31 of 31 terms in each of three runs, the same sets each run; its unit precision, 76%, missed the 85% prediction. Alias matching missed every paraphrase (24 of 31); BM25 matched almost everything (precision 30 of 92).
- **Selection:** the best translator and a model reading ADR titles both reached 16 of 16 unit recall, so on this small set selection by title wasn't what failed f8: the unit never reached `analyze`. The unit carried the constraint and its check's description, and the spike can't separate the two. Units added constraint-level delivery and stable selection (17 of 17 fixtures against the baseline's 15 of 17).
- **Applicability:** all five false selections by the best translator were ADR-011@v1 C3 matched on one term; applicability needs conjunctions.
- **Checks:** the mechanical and bright-line checks blocked and passed as expected (13 cases), with three predicted misses; the ADR-015@v1 C2 rubric gave 15 of 15 expected verdicts.
- **Delivery, decided by Andy on 2 Nov** (see Decided above; [delivery.md](spikes/rule-units/delivery.md)): an MCP server joining the parts, called by a harness hook or the orchestrator. Not a skill or Spec Kit's `before_analyze` hook, which leave the trigger to the model.
- **Andy, 2 Nov, after the run:** "deterministic judgement-unit selection approved, keep hard rule 4 always loaded, make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided." v1's other recommendations are still not ruled; build rather than install adrkit was decided later the same day (see Decided above).
- **Joined step and MCP server built** (expectations first, [server-expected.md](spikes/rule-units/server-expected.md)): one call translates (Anthropic API, alias fallback), validates, selects, checks and returns hook output or a record. Passes over stdio and from the generated hook config. Live, in one headless Claude Code run by the author with Andy's key: the hook fired before `speckit-analyze`, the API translator ran, and `analyze` raised C10 as CRITICAL; not blind, and the model could see the server's other tools.

Limits: 17 small fixtures and labels written by the author, and one model family throughout. Selection recall on real plans (the DEV-1 to DEV-3 spike above) is still unmeasured.

**Prior art to review (found 8 Oct, Spec Kit community catalogue):**

- *adrkit* (github.com/mbeacom/adrkit, Apache-2.0): pulls the decisions governing a piece of work into agent context, checks plans against them, and drafts ADRs from plans. Close to our selection and checking ideas; state what we add beyond it. Its Spec Kit extension is pinned to Spec Kit `>=0.13.0,<1.2.0` (checked 1 Nov; an earlier note said below 1.1.0), so v1.1.2 is in range. Installing it would need a source review and an ADR (ADR-009@v2 C4, C5).
- *arch-governance* (github.com/ashbrener/spec-kit-arch-governance, MIT): citation slots linking specs to ADRs, with a read-only, fail-closed validator. Also relevant to Q1.

### T7. From outcome to impacted domains [B2] · Partly decided · Gate · Deep research

Central to the capability and likely the first thing an interviewer probes. Research must start from prior art (how change impact analysis is done in industry and literature, software catalogues, dependency graphs) before evaluating our own design, and the chosen option is recorded in an ADR explaining why it beat the alternatives. Depends on P4, because impact analysis needs the domains to exist.

Options carried over from the original document: a domain catalogue classified by an LLM, deterministic expansion through events, cross-cutting ADR rules, embeddings as a safety net, and human confirmation, using the loyalty worked case.

**Decided (5 Oct):**

- **Per-domain agents, as proxies for domain experts and engineering domain owners.** Supporting reasons: context isolation, parallel work, and negotiating cross-domain contracts. Still tested against a single agent with domain-scoped retrieval, and the ablation published.
- **Deterministic expansion always applies.** Domains that consume an affected event, or are added by a cross-cutting ADR, join the set regardless of what the router decides.
- **The impact set can grow during stewardship** (G9) and can return "unowned capability" (G3).

**Working hypothesis (not decided):** a classifier or router identifies the impacted domains; each domain has a knowledge base indexed by domain; queries are routed to domain agents backed by their domain's knowledge.

**Open:**

- **The router is a single point of failure for recall.** A domain it misses is never consulted, so its ADRs are never applied. Compare against broadcast (every steward screens the outcome with a cheap model and claims or declines it; affordable at around seven domains) and a hybrid. Measure recall, precision and cost.
- **Retrieval may be unnecessary at eShop's size.** Each domain's knowledge (ADRs, contracts, code summaries, docs) may fit in context with prompt caching. Measure its size in tokens today and project it at larger scales (for example the 10, 50 and 200 ADR test in T6) to find where retrieval starts to pay off.

### T8. Subject knowledge: sources, extraction and retrieval · Open · Gate

Proposal (5 Oct): an ADR embedding pipeline as a generic mechanism for extracting project knowledge, usable for any subject.

**Open:**

- **Which knowledge, from which source?** The subject contract holds at least three kinds of knowledge: decisions (ADRs), structure (domains, APIs, events, dependencies) and domain facts (for example, that unredeemed points are a liability). ADRs hold only the first, and only where someone wrote one down.
- **Extraction versus retrieval.** Embeddings retrieve relevant passages; they don't produce a structured domain catalogue. Structure can be extracted deterministically from code and contracts (project references, OpenAPI documents, integration event types), which is generic per stack and exact.
- **Guaranteed versus likely.** Selecting the ADRs that bind a change must be guaranteed, which similarity search can't promise. Candidate role for embeddings: recall safety net alongside deterministic selection, and answering "has this been decided before?"
- **Where domain facts live.** In ADRs, in the domain catalogue (for example a glossary or invariants section per domain), or left to the model's general knowledge. The choice affects E4.
- **Evaluation.** Recall of embedding-based selection versus deterministic selection against a hand-labelled set; extraction accuracy of the catalogue against a hand-written one.

Depends on T6 and T7; closes jointly with them.

### T9. Durable workflow engine · Open · Gate

Outcomes wait hours or days at approval points (walkthrough W3), so the deterministic orchestrator needs durable state that survives restarts. Options in .NET include Dapr Workflow, the Durable Task framework and Temporal's .NET SDK, or a hand-built state machine over a database. Criteria: durability, visibility of workflow state, testability, fit with OpenTelemetry tracing, and operational weight for a demo that is deployed only on demand.

---

## Evaluation

Success is defined before building. These items turn product.md's success criteria into something measurable.

### E1. The outcome set · Partly decided · Gate

The decided part is recorded in [ADR-007](docs/adr/ADR-007-outcome-set-and-impact-scoring.md).

**Decided (5 Oct):**

- **Ten held-out evaluation outcomes,** used only for scored runs, plus a separate development set (DEV-1 to DEV-3, [development-outcomes.md](docs/outcomes/development-outcomes.md)) for iterating during the build.
- **Seven positive outcomes (one adding a new domain) and three negative** (ADR conflict, decision gap, ambiguous request). Spread across single-domain, multi-domain and cross-cutting.
- **Andy writes the outcomes and their expected impact sets.** The outcomes, their verification against eShop and their labels are held in the private evaluation repository and published with the results.
- **Scoring is a deterministic comparison** (recall and precision) with no LLM in the scoring.
- **Two-tier labels.** *Must change*: domains the change must modify, written by hand at domain level, with acceptable alternatives recorded where more than one design is valid. *Must consider*: domains that need checking but not changing (for example a domain whose ADR constrains the change), written by hand.
- **LLMs as disagreement detectors only.** Several models can label independently to flag outcomes worth a second look, never as the answer key.
- **Split outcomes are labelled by part** (A4).

**Impact set, defined:** for each outcome, the list of domains (and the contracts within them: APIs, events, data) that the change must modify or explicitly consider. It is an intermediate output of the capability (T7), scored for recall and precision against a label written before the run. It is not a measure of value; value measures such as time and human effort are covered in E3.

**Open:**

- **Second reviewer on a sample** (for example three of ten outcomes) by an experienced engineer, to show the labels aren't shaped by the same person's design of the system. Optional; adds credibility. The same question applies to tests (E2).

### E1b. Validate outcomes and overlaps before starting · Decided (ADR pending)

**Decided (5 Oct).** Every evaluation and development outcome was checked against the eShop source and against each other (overlap matrix), held privately. Public decisions from it:

- The storefront is its own context: a composition of the other domains plus the features that stitch them together.
- Evaluation outcomes run independently, each from the same pinned baseline.
- Business rules live in the owning domain (a baseline ADR).
- Times are stored in UTC; business time periods follow UK local time (Europe/London).
- The development set is DEV-1 to DEV-3.

Recorded so far: the development set in [ADR-007](docs/adr/ADR-007-outcome-set-and-impact-scoring.md), independent runs in [ADR-008](docs/adr/ADR-008-acceptance-tests-and-preregistration.md). The storefront context, business rules in the owning domain, and UTC with Europe/London are subject ADRs, to be written in the fork in Phase 2 (ADR-000@v2 C12). E1b closes when they are.

### E2. Acceptance tests · Partly decided · Gate

How is "the change works" judged independently, when coding agents write both the code and its tests?

The decided part, including the sequence, the withdrawal rule and mutation testing on DEV-1 first, is recorded in [ADR-008](docs/adr/ADR-008-acceptance-tests-and-preregistration.md).

**Decided (21 Oct, Andy), from review of ADR-008:** "pass after the change" is required for development outcomes only; for evaluation outcomes, passing is the measured result. In the D6 dry run, protocol drivers are built by Andy with Claude Code; in capability and evaluation runs, by the capability. Mutation testing covers the implementations that pass. Mutation scores and withdrawals are published with the results, if results are published (P2). The pre-registration also fixes the list of measures that all-or-none publication covers.

**Decided (5 Oct):**

- **Layered acceptance, with a four-layer acceptance test model at its core:** business-language test cases and DSL written by a human before the run; protocol drivers built by the capability; a deterministic check that drivers only use public APIs, events or the UI.
- **Acceptance tests are an input, written by Andy with Claude Code using the D6 skill,** not proposed by the capability.
- **Acceptance tests first, as the definition of done.** Reference acceptance tests are written for every outcome before the capability is built. The visible examples, plus the quality layers and ADR checks, form the definition of done the capability works to. Hidden examples are not part of the definition of done; they are used only for scoring.
- **Acceptance test-driven development at system level.** Every acceptance test must fail against the subject before the change (red), and pass after (green). For evaluation outcomes, "before" is the evaluation baseline tag (P4).
- **Visible and hidden examples.** Each outcome includes a few business-language examples the capability sees (specification by example), plus hidden examples it never sees, used to check it generalised rather than fitted to the visible ones.
- **No reference implementations for evaluation outcomes.** Reference implementations exist only for development outcomes on the exemplar (P9), to prove the test approach, the DSL and the D6 skill before any scored run.
- **Test the tests** with mutation testing (for example Stryker.NET), and publish the score as a measure of test strength.
- **Pre-registration.** Hidden tests, labels and thresholds committed with a hash and timestamp before the scored run; kept in the private repo until then.
- **Quality layers beyond functional acceptance:** number of steps for a user to achieve the outcome, measured by journey scripts (HEART is not used, because it needs real users), accessibility, REST and API contract rules, breaking-change detection, API security, architecture rules, performance budgets and observability coverage. Tools chosen in Q2.
- **Confirmation-bias control:** the E4 baseline runs the same tests; a test that the baseline also passes isn't discriminating.

**Sequence per evaluation outcome (proposed 5 Oct, decided 8 Oct):**

1. Write visible and hidden acceptance tests and labels (Phase 3).
2. Freeze the evaluation baseline tag in the fork, once our baseline work is complete (end of Phase 4; P4).
3. Confirm the tests fail against the evaluation baseline, then pre-register everything, including the baseline tag and the withdrawal criteria below. (Decided 8 Oct: tests written before the exemplar work could otherwise behave differently after it.)
4. Run the baseline and the capability, each from the evaluation baseline. Satisfiability is shown by any run passing a test; a test nothing passes is inspected by hand against the withdrawal criteria.
5. Mutation-test whichever implementations pass.

**Withdrawal rule.** A test found defective after the run is withdrawn only with a documented reason, and the withdrawal applies to the baseline and the capability alike. **What counts as defective is pre-registered (8 Oct)**, so the hand inspection in step 4 can't move the goalposts. Starting criteria, finalised before pre-registration: the test contradicts the outcome statement or its visible examples; it depends on behaviour outside the outcome; or it can't be satisfied through public interfaces (APIs, events or the UI). Every withdrawal is published with its reason.

**Mutation testing is proven on DEV-1 first (8 Oct),** as part of the D6 dry run, so the method is shown to work, and weak tests can still be strengthened, before any evaluation test is written.

Why no reference implementations for evaluation outcomes: building seven by hand roughly doubles the work. The cost is that satisfiability is only shown after the scored run; the pre-registered withdrawal criteria contain that risk.

**Open:**

- Second reviewer on a sample of tests (see E1).

### E3. Success thresholds · Open

What score on each measure in product.md (impact recall and precision, missed-ADR rate, acceptance pass rate, interventions, cost and time per outcome) counts as good enough? Thresholds set before the final run are credible; thresholds set after are not.

### E4. Baseline comparison · Open · Gate

What are results compared against? The strongest evidence is an ablation: the same outcomes run through plain Claude Code with the ADRs simply placed in context, versus through the governed capability. If governance doesn't measurably beat that baseline, we need to know early. The baseline must separate what governance adds from what the model already knows (P3).

### E5. Architecture design scenarios · Partly decided · Gate

An evaluation set for the capability's *architecture*, separate from E1's outcomes, which measure its results. Prior art: quality attribute scenarios from the Architecture Tradeoff Analysis Method (ATAM).

**Done (5 Oct):** every scenario below was walked through on paper ([architecture-sketch.md](docs/architecture/architecture-sketch.md), W5 to W11), producing gaps G5 to G14, all accepted.

| Scenario | Walkthrough |
| --- | --- |
| A cross-cutting concern is part of the change set (an outcome needs a new authorisation scope) | W9 |
| Two cross-cutting contexts disagree (synchronous token checks versus asynchronous messaging) | W5 |
| A domain steward's plan conflicts with a cross-cutting context | W10 |
| A cross-cutting ADR is superseded while an outcome is in flight | W6 |
| A new domain must adopt platform conventions (loyalty) | W11 |
| A change to a legacy domain that doesn't follow the exemplar's conventions | W7 |
| An agent times out or returns invalid output, and retries are exhausted | W8 |

**Open:** turn the scenarios into executable scenario tests, each with its expected behaviour, which role decides, and when the architecture coordinator is involved.

### E6. Running the private evaluation · Open · Gate

Hidden tests and labels live in a separate private repository (D1). How is an evaluation triggered and run without exposing them?

Options to evaluate:

- **Manual trigger in the private repo:** a GitHub Actions workflow started by hand, given a commit of the public repo to evaluate. Simple, and nothing in the public repo can start it.
- **Triggered from the public repo:** a release or tag in the public repo sends a dispatch event to the private repo. Automatic, but the public repo then holds a credential that can start evaluations, so it must be scoped narrowly.

Either way: the workflow checks out the public repo at the given commit, runs the hidden tests against it, and stores results in the private repo. Agents in build sessions never hold credentials for the private repo. Development-set runs can be frequent; the scored held-out run happens once, at a pre-registered commit, and results follow the all-or-none rule (P2).

**Open (added 21 Oct):** whether to anchor the pre-registration publicly. A commit in the private repository can be rewritten before it is published, so its date rests on trust. One option: publish the pre-registration commit's hash in this public repo, under an immutable tag, at the time of pre-registration. Raised by review of ADR-008; Andy chose to decide it here.

---

## Quality enforcement

### Q1. Enforcement map: which mechanism enforces which kind of rule · Open · Gate

No single tool covers every kind of rule. This item maps each rule type to a mechanism and checks the gaps.

| Rule type | Example | Candidate mechanisms | Notes |
| --- | --- | --- | --- |
| Code structure inside a service | Domain layer doesn't reference infrastructure | NetArchTest, ArchUnitNET | Works on compiled .NET code only. Blind to HTTP calls, events, data and anything before code exists |
| Service-to-service dependencies | Loyalty must not call Ordering synchronously | Aspire app model (service references declared in the AppHost), architecture tests on client types | An HTTP call built from a URL string is invisible to NetArchTest. The Aspire app model is a machine-readable dependency graph and may be the better check |
| Event and API contracts | Events carry an idempotency key | AsyncAPI or JSON Schema, Spectral for OpenAPI, OpenAPI diff for breaking changes | eShop already has a Spectral configuration |
| Proposals before code | Impact record lists every domain consuming an affected event | CUE, JSON Schema, OPA/Rego | The original document chose CUE to validate specs, impact records, agent messages and ADR front matter *before* code is written, and to detect conflicting ADRs because contradictory constraints fail to unify |
| Business policy | Refund within policy limit; price above margin floor | CUE, OPA/Rego, domain code with property-based tests | |
| Security | Users act only on their own orders | Authorisation tests, API security test suites | |
| Infrastructure and deployment | No public endpoints except the storefront | OPA/Rego, IaC policy tools | |
| Judgement residue | Trade-off explanation is clear to a merchant | Runtime and evaluation graders (A2) | Only what no deterministic check can cover |

**A second axis: where in the flow a rule is checked (proposed 1 Nov).** The table above maps rule types to tools. T6's four routes cover how a rule reaches an agent. Neither says at which points it is validated.

| Point | Mechanism | Can it be bypassed? | Today |
| --- | --- | --- | --- |
| Before work | Context loading (T6) | Yes, advisory | Designed |
| Plan | Constitution Check, `analyze` | Partly: `analyze` is optional | First tested 1 Nov (`tests/constitution/`) |
| Edit | Claude Code hooks | Yes: scripts can get past them | Planned, Step 7 |
| Commit | Pre-commit hook | Yes: `--no-verify` | Not planned yet |
| Pull request | CI as a required check | No, once required | **No CI exists** |
| Review | Adversarial reviewer and Andy | No, while Andy merges | Running |
| Merge | Branch rulesets | No | Partial: no pull-request rule yet |

Proposed principles:

1. **One rule, one definition, checked at many points,** so the layers can't disagree (compare *gates*, D1).
2. **Check as early as is cheap.** Hooks give an agent the fastest feedback.
3. **The last layer must be one that can't be bypassed.** Early layers are for speed, late ones for assurance. A hook alone isn't a control.
4. **Not every rule needs every layer.** Each rule's enforcement entry names the points that check it.

**Gap this exposes:** ADR-011 treats hooks as the control, yet no CI exists, so no planned hook check has an unbypassable backstop. Step 7 needs CI and required checks as well as hooks. The outcomes that close this are Q6.

**CUE, checked 4 Nov (for the ADR front-matter schema, Step 7 item 2).**
- **CUE itself:** v0.17.1 (16 Jul 2026), Apache-2.0, before 1.0, with Windows ARM64 and Linux binaries. `cue vet` checks YAML against a schema, but Markdown front matter would need extracting first. The only Python binding found (pycue) is alpha and shells out to the binary.
- **Its distinctive case is unification:** contradictory constraints fail to unify. That needs constraints written as data, on the same field. The author first counted 1 value constraint of 171 (ADR-016 C17, SARIF 2.1.0). *Corrected the same day:* there are 173 active constraints, because a case-insensitive filter had dropped two. A full classification at Andy's request ([spikes/cue-reach/](spikes/cue-reach/results.md); one rater, seven corrections from review run 2) found:
  - 136 of 173 (79%) concern a value, a structure or a record that could be data;
  - 69 (40%) have that record today, at least partly;
  - 22 (13%) constrain a field another clause also constrains, which is where unification can compare clauses.

  A first write-up headlined 32% (clauses in a shared definition), which overstated unification's reach; review run 2 caught it.
- **Andy's ruling, word for word:** CUE's unification case "rests on contracts, proposals and policy, to be evaluated where those exist". The author had added a list of places (impact records, event schemas, the subject's ADRs in Phase 2) and later credited a shortened version to Andy. Neither traces to him, and both are withdrawn. *From the classification:* most plan-time clauses fall on two records that don't exist yet, the outcome request and the split record.
- **Tested (4 Nov, Andy: "Yes, download and run it"):** CUE v0.17.1 checked 8 clauses from six ADRs. They were written as constraints on a shared outcome request and plan, and checked against DEV-1 as data. 8 of 9 cases matched in the second run ([demo](spikes/cue-reach/demo-results.md)). A planted test clause clashing with ADR-017 C5 was caught by unification from the definitions alone, against a control, with both files named. It was a literal against a literal on one field; no real conflict between ADRs was found or tested. One error named values but not its clause. Not compared with JSON Schema or OPA on the same clauses. Q1's question stays open.
- **Decided (Andy, 4 Nov):** "JSON Schema; record CUE finding in Q1". The front-matter schema uses JSON Schema.

**Open:** does CUE earn its learning curve over JSON Schema plus OPA for the proposal and policy rows? Is NetArchTest or ArchUnitNET better maintained and more expressive today? Can the Aspire app model be checked reliably in tests?

Output: the enforcement section of each baseline ADR (the ADR template, T2, defines the field), plus the published "share of ADR clauses enforced deterministically" metric. Each mechanism is tested blocking a violation when it is built, in the phase that builds it (*Andy, 2 Nov*; Q6). Rule units (T6, proposed) would give each mechanism one testable shape.

### Q2. Quality layer tooling · Open

Choose a default tool for each E2 quality layer: journey step counts, accessibility, REST rules (stricter Spectral ruleset), breaking-change detection, API security, performance budgets and observability coverage. Commodity research: pick, check briefly, record.

**Open (added 30 Oct): how tool outputs reach the capability.** Most consumers need no model: the ratchet, the structural-commit check and the budget are comparisons. Proposed direction: a deterministic step reads each tool's native output into one small typed evidence record per change. Gates run on that record, and agents receive only the slice they must act on, such as the new violations in code they touched. Agents are organised around decisions, not tools. Test the record's shape with a spike on DEV-1's real outputs (with Q1, T4; A1's "structure what the system acts on").

### Q3. Validate the system dependency map · Open · Gate

Impact analysis and service-dependency ADRs both rely on knowing which services depend on which. Where does that map come from, and how do we know it's right?

Candidate sources, each seeing only part of the picture:

- Aspire AppHost service references (declared intent).
- Configuration: appsettings service URLs and connection strings.
- Container definitions: Dockerfiles and compose files.
- Code: HTTP client registrations and event subscriptions (eShop registers subscriptions explicitly, for example in the storefront's startup extensions).
- Runtime: OpenTelemetry traces from a running system show the dependencies that actually happen.

**Open:** which sources we combine; how we reconcile them; and whether declared dependencies can be compared with observed ones from traces, so drift between what the system says and what it does is detected automatically. Output: a validated dependency map consumed by T7 and Q1.

### Q4. Improving legacy code a change touches · Closed (ADR-016) · Gate

**Decided (5 Oct):** when a change touches a legacy domain, it also improves the code it touches.

**Decided (29 Oct, Andy):** this governs the capability, when it changes a legacy domain during an outcome. Hand-built development outcomes stay under CLAUDE.md hard rule 5: defects noticed are reported, not fixed. Recorded in [ADR-016](docs/adr/ADR-016-improving-legacy-code-the-capability-touches.md).

**Decided (30 Oct, Andy):** SARIF covers rule violations only. Measurement tools keep their native formats, because Stryker.NET and coverlet have no SARIF output. How outputs reach the capability is open (Q2).

- **Scope by touch radius.** Improve only the code the change already modifies (files or methods in the diff), not the whole domain. Deterministic: computed from the diff.
- **Separate structural from behavioural change.** Improvements go in their own commits, which must not change behaviour: existing tests stay green before and after, and the mutation score doesn't fall. Prior art: Kent Beck's "Tidy First?".
- **Budget, not target.** Cap improvement effort as a share of the outcome, for example structural diff relative to behavioural diff, or a share of the token budget. Lines changed is used only as a budget proxy, never as a measure of value, because it rewards churn. Thresholds pre-registered, like E3.
- **Over budget becomes a follow-up.** Improvements beyond the budget are proposed as a separate improvement outcome for the architecture coordinator, rather than done inline (A4, S7).
- **Checks on legacy domains are differential** (G7): a baseline of existing violations, recorded as exceptions (G12), and a ratchet so the count can fall but never rise.
- **Security defects in touched code are never ratcheted silently** (G10): fixed as their own behavioural change with a test and flagged, or escalated.
- **Measure with existing tools, not bespoke metrics.** Roslyn analyzers (severities versioned in .editorconfig), Microsoft's code metrics (complexity, maintainability, coupling), and SonarAnalyzer.CSharp (runs in a normal build, so it works headlessly for agents and CI). SonarQube for IDE (formerly SonarLint) is IDE-only, so it suits Andy's own editing, not the pipeline. Coverage via coverlet; mutation score via Stryker.NET. Check the Sonar analyzer's licence before adopting.
- **One output format: SARIF.** The ratchet, the repair loop and GitHub code scanning consume one format, and any tool can be swapped without changing the capability.
- **Rule IDs feed the repair loop**, as ADR IDs do: a violation names its rule, and the agent repairs against it.
- **Measure value by what got better:** primary, the ratchet delta (violations of the exemplar's rules removed in the touched code); secondary, complexity, coverage and mutation score of touched code, coupling and duplication; prioritise hotspots (code that changes often and is complex), after Adam Tornhill.
- **Report review burden:** the reviewable size of each change alongside the improvement it bought. The burden is accepted for now; reducing it is an improvement goal, not a launch requirement.
- **No outcome claims.** Fewer defects or faster future changes would need real history, which we won't have. The repo says so.

### Q5. Feature flags with OpenFeature · Partly decided · Gate

**Decided (5 Oct):** feature flags in the subject system use OpenFeature, the vendor-neutral feature flag standard, through its .NET SDK (A4, deliver dark). OpenFeature is an API, not a flag store, so a provider must be chosen.

**Open:**

- **Provider.** Likely flagd, OpenFeature's own flag daemon, which reads flag definitions from files and has a .NET provider and an Aspire Community Toolkit integration. The provider package has been renamed (OpenFeature.Contrib.Providers.Flagd to OpenFeature.Providers.Flagd), and Aspire's documentation still shows the old name: confirm the current package and SDK versions when pinning. Alternatives: an in-memory provider for tests; a hosted flag service (unnecessary for a demo).
- **Ownership.** Feature flags are a cross-cutting concern (A3): which steward owns the flag conventions, and which ADR governs them?
- **Flag definitions as code.** Flags defined in versioned files, validated by schema, so the capability creates and changes them through the same governed path as code.
- **Consistency across services.** A partly delivered feature may span the storefront and Ordering; both must evaluate the same flag the same way (shared flag key, shared evaluation context such as the user).
- **Testing.** Acceptance tests run with the flag off (nothing visible changes) and on (the feature works). Decide whether both states are part of the definition of done.
- **Lifecycle.** Flags become debt if never removed. Give each flag an owner and an expiry, like exceptions (G12), and propose a removal outcome once it has been fully on for a set period.
- **Link to P8:** whether experiments are in scope or only on/off release.

### Q6. Validation layers: checks at several points, ending in one that can't be bypassed · Open

Added 1 Nov. Q1's second axis says where in the flow a rule is checked. This item delivers the layers that exist for this repository, in Step 7 (*Andy, 2 Nov:* not a Gate; later mechanisms are tested in the phase that builds them). Under ADR-012@v2 C10, each outcome's expected results are written first. Q6 also asks for tests that show each check blocking as well as passing.

Where a final layer that can't be bypassed exists, it is CI plus branch protection, and it only sees committed changes. A script that only reads, for example from outside the allowlist, leaves nothing for CI to see. Only the OS sandbox would stop that, and whether to move to WSL2 is open (D1).

| ID | Outcome | Done when |
| --- | --- | --- |
| VL-1 | One rule has one definition, whichever layer runs it | Changing a rule in one place changes its result at every layer that runs it, shown on one rule |
| VL-2 | Plans are checked against the constitution | `tests/constitution/` runs whenever the constitution, CLAUDE.md or the `analyze` and `plan` skills change. Results are reported as catch and false-alarm rates per fixture, as evidence, not a gate (*Andy, 2 Nov*). Expected results are never edited; a wrong one gets a new dated expectation beside it. Started: see [results](tests/constitution/results.md) |
| VL-3 | Agents get fast feedback as they edit | ADR-011's hooks are tested: the build, format and test hook (C1) runs after an edit, and each blocking hook (C2, C3, C5) refuses a bad write and allows a good one. Covers a write outside the allowlist, and a write to an acceptance test path during implement. C2 needs the list of protected paths first (D1, open) |
| VL-4 | Reads outside the allowlist are refused | `blockReadsOutsideWorkingDirectories` is on in user settings, a test read outside is refused, and reads of memory, the scratchpad and skills still succeed |
| VL-5 | Mistakes are caught before they are committed | A pre-commit hook runs the same rules, and a commit that breaks one is refused. Built only if it earns its cost (see Open) |
| VL-6 | CI can't be skipped | CI in this repository runs the same rules on every pull request as a required check. A deliberately failing pull request can't merge. CI in the fork is a Phase 2 question, under hard rules 2 and 5 |
| VL-7 | Bypassing an early layer is caught later | A change committed with `--no-verify`, and a change written by a script that a hook can't see, are both caught at CI. Reads leave nothing to catch (see above) |
| VL-8 | Nothing reaches `main` except through the gate | Both repositories' rulesets require a pull request and passing checks (Andy adds these), and a direct push to `main` is refused |
| VL-9 | The ADR format is checked | A validator enforces ADR-000's mechanical constraints, the constitution's index, and the quoted hard rules, with a test showing each failure caught |
| VL-10 | Coverage is visible | Each ADR's enforcement entries name the layers that check it, and a report gives the share of constraints enforced deterministically, and the share with a check that can't be bypassed |

**Progress (3 Nov):** VL-3 is partly met. With `claude -p` on v2.1.317, the C2 ask rules, the C3 hook and the C5 write block each refused a bad write and allowed a good one. But C2's prompt isn't yet observed interactively, shell writes get past C2 and C3, and C1 runs only a syntax check, because there is nothing yet to build, format or test. (Since 2 and 3 Nov, C2 asks rather than blocks, and C5 is a setting, not a hook.) VL-4 is partly met from user settings. A read outside was refused, and memory, the scratchpad and saved tool output were still read. A user skill read with the Read tool prompted in `default` mode, with or without the block; reading skills through the Skill tool is untested. Neither has yet been observed in a desktop app session. Results: [tests/controls/results.md](tests/controls/results.md).

**Decided (4 Nov, Andy), CI for this repository** (Step 7, item 3):

- **GitHub Actions on Ubuntu and Windows,** both required to pass ("Ubuntu and Windows").
- **One aggregate required job, `checks`,** so suites can be added without editing the ruleset ("One job: checks"). *Revised the same day (Andy): "require the leaf checks too".* The author had reported that, during a GitHub Actions outage, `checks` passed while two of its needed jobs were still queued. The job logs later showed both had run first: GitHub's status display was lagging, so the reason given was wrong ([results](tests/ci/results.md)). Told of the correction, Andy ruled "Back to `checks` only", and the leaf checks were removed again.
- **Andy added the rulesets** (4 Nov): in this repository, a pull request is required (0 approvals) and `checks` must pass (its final, `checks`-only form was written by the author through the API at Andy's ruling); in the fork, a pull request is required (0 approvals). Neither has bypass actors.
- **The trailer check covers commits on `claude/*` branches,** and skips merge commits ("Commits on claude/* branches", then "Skip merge commits"). Hand-written commits on other branches stay unmarked.
- **CI runs the C1 check and the private-material guard on each pull request's changed files.** Changes to acceptance-test paths are reported, not failed, because CI can't tell implement from the stage that writes tests ("C1 check + guard; C3 reported").
- **No deliberately non-compliant commit is published to test the trailer check** ("Drop the C3 test PR").
- Not run in CI, the author's default: the live `claude -p` cases and `tests/constitution/`, which call a model.
- Results: [tests/ci/results.md](tests/ci/results.md).

**Progress (4 Nov):** VL-6 is met for this repository. CI runs on every pull request, the ruleset requires `checks`, and the API reported a deliberately failing pull request (#17) as blocked. CI in the fork remains a Phase 2 question. VL-7 is met for the guard's rule: a file that shell commands force-added past `.gitignore`, which no hook saw, was caught at CI. `--no-verify` skips nothing while there is no pre-commit hook. VL-8 is met for this repository: a direct push to `main` was refused. The fork's ruleset requires a pull request, but no push to it has been tried. Recorded in ADR-010 v2 (C5) and ADR-013 v2 (C6). **Open:** Claude sessions use Andy's admin-capable credentials, so a session could merge or loosen the ruleset; whether agents get a token without admin rights is not decided (review run 2).

**VL-9, progress (4 Nov):** the ADR validator (`scripts/adr.py`) enforces ADR-000 C2, C3, C5, C8 and C9 and ADR-009 C10, C14 and C17, and its tests show each failure caught ([tests/adr/](tests/adr/results.md)). It runs in the C1 hook on edited ADRs and in CI. Recorded in ADR-000 v4 and ADR-009 v3. ADR-000 C1, the front-matter schema, came after research. Andy, 4 Nov: "Code checks now; CUE question researched first", then "JSON Schema; record CUE finding in Q1". It is `scripts/adr-front-matter.schema.json`, and its 11 cases pass. VL-9 is met locally; its CI run is pending.

**Proposed principles** are under Q1. **Depends on:** the WSL2 question (D1, open). Without the sandbox, a script can get past every local layer, which is why VL-6 and VL-7 matter.

**Open:** the order of the outcomes in Step 7; whether VL-5 is needed once VL-3 and VL-6 exist; what CI runs on, given Windows and the eShop stack.

---

## Delivery

### D1. Ways of working: speeding up development · Partly decided · Gate

The decided parts are recorded in [ADR-010](docs/adr/ADR-010-working-model.md) (working model), [ADR-011](docs/adr/ADR-011-deterministic-controls-on-agents.md) (deterministic controls) and [ADR-012](docs/adr/ADR-012-independent-checks-and-staged-autonomy.md) (independent checks and staged autonomy).

**Decided (5 Oct):**

- **Principle: Andy's review attention is the bottleneck, not typing speed,** so the setup is designed around review capacity.
- **Two or three parallel tracks, not five.** Track A: the critical path. Track B: research (prior-art reading, spikes). Optional track C: chores (documentation, tooling). Each runs as a named session in the Claude Code desktop app, in its own git worktree.
- **The Spec Kit workflow (T1) is at the centre;** skills, subagents and hooks support its stages rather than replacing them.
- **Configure once, commit to the repo:** a CLAUDE.md pointing to the constitution and conventions; skills for writing an ADR from the template, running a research spike using the backlog method, and writing acceptance tests (D6); an adversarial reviewer subagent; hooks for deterministic gates (build, format and tests after edits; blocking writes to protected paths). *(Revised 2 Nov: protected paths ask rather than block; 3 Nov: they are ask rules, not a hook.)*
- **Build it the way the capability works (dogfooding).** Decisions become ADRs as backlog items close; deterministic checks gate every change; AI-authored work is marked in commits (Co-Authored-By trailer) so the project's own delivery metrics (share of AI-authored changes, review time, change failure rate) can be published alongside the product's results.
- **Keep evaluation material out of reach.** Hidden tests and labels live in a separate private repository that is never cloned into a build worktree. How it is run is E6.
- **Token use is monitored.**

**Open:**

- The token budget, and how it is enforced.
- Which components are fine as thin stubs (for example the capability's web interface, P5a) versus which must be deep.

**Prior art for the hooks (found 8 Oct):** *gates* (github.com/schwichtgit/spec-gates, MIT), a Spec Kit extension enforcing one policy at three boundaries: Claude Code hooks, git pre-commit and CI. Review before writing our own hooks. *Reviewed 3 Nov at v0.5.0:* design borrowed, code not adopted (see the 3 Nov decisions below).

**Decided (20 Oct), from a review of Anthropic's [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook):** Spec Kit stays the engine; the playbook supplies the loop around it (who acts at each stage, what each stage measures, how autonomy is granted).

- **A hook blocks writes to acceptance test paths during implement.** Hard rule 3 becomes a deterministic control, not just an instruction in CLAUDE.md. Review *gates* (above) first. Done when Q6's VL-3 passes.
- **The adversarial reviewer works to a written policy, `REVIEW.md`:** findings ranked by severity, nits capped. Without a policy its output can't be compared across runs. *Revised 20 Oct (Andy):* documentation PRs get four passes now (fidelity, facts, constraints, honest enforcement). The playbook's three code passes (bugs, security, compliance with spec and plan) are added when there is code.
- **Each skill gets a small regression eval set,** re-run whenever the skill, CLAUDE.md or a hook changes. Configuration is treated as code.
- **Each delivery stage is run by hand before it is automated, and each run is recorded on a loop card** ([docs/loops/](docs/loops/README.md)). A stage's autonomy is raised one level at a time, only when its cards meet the readiness criteria. The cards also give each stage a leading and a lagging indicator, which feeds the delivery metrics above.

**Open, from the same review:**

- The autonomy levels (0 to 4) and the readiness criteria in docs/loops are a first draft. Refine them after the first DEV-1 runs.
- Where the skill eval sets live and how they are run (with A5 and Q2).
- Whether low-risk stages (tasks, analyze) need a lighter loop card.
- **Research skill: look for parallel problems first (proposed by Andy, 1 Nov).** A discernment step in the flow, which may extend the planned research-spike skill: describe the problem; research or ideate on prior art, including the same problem solved under a different name in other fields; understand those results; then solve it with the prior art, or innovatively where it falls short. It came from asking whether ADR placement is the same problem as tool discovery, which reframed T6. Andy's working name is a "taste or discernment" skill. Build in Step 7.

**Decided (20 Oct, revised 21 Oct): file access is an allowlist,** switched on and tested with the other D1 hooks in Step 7.

- **Reads: the built-in setting `permissions.blockReadsOutsideWorkingDirectories`,** in user settings. It refuses Read, Grep, Glob and LSP outside the working directories in every permission mode, including bypass, and keeps Claude Code's own files under `~/.claude/` readable (skills, plugins, rules, agents, CLAUDE.md). Anything else Claude needs, such as the session scratchpad or saved tool output, is added through `additionalDirectories` in user settings. *Revised 21 Oct (Andy):* the 20 Oct decision assumed no such setting existed, and planned a hook for reads too. The review of this PR found the setting.
- **Writes: a `PreToolUse` hook** denies Edit, Write and NotebookEdit on any path outside the same allowlist, with no prompt to click through. The setting doesn't cover writes, and a deny rule can't carve out the project folder, because deny beats allow.
- **Backstop:** a deny rule naming the private evaluation repo's path (hard rule 1) was added to Andy's user settings on 20 Oct. It lives outside this public repo and hasn't been tested, because testing it means trying to read the repo. In one documented setup (no managed settings, and no Team or Enterprise login), a mod can approve a call that a deny rule refuses, so the rule is a backstop, not a guarantee.
- **Limit:** shell commands aren't refused the same way, and none of these controls contain a script that opens files itself (Python, Node). Only the OS-level sandbox does. It runs on macOS, Linux and WSL2, not native Windows (Claude Code's sandboxing documentation). Whether to move to WSL2 is open.

**Open:** the exact `additionalDirectories` list, settled while testing; whether the write hook also checks paths named in shell commands. *Update 3 Nov:* the list is settled as empty (tested, see below). The write hook was replaced by a built-in setting, so the shell question is now whether anything checks shell writes at all. Not ruled; the default in Step 7 is that nothing does. A test (L5) showed a shell redirect writing into `docs/adr/` in `bypassPermissions` mode with no prompt.

**Decided (2 Nov, Andy), for Step 7** ([brief](docs/sessions/2026-11-02-step7-brief.md)):

- **Protected paths:** `.specify/memory/constitution.md`, `docs/adr/`, `REVIEW.md`, `CLAUDE.md`, `.claude/settings*.json`, `tests/constitution/expected.md`, and `subject/` from this repository's side. Edits there need Andy's approval: they are asked for, not blocked outright.
- **Order:** the rule-unit spike (T6) first. The Claude Code controls and the bootstrap guard run in parallel as a second track, in their own worktree (ADR-010@v1 C2, exercised for the first time).
- **The rule-unit spike is written in Python,** in a spike folder. This doesn't decide T5.

**Decided (3 Nov, Andy), the Claude Code controls** (Step 7, item 4; recorded in [ADR-011](docs/adr/ADR-011-deterministic-controls-on-agents.md) v2, approved 3 Nov):

- **Protected paths are `permissions.ask` rules** in the committed `.claude/settings.json`, not a hook. Explicit ask rules are never auto-approved, in any mode.
- **Acceptance tests: policy globs and a stage marker.** A hook denies writes to the globs in `.claude/hooks/acceptance-tests.json` while `.specify/stage` reads `implement`, and asks otherwise. The marker is protected. The globs are placeholders until DEV-1 fixes the fork's layout.
- **Writes outside: the built-in `blockWritesOutsideWorkingDirectories`,** in project settings, replacing the planned write hook. Andy: "install the latest version of the sdk and continue from there", then "project settings". It needs Claude Code v2.1.314. The CLI v2.1.317 was installed with npm for testing. The desktop app bundles v2.1.309, so desktop sessions are covered once it updates.
- **spec-gates: borrow the design, not the code.** It needs bash, `jq` and POSIX paths, and its commit hook refuses the `Co-Authored-By` trailer.
- **Read block on in user settings, with no `additionalDirectories`** (Andy: "Yes, make the change").
- **`.github/` joins the protected paths** (4 Nov, Andy: "Protect .github/"), so an agent's change to the CI that checks it is asked for. Recorded in ADR-011 v3. Tests showed auto memory, saved tool output and the scratchpad stay readable without them.
- **Results:** [tests/controls/results.md](tests/controls/results.md).

**Open, from the same work:** wiring the stage marker into `/speckit-implement` (set by hand today); whether `.claude/hooks/` joins the protected paths, since an agent could edit the hook it is checked by; what the write block's removal of `EnterWorktree` does to the desktop app's worktrees; observing C2's prompt in an interactive session, which `claude -p` can't show; the desktop app starting sessions with `~/.claude` as an extra working directory, so the read block treats all of it as inside, `.credentials.json` included; and C1 as a syntax check until there is code, the author's default, not ruled. *Ruled 3 Nov (Andy): "fail to ask"*: the C3 hook asks when it can't evaluate a call.

**Decided (1 Nov, Andy): behaviour is tested before a PR.** No capability, skill, hook or constitution change opens a PR until its behaviour has been tested, with expected results written first. Recorded in [ADR-012](docs/adr/ADR-012-independent-checks-and-staged-autonomy.md) (v2, C10). The first example is [tests/constitution/](tests/constitution/README.md).

**Decided (20 Oct): the adversarial reviewer runs on every documentation PR now, by hand,** to [REVIEW.md](REVIEW.md), ahead of Step 7. It is a subagent with a fresh context that sees the diff and the sources, not the author's reasoning. It never approves: its findings and the author's responses go in the PR description, and Andy decides. *Revised 21 Oct (Andy):* while stages are hand-run, review comes before any push (D7), so findings are recorded on the run's loop card, committed on the branch for Andy's local review, then summarised in the PR. The first run, on batch 1 after it was merged, found 3 High problems the author had missed ([loop card](docs/loops/cards/2026-10-20-adr-batch1-review-run1.md)). Code review joins the policy when there is code.

### D2. Timebox and milestones · Closed (ADR-018)

**Decided (5 Oct):** no hard deadline. Quality comes first; work continues beyond the nominal one-week date, and we see where we end up. Milestones are defined by the evidence they produce, so each phase leaves something publishable ([roadmap.md](roadmap.md)). Sizing at the time: about five to seven weeks for the full scope.

### D3. Demonstration package · Open

Public repo, short video of a recorded run, and a one-command deploy. Decide what the video shows (likely one outcome in depth plus the scoreboard across all ten; rung 5, where the capability extends itself, is a strong candidate) and its length.

### D4. Prior-work IP check · Closed (ADR-018)

**Decided (5 Oct):** we build the best engineering solution and do not avoid ideas because they overlap with previous work. Any overlap is flagged to Andy, who has the final say on whether and how it is used. *Revised 30 Oct (Andy):* the flag applies to an idea that may overlap with Andy's previous employment, as CLAUDE.md says, so a suspected overlap is enough. The README carries no prior-work statement until Andy decides what it should say. Whether to take legal advice on past employment contracts is Andy's call; Claude is not a lawyer.

### D5. Rework the original document [B4] · Open

Likely unnecessary: product.md and backlog.md supersede the original capabilities document, so it can be archived. If kept: retire the sections written for earlier vehicle candidates (merchant ops agents, issue triage, incident investigation, Astronomy Shop hosting); keep what carries over (own repo with upstream code pinned, deploy only on demand, replay for repeatable evals where relevant, the video); map the original in-product and SDLC capability tables onto the two-part product, dropping rows with no natural home.

### D6. System-level acceptance test skill · Partly decided · Gate

**Decided (5 Oct):** Andy writes the reference acceptance tests with Claude Code, guided by a purpose-built skill. Search found generic test-driven development skills (unit-level red, green, refactor) but nothing for system-level acceptance tests in the four-layer model, so we build our own, using Anthropic's skill-creator and the existing TDD skills as reference. The skill is itself a portfolio artefact showing disciplined use of AI.

**Prior art to check before building (found 8 Oct, Spec Kit community catalogue):** the *reqnroll-bdd* and *bdd* extensions (Gherkin from specs, step scaffolding, coverage), the *tdd* extension (red-green evidence, mutation-checked) and the *test-first-governance* preset (BDD/ATDD scenarios with traceability). None appears to cover the four-layer model or hidden examples, but this updates the 5 Oct search; confirm before building our own.

**Decided (8 Oct):** the skill is **dry-run end to end on DEV-1 before any evaluation test is written** ([roadmap.md](roadmap.md), Phase 2): tests written, confirmed red, DEV-1 implemented, confirmed green, then mutation-tested to prove the method (E2). Recorded in [ADR-008](docs/adr/ADR-008-acceptance-tests-and-preregistration.md) (C16, C23); in the dry run, protocol drivers are built by Andy with Claude Code (C2).

What the skill covers:

- **Business-language test cases** per outcome, in the four-layer model: test cases, DSL, protocol drivers, system under test.
- **Extending the DSL** as new outcomes need new steps.
- **A stub protocol driver**, so the tests compile and run before any implementation exists.
- **Splitting visible from hidden examples.** Visible examples go into the outcome request and are the definition of done. Hidden examples cover cases the outcome didn't spell out (edge cases, failure paths, interactions) and check that the capability understood the outcome rather than satisfying a checklist. This mirrors what a domain expert does, which is what domain stewards stand in for.
- **Keeping hidden examples hidden:** they live in the private evaluation repo the capability can't access, and are published with the results, if results are published (P2; *revised 21 Oct, Andy*: previously "published after the scored run", which conflicted with P2's option not to publish).
- **Red first:** confirming every test fails against the subject before the change (for evaluation outcomes, the evaluation baseline tag).
- **Pre-registration:** committing tests and labels with a hash before the scored run.

**Open: who builds the exemplar's reference implementations.** If the plan comes from the capability's own stewards, the reference is produced by the system under test, and impact scoring would agree with the capability by construction. The reference implementations must also exist before the capability is built (E2). Proposed: an independent plan and implementation, made by Andy with Claude Code in a separate session using this skill. To decide.

### D7. Licence and repository hosting · Closed (ADR-013)

**Decided (21 Oct, Andy):** "pushes happen only after Andy's review" means nothing is pushed, not even a branch, until Andy has reviewed the change locally; main changes only through a PR he merges. Both rules apply **while stages are hand-run** (autonomy level 2 or below). Before any stage is automated, the rule is revised to gate `main` instead of pushes (D8). PRs #4 to #9 were pushed before his review. Neither repository's `main` ruleset requires a pull request today; adding that rule is recorded for Step 7. Recorded in [ADR-013](docs/adr/ADR-013-public-repo-licence-and-review.md).

**Decided (8 Oct):**

- **This repo is public on GitHub** ([a-douglas-lab/architect-in-the-loop](https://github.com/a-douglas-lab/architect-in-the-loop)), built in the open. Its dated history is part of the evidence of authorship.
- **MIT licence for everything** in this repo, code and documents. Options considered: no licence (all rights reserved; odd for a portfolio and deters reviewers from running it); source-available such as PolyForm Noncommercial (less familiar); MIT for code with CC BY 4.0 for documents. Ideas can't be protected by any licence; being visibly first and able to defend the work is the practical protection.
- **The eShop fork is public** (a fork of a public repo must be) and keeps eShop's MIT licence.
- **Repository rulesets:** `main` in both repos cannot be force-pushed or deleted; tags in the fork cannot be moved or deleted, so baseline and pre-registration tags are trustworthy.
- **Pushes happen only after Andy's review.** Private evaluation material is kept out by `.gitignore`, the bootstrap check and, from Step 7, Claude Code hooks.

### D8. The gate for automated delivery loops · Open

Added 21 Oct. ADR-013's "no push before Andy's review" holds only while stages are hand-run; it would block automated loops, and puts human review before the deterministic checks. Before any stage goes above autonomy level 2 (ADR-012@v1 C9, ADR-013@v1 C7), decide:

- **What reaches `main`, and how:** every change by pull request, required checks passing, and Andy's approval where the change's risk calls for it, mirroring the capability's own approval points (A1). How risk is assessed for the project's own changes.
- **Where agents push:** a private mirror where CI and the reviewer run, so nothing unreviewed is public; or public draft branches, visibly unreviewed work in progress.
- **What Andy samples** at level 3, and how often.
- **How the reviewer and loop cards fit** once there is no local review step: findings move to the PR.

Prior art: the AI-native SDLC playbook's tiered autonomy by environment, and branch protection as the human gate.
