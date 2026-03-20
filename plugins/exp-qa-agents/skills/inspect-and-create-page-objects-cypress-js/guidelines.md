# Inspect and Create Page Objects (Cypress JS) - Guidelines

## Detailed Workflow Instructions

### Step 2: Extract data-test-section Attributes - JavaScript Template

**Complete JavaScript code for browser_evaluate:**

```javascript
browser_evaluate({
  function: `() => {
    const allElements = document.querySelectorAll('[data-test-section]');
    const results = [];
    allElements.forEach(el => {
      const tag = el.tagName.toLowerCase();
      const text = el.textContent.trim().substring(0, 50);
      const testSection = el.getAttribute('data-test-section');
      const classes = el.className ? el.className.toString().substring(0, 80) : '';
      results.push({ tag, testSection, text, classes });
    });
    return {
      totalDataTestSections: results.length,
      relevantElements: results.filter(r =>
        // Filter for elements related to the feature being inspected
        r.text.includes('{FEATURE_KEYWORD}') ||
        r.testSection.includes('{feature_keyword}') ||
        r.testSection.includes('dialog') ||
        r.testSection.includes('modal')
      )
    };
  }`
})
```

**Filtering strategy:**
- Replace `{FEATURE_KEYWORD}` with the actual feature name or UI text to filter by
- Adjust filter logic based on what you're inspecting (dialog, page section, etc.)
- If results are still too large, extract by container scope instead of full page

### Step 3: Analyze Existing Patterns - Background Agent Instructions

**Complete agent prompt:**

```
Agent({
  description: "Analyze existing page object patterns for {Feature}",
  subagent_type: "Explore",
  run_in_background: true,
  prompt: `
Analyze existing page object patterns for creating a {Feature} page object in the {Product} area.

Tasks:
1. Check if page objects already exist for this feature:
   - Glob: cypress/pages/webelements/{product}/**/{Feature}*
   - Glob: cypress/pages/{product}/**/{Feature}*
   - If found, read them and return list of existing elements (so only NEW ones are added)

2. Read the base classes to understand inheritance:
   - cypress/pages/webelements/common/CommonBasePageElements.js
   - cypress/pages/webelements/{product}/{ProductBase}PageElements.js (if product is web/flag)
   - cypress/pages/common/CommonBasePage.js

3. Check for similar dialog/modal page objects to understand patterns:
   - Glob: cypress/pages/**/*[Dd]ialog*
   - Glob: cypress/pages/**/*[Mm]odal*
   - Read 2-3 examples to understand structure

4. Return structured summary:
   - Existing elements: [list of element names already defined]
   - Base class methods: [inherited methods available]
   - Dialog patterns: [common patterns from similar files]
   - Recommended structure: [guidance based on analysis]
`
})
```

### Step 4: Element Classification Table

| Category | Element Types | Naming Suffix | Example Method Name |
|----------|--------------|---------------|---------------------|
| Buttons | button, submit, link-as-button | `Btn` | `saveBtn()`, `cancelBtn()` |
| Links | anchor, navigation links | `Link` | `documentationLink()`, `helpLink()` |
| Inputs | text input, textarea, number | `Input` / `Textarea` | `nameInput()`, `descriptionTextarea()` |
| Selects | dropdown, select, combobox | `Select` / `Dropdown` | `categorySelect()`, `statusDropdown()` |
| Checkboxes | checkbox, toggle, switch | `Checkbox` / `Toggle` | `enabledCheckbox()`, `activeToggle()` |
| Dialogs | modal, dialog, popup | `Dialog` / `Modal` / `Popup` | `confirmationDialog()`, `settingsModal()` |
| Containers | form, section, card, panel | `Form` / `Section` / `Card` | `filtersSection()`, `detailsCard()` |
| Tabs | tab, tabpanel | `Tab` | `settingsTab()`, `overviewTab()` |
| Labels | heading, label, text display | `Title` / `Label` / `Text` | `pageTitle()`, `errorLabel()` |
| Icons | close icon, action icon | `Icon` | `closeIcon()`, `editIcon()` |

**Selector priority (from most stable to least stable):**

