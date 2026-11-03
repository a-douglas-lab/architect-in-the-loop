# Feature Specification: Analyzer Objections for the Repair Loop

## User Scenarios & Testing

### User Story 1 - Act on what the analyzers object to (Priority: P1)

When the analyzers object to code the capability changed, the repair loop learns which rule, file and line each objection concerns.

## Requirements

- **FR-001**: The capability MUST gather every objection the analyzers raise.
- **FR-002**: The capability MUST record each objection as a row in a spreadsheet, with the rule, file, line and message.

## Success Criteria

- **SC-001**: Every objection an analyzer raises appears as a row in the spreadsheet.
