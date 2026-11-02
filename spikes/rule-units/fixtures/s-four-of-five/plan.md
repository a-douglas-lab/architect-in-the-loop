# Implementation Plan: Automatic Outcome Splitting

## Summary

A `SplitGate` runs deterministic checks before any automatic split, and the delivered part ships dark.

## Constitution Check

**ADRs that apply:** ADR-001, ADR-015.

- ADR-001@v2 C1: the split logic holds no subject-domain terms.
- ADR-015@v1 C2: the rules for an automatic split are checks in `SplitGate`.

## Design

`SplitGate` refuses the split unless these checks pass, each computed by code:

1. The delivered part passes its own subset of the visible acceptance examples, run by the test runner.
2. The contract dependency graph shows nothing in the delivered part depending on the blocked part.
3. A comparison of the outcome with the delivered part finds no reduction in what was asked for; any reduction waits for a person, at the flag switch.
4. A scan of user-visible routes finds no half-built feature: the delivered part's flag is off.

Risk is not compared: the delivered part is always smaller, so its risk is assumed to be no higher.
