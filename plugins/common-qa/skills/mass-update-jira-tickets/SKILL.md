---
description: Mass update JIRA tickets matching a JQL query. Supports workflow transitions, adding/removing labels, changing fields, and more. Use when you need to bulk-update many tickets at once.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** None

# Mass Update JIRA Tickets

Search for JIRA tickets using a JQL query, then apply bulk updates across all matching tickets with progress tracking and a final summary report. Supports multiple update actions including workflow transitions, label changes, field updates, and more.

## When to Use

Invoke this skill when you need to:

- Transition many tickets to a new workflow status (e.g., move all "To Do" to "In Progress")
- Add or remove labels across a batch of tickets
- Update fields (assignee, priority, components, etc.) in bulk
- Perform any combination of the above on tickets matching a JQL query
- Clean up or standardize ticket data across a project or epic

## Supported Actions

| Action | Description | Example |
|--------|------------|---------|
| **Transition status** | Change workflow status of tickets | Move all to "In Progress" |
| **Add label(s)** | Add one or more labels | Add `AI_Testing` to all test cases |
| **Remove label(s)** | Remove one or more labels | Remove `AutomationBlocked` |
| **Replace label** | Remove one label and add another | Replace `OldLabel` with `NewLabel` |
| **Update field(s)** | Change any editable field | Set assignee, priority, components |
| **Add comment** | Add a comment to all tickets | Add "Reviewed by QA team" |
| **Combined** | Multiple actions at once | Transition + add label + add comment |

## Workflow Overview

**Simple Flow:**
```
Pre-Flight → Search Tickets → Confirm Action → Execute Updates → Report Results
```

**See guidelines.md for detailed workflow diagram, action-specific handlers, batch processing logic, and report templates.**

## Execution Workflow

Follow these 5 sequential steps:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Validate user input:**
   - Check if user provided a JQL query (or natural language that can be converted to JQL)
   - Check if user specified the action to perform. If not, ask via AskUserQuestion:
     - "What is the JQL query to find the tickets?" (if not provided)
     - "What action do you want to perform on the matching tickets?"
       - "Transition workflow status", "Add/Remove labels", "Update fields", "Add comment"

2. **Gather action-specific details:**
   - Ask for parameters based on the action (target status, label names, field values, comment text)
   - Validate input (labels must not contain spaces, fields must be valid)
   - **See guidelines.md Section 1 for detailed action-specific gathering logic.**

3. **Parse and validate JQL:**
   - Ensure the JQL string is not empty
   - If user provides natural language, convert it to JQL
   - If unclear, ask user to confirm the JQL
   - **See guidelines.md Section 2 for JQL conversion patterns.**

4. **Verify Atlassian MCP is enabled:**
   - Attempt a test call to `mcp__atlassian__jira_search` with a simple query
   - If not available, display error and exit:
     ```
     Error: Atlassian MCP is not configured

     This skill requires Atlassian MCP server for JIRA access.

     Setup Instructions:
     1. Ensure .mcp.json.template exists in project root with Atlassian server configuration
     2. Restart Claude Code
     3. Verify JIRA access with: mcp__atlassian__jira_search

     See .mcp.json.template for detailed configuration.
     Cannot proceed without Atlassian MCP configuration.
     ```

5. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Atlassian MCP: Connected
      - JQL Query: {JQL_QUERY}
      - Action(s): {ACTION_SUMMARY}

   Proceeding to search tickets...
   ```

---

### Step 1: Search Tickets

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Search tickets matching JQL query" as `in_progress`.

1. **Execute the JQL query with pagination:**
   ```
   mcp__atlassian__jira_search({
     jql: "{JQL_QUERY}",
     fields: "summary,labels,status,issuetype,assignee,priority",
     limit: 50,
     start_at: 0
   })
   ```

2. **Handle pagination to collect ALL matching tickets:**
   - Check `total` in response. If `total > 50`, loop with incrementing `start_at` (50, 100, 150...)
   - If `total` is `-1` (Jira Cloud behavior), keep fetching until returned issues count < limit
   - **See guidelines.md Section 3 for detailed pagination logic.**

3. **Collect ticket data:**
   - For each ticket, store: `key`, `summary`, `labels` (current), `status`, `issuetype`, `assignee`, `priority`

4. **Report search results:**
   - Display total count and first 10 tickets in a table
   - Note remaining count if total > 10

---

### Step 2: Confirm Action

**Todo:** Mark "Search tickets matching JQL query" as `completed`, mark "Confirm action with user" as `in_progress`.

1. **Pre-filter tickets (where applicable):**
   - Skip tickets where action is a no-op (e.g., already has label, already in target status)
   - **See guidelines.md Section 4 for pre-filter logic table.**

2. **Present the action summary:**
   - Show action details, total count, skip count, update count

3. **Ask user for confirmation via AskUserQuestion:**
   - "Proceed with update" (Recommended)
   - "Show all tickets first"
   - "Cancel"

---

### Step 3: Execute Updates

**Todo:** Mark "Confirm action with user" as `completed`, mark "Execute updates on all matching tickets" as `in_progress`.

Execute the requested action(s) on each applicable ticket. Use these MCP calls based on action:

- **Transition:** `mcp__atlassian__jira_transition_issue({ issue_key, transition_id })`
- **Add/Remove/Replace label:** `mcp__atlassian__jira_update_issue({ issue_key, fields: "{\"labels\": [...]}" })`
- **Update field:** `mcp__atlassian__jira_update_issue({ issue_key, fields: "{...}" })`
- **Add comment:** `mcp__atlassian__jira_add_comment({ issue_key, body })`

**CRITICAL for labels:** Always preserve existing labels. Never overwrite — always merge.

**Batch processing:**
- Execute updates in parallel batches (up to 24 concurrent calls)
- For large batches (>20 tickets), report progress every 20 tickets
- Track: updated, skipped, failed counts

**See guidelines.md Section 5 for detailed action execution patterns, transition handling, batch processing strategy, and failure tracking.**

---

### Step 4: Report Results

**Todo:** Mark "Execute updates on all matching tickets" as `completed`, mark "Report results" as `in_progress`.

1. **Display final summary table:**
   - Results: Updated, Skipped, Failed, Total counts

2. **If failures occurred, list them:**
   - Table: Key, Error

3. **Display updated tickets table:**
   - Show: #, Key, Summary, Change Applied
   - For large results (>20 tickets), show first 20 and note the rest

4. **Mark "Report results" as `completed`.** All todos should now be `completed`.

**See guidelines.md Section 6 for detailed report templates and formatting examples.**

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, Notes, detailed workflow diagrams, action-specific handlers, batch processing logic, and report templates are in guidelines.md to reduce auto-loaded context size.
