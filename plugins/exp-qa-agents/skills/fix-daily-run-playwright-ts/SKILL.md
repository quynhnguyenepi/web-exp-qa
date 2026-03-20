---
description: Analyze failed GitHub Actions daily run for Playwright TypeScript E2E tests, identify root causes from CI logs, fix test code, run tests locally to verify, and report results. Use when a daily CI run has failures that need investigation and fixing.
---

## Dependencies

- **MCP Servers:** GitHub (for fetching CI run logs)
- **Related Skills:** `/common-qa:create-branch`, `/exp-qa-agents:create-pr`

You are a CI failure diagnosis and fix agent.
Domain: playwright-e2e-testing
Mode: sequential
Tools: Read, Write, Edit, TodoWrite, AskUserQuestion, Agent, Bash, Glob, Grep

Analyze a failed GitHub Actions daily run, diagnose test failures from CI logs, apply fixes to test code and page objects, run tests locally to verify, and report results.

## When to Use

Invoke this skill when you need to:

- Fix failures from a daily CI run (GitHub Actions)
- Investigate flaky Playwright tests
- Diagnose and fix timeout errors in E2E tests
- User provides a GitHub Actions run URL or run ID

## Workflow Overview

```
Fetch CI Logs -> Categorize Failures -> Identify Root Causes -> Apply Fixes -> Run Tests -> Report
```

## Execution Workflow

### Step 0: Parse Input and Fetch CI Logs

1. **Accept input** in any of these formats:
   - GitHub Actions URL: `https://github.com/{org}/{repo}/actions/runs/{run_id}`
   - Run ID: `22729053437`

2. **Extract run ID** from the input.

3. **Fetch failed test logs** using GitHub CLI:
   ```bash
   gh run view {RUN_ID} --log-failed 2>&1 | tail -100
   ```

4. **Get test summary** (passed/failed counts):
   ```bash
   gh run view {RUN_ID} --log 2>&1 | grep -E "Tests:|Failed:|Passed:|✘|✓|passed|failed"
   ```

5. **Extract error details** for each failing test:
   ```bash
   gh run view {RUN_ID} --log 2>&1 | grep -E "(✘|Error:|TimeoutError|locator|waiting for|Received|Expected)" | head -60
   ```

### Step 1: Categorize Failures and Identify Root Causes

1. **Group failures by error type:**
   - **TimeoutError on locator click** — element found but not stable/enabled/visible
   - **TimeoutError on expect** — element not found within timeout
   - **beforeAll hook failure** — setup code fails, causing test to show `(0ms)`
   - **afterAll hook failure** — cleanup code fails, doesn't affect test pass/fail but cascades

2. **Identify shared root causes:**
   - Multiple tests failing with the same locator/method = shared page object issue
   - Tests failing at `(0ms)` = `beforeAll` failure
   - Cascading failures from `afterAll` cleanup methods
   - Same page object method failing across specs = UI/selector changed

3. **Present failure analysis table to user:**
   ```
   | # | Test File | Error | Root Cause |
   |---|-----------|-------|------------|
   ```

4. **Classify each failure:**
   - **Selector/UI change** — element renamed, moved, or interaction pattern changed (most common)
   - **Missing await** — Playwright action not awaited, causing race conditions
   - **Timeout too short** — especially for AI-powered features (Opal, brainstorm, generate copy)
   - **Test code issue** — fixable by modifying test/page object code
   - **Application issue** — product bug or environment problem (not fixable in test code)
   - **Flaky/timing issue** — needs retry logic or better waits
   - **Obsolete test step** — verifies UI element/state that no longer exists

### Step 2: Apply Fixes

For each identified test code issue, apply appropriate fixes.

#### Fix Patterns and Diagnostics

Read `guidelines.md` for:
- 18 common fix patterns (timeout, missing await, selector changes, retry logic, silent try/catch, UI copy changes, etc.)
- Fix application rules (read before changing, fix in page objects first, minimize changes, verify syntax)
- Diagnostic checklist (12-point inspection per failure)
- Anti-patterns to avoid

**Key principles:**
- Fix in page objects first — a single page object fix often resolves multiple test failures
- Minimize changes — only fix what's broken, don't refactor unrelated code
- Preserve existing patterns — match the codebase style (naming, structure, timeouts)
- Inspect the live app when selectors fail — use Playwright MCP or Chrome DevTools to verify current DOM
- Check for missing `await` — a common silent bug that causes intermittent failures
- Remove obsolete steps rather than fixing assertions for UI elements that no longer exist
- Increase timeouts for AI features — Opal Chat, brainstorm, generate copy are inherently slow (use 120-240s)

### Step 3: Run Tests Locally to Verify

1. **Run all tests** (or the previously failing subset):
   ```bash
   npx playwright test e2e/ui --workers=1 --headed 2>&1
   ```
   - This is a long-running command — run in background and monitor progress
   - Tests may take 30+ minutes with `slowMo` and sequential execution

2. **Monitor progress periodically:**
   ```bash
   tail -50 {output_file}
   ```

3. **Wait for completion** and collect final results.

### Step 4: Report Results

1. **Present comparison table:**
   ```
   | Test | CI (Before) | Local (After) | Status |
   |------|-------------|---------------|--------|
   ```

2. **Categorize remaining failures:**
   - **Fixed** — previously failing, now passing
   - **Still failing (app issue)** — product/environment bug, not test code
   - **Still failing (needs more investigation)** — may need deeper debugging
   - **New failure** — regression introduced by the fix (must be addressed)

3. **List all changed files** with a summary of what was changed and why:
   ```bash
   git diff --stat
   ```

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
