# CUE across domains: results

Expectations: [domains-expected.md](domains-expected.md), committed before the model (`81ef63e`), with dated expectations after run 1 (`12c5deb`). Model: [domains/](domains/), an invented, eShop-flavoured module: canonical types, two cross-cutting policies (auth, data platform), a workflow capability, three domains (ordering, webhooks, payments) and a control package. Runner: `python -I spikes/cue-reach/domains_run.py`, with CUE v0.17.1 on Windows.

## Run 1 (5 Nov): one `cue vet -c ./...`

16 of 22 matched. Three findings changed the method:

- **`cue vet ./...` reported only one failing package,** even when others failed with different errors. In S1, webhooks fails on its own (`#ShippedHook.trackingNumber: conflicting values string and int`), but the module-wide run showed only ordering's error. In X3 it was payments, and in W2 payments again. Checked one package at a time, every affected domain failed.
- **X6 was a fault in the case.** The edit left an unused import, a compile error, so the PII rule was never reached.
- **Some errors name only the rule's file, not the domain's.** I3 cites two lines of `data.cue`, and W3 cites `workflow.cue`. The domain shows only in the field path (`events.captured`, `workflows.refund`).

## Run 2 (5 Nov): per-package mode, X6b added

Each case is also run once for each package; the packages that fail are the affected domains.

| Case | Scenario | Result | Failing packages (expected) | Match |
| --- | --- | --- | --- | --- |
| B0 | Baseline | Pass | none (none) | Yes |
| D1 | Internal change in ordering | Pass | none (none) | Yes |
| D2 | Ordering breaks its own ADR | Fail: `sampleOrder.status: conflicting values …`, ordering only | ordering (ordering) | Yes |
| S1 | Canonical field type change | Fail | ordering, webhooks (same) | Yes, in run 2 |
| S2 | Canonical field removed; consumer imports and refines | Fail: `#ShippedHook.trackingNumber: field not allowed` | webhooks (webhooks) | Yes |
| S3 | Same removal, consumer in the same package | **Pass: missed** | none (none) | Yes: predicted miss |
| S4 | Canonical field renamed | Fail: `field not allowed` | webhooks (webhooks) | Yes |
| S5 | Optional field added | Pass | none (none) | Yes |
| S6 | Carrier values narrowed | Fail: `sample.carrier: conflicting values …` | webhooks (webhooks) | Yes |
| S7 | Money currencies narrowed | Fail: `fxCharge.currency …` | payments (payments) | Yes |
| X1 | Authentication: unlisted public endpoint | Fail, citing `auth.cue` | ordering (ordering) | Yes |
| X2 | Authorisation: write endpoint, no roles | Fail: `incompatible list lengths`, `auth.cue` | payments (payments) | Yes |
| X3 | Auth policy tightens (admin needs MFA) | Fail: `endpoints.1.mfa: conflicting values true and false` | ordering, payments (same) | Yes, in run 2 |
| X4 | Data platform: event loses schemaVersion | Fail: `incomplete value >=1 & int` | ordering (ordering) | Yes |
| X5 | Data platform tightens retention | Fail: `invalid value 180 (out of bound <=90)` | webhooks (webhooks) | Yes |
| X6b | Canonical type drops the PII wrapper | Fail: `classification: field not allowed`, citing only `payments.cue` | payments (payments) | Partly: canon not named (low-confidence prediction) |
| W1 | Workflow rule broken (no compensation) | Fail: `incomplete value string`, `workflow.cue` | ordering (ordering) | Yes |
| W2 | Workflow capability tightens timeout | Fail | ordering, payments (same) | Yes, in run 2 |
| W3 | Workflow capability adds a required field | Fail, once per workflow | ordering, payments (same) | Yes by package; the error text names `workflow.cue` only |
| I2 | Meaning change (pounds to pence), same type | **Pass: missed** | none (none) | Yes: predicted miss |
| I3 | Two cross-cutting ADRs conflict (audit and privacy retention) | Fail: `incompatible integer bounds <=365 and >=2555`, two `data.cue` lines | payments (payments) | Yes by package; the error doesn't name payments' file |
| I4 | Domain contradicts a canonical type | Fail | webhooks (webhooks) | Yes |

**All 22 judged cases matched on which domains fail.** On the file names in the error text, 19 of 22 matched (X6b, W3 and I3 did not).

**I1, which domains a change affects.** CUE v0.17.1's commands (`cmd, completion, def, eval, export, fix, fmt, get, import, login, mod, trim, version, vet`) include none that lists the packages depending on another. A 20-line script reading the import lines gave the impact sets:
- canon: ordering, payments, webhooks;
- capability/workflow: ordering, payments;
- policy/data: canon, ordering, payments, webhooks;
- ordering: none.

**X6c, exploratory, not pre-registered.** Canon drops the PII wrapper, and payments drops the classification too. **Every package passes.** The data platform's PII rule stopped applying, and nothing noticed.

## What this answers

Andy's question: will clauses always reference the same field, and when a change in one place affects another domain, will CUE resolve it?

- **Clauses don't share fields by default.** They meet only where the model makes them meet, through imported canonical types, policies and capabilities. In this model that covered every cross-domain case tested.
- **Breaking changes are caught, and attributed to domains, but only if two conditions hold:**
  1. **Domains import and refine shared definitions** rather than redeclaring them. S2 against S3 is the proof: the same removal is caught across an import and missed in one package.
  2. **Each package is checked on its own.** The module-wide command under-reports.
- **Type changes, narrowed values, removals, renames and tightened policies all break the right domains:** shared types (S1, S2, S4, S6, S7), cross-cutting policies (X3, X5), the workflow capability (W2, W3), and a conflict between two cross-cutting ADRs (I3).
- **What CUE doesn't do:**
  - **Impact discovery.** Finding the affected domains needs the import graph, which CUE doesn't expose. The breakage per domain needs a per-package run.
  - **Changes in meaning** (I2).
  - **A rule that silently stops applying** (X6c). A canonical type stepping out from under a cross-cutting policy breaks nothing.
  - **Error text doesn't always name the domain** (I3, W3).
- **So CUE could be a compatibility check on change,** run per affected package, beside an impact step that reads the graph (backlog T7, Q3). It isn't an impact analyser, and it can't see changes in meaning or a rule that stops applying, which still need review or a grader.

## Limits

- **An invented model.** Three domains, small policies, written by the author to cover the scenarios. Real eShop types, events and contracts are larger, and live in the fork.
- **One run per mode, Windows only.**
- **Not compared with JSON Schema, OPA, or contract tools.** Breaking-change detection exists elsewhere (OpenAPI diff, AsyncAPI, Spectral), and backlog Q1 lists it.
- **X6c is exploratory.** It was run after the results, not pre-registered.
