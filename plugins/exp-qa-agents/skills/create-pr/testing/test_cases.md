# Test Cases for create-pr Skill

## TC-001: Full Flow — Commit, PR, and JIRA Update

**Input:** Run `/exp-qa-agents:create-pr` with generated test scripts in context from `/exp-qa-agents:create-test-scripts-cypress-js`

**Expected:**
- Stages only relevant files (spec files, page objects)
- Commits with `[TICKET_ID]` prefix and Co-Authored-By
- Pushes branch to remote
- Creates PR with structured body
- Transitions JIRA task to "In Review"
- Closes linked test case tickets with "AutomationDone" label
- Adds identification comment to JIRA task

**Pass Criteria:**
- Commit message follows format
- PR body includes all required sections
- JIRA transitions succeed
- Identification comment added

---

## TC-002: PR Only — Skip JIRA Updates

**Input:** Run and user selects "Skip JIRA updates"

**Expected:**
- Commits and pushes successfully
- Creates PR with structured body
- Skips all JIRA operations
- Reports PR URL

**Pass Criteria:**
- PR is created without JIRA operations
- No errors from skipped JIRA steps
- Step 3 marked as "Skipped — user declined"

---

## TC-003: No Changes to Commit

**Input:** Run when working tree is clean (no staged or unstaged changes)

**Expected:**
- Detects no changes
- Asks user what to stage or exits
- Does NOT create an empty commit

**Pass Criteria:**
- No empty commit created
- Clear message about missing changes

---

## TC-004: GitHub CLI Not Authenticated

**Input:** Run when `gh auth status` fails

**Expected:**
- Detects gh is not authenticated
- Displays `gh auth login` instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message
- No partial operations performed

---

## TC-005: JIRA Transition Not Available

**Input:** Run when the JIRA workflow has no "In Review" transition

**Expected:**
- Lists available transitions
- Skips the transition gracefully
- Continues with remaining JIRA operations (comment, labels)

**Pass Criteria:**
- Reports which transitions were available
- Does not fail on missing transition
- Other JIRA operations still succeed

---

## TC-006: Standalone Invocation (No generate-test-scripts Context)

**Input:** Invoke standalone with a JIRA ticket ID and files to commit

**Expected:**
- Asks for ticket ID and files
- Proceeds with commit, PR, and JIRA flow
- Handles missing context gracefully

**Pass Criteria:**
- Collects all required info from user
- Same quality output as context-based invocation
