# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them to a SARIF 1.0 file that the repair loop reads.

## Design

A `FindingsCollector` runs the analyzers with their default error log settings and merges their SARIF output into `findings.sarif`.
