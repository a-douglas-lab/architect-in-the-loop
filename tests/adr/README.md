# ADR validator tests

Behaviour tests for `scripts/adr.py`, the ADR validator and index generator (Step 7, item 2; backlog Q6, VL-9). Expected results are written and committed before each run (ADR-012@v2 C10), in [expected.md](expected.md). Results are in [results.md](results.md).

| Suite | What | Run |
| --- | --- | --- |
| A, F | The validator: ADR-000@v3 C1 (F, the front-matter schema), C2, C3, C5, C8, C9 and ADR-009@v2 C10, C14, C17 | `python -I tests/adr/test_adr.py`, in a venv with `requirements.txt` installed |
| K12–K14 | The C1 hook running the per-file checks on an edited ADR | `python -I tests/controls/test_hooks.py` |

Using the validator:

```bash
python -I scripts/adr.py check --base origin/main
```

```bash
python -I scripts/adr.py index --write
```

The first checks every ADR, the constitution's index and the quoted hard rules, and compares changed ADRs with `main`. The second regenerates the constitution's ADR index from front matter.

The front-matter schema (ADR-000@v3 C1) is `scripts/adr-front-matter.schema.json`, JSON Schema 2020-12 (Andy, 4 Nov: "JSON Schema; record CUE finding in Q1"). It needs the libraries pinned in `requirements.txt`. The per-file checks the C1 hook runs need none.
