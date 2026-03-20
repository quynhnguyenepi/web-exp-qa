# Test Cases for deploy-preproduction Skill

## TC-001: Successful Full Deployment

**Input:** Run `/exp-qa-agents:deploy-preproduction` with default settings (flags repo, master branch)

**Expected:**
- Navigates to workflow page
- Triggers workflow successfully
- Waits for approval gate
- Approves with comment
- Monitors until deployment completes

**Pass Criteria:**
- All 5 steps completed
- Workflow triggered on master branch
- Approval comment posted
- Final status is "Success"

---

## TC-002: GitHub Login Required

**Input:** Run when Playwright browser is not logged into GitHub

**Expected:**
- Detects login page or missing "Run workflow" button
- Asks user to authenticate
- After user logs in, retries the workflow

**Pass Criteria:**
- Clear message about login requirement
- Navigation to GitHub login page
- Successful retry after authentication

---

## TC-003: Workflow Fails Before Approval

**Input:** Run when the workflow has a failing step before the approval gate

**Expected:**
- Triggers workflow
- Detects failure status before reaching approval
- Reports failure with run URL
- Does not attempt approval

**Pass Criteria:**
- Failure detected accurately
- Screenshot captured of error
- Run URL provided for manual investigation

---

## TC-004: Approval Timeout

**Input:** Run when approval gate takes longer than expected (>5 min)

**Expected:**
- Triggers workflow
- Waits for approval gate
- Reports timeout after max wait
- Provides run URL for manual monitoring

**Pass Criteria:**
- Timeout message with duration
- Run URL for manual access
- No crash or hung state

---

## TC-005: Deployment Times Out

**Input:** Run when deployment takes longer than 10 minutes

**Expected:**
- All steps through approval complete
- Deployment monitoring times out
- Reports timeout with current status

**Pass Criteria:**
- Approval completed successfully
- Timeout reported with run URL
- User can check status manually

---

## TC-006: Custom Branch

**Input:** "Deploy branch feature-new-api to preproduction"

**Expected:**
- Extracts branch name from natural language
- Selects the specified branch in the dropdown
- Proceeds with deployment

**Pass Criteria:**
- Correct branch selected (not master)
- Workflow triggered on the specified branch

---

## TC-007: User Cancels at Confirmation

**Input:** User selects "Cancel" at the pre-flight confirmation

**Expected:**
- No workflow triggered
- Clean exit with message

**Pass Criteria:**
- No browser navigation to GitHub
- No workflow triggered
- Clear cancellation message

---

## TC-008: Playwright MCP Not Available

**Input:** Run when Playwright MCP is not configured

**Expected:**
- Detects MCP unavailability
- Displays setup instructions
- Exits gracefully

**Pass Criteria:**
- Error message with setup instructions
- No browser actions attempted
