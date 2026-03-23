# Test Cases for create-bug-ticket Skill

## TC-001: Basic Bug Creation from Test Failures

**Input:** Run `/exp-qa-agents:create-bug-ticket` with 2 test failures in context from `/exp-qa-agents:execute-test-case`

**Expected:**
- Parses failure details from context
- Searches JIRA for existing related bugs
- Creates bug tickets with proper description format
- Links bugs to source test case tickets
- Adds identification comment to each created ticket

**Pass Criteria:**
- Bug title follows `[Test Failure] {title}` format
- Description includes all required sections (Summary, Steps, Expected, Actual, Environment)
- Bug is linked to source test case ticket
- Identification comment is added

---

## TC-002: Duplicate Detection — Existing Bug Found

**Input:** Run with a failure that matches an existing open bug in JIRA

**Expected:**
- Searches JIRA and finds related bugs
- Presents existing bugs to user
- User chooses to skip or comment on existing bug
- Does NOT create a duplicate

**Pass Criteria:**
- Related bugs are found and presented
- User decision is respected (skip/comment/create anyway)
- No duplicate bugs created when user skips

---

## TC-003: Duplicate Detection — No Existing Bugs

**Input:** Run with a failure that has no matching bugs in JIRA

**Expected:**
- Searches JIRA, finds no related bugs
- Proceeds to create new bug without asking
- Bug is created with all required fields

**Pass Criteria:**
- Search is performed (not skipped)
- Bug is created automatically when no duplicates found

---

## TC-004: Manual Input (No Context from execute-test-case)

**Input:** Invoke standalone with manually described failure

**Expected:**
- Asks user for failure details
- Parses into structured format
- Asks for JIRA project key
- Proceeds with normal creation flow

**Pass Criteria:**
- Handles free-form text input
- Asks for missing required fields (project key, priority)
- Creates bug with same quality as automated path

---

## TC-005: Comment on Existing Bug

**Input:** User chooses "Add comment to existing bug" for a failure with related bugs

**Expected:**
- Adds formatted comment to the existing bug
- Comment includes failure details (test case, step, expected, actual)
- Does not create a new bug

**Pass Criteria:**
- Comment is added to the correct existing bug
- Comment follows the defined format
- No new bug ticket created

---

## TC-006: Atlassian MCP Not Available

**Input:** Invoke when Atlassian MCP is not configured

**Expected:**
- Detects MCP is unavailable
- Displays setup instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message with setup instructions
- No partial state or dangling operations
