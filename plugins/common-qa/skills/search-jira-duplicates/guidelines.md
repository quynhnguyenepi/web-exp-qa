# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify Atlassian MCP, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Extract search keywords from input", status: "pending", activeForm: "Extracting keywords" },
  { content: "Search JIRA for matching tickets", status: "pending", activeForm: "Searching JIRA" },
  { content: "Rank and return results", status: "pending", activeForm: "Ranking results" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| Atlassian MCP not available | Exit with standard setup instructions |
| No keywords provided | Ask user for keywords or summary |
| JQL syntax error | Simplify query, retry with broader search |
| Too many results (>20) | Narrow search with additional keywords |

---


## Self-Correction

1. **"Search in a different project"** -> Re-run with new project_key
2. **"Include resolved tickets"** -> Remove resolution filter from JQL
3. **"Search by error message instead"** -> Use error text as primary keywords

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | JIRA search (REQUIRED) | No fallback |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| Keywords | `["visual editor", "font size", "not saving"]` |
| Summary | `Font size changes not saved in Visual Editor` |
| Error message | `TimeoutError: waiting for selector '[data-test="save-btn"]'` |
| Combined | Keywords + project_key + issue_type |
