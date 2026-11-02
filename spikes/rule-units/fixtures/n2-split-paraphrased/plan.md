# Implementation Plan: Release What Is Ready

## Summary

Hold back a stuck piece of an outcome and release the remaining pieces, each behind a toggle that stays off.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the release logic holds no subject-domain terms.

## Design

A `ReleaseRunner` releases every piece that is not stuck, each behind an off toggle.
