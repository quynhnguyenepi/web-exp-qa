# Run Test Suite - Test Cases

## TC-001: Execute full suite from JIRA test cases

**Preconditions:** Playwright MCP is connected. Atlassian MCP is connected. JIRA ticket has 3 linked test cases with clear steps and expected results.

**Steps:**
1. Invoke skill with a JIRA ticket ID and target URL
2. Skill fetches test cases from JIRA
3. Skill presents suite summary and user selects "Run all"
4. All expected outcomes are validated
5. Suite executes in headless mode
6. Screenshot and snapshot captured after every step
7. Suite report is generated

**Expected Results:**
- All 3 test cases are executed sequentially
- Each step has a screenshot and snapshot captured
- Brief progress update after each TC: `TC-{N}: {PASS|FAIL}`
- Suite report includes per-TC breakdown, pass rate, and failed steps summary
- Follow-up actions are offered (bug tickets, re-run, done)

## TC-002: Suite execution with step failure and continuation

**Preconditions:** Playwright MCP is connected. Test case 2 of 3 has a step that will fail.

**Steps:**
1. Invoke skill with 3 test cases where TC-002 step 3 will fail
2. TC-001 executes and passes
3. TC-002 step 3 fails
4. TC-002 continues to step 4 and beyond
5. TC-003 executes normally

**Expected Results:**
- TC-002 failure does NOT stop the suite
- Remaining steps in TC-002 continue executing (unless dependent on failed step)
- TC-003 starts after TC-002 completes
- Browser state is reset between TC-002 and TC-003
- Final report shows TC-002 as FAIL, others as their actual results
- Failed steps summary includes TC-002 step 3

## TC-003: Suite with vague expected outcomes requiring clarification

**Preconditions:** Playwright MCP is connected. Test cases have some vague expected results.

**Steps:**
1. Invoke skill with test cases where 2 steps have vague outcomes ("it works", "page loads")
2. Skill detects the vague outcomes during validation
3. All unclear outcomes are presented to user at once
4. User provides concrete outcomes
5. Suite executes with updated outcomes

**Expected Results:**
- Execution does NOT start until all outcomes are clarified
- Vague outcomes are collected and presented in a single prompt (not one by one)
- After user provides concrete outcomes, execution proceeds normally
- Updated outcomes are used for pass/fail determination

## TC-004: Suite from pasted text (no JIRA)

**Preconditions:** Playwright MCP is connected. No Atlassian MCP required.

**Steps:**
1. Invoke skill without a JIRA ticket
2. User pastes 2 test cases as text
3. Skill parses test cases from the pasted text
4. Suite executes normally

**Expected Results:**
- Test cases are parsed from any reasonable text format
- Source is listed as "manual input" in the suite summary
- Execution and reporting proceed identically to JIRA-sourced test cases

## TC-005: Browser crash recovery mid-suite

**Preconditions:** Playwright MCP is connected. Browser will crash during TC-002.

**Steps:**
1. Invoke skill with 3 test cases
2. TC-001 passes
3. Browser crashes during TC-002
4. Skill detects the crash

**Expected Results:**
- Browser is restarted automatically
- TC-002 is marked as FAIL with crash error
- Execution resumes from TC-003
- Final report includes TC-002 as failed with crash reason
- TC-001 results are preserved
