# Feature Specification: Impact Report Export

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Download an impact report (Priority: P1)

The architecture coordinator downloads the impact report for an outcome as a file.

**Acceptance Scenarios**:

1. **Given** an outcome with an impact report, **When** the coordinator asks to export it, **Then** they receive a file listing the impacted domains, read from the subject contract.

## Requirements

- **FR-001**: The system MUST export an outcome's impact report as a file.
- **FR-002**: Domain names in the report MUST come from the subject contract, not from the capability's code.

## Success Criteria

- **SC-001**: An exported report lists every domain in the outcome's impact set.
