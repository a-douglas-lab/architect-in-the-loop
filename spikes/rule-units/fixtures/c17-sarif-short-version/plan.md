# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them to a SARIF v2.1 file that the repair loop reads.

## Design

A `FindingsCollector` runs the analyzers with `ErrorLog` set to `version=2.1` and merges their output into `findings.sarif`.
