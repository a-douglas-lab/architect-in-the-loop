# Implementation Plan: Offline Sample Classes

## Summary

Recreate the Ordering.Domain classes by hand in this repository, with a renamed namespace, so tests run offline.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the recreated classes sit under `tests/samples/`, not in the capability.

## Design

Each class is retyped from the original source into `tests/samples/ordering/`, with the namespace changed to `Samples.Ordering`.
