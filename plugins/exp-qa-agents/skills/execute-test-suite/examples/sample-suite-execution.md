# Sample: Test Suite Execution

## User Request

> Run test suite for CJS-175 on https://app.optimizely.com

## Execution

### Step 1: Gather Test Cases

Found 3 test cases linked to CJS-175:

```
Test Suite: 3 test cases

TC-001: Create experiment with single metric
  Steps: 5
  Source: CJS-175-TC-1

TC-002: Edit experiment name
  Steps: 4
  Source: CJS-175-TC-2

TC-003: Delete experiment with running status
  Steps: 6
  Source: CJS-175-TC-3

Total: 3 test cases, 15 total steps
```

User selected: "Run all"

### Step 2: Validate Expected Outcomes

All steps have concrete expected outcomes. No clarifications needed.

### Step 3: Configure Headless Mode

- Browser: Chromium (headless)
- Target URL: https://app.optimizely.com

### Step 4: Execute Suite

```
--- Test Case 1/3: Create experiment with single metric ---
Steps: 5
Starting...
```

| Step | Action | Expected | Actual | Verdict |
|------|--------|----------|--------|---------|
| 1 | Navigate to experiments list | Experiments page loads | Page loaded | PASS |
| 2 | Click "Create Experiment" | Create dialog opens | Dialog opened | PASS |
| 3 | Enter experiment name "Test Alpha" | Name field populated | Field populated | PASS |
| 4 | Select metric "Click Rate" | Metric appears in selected list | Metric selected | PASS |
| 5 | Click "Save" | Success notification appears | Notification shown | PASS |

```
TC-001: PASS (5/5 steps)
```

```
--- Test Case 2/3: Edit experiment name ---
Steps: 4
Starting...
```

| Step | Action | Expected | Actual | Verdict |
|------|--------|----------|--------|---------|
| 1 | Navigate to experiment "Test Alpha" | Experiment detail page loads | Page loaded | PASS |
| 2 | Click experiment name to edit | Name becomes editable | Name editable | PASS |
| 3 | Change name to "Test Beta" | Name field shows "Test Beta" | Field updated | PASS |
| 4 | Click "Save" | Name updated, notification appears | Notification shown | PASS |

```
TC-002: PASS (4/4 steps)
```

```
--- Test Case 3/3: Delete experiment with running status ---
Steps: 6
Starting...
```

| Step | Action | Expected | Actual | Verdict |
|------|--------|----------|--------|---------|
| 1 | Navigate to experiments list | Experiments page loads | Page loaded | PASS |
| 2 | Click on running experiment | Experiment detail page loads | Page loaded | PASS |
| 3 | Click "Delete" button | Confirmation dialog appears | Dialog appeared | PASS |
| 4 | Verify warning about running status | Warning text visible | Warning NOT visible | FAIL |
| 5 | Click "Confirm Delete" | Experiment deleted | Experiment deleted | PASS |
| 6 | Verify experiment removed from list | Experiment not in list | Not in list | PASS |

```
TC-003: FAIL (5/6 steps)
```

### Step 5: Suite Report

```
## Test Suite Execution Report

**Suite:** CJS-175
**Browser:** Chromium (headless)
**Target URL:** https://app.optimizely.com
**Overall Result:** FAIL

### Suite Summary

| # | Test Case | Steps | Passed | Failed | Skipped | Result |
|---|-----------|-------|--------|--------|---------|--------|
| 1 | Create experiment with single metric | 5 | 5 | 0 | 0 | PASS |
| 2 | Edit experiment name | 4 | 4 | 0 | 0 | PASS |
| 3 | Delete experiment with running status | 6 | 5 | 1 | 0 | FAIL |

**Pass Rate:** 67% (2/3 test cases passed)
**Total Steps:** 15 (14 passed, 1 failed, 0 skipped)

### Failed Steps Summary

| Test Case | Step | Action | Expected | Actual |
|-----------|------|--------|----------|--------|
| TC-003 | 4 | Verify warning about running status | Warning text visible | Warning NOT visible |
```

### Actions Offered

- "Create bug tickets for failures" -> file bug for TC-003 step 4 failure
- "Re-run failed test cases" -> re-execute TC-003 only
- "Re-run specific test case" -> interactive mode via execute-test-case
- "Done"
