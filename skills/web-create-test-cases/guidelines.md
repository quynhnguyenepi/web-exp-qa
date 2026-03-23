# Test Case Quality Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## 1. Good vs Bad Examples

### Titles

**Good:**
- "Verify Target By Dropdown - URL Option Selection"
- "Select Saved Page - Remove Selected Page"
- "Screenshot Upload - File Dialog Selection"
- "Validate Email Field - Empty Input Error Message"

**Bad:**
- "Test URL field" (too vague)
- "Check if it works" (not specific)
- "URL stuff" (unclear)
- "Test 1" or "Case A" (not descriptive)

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
9. Enter "Homepage" in the search field
10. Click on "Homepage" from the dropdown results
```

**Bad:**
```
1. Go to the form
2. Test the dropdown
3. Check it works
```
**Why bad:** Vague ("the form"), no specific elements ("the dropdown"), unclear action ("check it works"), missing login and navigation steps

**Also bad (starts mid-flow):**
```
1. Navigate to Idea Form
2. Click on "Target By" dropdown
3. Select "Saved Page" option
```
**Why bad:** Missing login step, missing product/project navigation. A tester cannot reproduce this without knowing which product area to navigate to

### Expected Results

**Good:**
```
- "Saved Page" option is selected in dropdown
- Search field appears below the dropdown
- Search field placeholder text reads "Search for a page"
- Dropdown menu expands showing list of available pages
```

**Bad:**
```
- It should work
- The form is correct
- No errors
```
**Why bad:** Not measurable, not specific, not verifiable

### Pre-condition

**Good:**
- `Product: Web Experimentation; Account with active project and at least one experiment`
- `Product: Feature Flags; Environment: Integration; Feature flag "new_checkout" enabled`
- `Product: Web Experimentation; Visual Editor loaded with target page`

**Bad:**
- `Login first` (too vague, missing product context)
- (empty) (missing setup requirements)

### Parameters

**Good:**
- `Experiment type: A/B; Rule type: Targeted delivery; Environment: Integration`
- `Experiment type: Multivariate; Environment: RC; Browser: Chrome`
- `Rule type: A/B test; Flag type: Boolean; Environment: Production`

**Bad:**
- `data: some data` (too vague, not using standard parameter names)
- `input: abc123` (unclear what this is for)
- (empty) (missing test configuration)

### Labels

**Good:**
- `Functional, UI`
- `Validation, Error Handling`
- `Integration, State Management`

**Bad:**
- `Important` (not a category)
- `Test` (too generic)
- (empty) (missing categorization)

---

## 2. Coverage Patterns with Examples

### Happy Path

**Definition:** Primary user journey with valid inputs, expected user behavior

**Guidelines:**
- Minimum 1 High test per critical user journey
- Cover all steps from entry to completion
- Use realistic, valid data

**Example:** User selects "URL" as Target By, enters valid URL, sees URL field populated

---

### Validation

**Definition:** Testing input validation rules for required and optional fields

**Guidelines:**
- 1 High test per required field (empty input)
- 1 High test per format rule (invalid format)
- Cover boundary values (min/max length, min/max number)

**Example:** Email field validation
- High: Empty email → error "Email is required"
- High: Invalid format "notanemail" → error "Invalid email format"
- Normal: Max length (255 chars) → accepted or error

---

### Error Handling

**Definition:** Testing system behavior when errors occur

**Guidelines:**
- 1 Normal test per API error scenario
- 1 Normal test per user-facing error message
- Include permission denied, network failures, server errors

**Example:** Saved Pages API fails
- Normal: API returns 500 → error message "Unable to load saved pages"
- Normal: API returns empty → "No saved pages available"

---

### State Management

**Definition:** Testing how UI state changes based on user actions

**Guidelines:**
- 1 High test per significant state transition
- Test field clearing, data persistence, conditional display

**Example:** Switching Target By options
- High: Select URL → shows URL field, hides Saved Page field
- High: Switch to Saved Page → shows Saved Page field, clears URL field

---

### Edge Cases

**Definition:** Boundary conditions, unusual inputs, extreme scenarios

**Guidelines:**
- 1 Low test per edge case
- Empty lists, max data, special characters, very long inputs

**Example:**
- Low: Search with no results → "No pages found"
- Low: Page name with special chars (<>&") → renders correctly
- Low: 1000+ saved pages → pagination works

---

## 3. Test Data Guidelines

### Valid Inputs

**Use realistic, representative data:**
- Email: `qa.tester@optimizely.com`
- URL: `https://www.optimizely.com/products`
- Name: `John Smith`
- Phone: `+1 (555) 123-4567`
- Date: `2026-02-24`

