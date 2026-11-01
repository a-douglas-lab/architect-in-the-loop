# Feature Specification: Automatic Outcome Splitting

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Keep work moving (Priority: P1)

When part of an outcome is blocked, the capability ships the rest without waiting.

**Acceptance Scenarios**:

1. **Given** an outcome with a blocked part, **When** a run reaches the block, **Then** the capability splits the outcome and ships the unblocked part.

## Requirements

- **FR-001**: The capability MUST split an outcome automatically whenever any part is blocked.
- **FR-002**: The unblocked part MUST ship switched on, straight away.

## Success Criteria

- **SC-001**: A blocked part never delays the rest of an outcome.
