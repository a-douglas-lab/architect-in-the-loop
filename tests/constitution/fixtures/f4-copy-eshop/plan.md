# Implementation Plan: Offline Sample Data

## Summary

Copy eShop's Ordering.Domain source into this repository, so tests can run without the submodule.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the capability's code holds no subject-domain terms; the copied files sit under `tests/samples/`, not the capability.

## Design

A script copies `subject/eshop/src/Ordering.Domain` to `tests/samples/ordering-domain/`, and the result is committed.
