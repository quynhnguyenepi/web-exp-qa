# Sample: Verify Bug Fix — PASSED

---

## Input

User request: "Verify bug https://optimizely-ext.atlassian.net/browse/DHK-4506"

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - Atlassian MCP: Connected
   - Playwright MCP: Connected
   - Ticket: DHK-4506

Proceeding to read ticket...
```

---

## Step 1: Read & Parse JIRA Ticket

Fetched ticket details:

```
Ticket: DHK-4506 - [Web] Experiment page crashes when clicking "Results" tab
Assignee: John Doe (accountId: 5b10ac8d82e05b22cc7d4ef5)
Status: In Review

Parsed Test Steps:
Precondition: User is logged in to app.optimizely.com

1. Navigate to app.optimizely.com/v2/projects/123/experiments
2. Click on experiment "Homepage Hero Test"
3. Click "Results" tab
4. Wait for results page to load

Expected Result:
Results page loads without errors, showing experiment metrics table
```

User selected: "Proceed with test execution"

---

## Step 2: Execute Test Steps via Playwright

```
Step 1/4: Navigate to experiments page
Status: Done
Actual: Page loaded, experiment list visible

Step 2/4: Click on experiment "Homepage Hero Test"
Status: Done
Actual: Experiment detail page opened

Step 3/4: Click "Results" tab
Status: Done
Actual: Results tab clicked, page loading

Step 4/4: Wait for results page to load
Status: Done
Actual: Results page loaded, metrics table visible with 3 variations

[Screenshot captured: results-page-loaded.png]
```

---

## Step 3: Compare & Determine Result

```
Test Result: PASSED

Ticket: DHK-4506 - [Web] Experiment page crashes when clicking "Results" tab
Steps Executed: 4/4
All steps completed successfully.

Expected: Results page loads without errors, showing experiment metrics table
Actual: Results page loaded successfully, metrics table visible with 3 variations -- matches expected

Evidence: [screenshot captured]
```

User selected: "Update JIRA with this result"

---

## Step 4: Update JIRA Ticket

Comment posted to DHK-4506:

```
Run test *PASSED* by CLAUDE CODE via /common-qa:verify-bug-simple skill.

*Test Steps Executed:*
1. Navigate to experiments page -- Done
2. Click on experiment "Homepage Hero Test" -- Done
3. Click "Results" tab -- Done
4. Wait for results page to load -- Done

*Expected:* Results page loads without errors, showing experiment metrics table
*Actual:* Results page loaded successfully, metrics table visible with 3 variations -- Matches expected.

@John Doe
```

Ticket transitioned: In Review → Done

```
JIRA updated successfully!

Ticket: DHK-4506
Comment: Run test PASSED — posted with @John Doe mention
Status: Transitioned to Done

Verification complete.
```
