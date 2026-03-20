# PR Review Quality Guidelines

Reference guide for reviewing GitHub Pull Requests against project coding conventions. Read this file during Step 1 (Sync Docs) to ensure consistent review quality.

---

## 1. Cypress Test Quality Checklist

### Critical Checks (Must Flag if Missing)

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| Page Object pattern | No `cy.get()` in spec files — all UI interactions via page objects | Critical |
| Builder pattern | Test data created via Builders, not object literals | Critical |
| Cleanup | `cy.deleteAccount()` in `after()` or `afterEach()` | Critical |
| No `.only()` / `.pause()` | These must never be committed | Critical |
| `function()` syntax | `describe`, `it`, `before`, `after` must use `function()`, not `() =>` | Critical |
| `testIsolation: false` | Required when using `before()`/`after()` hooks | Critical |
| Test case ↔ script mapping | Test steps in JIRA (from ticket ID in `it()` name) match script steps; mismatches need JIRA comment explanation | Critical |

### Important Checks (Should Flag)

| Check | What to Look For | Severity |
|-------|-----------------|----------|
| `eslint-disable` | `/* eslint-disable no-undef */` at top of spec files | Suggestion |
| Max 5 tests per file | Split into multiple spec files if >5 `it` blocks | Suggestion |
| Import path depth | Correct `../` count using `depth - 1` formula | Critical |
| Region comments | `#region Setup Test Data`, `#region Test Execution`, `#region Cleanup` | Suggestion |
| Test naming | `[TICKET-ID][Product][Module]_Description` format | Critical |
| Tags | Correct CommonTag/WebTag/FlagTag/EdgeTag from tagList.js | Suggestion |
| API-first setup | Setup via API commands in hooks, not UI navigation | Suggestion |

---

## 2. Code Convention Checks

### Architecture & Design

- **Single Responsibility**: Each function/method does one thing
- **DRY**: No duplicated code — extract into helpers/utilities
- **Separation of Concerns**: Page objects for UI, builders for data, APIs for setup
- **Consistent Patterns**: Follow existing codebase patterns

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Spec files | snake_case.spec.js | `ab_test_archive.spec.js` |
| Directories | snake_case | `experiment_details/` |
| Page objects | PascalCase.js | `ExperimentListPage.js` |
| Builders | camelCase.js | `experimentBuilder.js` |
| Variables | camelCase | `experimentName` |
| PO methods (actions) | `{verb}{Element}` | `clickSaveButton()` |
| PO methods (verify) | `verify{Condition}` | `verifyErrorMessageDisplayed()` |

### Common Anti-Patterns to Flag

| Anti-Pattern | Better Alternative |
|-------------|-------------------|
| `cy.get('[data-test="..."]')` in spec | Use page object method |
| `cy.wait(5000)` | Use `should('exist')` or proper assertion |
| Arrow functions in describe/it | Use `function()` for `this` context |
| Hardcoded test data | Use builders, testData files, or random values |
| Missing cleanup | Add `cy.deleteAccount()` in after/afterEach |
| `it.only()` or `describe.only()` | Remove before committing |
| Object literal for test data | Use Builder pattern |
| Consecutive calls on same object without chaining (`obj.a(); obj.b();`) | Use call chaining: `obj.a().b();` |
| Element logic (`.find()`, `.not()`, CSS selectors) in `Page.js` | Move to `Elements.js`; `Page.js` composes element methods |

---

## 3. Review Scoring Guide

| Score | Criteria | Action |
|-------|---------|--------|
| **10/10** | Excellent — follows all conventions, clean code, well-structured | Approve |
| **8-9/10** | Very good — minor suggestions only, no convention violations | Approve |
| **7/10** | Good — a few suggestions, no critical issues | Comment |
| **5-6/10** | Needs improvement — has convention violations that should be fixed | Request Changes |
| **3-4/10** | Poor — multiple critical issues (missing cleanup, .only(), no page objects) | Request Changes |
| **1-2/10** | Major problems — fundamental approach issues, needs rework | Request Changes |

---

## 4. Review Format Template

