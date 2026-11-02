# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them, one per line, in our own pipe-separated format.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the collector holds no subject-domain terms.

## Design

A `FindingsCollector` runs the analyzers and writes one pipe-separated line per violation.
