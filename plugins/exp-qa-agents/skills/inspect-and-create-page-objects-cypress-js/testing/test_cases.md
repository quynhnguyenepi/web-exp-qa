# Inspect and Create Page Objects (Cypress JS) - Test Cases

## TC-001: Create page objects for a new feature page

**Preconditions:** Playwright MCP is connected. Target page is accessible. No existing page objects for the feature.

**Steps:**
1. Invoke skill with a target URL, product area (`web`), and feature name (`audiences`)
2. Skill navigates to the URL in the main thread (NOT a background agent)
3. Skill takes a screenshot to confirm page loaded
4. Skill runs `browser_evaluate` to extract all `data-test-section` attributes from the DOM
5. Skill launches background Agent for codebase analysis in parallel
6. Skill identifies and classifies interactive elements from JS evaluation results
7. Skill generates webelements file and page object file
8. Skill presents files to user for review

**Expected Results:**
- Webelements file is generated at `cypress/pages/webelements/web/audiences/AudiencesPageElements.js`
- Page object file is generated at `cypress/pages/web/audiences/AudiencesPage.js`
- Webelements class extends the correct base class (`WebBasePageElements`)
- Page object class extends the webelements class (NOT the base page class)
- All selectors use `data-test-section` where available
- All methods return `this` for chaining
- User is asked to confirm before files are written
- `browser_evaluate` was used to extract selectors (not relying solely on snapshot)

## TC-002: Handle elements with generic data-test-section values

**Preconditions:** Playwright MCP is connected. Target page has elements with `undefined-link` or other generic `data-test-section` values.

**Steps:**
1. Invoke skill for a page where some elements have generic `data-test-section` (e.g., `undefined-link`)
2. Skill runs `browser_evaluate` and detects multiple elements with same `data-test-section`
3. Skill uses scoped `this.parentContainer().contains('tag', 'text')` for those elements

**Expected Results:**
- Elements with generic `data-test-section` use scoped `contains()` within parent container
- Selectors do NOT use `cy.getDataTestSection('undefined-link')` directly
- Each scoped selector uniquely identifies one element
- Parent container is a stable element with a unique `data-test-section`

## TC-003: Update existing page objects with new elements

**Preconditions:** Playwright MCP is connected. Page objects already exist for the feature. UI has new elements added.

**Steps:**
1. Invoke skill for a feature that already has page objects
2. Skill detects existing page object files
3. Skill reads existing files to identify current selectors
4. Skill inspects the page and identifies NEW elements not in existing files
5. Skill presents only the new elements to add

**Expected Results:**
- Existing elements are not duplicated
- Only new elements are added to the files
- Existing methods and structure are preserved
- User is shown what will be added vs what already exists

## TC-004: Handle page requiring login

**Preconditions:** Playwright MCP is connected. Target page requires authentication.

**Steps:**
1. Invoke skill with a URL behind authentication and credentials
2. Skill navigates to the URL in the main thread
3. Skill detects login page and fills credentials via `browser_fill_form`
4. Skill clicks login button and waits for redirect
5. Skill navigates to the target page or element
6. Skill proceeds with normal inspection

**Expected Results:**
- Login is handled entirely in the main thread (NOT delegated to background Agent)
- Login form is filled via `browser_fill_form`
- Navigation returns to the target URL after login
- Screenshot taken to confirm successful login
- Inspection proceeds normally after login

## TC-005: Handle large snapshots (complex pages)

**Preconditions:** Playwright MCP is connected. Target page is complex with many elements.

**Steps:**
1. Invoke skill for a complex page
2. `browser_snapshot()` returns result exceeding token limit
3. Skill falls back to `browser_evaluate` for targeted element extraction
4. Skill uses `browser_take_screenshot` for visual context

**Expected Results:**
- Skill does not fail on oversized snapshots
- `browser_evaluate` is used to extract relevant elements via JS
- Screenshot is taken for visual reference
- Elements are correctly identified despite snapshot overflow

## TC-006: Create common page objects (cross-product)

**Preconditions:** Playwright MCP is connected. Feature is accessible from all products (e.g., Help Center, Settings).

**Steps:**
1. Invoke skill for a common feature (e.g., Help Center dialog)
2. Skill determines product area is `common`
3. Skill generates files in the common directory (not web or flag)

**Expected Results:**
- Webelements file placed at `cypress/pages/webelements/common/{ClassName}Elements.js`
- Page object file placed at `cypress/pages/common/{ClassName}.js`
- Webelements class extends `CommonBasePageElements`
- Import paths are correct for the common directory structure
- Files placed directly in folder (no feature subfolder) for standalone dialogs

## TC-007: Multi-state page inspection (dialogs, tabs)

**Preconditions:** Playwright MCP is connected. Target page has multiple interactive states (tabs, modals).

**Steps:**
1. Invoke skill for a complex page
2. Skill takes initial screenshot
3. Skill asks user which sections to inspect
4. User clicks to trigger a dialog
5. Skill takes screenshot of dialog state
6. Skill runs `browser_evaluate` to extract elements in the dialog state
7. Skill combines elements from all states

**Expected Results:**
- Elements from all inspected states are included
- Selectors from default state and dialog/tab states are grouped appropriately
- Region comments reflect the different sections/states
- No duplicate selectors across states
- `browser_evaluate` was used in each state (not just snapshot)

## TC-008: Playwright MCP not delegated to background agent

**Preconditions:** Playwright MCP is connected.

**Steps:**
1. Invoke skill with any target URL
2. Observe that all Playwright MCP calls happen in the main thread

**Expected Results:**
- `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_evaluate`, `browser_fill_form`, `browser_take_screenshot` are ALL called in the main thread
- Only codebase analysis (Glob, Grep, Read) runs in background Agent
- No Playwright MCP calls appear in background Agent prompts
