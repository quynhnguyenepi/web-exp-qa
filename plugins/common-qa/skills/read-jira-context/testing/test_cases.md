# Test Cases: read-jira-context

## TC-001: Basic Ticket with All Context
- **Input:** Valid ticket ID with description, comments, linked tickets, and epic
- **Expected:** All sections populated in output

## TC-002: Ticket with No Comments
- **Input:** Ticket ID where all comments are bot messages
- **Expected:** "Relevant Comments (0)" section, no error

## TC-003: Ticket with No Epic
- **Input:** Ticket ID with no parent epic
- **Expected:** Epic Context section shows "No parent Epic"

## TC-004: Ticket with No Linked Tickets
- **Input:** Ticket with empty issuelinks
- **Expected:** "Linked Tickets (0)" section, no error

## TC-005: Ticket Not Found
- **Input:** Invalid ticket ID (e.g., FAKE-99999)
- **Expected:** Error message with ticket ID, prompt to verify
