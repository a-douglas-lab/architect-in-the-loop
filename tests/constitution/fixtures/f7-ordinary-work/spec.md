# Feature Specification: Rename the Report Field

**Status**: Draft (test fixture)

## User Scenarios & Testing

### User Story 1 - Clearer field name (Priority: P1)

The coordinator sees `impactedDomains` in place of `domains` in the capability's API response.

**Acceptance Scenarios**:

1. **Given** an impact report, **When** the API returns it, **Then** the field is named `impactedDomains`.

## Requirements

- **FR-001**: The capability's API MUST name the field `impactedDomains`.

## Success Criteria

- **SC-001**: API responses use the new field name.
