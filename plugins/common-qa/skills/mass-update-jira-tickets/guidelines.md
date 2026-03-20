# Mass Update JIRA Tickets Guidelines

Standards for safely updating JIRA tickets in bulk, handling pagination, preserving existing data, and reporting results.

---

# Detailed Workflow Content (moved from SKILL.md)

## Section 1: Action-Specific Gathering Details (Step 0)

When gathering action-specific details in Step 0, use these patterns:

### For Transition:
- Ask: "What status do you want to transition tickets to?" (e.g., "In Progress", "Done", "Closed")
- Note: Available transitions depend on each ticket's current status and workflow

### For Add/Remove labels:
- Ask: "Which label(s) to add/remove?"
- Validate: Labels must not contain spaces (JIRA restriction), are case-sensitive
- If labels contain spaces, suggest underscore replacement (e.g., `AI Testing` → `AI_Testing`)

### For Update fields:
- Ask: "Which field(s) do you want to update and to what value?"
- Examples: `assignee`, `priority`, `components`, `summary`, `description`, `fixVersions`

### For Add comment:
- Ask: "What comment text do you want to add?"

### For Combined actions:
- Collect all actions the user wants to perform together

---

## Section 2: JQL Conversion Patterns (Step 0)

Natural language to JQL conversion examples:

| Natural Language | JQL |
|-----------------|-----|
| "All test cases with SlackApp label" | `issuetype = Test AND labels = SlackApp` |
| "All open bugs in DHK project" | `project = DHK AND issuetype = Bug AND status != Done` |
| "Move all To Do tickets to In Progress" | `status = "To Do" AND project = {PROJECT}` |
| "My unresolved tickets" | `assignee = currentUser() AND resolution = Unresolved` |
| "All test cases in project DHK" | `issuetype = Test AND project = DHK` |
| "Tickets in a specific epic" | `parent = EPIC-123` |
| "Recently created tickets" | `created >= -7d AND project = DHK` |
| "Specific ticket keys" | `key in (DHK-2776, DHK-2777, DHK-2778)` |

---

## Section 3: Detailed Pagination Handling (Step 1)

JIRA returns max 50 results per API call. For queries matching more than 50 tickets, use pagination:

```
# First page
mcp__atlassian__jira_search({
  jql: "{JQL_QUERY}",
  fields: "summary,labels,status,issuetype,assignee,priority",
  limit: 50,
  start_at: 0
})

# Subsequent pages
mcp__atlassian__jira_search({
  jql: "{JQL_QUERY}",
  fields: "summary,labels,status,issuetype,assignee,priority",
  limit: 50,
  start_at: 50  # then 100, 150, etc.
})
```

### Pagination Logic:

```
Page 1: start_at=0,  limit=50  → tickets 1-50
Page 2: start_at=50, limit=50  → tickets 51-100
Page 3: start_at=100, limit=50 → tickets 101-150
...continue until all fetched
```

### Determining Total Count:
- Jira Cloud may return `total: -1` (unknown total)
- In that case, keep fetching until the returned issues count < limit
- If `total` is a positive number, use it to calculate remaining pages

---

## Section 4: Pre-Filter Logic Table (Step 2)

Before calling the update API, skip tickets where the action is a no-op:

| Action | Pre-filter Logic | Skip Reason |
|--------|-----------------|-------------|
| **Add label** | Ticket already has the label | "Already has label" |
| **Remove label** | Ticket doesn't have the label | "Label not present" |
| **Replace label** | Ticket doesn't have the old label | "Old label not present" |
| **Transition** | Ticket already in target status | "Already in target status" |
| **Update field** | Field already has the target value | "Field already set" |
| **Add comment** | No pre-filter (always applicable) | — |

This avoids unnecessary API calls and prevents modifying `updated` timestamps on tickets.

### Confirmation Flow:

**Option 1: Proceed with update (Recommended)**
- Update all applicable tickets immediately

**Option 2: Show all tickets first**
- Display the full list of tickets with their current state
- Ask again for confirmation

**Option 3: Cancel**
- Exit without making changes

---

## Section 5: Detailed Action Execution (Step 3)

### For Transition:

1. **Get available transitions for the first ticket** to find the transition ID:
   ```
   mcp__atlassian__jira_get_transitions({
     issue_key: "{TICKET_KEY}"
   })
   ```

   **Response example:**
   ```json
   [
     { "id": "11", "name": "To Do" },
     { "id": "21", "name": "In Progress" },
     { "id": "31", "name": "Done" }
   ]
   ```

2. **Find the matching transition** by name (e.g., "In Progress", "Done")

