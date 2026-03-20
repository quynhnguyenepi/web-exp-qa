---
description: Verify a bug fix by reading the JIRA ticket, executing test steps via Playwright browser automation, and updating the ticket with results. Use when you need to quickly verify a bug fix by following the test steps in a JIRA ticket.
---

## Dependencies

- **MCP Servers:** Atlassian, Playwright
- **Related Skills:** `/exp-qa-agents:create-bug-ticket`

# Verify Bug Fix (Simple)

Read a JIRA bug ticket, follow the test steps/reproduction steps in the description using Playwright MCP browser automation, compare actual results to expected results, then update the JIRA ticket with the test result (PASSED or FAILED) and mention the assignee.

## When to Use

Invoke this skill when you need to:

- Verify a bug fix by following the test steps in a JIRA ticket
- Quickly check if a reported bug is still reproducible
- Run a manual verification test via browser automation
- Confirm a fix before closing a bug ticket
- Re-verify a previously fixed bug after a regression

## Workflow Overview

**Simple Flow:**
```
Pre-Flight → Read Ticket → Execute Test → Compare Results → Update JIRA
```

**Detailed workflow diagram with step details available in guidelines.md.**

## Execution Workflow

Follow these 5 sequential steps. **See guidelines.md for detailed instructions, parsing examples, action mapping tables, and output templates.**

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Validate user input:**
   - Extract JIRA ticket key from URL or direct input
   - If not provided, ask user via AskUserQuestion

2. **Verify Atlassian MCP is enabled:**
   - Test call to `mcp__atlassian__jira_get_issue`
   - On failure, display setup instructions and exit (see guidelines.md)

3. **Verify Playwright MCP is enabled:**
   - Test call to `mcp__playwright__browser_snapshot`
   - On failure, display setup instructions and exit (see guidelines.md)

4. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Atlassian MCP: Connected
      - Playwright MCP: Connected
      - Ticket: {TICKET_KEY}
   ```

---

### Step 1: Read & Parse JIRA Ticket

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Read and parse JIRA ticket" as `in_progress`.

1. **Fetch ticket details:**
   ```
   mcp__atlassian__jira_get_issue({
     issue_key: "{TICKET_KEY}",
     fields: "summary,description,status,assignee,issuetype,labels,comment",
     comment_limit: 10
   })
   ```

2. **Extract key information:**
   - Summary, Description, Assignee, Status, Issue Type

3. **Parse test steps from description:**
   - Look for "Steps to Reproduce", "Test Steps", numbered lists
   - Extract Preconditions, Test Steps, Expected Results, Target URL
   - **Multiple format examples (Format A/B/C/D) in guidelines.md Section 1**

4. **If parsing fails:**
   - Show raw description to user
   - Ask for help identifying test steps

5. **Present parsed information and ask for confirmation:**
   - "Proceed with test execution" (Recommended)
   - "Edit test steps"
   - "Cancel"

---

### Step 2: Execute Test Steps via Playwright

**Todo:** Mark "Read and parse JIRA ticket" as `completed`, mark "Execute test steps via Playwright browser" as `in_progress`.

1. **Open browser and navigate:**
   ```
   mcp__playwright__browser_navigate({ url: "{TARGET_URL}" })
   ```

2. **Handle login if needed:**
   - Ask user for credentials if required

3. **Execute each test step:**
   - Map step description to Playwright action (see guidelines.md Section 2 for action mapping table)
   - For each step:
     a. Take snapshot before action
     b. Perform action
     c. Take snapshot/screenshot after
     d. Record actual result
     e. Report progress

4. **At final step:**
   - Take screenshot for evidence
   - Capture page snapshot for text verification

5. **On error:**
   - Take screenshot of error state
   - Log error
   - Determine if test can continue

---

### Step 3: Compare & Determine Result

**Todo:** Mark "Execute test steps via Playwright browser" as `completed`, mark "Compare results and determine PASS/FAIL" as `in_progress`.

1. **Compare actual results to expected results:**
   - Actual matches expected → **PASSED**
   - Actual does not match expected → **FAILED**
   - Test steps could not be completed → **FAILED**

2. **Build result summary:**
   - **Detailed PASSED and FAILED templates in guidelines.md Section 1 (moved from SKILL.md)**

3. **Present result to user for confirmation:**
   - "Update JIRA with this result" (Recommended)
   - "Re-run the test"
   - "Cancel — don't update JIRA"

---

### Step 4: Update JIRA Ticket

**Todo:** Mark "Compare results and determine PASS/FAIL" as `completed`, mark "Update JIRA ticket with results" as `in_progress`.

#### If PASSED:

1. **Add comment:**
   ```
   mcp__atlassian__jira_add_comment({
     issue_key: "{TICKET_KEY}",
     body: "Run test *PASSED* by CLAUDE CODE via /common-qa:verify-bug-simple skill.\n\n*Test Steps Executed:*\n{NUMBERED_STEPS}\n\n*Expected:* {EXPECTED_RESULT}\n*Actual:* {ACTUAL_RESULT} -- Matches expected.\n\n[~accountid:{ASSIGNEE_ACCOUNT_ID}]"
   })
   ```

2. **Transition ticket to Done/Closed:**
   - Get available transitions: `mcp__atlassian__jira_get_transitions`
   - Execute transition: `mcp__atlassian__jira_transition_issue`

3. **Report completion.**

#### If FAILED:

1. **Add comment:**
   ```
   mcp__atlassian__jira_add_comment({
     issue_key: "{TICKET_KEY}",
     body: "Run test *FAILED* by CLAUDE CODE via /common-qa:verify-bug-simple skill.\n\n*Test Steps Executed:*\n{NUMBERED_STEPS}\n\n*Failed at:* Step {N} - {STEP_DESCRIPTION}\n*Expected:* {EXPECTED_RESULT}\n*Actual:* {ACTUAL_RESULT}\n\nThe bug appears to still be present.\n\n[~accountid:{ASSIGNEE_ACCOUNT_ID}]"
   })
   ```

2. **Keep ticket open** (do NOT transition).

3. **Report completion.**

4. **Mark "Update JIRA ticket with results" as `completed`.** All todos should now be `completed`.

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, Notes, detailed workflow diagram, parsing examples, action mapping tables, and output templates are in guidelines.md to reduce auto-loaded context size.
