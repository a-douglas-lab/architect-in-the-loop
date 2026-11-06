# CUE demo: results

Expectations: [demo-expected.md](demo-expected.md), committed before CUE was downloaded (`23dd744`), with a dated Q8 and Q9 added after review run 2 (`c7c3db4`).

- **The tool:** CUE v0.17.1 for Windows ARM64. The release has no checksums file. The downloaded zip's SHA-256 was `db88b2c302be1829e653e20ea87e3f1adc10ae2052d58fe87d21d0ed97102e51`, which matched the digest GitHub publishes for the asset. That digest comes from the same host as the file, so it isn't an independent check.
- **The model:** 8 clauses from six ADRs, in five files. ADR-000 C10 sits in `adr009.cue` with ADR-009 C13.
- **The command:** `python -I spikes/cue-reach/run_demo.py`.

## Run 1 (4 Nov)

Every case matched on exit code. Against the expectations as written, 7 of 8 matched. Q2's error didn't name the ADR-005 C6 constraint, though its expectation said it would. Of the six failing cases, five named their clause's file. The harness then compared exit codes only.

## Run 2 (5 Nov), after review run 2

Review run 2 found Q8 had no control. With `-c`, `cue vet` fails on any model given no data, because `request` and `plan` are incomplete. So Q8's exit code proved nothing; only its error text did. The runner now runs Q8 with `-c=false` and adds Q9, the same model with no clash. It also checks that each error names the expected files.

| Case | Expected | Exit | Error, first lines | Match |
| --- | --- | --- | --- | --- |
| Q1 | Pass | 0 | | Yes |
| Q2 | Fail, naming `adr005.cue` | 1 | `request.areas_touched.2: conflicting values "ordering" and "basket"`, citing `dev1.yaml` and `request.cue`, not `adr005.cue` | **No**: the constraint `or(areas_listed)` reports the values it compared, not the clause |
| Q3 | Fail, naming `adr005.cue` | 1 | `request.id: invalid value "EVAL-3" (out of bound =~"^DEV-[1-3]$")`, `adr005.cue:8:7` | Yes |
| Q4 | Fail, naming `adr008.cue` | 1 | `request.examples.hidden: incompatible list lengths (0 and 1)`, `adr008.cue:6:10` | Yes |
| Q5 | Fail, naming `adr009.cue` | 1 | `plan.citations.0: invalid value "ADR-005 C6" (out of bound …)`, `adr009.cue:7:17` | Yes |
| Q6 | Fail, naming `adr017.cue` and `adr099.cue` | 1 | `#OutcomeRequest.stated_by: conflicting values "merchant" and "architecture-coordinator"`, both files | Yes |
| Q7 | Pass | 0 | | Yes |
| Q8 | Fail, naming both files, no data, `-c=false` | 1 | The same conflict as Q6 | Yes |
| Q9 | Pass, no data, `-c=false` (control) | 0 | | Yes |

8 of 9 matched.

## Measures

- **Size:** 23 lines of CUE for the 8 clauses, excluding comments, plus 19 for the shared definitions.
- **Time:** 0.06 to 0.16 seconds a case.

## What this shows

- **Clauses from six ADRs, written as constraints on a shared outcome request and plan, were checked together against DEV-1, before any code.** Each ADR's file adds to the definitions, and loading the package loads them all.
- **A planted clash was caught by unification from the definitions alone (Q8, against its control Q9), naming both files.** It was `adr099.cue`, a test clause the runner writes, not a conflict between real ADRs. It is a literal against a literal on one field, the easiest case for unification. A conflict expressed through different fields wouldn't be caught.
- **Error messages are usable, with one gap.** A constraint built from other fields reports values, not its clause (Q2).

## Limits

- **8 clauses of 173, chosen because they model cleanly.**
- **The outcome request's shape is the author's invention, and DEV-1's examples are placeholders.** The model also checks only fields the request declares about itself (`areas_touched`). ADR-005 C6 governs what was actually changed, which needs the diff.
- **Windows only.** CI cost, the Linux binary and the learning curve for others are untested.
- **Not compared with JSON Schema or OPA** on the same clauses.
