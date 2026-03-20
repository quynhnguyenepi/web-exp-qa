---
description: Run multiple test cases as a suite in headless mode using Playwright MCP browser automation. Captures screenshot evidence for the last 2 steps of each test case and at any failure step (cost-optimized). Accepts test cases from JIRA, pasted text, image, or file. Use when executing a full test suite against a live application.
---

## Dependencies

- **MCP Servers:** Atlassian (optional), Playwright (2 isolated instances: `playwrightA`, `playwrightB`)
- **Related Skills:** `/exp-qa-agents:execute-test-case`, `/exp-qa-agents:create-bug-ticket`, `/exp-qa-agents:create-test-cases`

You are a **coordinator agent** for QA test suite execution.
Your role is to gather context, validate test cases, then **delegate the actual browser execution to sub-agents running on Sonnet** via the Agent tool. Test cases are split across **2 parallel agents** with isolated Playwright browser instances for faster execution.

## Workflow Overview

1. **Pre-flight:** Verify Playwright MCP is available
2. **Gather test cases:** Collect all test cases from JIRA, pasted text, image, or file
3. **Ask test environment and credentials:** Collect target URL, login credentials (see Login Configuration below)
4. **Validate expected outcomes:** Ensure every step has a concrete expected outcome
5. **Smart grouping:** Group TCs by shared context/state to minimize redundant steps (login, generation, navigation)
6. **Delegate execution:** Split TCs into 2 agents with isolated Playwright instances and launch in parallel via Agent tool
7. **Consolidate, save & present report:** Merge reports from all agents, save to `{source_name} Result Report.md`
8. **Offer follow-up actions:** Create bug tickets, re-run failed TCs, etc.

## Login Configuration

**CRITICAL:** Read `../execute-test-case/guidelines.md` for full login configuration including default credentials, environment URLs, feature-environment constraints, RC login flow, and OptiID login flow. Both skills share the same login reference.

Before execution, ask the user for test environment details via AskUserQuestion:
- Target URL (default: `https://rc-app.optimizely.com/signin`)
- Username (default: `bdd+test1752566905289@optimizely.com`)
- Password (default available)
- Browser: Chromium (headless, not configurable for suite)

**Rule:** If test steps involve Opal or AI features, use **Production** environment (not RC) with OptiID login (`https://login.optimizely.com`). See `../execute-test-case/guidelines.md` for the complete login flows.

## Step 1: Gather Test Cases

Accept test cases from any of these sources:

**From JIRA ticket(s):**
- Accept one or more JIRA ticket IDs or URLs
- Call `mcp__atlassian__jira_get_issue` directly for each ticket (call multiple in a single message for parallel execution). **Do NOT use Agent** -- each fetch is one MCP call
- Parse test steps from each ticket's summary, description, comments, or linked Test tickets
- If NO test steps found in a ticket: log it and ask user for that ticket's test steps

**From user input:**
- Pasted text (multiple test cases separated by clear delimiters like TC-001, TC-002, etc.)
- Image/screenshot (of test case document)
- File path (to a local file containing test cases, e.g., .md, .txt, .csv)

**From mixed sources:**
- Accept a combination of JIRA tickets + manual input

**After gathering, present the full suite to user:**

```
Test Suite: {N} test cases

TC-001: {title}
  Steps: {count}
  Source: {JIRA key or "manual input"}

TC-002: {title}
  Steps: {count}
  Source: {JIRA key or "manual input"}

...

Total: {N} test cases, {M} total steps
```

Ask user to confirm via AskUserQuestion:
- **"Run all" (Recommended)** -- execute entire suite
- **"Select specific test cases"** -- choose which ones to run
- **"Cancel"**

## Step 2: Validate Expected Outcomes

Before execution, scan ALL steps across ALL test cases:

- For any step where the expected outcome is missing or vague (e.g., "it works", "page loads", "verify"):
  - Collect all unclear steps and present them to user at once
  - Ask user to provide concrete expected outcomes for each
- Every expected outcome MUST be a concrete, verifiable condition (e.g., "Success notification appears", "Row count is 5", "URL contains /dashboard")

## Step 3: Smart Grouping & Parallel Execution

**This is the critical step.** Group test cases by shared context, then launch **2 agents in parallel** — each with its own isolated Playwright browser instance.

### Parallel Execution with Isolated Browser Instances

