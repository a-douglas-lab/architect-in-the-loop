# Feature Specification: Offline Sample Classes

## User Scenarios & Testing

### User Story 1 - Run capability tests offline (Priority: P1)

A developer runs the capability's tests without the subject checked out.

## Requirements

- **FR-001**: The repository MUST include the classes from eShop's Ordering.Domain, retyped by hand under `tests/samples/` with the namespace renamed.

## Success Criteria

- **SC-001**: The capability's tests pass with nothing checked out under subject/.
