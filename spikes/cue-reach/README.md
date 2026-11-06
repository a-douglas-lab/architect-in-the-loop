# CUE reach: which ADR clauses could CUE check?

Andy, 4 Nov: "have you modelled typical adr clauses and whether we can model these in Cue schemas, and load them against an outcome request", and "yes measure CUEs real reach". This measures it, for backlog Q1's open question ("does CUE earn its learning curve over JSON Schema plus OPA"). Method and predictions are committed before any clause is classified.

## Method

The population is every active constraint in `docs/adr/` at `origin/main` `67b1bd4`. That's 173: 174 constraint lines, minus ADR-000 C4, the only withdrawn one. Review run 1 corrected an earlier count of 171, which came from a case-insensitive filter.

`clauses.csv` gives each constraint:

| Column | Meaning |
| --- | --- |
| `kind` | **V**, a value on an artefact: the clause fixes a value or range in a file or document (SARIF version, a threshold). **R**, process with a record: compliance shows in a record that is or could be data (git history, the GitHub API, a structured file such as front matter or a plan). **J**, judgement: compliance needs reading for meaning, so a rubric or a human. **X**, no witness: compliance leaves no trace any record would hold, such as a read that was never made |
| `witness` | The record that would show compliance, or "none" |
| `exists` | Whether that record exists as data today: yes, partly (it exists but isn't structured), or no |
| `pre_code` | Whether the clause could be checked against an outcome request, before any code: against the outcome, its spec and plan, or an impact record. yes or no |
| `note` | Anything that makes the call unclear |

"CUE can check it" means V or R, and the witness exists, or partly exists. For a CUE check, the record is read as data and the clause is written as a CUE constraint over it. Conflict detection by unification also needs two clauses to constrain the same field of a shared definition. That is counted separately: the clauses that constrain a field another clause also constrains.

**Limits, stated before the run.**
- **One rater, the author,** classifies, and the kinds need judgement at the edges. A second, blind rater would show how reliable the classes are. That's not done here; Andy can ask for it.
- **No CUE is run.** The CUE examples are sketches, until a download is approved.

## Predictions (before classifying)

| Measure | Predicted share of 173 |
| --- | --- |
| V | 3% |
| R | 40% |
| J | 40% |
| X | 17% |
| CUE can check it today (V or R, witness exists or partly) | 25% |
| Checkable against an outcome request, before code (`pre_code` yes) | 20% |
| Constrains a field another clause also constrains (unification could compare them) | 5% |

Results go in [results.md](results.md).
