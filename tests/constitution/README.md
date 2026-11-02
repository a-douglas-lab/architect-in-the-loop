# Constitution behaviour tests

Tests that the constitution makes Spec Kit behave as ADR-009 intends. This is the first regression eval set under ADR-012@v2 C8. Re-run it whenever the constitution changes.

## How it works

- `fixtures/` holds small invented features (spec, plan, tasks) about the capability. They contain no evaluation outcomes and no real work.
- [expected.md](expected.md) states the expected result for each fixture. It is committed before any run, so expectations can't shift after seeing results.
- Each fixture runs three times through the real `speckit-analyze` skill, in a fresh context, on the model used for real work. The agent is told not to read `tests/`, and to read only what the skill tells it to; nothing enforces either. It also has the session's CLAUDE.md, which lists the hard rules.
- Fixture folder names give away the answers, so runs use copies under neutral names, without the "test fixture" label, kept outside `tests/`.
- `plan-check` runs the `speckit-plan` skill once on f2's spec, to see what the Constitution Check produces unprompted.
- [results.md](results.md) records actual against expected, per run.

Results are reported as catch and false-alarm rates per fixture, as evidence, not a gate (Andy, 2 Nov). `analyze` is a model following instructions, so one run proves little. Expected results are never edited after a run; a wrong one gets a new dated expectation beside it.

Prompts, the neutral copies and the agents' reports aren't committed, so the results can't be re-checked from the repository. Committing them is a candidate for the next run.
