# Cypress Test Script Generation Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## 1. Test Script Templates

### Web Test Template

```javascript
/* eslint-disable no-undef */
import ExperimentListPage from '../../../../../pages/web/optimizations/ExperimentListPage';
import ExperimentBuilder from '../../../../../support/builders/web/experiment/experimentBuilder';
import PageBuilder from '../../../../../support/builders/web/pageBuilder';
import WebMetricBuilder from '../../../../../support/builders/web/experiment/metricBuilder';
import CommonTag, { WebTag } from '../../../../../support/resources/tagList';
import referenceData from '../../../../../support/resources/web/referenceData.json';

const experimentListPage = new ExperimentListPage();
const examplePage = new PageBuilder().examplePage();

describe(
  'Feature Description',
  {
    testIsolation: false,
    tags: [WebTag.web, WebTag.campaign_ab, CommonTag.experiment_detail],
  },
  function () {
    //#region Setup Test Data
    before(function () {
      cy.createAccount(Cypress.env('web_account'))
        .saveGeneratedTimeBasedIdAs('expName')
        .then(function () {
          return cy.createAPageV1(examplePage);
        })
        .then(function (response) {
          cy.wrap(response.body.id).as('testPageId');
          const experiment = new ExperimentBuilder(
            referenceData.experimentType.abTesting,
            this.expName
          )
            .setUrl('www.optimizely.com')
            .build();
          return cy.createExperimentV1(experiment.layer, experiment.layerExperiment);
        });
    });
    //#endregion

    //#region Test Execution
    it('[TICKET-ID][Web][Module]_Description', function () {
      cy.visitProject();
      experimentListPage.openAnExperiment(this.expName);
      // Test interactions using page objects
    });
    //#endregion

    //#region Cleanup
    after(function () {
      cy.deleteAccount();
    });
    //#endregion
  }
);
```

### Flag Test Template

```javascript
/* eslint-disable no-undef */
import CommonBasePage from '../../../../pages/common/CommonBasePage';
import FlagsListPage from '../../../../pages/flag/flags/FlagsListPage';
import FlagsPage from '../../../../pages/flag/flags/FlagsPage';
import CommonTag, { FlagTag } from '../../../../support/resources/tagList';

const commonBasePage = new CommonBasePage();
const flagsListPage = new FlagsListPage();
const flagsPage = new FlagsPage();

describe(
  'Feature Description',
  { tags: [FlagTag.flags, CommonTag.smoke_suite, CommonTag.variations] },
  function () {
    beforeEach(function () {
      cy.createFlagsAccount()
        .saveGeneratedTimeBasedIdAs('flagName')
        .then(function () {
          cy.createFlag(this.flagName);
        })
        .then(() => {
          cy.visitProject();
          commonBasePage.waitForTableLoadSpinnerDisappear();
          flagsListPage.openAFlag(this.flagName);
        });
    });

    afterEach(function () {
      cy.deleteAccount();
    });

    it('[TICKET-ID][Flag][Module]_Description', function () {
      // Test interactions using page objects
    });
  }
);
```

---

## 2. Import Path Depth Calculation

Import paths are RELATIVE. Count the number of directories from the project root to your spec file directory (= depth), then use `depth - 1` as the number of `../` to reach `cypress/`.

**Examples:**
- `cypress/e2e/web/smoke_suite/ve/spec.js` → depth 5 → **4** `../` → `../../../../pages/web/...`
- `cypress/e2e/web/regression/module/sub_module/spec.js` → depth 6 → **5** `../` → `../../../../../pages/web/...`

### Quick Reference by Depth

**Depth 6** (`cypress/e2e/web/regression/module/sub_module/`):
```javascript
import PageObject from '../../../../../pages/web/module/PageObject';
import ExperimentBuilder from '../../../../../support/builders/web/experiment/experimentBuilder';
import CommonTag, { WebTag } from '../../../../../support/resources/tagList';
```

**Depth 5** (`cypress/e2e/web/smoke_suite/module/` or `cypress/e2e/flag/smoke_suite/module/`):
```javascript
import PageObject from '../../../../pages/web/module/PageObject';
import ExperimentBuilder from '../../../../support/builders/web/experiment/experimentBuilder';
import CommonTag, { WebTag } from '../../../../support/resources/tagList';
```

