# Implementation Plan: Automatic Outcome Splitting

## Summary

A `SplitGate` runs five deterministic checks before any automatic split, and the delivered part ships dark.

## Constitution Check

**ADRs that apply:** ADR-001, ADR-015.

- ADR-001@v2 C1: the split logic holds no subject-domain terms.
- ADR-015@v1 C2 to C8: each rule for an automatic split is a check in `SplitGate`.

## Design

`SplitGate` refuses the split unless all five checks pass, each computed by code:

1. The delivered part passes its own subset of the visible acceptance examples, run by the test runner.
2. The contract dependency graph shows nothing in the delivered part depending on the blocked part.
3. A comparison of the outcome with the delivered part finds no reduction in what was asked for; any reduction waits for a person, at the flag switch.
4. The delivered part's risk rung, read from the use-case ladder, is no higher than the outcome's.
5. A scan of user-visible routes finds no half-built feature: the delivered part's flag is off.
