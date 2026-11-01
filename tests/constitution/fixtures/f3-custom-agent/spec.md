# Feature Specification: Faster Implementation Runs

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Implement a task faster (Priority: P1)

The capability completes implementation tasks with less waiting.

**Acceptance Scenarios**:

1. **Given** a planned task, **When** the capability implements it, **Then** the change is produced without calling an external tool.

## Requirements

- **FR-001**: The capability MUST complete implementation tasks using its own in-house coding agent loop: its own model calls, file-editing tools and repair logic.

## Success Criteria

- **SC-001**: Implementation tasks complete without any external coding agent.
