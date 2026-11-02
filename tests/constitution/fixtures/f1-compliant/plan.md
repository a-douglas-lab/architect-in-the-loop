# Implementation Plan: Impact Report Export

## Summary

Add an export endpoint to the capability's API that returns the impact report as a file.

## Constitution Check

**ADRs that apply:** ADR-001, ADR-003, ADR-017.

- ADR-001@v2 C1: the export code holds no subject-domain terms.
- ADR-001@v2 C2: domain names come from the subject contract.
- ADR-003@v2 C3: the subject's path is not hard-coded.
- ADR-017@v1 C3: the endpoint is part of the C# REST API.

**Hard rules:** none affected.

## Design

An `ExportController` in the C# API reads the stored impact report, and resolves domain names through the subject contract at its given location.
