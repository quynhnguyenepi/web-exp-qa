# Test Cases for mass-update-jira-tickets Skill

## TC-001: Transition Tickets to New Status

**Input:** Run `/common-qa:mass-update-jira-tickets` with JQL `status = "To Do" AND project = DHK` and action "Transition to In Progress"

**Expected:**
- Searches JIRA and finds matching tickets
- Gets available transitions from the first ticket
- Shows summary and asks for confirmation
- Transitions all tickets to "In Progress"
- Reports results with updated count

**Pass Criteria:**
- All matching tickets transitioned to "In Progress"
- Tickets already "In Progress" are skipped
- Summary shows correct updated/skipped/failed counts

---

## TC-002: Add Label to Tickets

**Input:** Run with JQL `issuetype = Test AND labels = SlackApp` and action "Add AI_Testing"

**Expected:**
- Searches JIRA and finds matching tickets
- Shows summary and asks for confirmation
- Adds label to all tickets, preserving existing labels
- Reports results with updated count

**Pass Criteria:**
- All matching tickets have `AI_Testing` added
- Existing labels (`AutomationBlocked`, `SlackApp`) are preserved
- Tickets that already have `AI_Testing` are skipped

---

## TC-003: Remove Label from Tickets

**Input:** Run with action "Remove" and label `AutomationBlocked`

**Expected:**
- Removes `AutomationBlocked` from each ticket's labels
- Preserves all other labels
- Skips tickets without `AutomationBlocked`

**Pass Criteria:**
- `AutomationBlocked` is removed from all matching tickets
- Other labels remain intact
- Skipped count matches tickets without the label

---

## TC-004: Combined Actions (Transition + Label)

**Input:** Run with action "Transition to Done" + "Add label AutomationDone"

**Expected:**
- Transitions tickets to "Done" status
- Adds `AutomationDone` label in the same operation
- Both actions applied per ticket

**Pass Criteria:**
- Tickets are in "Done" status after update
- `AutomationDone` label is added
- Existing labels preserved

---

## TC-005: Update Field (Assignee)

**Input:** Run with JQL `project = DHK AND issuetype = Bug` and action "Set assignee to user@example.com"

**Expected:**
- Updates assignee field on all matching tickets
- Reports results

**Pass Criteria:**
- All matching tickets have new assignee
- Other fields unchanged

---

## TC-006: Add Comment to Tickets

**Input:** Run with JQL `parent = DHK-2304` and action "Add comment: Reviewed by QA team"

**Expected:**
- Adds comment to all matching tickets
- No pre-filtering (comments always applicable)

**Pass Criteria:**
- Comment appears on all matching tickets
- No tickets skipped

---

## TC-007: Large Batch with Pagination (>50 Tickets)

**Input:** Run with a JQL query that returns 120 tickets

**Expected:**
- Fetches page 1 (tickets 1-50), page 2 (51-100), page 3 (101-120)
- Collects all 120 tickets before showing confirmation
- Updates all tickets in parallel batches
- Reports progress every 20 tickets

**Pass Criteria:**
- All 120 tickets are found (not just first 50)
- Pagination handles correctly
- All tickets are updated

---

## TC-008: Transition Not Available for Some Tickets

**Input:** Run transition on tickets where some are in different workflow states

**Expected:**
- Tickets with available transition are updated
- Tickets without the transition are logged as skipped
- Does not abort the entire batch

**Pass Criteria:**
- Successfully transitioned tickets are counted as "Updated"
- Non-transitionable tickets are counted as "Skipped" with reason
- Summary is accurate

---

## TC-009: No Tickets Found

**Input:** Run with a JQL query that returns 0 results

**Expected:**
- Reports "No tickets found matching query"
- Suggests broadening the query
- Exits gracefully

**Pass Criteria:**
- Clear message about no results
- No confirmation prompt shown
- No update attempts made

---

## TC-010: User Cancels After Seeing Results

**Input:** User chooses "Cancel" at the confirmation step

**Expected:**
- No tickets are updated
- Clean exit with message "Operation cancelled. No changes made."

**Pass Criteria:**
- Zero API update calls made
- Clear cancellation message

---

## TC-011: Natural Language Input

**Input:** "Move all To Do test cases in DHK to In Progress and add label AI_Testing"

**Expected:**
- Converts to JQL: `issuetype = Test AND status = "To Do" AND project = DHK`
- Extracts actions: Transition to "In Progress" + Add label "AI_Testing"
- Shows interpreted query for user confirmation

**Pass Criteria:**
- Correct JQL is generated
- Both actions extracted correctly
- User sees and confirms the interpreted query

---

## TC-012: Partial Failure During Update

**Input:** Run update on 10 tickets where 2 fail (e.g., permission denied)

**Expected:**
- Updates 8 tickets successfully
- Logs errors for 2 failed tickets
- Continues processing after failures
- Reports: 8 updated, 0 skipped, 2 failed

**Pass Criteria:**
- Failures don't stop the batch
- Failed tickets are listed with error details
- Successfully updated tickets are confirmed

---

## TC-013: Atlassian MCP Not Available

**Input:** Invoke when Atlassian MCP is not configured

**Expected:**
- Detects MCP is unavailable
- Displays setup instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message with setup instructions
- No partial state or dangling operations
