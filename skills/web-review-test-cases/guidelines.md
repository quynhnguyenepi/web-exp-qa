# Review Test Cases - Guidelines

Detailed reference material, examples, and review rules. Read this file during pre-flight (Step 1) to apply consistent review standards.

---

## 1. Input Format Parsing

### Excel (.xlsx / .xls)

- Auto-detect test case columns by matching headers (case-insensitive, partial match):
  - Title / Test Case Name / Summary
  - Test Steps / Steps / Actions
  - Expected Results / Expected / Expected Outcome
  - Priority / Severity
  - Preconditions / Pre-condition / Prerequisites
  - Parameters / Test Data / Data
  - Labels / Tags / Category
- If a sheet has no recognizable headers, treat row 1 as headers and ask user to confirm mapping
- Multiple sheets: review each sheet separately, prefix TC IDs with sheet name
- Skip empty rows and summary/header rows (e.g., "Total:", "Coverage:")

### Markdown (.md)

- **Table format:** Parse pipe-delimited tables. Match column headers same as Excel
- **Heading format:** Each `### TC-XX` section is one test case. Extract fields from bold labels (`**Priority:**`, `**Steps:**`, etc.)
- **Mixed format:** Summary table + detailed cards (as used by create-test-cases). Parse both parts

### Image / Screenshot

- Read image with Read tool (multimodal)
- Extract all visible text, reconstruct table structure
- If any text is unclear or cut off, flag it and ask user to confirm
- Common image sources: JIRA ticket screenshots, Confluence page captures, spreadsheet screenshots

### Pasted Text

- Detect structure: numbered lists, tables, free-form paragraphs
- If no clear structure, ask user to clarify which parts are steps vs expected results
- Handle copy-paste artifacts (extra whitespace, broken formatting)

---

## 2. Good vs Bad Examples

### Titles

**Good:**
- "[DHK-1234] Verify Target By Dropdown - URL Option Selection"
- "[DHK-1234] Verify Saved Page - Remove Selected Page"
- "[DHK-1234] Validate Email Field - Empty Input Error Message"

**Bad (flag these):**
- "Test URL field" (too vague, no ticket ID)
- "Check if it works" (not specific)
- "Test 1" or "Case A" (not descriptive)
- "Verify feature" (which feature?)

### Test Steps

**Good (full flow from login):**
```
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page
4. Open experiment "Homepage A/B Test"
5. Click on "Variation #1" to open Visual Editor
6. Wait for Visual Editor to fully load (bottom bar visible)
7. Click on "Target By" dropdown
8. Select "Saved Page" option
```

**Bad (flag these):**
```
1. Go to the form
2. Test the dropdown
3. Check it works
```
Why bad: Vague ("the form"), no specific elements, unclear action, missing login and navigation

**Also bad (starts mid-flow):**
```
1. Navigate to Idea Form
2. Click on "Target By" dropdown
3. Select "Saved Page" option
```
Why bad: Missing login step, missing product/project navigation. A tester cannot reproduce this

### Expected Results

**Good:**
```
1. Login succeeds and dashboard loads with project list
2. Web project page displays with experiment list
3. "Saved Page" option is selected in dropdown
4. Search field appears below the dropdown with placeholder "Search for a page"
```

**Bad (flag these):**
```
- It should work
- The form is correct
- No errors
- Page loads
```
Why bad: Not measurable, not specific, not verifiable

### Preconditions

**Good:**
- `Product: Web Experimentation; Account with active project and at least one A/B experiment in Running state`
- `Product: Feature Flags; Environment: Integration; Feature flag "new_checkout" enabled`

**Bad (flag these):**
- `Login first` (too vague, missing product context)
- (empty) (missing setup requirements entirely)

### Parameters / Test Data

**Good:**
- `Experiment type: A/B; Environment: Integration; Browser: Chrome`
- `email: qa.tester@optimizely.com; input: Test Project Alpha`

**Bad (flag these):**
- `data: some data` (too vague)
- `input: abc123` (unclear what this is for)
- (empty) (missing test configuration)

### Labels

