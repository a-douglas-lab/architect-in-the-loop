# Feature Specification: Orchestrate Coding Tasks

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Hand a task to the coding agent (Priority: P1)

The capability hands each implementation task to Claude Code and collects the result.

**Acceptance Scenarios**:

1. **Given** a planned task, **When** the capability runs it, **Then** Claude Code carries out the change and the capability records the result.

## Requirements

- **FR-001**: The capability MUST run implementation tasks through Claude Code, using the Claude Agent SDK.
- **FR-002**: The capability MUST set each run's system prompt, allowed tools and working directory.

## Success Criteria

- **SC-001**: Every implementation task is carried out by Claude Code, and its result recorded.