3. **Apply transition to each ticket:**
   ```
   mcp__atlassian__jira_transition_issue({
     issue_key: "{TICKET_KEY}",
     transition_id: "{TRANSITION_ID}"
   })
   ```

**Best Practices:**
- Same workflow assumption: Tickets in the same project usually share the same workflow, so the transition ID from the first ticket typically works for others
- Handle exceptions: Some tickets may have different workflows (e.g., different issue types). If a transition fails, log it and continue
- Status mismatch: A ticket in "Done" status won't have a "Done" transition available — skip these

**Note:** Different tickets may have different available transitions depending on their current status. If a transition is not available for a ticket, log it as skipped.

### Transition with Required Fields:

Some transitions require fields (e.g., resolution when closing):
```
mcp__atlassian__jira_transition_issue({
  issue_key: "DHK-2776",
  transition_id: "31",
  fields: "{\"resolution\": {\"name\": \"Done\"}}"
})
```

---

### For Add Label(s):

1. Compute new labels: `new_labels = current_labels + [new_label]` (no duplicates)
2. Update ticket:
   ```
   mcp__atlassian__jira_update_issue({
     issue_key: "{TICKET_KEY}",
     fields: "{\"labels\": [\"label1\", \"label2\", \"new_label\"]}"
   })
   ```

**CRITICAL**: Always preserve existing labels. Never overwrite — always merge.

**Correct approach:**
```
current_labels = ["AutomationBlocked", "SlackApp"]
label_to_add = "AI_Testing"
new_labels = ["AutomationBlocked", "SlackApp", "AI_Testing"]  # merged
```

**Wrong approach:**
```
new_labels = ["AI_Testing"]  # THIS DELETES EXISTING LABELS
```

---

### For Remove Label(s):

1. Compute new labels: `new_labels = current_labels - [label_to_remove]`
2. Update ticket with the filtered labels array

---

### For Replace Label:

1. Compute new labels: `new_labels = (current_labels - [old_label]) + [new_label]`
2. Update ticket with the new labels array

---

### For Update Field(s):

1. Build the fields JSON based on user input:
   ```
   mcp__atlassian__jira_update_issue({
     issue_key: "{TICKET_KEY}",
     fields: "{\"assignee\": \"user@example.com\", \"priority\": {\"name\": \"High\"}}"
   })
   ```

---

### For Add Comment:

1. Add comment to each ticket:
   ```
   mcp__atlassian__jira_add_comment({
     issue_key: "{TICKET_KEY}",
     body: "{COMMENT_TEXT}"
   })
   ```

---

### Batch Processing Strategy:

Update tickets in parallel batches for efficiency:

| Batch Size | Use When |
|-----------|----------|
| Up to 24 parallel calls | Default — matches API concurrency limits |
| 10 parallel calls | If getting rate limit errors |
| 1 sequential call | If critical failures on parallel calls |

**Progress Reporting:**
- For large batches (>20 tickets), report progress every 20 tickets:
  ```
  Progress: {COMPLETED}/{TOTAL} tickets updated...
  ```

**Track Results:**
- Count: updated, skipped, failed
- For failures: record ticket key and error message

**Failure Handling:**
- Never stop the entire batch for a single failure
- Log failures and continue with remaining tickets
- Report all failures at the end with error details
- Offer to retry failed tickets

---

## Section 6: Detailed Report Templates (Step 4)

### Summary Format:

```
Update complete!

Action(s): {ACTION_SUMMARY}
JQL: {JQL_QUERY}

Results:
| Status | Count |
|--------|-------|
| Updated | {UPDATED_COUNT} |
| Skipped | {SKIPPED_COUNT} |
| Failed | {FAILED_COUNT} |
| **Total** | **{TOTAL_COUNT}** |
```

### Failure Report:

If there were failures, list them:

```
Failed tickets:
| Key | Error |
|-----|-------|
| DHK-XXXX | {error_message} |
```

### Updated Tickets Table:

```
Updated tickets:
| # | Key | Summary | Change Applied |
|---|-----|---------|----------------|
| 1 | DHK-2776 | [SlackApp] Subscribe... | Status: To Do → In Progress |
| 2 | DHK-2777 | [SlackApp] Unsubscri... | Status: To Do → In Progress |
...
```

For large results (>20 tickets), show first 20 and note the rest:
```
... and {REMAINING} more tickets updated successfully.
```

### Change Details Format:

Show what changed for each ticket:

| Action | Change Applied Column |
|--------|----------------------|
| Transition | `Status: To Do → In Progress` |
| Add label | `Added label: AI_Testing` |
| Remove label | `Removed label: AutomationBlocked` |
| Update field | `Priority: Medium → High` |
| Add comment | `Comment added` |