**Good:**
- `Functional, UI`
- `Validation, Error Handling`
- `Edge Case, State Management`

**Bad (flag these):**
- `Important` (not a category)
- `Test` (too generic)
- (empty)

---

## 3. Step Quality Rules (from create-test-cases)

### Full User Flow Required

Test steps MUST follow the complete user flow:
```
Login -> Navigate to product area -> Navigate to feature -> Action -> Verify
```

Always start from login (step 1). Never assume the user is already on a specific page.

### 1:1 Step-to-Result Mapping (CRITICAL)

Every step number MUST have a corresponding expected result with the same number:
- 12 steps = 12 expected results
- 15 steps / 10 results = **FAIL** (mismatched)
- Steps without expected results = **FAIL**

Count both sides and flag any mismatch.

### One Action Per Step

Each step = one action. Flag combined actions:
- **Bad:** "Click Save and verify notification appears" (two actions)
- **Good:** Split into: "9. Click Save" + "10. Verify success notification appears"

### Exact UI Labels

Use exact UI labels from the product, not informal names:
- "Ask Opal" not "open chat"
- "Start Experiment" not "run it"
- "Ideas" (sidebar label) not "Idea Builder" (internal product name)
- "Targeted delivery" not "rollout rule"

### Wait/Load Steps

Include wait steps where UI needs time:
- "Wait for Visual Editor to fully load (bottom bar visible)"
- "Wait for search results to appear"
- "Wait for page to finish loading"

---

## 4. Coverage Patterns

### Happy Path
- Minimum 1 High test per critical user journey
- Cover all steps from entry to completion
- Use realistic, valid data

### Validation
- 1 High test per required field (empty input)
- 1 High test per format rule (invalid format)
- Cover boundary values (min/max length, min/max number)

### Error Handling
- 1 Normal test per API error scenario
- 1 Normal test per user-facing error message
- Include permission denied, network failures, server errors

### State Management
- 1 High test per significant state transition
- Test field clearing, data persistence, conditional display

### Edge Cases
- 1 Low test per edge case
- Empty lists, max data, special characters, very long inputs

---

## 5. Test Data Guidelines

### Valid Inputs (expect these or similar)
- Email: `qa.tester@optimizely.com`
- URL: `https://www.optimizely.com/products`
- Name: `Test Project Alpha`
- Date: `2026-03-12`

### Invalid Inputs (expect these for negative tests)
- Empty string: ``
- Only whitespace: `   `
- Email without @: `testexample.com`
- Special chars: `<script>alert('xss')</script>`
- Very long: `{5000+ chars}`

Flag test cases that say "enter invalid data" without specifying WHAT invalid data.

---

## 6. Anti-Patterns to Flag

| Anti-Pattern | Why It's Bad | What to Suggest |
|-------------|-------------|-----------------|
| Vague steps ("Test the form") | Not reproducible | Specific actions with element names |
| Unclear results ("It should work") | Not verifiable | Observable, measurable outcomes |
| Missing test data ("Enter invalid email") | Ambiguous | Specify exact value: `notanemail` |
| Over-prioritization (all High) | Defeats prioritization | Distribute: 50-60% High, 30-40% Normal, 10-20% Low |
| Generic titles ("Test case 1") | Not descriptive | `[TICKET] Verify [Component] - [Scenario]` |
| No labels/categories | Hard to filter | Add functional categories |
| Steps start mid-flow | Cannot reproduce | Start from login step |
| Combined actions in one step | Hard to pinpoint failures | One action per step |
| Mismatched step/result count | Incomplete verification | 1:1 mapping required |
| Wrong environment for Opal | Opal not available on RC | Use Development or Production with OptiID |
| Single test case covers too many scenarios | Hard to maintain, unclear failures | Split into focused test cases |

---

## 7. Quality Scoring

Apply scores consistently:

| Score | Meaning | Criteria |
|-------|---------|----------|
| **A** | Complete | All required items present and clear. Full user flow. 1:1 step mapping. Specific test data |
| **B** | Minor gaps | 1-2 minor issues: slightly vague result, missing wait step, or missing labels. Still executable |
| **C** | Needs work | Missing preconditions, starts mid-flow, vague steps/results, or mismatched step count |
| **D** | Incomplete | Most required items missing. Not executable as written |

