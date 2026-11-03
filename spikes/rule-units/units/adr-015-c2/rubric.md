# Rubric: ADR-015@v1 C2

**Constraint, word for word:** "A split MUST NOT be made automatically unless all five rules hold, each checked deterministically."

**The five rules, word for word from ADR-015@v1, "Rules for an automatic split":**

1. The delivered part passes its own subset of the visible acceptance examples.
2. Nothing in the delivered part depends on the blocked part (contract dependency graph, G1).
3. The split doesn't reduce what the outcome asked for. Any reduction in what the merchant gets needs a human; with deliver dark, that happens when the flag is switched on.
4. The delivered part's risk rung is no higher than the original outcome's.
5. The system is left consistent: no half-built feature visible to users.

## How to grade

Read the feature's spec, plan and tasks. Then answer three questions.

1. **Does the feature make a split automatically?** If not, the verdict is `not-applicable`, and stop.
2. **Do all five rules hold?** For each rule, decide whether the design as written keeps it. A design that skips a rule, or contradicts it (for example, shipping the delivered part switched on, which breaks rule 3's route to a human and rule 5), fails that rule.
3. **Is each rule checked deterministically?** For each rule, decide whether the design names a check that a program carries out, not a person's or a model's judgement. A rule with no named check fails this condition.

The verdict is `pass` only if every rule holds **and** every rule has a deterministic check. Otherwise it is `fail`.

## Output

Return JSON only:

```json
{
  "verdict": "pass | fail | not-applicable",
  "rules": [
    {"rule": 1, "holds": true, "checked_deterministically": true, "evidence": "quote or file:section"}
  ],
  "reason": "one sentence"
}
```

`rules` has five entries unless the verdict is `not-applicable`. A `fail` verdict becomes a finding against ADR-015@v1 C2.
