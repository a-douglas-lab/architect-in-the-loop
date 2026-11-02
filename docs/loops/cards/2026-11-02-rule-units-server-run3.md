# Loop card: build, the rule-unit MCP server · rule-unit spike · run 3

| Field | Value |
| --- | --- |
| Stage | Build and behaviour test (spike code) |
| Outcome | None: project work, Step 7 item 1 (T6) |
| Run | 3 (run 2 is the `analyze` re-run with rule units) |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Analyze with rule units, run 2](2026-11-02-rule-units-analyze-run2.md) |

## 1. Purpose

Builds the step that joins translate, validate, select, check and report, as an MCP server for a hook or an orchestrator to call, and tests its behaviour against expectations written first.

## 2. Trigger and inputs

- **Trigger:** Andy, 2 Nov: "make sure you add the step that joins the parts (MCP server called by a hook/orchestrator), this feels like a roadmap you decided."
- **Andy's build choices:** the Anthropic API translator with an alias fallback; the MCP Python SDK (mcp 2.3.0) in a spike venv; a live hook run from a spike settings file, which he runs.
- **Inputs:** the spike at `d96d26c`; [server-expected.md](../../../spikes/rule-units/server-expected.md) and the tests, committed in `c7b89cb` before the code; the Claude Code hooks reference for `mcp_tool` hooks; Spec Kit's feature-folder resolution in `.specify/scripts/powershell/common.ps1`.

## 3. Actor

- **Who:** the author, in this session. No subagent; no model calls.
- **Human role:** Andy chose the translator, the dependency and the live-test route before the build.

## 4. What happened

1. Expected results J1 to J9, H1 to H5, M1 to M4 and L1 to L4 written, with tests for all but L, and committed; the new tests failed.
2. `translate_model.py`, `join.py`, `server.py` and `hookfiles.py` written.
3. pytest: J3 failed as written (below); everything else passed.
4. Two tests added after the code, both passing: the generated config end to end, and a failing client constructor (J6b).

## 5. Feedback loop

- **Signal:** pytest.
- **Stop condition:** every pre-registered test passes, or a failure is recorded.
- **Iteration cap:** not set.
- **Iterations taken:** 2 (one failing run, one after J3's test was corrected and a credentials bug fixed).

## 6. Output

- **Artefact:** `spikes/rule-units/ruleunits/join.py`, `server.py`, `translate_model.py`, `hookfiles.py`; [hook/README.md](../../../spikes/rule-units/hook/README.md); results in [results.md](../../../spikes/rule-units/results.md).
- **Feeds:** Andy's live run; T6; Step 7 item 4 (hooks), with the controls track.

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| Joined step, J1 to J9 | Deterministic | As in server-expected.md | Pass after J3's test was corrected |
| Hook contract, H1 to H5 | Deterministic | As written | Pass |
| Server over stdio, M1 to M4 | Deterministic, real subprocess | As written, `legacy` and `auto` modes | Pass |
| Generated config end to end | Deterministic | C10 in the context; call logged | Pass (test written after the code) |
| Live hook, L1 to L4 | Model, 1 run | As written | Not run: no CLI or key here |
| Model translator against the API | Model | Valid IDs returned | Not run: no credentials |

## 8. Gate

- **Approver:** Andy.
- **Evidence shown:** pending; this card, server-expected.md, results.md and the code, for local review and the live run.
- **Decision:** pending.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | Not timed | |
| Tokens / cost | No model calls | |
| Test run | 49 passed, 3 expected failures, about 10 s | pytest |
| Fallback with no credentials | About 3 s, mostly importing the SDK | `measurements.duration_ms` |
| Leading indicator | Hook contract tests passing: 5 of 5 | pytest |
| Lagging indicator | f8 caught through the live hook: not known yet | Fill in after Andy's run |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| J3's test asked for exactly one finding; f4 has two (spec and plan) | The test was stricter than its written expectation, "a finding" | Test corrected to match the expectation, with a comment; recorded in results.md | tests/test_join.py | Fill in on the next card |
| The client was built outside the `try`, so missing credentials would have raised instead of falling back | Order of statements | Moved inside the `try`; test J6b added for a failing constructor | translate_model.py, tests/test_join.py | Fill in on the next card |
| "FastMCP" import failed | mcp 2.x renamed it `MCPServer` | Used the 2.x API, after reading the installed package | server.py | n/a |

## 11. Ready to automate?

- [ ] Stable inputs and outputs: the hook's input field for the skill name is assumed, not confirmed
- [x] A trustworthy check: the contract tests run a real subprocess over the real protocol
- [ ] Known failures: the live run hasn't happened
- [ ] An evidence-based gate: Andy hasn't reviewed
- [ ] Known cost: the model translator's cost per call isn't measured

**Verdict:** keep at level 1. **Why:** the live hook and the real API call are unproven.

**Next run changes:** Andy's live run; confirm the Skill tool's input field from the hook log.
