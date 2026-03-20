# QA Pipeline - Test Cases

## TC-001: Full pipeline execution in Mode A (Manual)

**Preconditions:** Atlassian and Playwright MCP are connected. Valid JIRA ticket exists with acceptance criteria.

**Steps:**
1. Invoke skill with a JIRA ticket ID and select Mode A
2. Stage 1 (Analyze) completes and presents summary at gate
3. User approves, Stage 2 (Generate TC) runs
4. User approves, Stage 3 (Review TC) runs
5. User approves, Stage 4 (Execute) runs full test suite
6. Stage 5 (File Bugs) runs for any failures
7. Pipeline summary is presented

**Expected Results:**
- Each stage passes its output as context to the next stage
- User is prompted at every gate between stages
- Test cases are generated based on the analysis (not re-analyzed)
- Execution captures screenshots and snapshots per step
- Bug tickets are created only for failed test cases
- Final summary includes all stages, pass rate, and bug ticket links

## TC-002: Pipeline execution in Mode B (Automated)

**Preconditions:** Atlassian and GitHub MCP are connected. Valid JIRA ticket exists.

**Steps:**
1. Invoke skill with a JIRA ticket ID and select Mode B
2. Stage 1 (Analyze) completes
3. Stage 2 (Generate TC) completes
4. Stage 3 (Review TC) is skipped
5. Stage 4 (Generate Scripts) runs, then Create PR
6. Stage 5 (Review PR) runs

**Expected Results:**
- Stage 3 (Review TC) is skipped in Mode B
- Cypress scripts are generated from the test cases
- PR is created with the generated scripts
- PR review is performed and findings presented
- No browser execution or bug filing occurs

## TC-003: User aborts pipeline at a gate

**Preconditions:** Atlassian MCP is connected.

**Steps:**
1. Invoke skill with a JIRA ticket ID, Mode A
2. Stage 1 (Analyze) completes
3. User approves, Stage 2 (Generate TC) completes
4. At the Stage 2 gate, user selects "abort"

**Expected Results:**
- Pipeline stops immediately after abort
- Partial summary is presented covering completed stages (1 and 2)
- No further stages are attempted
- Analysis and test case outputs are preserved in the summary

## TC-004: Stage failure with retry

**Preconditions:** Atlassian MCP is connected. Playwright MCP has intermittent connectivity.

**Steps:**
1. Invoke skill with a JIRA ticket ID, Mode A
2. Stages 1-3 complete successfully
3. Stage 4 (Execute) fails due to browser crash
4. User selects "re-run" at the gate

**Expected Results:**
- Failure is reported with the error details
- User is offered retry option for the specific failed stage
- Previous stages are NOT re-run on retry
- Successful stage outputs are preserved
- Retried stage receives the same context as the original attempt

## TC-005: Mode C parallel execution (manual + automated)

**Preconditions:** Atlassian, Playwright, and GitHub MCP are connected.

**Steps:**
1. Invoke skill with a JIRA ticket ID, Mode C
2. Stages 1-3 complete sequentially
3. Stage 4 launches execute-test-suite AND generate-test-scripts in parallel
4. Both complete, results are presented
5. Bug filing and PR creation proceed

**Expected Results:**
- Manual execution and script generation run simultaneously
- Results from both parallel tasks are collected
- Bug tickets are created for manual test failures
- PR is created with generated scripts
- PR review runs after PR creation
- Final summary includes both manual and automated results
