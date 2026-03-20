# Verify Bug Simple Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## Detailed Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  0. Pre-Flight Checks                                                            │
│     ├─ Verify Atlassian MCP and Playwright MCP connectivity                     │
│     └─ Validate JIRA ticket input                                               │
│                                                                                  │
│  1. Read & Parse JIRA Ticket                                                     │
│     ├─ Fetch ticket details (summary, description, assignee, status)            │
│     ├─ Extract test steps / reproduction steps from description                 │
│     └─ Extract expected results                                                 │
│                                                                                  │
│  2. Execute Test Steps via Playwright                                            │
│     ├─ Open browser and navigate to the target URL                              │
│     ├─ Follow each test step sequentially                                       │
│     ├─ Capture screenshots at key checkpoints                                   │
│     └─ Record actual results for each step                                      │
│                                                                                  │
│  3. Compare & Determine Result                                                   │
│     ├─ Compare actual results to expected results                               │
│     └─ Determine overall: PASSED or FAILED                                      │
│                                                                                  │
│  4. Update JIRA Ticket                                                           │
│     ├─ Add comment with test result + mention assignee                          │
│     ├─ If PASSED: transition ticket to Closed/Done                              │
│     └─ If FAILED: keep ticket open                                              │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Supported Description Formats (Step 1 Detail)

The skill must handle these description formats found in JIRA bug tickets:

**Format A — Steps to Reproduce:**
```
Steps to Reproduce:
1. Go to https://example.com
2. Click on "Login"
3. Enter credentials
4. Click "Submit"

Expected Result:
- User is redirected to dashboard
```

**Format B — Test Steps / Test Script:**
```
Test Steps:
1. Navigate to the settings page
2. Toggle dark mode
3. Verify background changes to dark

Expected: Background color is #1a1a1a
```

**Format C — Precondition + Steps:**
```
Precondition: User is logged in
Steps:
1. Click profile icon
2. Select "Settings"
Expected: Settings page loads without error
```

**Format D — Acceptance Criteria style (Given/When/Then):**
```
Given I am on the login page
When I enter valid credentials
And I click "Sign In"
Then I should see the dashboard
And the welcome message shows my name
```

---

## 2. Step-to-Action Mapping for Playwright (Step 2 Detail)

| Step Description Pattern | Playwright Action |
|-------------------------|-------------------|
| "Go to" / "Navigate to" / "Open" + URL | `browser_navigate({ url })` |
| "Click" + element description | `browser_click({ ref, element })` |
| "Type" / "Enter" / "Input" + text | `browser_type({ ref, text })` |
| "Select" + option | `browser_select_option({ ref, values })` |
| "Wait for" + text/element | `browser_wait_for({ text })` |
| "Verify" / "Check" / "Confirm" + condition | `browser_snapshot()` + verify |
| "Upload" + file | `browser_file_upload({ paths })` |
| "Press" + key | `browser_press_key({ key })` |
| "Scroll" to element | `browser_click` to scroll into view |

---

## 3. Element Finding Strategy (Step 2 Detail)

Always take a snapshot first to identify elements:

```
1. browser_snapshot() → get page structure with refs
2. Find the target element by text, role, or label
3. Use the ref from snapshot for the action
```

Never guess CSS selectors. Always use the snapshot ref system.

---

## 4. Screenshot Strategy (Step 2 Detail)

Take screenshots at these moments:
- **Before test starts**: Initial page state
- **After each significant step**: To track progress
- **At verification point**: Evidence of actual result
- **On failure**: Current page state when something goes wrong

---

## 5. Result Determination (Step 3 Detail)

### What "Matches Expected" Means

When comparing actual results to expected results, use these criteria:

- **Text comparison**: Expected text is visible on the page (use snapshot)
- **State comparison**: Element is in expected state (visible, enabled, checked)
- **Navigation**: Page navigated to expected URL
- **Visual**: Page looks as described (use screenshot for evidence)
- **Absence**: Error message or broken state is NOT present

### Result Summary Templates

**If PASSED:**
```
Test Result: PASSED

Ticket: {TICKET_KEY} - {SUMMARY}
Steps Executed: {N}/{TOTAL}
All steps completed successfully.

Expected: {EXPECTED_RESULT}
Actual: {ACTUAL_RESULT} -- matches expected

Evidence: [screenshot captured]
```

**If FAILED:**
```
Test Result: FAILED

Ticket: {TICKET_KEY} - {SUMMARY}
Steps Executed: {N}/{TOTAL}
Failed at: Step {N} - {STEP_DESCRIPTION}

Expected: {EXPECTED_RESULT}
Actual: {ACTUAL_RESULT} -- does NOT match expected

Evidence: [screenshot captured]
```

---

## 6. MCP Setup Instructions (Step 0 Detail)

### Atlassian MCP Not Available

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

### Playwright MCP Not Available

