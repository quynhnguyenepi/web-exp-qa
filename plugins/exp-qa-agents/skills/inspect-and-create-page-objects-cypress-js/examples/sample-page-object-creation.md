# Sample: Inspect and Create Page Objects

## Example 1: Help Center Dialog (Real Execution)

### User Request

> Access https://rc-app.optimizely.com/signin, login with credentials, click on Help link, create page object for Help popup

### Step 0: Get Target URL and Context

- URL: `https://rc-app.optimizely.com/signin`
- Credentials provided by user
- Product area: `common` (Help Center is accessible from all products)
- Feature: standalone dialog (no subfolder needed)
- Webelements path: `cypress/pages/webelements/common/HelpCenterDialogElements.js`
- Page object path: `cypress/pages/common/HelpCenterDialog.js`

### Step 1: Navigate, Login, and Open Help Dialog (Main Thread)

1. Navigated to signin page
2. Filled login form via `browser_fill_form`
3. Clicked "Log In" button
4. Took screenshot to confirm dashboard loaded
5. Found Help link in sidebar via snapshot
6. Clicked Help link to open the popup
7. Took screenshot of the Help Center dialog

### Step 2: Extract data-test-section via browser_evaluate

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
        r.text.includes('Help') || r.text.includes('Knowledge') ||
        r.text.includes('Ticket') || r.text.includes('Cancel') ||
        r.testSection.includes('help') || r.testSection.includes('dialog')
      )
    };
  }`
})
```

**Result:** Found 25 relevant elements with their `data-test-section` values.

### Step 3: Analyze Existing Patterns (Background Agent)

Launched background Agent to check:
- No existing Help page objects found
- Read `CommonBasePageElements.js` for inheritance pattern
- Read dialog examples (`ErrorDialogElements.js`, `ErrorDialog.js`) for popup pattern
- Found `cy.getDataTestSection()` and `.findDataTestSection()` as primary selector commands

### Step 4: Elements Identified

| Element | `data-test-section` | Type | Selector Approach |
|---------|-------------------|------|-------------------|
| Support dialog | `support-dialog` | Container | `cy.getDataTestSection()` |
| Dialog frame | `dialog-frame` | Container | `cy.getDataTestSection()` |
| Help center home | `help-center-home` | Container | `cy.getDataTestSection()` |
| Search form | `help-center-modal-support-doc-search-form` | Form | `cy.getDataTestSection()` |
| Search input | `help-center-modal-support-doc-search-input` | Input | `cy.getDataTestSection()` |
| Knowledge Base | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Knowledge Base')` |
| Developer Docs | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Developer Docs')` |
| Academy | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Academy')` |
| Create Ticket card | `help-center-home-create-request-epi-zendesk` | Container | `cy.getDataTestSection()` |
| Create Ticket link | `help-center-home-create-request-epi-zendesk-link` | Link | `cy.getDataTestSection()` |
| View Tickets card | `help-center-home-my-requests` | Container | `cy.getDataTestSection()` |
| View Tickets link | `help-center-home-my-requests-link` | Link | `cy.getDataTestSection()` |
| Optimizely Blog | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Optimizely Blog')` |
| Content Library | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Content Library')` |
| Sample Size Calculator | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Sample Size Calculator')` |
| Solutions Partners | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Solutions Partners')` |
| Optimizely Community | `undefined-link` | Link | **Scoped** `this.supportDialog().contains('a', 'Optimizely Community')` |
| Cancel button | `cancel-button` | Button | `cy.getDataTestSection()` |
| Close icon | N/A | Button | `this.dialogFrame().find('button').first()` |
| Help nav link | `help-nav-link-button` | Link | `cy.getDataTestSection()` |

**Key Decision:** Links with `undefined-link` as `data-test-section` were scoped to `this.supportDialog()` parent container to avoid matching multiple elements.

### Step 5: Generated Webelements File

