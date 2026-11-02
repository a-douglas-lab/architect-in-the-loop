# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them to a CSV file that the repair loop reads.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the collector holds no subject-domain terms.

**Hard rules:** none affected.

## Design

A `FindingsCollector` runs the analyzers, converts their output to rows with rule, file, line and message, and writes `findings.csv`. The repair loop reads the CSV.
