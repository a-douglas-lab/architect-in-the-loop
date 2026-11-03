# Feature Specification: Analyzer Findings for the Repair Loop

## User Scenarios & Testing

### User Story 1 - Feed analyzer findings to the repair loop (Priority: P1)

When an analyzer reports problems in code the capability changed, the repair loop receives them in a form it can act on.

## Requirements

- **FR-001**: The capability MUST collect rule violations reported by the analyzers it runs.
- **FR-002**: The capability MUST write the violations to a file in our own line format: rule, file, line and message, separated by pipes.

## Success Criteria

- **SC-001**: Every violation an analyzer reports appears as a line in the file.