---

## 3. Builder Usage Reference

### Web Builders

| Builder | Import Path | Common Methods |
|---------|-------------|----------------|
| `ExperimentBuilder` | `support/builders/web/experiment/experimentBuilder` | `constructor(type, name)`, `setUrl()`, `setMetrics()`, `setAudiences()`, `setOutlierFilterEnable()`, `setDescription()`, `setVariations()`, `build()` |
| `CampaignBuilder` | `support/builders/web/campaign/campaignBuilder` | `constructor(name)`, `setViewIds()`, `build()` |
| `PageBuilder` | `support/builders/web/pageBuilder` | `examplePage()`, `setPageName()`, `setPageDescription()`, `setPageUrl()`, `build()` |
| `WebMetricBuilder` | `support/builders/web/experiment/metricBuilder` | `clickMetric()`, `buildOverallRevenueEventMetricTotalRevenuePerVisitorIncrease()`, `build()` |
| `AudienceBuilder` | `support/builders/web/audienceBuilder` | `defaultAudience()`, `build()` |
| `VisualEditorBuilder` | `support/builders/web/visualEditorBuilder` | `constructor(selector)`, `setTypography()`, `setLayout()`, `build()` |

### Flag Builders

| Builder | Import Path | Common Methods |
|---------|-------------|----------------|
| `FlagBuilder` | `support/builders/flag/flagBuilder` | `constructor(name)`, `build()` |

### Builder Pattern Rules

- Constructor: Maximum 2 arguments
- From 3rd argument: Use setter methods
- Setter methods always return `this` for chaining
- Final `build()` method returns the constructed object
- Use convenience methods when available: `new PageBuilder().examplePage()`

---

## 4. Page Object Usage Reference

### Web Page Objects

| Page Object | Import Path | Common Methods |
|-------------|-------------|----------------|
| `ExperimentListPage` | `pages/web/optimizations/ExperimentListPage` | `openAnExperiment()`, `verifyExperimentRowIsDisplayed()`, `verifyExperimentNotDisplayed()` |
| `WebBasePage` | `pages/web/WebBasePage` | Base methods for web pages |
| `WebLeftSideBar` | `pages/web/experiment_details/WebLeftSideBar` | `openVariationMenu()`, `startAnExperiment()`, `clickStartExperimentAndCancel()`, `navigateToTrafficAllocationTab()` |
| `VariationsTab` | `pages/web/experiment_details/VariationsTab` | `addNewVariation()`, `stopAVariation()`, `restoreAVariation()`, `verifyVariationCount()`, `verifyVariationTrafficAllocation()` |
| `VisualEditorPage` | `pages/web/visual_editor/VisualEditorPage` | Visual editor interactions |
| `VisualEditorBottomBar` | `pages/web/visual_editor/VisualEditorBottomBar` | `verifyBottomBarVisible()` |

### Flag Page Objects

| Page Object | Import Path | Common Methods |
|-------------|-------------|----------------|
| `FlagsListPage` | `pages/flag/flags/FlagsListPage` | `openAFlag()` |
| `FlagsPage` | `pages/flag/flags/FlagsPage` | `openVariationsTab()`, `variationsTab` |
| `CommonBasePage` | `pages/common/CommonBasePage` | `waitForTableLoadSpinnerDisappear()` |

### Page Object Method Naming

| Type | Convention | Examples |
|------|-----------|---------|
| **Actions** | `{verb}{ElementName}` | `clickSaveButton()`, `inputEmailAddress()`, `selectStartDate()`, `uploadImage()` |
| **Verifications** | `verify{Condition}{ElementName}` | `verifySaveButtonVisible()`, `verifyErrorMessageDisplayed()`, `verifyVariationCount()` |

---

## 5. API Command Reference

### Account Commands

```javascript
// Web account
cy.createAccount(Cypress.env('web_account'));

// Flag account
cy.createFlagsAccount();

// Cleanup (both)
cy.deleteAccount();

// Login
cy.login(email, password);
```

### Web API Commands

