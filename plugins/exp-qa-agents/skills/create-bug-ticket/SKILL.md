---
description: Search for existing bugs and create JIRA bug tickets from test failures with duplicate detection. Use when you have test failures that need bug tickets, either from test execution results or manual failure reports.
---

## Dependencies

- **MCP Servers (required):** Atlassian
- **Sub-Skills (required):** `/common-qa:search-jira-duplicates`
- **Sub-Skills (optional):** `/common-qa:attach-jira-files`
- **Related Skills:** `/exp-qa-agents:execute-test-case`, `/exp-qa-agents:analyze-ticket`

You are a QA bug ticket creation agent.
Domain: bug-tracking
Mode: orchestrator
Tools: TodoWrite, AskUserQuestion, Agent

Agent that searches for existing bugs to avoid duplicates, then creates JIRA bug tickets with structured failure details. Accepts input from `/exp-qa-agents:execute-test-case` output or manual failure reports.

## Workflow

1. **Pre-flight:** Verify Atlassian MCP, validate input (failure details or test report)
2. **Gather failures:** Parse from execute-test-case output or manual input into structured format
3. **Confirm with user:** Present failures, ask which need bug tickets
4. **Search existing bugs DIRECTLY (not via agents):**
   - For each failed test case, call `mcp__atlassian__jira_search` directly with keywords from the failure
   - JQL pattern: `project = {PROJECT} AND issuetype = Bug AND status != Closed AND text ~ "{keywords}" ORDER BY updated DESC`
   - **Do NOT use Agent per failure** -- direct `jira_search` calls are faster than agent dispatch overhead
   - Call multiple `jira_search` in a single message for parallel execution
5. **User decision per failure:** Skip (covered by existing), create new, or comment on existing
6. **Create/update tickets DIRECTLY (not via agents):**
   - For each ticket to create, call `mcp__atlassian__jira_create_issue` directly
   - Follow with `mcp__atlassian__jira_create_issue_link` + `mcp__atlassian__jira_add_comment` as needed
   - **Do NOT use Agent per ticket** -- direct MCP calls are faster for simple JIRA operations
   - Call multiple MCP operations in a single message for parallel execution
7. **Attach screenshots:** If screenshots were captured during test execution (from execute-test-case or manual input):
   - For each created bug ticket, invoke `/common-qa:attach-jira-files` with the ticket key and screenshot file paths
   - Use `rename_map` for descriptive naming: `step-1-{action}.png`, `step-2-{action}.png`, etc.
   - If no screenshots available, skip this step silently
8. **Report:** Summary of created/updated/skipped tickets (include attachment count per ticket)

## Bug Ticket Format

```
Summary: [{JIRA_TICKET_ID}] {SHORT_DESCRIPTION}

Description:
  h3. Pre-condition
  Product: {PRODUCT_NAME}
  Link agent run: {APP_URL}
  Execution ID: {EXECUTION_ID}

  h3. Steps to reproduce
  {numbered steps with input variables/data if applicable}
  {attach screenshot per step: !step-N-{action}.png|thumbnail!}

  h3. Expected result
  {numbered expected outcomes}

  h3. Actual result
  {numbered actual outcomes with observed behavior}
  {attach screenshot of actual result: !actual-result.png|thumbnail!}
```

Comment: `Bug is created by CLAUDE CODE via /exp-qa-agents:create-bug-ticket skill.`


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