This skill requires **2 separate Playwright MCP server instances** configured in `.mcp.json`:
- `playwrightA` — used by Agent 1 (tools prefixed `mcp__playwrightA__*`)
- `playwrightB` — used by Agent 2 (tools prefixed `mcp__playwrightB__*`)

Each instance runs its own browser process, so agents can execute **truly in parallel** without interference.

**Pre-flight check:** Verify both `playwrightA` and `playwrightB` MCP servers are available. If only one Playwright instance exists (e.g., `playwright`), fall back to sequential execution with that single instance.

### Agent Count Rules

| Total TCs | Agents | Mode |
|-----------|--------|------|
| 1-3 | 1 | Single agent (use `playwrightA`) |
| 4+ | 2 | Parallel agents (`playwrightA` + `playwrightB`) |

**Max 2 agents.** Never more — each agent needs its own isolated Playwright instance.

### Smart TC Grouping (Context-Based)

**DO NOT distribute TCs in sequential order.** Instead, analyze all TCs and group them by shared context to minimize redundant steps (login, data generation, navigation).

**Grouping principles:**
1. **TCs that need generated data** (e.g., generate ideas, create items) → group together so data is generated once and reused
2. **TCs that share the same UI state** (e.g., same tab, same page, same dialog) → group together to avoid repeated navigation
3. **TCs that are independent/stateless** → use as balancers to even out batch sizes
4. **TCs that produce data needed by other TCs** → place them FIRST in the batch so subsequent TCs reuse the state

**Grouping algorithm:**
1. Analyze each TC's preconditions, required state, and side effects
2. Identify context clusters:
   - **Cluster A:** TCs needing generated/created data (e.g., generate ideas → view details → delete → verify fields)
   - **Cluster B:** TCs operating on existing data (e.g., saved items tab → search → scroll → view dialog)
   - **Cluster C:** TCs testing form/input features (e.g., fill form → upload file → select options)
3. Distribute clusters across 2 agents, balancing by total step count
4. Within each agent's batch, ORDER TCs so that data-producing TCs run first

**Example grouping (Idea Builder P1 test cases):**
```
Agent 1 (playwrightA) — "Generation & Card Interaction"
├── TC-P1-01: Generate via Screenshot        → produces ideas (run FIRST)
├── TC-P1-02: View idea details              → reuses ideas from P1-01
├── TC-P1-05: Delete generated idea          → reuses ideas
├── TC-P1-10: Screenshot empty fields        → reuses screenshot flow
└── TC-P1-07: Additional context generation  → needs fresh generation

Agent 2 (playwrightB) — "Saved Tab & Form Features"
├── TC-P1-06: Tab navigation                 → starts fresh
├── TC-P1-03: View saved idea dialog         → on Saved tab (reuse)
├── TC-P1-04: Search saved ideas             → on Saved tab (reuse)
├── TC-P1-09: Infinite scroll                → on Saved tab (reuse)
└── TC-P1-08: Previous experiments           → back to All tab
```

**Present grouping to user** before execution:
```
Proposed TC Grouping:

Agent 1 (playwrightA): {N} TCs, {M} steps
  {TC_ID}: {title} — {reason for grouping}
  ...

Agent 2 (playwrightB): {N} TCs, {M} steps
  {TC_ID}: {title} — {reason for grouping}
  ...

Estimated time savings: {X} fewer logins, {Y} fewer data generations
```

### How to build each sub-agent prompt

Each agent gets the SAME template but with DIFFERENT test cases and a DIFFERENT Playwright instance. Construct one prompt per agent:

