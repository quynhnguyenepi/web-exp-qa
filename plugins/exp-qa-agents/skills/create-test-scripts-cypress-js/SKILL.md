---
description: Generate Cypress test scripts from JIRA tickets containing test cases. Full automation from ticket to test scripts with lint and test execution.
---

## Dependencies

- **MCP Servers (required):** Atlassian
- **MCP Servers (optional):** Context7 (Cypress API docs lookup for code review)
- **Sub-Skills (required):** `/common-qa:read-jira-context`, `/common-qa:create-branch`, `/common-qa:read-repo-docs`
- **Sub-Skills (optional):** `/common-qa:update-claude`, `/exp-qa-agents:inspect-and-create-page-objects-cypress-js`
- **Related Skills:** `/exp-qa-agents:create-test-cases`, `/exp-qa-agents:create-pr`, `/exp-qa-agents:review-github-pr-cypress-js`, `/exp-qa-agents:execute-test-case`

You are a QA test automation agent.
Domain: cypress-test-generation
Mode: orchestrator
Tools: Read, Write, Bash, Grep, Glob, TodoWrite, AskUserQuestion, Agent

Agent that generates Cypress test script files from JIRA tickets. Reads test cases, analyzes codebase patterns, generates spec files with page objects and builders, runs lint and tests.

**After completion, use `/exp-qa-agents:create-pr` to commit, create PR, and update JIRA.**

## Workflow

1. **Pre-flight:** Verify Atlassian MCP, validate ticket ID, check git clean, verify `gh` auth, check node_modules
2. **Read JIRA task DIRECTLY (not via Agent):**
   - Call `mcp__atlassian__jira_get_issue` with `fields: "summary,status,description,labels,components,issuetype,priority,assignee,reporter,parent,issuelinks,attachment,customfield_10014"`, `expand: "renderedFields"`, `comment_limit: 20`
   - Call `mcp__atlassian__jira_get_issue` with `fields: "issuelinks,parent"` to get linked Test tickets
   - **Follow the reference chain:** The automation ticket description may reference other ticket IDs (e.g., "automate CJS-10590"). Fetch those referenced tickets too — they contain the actual test cases.
   - **Do NOT use Agent for read-jira-context** -- it's 2-3 direct MCP calls
3. **Read & parse test cases:** Fetch each linked/referenced test case, parse, group by module (max 5 per spec)
   - **If test case has no description:** The test steps may be in proforma forms or only visible in the JIRA UI. Ask the user to provide a screenshot of the test steps.
   - **Parameterized test data:** If test steps contain `@variable=value1, @variable=value2` patterns, plan for data-driven tests using `forEach` with test data arrays.
4. **Sync code & create branch:** Invoke `/common-qa:create-branch` with the ticket ID to checkout default branch, pull latest, and create `{username}/{TICKET_ID}-{kebab-case-title}`
5. **Analyze codebase — Agent 1 (background) + direct calls (main thread):**
   - **Agent 1 (background):** Run `/common-qa:update-claude` + `/common-qa:read-repo-docs` to sync CLAUDE.md and fetch project docs. This is a multi-step workflow that benefits from Agent dispatch. Set `run_in_background: true` and `model: "haiku"`.
   - **Main thread (direct, while Agent 1 runs):** Use Glob and Grep directly to:
     - **Reference scripts in the same folder AND its smoke/regression counterpart (CRITICAL):**
       - If target is `regression/visual_editor/campaign/`, also check `smoke_suite/visual_editor/campaign/`
       - If target is `smoke_suite/visual_editor/ab_test/`, also check `regression/visual_editor/ab_test/`
       - Read 2-3 reference scripts from these folders to understand setup patterns, page object usage, and test flow
     - Find similar tests: `Glob("cypress/e2e/**/*.js")` + `Grep("describe.*{feature}", type: "js")`
     - Identify page objects: `Glob("cypress/pages/**/*.js")` + `Glob("cypress/pages/webelements/**/*.js")`
     - Identify builders + API commands: `Glob("cypress/support/builders/**/*.js")` + `Glob("cypress/support/commands/**/*.js")`
   - **Do NOT use Agent for codebase searches** -- Glob/Grep/Read are direct tools that don't need agent overhead
6. **Check page objects:** Before generating test scripts, verify required page objects exist:
   - Search `cypress/pages/` and `cypress/pages/webelements/` for needed page objects
   - If a page object is missing OR an existing page object is missing elements needed by the test:
     - **Ask user via AskUserQuestion** for the steps to navigate to the page/component that needs a new POM (e.g., "Go to Experiments > click Create New > select A/B Test")
     - **Default login credentials (RC):**
       - URL: `https://rc-app.optimizely.com/signin`
       - Email: `bdd+test1752566905289@optimizely.com`
       - Password: `asdfASDF1`
     - Ask user to confirm or override these credentials before proceeding
     - Invoke `/exp-qa-agents:inspect-and-create-page-objects-cypress-js` with the target URL, credentials, and navigation steps to inspect the page and generate the missing page object/elements
   - Do NOT use `cy.get('TODO')` in spec files -- always ensure page objects have proper selectors first
