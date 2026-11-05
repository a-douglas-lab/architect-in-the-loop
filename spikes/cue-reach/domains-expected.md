# CUE across domains: expected results

Written 2026-11-05, before any of this model exists. Andy asked: "do you think the cue schemas for ADR clauses will always reference the same field? … could have a change that impacts another domain and we have to understand that, so will CUE resolve that scenario". Then: "run the test first, ensure we've got coverage of scenarios we'll have, e.g., domain specific changes, cross cutting changes (e.g., authentication, authorisation, data platform), shared types/canonical types, capabilities like workflow that would be used across domains etc."

The first demo ([demo-results.md](demo-results.md)) only clashed a literal against a literal on one field. This test asks the harder questions. When one part of the system changes, does CUE flag the clauses elsewhere that the change breaks? And can the affected domains be found?

## The model (invented, eShop-flavoured, in `domains/`)

One CUE module with separate packages, so domains import what they share, as real teams would.

| Package | Stands for | Holds |
| --- | --- | --- |
| `canon` | Shared canonical types | `#Money`, `#CustomerRef` (with PII email), `#OrderShipped` event (order id, carrier, tracking number) |
| `policy/auth` | Cross-cutting ADR: authentication and authorisation | Every `#Endpoint` requires authentication unless it is on a public allowlist; write endpoints name at least one role; admin endpoints need MFA (added in X3) |
| `policy/data` | Cross-cutting ADR: data platform | Every `#Event` has a `schemaVersion` and a retention period within a limit; PII fields carry a classification; a privacy rule caps PII retention (added in I3) |
| `capability/workflow` | A shared capability | `#Workflow`: steps with side effects need a compensation; a step timeout has a maximum |
| `ordering` | A domain: produces `#OrderShipped` | Its own ADR clause (order status values), endpoints, an event, a workflow |
| `webhooks` | A domain: consumes `#OrderShipped` | Its ADR clause: the tracking number is a string it forwards. Its carrier list includes `DHL` |
| `payments` | A domain: uses `#Money` and workflow | Endpoints, a refund workflow, a payment event with PII |
| `samepkg` | A control for one modelling pitfall | A producer and a consumer declaring the same definition in one package, not importing it |

Each domain declares its endpoints, events and workflows as concrete values. Those values are the data. `cue vet -c ./...` checks everything at once. Each case edits one file in a temporary copy and reruns. A script lists which packages import which, to answer "which domains are affected".

## Cases and predictions

Confidence: H high, M medium, L low.

| Case | Scenario | Change | Expected | Conf. |
| --- | --- | --- | --- | --- |
| B0 | Baseline | None | Pass | H |
| **Domain-specific** | | | | |
| D1 | Internal change | Ordering adds a field to its own internal type, used by no one else | Pass. Impact script: ordering only | H |
| D2 | Domain breaks its own ADR | Ordering uses an order status its ADR doesn't allow | Fail, naming ordering's ADR file only | H |
| **Shared and canonical types** | | | | |
| S1 | Type change | `#OrderShipped.trackingNumber` becomes an int | Fail, naming canon and webhooks | H |
| S2 | Removal, consumer imports and refines | canon drops `trackingNumber`; webhooks refines `canon.#OrderShipped` to require it | Fail ("field not allowed", from closedness across the import) | M |
| S3 | Removal, same package | In `samepkg`, the producer drops the field; the consumer's own declaration of the same definition still requires it | **Pass: missed.** The two declarations merge, so the field quietly comes back | M |
| S4 | Rename | canon renames `trackingNumber` to `trackingNo` | As S2: fail | M |
| S5 | Optional addition | canon adds an optional `estimatedDelivery` | Pass | H |
| S6 | Narrowed values | canon narrows carriers to `"royal-mail" \| "ups"`; webhooks' list includes `DHL` | Fail, naming canon and webhooks | H |
| S7 | Shared money type | `#Money.currency` narrows to `"GBP" \| "EUR"`; payments has a `USD` value | Fail, naming payments' value | H |
| **Cross-cutting** | | | | |
| X1 | Authentication | Ordering adds an endpoint with `auth: "none"`, not on the allowlist | Fail, naming the auth policy | H |
| X2 | Authorisation | A payments write endpoint has no roles | Fail, naming the auth policy | H |
| X3 | A cross-cutting rule tightens | The auth policy adds "admin endpoints need MFA"; ordering and payments each have an admin endpoint without it | Fail, with errors in **both** domains. The errors are the impact list | H |
| X4 | Data platform | An ordering event loses `schemaVersion` | Fail, as incomplete or missing | H |
| X5 | Data platform tightens | The retention limit drops from 365 to 90 days; webhooks' event keeps 180 | Fail, naming webhooks' value | H |
| X6 | PII classification | canon `#CustomerRef.email` loses its classification | Fail, naming the data policy | M |
| **Shared capability: workflow** | | | | |
| W1 | Capability rule broken | An ordering workflow step with a side effect has no compensation | Fail, naming the workflow capability | H |
| W2 | Capability tightens | The maximum step timeout drops from 24h to 1h; payments' refund step uses 2h | Fail, naming payments | H |
| W3 | Capability adds a required field | `#Workflow` gains a required `owner`; no domain sets it | Fail, once for each domain with a workflow | H |
| **Limits and conflicts** | | | | |
| I1 | Which domains are affected | For S1's change, list the packages that import `canon` | The impact script lists ordering, webhooks and payments. CUE itself offers no command for this (to be confirmed); its errors name only the domains a change *breaks* | M |
| I2 | A meaning change that is type-compatible | `#Money.amount` changes from pounds to pence, still an int | **Pass: missed.** CUE checks shape and values, not meaning | H |
| I3 | Two cross-cutting ADRs conflict | The data policy gains an audit rule (financial events kept at least 2,555 days); a privacy rule caps PII retention at 365. A payments event is both financial and PII | Fail: the two ADRs can't both hold for that event, naming both policies | M |
| I4 | A domain overrides a canonical rule | webhooks redeclares `trackingNumber: int` locally while refining canon's `string` | Fail | H |

## What would count as an answer to Andy's question

- **Changes that break other domains (S1, S2, S4, S6, S7, X3, X5, W2, W3, I3, I4):** CUE flags them, and its errors name the domains affected.
- **Modelling pitfalls (S3):** whether the convention matters, in practice.
- **Limits (I1, I2):** what CUE doesn't do. Finding the affected domains is a graph question. A change in meaning is invisible to shape checks.
