# Multi-Agents - Test Cases

## TC-001: Parallel analysis of multiple tickets

**Preconditions:** Atlassian MCP is connected. Multiple valid JIRA tickets exist.

**Steps:**
1. Invoke skill with "Analyze CJS-100 and CJS-101"
2. Skill parses two tasks and maps them to analyze-ticket
3. Skill presents task plan with both tasks marked as parallel
4. User confirms the plan
5. Both agents are dispatched in parallel
6. Results are presented as each agent completes

**Expected Results:**
- Both tasks are identified and mapped to `/exp-qa-agents:analyze-ticket`
- Task plan shows both as parallelizable
- Agents run simultaneously (both with `run_in_background: true`)
- Each result is presented for user review upon completion
- Consolidated report includes both analyses

## TC-002: Mixed parallel and sequential tasks

**Preconditions:** Atlassian MCP and Playwright MCP are connected.

**Steps:**
1. Invoke skill with "Analyze CJS-100 and run test case for CJS-101"
2. Skill identifies T1 as analyze-ticket (parallelizable) and T2 as execute-test-case (sequential/browser)
3. Task plan shows T1 as parallel and T2 as sequential
4. User confirms
5. T1 launches in background, T2 runs after T1 or sequentially

**Expected Results:**
- analyze-ticket is dispatched immediately (parallel-safe)
- execute-test-case is queued as sequential (browser-dependent)
- Browser-dependent task does not conflict with API-only tasks
- Both results are reported in the final summary

## TC-003: Task count exceeds limit (>10 tasks)

**Preconditions:** Atlassian MCP is connected.

**Steps:**
1. Invoke skill with 12 ticket IDs to analyze
2. Skill detects more than 10 tasks

**Expected Results:**
- Skill warns user about context limits
- Suggests batching (e.g., "Process first 10, then remaining 2")
- Proceeds only after user confirms the approach

## TC-004: One agent fails while others succeed

**Preconditions:** Atlassian MCP is connected. One ticket ID is invalid.

**Steps:**
1. Invoke skill with "Analyze CJS-100, CJS-INVALID, and CJS-102"
2. T1 and T3 succeed, T2 fails (invalid ticket)
3. Results are presented as agents complete

**Expected Results:**
- T2 failure is reported with the error (ticket not found)
- T1 and T3 results are presented normally
- Consolidated report shows T2 as "failed" with error details
- User is asked whether to retry T2 or skip it

## TC-005: User cancels mid-execution

**Preconditions:** Atlassian MCP is connected. Multiple agents are running.

**Steps:**
1. Invoke skill with 3 tasks
2. All 3 agents are dispatched
3. After T1 completes, user says "skip remaining"
4. T2 and T3 are still running in background

**Expected Results:**
- Running agents are allowed to finish (cannot cancel)
- Results for T2 and T3 are not presented to the user
- Consolidated report shows T1 as approved, T2/T3 as skipped
