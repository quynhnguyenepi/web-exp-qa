# Test Cases for fix-daily-run-playwright-ts Skill

## TC-001: Fix Timeout Errors from CI Run

**Input:** Run `/exp-qa-agents:fix-daily-run-playwright-ts` with a GitHub Actions run URL containing 3 timeout failures in page object methods.

**Expected:**
- Fetches CI logs and identifies all 3 failures
- Categorizes them as test code issues
- Identifies shared root cause in page object
- Applies fix to the page object (single fix resolves all 3)
- Runs tests locally and confirms they pass

**Pass Criteria:**
- All 3 tests pass after fix
- Only the page object file is modified
- Comparison table shows before/after status

---

## TC-002: Mixed Test Code and App Failures

**Input:** Run with a CI run that has 5 failures: 3 are test code issues, 2 are application bugs.

**Expected:**
- Categorizes failures correctly (test code vs app issue)
- Applies fixes only for test code issues
- Reports app issues without modifying test code
- Local run shows 3 fixed, 2 still failing (app issues)

**Pass Criteria:**
- Test code failures are fixed
- App failures are clearly reported as product bugs
- No test assertions modified to force passing

---

## TC-003: beforeAll Hook Failure Cascade

**Input:** Run with a CI run where a `beforeAll` hook fails, causing 4 downstream tests to show `(0ms)`.

**Expected:**
- Identifies beforeAll as the root cause
- Fixes the hook, not the individual tests
- All 4 downstream tests pass after hook fix

**Pass Criteria:**
- Only the beforeAll hook is modified
- Downstream tests are not individually changed
- Report correctly attributes cascade to the hook

---

## TC-004: No Failures Found

**Input:** Run with a GitHub Actions run ID where all tests passed.

**Expected:**
- Fetches CI logs
- Reports that all tests passed
- Does not attempt any fixes

**Pass Criteria:**
- Clear message: "All tests passed, no failures to fix"
- No files modified

---

## TC-005: Fix Introduces New Failure

**Input:** Run where the applied fix causes a previously passing test to fail during local verification.

**Expected:**
- Detects the new failure in local run results
- Reverts the problematic change
- Tries an alternative fix approach
- Reports the regression and resolution

**Pass Criteria:**
- New failure is detected and reported
- Problematic fix is reverted
- Alternative approach attempted or escalated to user