**Include boundary values:**
- Min length: `a` (1 char)
- Max length: `{254 chars}` for email
- Min number: `0` or `-1`
- Max number: `999999`

### Invalid Inputs

**Common user mistakes:**
- Email without @: `testexample.com`
- URL without protocol: `www.example.com`
- Phone with letters: `555-OPTI`
- Date in wrong format: `24/02/2026` (when expecting `YYYY-MM-DD`)

**Malformed data:**
- Empty string: ``
- Only whitespace: `   `
- Special chars: `<script>alert('xss')</script>`
- Very long: `{10000 chars}`

---

## 4. Anti-Patterns

### Vague Steps

**Bad:** "Test the form"
**Why:** Unclear what to test, how to test it, what the outcome should be
**Good:** "1. Navigate to Idea Form\n2. Observe all form fields are rendered"

### Unclear Results

**Bad:** "It should work"
**Why:** Not measurable, not verifiable
**Good:** "- Form submits successfully\n- Success message 'Idea saved' appears\n- User redirected to Ideas list page"

### Missing Data

**Bad:** "Enter invalid email"
**Why:** Unclear what constitutes "invalid"
**Good:** "Enter `notanemail` in email field" or "Parameters: `email: notanemail`"

### Over-Prioritization

**Bad:** All 50 test cases are High
**Why:** Not everything is critical; defeats the purpose of prioritization
**Good:** Distribute priorities: 30 High (core), 15 Normal (important), 5 Low (edge cases)

### Generic Titles

**Bad:** "Test case 1", "Check functionality", "Verify feature"
**Why:** Not descriptive, hard to understand what's being tested
**Good:** "Verify URL Field - Valid HTTPS URL Input Acceptance"

### No Categorization

**Bad:** (empty Labels column)
**Why:** Hard to filter, analyze coverage, plan automation
**Good:** "Functional, Validation" or "UI, Accessibility"

---

## 6. Universal Test Case Format — Navigation in Pre-condition

> **CRITICAL:** Áp dụng cho TẤT CẢ Optimizely tickets: VE, Monolith, Opal, FX, Edge.
> Navigation đến màn hình cần test → Pre-condition. Test Steps bắt đầu từ hành động trên màn hình đó.
> Xem file gốc: `CJS-9865_Test_Design.md` (VE) để tham khảo format chuẩn.

---

### Rule 1: Pre-condition absorbs navigation — Steps bắt đầu từ action (áp dụng cho TẤT CẢ tickets)

**SAI (cũ — mọi ticket type):**
```
Test Steps:
1. Navigate to https://rc-app.optimizely.com and login
2. Select experiment instance
3. Navigate to Web project
4. Go to Experiments page
5. Open experiment → Metrics tab
6. Click "Add Metric"
```

**ĐÚNG (tất cả tickets):**
```
Pre-condition:
- A/B experiment in Draft status with at least one click event
- User is logged in and navigated to the experiment's Metrics tab

Test Steps:
1. Click "Add Metric" button
2. Select "Click-Donate2" from the metric list
3. Click "Save"
4. Observe the Metrics tab
```

**VE tickets đặc biệt:**
```
Pre-condition:
- Experiment A/B test in Draft status with at least one saved change on Variation #1
- User is logged in and navigated to the experiment

Test Steps:
1. Open variation in Visual Editor        ← Step 1 CỐ ĐỊNH cho VE
2. Click "Changes" button in the bottom bar
3. Observe the ChangeLog panel
```

**Quy tắc:**
- Pre-condition luôn kết thúc bằng: `"User is logged in and navigated to [specific screen]"`
  - VE: `"...navigated to the experiment"`
  - Monolith Experiments: `"...navigated to the Optimizations page"`
  - Monolith Experiment detail: `"...navigated to the experiment detail page"`
  - Monolith Metrics tab: `"...navigated to the experiment's Metrics tab"`
  - Campaign: `"...navigated to Experience #X"`
