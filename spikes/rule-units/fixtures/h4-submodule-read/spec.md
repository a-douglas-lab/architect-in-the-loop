# Feature Specification: Sample Source for Capability Tests

## User Scenarios & Testing

### User Story 1 - Test against real source (Priority: P1)

A developer runs the capability's tests against real subject source.

## Requirements

- **FR-001**: The capability's tests MUST read eShop's Ordering.Domain source through the subject/eshop submodule at run time; nothing is copied into this repository.

## Success Criteria

- **SC-001**: The tests pass with the submodule checked out at its pinned commit.
