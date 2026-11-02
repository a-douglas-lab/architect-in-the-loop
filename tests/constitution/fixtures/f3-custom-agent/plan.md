# Implementation Plan: Faster Implementation Runs

## Summary

Replace calls to the external coding agent with an in-house agent loop, written in the capability.

## Constitution Check

**ADRs that apply:** ADR-001.

- ADR-001@v2 C1: the agent loop holds no subject-domain terms.

## Design

An `AgentLoop` class calls the model API directly, with its own tools for reading and editing files, and its own repair logic.
