# Loop card: <stage> · <outcome> · run <n>

How to use this template: [README.md](README.md). Delete the guidance in italics as you fill each section.

| Field | Value |
| --- | --- |
| Stage | *For example: specify* |
| Outcome | *For example: DEV-1* |
| Run | *1, 2, 3 …* |
| Date | *YYYY-MM-DD* |
| Autonomy level | *0 to 4, see README* |
| Session | *Session log or transcript link* |
| Previous card for this stage | *Link, or "first run"* |

## 1. Purpose

*One sentence: this stage turns X into Y so that Z.*

## 2. Trigger and inputs

- **Trigger:** *What started the stage: a human, the previous stage's commit, a failed check.*
- **Inputs:** *Each artefact read, as a path at a commit.*
- **Context loaded:** *CLAUDE.md, constitution, the ADRs, skills and files the actor was given. Note anything it needed and didn't have.*

## 3. Actor

- **Who:** *Human, agent, or both.*
- **Agent setup:** *Model, effort, permission mode, skill or subagent used, tools allowed.*
- **Human role:** *What the human did during the stage, apart from the gate.*

## 4. What happened

*Numbered steps as actually run, not as planned. Note each point where a human stepped in, and why.*

1.
2.

## 5. Feedback loop

*The inner loop: the signal the actor iterated against before a human saw the work.*

- **Signal:** *For example: build output, test results, rubric score, analyser report. "None" is a valid and important answer.*
- **Stop condition:** *What counted as done.*
- **Iteration cap:** *The limit, and whether it was reached.*
- **Iterations taken:**

## 6. Output

- **Artefact:** *Path and commit.*
- **Feeds:** *The next stage that reads it.*

## 7. Checks

| Check | Type | Pass criterion | Result |
| --- | --- | --- | --- |
| | *Deterministic, rubric or human judgement* | | *Pass, fail, not run* |

*For each check that is a human judgement, could it become a rubric or a deterministic check? Note how.*

## 8. Gate

- **Approver:** *Who, and in which role (architecture coordinator, engineer reviewer).*
- **Evidence shown:** *What they decided from.*
- **Decision:** *Approved, rejected, or approved with changes. Why.*
- **Did the approver redo any of the work to decide?** *Yes or no. If yes, what. A yes means the evidence is not yet enough.*

## 9. Measurements

*Write "not measured" with a reason wherever a value is missing.*

| Measure | Value | How measured |
| --- | --- | --- |
| Wall time | | |
| Human minutes (work plus review) | | |
| Tokens / cost | | |
| Iterations to pass checks | | |
| Leading indicator for this stage | | *Name it, for example: spec accepted without rework* |
| Lagging indicator for this stage | | *Name it, for example: rework found in a later stage. Fill in when known* |

## 10. What went wrong

| Failure | Root cause | Fix | Where the fix landed | Recurred on the next run? |
| --- | --- | --- | --- | --- |
| | | | *CLAUDE.md, skill, hook, rubric, template, ADR, or nowhere* | *Fill in on the next card* |

*Did the failure send work back to an earlier stage? Which one?*

## 11. Ready to automate?

*Check against the criteria in the README.*

- [ ] Stable inputs and outputs
- [ ] A trustworthy check
- [ ] Known failures
- [ ] An evidence-based gate
- [ ] Known cost

**Verdict:** *Keep at this level, raise to level n, or lower to level n.* **Why:**

**Next run changes:** *What will be different next time.*
