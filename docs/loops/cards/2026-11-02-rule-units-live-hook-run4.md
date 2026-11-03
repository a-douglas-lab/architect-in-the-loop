# Loop card: analyze, with the rule-unit hook live · rule-unit spike · run 4

| Field | Value |
| --- | --- |
| Stage | Analyze, run against a test fixture, with the rule-unit MCP server called by a `PreToolUse` hook |
| Outcome | None: project work, Step 7 item 1 (T6) |
| Run | 4 (run 3 is the server build) |
| Date | 2026-11-02 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [MCP server build, run 3](2026-11-02-rule-units-server-run3.md) |

## 1. Purpose

Tests L1 to L4 in [server-expected.md](../../../spikes/rule-units/server-expected.md): in a real Claude Code session, does the hook fire before `speckit-analyze`, does its context reach the session, and does `analyze` catch f8?

## 2. Trigger and inputs

- **Trigger:** Andy, 2 Nov: "i can provide an API key if it means you can run the live hook run?", then "key file saved, go ahead and run it."
- **Inputs:** the spike at `e16fad0`; a neutral copy of f8 (`x02`); the generated settings and MCP config; Andy's key, read from a file outside the repository into the environment of each run only, never printed or written elsewhere.
- **Context loaded:** user and project settings (not local), CLAUDE.md, the auto-memory path the init event lists, the project's skills, the rule-unit server and its tool names.

## 3. Actor

- **Who:** the author ran Claude Code 2.1.316 headless (`claude -p`), installed in a scratch folder and removed afterwards.
- **Agent setup:** Claude Opus 5.5; tools Skill, Read, Glob, Grep, Bash and PowerShell; allowed shell command: the prerequisites script (two read-only `ls` commands were also accepted, one Bash command denied); spend capped at $2. The exact command is in results.md.
- **Human role:** Andy provided the key and the go-ahead. server-expected.md planned for Andy to run the session; the author did.

## 4. What happened

1. Run 1: `--setting-sources user` dropped the project's skills; the Skill call failed with "Unknown skill"; the hook didn't fire.
2. Run 2: `--setting-sources "user,project"`; the hook fired, the server called the API translator, `analyze` produced its report.
3. Evidence copied to `spikes/rule-units/runs/live/`; checked for the key (none).

## 5. Feedback loop

- **Signal:** the hook log and the report, scored against L1 to L4 afterwards.
- **Stop condition:** a report is produced.
- **Iteration cap:** not set; Andy's go-ahead covered running it.
- **Iterations taken:** 2 (one setup failure).

## 6. Output

- **Artefact:** [runs/live/analyze-f8-live-run2.md](../../../spikes/rule-units/runs/live/analyze-f8-live-run2.md); results in [results.md](../../../spikes/rule-units/results.md).
- **Feeds:** Andy's review; T6; the hook wiring with the controls track.

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| L1 hook fires | Deterministic (log) | One call, skill `speckit-analyze` | Pass |
| L2 context reaches the session | Inferred from the report | Report reflects the server's output | Pass, inferred: the transcript doesn't carry the context text |
| L3 f8 caught | Model, 1 run | A finding naming C10 or SARIF | Pass: CRITICAL |
| L4 no rules-file prompt | By construction | Prompt is the one sentence | Pass |
| Translator against the real API | Model, 1 call | Valid IDs, no fallback | Valid, no fallback; 2 terms more than the labels |
| Key not leaked | Deterministic | No `sk-ant-` in any saved file | Pass |

## 8. Gate

- **Approver:** Andy.
- **Evidence shown:** pending; this card, the report, the hook log and the transcripts.
- **Decision:** pending.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | Run 1, 14 s; run 2, 54 s, of which the hook took 8.0 s (shell timer: 17 s and 58 s) | `duration_ms` in each transcript; hook log |
| Tokens / cost | Run 1, $0.10; run 2, $0.19, excluding the translator's own API call | `total_cost_usd` in each transcript |
| Iterations | 2 | |
| Leading indicator | f8 caught through the live hook: 1 of 1 | Report |
| Lagging indicator | Breaches reaching implement although a unit covered them: not known | Needs real features |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| Run 1: skills not loaded | `--setting-sources user` also drops project skills | `user,project` | hook/README.md | No |
| Not blind | The worktree's folder name, "spike-rule-units-0fd90a", is in every path the session saw; the hook's text and the server's tool names name it too | Not fixed; recorded | results.md | Fill in on the next card |
| The model sees `get_rules` and `index` | The server offers every tool to the session | Not fixed; part of the wiring | delivery.md | Fill in on the next card |
| Translator returned 2 terms beyond the labels | Unknown from one call | Not fixed; recorded | results.md | Fill in on the next card |

## 11. Ready to automate?

- [ ] Stable inputs and outputs: one run
- [ ] A trustworthy check: L2 is inferred, and the translator's live output differs from the recorded one
- [ ] Known failures: blindness and tool visibility are open
- [ ] An evidence-based gate: Andy hasn't reviewed
- [ ] Known cost: about $0.19 a session; the translator call's cost isn't measured

**Verdict:** keep at level 1. **Why:** one unblind run.

**Next run changes:** a checkout whose path doesn't name the spike; hide `get_rules` and `index` from the session; three runs; log the translator call's tokens.