### Grade Modifiers (from create-test-cases rules)

These issues automatically **lower the grade by one level**:
- Steps start mid-flow (no login) -> max grade B
- Mismatched step/result count -> max grade C
- All expected results are vague ("works", "no errors") -> max grade D
- Wrong environment for feature (Opal on RC) -> flag, max grade B

---

## 8. Navigation Pattern Checks

When domain expert knowledge is available, validate navigation follows the correct product patterns:

### Web Experimentation
```
Login -> [Instance selection] -> Web project -> Experiments -> Experiment -> [Tab] -> Action
```

### Feature Experimentation
```
Login -> [Instance selection] -> FX project -> Flags -> Flag -> [Tab] -> [Environment] -> Action
```

### Edge Experimentation
```
Login -> [Instance selection] -> Edge project -> Experiments -> Experiment -> [Area] -> Action
```

### Opal Chat
```
Login via OptiID -> Instance selection -> Project -> [Navigate to Opal feature] -> "Ask Opal" -> Action
```
Note: Opal requires OptiID login (Production or Development), NOT RC.

### Visual Editor
```
Login -> [Instance selection] -> Project -> Experiment -> Variation click -> Wait for VE load -> Action
```

---

## 9. Rewriting Existing Test Cases

When the user selects "Rewrite existing test cases", apply these patterns:

### Common Rewrite Patterns (from real reviews)

#### Missing Login Steps (most common issue)

**Before (starts mid-flow):**
```
1. Create new experiment without linking to hypothesis
2. Open experiment > Plan > Hypothesis
```

**After (full flow):**
```
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page
4. Click "Create New..." and select "A/B Test"
5. In the experiment creation form, do NOT click on Link Hypothesis dropdown
6. Fill in experiment name "No Hypothesis Experiment" and required fields
7. Click "Create Experiment"
8. Open the newly created experiment
9. Navigate to Plan > Hypothesis tab
```

#### Missing Expected Results

**Before:**
```
Expected Results:
1. (no expected result specified)
2. Create Hypothesis popup is opened
3. (no expected result specified)
```

**After:**
```
Expected Results:
1. Experiment creation form opens with Link Hypothesis dropdown visible
2. Create Hypothesis popup opens with title, start date, and end date fields
3. Date fields accept the values; title field remains blank
```

Rules:
- NEVER leave "(no expected result specified)" in rewritten TCs
- Each expected result must be concrete and verifiable
- Navigation steps get navigation-related results ("page loads", "tab opens", "section displays")
- Action steps get action-related results ("field accepts input", "dropdown expands", "popup opens")

#### Copy-Paste Precondition Errors

Common in permission matrix test cases. The title says one role combination but the precondition says another (copied from a different TC).

**Detection:** Compare the role mentioned in the title with the role in the precondition. If they differ, the precondition is wrong.

**Example:**
- Title: "Verify behavior when user is Viewer in experiment but **creator** in CMP"
- Precondition (wrong): "User A has viewer role in experiment A and **admin** role in CMP"
- Fix: "User A has viewer role in experiment A and **creator** role in CMP"

#### Expanding Thin Test Cases

Test cases with only 2-4 steps are usually incomplete. Expand by:
1. Adding login steps (3-4 steps)
2. Adding navigation steps (1-2 steps)
3. Adding verification steps after each significant action
4. Adding cleanup/validation steps at the end (e.g., verify in CMP)

**Typical expansion:** 2-4 steps -> 8-16 steps

---

## 10. Report Standards

- Always include BOTH quality summary (scores) and coverage analysis (gaps)
- List specific suggestions for each test case graded C or D
- Quantify coverage as percentage: `{covered}/{total} ACs covered`
- Missing test cases table must include priority classification
- Offer actionable next steps: fix in JIRA, generate missing TCs, export report
- When reviewing from Excel/image, note the original source format in the report header
