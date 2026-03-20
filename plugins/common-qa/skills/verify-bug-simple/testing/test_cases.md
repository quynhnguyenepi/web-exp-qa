# Test Cases for verify-bug-simple Skill

## TC-001: Bug Fix Verified — PASSED

**Input:** Run `/common-qa:verify-bug-simple` with a JIRA bug ticket where the fix works correctly

**Expected:**
- Reads ticket and parses test steps from description
- Executes all steps via Playwright
- Actual result matches expected result
- Posts "Run test PASSED" comment with assignee mention
- Transitions ticket to Done/Closed

**Pass Criteria:**
- Comment posted with PASSED status
- Assignee mentioned in comment
- Ticket transitioned to Done/Closed
- Screenshots captured as evidence

---

## TC-002: Bug Still Present — FAILED

**Input:** Run with a bug ticket where the fix is NOT working

**Expected:**
- Reads ticket and parses test steps
- Executes steps, actual result does NOT match expected
- Posts "Run test FAILED" comment with assignee mention
- Ticket remains open (NOT transitioned)

**Pass Criteria:**
- Comment posted with FAILED status
- Failed step identified in comment
- Assignee mentioned
- Ticket NOT closed

---

## TC-003: JIRA URL Input

**Input:** Provide full URL: `https://optimizely-ext.atlassian.net/browse/DHK-4506`

**Expected:**
- Extracts ticket key `DHK-4506` from URL
- Proceeds with normal flow

**Pass Criteria:**
- Ticket key correctly extracted
- Ticket fetched successfully

---

## TC-004: Ticket With No Description

**Input:** Run with a ticket that has empty description

**Expected:**
- Detects no description
- Asks user to provide test steps manually
- Proceeds with user-provided steps

**Pass Criteria:**
- User prompted for test steps
- Skill continues with manual input
- No crash or empty execution

---

## TC-005: Test Steps Cannot Be Parsed

**Input:** Run with a ticket whose description is free-form text (no structured steps)

**Expected:**
- Shows raw description to user
- Asks user to identify the test steps
- Proceeds with user-identified steps

**Pass Criteria:**
- Raw description displayed
- User can provide structured steps
- Skill continues normally

---

## TC-006: Login Required During Test

**Input:** Run test steps that navigate to a page requiring authentication

**Expected:**
- Detects login page
- Asks user for credentials or to pre-login
- Does not proceed without authentication

**Pass Criteria:**
- Login requirement detected
- User prompted for action
- No false FAIL result due to auth issues

---

## TC-007: Element Not Found During Execution

**Input:** Run test where a step references an element that doesn't exist on the page

**Expected:**
- Takes screenshot of current state
- Logs the error for that step
- Marks test as FAILED
- Reports which step failed and why

**Pass Criteria:**
- Screenshot captured at failure point
- Specific step and element identified
- FAILED comment includes details

---

## TC-008: No Done/Closed Transition Available

**Input:** Run PASSED test on a ticket with no Done transition (e.g., already in a terminal state workflow)

**Expected:**
- Posts PASSED comment successfully
- Warns user that transition is not available
- Does not crash

**Pass Criteria:**
- Comment posted correctly
- Clear warning about missing transition
- Skill completes without error

---

## TC-009: Ticket Has No Assignee

**Input:** Run on a ticket with no assignee set

**Expected:**
- Posts comment without user mention
- Warns user that assignee is not set
- Still marks PASSED/FAILED correctly

**Pass Criteria:**
- Comment posted (without mention)
- Warning about missing assignee
- Test result still accurate

---

## TC-010: User Cancels Before JIRA Update

**Input:** User selects "Cancel — don't update JIRA" after seeing results

**Expected:**
- No comment posted to JIRA
- No ticket transition
- Clean exit with message

**Pass Criteria:**
- Zero JIRA API update calls
- Clear cancellation message
- Test results still displayed to user

---

## TC-011: User Requests Re-Run

**Input:** User selects "Re-run the test" after seeing results

**Expected:**
- All test steps executed again from scratch
- New results captured
- New result summary presented

**Pass Criteria:**
- Fresh execution (not cached results)
- New screenshots captured
- Updated result summary

---

## TC-012: Atlassian MCP Not Available

**Input:** Invoke when Atlassian MCP is not configured

**Expected:**
- Detects MCP is unavailable
- Displays setup instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message with setup instructions
- No partial state

---

## TC-013: Playwright MCP Not Available

**Input:** Invoke when Playwright MCP is not configured

**Expected:**
- Detects MCP is unavailable
- Displays setup instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message with setup instructions
- No partial state
