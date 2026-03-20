# Sample Mass Update: Transition + Add Label

This is an example of a mass update produced by the mass-update-jira-tickets skill, combining a workflow transition with a label addition.

---

## Input

User request: "Move all To Do test cases with SlackApp label to In Progress and add label AI_Testing"

Parsed:
- **JQL:** `issuetype = Test AND labels = SlackApp AND status = "To Do" ORDER BY key ASC`
- **Actions:**
  1. Transition to "In Progress"
  2. Add label `AI_Testing`

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - Atlassian MCP: Connected
   - JQL Query: issuetype = Test AND labels = SlackApp AND status = "To Do" ORDER BY key ASC
   - Action(s): Transition to "In Progress" + Add label "AI_Testing"

Proceeding to search tickets...
```

---

## Step 1: Search Tickets

```
Found 12 ticket(s) matching query:
JQL: issuetype = Test AND labels = SlackApp AND status = "To Do" ORDER BY key ASC

Sample (first 10):
| # | Key | Summary | Status | Labels |
|---|-----|---------|--------|--------|
| 1 | DHK-2776 | [SlackApp] Subscribe/Unsubscribe for Web | To Do | AutomationBlocked, SlackApp |
| 2 | DHK-2777 | [SlackApp] Subscribe/Unsubscribe for Edge | To Do | AutomationBlocked, SlackApp |
| 3 | DHK-2778 | [SlackApp] Subscribe/Unsubscribe for Flag | To Do | AutomationBlocked, SlackApp |
| 4 | DHK-2779 | [SlackApp] Subscribe to multiple projects | To Do | AutomationBlocked, SlackApp |
| 5 | DHK-2784 | [SlackApp] Verify /disconnect | To Do | AutomationBlocked, SlackApp |
| 6 | DHK-2786 | [SlackApp] Login with SSO | To Do | SlackApp |
| 7 | DHK-2787 | [SlackApp] Change notification channel | To Do | SlackApp |
| 8 | DHK-2788 | [SlackApp] DM notifications | To Do | SlackApp |
| 9 | DHK-2789 | [SlackApp] Flag change notifications | To Do | SlackApp |
| 10 | DHK-2790 | [SlackApp] Experiment result notifications | To Do | SlackApp |

... and 2 more tickets
```

---

## Step 2: Confirm Action

```
Ready to update 12 ticket(s):

Action(s):
1. Transition: To Do → In Progress
2. Add label: AI_Testing

Tickets that will be skipped: 0
Tickets that will be updated: 12
```

User selected: "Proceed with update"

---

## Step 3: Execute Updates

For each ticket:
1. Get available transitions → find "In Progress" transition (ID: 21)
2. Transition ticket to "In Progress"
3. Read current labels, merge with `AI_Testing`, update labels

All 12 tickets updated in parallel (single batch).

---

## Step 4: Report Results

```
Update complete!

Action(s): Transition to "In Progress" + Add label "AI_Testing"
JQL: issuetype = Test AND labels = SlackApp AND status = "To Do" ORDER BY key ASC

Results:
| Status | Count |
|--------|-------|
| Updated | 12 |
| Skipped | 0 |
| Failed | 0 |
| **Total** | **12** |

Updated tickets:
| # | Key | Summary | Change Applied |
|---|-----|---------|----------------|
| 1 | DHK-2776 | [SlackApp] Subscribe/Unsubscribe for Web | Status: To Do → In Progress, Added: AI_Testing |
| 2 | DHK-2777 | [SlackApp] Subscribe/Unsubscribe for Edge | Status: To Do → In Progress, Added: AI_Testing |
| 3 | DHK-2778 | [SlackApp] Subscribe/Unsubscribe for Flag | Status: To Do → In Progress, Added: AI_Testing |
| ... | ... | ... | ... |
| 12 | DHK-2791 | [SlackApp] Webhook retry notifications | Status: To Do → In Progress, Added: AI_Testing |

Summary: 12 updated, 0 skipped, 0 failed
```