1. `data-test-section` attribute -> use `cy.getDataTestSection()`
2. `data-test-section` on parent + `.findDataTestSection()` for child
3. `data-testid` attribute -> use `cy.get('[data-testid="..."]')`
4. Unique `id` attribute -> use `cy.get('#id')` or `.find('#id')`
5. **Scoped `cy.contains('tag', 'text')` within parent** -> for elements with generic/undefined `data-test-section`
6. Unique CSS class -> use `cy.get('.class-name')`

**Never use:**
- XPath selectors
- Positional selectors (`:nth-child`) unless no alternative exists
- Unscoped `cy.contains()` for elements with generic `data-test-section` values

### Step 5: Webelements File - Complete Code Template

```javascript
import {ProductBase}PageElements from '../{relative-path}/{ProductBase}PageElements';

export default class {ClassName}Elements extends {ProductBase}PageElements {
  //#region {Section Name}

  // Simple data-test-section selector
  {elementName}(options) {
    return cy.getDataTestSection('{selector-value}', options);
  }

  // Nested element (find within parent using data-test-section)
  {childElement}(options) {
    return this.{parentElement}().findDataTestSection('{child-selector}', options);
  }

  // Nested element using CSS selector
  {nestedElement}(options) {
    return this.{parentElement}(options).find('#{css-selector}');
  }

  // Text-based selector scoped to parent (for elements with generic data-test-section)
  {linkElement}(options) {
    return this.{parentContainer}(options).contains('a', '{Link Text}');
  }

  // Element with data-testid (fallback when no data-test-section)
  {testIdElement}(options) {
    return cy.get('[data-testid="{testid-value}"]', options);
  }

  //#endregion

  //#region {Another Section}

  // Group related elements by section/feature area
  {anotherElement}(options) {
    return cy.getDataTestSection('{another-selector}', options);
  }

  //#endregion
}
```

**Import path examples by product area:**

| Product | Webelements Class | Import Path |
|---------|------------------|-------------|
| `common` (direct folder) | `CommonBasePageElements` | `import CommonBasePageElements from './CommonBasePageElements';` |
| `web` (direct folder) | `WebBasePageElements` | `import WebBasePageElements from '../web/WebBasePageElements';` |
| `web` (feature subfolder, e.g., `visual_editor/`) | `WebBasePageElements` | `import WebBasePageElements from '../../web/WebBasePageElements';` |
| `flag` (direct folder) | `FlagBasePageElements` | `import FlagBasePageElements from '../flag/FlagBasePageElements';` |
| `flag` (feature subfolder) | `FlagBasePageElements` | `import FlagBasePageElements from '../../flag/FlagBasePageElements';` |

**Webelements rules:**
- One method per element, accepting optional `options` parameter
- No action logic — only return element references
- Use `#region` / `#endregion` comments to group related selectors
- Pass `options` through to Cypress commands for timeout overrides
- Never put action methods in webelements — they belong in the page object class

### Step 6: Page Object File - Complete Code Template

```javascript
import {ClassName}Elements from '../webelements/{product}/{ClassName}Elements';

export default class {ClassName} extends {ClassName}Elements {
  //#region {Section Name}

  // Action methods (verb-first naming)
  click{ElementName}() {
    this.{elementName}().click();
    return this;
  }

  input{FieldName}(value) {
    this.{fieldInput}().clear().type(value);
    return this;
  }

  select{OptionName}(value) {
    this.{selectElement}().select(value);
    return this;
  }

  toggle{CheckboxName}() {
    this.{checkboxElement}().click();
    return this;
  }

  open{DialogName}() {
    this.{triggerElement}().click();
    return this;
  }

  close{DialogName}() {
    this.{closeBtn}().click();
    return this;
  }

  // Verification methods (verify prefix)
  verify{ElementName}IsVisible() {
    this.{elementName}().shouldBeVisible();
    return this;
  }

  verify{ElementName}IsNotDisplayed() {
    this.{elementName}().should('not.exist');
    return this;
  }

  verify{ElementName}HasText(expectedText) {
    this.{elementName}().shouldHaveText(expectedText);
    return this;
  }

  verify{ElementName}IsDisabled() {
    this.{elementName}().shouldBeDisabled();
    return this;
  }

  verify{ElementName}IsEnabled() {
    this.{elementName}().shouldBeEnabled();
    return this;
  }

  // Compound verification methods (verify multiple elements at once)
  verifyAll{Section}LinksAreVisible() {
    this.{link1}().shouldBeVisible();
    this.{link2}().shouldBeVisible();
    this.{link3}().shouldBeVisible();
    return this;
  }

  verify{Dialog}IsOpen() {
    this.{dialogContainer}().shouldBeVisible();
    this.{dialogTitle}().shouldBeVisible();
    return this;
  }

  //#endregion

  //#region Composed Page Objects (Optional)

  // Only add constructor if you need to interact with other page objects
  constructor() {
    super();
    this.otherPage = new OtherPage();
  }

  navigateTo{OtherPage}() {
    this.{navigationLink}().click();
    this.otherPage.verify{Element}IsVisible();
    return this.otherPage;
  }

  //#endregion
}
```

