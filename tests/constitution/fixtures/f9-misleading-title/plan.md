# Implementation Plan: Orchestrate Coding Tasks

## Summary

A small worker drives Claude Code through the Claude Agent SDK, with a custom system prompt and tool settings for each task.

## Constitution Check

**ADRs that apply:** ADR-001, ADR-004.

- ADR-001@v2 C1: the worker's prompts hold no subject-domain terms.
- ADR-004@v2 C3: the capability orchestrates an existing coding agent, Claude Code, and implements none of its own.

**Hard rules:** rule 6 considered: this orchestrates Claude Code; it is not a custom coding agent.

## Design

A `TaskWorker` calls the Claude Agent SDK to start a Claude Code session per task, passing a system prompt, an allowed-tools list and a working directory. It records the session's result.
