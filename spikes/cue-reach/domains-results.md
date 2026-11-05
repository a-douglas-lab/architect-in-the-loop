# CUE across domains: results

Expectations: [domains-expected.md](domains-expected.md), committed before the model (`81ef63e`), with dated expectations after run 1 (`12c5deb`). Model: [domains/](domains/), an invented, eShop-flavoured module: canonical types, two cross-cutting policies (auth, data platform), a workflow capability, three domains (ordering, webhooks, payments) and a control package. Runner: `python -I spikes/cue-reach/domains_run.py`, with CUE v0.17.1 on Windows. The runner's version from run 1 was not committed; the committed one does runs 2 and 3.

## How to read the counts

- **Pre-registered** (`81ef63e`): pass or fail for 22 cases, and which files each error names, judged on one module-wide `cue vet -c ./...`. That is run 1.
- **Not pre-registered:**
  - **The failing package sets** used in run 2 were written after run 1. They copy run 1's output, and the author's per-package checks by hand of S1, X3 and W2. Run 2's agreement with them is a reproduction, not a confirmed prediction.
  - **The exploratory cases** came after run 2.

## Run 1 (5 Nov): pre-registered, one `cue vet -c ./...`

All 22 cases matched on pass or fail. With the named-files criterion, 16 of 22 matched. The six that didn't:
- **S1, X3, W2:** only one affected domain was reported (below).
- **X6:** a fault in the case. The edit left an unused import, a compile error ("imported and not used"), so the PII rule was never reached.
- **W3, I3:** the error named only the rule's file, not the domain's.

**Where the pre-registered wording implied which domains a change affects, two predictions were wrong:**
- **S1** predicted canon and webhooks. Canon itself passes; ordering, whose own event data breaks, fails.
- **W2** predicted payments only. Ordering's workflow uses the same 2-hour timeout and also fails.

**`cue vet ./...` reports only one failing package.** In S1, X3 and W2 the module-wide run showed one domain's error. Checked one package at a time, others failed too: webhooks in S1, payments in X3 and W2. **The `-E` (`--all-errors`) flag doesn't change this** (exploratory, below). So the per-package method is needed, not an artefact of CUE's default error limit.

## Run 2 (5 Nov): per-package mode, X6b added

Each case is also run for each package on its own, and the failing packages are recorded.

| Case | Scenario | Failing packages | Notes |
| --- | --- | --- | --- |
| B0, D1, S3, S5, I2 | Baseline; internal change; same-package removal; optional field; meaning change | none | S3 and I2 are predicted misses |
| D2 | Ordering breaks its own ADR | ordering | |
| S1 | Canonical field type change | ordering, webhooks | |
| S2, S4 | Canonical field removed or renamed; webhooks imports and refines | webhooks | **The case also updates ordering, the producer, to match.** Without that, ordering would fail too |
| S6 | Carriers narrowed | webhooks | **The case also moves ordering off the dropped carrier.** Without that, ordering would fail too |
| S7 | Currencies narrowed | payments | |
| X1, X4 | Auth: unlisted public endpoint; data: missing schemaVersion | ordering | |
| X2 | Authorisation: write endpoint, no roles | payments | |
| X3 | Auth policy tightens: admin needs MFA | ordering, payments | |
| X5 | Data-platform retention tightened to 90 days | webhooks | Payments isn't affected: the model exempts financial events from the general limit, a detail the expectations didn't mention |
| X6b | Canonical type drops the PII wrapper | payments | It fails on closedness (`classification: field not allowed`, payments' file only), **not because the data policy caught anything.** See X6c |
| W1 | Workflow rule broken | ordering | |
| W2, W3 | Workflow capability tightens, or adds a required field | ordering, payments | W3's errors cite only `workflow.cue`; the domain shows in the path |
| I3 | Audit and privacy rules on one event | payments | Its control is below |
| I4 | Domain contradicts a canonical type | webhooks | |

All 22 judged cases match the dated sets, which reproduces run 1. The runner prints "mismatches: 4 of 23" because it still checks named files. X6 still fails, as a broken case; W3, I3 and X6b don't name every expected file.

## Exploratory cases (after run 2, not pre-registered; now in the runner)

| Case | Result |
| --- | --- |
| S1, X3, W2 module-wide with `-E` | Each still reports one domain only |
| I3a: audit rule only | Payments passes |
| I3p: privacy rule only | Payments fails on its value: `invalid value 2555 (out of bound <=365)`. **So the original I3 had no control. The privacy rule alone fails it** |
| I3n: both rules, and the event gives no retention value | Payments fails: `incompatible integer bounds <=365 and >=2555`. The rules can't both hold for an event that is financial and PII, whatever its value |
| I3na: audit only, no retention value (control) | Payments passes |
| X6c: canon drops the PII wrapper, and payments drops the classification | **Every package passes.** The data platform's PII rule stopped applying, and nothing noticed |

## Impact discovery (I1)

- **CUE's commands:** its top-level commands are `cmd, completion, def, eval, export, fix, fmt, get, import, login, mod, trim, version, vet`. `cue mod`'s subcommands are `edit, fix, get, init, mirror, publish, registry, rename, resolve, tidy`; they manage module dependencies, not the packages that import a package.
- **Not checked:** CUE's Go API (`cue/load`), which resolves imports and could probably be used to build the graph.
- **The script:** `impact()`, 17 lines reading the import lines, gave:
  - canon: ordering, payments, webhooks;
  - capability/workflow: ordering, payments;
  - policy/data: canon, ordering, payments, webhooks;
  - ordering: none.

## What this answers

Andy's question: will clauses always reference the same field, and when a change in one place affects another domain, will CUE resolve it?

- **Clauses don't share fields by default.** They meet only where the model makes them meet: imported canonical types, policies and capabilities.
- **In this invented model, breaking changes to shared types, cross-cutting policies and the workflow capability failed the domains that use them,** when each package was checked on its own. That's run 1's pass/fail predictions plus the per-package reproduction.
- **Two conditions, each shown by one pair of cases:**
  1. **Import and refine shared definitions, don't redeclare them.** The same removal was caught across an import (S2) and missed in one package (S3).
  2. **Check each package on its own.** The module-wide check reported one domain, with or without `-E`.
- **A conflict between two cross-cutting rules was detected at rule level** (I3n against I3na), though only for an event carrying both flags. Both rules were invented together in one file. No conflict between real ADRs has been tested.
- **What CUE didn't do here:**
  - list the affected domains, which needs the import graph;
  - notice a change in meaning (I2);
  - notice a rule that stops applying (X6c);
  - always name the domain in its errors (I3, W3).
- **So CUE could serve as a compatibility check on change,** run per affected package, beside an impact step that reads the graph (T7, Q3). It isn't an impact analyser. Meaning changes, and rules that stop applying, still need review or a grader.

## Limits

- **An invented model:** three domains, small policies, written by the author to cover the scenarios.
- **One run per mode, Windows only.**
- **Review run 3 (5 Nov) found 1 High, 4 Medium, 5 Low and 5 nits,** all answered in this version: the counts are separated by when they were written; the `-E` flag and the I3 controls were run; the producer edits and the financial exemption are stated; `cue mod` was checked; X6c is in the runner. Unanswered: whether CUE's Go API lists dependants.
- **Not compared** with JSON Schema, OPA or contract tools (OpenAPI diff, AsyncAPI, Spectral).
- **X6b and X6 answer different questions:** X6b removes the PII wrapper; X6 was meant to test losing the classification.
