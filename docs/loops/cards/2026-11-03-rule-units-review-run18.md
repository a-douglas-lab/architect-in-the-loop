# Loop card: review · SARIF version decision · run 18

| Field | Value |
| --- | --- |
| Stage | Review (documentation change) |
| Outcome | None: project work, Step 7 item 1 (T6, rule units) |
| Run | 18 |
| Date | 2026-11-03 |
| Autonomy level | 1, drafted |
| Session | [Step 7 rule-unit spike log](../../sessions/2026-11-02-step7-rule-units.md) |
| Previous card for this stage | [Run 17](2026-11-02-rule-units-review-run17.md) |

## Run

- **Inputs:** the uncommitted diff on `f3d9896` (backlog T6, prior-art.md, the session log); REVIEW.md; Andy's message word for word: "you decide the sarif version, is there a condition where we need to align between versions to allow consistency?". The reviewer fetched GitHub's SARIF docs, Roslyn's source and the OASIS pages itself.
- **Cost:** about 73,000 tokens, 16 tool calls. Harness duration 5,077 s, which includes idle time and isn't a fair measure of effort.
- **Result:** 0 High, 3 Medium, 3 Low, 1 nit.

## What it found

- **Medium:** the author's 3 Nov decision sat under headings crediting Andy, dated 2 Nov, in backlog T6 and prior-art.md. "eShop's analysers need that setting" was actionable without saying an eShop change needs an approved spec (hard rules 2 and 5).
- **Low:** "OASIS, 2019": 2.1.0 became an OASIS Standard in March 2020. "2.2 work started in 2023" not confirmed, and no sources cited. The session log and backlog disagreed on what waits for Andy.
- **Nit:** "each read one format" stretches ADR-016's "one format" to one version; acceptable as the author's labelled reasoning.
- **Checks that held:** GitHub accepts only 2.1.0; Roslyn defaults to 1.0.0 (evidence in `SarifVersion.cs`); C10 names no version; the spike's check accepts any version; pinning is a revision under ADR-000@v3 C8 and C11; no claim of enforcement; no contradiction left; edits inside T6.

## Responses

All accepted and fixed. The decision has its own heading, "Decided (3 Nov), by the author at Andy's request", in backlog T6 and prior-art.md. The text now says "OASIS Standard since March 2020", "a 2.2 draft exists, status not confirmed", cites GitHub's docs and Roslyn's `SarifVersion.cs`, flags the eShop setting as needing an approved spec, and labels the one-version reasoning as the author's. The session log and backlog now agree.

Author-scored. Not independent.

## What the run showed

A new decision appended to an existing list takes on that list's heading, including who decided it and when. Decisions by different people, or on different dates, need their own headings.

## Measurements

About 73,000 tokens; 16 tool calls.

**Not re-reviewed:** the fixes.