```javascript
import CommonBasePageElements from './CommonBasePageElements';

export default class HelpCenterDialogElements extends CommonBasePageElements {
  //#region Dialog container
  supportDialog(options) {
    return cy.getDataTestSection('support-dialog', options);
  }
  dialogFrame(options) {
    return cy.getDataTestSection('dialog-frame', options);
  }
  helpCenterHome(options) {
    return cy.getDataTestSection('help-center-home', options);
  }
  //#endregion

  //#region Search
  searchForm(options) {
    return cy.getDataTestSection('help-center-modal-support-doc-search-form', options);
  }
  searchInput(options) {
    return cy.getDataTestSection('help-center-modal-support-doc-search-input', options);
  }
  //#endregion

  //#region Support articles and courses
  knowledgeBaseLink(options) {
    return this.supportDialog(options).contains('a', 'Knowledge Base');
  }
  developerDocsLink(options) {
    return this.supportDialog(options).contains('a', 'Developer Docs');
  }
  academyLink(options) {
    return this.supportDialog(options).contains('a', 'Academy');
  }
  //#endregion

  //#region Support team
  createTicketLink(options) {
    return cy.getDataTestSection('help-center-home-create-request-epi-zendesk-link', options);
  }
  viewTicketsLink(options) {
    return cy.getDataTestSection('help-center-home-my-requests-link', options);
  }
  //#endregion

  //#region Additional resources
  optimizelyBlogLink(options) {
    return this.supportDialog(options).contains('a', 'Optimizely Blog');
  }
  // ... more scoped links
  //#endregion

  //#region Dialog actions
  cancelBtn(options) {
    return cy.getDataTestSection('cancel-button', options);
  }
  closeDialogIcon(options) {
    return this.dialogFrame(options).find('button').first();
  }
  //#endregion

  //#region Sidebar Help link
  helpNavLink(options) {
    return cy.getDataTestSection('help-nav-link-button', options);
  }
  //#endregion
}
```

### Step 6: Generated Page Object File

```javascript
import HelpCenterDialogElements from '../webelements/common/HelpCenterDialogElements';

export default class HelpCenterDialog extends HelpCenterDialogElements {
  //#region Open / Close
  openHelpCenter() {
    this.helpNavLink().click();
    return this;
  }
  closeHelpCenter() {
    this.cancelBtn().click();
    return this;
  }
  //#endregion

  //#region Verifications
  verifyHelpCenterIsDisplayed() {
    this.supportDialog().shouldBeVisible();
    this.searchInput().shouldBeVisible();
    return this;
  }
  verifyAllSupportLinksAreVisible() {
    this.knowledgeBaseLink().shouldBeVisible();
    this.developerDocsLink().shouldBeVisible();
    this.academyLink().shouldBeVisible();
    return this;
  }
  // ... more verification methods
  //#endregion
}
```

### Step 7: Presented to User

```
Page objects created
  - Webelements: cypress/pages/webelements/common/HelpCenterDialogElements.js
  - Page object: cypress/pages/common/HelpCenterDialog.js
  - Elements: 16 selectors
  - Methods: 15 action + 10 verification methods

Usage example:
  import HelpCenterDialog from '../../pages/common/HelpCenterDialog';
  const helpCenterDialog = new HelpCenterDialog();
  helpCenterDialog
    .openHelpCenter()
    .verifyHelpCenterIsDisplayed()
    .verifyAllSupportLinksAreVisible()
    .closeHelpCenter();
```

---

## Example 2: Audiences Page (Hypothetical)

### User Request

> Create page objects for the Audiences page in the web product

### Execution

- URL: `https://app.optimizely.com/v2/projects/123/audiences`
- Product area: `web`
- Feature: `audiences`
- Webelements path: `cypress/pages/webelements/web/audiences/AudiencesPageElements.js`
- Page object path: `cypress/pages/web/audiences/AudiencesPage.js`

### Key Differences from Example 1

- Product area is `web` (not `common`) -> extends `WebBasePageElements`
- Feature has its own subfolder: `audiences/`
- All elements had unique `data-test-section` values -> no scoped `contains()` needed
- Page has multiple states (list view + create dialog) -> multiple snapshots taken

### Generated Files

```javascript
// Webelements
import WebBasePageElements from '../../web/WebBasePageElements';

export default class AudiencesPageElements extends WebBasePageElements {
  createAudienceBtn(options) {
    return cy.getDataTestSection('create-audience-btn', options);
  }
  audienceNameInput(options) {
    return cy.getDataTestSection('audience-name-input', options);
  }
  // ...
}
```

```javascript
// Page Object
import AudiencesPageElements from '../../webelements/web/audiences/AudiencesPageElements';

export default class AudiencesPage extends AudiencesPageElements {
  clickCreateAudience() {
    this.createAudienceBtn().click();
    return this;
  }
  // ...
}
```

```
Page objects created
  - Webelements: cypress/pages/webelements/web/audiences/AudiencesPageElements.js
  - Page object: cypress/pages/web/audiences/AudiencesPage.js
  - Elements: 8 selectors
  - Methods: 6 action + 2 verification methods
```
