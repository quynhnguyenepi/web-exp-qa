---
description: Fetch a JIRA ticket's full context including details, comments, parent ticket, subtasks/children, and linked tickets -- all with their comments. Use when any skill needs comprehensive JIRA ticket data before analysis.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** `/exp-qa-agents:analyze-ticket`

# Reading JIRA Context

Fetch comprehensive JIRA ticket context: ticket details, filtered comments, parent ticket (epic or regular parent) with comments, subtasks/children with comments, and linked/related tickets with comments. Returns structured output with extracted URLs (Confluence, Figma) for downstream sub-skills.

## When to Use

Invoke this skill when you need to:

- Fetch a JIRA ticket's full details, description, and acceptance criteria
- Read and filter ticket comments for relevant context
- Fetch the parent ticket (epic or regular parent) with its comments
- Fetch subtasks/children with their comments
- Fetch linked/related tickets with their comments
- Extract Confluence and Figma URLs from ticket content for other sub-skills

## Workflow Overview

```
Pre-Flight -> Fetch Ticket -> Parse Comments -> Fetch Parent + Children + Linked (parallel) -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate user input:** Extract ticket ID using regex `([A-Z]+-\d+)` from URLs or direct IDs.
2. **Verify Atlassian MCP:** Attempt `mcp__atlassian__jira_get_issue` with the ticket ID. If not available, display standard error and exit:
   ```
   Error: Atlassian MCP is not configured

   This skill requires Atlassian MCP server for JIRA access.

   Setup Instructions:
   1. Ensure .mcp.json.template exists in project root with Atlassian server configuration
   2. Restart Claude Code
   3. Verify JIRA access with: mcp__atlassian__jira_get_issue

   See .mcp.json.template for detailed configuration.
   Cannot proceed without Atlassian MCP configuration.
   ```

### Step 1: Fetch Main Ticket

```
mcp__atlassian__jira_get_issue({
  issue_key: "{TICKET_ID}",
  fields: "summary,status,description,labels,components,issuetype,priority,assignee,reporter,parent,issuelinks,attachment,customfield_10014",
  expand: "renderedFields",
  comment_limit: 5
})
```

Extract: summary, description, AC, status, priority, labels, assignee, reporter, issue type, components, issuelinks, epic/parent field.

### Step 2: Parse and Filter Comments

For each comment, extract: author name, body, created date.

**Keep comments that contain:** clarifications on AC, edge cases, design decisions, bug reports, links to external resources.

**Discard comments that are:** status update bot messages, CI/CD notifications, automated workflow messages.

If AC is missing and comments provide insufficient context, ask user via AskUserQuestion.

### Step 3+4: Fetch Parent + Children + Linked Tickets IN PARALLEL

From the ticket's `issuelinks`, `parent`/`epic` fields, and subtasks, dispatch all fetches as **direct parallel MCP calls in a single message** (no Agent tool needed — each is 1-2 MCP calls):

**Call 1: Fetch Parent Ticket (with comments):**

From the ticket's `parent` or `epic` field (could be an Epic, Story, or any parent type):

```
mcp__atlassian__jira_get_issue({
  issue_key: "{PARENT_KEY}",
  fields: "summary,status,description,labels,components,issuetype,priority,assignee,reporter,parent,issuelinks,attachment",
  expand: "renderedFields",
  comment_limit: 5
})
```
Extract: summary, description, AC, status, type, and filtered comments (same rules as Step 2).
If parent itself has a parent, note it but do NOT recurse further (1 level up only).

**Call 2: Fetch Subtasks/Children:**

```
mcp__atlassian__jira_search({
  jql: "parent = {TICKET_ID} AND issuetype in (Story, Bug) ORDER BY created DESC",
  fields: "summary,status,issuetype,assignee,labels",
  limit: 50
})
```

For each child found, fetch with comments (batch all `get_issue` calls in one message):
```
mcp__atlassian__jira_get_issue({
  issue_key: "{CHILD_KEY}",
  comment_limit: 5
})
```
Extract per child: summary, status, type, assignee, labels, and filtered comments.
Note children with: `Requires_QA` label, Bug type, In Testing/In Review status.

**Call 3: Fetch Children of Parent (siblings):**

If a parent was found, search for its children to get sibling tickets:
```
mcp__atlassian__jira_search({
  jql: "parent = {PARENT_KEY} ORDER BY created DESC",
  fields: "summary,status,issuetype,assignee,labels",
  limit: 30
})
```
Note siblings with: `Requires_QA` label, Bug type, same assignee. Do NOT fetch comments for siblings (summary only).

**Calls 4+: Fetch Linked/Related Tickets (with comments):**

For each linked ticket from `issuelinks`, call directly (batch all in one message):
```
mcp__atlassian__jira_get_issue({
  issue_key: "{LINKED_KEY}",
  comment_limit: 5
})
```
Record: link type (Blocks, Relates to, Is tested by, Clones, Duplicates), summary, status, and filtered comments.

**Key optimization:** All of Calls 1-4+ are independent MCP calls. Issue them all in a single response message for maximum parallelism. No Agent tool overhead needed.

### Step 5: Extract URLs and Return Output

Scan description and comments for:
- **Confluence URLs:** Pattern `atlassian.net/wiki`
- **Figma URLs:** Pattern `figma.com/(?:file|design|proto)/`
- **Other external URLs:** Any other http/https links

Present output in the structured format below.

---

## Output Format

```markdown
### Ticket Details
- **Key:** {TICKET_ID}
- **Summary:** {summary}
- **Type:** {issue_type}
- **Status:** {status}
- **Priority:** {priority}
- **Assignee:** {assignee}
- **Reporter:** {reporter}
- **Labels:** {labels}
- **Components:** {components}

### Description & Acceptance Criteria
{full description text}

### Relevant Comments ({count})
For each relevant comment:
- **Author:** {name} | **Date:** {date}
- **Content:** {comment body}

### Parent Ticket
- **Key:** {PARENT_KEY}
- **Type:** {issue_type} (Epic / Story / Task / etc.)
- **Summary:** {summary}
- **Status:** {status}
- **Description:** {description snippet}
- **Comments ({count}):**
  - **Author:** {name} | **Date:** {date} | **Content:** {body}

### Subtasks/Children ({count})
For each child:
- **{CHILD_KEY}:** {summary} | Type: {type} | Status: {status} | Assignee: {assignee}
  - **Comments ({count}):**
    - **Author:** {name} | **Date:** {date} | **Content:** {body}

### Siblings (from parent) ({count})
- {count} total, {qa_count} with Requires_QA, {bug_count} bugs
- **{SIBLING_KEY}:** {summary} | Status: {status} | Labels: {labels}

### Linked/Related Tickets ({count})
For each linked ticket:
- **{LINKED_KEY}:** {summary} | Link type: {type} | Status: {status}
  - **Comments ({count}):**
    - **Author:** {name} | **Date:** {date} | **Content:** {body}

### URLs Found
- **Confluence:** {list of URLs}
- **Figma:** {list of URLs}
- **Other:** {list of URLs}
```

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
