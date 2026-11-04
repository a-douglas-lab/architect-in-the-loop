# CUE demo: results

Expectations: [demo-expected.md](demo-expected.md), committed before CUE was downloaded (`23dd744`).

- **The tool:** CUE v0.17.1 for Windows ARM64. The release has no checksums file; the downloaded zip's SHA-256, `db88b2c3…7102e51`, matched the digest GitHub publishes for the asset.
- **The command:** `python -I spikes/cue-reach/run_demo.py`, run once, on 4 Nov.

## Results

| Case | Expected | Exit | Error, first lines (temporary paths shortened) | Match |
| --- | --- | --- | --- | --- |
| Q1 | Pass | 0 | | Yes |
| Q2 | Fail, pointing at ADR-005 C6 | 1 | `request.areas_touched.2: conflicting values "ordering" and "basket"` … `"storefront-checkout" and "basket"`, citing `dev1.yaml` lines and `request.cue:26` | **Partly.** It fails, but the error doesn't name `adr005.cue`: `or(areas_listed)` reports the values it compared, not the clause |
| Q3 | Fail, pointing at ADR-005 C1 | 1 | `request.id: invalid value "EVAL-3" (out of bound =~"^DEV-[1-3]$")`, citing `adr005.cue:8:7` | Yes |
| Q4 | Fail, pointing at ADR-008 C8 | 1 | `request.examples.hidden: incompatible list lengths (0 and 1)`, citing `adr008.cue:6:10` | Yes |
| Q5 | Fail, pointing at the citation format | 1 | `plan.citations.0: invalid value "ADR-005 C6" (out of bound =~"^ADR-[0-9]{3}@v[0-9]+ C[0-9]+$")`, citing `adr009.cue:7:17` | Yes |
| Q6 | Fail, naming both values and both files | 1 | `#OutcomeRequest.stated_by: conflicting values "merchant" and "architecture-coordinator"`, citing `adr017.cue:4:29` and `adr099.cue:4:29` | Yes |
| Q7 | Pass | 0 | | Yes |
| Q8 | Fail, with no data (low-confidence prediction) | 1 | The same conflict as Q6, from the definitions alone | Yes |

All eight cases matched on pass or fail. Seven named the clause's file and line. Q2 named the values but not the clause.

## Measures

- **Size:** 23 lines of CUE for the 8 clauses, excluding comments, plus 19 for the shared definitions. ADR-017 C5 took 1 line; ADR-005 C1 and C6 together took 8.
- **Time:** 0.06 to 0.13 seconds a case.

## What this shows

- **Clauses from five ADRs, written as constraints on one shared outcome request, were checked together against DEV-1 before any code.** Each ADR's file adds to the definition, and loading the package loads them all.
- **A clash between two ADRs was caught by unification, with no request at all (Q8).** The error named both files. That is the conflict detection the backlog lists as a limit (T6) and the original document chose CUE for. It held here because both clauses constrain the same field of the same definition. A clash expressed through differently named fields would not be caught.
- **Error messages are usable, with one gap.** A constraint built from other fields (`or(areas_listed)`) reports values, not the clause. Naming each clause in its error would need a custom message, or a check wrapped around it.

## Limits

- **8 clauses of 173, chosen because they model cleanly.** They are not a random sample.
- **DEV-1's examples are placeholders.** The outcome request's shape is the author's invention: no such record exists yet.
- **One run, on Windows only.** CI cost, the Linux binary and the CUE learning curve for anyone else are untested.
- **Not compared with JSON Schema or OPA on the same clauses.** JSON Schema has no unification, so it would need a separate cross-ADR check for Q6 and Q8.
