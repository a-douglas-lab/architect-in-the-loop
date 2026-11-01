# Implementation Plan: Rename the Report Field

## Summary

A small change to the capability's own C# API, written by hand. Nothing in eShop changes.

## Constitution Check

**ADRs that apply:** ADR-017.

- ADR-017@v1 C3: the field is part of the C# REST API.

**Hard rules:** none affected. This is capability code, not eShop.

## Design

Rename the field in the response type, and update the capability's own unit test that asserts the field name. It is not an acceptance test.
