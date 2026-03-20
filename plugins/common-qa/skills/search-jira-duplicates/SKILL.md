---
description: Search JIRA for existing tickets that may be duplicates of a new issue. Use when you need to check for duplicates before creating a bug ticket, test case, or any JIRA issue.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** `/exp-qa-agents:create-bug-ticket`

# Search JIRA for Duplicates

Search JIRA for existing tickets that match keywords, summary, or error messages to detect potential duplicates before creating new tickets. Returns a ranked list of matching tickets with relevance indicators.

## When to Use

Invoke this skill when you need to:

- Check if a bug already exists before filing a new one
- Find related tickets before creating a test case
- Detect duplicate issues across projects
- Search for tickets by error message, component, or description keywords

## Workflow Overview

```
Pre-Flight -> Extract Keywords -> Search JIRA -> Rank Results -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:** Accept one or more of:
   - `keywords`: list of search terms (e.g., error messages, component names)
   - `summary`: short description of the issue
   - `project_key`: JIRA project to search within (optional, searches all if omitted)
   - `issue_type`: filter by type (e.g., Bug, Test, Story) (optional)
2. **Verify Atlassian MCP:** Attempt `mcp__atlassian__jira_search`. If not available, exit with standard error:
   ```
   Error: Atlassian MCP is not configured

   This skill requires Atlassian MCP server for JIRA access.

   Setup Instructions:
   1. Ensure .mcp.json exists in project root with Atlassian server configuration
   2. Restart Claude Code
   3. Verify JIRA access with: mcp__atlassian__jira_search

   See .mcp.json.template for detailed configuration.
   Cannot proceed without Atlassian MCP configuration.
   ```

### Step 1: Extract Search Keywords

From the input, build search queries:

1. **From summary/description:** Extract key nouns, error codes, component names
2. **From error messages:** Extract the core error text (strip stack traces, timestamps)
3. **Build JQL queries** (run multiple to maximize coverage):
   - **Exact match:** `summary ~ "\"{EXACT_PHRASE}\""`
   - **Keyword match:** `summary ~ "{KEYWORD1}" AND summary ~ "{KEYWORD2}"`
   - **Text search:** `text ~ "{KEYWORD1} {KEYWORD2}"`
   - Add project filter if `project_key` provided: `AND project = {PROJECT_KEY}`
   - Add type filter if `issue_type` provided: `AND issuetype = {ISSUE_TYPE}`
   - Exclude resolved tickets older than 6 months: `AND (status != Done OR updated >= -180d)`

### Step 2: Search JIRA

Run up to 3 JQL queries to find matches:

```
mcp__atlassian__jira_search({
  jql: "{JQL_QUERY}",
  fields: "summary,status,issuetype,assignee,priority,labels,created,updated,resolution",
  limit: 10
})
```

Deduplicate results across queries by ticket key.

### Step 3: Rank and Return Results

For each matching ticket, assess relevance:

| Relevance | Criteria |
|-----------|----------|
| **High** | Summary contains 3+ matching keywords, same issue type, open status |
| **Medium** | Summary contains 1-2 matching keywords, or similar component |
| **Low** | Only text body matches, or ticket is resolved/old |

---

## Output Format

```markdown
### Duplicate Search Results ({count} found)

| # | Key | Summary | Status | Relevance | Updated |
|---|-----|---------|--------|-----------|---------|
| 1 | {KEY} | {summary} | {status} | High | {date} |
| 2 | {KEY} | {summary} | {status} | Medium | {date} |

### Recommendation
- **{HIGH_COUNT} high-relevance matches** -- review before creating a new ticket
- **{MEDIUM_COUNT} medium-relevance matches** -- may be related
- **{LOW_COUNT} low-relevance matches** -- likely different issues
```

If no matches found:
```markdown
### Duplicate Search Results (0 found)
No potential duplicates found for the given keywords. Safe to create a new ticket.
```

---


## Guidelines

### Search Strategy

1. **Build multiple JQL queries** to maximize coverage:
   - Exact phrase match on summary
   - Keyword combination match
   - Full-text search across all fields

2. **Relevance ranking** criteria:
   - High: 3+ keyword matches, same issue type, open status
   - Medium: 1-2 keyword matches, or similar component
   - Low: Only text body matches, or ticket is resolved/old

3. **Deduplication**: When multiple queries return the same ticket, keep it once with the highest relevance.

4. **Scope control**: Exclude resolved tickets older than 6 months unless explicitly requested.

### Keyword Extraction

- From error messages: strip stack traces, timestamps, dynamic values
- From summaries: extract nouns, component names, action verbs
- From descriptions: extract error codes, UI element names, feature names

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
