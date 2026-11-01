# Constitution behaviour tests

Tests that the constitution makes Spec Kit behave as ADR-009 intends. This is the first regression eval set under ADR-012@v2 C8. Re-run it whenever the constitution changes.

## How it works

- `fixtures/` holds small invented features (spec, plan, tasks) about the capability. They contain no evaluation outcomes and no real work.
- [expected.md](expected.md) states the expected result for each fixture. It is committed before any run, so expectations can't shift after seeing results.
- Each fixture runs three times through the real `speckit-analyze` skill, in a fresh context, on the model used for real work. The agent never sees `expected.md`, and reads only what the skill tells it to.
- Fixture folder names give away the answers, so runs use copies under neutral names, without the "test fixture" label, kept outside `tests/`.
- `plan-check` runs the `speckit-plan` skill once on fixture 2's spec, to see what the Constitution Check produces unprompted.
- [results.md](results.md) records actual against expected, per run.

A fixture passes only if all three runs match. `analyze` is a model following instructions, so one pass proves little.