---

## Section 7: Detailed Workflow Diagram (Complete Version)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  Step 0: Pre-Flight Checks                                                       │
│     ├─ Verify Atlassian MCP connectivity                                         │
│     │  └─ Test call to mcp__atlassian__jira_search                               │
│     ├─ Validate user input (JQL query + action)                                 │
│     │  ├─ Ask for JQL query if not provided                                     │
│     │  ├─ Ask for action type if not provided                                   │
│     │  └─ Gather action-specific parameters                                     │
│     └─ Parse and validate JQL                                                    │
│        ├─ Convert natural language to JQL if needed                             │
│        └─ Confirm JQL with user if unclear                                      │
│                                                                                  │
│  Step 1: Search Tickets                                                          │
│     ├─ Execute JQL query with pagination                                        │
│     │  ├─ First page: start_at=0, limit=50                                      │
│     │  ├─ Check total count in response                                         │
│     │  └─ Loop: start_at=50, 100, 150... until all fetched                      │
│     ├─ Collect all matching tickets                                              │
│     │  └─ Store: key, summary, labels, status, issuetype, assignee, priority    │
│     └─ Present summary to user for confirmation                                 │
│        ├─ Display total count                                                    │
│        └─ Show first 10 tickets in table                                         │
│                                                                                  │
│  Step 2: Confirm Action                                                          │
│     ├─ Pre-filter tickets (skip no-op actions)                                  │
│     │  ├─ Already has label → skip                                              │
│     │  ├─ Label not present → skip                                              │
│     │  ├─ Already in target status → skip                                       │
│     │  └─ Field already set → skip                                              │
│     ├─ Show ticket count and planned action(s)                                  │
│     │  ├─ Total count                                                            │
│     │  ├─ Skip count (pre-filtered)                                             │
│     │  └─ Update count (applicable)                                             │
│     └─ Ask user to confirm before proceeding                                    │
│        ├─ Option 1: Proceed with update                                         │
│        ├─ Option 2: Show all tickets first                                      │
│        └─ Option 3: Cancel                                                       │
│                                                                                  │
│  Step 3: Execute Updates                                                         │
│     ├─ For each ticket, apply the requested action(s)                           │
│     │  ├─ Transition: get available transitions → find ID → apply               │
│     │  ├─ Add label: merge with existing labels → update                        │
│     │  ├─ Remove label: filter from existing labels → update                    │
│     │  ├─ Replace label: remove old + add new → update                          │
│     │  ├─ Update field: build fields JSON → update                              │
│     │  └─ Add comment: add comment to ticket                                    │
│     ├─ Handle transitions, labels, fields, comments                             │
│     │  ├─ Execute in parallel batches (up to 24 concurrent)                     │
│     │  ├─ Report progress every 20 tickets (for large batches)                  │
│     │  └─ Handle failures gracefully (log, continue)                            │
│     └─ Track successes and failures                                             │
│        ├─ Count: updated, skipped, failed                                       │
│        └─ Record failure details (key, error message)                           │
│                                                                                  │
│  Step 4: Report Results                                                          │
│     ├─ Summary table of all updated tickets                                      │
│     │  ├─ Results: Updated, Skipped, Failed, Total                              │
│     │  └─ For each ticket: #, Key, Summary, Change Applied                      │
│     └─ Report any failures                                                       │
│        ├─ Failure table: Key, Error                                             │
│        └─ Offer to retry failed tickets                                         │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

# General Safety Rules

## 1. Always Confirm Before Bulk Updates

**CRITICAL**: Never execute bulk updates without explicit user confirmation.

**Small batch (1-10 tickets):** Show all tickets in the confirmation prompt.

**Medium batch (11-50 tickets):** Show first 10, mention total count.

**Large batch (>50 tickets):** Show first 10, mention total count, warn about duration:
```
Large batch: {COUNT} tickets will be updated.
Estimated time: ~{SECONDS} seconds.
```

## 2. Never Overwrite — Always Merge (Labels)

When updating a ticket's labels, always preserve existing labels.

**Correct approach:**
```
current_labels = ["AutomationBlocked", "SlackApp"]
label_to_add = "AI_Testing"
new_labels = ["AutomationBlocked", "SlackApp", "AI_Testing"]  # merged
```

**Wrong approach:**
```
new_labels = ["AI_Testing"]  # THIS DELETES EXISTING LABELS
```

---

# Label Validation