```
You are a QA test execution agent running in headless mode.
You are Agent {X} of {TOTAL_AGENTS}. Execute ONLY the test cases assigned to you.

## Guidelines
Read the file at: {absolute_path_to}/execute-test-case/guidelines.md
for Playwright action mapping, login flows, verification strategies, and error handling patterns.
Also read: {absolute_path_to}/execute-test-suite/guidelines.md
for suite-specific execution rules.

## Test Environment
- Target URL: {url}
- Username: {username}
- Password: {password}
- Login Method: {RC direct | OptiID}
- Browser: Chromium (headless)

## Your Playwright Instance (CRITICAL)
You MUST use ONLY `playwright-{X}` MCP tools. NEVER use tools from the other instance.
- Use `mcp__playwright-{X}__browser_navigate` (NOT `mcp__playwright__browser_navigate`)
- Use `mcp__playwright-{X}__browser_click` (NOT `mcp__playwright__browser_click`)
- Use `mcp__playwright-{X}__browser_snapshot`, `mcp__playwright-{X}__browser_take_screenshot`, etc.
- ALL Playwright tool calls MUST be prefixed with `mcp__playwright-{X}__`

## Your Assigned Test Cases
{Paste ONLY the test cases for THIS agent, with every step and expected result}

## Why These TCs Are Grouped Together
{Explain the grouping rationale so the agent understands state reuse opportunities}
- Example: "TC-P1-01 generates ideas that TC-P1-02 and TC-P1-05 will reuse. Run P1-01 first."

## Browser Isolation (CRITICAL)
- You have your OWN isolated browser instance (`playwright-{X}`).
- Another agent is running in parallel with a DIFFERENT browser — do not worry about interference.
- Start by navigating to the target URL to ensure a clean browser state.
- If you detect a stale session or unexpected page, re-login from scratch.

## Pre-Execution Setup
- Create result folders for YOUR test cases only:
  `mkdir -p "{TC_ID_1} Result/" "{TC_ID_2} Result/" ...`
- Calculate the last 2 step numbers for each test case and record them:
  `{TC_ID_1}: steps 15,16 | {TC_ID_2}: steps 13,14 | ...`

## Screenshot Policy (STRICT — COST CONTROL)

**You MUST follow this policy exactly. Capturing extra screenshots wastes cost.**

- **Steps 1 to N-2 (early steps):** Execute action ONLY. Use `browser_snapshot` ONLY when needed to find element refs for interaction. Do NOT call `browser_take_screenshot`. Do NOT save any .png files.
- **Steps N-1 and N (last 2 steps):** MUST capture `browser_snapshot` + `browser_take_screenshot`.
- **ANY step that FAILS:** IMMEDIATELY capture `browser_snapshot` + `browser_take_screenshot` with `-FAIL` suffix. This is the MOST important screenshot.
- **Login/setup steps:** NEVER capture screenshots during login or navigation to the test starting point. These are setup, not test evidence.

**Screenshot budget per test case:**
- TC PASSES: exactly **2 screenshots** (last 2 steps only)
- TC FAILS at step K (before last 2): exactly **1 screenshot** (the failure step)
- TC FAILS at step K (within last 2): exactly **1-2 screenshots** (failure + any remaining last step)

**After EACH test case, verify your screenshot count:**
```bash
ls "{TC_ID} Result/" | wc -l
```
- If TC PASSED and count > 2: you captured too many. DELETE the extras.
- If TC FAILED and count > 1 (excluding last-2-step screenshots): you captured too many.

**FORBIDDEN — these are the most common mistakes:**
- Capturing screenshots for steps 1 through N-2 (early/middle steps)
- Capturing screenshots during login flow
- Capturing multiple screenshots for the same step (e.g., step-15.png AND step-15-expanded.png)
- Capturing "extra evidence" or "documentation" screenshots beyond the budget

## Execution Rules
1. For EACH test case, for EACH step:
   - Execute the action via Playwright MCP tool
   - For early steps (1 to N-2): ONLY use browser_snapshot when needed for element refs. NO browser_take_screenshot.
   - For the LAST 2 steps ONLY: capture browser_snapshot + browser_take_screenshot
   - Compare actual vs expected -> PASS or FAIL
2. **Screenshot folder structure (MANDATORY):** Save screenshots using the `filename` parameter:
   - `browser_take_screenshot(filename: "{TC_ID} Result/step-{N}.png")`
   - Example: `TC-P0-01 Result/step-15.png`
   - NEVER use arbitrary names. NEVER save to root directory. ALWAYS use folder convention.
3. **On step failure (CRITICAL):** IMMEDIATELY capture `browser_snapshot` + `browser_take_screenshot(filename: "{TC_ID} Result/step-{N}-FAIL.png")` at the failing step. After capturing evidence, STOP current test case, mark remaining steps SKIPPED, move to next TC.
4. Between test cases: navigate back to target URL, wait for page load, take fresh snapshot
5. After each TC, output: TC-{ID}: {PASS|FAIL} ({passed}/{total} steps)
6. Between test cases: check if session is still active. If redirected to login page, re-login.

## MANDATORY Evidence Checkpoint (after EACH test case)
After completing each TC, STOP and run this verification before moving to the next:

1. Count screenshots: `ls "{TC_ID} Result/" | wc -l`
2. Verify against budget:
   - If TC PASSED: MUST have EXACTLY 2 files (`step-{N-1}.png` and `step-{N}.png`). If more than 2, DELETE extras.
   - If TC FAILED at step K: MUST have EXACTLY 1 failure file (`step-{K}-FAIL.png`). If more than 1, DELETE extras.
3. Verify all screenshots are in the correct folder: `{TC_ID} Result/`
4. If screenshots are MISSING: capture them NOW before proceeding.
5. If screenshots EXCEED the budget: DELETE the extras NOW before proceeding.
- CRITICAL: A failed TC without a failure screenshot is UNACCEPTABLE. Do NOT proceed until failure evidence is captured.

## Report Format
After ALL your assigned test cases, generate this report:

### Agent {X} Execution Report

| # | Test Case | Steps | Passed | Failed | Skipped | Result |
|---|-----------|-------|--------|--------|---------|--------|

**Pass Rate:** {X}% ({passed_tc}/{total_tc})

### Detailed Results
(Per test case table with Step | Action | Expected | Actual | Verdict | Screenshot)

### Failed Steps Summary
(All failures in one table)
```

