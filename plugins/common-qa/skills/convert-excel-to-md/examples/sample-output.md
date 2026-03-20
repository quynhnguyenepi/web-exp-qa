# Example Output - Convert Excel to Markdown

This example shows the expected output format when converting an Excel file with multi-row test cases.

## Input

Excel file: `Feature_Test_Cases.xlsx`, Sheet: `Login Tests`

| Title | Test Step | Expected Result | Priority |
|-------|-----------|-----------------|----------|
| Verify valid login | Pre-con: user exists | | High |
| | Enter valid email | Email field accepts input | |
| | Enter valid password | Password field accepts input | |
| | Click Login | Dashboard loads | |
| Verify invalid login | Pre-con: user exists | | Normal |
| | Enter invalid email | Email field accepts input | |
| | Click Login | Error message displayed | |

## Expected Output

```markdown
# Test Cases - Feature_Test_Cases

**Source:** Feature_Test_Cases.xlsx
**Sheet:** Login Tests
**Total Test Cases:** 2
**Converted:** 2026-03-12

## Summary

| # | Title | Priority | Labels |
|---|-------|----------|--------|
| TC-01 | Verify valid login | High | |
| TC-02 | Verify invalid login | Normal | |

---

### TC-01: Verify valid login

**Priority:** High | **Labels:**

**Pre-condition:**
- User exists

**Test Steps:**
1. Enter valid email
2. Enter valid password
3. Click Login

**Expected Results:**
1. Email field accepts input
2. Password field accepts input
3. Dashboard loads

---

### TC-02: Verify invalid login

**Priority:** Normal | **Labels:**

**Pre-condition:**
- User exists

**Test Steps:**
1. Enter invalid email
2. Click Login

**Expected Results:**
1. Email field accepts input
2. Error message displayed
```
