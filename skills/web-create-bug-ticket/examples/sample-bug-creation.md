# Sample Bug Creation: Test Failures from DHK-4456

This is an example of bug ticket creation produced by the create-bug-ticket skill.

---

## Input

From `/exp-qa-agents:execute-test-case` execution against DHK-4456:

- TC-002: Verify login with invalid credentials — FAILED at Step 3
- TC-005: Verify password reset flow — FAILED at Step 2

---

## Step 1: Gather Failure Details

```
2 test failure(s) to process:

1. TC-002: Verify login with invalid credentials
   Failed at Step 3 | Priority: High

2. TC-005: Verify password reset flow
   Failed at Step 2 | Priority: Normal
```

User selected: "Create bug tickets for all failures"

---

## Step 2: Search Existing Bugs

### TC-002: "login invalid credentials"

```
Found 2 existing bug(s) related to "TC-002: Verify login with invalid credentials":

1. DHK-5001: Login page allows invalid email format (Status: In Progress)
2. DHK-5023: Authentication error not displayed on failed login (Status: Open)
```

User decision: "Skip — existing bug DHK-5023 covers this"

### TC-005: "password reset flow"

No existing bugs found. Proceeding to create new bug.

---

## Step 3: Create Bug Tickets

### Created: DHK-5050

**Title:** [Test Failure] Verify password reset flow

**Description:**
```
h3. Summary
Test case "Verify password reset flow" failed during automated execution.

h3. Steps to Reproduce
1. Navigate to the login page
2. Click "Forgot Password" link — FAILED HERE

h3. Expected Result
Password reset form is displayed with email input field

h3. Actual Result
Page shows 404 error "Page not found"

h3. Environment
- Target URL: https://app.optimizely.com
- Execution Date: 2026-03-03
- Browser: Chromium (Playwright)

h3. Additional Context
- Source Test Case: DHK-4458
- Failed at Step: 2/5
```

Link: DHK-5050 → relates to → DHK-4458

---

## Final Summary

```
Bug ticket creation complete!

Created:
- DHK-5050: [Test Failure] Verify password reset flow
  → Linked to: DHK-4458

Skipped:
- TC-002: Covered by existing DHK-5023

Summary: 1 created, 0 updated, 1 skipped
```