### Launch agents in PARALLEL

Both agents launch simultaneously in a **single message with multiple Agent tool calls**. Each agent uses its own isolated Playwright instance, so there is no browser conflict.

```
# Launch BOTH agents in parallel (single message, multiple tool calls):
Agent(description: "Agent 1/2: Execute {TC_IDs}", model: "sonnet", prompt: <prompt_1>)
Agent(description: "Agent 2/2: Execute {TC_IDs}", model: "sonnet", prompt: <prompt_2>)
# Both agents run simultaneously — wait for both to complete
```

**IMPORTANT:**
- Each sub-agent has access to ALL tools including its assigned Playwright MCP instance.
- Agent 1 uses `mcp__playwrightA__*` tools ONLY. Agent 2 uses `mcp__playwrightB__*` tools ONLY.
- Pass the absolute paths to guidelines files so the sub-agent can read them.
- Include the FULL test case content in the prompt -- do not just pass file paths for test cases.
- Both agents CAN use `run_in_background: true` since they have isolated browser instances. However, using foreground mode is preferred so you get results immediately for the consolidated report.

### Fallback: Sequential Execution (Single Playwright Instance)

If only ONE Playwright MCP instance is configured (e.g., `playwright` without `-1`/`-2` suffix), fall back to sequential execution:
- Launch agents ONE AT A TIME, waiting for each to complete
- All agents use the same `mcp__playwright__*` tools
- **NEVER use `run_in_background: true`** in this mode — agents would share the browser

## Step 4: Consolidate Reports, Save to File, and Follow-Up

After ALL agents complete, merge their individual reports into one consolidated report.

### Report content

```
## Test Suite Execution Report

**Suite:** {title}
**Browser:** Chromium (headless)
**Target URL:** {url}
**Executed:** {timestamp}
**Agents Used:** {N}
**Overall Result:** {PASS|FAIL}

### Suite Summary

| # | Test Case | Agent | Steps | Passed | Failed | Skipped | Result |
|---|-----------|-------|-------|--------|--------|---------|--------|

**Pass Rate:** {X}% ({passed_tc}/{total_tc})
**Total Steps:** {total} ({passed} passed, {failed} failed, {skipped} skipped)

### Detailed Results
(Per test case table with Step | Action | Expected | Actual | Verdict | Screenshot)

### Failed Steps Summary
(All failures across all agents in one table)
```

### Save report to file (MANDATORY)

After consolidating, write the report to a markdown file using the Write tool:

- **File name:** `{test_case_source_name} Result Report.md`
- **Derive source name from where the test cases came from:**
  - From a file (e.g., `DHK-1234 Test Cases.md`) → `DHK-1234 Test Cases Result Report.md`
  - From a JIRA ticket (e.g., `DHK-1234`) → `DHK-1234 Result Report.md`
  - From multiple JIRA tickets (e.g., `DHK-1234`, `DHK-1235`) → `DHK-1234 DHK-1235 Result Report.md`
  - From pasted text with a suite name → `{Suite Name} Result Report.md`
- **Save location:** Current working directory (same level as the screenshot result folders)

### Follow-up actions

Display the report to the user, then offer:
- **"Create bug tickets for failures"** -> Invoke `/exp-qa-agents:create-bug-ticket` with all failure details
- **"Re-run failed test cases"** -> Re-execute only the failed TCs (launch new agents)
- **"Re-run specific test case"** -> Ask which one to re-run (switches to `/exp-qa-agents:execute-test-case` for interactive mode)
- **"Done"** -> End session


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
