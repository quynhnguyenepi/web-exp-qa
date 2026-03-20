# Test Cases: update-jira-ticket

## TC-01: Transition only
- Input: Issue key + target status
- Expected: Ticket transitioned, other actions skipped

## TC-02: Add labels preserving existing
- Input: Issue key + new labels
- Expected: New labels added without removing existing ones

## TC-03: Combined actions
- Input: Transition + labels + comment
- Expected: All 3 actions executed in order

## TC-04: Transition not available
- Input: Issue key + unavailable transition
- Expected: Warning with available transitions, other actions still execute

## TC-05: Atlassian MCP not available
- Input: Any action
- Expected: Standard error with .mcp.json.template reference
