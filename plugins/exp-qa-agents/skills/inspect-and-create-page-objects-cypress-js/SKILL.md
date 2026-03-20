---
description: Inspect a web page using Playwright MCP browser automation, identify interactive elements and their selectors, and generate Cypress page object files (webelements + page object) following the project's conventions. Use when you need to create or update page objects for a new feature or page.
---

## Dependencies

- **MCP Servers:** Playwright (for browser inspection)
- **Related Skills:** `/exp-qa-agents:create-test-scripts-cypress-js`

You are a page object generation agent.
Domain: cypress-page-objects
Mode: sequential-then-parallel
Tools: Read, Write, Edit, TodoWrite, AskUserQuestion, Agent, Bash, Glob, Grep

Navigate to a web page using Playwright MCP, take a snapshot to identify interactive elements and their selectors, then generate Cypress page object files (webelements class + page object class) following the project's conventions.

## When to Use

Invoke this skill when you need to:

- Create page objects for a new feature or page that doesn't have them yet
- Update existing page objects with new elements after a UI change
- Generate selectors for elements you can see in the browser but don't know the attributes for
- Quickly scaffold webelements + page object files for a new area of the application

## Workflow Overview

```
Get URL & Context -> Navigate & Login -> Extract data-test-section via JS -> Analyze Existing Patterns (parallel) -> Identify Elements -> Generate Webelements -> Generate Page Object -> Present to User
```

**Simple Flow:**
```
URL + Credentials -> Browser Navigate + Evaluate JS -> Codebase Analysis (background) -> Classify Elements -> Generate Files -> User Review
```

## Execution Workflow

### Step 0: Get Target URL and Context

**Todo:** Mark "Get target URL" as `completed`, mark "Navigate, login, and inspect" as `in_progress`

1. **Accept input:**
   - Target URL to inspect (e.g., `https://app.optimizely.com/v2/projects/123/experiments`)
   - Login credentials (if provided)
   - Product area: `web`, `flag`, or `common`
   - Feature/module name (e.g., `audiences`, `visual_editor`, `settings`)

2. **If not provided**, use AskUserQuestion to gather:
   - "What is the URL of the page to inspect?"
   - "Which product area? (web / flag / common)"
   - "What is the feature/module name? (e.g., audiences, settings, visual_editor)"

3. **Determine file paths** (files may live directly in the product folder or in a feature subfolder):
   - Webelements: `cypress/pages/webelements/{product}/{ClassName}Elements.js` or `cypress/pages/webelements/{product}/{feature}/{ClassName}Elements.js`
   - Page object: `cypress/pages/{product}/{ClassName}.js` or `cypress/pages/{product}/{feature}/{ClassName}.js`
   - Use feature subfolder when the feature has multiple page objects; use direct folder for standalone dialogs/popups

### Step 1: Navigate and Inspect Page (MAIN THREAD)

**CRITICAL:** Playwright MCP tools can ONLY be used in the main thread. Do NOT delegate browser navigation to a background Agent.

1. **Navigate to the page:**
   ```
   browser_navigate({ url: "{TARGET_URL}" })
   ```

2. **Handle login if needed:**
   - If redirected to login page or credentials were provided, fill the login form:
     ```
     browser_fill_form({ fields: [
       { name: "Email", type: "textbox", ref: "{ref}", value: "{email}" },
       { name: "Password", type: "textbox", ref: "{ref}", value: "{password}" }
     ]})
     browser_click({ ref: "{login_button_ref}", element: "Log In button" })
     ```
   - If credentials not provided, ask user via AskUserQuestion
   - After login, navigate to target URL if not automatically redirected

3. **Take a screenshot** to visually confirm the page:
   ```
   browser_take_screenshot({ type: "png", filename: "page-inspection.png" })
   ```

4. **If the page has multiple sections/tabs**, ask user which area to inspect and click through to reveal elements:
   ```
   browser_click({ ref: "{tab_ref}", element: "{tab_or_section}" })
   ```

5. **For dialogs/popups**, click to open them first, then inspect:
   ```
   browser_click({ ref: "{trigger_ref}", element: "{trigger element}" })
   browser_take_screenshot({ type: "png", filename: "dialog-open.png" })
   ```

### Step 2: Extract data-test-section Attributes (CRITICAL STEP)

**Todo:** Mark "Navigate, login, and inspect" as `completed`, mark "Extract data-test-section attributes" as `in_progress`

**IMPORTANT:** The `browser_snapshot()` accessibility tree does NOT show `data-test-section` attributes. You MUST use `browser_evaluate` to extract them from the DOM.

Use `browser_evaluate` to run JavaScript on the page and extract all `data-test-section` attributes from relevant elements. Filter results by feature keyword or container scope to avoid overwhelming output.

**See guidelines.md** for the complete JavaScript code template and filtering strategy.

**Why this step is critical:**
- Without this, you'll miss `data-test-section` selectors and fall back to fragile selectors
- The snapshot shows element roles/text but NOT custom attributes
- This step was the key learning from real execution — always extract `data-test-section` via JS