7. **Determine target folder based on JIRA labels (CRITICAL):**
   - Check the **test case ticket** labels (NOT the automation ticket labels)
   - If labels contain `smoke_suite` or `smoke` → place spec in `cypress/e2e/{product}/smoke_suite/` folder
   - If labels do NOT contain smoke → place spec in `cypress/e2e/{product}/regression/` folder
   - **Tags must match the folder:**
     - `smoke_suite/` tests: use `CommonTag.smoke_ve` (or similar smoke tags) in the tags array
     - `regression/` tests: do NOT include smoke tags, use product-specific tags only (e.g., `[WebTag.web, WebTag.new_ve]`)
   - Check existing tests in the target folder to confirm the tag pattern used
8. **Generate test scripts IN PARALLEL using Agent tool (if multiple specs):**
   - Group test cases by module (max 5 per spec file)
   - If multiple spec files needed, launch one Agent per spec file with `run_in_background: true` and `model: "sonnet"`
   - Each agent receives: test cases for that spec, codebase context from step 5, page objects from step 6, coding conventions
   - Each agent generates one complete spec file independently
   - If only one spec file, generate directly without sub-agent
   - **Data-driven tests:** When test steps have parameterized data (e.g., `@rearrange=Before/After/Prepend/Append`), use `forEach` with a test data array to generate multiple `it()` blocks from one test case
9. **Lint & code review:**
   - Run `npm run lint:fix`, check for `.only()`/`.pause()`
   - **Cypress API validation via Context7 (if available):**
     1. Resolve library: `mcp__context7__resolve-library-id({ query: "Cypress API", libraryName: "cypress" })` → use `/cypress-io/cypress-documentation`
     2. For each Cypress command used in generated specs (e.g., `cy.intercept`, `cy.get`, `cy.request`, `.should`), validate usage against official docs:
        ```
        mcp__context7__query-docs({
          libraryId: "/cypress-io/cypress-documentation",
          query: "How to use cy.{command} with correct syntax and options"
        })
        ```
     3. Check for: deprecated APIs, incorrect argument order, missing assertions, anti-patterns (e.g., `cy.wait(5000)` instead of proper aliasing)
     4. If Context7 is not available, skip this step (not a blocker)
   - Present generated code to user for review
10. **Run tests:** `npx cypress run --config ... --spec ... --browser=chrome`, fix & re-run (max 3)

**See guidelines.md** for Coding Conventions Reference (naming conventions, code structure rules, AI-generated code tracking, region organization, linting rules). Also read `.claude/docs/coding-conventions.md` from the target repo.

## Cypress Run

**RC:** `npx cypress run --config 'baseUrl=https://rc-app.optimizely.com,retries=2,watchForFileChanges=false' --env '...' --spec {PATHS} --browser=chrome`

**See guidelines.md** for Failure Recovery Per Step table (checkpoint mechanism) and Folder Placement Rules (label-to-folder mapping, tag verification).

## VE Test Splitting Rules

Visual Editor tests that involve both Preview and Start/Publish can be handled in two ways:

### Option 1: Split into separate spec files
Use when Preview and Start have **different setup or different VE changes**. The snippet cannot be changed within the same `it()` block.

| Spec File | Covers | Naming |
|-----------|--------|--------|
| Preview spec | VE changes + verify in VE iframe preview | `{feature}_ve_{action}.spec.js` |
| Start check spec | VE changes + start experiment + verify on live website | `{feature}_ve_{action}_start_check.spec.js` |

**Example:**
- `campaign_ve_rearrange_element.spec.js` — Apply rearrange in VE, verify element position in VE preview
- `campaign_ve_rearrange_element_start_check.spec.js` — Apply rearrange, start experiment, verify on live website

### Option 2: Use `[false, true].forEach` in one spec file (PREFERRED when applicable)
Use when Preview and Visit site share the **same setup and VE changes** but diverge only at the verification step. Each `forEach` iteration creates a separate `it()` with its own `beforeEach`/`afterEach` lifecycle, so the snippet issue doesn't apply.

```javascript
[false, true].forEach(function (isPreview) {
  const testType = isPreview ? 'Preview' : 'Visit site';

  it(`[TICKET-ID] Campaign, VE - ${testType} description`, function () {
    // ... shared VE setup and changes ...

    if (isPreview) {
      // Preview flow: open preview window, verify changes
      cy.openNewWindow();
      cy.waitForPreviewUI();
      webLeftSideBar.clickPreviewPage();
      cy.visitPreviewFromWindowOpen(variationId);
      exampleWebsitePage.verifyVariationHaveCSS(...);
    } else {
      // Visit site flow: publish, wait for CDN, verify on live
      cy.interceptCommitLayer(this.layerId);
      webLeftSideBar.publishExperimentOnly(name, type);
      cy.waitForCommitLayer().then((rev) => { cy.waitForCDNUpload(rev); });
      exampleWebsitePage.visitAfterPublishChange().verifyVariationHaveCSS(...);
    }
  });
});
```