| Rule | Example |
|------|---------|
| No spaces in labels | `AI Testing` → use `AI_Testing` |
| Case-sensitive | `AI_Testing` ≠ `ai_testing` |
| No special characters except `_` and `-` | `AI_Testing` or `AI-Testing` are valid |
| No duplicates in label array | Check before adding |

---

# Anti-Patterns

### Updating Without Confirmation
**Problem**: User may have wrong JQL query, updating wrong tickets
**Solution**: Always show ticket count and sample before proceeding

### Overwriting Labels
**Problem**: Setting labels array to only the new label deletes existing ones
**Solution**: Always read current labels first and merge

### Ignoring Pagination
**Problem**: Only updating the first 50 tickets, missing the rest
**Solution**: Always paginate through all results

### No Pre-filtering
**Problem**: Unnecessary API calls for tickets that already match the target state
**Solution**: Check current state before calling update

### Assuming All Tickets Have Same Transitions
**Problem**: Different issue types may have different workflows
**Solution**: Handle transition failures gracefully, log as skipped

### Sequential Updates for Large Batches
**Problem**: Updating 100+ tickets one at a time is slow
**Solution**: Use parallel batches (up to 24 concurrent calls)

---

# Quality Checklist

Before executing the mass update:

- [ ] JQL query is correct and returns expected tickets
- [ ] Action and parameters are validated
- [ ] User has confirmed the action
- [ ] Pre-filtering is applied (skip no-op tickets)
- [ ] For labels: existing labels are preserved in the update
- [ ] For transitions: available transitions are checked
- [ ] Pagination is handled for queries with >50 results
- [ ] Results are reported with success/skip/failure counts

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (verify Atlassian MCP, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Search tickets matching JQL query", status: "pending", activeForm: "Searching tickets matching JQL query" },
  { content: "Confirm action with user", status: "pending", activeForm: "Confirming action with user" },
  { content: "Execute updates on all matching tickets", status: "pending", activeForm: "Executing updates on tickets" },
  { content: "Report results", status: "pending", activeForm: "Reporting results" }
])
```

**Update rules:**
- Mark current step as `in_progress` when starting it
- Mark step as `completed` immediately when finished (do not batch)
- Only ONE step should be `in_progress` at any time

---

## Error Handling

| Error | Action |
|-------|--------|
| Atlassian MCP not available | Display setup instructions, exit |
| Invalid JQL syntax | Display JIRA error message, ask user to correct query |
| No tickets found for query | Inform user, suggest broadening query, exit |
| Single ticket update fails | Log error, continue with remaining tickets, report at end |
| JIRA API rate limit | Wait 2 seconds between batches, retry failed calls once |
| Label contains spaces | Warn user, suggest underscore replacement |
| Permission denied on ticket | Log error, continue, report at end |
| Transition not available | Log as skipped (ticket may be in a different workflow state), continue |
| Field not editable | Log error, inform user, continue with other tickets |

---

## Self-Correction

When user requests adjustments:

1. **"Use a different JQL query"** → Re-run search with new query
2. **"Add another action"** → Chain additional action to the current operation
3. **"Only update tickets in To Do status"** → Refine JQL with `AND status = "To Do"`
4. **"Skip certain tickets"** → Allow user to exclude specific ticket keys
5. **"Undo the changes"** → Offer reverse operation (remove added label, reverse transition if possible)
6. **"Try a different transition"** → Show available transitions and let user pick

---

## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Ticket search, updates, transitions, comments (REQUIRED) | No fallback - skill cannot run without it |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| JQL + action | `issuetype = Test AND project = DHK` + transition to "Done" |
| Natural language | "Move all To Do test cases in DHK to In Progress" |
| Multiple actions | Transition to Done + add label `AutomationDone` + add comment |
| Ticket list | "Add label X to DHK-2776, DHK-2777" (converted to JQL: `key in (...)`) |

### Label Rules

- Labels are **case-sensitive** in JIRA (`AI_Testing` ≠ `ai_testing`)
- Labels **cannot contain spaces** — use underscores or camelCase
- Existing labels are **always preserved** — never overwrite the entire labels array
- Adding a label that already exists is a **no-op** (ticket is skipped)

### Transition Rules

- Available transitions depend on the ticket's **current status** and **workflow configuration**
- Not all tickets in a batch may support the same transition
- Always check available transitions before attempting to transition
- Tickets already in the target status are skipped

### Integration with Other Skills

- **`/exp-qa-agents:execute-test-case`**: After test execution, use this skill to tag or transition tested tickets
- **`/exp-qa-agents:create-test-cases`**: After generating test cases, bulk-label or transition them
- **`/exp-qa-agents:analyze-ticket`**: Analyze tickets before deciding which updates to apply
