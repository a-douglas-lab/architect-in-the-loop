# Rule-unit spike

Step 7, item 1 (backlog T6, "Rule units"). Python, in a spike folder; it doesn't decide the capability's stack (T5).

Each ADR constraint, or hard rule, becomes a unit with an identity, applicability, a check or rubric, and tests. Units are selected deterministically from glossary terms, then checked, and the result is reported as one typed record.

| File | Holds |
| --- | --- |
| [prior-art.md](prior-art.md) | Problem, criteria, prior art, and the shape Andy approved |
| [expected.md](expected.md) | Method and predictions, committed before any run |
| [results.md](results.md) | What happened, as rates |
| [delivery.md](delivery.md) | Recommendation: MCP server, skill, or a step before `analyze` |
| [glossary/](glossary/) | The ubiquitous language: capability terms, and subject terms standing in for the contract |
| [units/](units/) | Three units and four decoys; `index.yaml` is generated from them |
| [fixtures/](fixtures/), [labels.yaml](labels.yaml) | Eight new fixtures; labels for all 17 |
| [runs/](runs/) | Prompts, raw model outputs, scores and `analyze` reports |
| `ruleunits/`, `tests/` | The runner and its tests |

## Run it

From this folder, with Python 3.13, PyYAML and pytest:

```bash
python -m pytest -q
```

```bash
python -m ruleunits index
```

```bash
python -m ruleunits eval-deterministic
```

```bash
python -m ruleunits rules-file ../../tests/constitution/fixtures/f8-subtle-breach rules.md
```

Model runs (the constrained translator, the title baseline, the rubric, `analyze`) were made by fresh subagents with the prompts in `runs/prompts/`; their outputs are scored with `python -m ruleunits eval-model`.

The fake subject tree under `units/hard-rule-4-copy/tests/trees/subject/` is invented for the test; nothing in it comes from eShop.