**When to use which:**
- Same VE changes, different verification → **Option 2** (one spec, `forEach`)
- Different VE changes or setup → **Option 1** (separate specs)

## Explicit UI Step Matching

**CRITICAL:** When test case steps describe explicit UI interactions, do NOT use bundled helper methods (e.g., `inputElementChangeDetails`). Instead, call individual page object methods to match each test step exactly.

**Use method chaining** to group related actions together (page objects return `this`):
```javascript
// DON'T: Bundle everything into one call (hides steps)
elementChangeManagerDialog.inputElementChangeDetails(changeRearrange);

// DON'T: Separate calls on the same page object without chaining
visualEditorBottomBar.selectPageByUrlFragment(URIs.optimizelyExampleReservationUriNoParam);
visualEditorBottomBar.verifyBottomBarVisible();

// DO: Chain consecutive calls on the same page object
visualEditorBottomBar
  .selectPageByUrlFragment(URIs.optimizelyExampleReservationUriNoParam)
  .verifyBottomBarVisible();

// DO: Chain related actions, group by test step
elementChangeManagerDialog
  .toggleLayout()
  .clickShowElement()
  .selectRearrangeOption(rearrangeCase.option);       // Step 5: Select @rearrange

elementChangeManagerDialog
  .inputRearrangeSelector(targetSelector)
  .clickRearrangeSearchSelectorButton()               // Step 6: Click magnifying glass
  .selectRearrangePosition(position);                 // Step 7: Select position

visualEditorPage.verifySaveChangesSuccess();          // Step 8: Save
```

## Element vs Page Object Separation

**Methods with direct element selectors (`.find()`, `.not()`, CSS selectors) belong in `...Elements.js`, NOT in `...Page.js`.**

```javascript
// DON'T: Put element-level logic in Page.js
// targetingPage.js
verifyTargetingListPageCount(count) {
  this.targetingList()
    .find('li.oui-dropdown__item')
    .not(':contains("Edit Targeting")')
    .should('have.length', count);
  return this;
}

// DO: Put element-level logic in Elements.js, compose in Page.js
// targetingElements.js
targetingListItems() {
  return this.targetingList()
    .find('li.oui-dropdown__item')
    .not(':contains("Edit Targeting")');
}

// targetingPage.js
verifyTargetingListPageCount(count) {
  this.targetingListItems().should('have.length', count);
  return this;
}
```

**Rule:** If a method uses `.find()`, `.not()`, `.filter()`, `.children()`, `.closest()`, or raw CSS selectors to locate sub-elements — it belongs in `Elements.js`. `Page.js` methods should only call element methods and add assertions/actions.

## Data-Driven Test — Initial Run Strategy

When generating data-driven tests with multiple test cases, **only enable the first test case** initially. Comment out the rest for faster debugging:

```javascript
const rearrangeTestCases = [
  {
    name: 'Before',
    option: CommonEnumUtils.PositionEnum.BEFORE.upperCase,
    verifyPosition: CommonEnumUtils.PositionEnum.BEFORE.lowerCase,
  },
  // {
  //   name: 'After',
  //   option: CommonEnumUtils.PositionEnum.AFTER.upperCase,
  //   verifyPosition: CommonEnumUtils.PositionEnum.AFTER.lowerCase,
  // },
  // ... uncomment after first case passes
];
```

## Campaign Test Patterns

When generating tests for **Personalization Campaign** experiments:

| Pattern | Correct | Incorrect |
|---------|---------|-----------|
| Experience setup | `new Experience()` (single, no name) | `new Experience('Experience 1')` with multiple experiences |
| Start experiment | `webLeftSideBar.startAnExperiment(name, referenceData.experimentTypes.personalizationCampaign.lowerCase)` | `webLeftSideBar.startACampaign(name)` |
| Holdback | `.setHoldback(500)` (5%) | Omitting holdback |

Always check reference scripts in the same campaign folder to verify the correct method signatures.

## Data-Driven Test Pattern

When test steps contain parameterized data (e.g., `@rearrange=Before, @Rearrange=After, @Rearrange=At the beginning of`), generate data-driven tests:

```javascript
const testCases = [
  { name: 'Before', option: CommonEnumUtils.PositionEnum.BEFORE.upperCase, ... },
  { name: 'After', option: CommonEnumUtils.PositionEnum.AFTER.upperCase, ... },
];

describe('Feature', { tags: [...] }, function () {
  testCases.forEach(function (testCase) {
    describe(`Sub-feature ${testCase.name}`, function () {
      beforeEach(function () { /* setup */ });
      afterEach(function () { /* cleanup */ });
      it(`[TICKET-ID] Test description ${testCase.name}`, function () { /* test */ });
    });
  });
});
```


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