- **VE Step 1 luôn là: `"Open variation in Visual Editor"`**
- **Monolith/FX/Edge Step 1:** hành động đầu tiên trên màn hình được navigate tới
- Không bao giờ đặt login/navigation vào Test Steps với bất kỳ ticket nào

---

### Rule 2: Expected Results — chỉ cho verification steps, KHÔNG phải 1:1

**SAI (cũ):**
```
Expected Results:
1. Login page loads successfully
2. Authentication completes
3. Instance selected
4. VE loads on website
5. Bottom bar visible
6. Changes button visible
7. ChangeLog panel opens
```

**ĐÚNG (VE format):**
```
Expected Results:
3. ChangeLog panel opens with both tab labels (Preview, Saved) visible
```

**Quy tắc:**
- Expected Results chỉ có số cho các steps có từ: `"Observe"`, `"Confirm"`, `"Check"` — và chỉ verify kết quả thực sự cần kiểm tra
- Số Expected Result = số của step tương ứng (e.g., nếu step 5 là "Observe the error", thì Expected Result viết `5. Error notification: "..."`)
- Có thể có thêm kết quả bổ sung với số tiếp theo (e.g., `6. No new variation tab is created`) dù flow chỉ có 5 steps
- KHÔNG viết "Login succeeds", "Authentication completes", "Instance selected" — đây là pre-condition, không phải expected result

---

### Rule 3: Labels — lowercase, comma-separated, dùng JIRA tag format

**SAI:** `Functional, UI` / `State Management` / `Error Handling`

**ĐÚNG:** `new_ve,opal,web` / `new_ve,variation,web` / `new_ve,opal,web,smoke_suite`

**Standard label sets cho VE:**
- VE Opal ticket: `new_ve,opal,web`
- VE Variation ticket: `new_ve,variation,web`
- Smoke test: thêm `,smoke_suite`
- Simplified VE: `new_ve,web`

---

### Rule 4: Parameters — loại bỏ fields thừa

**LOẠI BỎ khỏi Parameters:**
- `Environment: Development` — global setting, không cần repeat
- `Login: OptiID (Okta SSO)` — global for Opal, không cần repeat

**GIỮ trong Parameters:**
- `Experiment type: A/B Test / MVT / MAB / Campaign`
- `Browser: Chrome`
- `Enable Support for Dynamic Websites: ON/OFF` (nếu test case liên quan)
- Test data cụ thể (e.g., 501-char string)

---

### Rule 5: Priority mapping cho VE tickets

| Priority | Khi nào dùng | Số TCs |
|---|---|---|
| **Critical** | Full flow duy nhất (1 TC toàn document) | 1 |
| **High** | Core AC + Running status check + quan trọng | ~8-10 |
| **Normal** | Statuses khác, validation, edge cases, bug regression | ~10-14 |
| **Low** | Boundary values, special chars, regression smoke | ~3-5 |

---

### Rule 6: Full Flow TC (Critical) — format đặc biệt

Full Flow TC có Expected Results chỉ tại 3 checkpoints:
1. Preview variation (step số X)
2. Preview experiment / QA ball (step số Y)
3. Live website sau publish (step cuối)

Không có Expected Results cho các setup steps.

---

### Rule 7: "Confirm" trong Steps vs Expected Results

- `"Confirm X"` ở ĐẦU step → OK, là pre-condition check trước action chính
- `"Verify X"` ở CUỐI step → **MOVE sang Expected Results**
- `"Observe X"` → OK trong step, kết quả viết trong Expected Results với cùng số

---

## 5. Quality Checklist

Before finalizing test cases, verify:

- [ ] All titles are action-oriented and descriptive
- [ ] All test steps are numbered and specific
- [ ] All expected results are measurable and verifiable
- [ ] Priority distribution is balanced (50-60% High, 30-40% Normal, 10-20% Low)
- [ ] Test data is specified in Parameters column
- [ ] All test cases have at least one Label
- [ ] Coverage includes happy path, validation, error handling, edge cases
- [ ] Total test case count is appropriate for ticket type (Story: 15-30, Bug: 5-10)
- [ ] No vague language ("test it", "check it", "should work")
- [ ] No duplicate test cases
- [ ] Coverage summary calculations are accurate