```javascript
// Experiments
cy.createExperimentV1(layer, layerExperiment);
cy.createACampaignWithPageV1(campaign);
cy.addNewExperimentToCampaignV1(experiment, variations);

// Pages
cy.createAPageV1(page);

// Metrics
cy.createMetricV1(metric);

// Audiences
cy.createAudienceV1(audience);

// Campaign management
cy.publishCampaignV1(layer_id);
cy.updateCampaignV1(layer_id, updatePayload);

// Visual Editor
cy.addVariationToViewV1(experimentId, variationId, pageId, changeData);
```

### Flag API Commands

```javascript
// Flags
cy.createFlag(flagName);
cy.createVariation(variationName, flagName);

// Environments
cy.createEnvironment(environment);

// Rules
cy.createFlagRule(rule);

// Events
cy.createEvent(event);

// Projects
cy.createFlagsProject();
```

### Utility Commands

```javascript
// Navigation
cy.visitProject();

// Dynamic naming
cy.saveGeneratedTimeBasedIdAs('aliasName');

// Aliases
cy.wrap(value).as('aliasName');

// Spinners
cy.waitForSpinnerToDisappear();
cy.waitForTableLoadSpinnerDisplayed();

// Drag and drop
cy.dragAndDrop(sourceSelector, targetSelector);
```

---

## 6. File Path Decision Tree

```
Product = Web?
├── Is it a smoke test (core flow, critical path)?
│   └── cypress/e2e/web/smoke_suite/{module}/
├── Is it a regression test (detailed, edge cases)?
│   └── cypress/e2e/web/regression/{module}/{sub_module}/
└── Module examples:
    ├── visual_editor/    (VE tests)
    ├── ab_test/          (AB experiment tests)
    ├── campaign_p13n/    (Personalization tests)
    ├── account/          (Account management)
    └── experiments/      (General experiment tests)

Product = Flag?
├── cypress/e2e/flag/smoke_suite/{module}/
└── Module examples:
    ├── flag/             (Flag CRUD)
    ├── variations/       (Variation management)
    ├── rules/            (Delivery rules)
    ├── ab-testing/       (AB test rules)
    ├── environment/      (Environment settings)
    └── projects/         (Project management)

Product = Edge?
└── cypress/e2e/edge/{smoke_suite|regression}/{module}/
```

---

## 7. Common Pitfalls (Anti-Patterns)

### Must Use `function()` Not Arrow Functions

```javascript
// CORRECT
describe('Feature', function () {
  before(function () {
    cy.createAccount(Cypress.env('web_account'));
  });
  it('test', function () {
    // can access this.aliasName
  });
});

// WRONG - arrow functions lose `this` context
describe('Feature', () => {
  before(() => {
    cy.createAccount(Cypress.env('web_account'));
  });
  it('test', () => {
    // this.aliasName will be undefined!
  });
});
```

### testIsolation and Hook Choice

```javascript
// Use before/after with testIsolation: false (tests share state)
describe('Feature', { testIsolation: false }, function () {
  before(function () { /* runs once */ });
  after(function () { /* runs once */ });
});

// Use beforeEach/afterEach without testIsolation (tests are independent)
describe('Feature', function () {
  beforeEach(function () { /* runs before each test */ });
  afterEach(function () { /* runs after each test */ });
});
```

### API Call Chaining

```javascript
// CORRECT - use .then() for sequential API calls
cy.createAccount(Cypress.env('web_account'))
  .saveGeneratedTimeBasedIdAs('expName')
  .then(function () {
    return cy.createAPageV1(examplePage);
  })
  .then(function (response) {
    cy.wrap(response.body.id).as('testPageId');
  });

// WRONG - saveGeneratedTimeBasedIdAs is chained, not standalone
cy.saveGeneratedTimeBasedIdAs('expName'); // This won't work standalone
```

### Never Use Direct cy.get() in Spec Files

```javascript
// CORRECT - use page object
experimentListPage.openAnExperiment(this.expName);
variationsTab.verifyVariationCount(3);

// WRONG - direct selector in spec
cy.get('[data-test="experiment-name"]').click();
cy.get('.variation-row').should('have.length', 3);
```

### Store Response Only When Needed

