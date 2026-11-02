# Feature Specification: Analyzer Findings for the Repair Loop

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Feed analyzer findings to the repair loop (Priority: P1)

When an analyzer reports problems in code the capability changed, the repair loop receives them in a form it can act on.

**Acceptance Scenarios**:

1. **Given** analyzer findings for a change, **When** the capability collects them, **Then** the repair loop receives each finding with its rule, file and line.

## Requirements

- **FR-001**: The capability MUST collect rule violations reported by the analyzers it runs.
- **FR-002**: The capability MUST write the violations to `findings.csv`, one row per violation, with columns rule, file, line and message.

## Success Criteria

- **SC-001**: Every violation an analyzer reports appears as a row in `findings.csv`.
