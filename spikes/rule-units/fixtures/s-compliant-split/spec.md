# Feature Specification: Automatic Outcome Splitting

## User Scenarios & Testing

### User Story 1 - Keep work moving safely (Priority: P1)

When part of an outcome is blocked, the capability delivers the rest dark, if it is safe to do so.

## Requirements

- **FR-001**: The capability MUST split an outcome automatically only when every rule for an automatic split, checked by a program, holds.
- **FR-002**: The delivered part MUST ship behind a feature flag that is switched off; a person switches it on.

## Success Criteria

- **SC-001**: No automatic split is made unless every check passes.
