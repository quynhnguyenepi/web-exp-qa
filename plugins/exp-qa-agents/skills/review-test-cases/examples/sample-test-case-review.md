# Sample: Test Case Review

## User Request

> Review test cases for CJS-150

## Execution

### Step 1: Gather Test Cases

Found 4 test cases linked to CJS-150:

```
Found 4 test cases from JIRA

TC-001: Create new audience (source: CJS-150-TC-1)
TC-002: Edit audience name (source: CJS-150-TC-2)
TC-003: Delete audience (source: CJS-150-TC-3)
TC-004: Duplicate audience (source: CJS-150-TC-4)
```

### Step 2: Gather Requirements Context (Parallel)

- Agent 1: JIRA context -- 3 acceptance criteria found
  - AC-1: User can create a new audience with name, description, and conditions
  - AC-2: User can edit and delete existing audiences
  - AC-3: Error shown when audience name is duplicate
- Agent 2: Confluence -- No linked pages
- Agent 3: Attachments -- 1 Figma design showing audience list and create dialog

### Step 3: Quality Review

| Score | Count | Test Cases |
|-------|-------|------------|
| A (Complete) | 1 | TC-001 |
| B (Minor gaps) | 1 | TC-002 |
| C (Needs work) | 1 | TC-003 |
| D (Incomplete) | 1 | TC-004 |

**Overall Quality: 50% complete** (2/4 at acceptable level)

#### TC-001: Create new audience -- Grade: A

| Check | Status | Notes |
|-------|--------|-------|
| Title | PASS | Clear and includes ticket ID |
| Preconditions | PASS | Login + project setup specified |
| Test Data | PASS | Specific audience name and conditions |
| Steps | PASS | 6 numbered steps |
| Expected Results | PASS | Concrete outcomes per step |

#### TC-002: Edit audience name -- Grade: B

| Check | Status | Notes |
|-------|--------|-------|
| Title | PASS | Clear |
| Preconditions | PASS | Existing audience required |
| Test Data | WARN | Missing new name value |
| Steps | PASS | 4 numbered steps |
| Expected Results | PASS | Name updated confirmation |

**Suggestions:**
- Add specific test data: "Change name from 'Audience Alpha' to 'Audience Beta'"

#### TC-003: Delete audience -- Grade: C

| Check | Status | Notes |
|-------|--------|-------|
| Title | PASS | Clear |
| Preconditions | FAIL | No mention of existing audience |
| Test Data | FAIL | No audience specified |
| Steps | PASS | 3 numbered steps |
| Expected Results | WARN | "Audience is deleted" -- should specify what happens in the UI |

**Suggestions:**
- Add precondition: "An audience named 'Test Audience' exists in the project"
- Add test data: audience name to delete
- Clarify expected result: "Audience removed from list, success notification appears"

#### TC-004: Duplicate audience -- Grade: D

| Check | Status | Notes |
|-------|--------|-------|
| Title | PASS | Clear |
| Preconditions | FAIL | None specified |
| Test Data | FAIL | None specified |
| Steps | FAIL | "Duplicate the audience" -- single vague step |
| Expected Results | FAIL | "It works" |

**Suggestions:**
- Add preconditions: login state, existing audience
- Add test data: source audience name, expected duplicate name
- Expand steps: navigate to audience, click duplicate, verify duplicate created
- Specify expected result: "New audience 'Copy of {name}' appears in the list"

### Step 4: Coverage Analysis

**Coverage: 67% of requirements** (2/3 ACs covered)

| Requirement / AC | Status | Covered By |
|-----------------|--------|------------|
| AC-1: Create audience | COVERED | TC-001 |
| AC-2: Edit and delete | PARTIAL | TC-002 (edit), TC-003 (delete, Grade C) |
| AC-3: Duplicate name error | GAP | -- |

### Missing Test Cases

| # | Missing Scenario | Related AC | Priority |
|---|-----------------|------------|----------|
| 1 | Duplicate audience name shows error | AC-3 | P0 |
| 2 | Create audience with empty name | AC-1 | P1 |
| 3 | Delete audience confirmation dialog | AC-2 | P2 |
| 4 | Edit audience conditions (not just name) | AC-2 | P1 |

### Recommendations

1. Fix 2 incomplete test cases (TC-003, TC-004) before automation
2. Add 4 missing test cases to close coverage gaps (1 P0, 2 P1, 1 P2)
3. AC-3 has zero coverage -- this is a P0 gap

### Actions Offered

- "Fix test cases in JIRA" -- update TC-003 and TC-004 with missing fields
- "Generate missing test cases" -- create 4 new test cases for gaps
- "Export report" -- save to local file
- "Done"
