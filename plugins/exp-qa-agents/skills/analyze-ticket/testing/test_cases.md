# Test Cases for analyze-ticket Skill

## TC-001: Basic Ticket Analysis

**Input:** `Analyze CJS-10873`

**Expected:**
- Fetches ticket details from JIRA
- Identifies parent epic CJS-9699
- Finds related PRs (#374, #382, #387)
- Reads PR diffs and identifies code changes
- Generates prioritized test cases (P0-P3)
- Includes verification methodology

**Pass Criteria:**
- P0 test cases match the ticket's acceptance criteria
- P2 test cases identify changes beyond the AC (global properties refactor)
- Verification method is specific (not vague)

---

## TC-002: Ticket with No PRs

**Input:** `Analyze {TICKET_ID}` where ticket has no linked PRs or commits

**Expected:**
- Fetches ticket details
- Reports no PRs found
- Falls back to git log search
- If still no PRs, generates test cases from AC only
- Warns user that analysis is limited without code context

**Pass Criteria:**
- Graceful handling of missing development info
- Test cases still generated from AC
- Warning message about limited analysis

---

## TC-003: Ticket with Multiple PRs

**Input:** `Analyze {TICKET_ID}` where ticket has 3+ related PRs

**Expected:**
- Finds and analyzes all PRs
- Identifies follow-up PRs
- Consolidates changes across all PRs
- Generates comprehensive test cases covering all changes

**Pass Criteria:**
- All PRs are analyzed (not just the first one)
- Test cases cover changes from follow-up PRs
- Scope assessment reflects cumulative changes

---

## TC-004: Bug Ticket Analysis

**Input:** `Analyze {BUG_TICKET_ID}`

**Expected:**
- Identifies it as a Bug type
- Focuses on regression testing
- Includes the specific fix verification
- Generates edge case tests around the bug area

**Pass Criteria:**
- P0 focuses on verifying the fix
- P3 includes regression checks
- Test cases address the root cause, not just symptoms

---

## TC-005: URL Input

**Input:** `Analyze https://optimizely-ext.atlassian.net/browse/CJS-10873`

**Expected:**
- Extracts ticket ID from URL
- Proceeds with normal analysis flow

**Pass Criteria:**
- Correctly parses `CJS-10873` from the URL
- No errors from URL parsing