```javascript
// CORRECT - store when needed later
cy.createAPageV1(examplePage).then(function (response) {
  cy.wrap(response.body.id).as('testPageId');
});

// WRONG - unused variable
cy.createAPageV1(examplePage).then(function (response) {
  const page = response.body; // never used later
});
```

### Max 5 Tests Per Spec File

If you have more than 5 test cases for a module, split them into multiple spec files:
```
ab_test_archive.spec.js          (5 tests)
ab_test_archive_restore.spec.js  (3 tests)
```

### AI-Generated Code Comments

```javascript
// Add ONLY to infrastructure code (page objects, builders, commands)
// Generated by CLAUDE CODE
clickArchiveButton() {
  this.archiveBtn().should('exist').click();
  return this;
}

// Do NOT add to spec files
```

---

## 8. Checklist Before Finalizing Generated Code

- [ ] All imports use correct relative paths (see depth calculation in Section 2)
- [ ] `function()` syntax used in describe/it/before/after (not arrow functions)
- [ ] `testIsolation: false` set when using before/after
- [ ] Tags imported from tagList.js using correct class (CommonTag, WebTag, FlagTag)
- [ ] Test names follow `[TICKET-ID][Product][Module]_Description` format
- [ ] Setup uses API commands (not UI) in before/beforeEach
- [ ] Cleanup includes `cy.deleteAccount()` in after/afterEach
- [ ] Page objects used for all UI interactions (no direct cy.get in specs)
- [ ] Builders used for test data creation
- [ ] Region comments used: `#region Setup Test Data`, `#region Test Execution`, `#region Cleanup`
- [ ] No `.only()` or `.pause()` calls
- [ ] No hardcoded test data (use builders, testData files, or random values)
- [ ] Max 5 tests per spec file
- [ ] TODO selectors documented with comments
- [ ] New infrastructure code has `// Generated by CLAUDE CODE` comment
- [ ] No unused variables or imports

---

## Coding Conventions Reference

**CRITICAL**: Read the full coding conventions from the target repo before generating code:
```
.claude/docs/coding-conventions.md
```

### Naming Conventions

| What | Convention | Example |
|------|-----------|---------|
| Branch | `{username}/{TICKET_ID}-{kebab-case-title}` | `phanh/CJS-10886-add-new-ve` |
| Commit | `[TICKET_ID] message` | `[CJS-7934] Update failed tests` |
| Folders | lowercase_underscores | `visual_editor/`, `ab_test/` |
| Class files | camelCase.js | `campaignBuilder.js`, `visualEditorPage.js` |
| Class names | PascalCase | `CampaignBuilder`, `VisualEditorPage` |
| Variables | camelCase | `projectName`, `emailAddress` |
| Tags | snake_case in arrays | `['web', 'smoke_suite']` |
| Elements | nameType | `saveBtn()`, `emailInput()`, `genderDropdown()` |
| Test names | `[ID][Platform][Module]_Desc` | `[CJS-8492][Web][CMAB]_Explore` |

### Code Structure Rules

| Rule | Value |
|------|-------|
| Max tests/file | 5 |
| Max methods/class | ~30 (split if more) |
| Max args/method | 5 (use Builder for more) |
| Builder constructor args | Max 2 (use setters from 3rd) |
| Function syntax | `function()` not arrow |
| Setup | API-first via builders |
| Cleanup | `cy.deleteAccount()` |
| Page objects | Always, never direct `cy.get()` in specs |
| Random values | Always use `Utilities.randomFruit()`, never fixed strings |
| Text resources | Use `support/resources/textResource.js`, not hardcoded |
| Method chaining | Return `this` (or another page object if navigating) |
| Call chaining | Chain consecutive calls on the same page object instead of repeating the variable name |
| Element vs Page | Methods with `.find()`, `.not()`, CSS selectors go in `Elements.js`; `Page.js` composes element methods |
| Single responsibility | One action per method, separate action and verification |

### AI-Generated Code Tracking

- Add `// Generated by CLAUDE CODE` to Page Objects, Page Elements, Builders, APIs
- Do NOT add it to test scripts (spec files)
- Use `cy.get('TODO')` for uninvestigated selectors with `// TODO: Update selector after investigation`

