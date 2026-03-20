# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify Atlassian MCP, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Execute update actions on ticket", status: "pending", activeForm: "Updating ticket" },
  { content: "Report result", status: "pending", activeForm: "Reporting result" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| Atlassian MCP not available | Exit with standard setup instructions |
| Ticket not found (404) | Ask user to verify ticket key |
| Transition not available | Log available transitions, skip, continue with other actions |
| Label contains spaces | Suggest underscore replacement, skip |
| Field not editable | Log error, continue with other actions |
| Permission denied | Log error, report to user |

---


## Self-Correction

1. **"Use a different transition"** -> Show available transitions, let user pick
2. **"Don't add the comment"** -> Skip comment action
3. **"Update a different ticket"** -> Accept new issue_key, re-run

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | All ticket operations (REQUIRED) | No fallback |

### Difference from mass-update-jira-tickets

| Feature | update-jira-ticket | mass-update-jira-tickets |
|---------|-------------------|-------------------------|
| Scope | Single ticket | Multiple tickets via JQL |
| Input | Ticket key + actions | JQL query + actions |
| Confirmation | No user confirmation needed | Requires user confirmation |
| Use case | Sub-skill for orchestrators | Standalone bulk operation |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| Transition only | `{ issue_key: "CJS-100", transition: "In Review" }` |
| Labels only | `{ issue_key: "CJS-100", add_labels: ["AutomationDone"] }` |
| Comment only | `{ issue_key: "CJS-100", comment: "PR #45 submitted." }` |
| Combined | `{ issue_key: "CJS-100", transition: "Done", add_labels: ["AutomationDone"], comment: "Completed." }` |