**Handle elements with generic `data-test-section` values:**
- Elements with `undefined-link` or similar generic values should use **scoped `cy.contains()`** within a parent container instead:
  ```javascript
  // BAD: cy.getDataTestSection('undefined-link') — matches multiple elements
  // GOOD: this.supportDialog().contains('a', 'Knowledge Base') — scoped to parent
  ```

### Step 3: Analyze Existing Patterns (BACKGROUND AGENT)

**Todo:** Mark "Extract data-test-section" as `completed`, mark "Analyze existing patterns" as `in_progress`

Launch a background Agent to analyze codebase patterns while you process the extracted elements:

```
Agent({
  description: "Analyze existing page object patterns",
  subagent_type: "Explore",
  run_in_background: true,
  prompt: "Analyze existing page object patterns for creating a {Feature} page object. Check for existing files, read base classes, examine similar dialogs/modals, and return: existing elements list, base class info, available commands, dialog patterns."
})
```

The agent analyzes inheritance patterns, existing files, and similar page objects in the background. **See guidelines.md** for detailed agent instructions.

### Step 4: Identify and Classify Elements

**Todo:** Mark "Analyze existing patterns" as `completed`, mark "Identify and classify elements" as `in_progress`

From the `browser_evaluate` results and snapshot, identify all interactive elements and classify them by category (Buttons, Links, Inputs, Selects, Checkboxes, Dialogs, Containers, Tabs, Labels, Icons).

**For each element, select the best selector** (in priority order):

1. `data-test-section` attribute -> use `cy.getDataTestSection()`
2. `data-test-section` on parent + `.findDataTestSection()` for child
3. `data-testid` attribute -> use `cy.get('[data-testid="..."]')`
4. Unique `id` attribute -> use `cy.get('#id')` or `.find('#id')`
5. **Scoped `cy.contains('tag', 'text')` within parent** -> for elements with generic/undefined `data-test-section`
6. Unique CSS class -> use `cy.get('.class-name')`

**See guidelines.md** for the complete element classification table with naming suffixes.

**Present the element table to the user** before generating files, showing:
- Element name, `data-test-section` value, type, and proposed selector approach

### Step 5: Generate Webelements File

**Todo:** Mark "Identify and classify elements" as `completed`, mark "Generate webelements file" as `in_progress`

Generate the webelements class following conventions. Each element gets one method accepting optional `options` parameter.

**Rules:**
- Use `cy.getDataTestSection()` for `data-test-section` attributes
- Use `.findDataTestSection()` for nested elements within a parent that has `data-test-section`
- Use `.find()` for nested elements using CSS selectors
- Use `this.{parent}().contains('tag', 'text')` for text-based selectors scoped to a container
- Group related selectors with `#region` / `#endregion` comments
- No action logic — only return element references
- Import path must be relative and correct for the file location

**Inheritance by product area:**
- `common` -> extends `CommonBasePageElements`
- `web` -> extends `WebBasePageElements`
- `flag` -> extends `FlagBasePageElements`

**See guidelines.md** for the complete code template and inheritance patterns.

### Step 6: Generate Page Object File

**Todo:** Mark "Generate webelements file" as `completed`, mark "Generate page object file" as `in_progress`

Generate the page object class extending the webelements class. Add action methods (verb-first naming: `click*`, `input*`, `select*`) and verification methods (`verify*` prefix).

**Rules:**
- Extend the webelements class (inheritance) — NOT the base page class
- All methods return `this` for chaining (fluent interface)
- No direct `cy.get()` or `cy.getDataTestSection()` calls — use inherited selector methods
- Use `shouldBeVisible()` custom command for visibility checks
- Import path must be relative and correct for the file location

**See guidelines.md** for the complete code template and method patterns.

### Step 7: Present to User

**Todo:** Mark "Generate page object file" as `completed`, mark "Present files to user" as `in_progress`

1. **Show the generated files** with full content
2. **Show summary table** of all elements mapped
3. **Ask for confirmation** via AskUserQuestion:
   - **"Keep files as-is" (Recommended)** — files are already written to the codebase
   - **"Edit first"** — let user suggest changes before finalizing
   - **"Run lint"** — run `npm run lint:fix` to ensure files pass linting
4. **Report:**
   ```
   Page objects created
     - Webelements: cypress/pages/webelements/{product}/{ClassName}Elements.js
     - Page object: cypress/pages/{product}/{ClassName}.js
     - Elements: {N} selectors
     - Methods: {M} action + {K} verification methods

   Usage example:
     import {ClassName} from '../../pages/{product}/{ClassName}';
     const page = new {ClassName}();
     page.click{Element}().verify{Element}IsVisible();
   ```

**Todo:** Mark "Present files to user" as `completed`

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, Notes, code templates, and detailed classification tables are in guidelines.md to reduce auto-loaded context size.