```
Error: Playwright MCP is not configured

This skill requires Playwright MCP server for browser automation.

Setup Instructions:
1. Ensure .mcp.json.template exists in project root with Playwright server configuration
2. Restart Claude Code
3. Verify access with: mcp__playwright__browser_snapshot

See .mcp.json.template for detailed configuration.
Cannot proceed without Playwright MCP configuration.
```

---

## 7. Anti-Patterns

### Skipping Confirmation
**Problem**: Updating JIRA without user reviewing the result
**Solution**: Always show result summary and ask for confirmation before posting

### Guessing Element Selectors
**Problem**: Trying CSS selectors instead of using snapshot refs
**Solution**: Always take a snapshot first, find elements by their text/role/ref

### Ignoring Login Requirements
**Problem**: Test fails because the page requires authentication
**Solution**: Check for login pages, ask user for credentials or pre-login

### Posting Comment Without Mention
**Problem**: Assignee doesn't get notified of the test result
**Solution**: Always include `[~accountid:...]` mention in the comment

### Closing Ticket on Failure
**Problem**: Accidentally transitioning ticket to Done when test failed
**Solution**: Only transition on PASS; on FAIL, keep ticket open

### Not Taking Screenshots
**Problem**: No evidence of test execution
**Solution**: Take screenshots at verification points for evidence

---

## 8. Quality Checklist

Before updating JIRA:

- [ ] Test steps were parsed correctly from the description
- [ ] User confirmed the parsed steps before execution
- [ ] All steps were executed (or failures documented)
- [ ] Screenshots captured at key checkpoints
- [ ] Actual result compared to expected result
- [ ] PASSED/FAILED determination is accurate
- [ ] Comment includes step-by-step results
- [ ] Assignee is mentioned in the comment
- [ ] Only close ticket on PASS (not on FAIL)
- [ ] User confirmed before posting to JIRA

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (verify MCP servers, validate ticket)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Read and parse JIRA ticket", status: "pending", activeForm: "Reading and parsing JIRA ticket" },
  { content: "Execute test steps via Playwright browser", status: "pending", activeForm: "Executing test steps via Playwright" },
  { content: "Compare results and determine PASS/FAIL", status: "pending", activeForm: "Comparing results" },
  { content: "Update JIRA ticket with results", status: "pending", activeForm: "Updating JIRA ticket with results" }
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
| Playwright MCP not available | Display setup instructions, exit |
| JIRA ticket not found | Display error, ask user to verify ticket key |
| Ticket has no description | Ask user to provide test steps manually |
| Test steps cannot be parsed | Show raw description, ask user to identify steps |
| Element not found in browser | Take screenshot, log error, mark step as failed |
| Page timeout | Take screenshot, log error, retry once, then mark as failed |
| Login required but no credentials | Ask user for credentials or to pre-login |
| No Done/Closed transition available | Warn user, skip closing, still add comment |
| Assignee not set on ticket | Post comment without mention, warn user |
| Browser crashes | Report error, suggest re-running |

---


## Self-Correction

When user requests adjustments:

1. **"Use a different URL"** → Re-navigate and re-run test steps
2. **"Skip step N"** → Skip the specified step and continue
3. **"The expected result is wrong"** → Accept user's corrected expected result
4. **"Re-run the test"** → Execute all test steps again from the beginning
5. **"Don't close the ticket"** → Post comment but skip the transition
6. **"Add more details to the comment"** → Edit comment before posting
7. **"Try with different credentials"** → Re-login and re-run

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Read ticket, post comment, transition (REQUIRED) | No fallback |
| Playwright | Browser automation for test execution (REQUIRED) | No fallback |

### Mentioning Assignee in JIRA Comments

To mention a user in JIRA Cloud comments, use the account ID format:
```
[~accountid:ACCOUNT_ID_HERE]
```

The account ID is available from the ticket's `assignee` field. If the assignee field returns a `displayName` but no `accountId`, use the display name format:
```
@DisplayName
```

### Test Step Parsing Hints

The skill looks for test steps in the description using these keywords:
- "Steps to Reproduce"
- "Test Steps"
- "Steps"
- "Reproduction Steps"
- "How to Test"
- Numbered lists (1. 2. 3.)

And expected results using:
- "Expected Result"
- "Expected"
- "Expected Behavior"
- "Should"

### Input Flexibility

| Input Type | Example |
|------------|---------|
| JIRA URL | `https://optimizely-ext.atlassian.net/browse/DHK-4506` |
| Ticket key | `DHK-4506` |
| Natural language | "Verify bug DHK-4506" |

### Integration with Other Skills

- **`/exp-qa-agents:create-bug-ticket`**: If verification fails and a new bug is needed, use this skill
- **`/exp-qa-agents:analyze-ticket`**: For deeper analysis of the ticket before verification
- **`/common-qa:mass-update-jira-tickets`**: For bulk verification of multiple bugs (run this skill per ticket, then bulk-update)
