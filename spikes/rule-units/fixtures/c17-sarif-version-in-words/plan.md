# Implementation Plan: Analyzer Findings for the Repair Loop

## Summary

Collect analyzer rule violations and write them to a SARIF file that the repair loop reads, using the first version of the format, which the compiler writes by default.

## Design

A `FindingsCollector` merges the analyzers' output into `findings.sarif`.
