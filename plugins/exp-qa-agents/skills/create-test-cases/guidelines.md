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

---

## Domain Expert Selection

Same rules as `/exp-qa-agents:analyze-ticket`. Scan ticket content for domain keywords:

| Domain Expert | Trigger keywords |
|--------------|-----------------|
| `web-experimentation` | experiment, A/B test, visual editor, VE, snippet, personalization, campaign, MVT, MAB, web project |
| `feature-experimentation` | flag, feature flag, rollout, targeted delivery, rule, environment, SDK, decide, datafile, FX, CMAB |
| `edge-experimentation` | edge, performance edge, micro-snippet, edge decider, CDN proxy, optimizelyEdge |
| `opal-chat` | Opal, chat, brainstorm, summarize results, review experiment, test ideas, generate copy |
| `product-glossary` | Ambiguous terms, cross-product comparisons |

### Opal Chat Cross-Product Rule

- **Opal + no specific product mentioned** → select `opal-chat` + `web-experimentation` + `edge-experimentation` + `feature-experimentation` (generate test cases covering all 3 products)
- **Opal + specific product mentioned** → select `opal-chat` + only the mentioned product(s)

---

## Failure Recovery Per Step

| Step | On Failure | Checkpoint Saved |
|------|-----------|-----------------|
| Pre-flight (MCP check) | **skip_continue** if file/text input (JIRA not needed); **abort** if JIRA input | None |
| Gather requirements (Step 1) | **ask_user** -- Ask for alternative input source or more context | None |
| Excel parsing | **retry** -- Try csv fallback; if still fails, ask user to export as .csv or .md | None |
| Image parsing | **ask_user** -- Ask user to provide clearer image or paste as text | None |
| Select domain expert(s) | **skip_continue** -- Generate test cases without product-specific steps (generic navigation) | `{ID}_analysis.md` |
| Generate test cases (parallel agents) | **retry** -- Re-dispatch failed category agent once, then merge partial results | `{ID}_analysis.md` |
| Synthesize & deduplicate | **skip_continue** -- Present unsynthesized results, warn about potential duplicates | `{ID}_raw_test_cases.md` |
| User review | **ask_user** -- Allow regenerate, edit, or abort | `{ID}_Test_Design.md` |
| JIRA upload | **retry** -- Retry failed tickets once, then save remaining locally | `{ID}_Test_Design.md` |

**Checkpoint mechanism:** Save the test design document to `{ID}_Test_Design.md` after synthesis (`{ID}` = JIRA ticket ID or input filename). If JIRA upload partially fails, the document serves as the source of truth for manual creation.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| Atlassian MCP not available + JIRA input | **abort**: Exit with error: "Atlassian MCP is not configured. See .mcp.json.template for detailed configuration." |
| Atlassian MCP not available + file/text input | **skip_continue**: Proceed without JIRA. Skip JIRA upload at the end, save locally only |
| No input provided | **ask_user**: Ask user to provide JIRA ticket, file path, or paste test design text |
| Excel file not found or unreadable | **ask_user**: Ask for correct path or alternative format |
| Image text unreadable | **ask_user**: Ask for clearer image or paste content as text |
| No ticket description (JIRA input) | **ask_user**: Ask user for context |
| JIRA upload fails | **retry**: Retry failed ones once, then save locally as `{ID}_Test_Design.md` |
| User cancels upload | **skip_continue**: Save test design file locally |


## Self-Correction

1. **"Add more tests for X"** → Generate additional, deduplicate before adding
2. **"Change priority distribution"** → Adjust and regenerate
3. **"Regenerate from scratch"** → Return to step 3 with new guidance