**Import path examples:**

| Webelements Location | Page Object Import |
|---------------------|-------------------|
| `cypress/pages/webelements/common/HelpCenterDialogElements.js` | `import HelpCenterDialogElements from '../webelements/common/HelpCenterDialogElements';` |
| `cypress/pages/webelements/web/AudiencesPageElements.js` | `import AudiencesPageElements from '../webelements/web/AudiencesPageElements';` |
| `cypress/pages/webelements/web/visual_editor/BottomBarElements.js` | `import BottomBarElements from '../webelements/web/visual_editor/BottomBarElements';` |

**Page object rules:**
- Extend the webelements class (NOT the base page class)
- All methods return `this` for chaining (fluent interface)
- Action methods: `click*`, `input*`, `select*`, `open*`, `close*`, `toggle*`
- Verification methods: `verify*` prefix
- Use `shouldBeVisible()` custom command (not `.should('be.visible')`)
- No direct `cy.get()` or `cy.getDataTestSection()` calls — use inherited selector methods
- Only add constructor with composed page objects if actually needed

---

## Quality Guidelines

### Selector Priority

Always prefer selectors in this order (most stable to least stable):

1. `data-test-section` -> `cy.getDataTestSection('name')`
2. `data-test-section` on parent + `.findDataTestSection('child')` -> nested lookup
3. `data-testid` -> `cy.get('[data-testid="name"]')`
4. Unique `id` attribute -> `cy.get('#id')`
5. Unique CSS class -> `cy.get('.class-name')`
6. Text content scoped to parent -> `this.parentContainer().contains('tag', 'text')` (last resort)

Never use XPath selectors. Never use positional selectors (`:nth-child`) unless no alternative exists.
Never use unscoped `cy.contains()` for elements with generic `data-test-section` values like `undefined-link`.

### Critical: Always Use browser_evaluate for Selector Extraction

**The `browser_snapshot()` accessibility tree does NOT show `data-test-section` attributes.** You MUST use `browser_evaluate` to run JavaScript on the page and extract all `data-test-section` values from the DOM.

Without this step, you will:
- Miss proper `data-test-section` selectors
- Fall back to fragile selectors unnecessarily
- Generate page objects that don't match the project's conventions

**Example:**
```javascript
browser_evaluate({
  function: `() => {
    const elements = document.querySelectorAll('[data-test-section]');
    return Array.from(elements).map(el => ({
      tag: el.tagName.toLowerCase(),
      testSection: el.getAttribute('data-test-section'),
      text: el.textContent.trim().substring(0, 50),
      classes: el.className.toString().substring(0, 80)
    }));
  }`
})
```

### Handling Generic data-test-section Values

Some elements have generic/shared `data-test-section` values like `undefined-link` that match multiple elements. For these:

```javascript
// BAD - matches multiple elements on the page
knowledgeBaseLink() {
  return cy.getDataTestSection('undefined-link');
}

// GOOD - scoped to parent container, unique match
knowledgeBaseLink(options) {
  return this.supportDialog(options).contains('a', 'Knowledge Base');
}
```

