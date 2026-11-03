# Implementation Plan: Analyzer Objections for the Repair Loop

## Summary

Gather what the analyzers object to and record it in a spreadsheet that the repair loop reads.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the gatherer holds no subject-domain terms.

## Design

An `ObjectionGatherer` runs the analyzers and writes one spreadsheet row per objection.
