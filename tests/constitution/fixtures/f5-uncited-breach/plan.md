# Implementation Plan: Automatic Outcome Splitting

## Summary

Split an outcome as soon as any part is blocked, and ship the rest switched on.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the split logic holds no subject-domain terms.

## Design

A `SplitRunner` splits on any blocked part. It skips acceptance, dependency and risk checks, to save time, and ships the unblocked part without a feature flag.
