# Implementation Plan: Impact Report Export

## Summary

Add an export endpoint to the capability's API that returns the impact report as a file.

## Design

An `ExportController` in the C# API reads the stored impact report, and resolves domain names through the subject contract at its given location.