```markdown
## CODE is reviewed by CLAUDE CODE

**Score: X/10**

### Positives
- Point 1
- Point 2

### Issues / Improvements

#### Critical (Must Fix)
- Issue with code snippet and suggested fix

#### Suggestions (Should Consider)
- Suggestion 1

#### Minor Notes
- Note 1

### JIRA Context
_(Only if JIRA ticket found)_
- Ticket: [ID](URL)
- Requirements alignment: summary

### Questions
- Question 1?

---
*Review generated following coding conventions in .claude/docs/*
```

---

## 5. Product-Specific Review Notes

### Web Tests
- Account: `cy.createAccount(Cypress.env('web_account'))`
- Tags: `WebTag.web` + module-specific CommonTag
- Builders: ExperimentBuilder, CampaignBuilder, PageBuilder, etc.
- Visual Editor: Check `verifyBottomBarVisible()` before VE interactions

### Flag Tests
- Account: `cy.createFlagsAccount()`
- Tags: `FlagTag.flags` + module-specific CommonTag
- Hooks: Typically `beforeEach`/`afterEach` (independent tests)
- Wait: `commonBasePage.waitForTableLoadSpinnerDisappear()` after navigation

### Edge Tests
- Tags: `EdgeTag.edge`
- Follow patterns from `cypress/e2e/edge/` directory

---

## 6. JIRA Context Review

When JIRA ticket is linked to the PR:

- **Verify AC coverage**: Do the PR changes address all acceptance criteria?
- **Check attached files**: Are requirements from attached specs/mockups reflected?
- **Note gaps**: Flag any AC or requirements not covered by the changes
- **Cross-reference**: Link specific code changes to specific AC items

---

## 7. Test Case ↔ Script Mapping

When the PR contains test files (`cypress/e2e/**/*.spec.js`) with JIRA ticket IDs in `it()` block names:

### When to Check
- PR contains `.spec.js` files under `cypress/e2e/`
- `it()` blocks contain JIRA ticket IDs in format `[TICKET-ID]` (e.g., `it('[CJS-9525] Dashboard...')`)
- Atlassian MCP is available

### How to Evaluate
1. **Extract ticket IDs** from `it()` block names using pattern `\[([A-Z]{2,4}-\d{4,5})\]`
2. **Fetch test cases** from JIRA (`mcp__atlassian__jira_get_issue`) and Zephyr Scale (`mcp__atlassian__jira_search`)
3. **Extract script steps** from `it()` blocks and `beforeEach`/`before` hooks
4. **Semantic matching**: Compare intent of each JIRA step against script actions
   - Allow different wording (e.g., "Click login" ≈ `loginPage.clickLoginButton()`)
   - Allow API setup replacing UI steps
   - Allow combined/reordered steps

### Pass/Fail Criteria

| Result | Condition | Action |
|--------|-----------|--------|
| **PASS** | All JIRA test steps semantically covered by script | No issue to flag |
| **PASS (with note)** | Mismatch found BUT JIRA comment explains deviation | Note in review, no score impact |
| **FAIL** | Mismatch found AND no JIRA comment explanation | Flag as issue, deduct score |

### Score Impact
- All PASS or PASS (with note): No deduction
- 1 FAIL: -1 point, add to Suggestions
- 2+ FAIL: -2 points, add to Critical Issues

---

## References

This guidelines document should be read during Step 1 (Sync Docs) before analyzing any PR. SKILL.md references these patterns when evaluating code quality.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| `gh` not authenticated | Display instructions, exit |
| PR not found | Ask user to verify |
| JIRA MCP unavailable | Mark JIRA checks as "N/A -- unable to verify", continue with code review |
| Post fails | Save to file, provide manual instructions |
| PR too large to diff | Warn user, review what's available |


## Self-Correction

1. **"Too harsh/lenient"** -> Re-evaluate, adjust score
2. **"Focus on architecture"** -> Re-review with emphasis
3. **"Change to Approve"** -> Update action, re-present
4. **"Skip JIRA checks"** -> Mark as N/A, focus on code quality only
5. **"Check GitHub Actions results"** -> Fetch workflow runs via `gh run list`
