# Loop card: implement · Step 7 controls and bootstrap guard · run 1

| Field | Value |
| --- | --- |
| Stage | Implement, with research first and behaviour tests (no Spec Kit feature folder: project tooling) |
| Outcome | None: project work, Step 7 items 4 and 6 |
| Run | 1 |
| Date | 2026-11-02 to 2026-11-03 |
| Autonomy level | 1, drafted: the agent built, Andy chose at four decision points and approved the user-settings change |
| Session | [Session log](../../sessions/2026-11-03-step7-controls.md) |
| Previous card for this stage | First run |

## 1. Purpose

This run turns ADR-011's planned controls into working, tested ones, so the rules that matter most hold even when an agent gets them wrong.

## 2. Trigger and inputs

- **Trigger:** the Step 7 plan, approved by Andy on 2 Nov; this track ran in parallel with the rule-unit spike.
- **Inputs:** the [Step 7 brief](../../sessions/2026-11-02-step7-brief.md), ADR-011@v1, backlog D1 and Q6 at `624a523`, `scripts/bootstrap.*`, spec-gates v0.5.0, and the Claude Code docs as fetched on 3 Nov.
- **Context loaded:** CLAUDE.md, the brief, ADR-011, ADR-012, ADR-000, backlog D1 and Q6. Missing: where acceptance tests live, and how a hook knows it is "during implement". Both went to Andy.

## 3. Actor

- **Who:** an agent (Claude Opus 5.5 in the desktop app, v2.1.309), with Andy deciding.
- **Agent setup:** a worktree session. Live tests drove `claude -p` v2.1.317 with `claude-sonnet-5-5`.
- **Human role:** chose among options at four points, asked for the CLI to be installed, signed it in, chose where the write block lives, and approved the user-settings change after seeing it.

## 4. What happened

1. Read the brief and sources, then reviewed spec-gates and the Claude Code docs. Found the built-in write block and that the installed CLI was too old for it.
2. Brought findings and four questions to Andy. He chose ask rules, globs plus marker, and design-not-code. For the write block he replied "install the latest version of the sdk and continue from there".
3. Wrote the guard's expected results and committed them (`f5a9ea1`), then built and tested the guard.
4. Wrote the hooks' and live cases' expected results and committed them (`e678923`), then built and unit-tested the hooks.
5. Installed the npm CLI at 2.1.317. It wasn't signed in, so Andy signed it in. He chose project settings for the write block.
6. Ran the live cases, then wrote the read-block expectations (`60beb57`) and ran those.
7. Showed Andy the exact user-settings change. He approved, the change was made, and it was tested from user settings (`68c3009`, then the run).
8. Drafted ADR-011 v2 and updated the backlog, this card and the session log.

## 5. Feedback loop

- **Signal:** test runners comparing each case with the expected results committed before the run; for live cases, the disk and `permission_denials`, not the model's words.
- **Stop condition:** every case run, every miss explained, no expectation edited.
- **Iteration cap:** none set.
- **Iterations taken:** guard 1; hook units 2 (one fix); live 1 plus two single-case re-runs to diagnose harness faults.

## 6. Output

- **Artefacts:** `scripts/check-private-material.*`, `.claude/settings.json`, `.claude/hooks/`, `tests/controls/`, Andy's `~/.claude/settings.json` (outside the repository), and the ADR-011 v2 draft, all on `claude/step7-controls-cc0237`.
- **Feeds:** Andy's review; CI (Step 7, item 3), which should run `tests/controls/test_hooks.py` and the guard tests.

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| Guard G1–G10, both shells | Deterministic | Match expected | 10 of 10, both shells |
| Hook units H1–H15, K1–K10 | Deterministic | Match expected | 23 of 25, then 25 of 25 after a fix |
| Live L1–L11 | Deterministic control, model as driver | Match expected | 9 of 11: one wrong prediction (L7), one harness fault (L10) |
| Read R1–R8 | Same | Match expected | 4 of 8: three wrong predictions (R2 to R4), one harness fault (R8) |
| User settings U1, U3, U4, U7 | Same | Match expected | 4 of 4 |
| Adversarial review of the documentation | Rubric (REVIEW.md) | No unresolved High | See section 10 |

The wrong predictions are recorded, not corrected: they came from docs that say less than the tool does.

## 8. Gate

- **Approver:** Andy, as architecture coordinator.
- **Evidence shown:** the research findings with options; the exact user-settings change; this branch, for local review.
- **Decision:** pending his review.
- **Did the approver redo any of the work to decide?** Not yet known.

## 9. Measurements

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | Not measured: the session spanned two days with waits for Andy | |
| Human minutes (work plus review) | Not measured | |
| Tokens / cost | Live cases: about $0.06 each on the one where cost was read (L10); 23 live cases (L 11, R 8, U 4) and 3 diagnostic re-runs, plus 2 smoke-test attempts that failed before sign-in. This session's own tokens not measured | `modelUsage` in the stream output |
| Iterations to pass checks | 2 for the hook units; 1 elsewhere | Test runs |
| Leading indicator | Share of cases matching expectation on the first run: 52 of 56 for G, H, K and L (G 20 of 20 across both shells, H and K 23 of 25, L 9 of 11); R 4 of 8; U 4 of 4 | results.md |
| Lagging indicator | Controls failing in real use. Fill in when known | |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| Hook crashed on `.sh` files | Only Git's `cmd` folder is on PATH, so no bash | Look for Git Bash beside `git` | Hook | Fill in on the next card |
| L10 judged "reason not seen" | `-p` stream output doesn't carry `PostToolUse` reasons | Harness reads the hook debug log | `run_live.py` | |
| R8 judged "refused" | Model passed `limit: 1`; marker on line 2 | Prompt asks for the whole file | `run_live.py` | |
| Three read predictions wrong | Docs name fewer readable paths than the tool allows | None needed; recorded | results.md | |
| The planned write hook duplicated a setting | Docs changed after ADR-011@v1 | Checked the current docs before building | ADR-011 v2 draft | |

Did a failure send work back to an earlier stage? Yes: the C5 mechanism went back to Andy, who chose the built-in.

## 11. Ready to automate?

- [ ] Stable inputs and outputs
- [x] A trustworthy check: the hook and guard tests are deterministic
- [ ] Known failures
- [ ] An evidence-based gate
- [ ] Known cost

**Verdict:** keep at level 1. **Why:** first run; the controls are not yet observed in the desktop app, and CI doesn't yet run the tests.

**Next run changes:** run `test_hooks.py` and the guard tests in CI; observe C2 to C5 in a desktop session once the app runs v2.1.314 or later; replace the placeholder globs once DEV-1 fixes the fork's layout.
