# Test Cases for execute-test-case Skill

## Overview

This document describes the test scenarios for validating the `execute-test-case` skill, which runs test cases via Playwright MCP and optionally creates JIRA bug tickets for failures.

---

## Test Categories

### Category 1: Input Handling

Tests that the skill correctly handles various input formats.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | JIRA ticket ID input | `Run test cases for DHK-4456` | Extracts `DHK-4456`, fetches ticket from JIRA |
| TC-002 | JIRA URL input | `Run test cases from https://optimizely-ext.atlassian.net/browse/QAK-1234` | Extracts `QAK-1234` from URL, fetches ticket |
| TC-003 | Direct content input | `Run this test case: [content with steps]` | Parses steps and expected results from content |
| TC-004 | No input provided | `Run test cases` | Asks user for JIRA ticket ID or content via AskUserQuestion |
| TC-005 | Invalid ticket ID | `Run test cases for INVALID-999999` | Reports ticket not found, asks user to verify |

### Category 2: Pre-Flight Checks

Tests that the skill verifies MCP connectivity before proceeding.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Playwright MCP disabled | Any input with Playwright MCP disabled | Shows error with enable instructions, exits gracefully |
| TC-007 | Atlassian MCP disabled (JIRA input) | JIRA ticket with Atlassian MCP disabled | Shows error with enable instructions, exits gracefully |
| TC-008 | Atlassian MCP disabled (direct content) | Direct content with Atlassian MCP disabled | Warns but proceeds (JIRA only needed for bug creation later) |
| TC-009 | Both MCPs enabled | Any input with both MCPs enabled | Reports pre-flight checks passed, proceeds |

### Category 3: Test Case Gathering

Tests that the skill correctly fetches and parses test cases.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-010 | Test type ticket | JIRA ticket with type "Test" | Extracts steps from ticket description directly |
| TC-011 | Story with linked tests | Story ticket with linked Test tickets | Finds and fetches linked Test tickets |
| TC-012 | Ticket with no test cases | Story ticket with no linked tests and no steps | Reports no test cases found, offers alternatives |
| TC-013 | Multiple test cases | Ticket with 5 linked Test tickets | Parses all 5, presents count to user |
| TC-014 | Markdown table format | Direct content in markdown table | Correctly parses table rows into test cases |

### Category 4: Test Execution

Tests that the skill correctly executes test steps via Playwright MCP.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-015 | All steps pass | Test case with verifiable steps | All steps marked PASSED, test case PASSED |
| TC-016 | Step fails at middle | Test case where step 3/5 fails | Steps 1-2 PASSED, step 3 FAILED, stops execution for this case |
| TC-017 | First step fails | Test case where step 1 fails | Step 1 FAILED, screenshot taken, moves to next test case |
| TC-018 | Browser error recovery | Playwright error during execution | Records error, attempts recovery, reports which tests couldn't run |
| TC-019 | Clean state between tests | Multiple test cases | Navigates back to target URL between test cases |

### Category 5: Test Report Generation

Tests that the skill generates correct reports.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-020 | All passed report | All tests pass | Shows 100% pass rate, no failures section |
| TC-021 | Mixed results report | 2 passed, 1 failed | Shows pass rate, detailed failure info, screenshots |
| TC-022 | All failed report | All tests fail | Shows 0% pass rate, all failure details |

### Category 6: Failure Handling & Bug Creation

Tests the bug ticket creation workflow.

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-023 | Create bugs for all failures | User selects "Create bug tickets for all failures" | Creates bug for each failed case |
| TC-024 | Select specific failures | User selects specific failures for bug creation | Creates bugs only for selected cases |
| TC-025 | Skip bug creation | User selects "Skip bug creation" | Skips Steps 5-6, exits gracefully |
| TC-026 | Existing bug found - skip | Related bug found, user skips | No new bug created |
| TC-027 | Existing bug found - create new | Related bug found, user creates new anyway | New bug created despite existing one |
| TC-028 | Existing bug found - add comment | Related bug found, user adds comment | Comment added to existing bug |
| TC-029 | Bug creation error | JIRA create_issue fails | Reports error, continues with remaining, suggests retry |
| TC-030 | No existing bugs found | No related bugs in search results | Proceeds to create new bug without asking |

---

## Test Execution Instructions

### Running Evaluations

Use the evaluation-runner skill to execute the test suite:

```
/evaluation-runner execute-test-case
```

### Manual Testing

1. Enable both Playwright and Atlassian MCPs in `.claude/settings.local.json`
2. Have a JIRA ticket with linked Test tickets ready
3. Invoke the skill: `/execute-test-case DHK-4456`
4. Follow the workflow and verify each step produces expected output

---

## Success Criteria

- [ ] Pre-flight checks verify both MCP servers before starting
- [ ] Accepts JIRA ticket IDs, URLs, and direct content as input
- [ ] Correctly parses test cases from JIRA and direct content
- [ ] Executes test steps via Playwright MCP browser actions
- [ ] Takes screenshots on failure
- [ ] Generates clear test execution report with pass/fail results
- [ ] Asks user before creating bug tickets (never auto-creates)
- [ ] Searches JIRA for existing related bugs before creating new ones
- [ ] Creates properly formatted bug tickets with failure details
- [ ] Links new bugs to original test case tickets
- [ ] Handles errors gracefully at every step
- [ ] TodoWrite progress tracking works throughout execution

---

## Known Limitations

- Playwright MCP runs in Chromium only — no cross-browser testing
- Screenshots are captured as visual references but not uploaded to JIRA
- Complex authentication flows may need manual login steps in test cases
- Dynamic SPAs may require explicit wait steps for reliable execution
- File upload steps require files to exist on the local filesystem
