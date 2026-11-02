# Feature Specification: Offline Sample Data

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Run capability tests offline (Priority: P1)

A developer runs the capability's tests without the eShop submodule checked out.

**Acceptance Scenarios**:

1. **Given** no `subject/eshop` checkout, **When** the capability's tests run, **Then** they find sample source files in this repository.

## Requirements

- **FR-001**: The repository MUST include a copy of eShop's Ordering.Domain source, under `tests/samples/`.

## Success Criteria

- **SC-001**: The capability's tests pass with no submodule checked out.
