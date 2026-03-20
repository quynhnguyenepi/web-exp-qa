---
description: Update a single JIRA ticket with workflow transition, labels, comment, or field changes. Use when any skill needs to update one ticket's status, add labels, or post a comment after completing an action.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** `/exp-qa-agents:create-pr`, `/exp-qa-agents:create-bug-ticket`, `/common-qa:mass-update-jira-tickets`

# Update a Single JIRA Ticket

Perform one or more update actions on a single JIRA ticket: transition workflow status, add/remove labels, update fields, and/or add a comment. Designed as a lightweight sub-skill for use by orchestrator agents that need to update individual tickets after completing an action.

**For bulk updates across many tickets, use `/common-qa:mass-update-jira-tickets` instead.**

## When to Use

Invoke this skill when you need to:

- Transition a ticket to a new status (e.g., "In Review", "Done", "Closed")
- Add labels to a ticket (e.g., `AutomationDone`, `TestCase`)
- Add a comment to a ticket (e.g., PR link, test results)
- Update fields on a ticket (e.g., assignee, priority)
- Perform a combination of the above on a single ticket

## Workflow Overview

```
Pre-Flight -> Execute Actions -> Report Result
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:**
   - `issue_key`: JIRA ticket key (e.g., `CJS-10873`) -- required
   - At least one action must be specified:
     - `transition`: target status name (e.g., `"In Review"`, `"Done"`, `"Closed"`)
     - `add_labels`: list of labels to add (e.g., `["AutomationDone", "TestCase"]`)
     - `remove_labels`: list of labels to remove
     - `comment`: comment text to add
     - `fields`: field updates as JSON (e.g., `{"priority": {"name": "High"}}`)
2. **Verify Atlassian MCP:** Attempt `mcp__atlassian__jira_get_issue` with the ticket key. If not available, exit with standard error:
   ```
   Error: Atlassian MCP is not configured

   This skill requires Atlassian MCP server for JIRA access.

   Setup Instructions:
   1. Ensure .mcp.json exists in project root with Atlassian server configuration
   2. Restart Claude Code
   3. Verify JIRA access with: mcp__atlassian__jira_get_issue

   See .mcp.json.template for detailed configuration.
   Cannot proceed without Atlassian MCP configuration.
   ```

### Step 1: Execute Update Actions

Execute the requested actions in order: transition -> labels -> fields -> comment.

#### Transition (if requested)

1. Get available transitions:
   ```
   mcp__atlassian__jira_get_transitions({ issue_key: "{ISSUE_KEY}" })
   ```
2. Find matching transition by name (case-insensitive match)
3. If found, execute:
   ```
   mcp__atlassian__jira_transition_issue({
     issue_key: "{ISSUE_KEY}",
     transition_id: "{TRANSITION_ID}"
   })
   ```
4. If not found, log available transitions and skip:
   ```
   Warning: Transition "{TARGET_STATUS}" not available for {ISSUE_KEY}.
   Available transitions: {list}
   ```

#### Add/Remove Labels (if requested)

1. Get current labels from ticket (already fetched in pre-flight)
2. Compute new labels:
   - Add: `new_labels = current_labels + add_labels` (no duplicates)
   - Remove: `new_labels = current_labels - remove_labels`
3. Update:
   ```
   mcp__atlassian__jira_update_issue({
     issue_key: "{ISSUE_KEY}",
     fields: "{\"labels\": [\"label1\", \"label2\"]}"
   })
   ```
   **CRITICAL**: Always preserve existing labels. Never overwrite -- always merge.

#### Update Fields (if requested)

```
mcp__atlassian__jira_update_issue({
  issue_key: "{ISSUE_KEY}",
  fields: "{FIELDS_JSON}"
})
```

#### Add Comment (if requested)

```
mcp__atlassian__jira_add_comment({
  issue_key: "{ISSUE_KEY}",
  body: "{COMMENT_TEXT}"
})
```

### Step 2: Report Result

```markdown
### Update Result for {ISSUE_KEY}

| Action | Status | Details |
|--------|--------|---------|
| Transition | {Done/Skipped/Failed} | {old_status} -> {new_status} |
| Add labels | {Done/Skipped/Failed} | Added: {labels} |
| Remove labels | {Done/Skipped/Failed} | Removed: {labels} |
| Update fields | {Done/Skipped/Failed} | {field_names} |
| Comment | {Done/Skipped/Failed} | Comment added |
```

---


## Guidelines

### Action Execution Order

Always execute actions in this order: transition -> labels -> fields -> comment.

### Label Safety

- **Always preserve existing labels** -- never overwrite the entire labels array
- Compute: `new_labels = current_labels + add_labels - remove_labels`
- Labels are case-sensitive and cannot contain spaces

### Transition Handling

- Always check available transitions first via `mcp__atlassian__jira_get_transitions`
- Match transition name case-insensitively
- If target transition not available, log available transitions and skip gracefully

### Difference from mass-update-jira-tickets

This skill operates on a **single ticket** without user confirmation -- designed as a lightweight sub-skill for orchestrators. Use `mass-update-jira-tickets` for bulk operations with JQL queries and user confirmation gates.

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
