# Implementation Plan: Sample Source for Capability Tests

## Summary

Point the capability's tests at the subject/eshop submodule, read in place.

## Constitution Check

**ADRs that apply:** ADR-002, ADR-003.

**Hard rules:** rule 4 considered: the tests read eShop through the submodule and nothing is copied.

## Design

A test fixture resolves the submodule path from configuration and reads the source files in place.
