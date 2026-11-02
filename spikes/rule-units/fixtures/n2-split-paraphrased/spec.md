# Feature Specification: Release What Is Ready

## User Scenarios & Testing

### User Story 1 - Do not wait on a stuck piece (Priority: P1)

When one piece of an outcome is held up, the capability holds that piece back and releases the remaining pieces.

## Requirements

- **FR-001**: The capability MUST hold back a stuck piece of an outcome and release the remaining pieces on its own.
- **FR-002**: Each released piece MUST sit behind a toggle that stays off until a person turns it on.

## Success Criteria

- **SC-001**: A stuck piece never delays the remaining pieces.