### Playwright MCP Threading Rules

**CRITICAL:** Playwright MCP tools (`browser_navigate`, `browser_click`, `browser_snapshot`, `browser_evaluate`, `browser_fill_form`, `browser_take_screenshot`) can ONLY be used in the main thread.

- Do NOT delegate browser interactions to background Agents
- Only the codebase analysis (Glob, Grep, Read) can run in background Agents
- Handle login flow in the main thread before launching background analysis

### File Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Webelements file | PascalCase + `Elements` suffix | `AudiencesPageElements.js`, `HelpCenterDialogElements.js` |
| Page object file | PascalCase (no suffix required, but `Page`/`Dialog` descriptors OK) | `AudiencesPage.js`, `HelpCenterDialog.js` |
| Directory | snake_case | `visual_editor/`, `experiment_details/` |
| Class name | PascalCase | `VisualEditorBottomBar`, `HelpCenterDialog` |
| Method name | camelCase | `clickSaveButton`, `verifyHelpCenterIsDisplayed` |

### File Placement

- **Feature with multiple page objects** -> use feature subfolder: `cypress/pages/{product}/{feature}/`
- **Standalone dialog/popup** -> place directly in product folder: `cypress/pages/{product}/`
- **Cross-product dialog** -> use `common` folder: `cypress/pages/common/`

### Inheritance by Product Area

| Product | Webelements Base | Import Path |
|---------|-----------------|-------------|
| `common` | `CommonBasePageElements` | `./CommonBasePageElements` |
| `web` | `WebBasePageElements` | `../web/WebBasePageElements` or relative |
| `flag` | `FlagBasePageElements` | relative path to Flag base |

### Best Practices

- Webelements classes contain ONLY selector methods -- no action logic
- Page object classes extend webelements and add action/verification methods
- All page object methods return `this` for fluent chaining
- Use `#region` / `#endregion` comments to group related selectors
- Check for existing page objects before creating new ones to avoid duplication
- When updating existing files, add only NEW elements; do not duplicate existing ones
- Verify the inheritance chain matches the product area (Web, Flag, Common)
- Use `shouldBeVisible()` custom command (not `.should('be.visible')`) for verification methods
- Use `should('not.exist')` for verifying elements are not displayed (this is standard Cypress)
- Only add a constructor with composed page objects if actually needed

### Anti-Patterns

- Do NOT put `cy.get()` or `cy.getDataTestSection()` calls directly in page object action methods -- use inherited selector methods
- Do NOT combine multiple actions in a single method unless they are always performed together
- Do NOT use hard-coded waits (`cy.wait(5000)`) in page objects -- use Cypress assertions instead
- Do NOT create page objects for elements that already exist in a parent class
- Do NOT skip the `browser_evaluate` step -- always extract `data-test-section` attributes via JS
- Do NOT skip the browser inspection step -- always verify selectors against the live page
- Do NOT use generic method names like `clickButton()` -- be specific: `clickSaveButton()`
- Do NOT use unscoped `cy.contains()` for elements with generic `data-test-section` values
- Do NOT delegate Playwright MCP calls to background Agents -- they only work in the main thread
- Do NOT rely solely on `browser_snapshot()` for selector discovery -- it misses `data-test-section` attributes

### Verification Checklist

