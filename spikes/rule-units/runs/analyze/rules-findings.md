# Rules that apply to this feature

Selected deterministically for this feature. Each rule is quoted word for word from its source.

## ADR-016@v1 C10

Rule: Tools that report rule violations MUST report in SARIF.

Source: docs/adr/ADR-016-improving-legacy-code-the-capability-touches.md

Kind: mechanical

Check: Plan and analyze stages: a finding if the artefacts describe a violation report and name an output format other than SARIF, without naming SARIF. Implement stage: a finding if a violations file is not SARIF, judged by its "$schema" and "version" fields; any SARIF version is accepted and reported, because ADR-016 names none.

## CLAUDE.md hard rule 4 (copy clause)

Rule: never copy eShop files into this repo.

Source: CLAUDE.md

Kind: bright-line

Check: Plan and analyze stages: a finding if a sentence describes copying subject-system files and isn't negated. Implement stage: a finding if a file outside subject/ is byte-identical to a file in the subject tree. Covers the copy clause only; the rule's other clauses (pinned, fork only, AI features off) are out of the spike.
