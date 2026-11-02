# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them to a SARIF file that the repair loop reads.

## Constitution Check

**ADRs that apply:** ADR-001, ADR-016.

- ADR-001@v2 C1: the collector holds no subject-domain terms.
- ADR-016@v1 C10: violations are reported in SARIF.

## Design

A `FindingsCollector` runs the analyzers and merges their SARIF output into `findings.sarif`.