Before presenting generated files to the user:
- [ ] All selectors verified against `browser_evaluate` results (not just snapshot)
- [ ] No duplicate elements with existing page objects
- [ ] Inheritance chain is correct for the product area
- [ ] All methods return `this`
- [ ] Naming conventions are followed consistently
- [ ] Elements with generic `data-test-section` use scoped `contains()` instead
- [ ] Import paths are correct and relative
- [ ] Screenshot taken showing the inspected state

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Get target URL and page context from user", status: "in_progress", activeForm: "Getting target URL" },
  { content: "Navigate, login, and inspect page elements", status: "pending", activeForm: "Navigating and inspecting" },
  { content: "Extract data-test-section attributes via JS evaluation", status: "pending", activeForm: "Extracting selectors" },
  { content: "Analyze existing patterns in codebase (background)", status: "pending", activeForm: "Analyzing patterns" },
  { content: "Identify and classify elements", status: "pending", activeForm: "Classifying elements" },
  { content: "Generate webelements file", status: "pending", activeForm: "Generating webelements" },
  { content: "Generate page object file", status: "pending", activeForm: "Generating page object" },
  { content: "Present files to user for review", status: "pending", activeForm: "Presenting for review" }
])
```

**Todo Update Rules:**
- Only ONE task `in_progress` at a time
- Mark `completed` immediately when done
- Mark `in_progress` on the next task right after
- On failure: keep task `in_progress`, add new task for resolution
- On cancel: mark remaining as `completed` with note

---


## Error Handling

| Error | Action |
|-------|--------|
| Playwright MCP not available | Exit with error: "Playwright MCP is not configured. See .mcp.json.template for detailed configuration." |
| Page requires login | Fill login form with provided credentials, or ask user for credentials via AskUserQuestion |
| Snapshot too large (exceeds token limit) | Use `browser_evaluate` to extract elements via JS instead of relying on snapshot. Use `browser_take_screenshot` for visual context |
| No interactive elements found | Take screenshot, ask user to point out elements or click to reveal them |
| Page object files already exist | Read existing, show only NEW elements to add |
| Elements lack data-test-section | Use fallback selectors (scoped contains, id, class), note in output |
| `browser_evaluate` returns too many elements | Filter results by feature keyword or container scope |
| Login timeout | Retry once, then ask user to verify credentials |

---


## Self-Correction

1. **"Inspect a different section"** -> Navigate/click to new section, re-run `browser_evaluate`
2. **"Wrong selector for element X"** -> Update selector, re-present
3. **"Add methods for element Y"** -> Add action/verification methods
4. **"Merge with existing page object"** -> Read existing file, add only new elements/methods
5. **"Use different class name"** -> Rename class and files accordingly
6. **"Selector matches multiple elements"** -> Scope to parent container using `this.{parent}().contains()`

---


## Notes

### Selector Priority

Always prefer selectors in this order (most stable to least):

1. `data-test-section` -> `cy.getDataTestSection('name')`
2. `data-test-section` on parent + `findDataTestSection('child')` -> nested lookup
3. `data-testid` -> `cy.get('[data-testid="name"]')`
4. `id` attribute -> `cy.get('#name')` or `.find('#name')`
5. Scoped `this.{parent}().contains('tag', 'text')` -> text-based within container
6. Unique CSS class -> `cy.get('.class-name')`

**IMPORTANT:** Never use unscoped `cy.contains()` for elements with generic `data-test-section` values like `undefined-link`. Always scope to a parent container to avoid matching multiple elements.

### Inheritance Chain

```
CommonBasePageElements
  -> WebBasePageElements / FlagBasePageElements
    -> FeatureElements (selectors only)
      -> FeaturePage (actions + verification)
```

For `common` product area:
```
CommonBasePageElements
  -> FeatureElements (selectors only)
    -> FeaturePage (actions + verification)
```

### File Naming

| Convention | Example |
|------------|---------|
| Webelements file | `AudiencesPageElements.js` or `HelpCenterDialogElements.js` |
| Page object file | `AudiencesPage.js` or `HelpCenterDialog.js` |
| Directory | snake_case (`visual_editor/`, `experiment_details/`) |
| Class name | PascalCase (`VisualEditorBottomBar`, `HelpCenterDialog`) |
| Method name | camelCase (`clickSaveButton`, `verifyHelpCenterIsDisplayed`) |

### Key Custom Commands

| Command | Usage |
|---------|-------|
| `cy.getDataTestSection(selector, options)` | Get element by `data-test-section` attribute |
| `.findDataTestSection(selector, options)` | Find within existing element (chainable) |
| `cy.getMultipleDataTestSections(...selectors)` | Get multiple selectors with OR logic |
| `.shouldBeVisible()` | Custom assertion for visibility |
| `.shouldHaveText(text)` | Custom assertion for text content |
| `.shouldBeDisabled()` / `.shouldBeEnabled()` | Custom assertions for button state |