### Region Organization

Use `#region` comments to organize code blocks:
```javascript
//#region Setup Test Data
//#endregion
//#region Verification Methods
//#endregion
```

### Linting

Always run before pushing: `npm run lint:fix`
- Single quotes, semicolons, 2-space indent (Prettier)
- No `.only()`, `.pause()` in committed code

---

## Failure Recovery Per Step

| Step | On Failure | Checkpoint Saved |
|------|-----------|-----------------|
| Pre-flight (MCP, git, node) | **abort** -- Cannot proceed without prerequisites | None |
| Read JIRA task | **abort** -- Cannot generate scripts without test cases | None |
| Create branch | **ask_user** -- Branch conflict? Ask user to resolve or provide branch name | None |
| Analyze codebase (parallel) | **skip_continue** -- Generate scripts with partial context, warn conventions may be missed | `{TICKET_ID}_test_cases.md` |
| Check/create page objects | **skip_continue** -- Use `cy.get('TODO')` placeholders, warn user to update | `{TICKET_ID}_codebase_context.md` |
| Determine target folder | **ask_user** -- If labels are ambiguous, ask user whether smoke or regression | `{TICKET_ID}_codebase_context.md` |
| Generate test scripts | **retry** -- Re-generate failed spec once, then save partial specs | `{TICKET_ID}_page_objects.md` |
| Lint & review | **retry** -- Auto-fix lint errors, retry once, then present with warnings | Generated spec files |
| Run tests | **retry** -- Fix and re-run (max 3 attempts), then present failures to user | Generated spec files |

**Checkpoint mechanism:** Generated spec files are written to disk incrementally. If the process aborts at any point, all previously generated files remain on disk for manual review.

---

## Folder Placement Rules

**CRITICAL:** The spec file location is determined by the **test case JIRA ticket labels**, not the automation ticket labels.

| Test Case Labels | Target Folder | Tags |
|-----------------|---------------|------|
| Contains `smoke_suite` or `smoke` | `cypress/e2e/{product}/smoke_suite/{feature}/` | Include `CommonTag.smoke_ve` or `CommonTag.smoke_suite` |
| No smoke label | `cypress/e2e/{product}/regression/{feature}/` | Product tags only, e.g. `[WebTag.web, WebTag.new_ve]` |

**Always verify** by checking tags in existing tests in the target folder:
```
Grep("tags:", path: "cypress/e2e/{product}/{smoke_suite|regression}/{feature}/", output_mode: "content")
```

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| No test cases in ticket | **ask_user**: Suggest `/exp-qa-agents:create-test-cases` first |
| Test case has no description/steps | **ask_user**: Ask user to provide a screenshot of the test steps from JIRA UI |
| Automation ticket references other tickets | **follow_chain**: Fetch referenced tickets (e.g., "automate CJS-10590") to find actual test cases |
| Page object missing | **retry**: Invoke `/exp-qa-agents:inspect-and-create-page-objects-cypress-js` to create it |
| Element missing in page object | **retry**: Invoke `/exp-qa-agents:inspect-and-create-page-objects-cypress-js` to add missing elements |
| Selector not found at runtime | **retry**: Update page object via inspect skill, re-run |
| Max fix attempts (3) | **ask_user**: Present failures, ask user for guidance |


## Self-Correction

1. **"Wrong product area"** → Re-analyze, adjust imports/tags
2. **"Combine into one spec"** → Merge, ensure ≤5 per file
3. **"Wrong folder (smoke vs regression)"** → Check test case JIRA labels, move file, update tags
4. **"Test case has no steps"** → Ask user for screenshot, or follow reference chain to linked tickets
5. **"Preview and Start in same spec"** → If same setup: use `[false, true].forEach` with `isPreview` flag in one file. If different setup/changes: split into 2 files (`*_action.spec.js` + `*_action_start_check.spec.js`)
6. **"Missing UI steps (e.g., magnifying glass click)"** → Don't use bundled helpers; call individual page object methods to match each test step
7. **"Wrong method for starting campaign"** → Use `startAnExperiment(name, type)` not `startACampaign(name)` — check reference scripts
