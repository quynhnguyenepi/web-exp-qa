# Fix Daily Run (Playwright TypeScript) Guidelines

Standards for diagnosing and fixing failed Playwright TypeScript E2E tests from GitHub Actions daily runs.

## Root Cause Analysis

### Categorize Before Fixing

Always categorize every failure before applying any fix:

| Category | Action |
|----------|--------|
| **Test code issue** | Fix in test/page object code |
| **Application issue** | Report as product bug, do not modify test code |
| **Flaky/timing issue** | Add retry logic, better waits, or scroll-into-view |
| **Environment issue** | Report, do not modify test code |

### Shared Root Causes

Look for patterns across failures before fixing individually:
- Multiple tests failing on the same locator = page object issue (fix once)
- Tests showing `(0ms)` = `beforeAll` failure (fix the hook, not the tests)
- Cascading `afterAll` failures = cleanup dependency (fix the first failure)

---

## Fix Patterns

### Do

- Read the page object and test file before making changes
- Fix in page objects first -- a single fix often resolves multiple failures
- Add `scrollIntoViewIfNeeded()` before clicks on elements that may be off-screen
- Add `toBeEnabled()` or `toBeVisible()` checks before interactions
- Use retry loops (max 3 attempts) for toggle/panel operations
- Ensure `afterAll` hooks set up their own prerequisite state
- Verify syntax with `npx playwright test --list` after changes

### Do Not

- Refactor unrelated code while fixing failures
- Change timeout values without justification
- Remove or skip failing tests instead of fixing them
- Introduce new dependencies or libraries
- Change test assertions to make them pass (fix the interaction, not the expectation)
- Apply fixes without understanding the root cause

---

## Local Verification

### Running Tests

- Use `--workers=1 --headed` for debugging visibility
- Run the full affected suite, not just the single failing test
- Monitor long-running tests in background and check periodically

### Interpreting Results

| Result | Action |
|--------|--------|
| Previously failing, now passing | Fixed -- include in report |
| Still failing with same error | Fix did not work -- try alternative |
| Still failing with different error | Fix introduced regression -- revert |
| New failure in unrelated test | Regression from fix -- investigate |

---

## Reporting

### Comparison Table

Always present a before/after comparison:
```
| Test | CI (Before) | Local (After) | Status |
|------|-------------|---------------|--------|
```

### Changed Files

List every modified file with a one-line summary of the change and the reason.

---

## Anti-Patterns

### Increasing Timeouts Without Diagnosis

**Problem:** Bumping timeout from 30s to 120s without understanding why the element is slow.
**Solution:** Investigate why the element is not ready. Add proper waits or state checks instead.

### Fixing Symptoms Instead of Causes

**Problem:** Adding a retry around a click that fails because the element is behind a modal.
**Solution:** Dismiss the modal or wait for it to close before clicking.

### Ignoring afterAll Failures

**Problem:** Treating afterAll failures as non-critical because they happen after the test.
**Solution:** afterAll failures cascade and pollute subsequent test runs. Fix them.

### Silent try/catch Hiding Real Failures

**Problem:** A method catches errors silently (e.g., `console.log('skipping...')`), making the test fail at a later step with a misleading error. You waste time debugging the wrong step.
**Solution:** Only catch silently when the step is truly optional. Add a `required` parameter and throw when the step is mandatory. Always check preceding steps for silent catches when the error location doesn't match the logical failure point.

### Assuming Clean State Without Verifying

**Problem:** Test assumes it starts from a clean state (e.g., integration OFF, no data). But if a previous run's cleanup failed, the state is already set. The test then performs the wrong action (e.g., turning ON what's already ON → actually turns it OFF).
**Solution:** Either verify the starting state before acting, or handle both clean and pre-existing states gracefully. Check if the expected UI element exists; if not, check if the desired state is already achieved.

### page.reload() Without waitForLoadState

**Problem:** After `page.reload()`, the next action runs before the page finishes loading. Elements appear in their default/loading state instead of their actual saved state, causing wrong interactions.
**Solution:** Always follow `page.reload()` with `await page.waitForLoadState('networkidle')` to ensure all data has loaded before proceeding.

### UI Copy/Label Changes Breaking Role-Based Locators

**Problem:** Product team updates UI text (e.g., "Thread" → "Chat", "Delete thread" → "Delete"). Locators using `getByRole({ name: '...' })` or `getByText('...')` silently fail because the text no longer matches. The error looks like "element not found" but the element is there — just with different text.
**Solution:** Inspect the live app to check current UI text. Update the locator text to match. For long-term stability, prefer `getByTestId()` when available, as test IDs don't change with copy updates.

---

## Common Fix Patterns for Playwright Tests

**1. Button click timeout (element found but not stable):**
```typescript
// Before (fragile):
await this.button.click();

// After (robust):
await this.button.scrollIntoViewIfNeeded();
await expect(this.button).toBeEnabled({ timeout: 30_000 });
await this.button.click();
```

**2. Missing `await` on Playwright actions:**
```typescript
// Before (silently fails — no await means fire-and-forget):
this.selectorTextbox.fill(content);
this.checkIcon.click();

// After (properly awaited):
await this.selectorTextbox.fill(content);
await expect(this.checkIcon).toBeEnabled({ timeout: 30_000 });
await this.checkIcon.click();
await this.page.waitForLoadState();
```

**3. Sidebar/panel toggle not registering:**
```typescript
// Before (single attempt):
await this.toggleButton.click();
await expect(this.panel).toBeVisible({ timeout: 120_000 });

// After (retry logic):
for (let attempt = 0; attempt < 3; attempt++) {
  await this.toggleButton.click();
  try {
    await expect(this.panel).toBeVisible({ timeout: 15_000 });
    return;
  } catch {
    // Click didn't register, retry
  }
}
// Final attempt with longer timeout
await this.toggleButton.click();
await expect(this.panel).toBeVisible({ timeout: 30_000 });
```

**4. Iterating over dynamic list (items scroll out of view):**
```typescript
// Before (fragile - items at high index are out of view):
const count = await this.items.count();
for (let i = count - 1; i >= 0; i--) {
  await this.items.nth(i).hover();
  // ...
}

// After (robust - always target first visible item):
let count = await this.items.count();
while (count > 0) {
  const item = this.items.first();
  await item.scrollIntoViewIfNeeded();
  await item.hover();
  // ... delete/action ...
  count = await this.items.count();
}
```

**5. afterAll cleanup missing prerequisite state:**
```typescript
// Before (assumes state from test):
test.afterAll(async () => {
  await page.deleteAllItems();  // May fail if sidebar isn't open
});

// After (ensures correct state first):
test.afterAll(async () => {
  await page.openPanel();       // Ensure panel is open
  await page.openSidebar();     // Ensure sidebar is open
  await page.deleteAllItems();
});
```

**6. UI selector changes (element redesigned/renamed):**
```typescript
// Before (old selector — element was redesigned):
this.opalChatInput = page.getByPlaceholder('Ask Opal');
this.deleteChatButton = page.getByRole('button', { name: 'Delete Chat' });
this.newChatButton = page.getByRole('button', { name: 'New Chat' });

// After (updated selectors matching new UI):
this.opalChatInput = page.locator('div[contenteditable="true"]');
this.deleteChatOption = page.getByRole('option', { name: 'Delete' });
this.newChatButton = page.locator('button').filter({ hasText: 'New Chat' });
```
When locators fail, **inspect the live app** to verify the current DOM structure.
Common causes: button renamed, element type changed (button → option), placeholder removed,
input replaced with contenteditable div, action moved behind a menu (e.g., direct delete button
→ hover + "Chat options" menu + "Delete" option).

**IMPORTANT:** Label text changes frequently (e.g., `'Delete Chat'` → `'Delete thread'` → `'Delete'`,
`'Thread options'` → `'Chat options'`, `'Search Thread Title'` → `'Search Chat Title'`).
When fixing a selector, always verify the **current** label in the live app rather than guessing.

**7. Interaction pattern changes (e.g., direct action → menu action):**
```typescript
// Before (direct delete button):
await chatItem.click();
await this.deleteChatButton.click();

// After (hover → options menu → delete):
await chatItem.hover();
const threadOptionsButton = chatItem.getByRole('button', { name: 'Thread options' });
await threadOptionsButton.click();
await this.deleteChatOption.click();
await this.deleteChatConfirmButton.click();
```

**8. Fragile CSS selectors replaced with stable ones:**
```typescript
// Before (brittle — depends on DOM structure/class names):
await editorPage.editElement(".AghGtd > a:nth-of-type(1)");

// After (stable — uses ID or semantic selector):
await editorPage.editElement("#footer");
```

**9. Login/re-login flow simplified:**
```typescript
// Before (complex multi-step re-auth with conditionals):
await this.nextButton.click();
await this.passWord.fill(password);
await this.verifyButton.click();
if (await this.nextButton.isVisible()) { /* repeat */ }

// After (navigate to login URL directly — simpler, more reliable):
await this.page.goto(this.LOGIN_URL);
await this.page.waitForLoadState('domcontentloaded', { timeout: 80_000 });
await expect(this.loginLoadingIcon).toBeHidden({ timeout: 80_000 });
await this.experimentationInstanceLink.click();
await expect(this.passWord).toBeVisible();
await this.passWord.fill(password);
await this.verifyButton.click();
```

**10. Waiting for async operations to complete before asserting success:**
```typescript
// Before (asserts immediately — may fail if generation is still running):
async verifyGenerateCopySuccess() {
  await expect(this.moreOptionsBtn).toBeVisible();
}

// After (waits for loading indicator to disappear first):
async verifyGenerateCopySuccess() {
  await expect(this.generatingCopyText).toBeHidden({ timeout: 120_000 });
  await expect(this.moreOptionsBtn).toBeVisible();
}
```

**11. Timeout increases for AI/LLM-powered features:**
AI-powered features (Opal Chat, brainstorm, generate copy) are inherently slower and variable.
```typescript
// Opal chat answer verification — increased from 120s to 240s:
async verifyAnswer(timeout: number = 240_000) { ... }

// Visual editor iframe loading — increased from 2s to 30s:
await this.page.waitForTimeout(30_000);
await expect(this.createBtn).toBeEnabled({ timeout: 30_000 });
```

**12. Removing test steps that verify intermediate state no longer present:**
When the product UI changes, some intermediate verification steps become invalid.
Rather than fixing broken assertions for removed UI elements, **remove the obsolete steps**.
```typescript
// Before (verifies UI element that no longer exists):
await flagsPage.verifyVariationFormNotEmpty(variableName);

// After (step removed entirely — the UI no longer shows this form)
```

**13. Different Visual Editor versions require different page object methods:**
Some projects use the new VE (variation opened via row click + "Classic editor" link),
while others use the old VE (variation opened directly by test ID with variation ID).
Create **separate methods** for each VE version rather than forcing one method to handle both.
```typescript
// New VE — opens via row click + classic editor link (Web projects):
async openVariationDetail(variationName: string) {
  await this.page.getByRole('row', { name: new RegExp(variationName) })
    .getByTestId('variation-table-row-editor-cta').click();
  await this.page.getByTestId('classic-editor-link').click();
}

// Old VE — opens directly by variation ID (Edge projects):
async openVariationDetailOldVE(variationId: number) {
  await this.page.getByTestId(`variation-table-row-edit-${variationId}`).click();
}
```
When a test uses the wrong VE method for its project type, the locator will fail.
Check whether the test targets a **Web** or **Edge** project and use the appropriate method.

**14. Silent try/catch swallowing real errors:**
When a method catches errors silently, the test fails at a **later step** with a misleading error.
The real root cause is hidden by the catch block.
```typescript
// Before (silent catch hides the real failure — error appears at Save button, not org selector):
async selectItem(itemName: string) {
  try {
    await this.chooseBtn.waitFor({ state: 'visible', timeout: 5000 });
    await this.chooseBtn.click();
    await this.page.getByText(itemName).click();
  } catch (e) {
    console.log('Selector not visible, skipping...');  // Silently swallows the error!
  }
}

// After (throw when the step is required, only skip when truly optional):
async selectItem(itemName: string, required = true) {
  try {
    await this.chooseBtn.waitFor({ state: 'visible', timeout: 10000 });
    await this.chooseBtn.click();
    await this.page.getByText(itemName).click();
  } catch {
    if (required) {
      throw new Error(`Item selector not found for "${itemName}"`);
    }
    console.log('Selector not visible, skipping...');
  }
}
```
**Diagnostic tip:** When an error occurs at step N but the real cause is step N-1, look for
silent `try/catch` blocks in the preceding steps that may have swallowed the actual failure.

**15. Pre-existing state from previous failed test runs:**
When a test's cleanup step fails (e.g., `turnOff` or `delete`), the next run starts with
leftover state. The test assumes a clean state but encounters pre-existing data.
```typescript
// Before (assumes "Choose an organization..." button always appears after turning on):
await this.turnOnIntegration();
await this.selectOrganization(orgName);  // Fails — org already selected from previous run

// After (handles both fresh and pre-existing state):
await this.turnOnIntegration();
try {
  await chooseBtn.waitFor({ state: 'visible', timeout: 10000 });
  await chooseBtn.click();
  await this.page.getByText(orgName).click();
} catch {
  // Org may already be selected from a previous run — check if Save is available
  const isSaveVisible = await saveBtn.isVisible().catch(() => false);
  if (isSaveVisible) {
    console.log(`"${orgName}" already selected, proceeding...`);
  } else {
    throw new Error(`Cannot select "${orgName}" and Save not available`);
  }
}
```

**16. Page reload without waiting for network idle:**
After `page.reload()`, subsequent actions may execute before the page is fully loaded,
causing elements to be in their default/loading state rather than the actual saved state.
```typescript
// Before (race condition — next action runs before page is ready):
async verifySavedSettings() {
  await expect(this.saveButton).toBeHidden();
  await this.page.reload();
}

// After (waits for all network requests to settle after reload):
async verifySavedSettings() {
  await expect(this.saveButton).toBeHidden();
  await this.page.reload();
  await this.page.waitForLoadState('networkidle');
}
```

**17. Sidebar/panel content not fully loaded before interaction:**
After opening a sidebar or panel, the content may still be loading. Interacting with elements
(like toggles) before the content is ready can produce wrong behavior (e.g., clicking a toggle
that appears OFF but is actually loading its ON state).
```typescript
// Before (clicks toggle immediately — may catch it in loading/default state):
async turnOffIntegration() {
  await this.turnOnSlide.click();
  await this.clickContinueButton();
}

// After (waits for a content-loaded indicator before interacting):
async turnOffIntegration() {
  // editBtn only appears when integration is ON and configured — proves content is loaded
  await this.editOrganizationBtn.waitFor({ state: 'visible', timeout: 15000 });
  await this.turnOnSlide.click();
  await this.clickContinueButton();
}
```

**18. UI copy/label text changes breaking role-based locators:**
When the product team updates UI text (e.g., renaming "Thread" to "Chat"), locators that match on
text content (`getByRole({ name: '...' })`, `getByText('...')`) break silently.
```typescript
// Before (locators match on old UI text — broken after rename):
this.opalChatHistorySearch = page.getByRole('button', { name: 'Search Thread Title' });
this.deleteChatOption = page.getByRole('option', { name: 'Delete thread' });
const threadOptionsButton = chatItem.getByRole('button', { name: 'Thread options' });

// After (update text to match current UI):
this.opalChatHistorySearch = page.getByRole('button', { name: 'Search Chat Title' });
this.deleteChatOption = page.getByRole('option', { name: 'Delete' });
const threadOptionsButton = chatItem.getByRole('button', { name: 'Chat options' });
```
**Diagnostic tip:** When a `getByRole` or `getByText` locator fails, ask the user:
> "The locator `getByRole('button', { name: 'Search Thread Title' })` is failing. Would you like me to
> open the browser via Playwright MCP, navigate to the page, and inspect the current elements to find
> the correct selector?"

If user agrees, use this workflow:
1. `browser_navigate` to the page where the failing locator is used
2. Perform login if needed (use credentials from test-data or ask user)
3. Navigate step-by-step to reach the UI area with the broken locator
4. `browser_snapshot` to capture the accessibility tree — find the actual current text/role/testid
5. Compare old locator text vs actual element text in snapshot
6. Update the locator in the page object to match the current UI
7. Prefer `getByTestId()` if a `data-testid` attribute exists (stable across copy changes)

If user declines, update the text based on CI error messages and common rename patterns.

---

## Fix Application Rules

- **Read the page object and test file BEFORE making changes** — understand existing patterns
- **Fix in page objects first** — a single page object fix often resolves multiple test failures
- **Minimize changes** — only fix what's broken, don't refactor unrelated code
- **Preserve existing patterns** — match the codebase style (naming, structure, timeouts)
- **Inspect the live app** when selectors fail — use Playwright MCP or Chrome DevTools to verify current DOM
- **Check for missing `await`** — a common silent bug that causes intermittent failures
- **Remove obsolete steps** rather than fixing assertions for UI elements that no longer exist
- **Increase timeouts for AI features** — Opal Chat, brainstorm, generate copy are inherently slow (use 120-240s)
- **Simplify complex flows** — if a multi-step workaround exists (e.g., conditional re-login), replace with a direct approach (e.g., navigate to URL)
- **Verify syntax** after changes:
  ```bash
  npx playwright test --list 2>&1 | head -20
  ```

---

## Diagnostic Checklist (run through for each failure)

1. Is the locator still valid? → Inspect the live app DOM
2. Is there a missing `await`? → Check all Playwright calls in the failing method
3. Is the timeout sufficient? → AI features need 120-240s, standard UI needs 30-60s
4. Did the interaction pattern change? → Direct button → menu, input → contenteditable, etc.
5. Does the test step still make sense? → If the UI removed the element, remove the step
6. Is the `afterAll` cleanup robust? → Ensure it opens panels/sidebars before deleting
7. Are CSS selectors stable? → Prefer `getByTestId`, `getByRole`, IDs over class-based selectors
8. Is a `try/catch` hiding the real error? → Check preceding steps for silent catches that swallow failures
9. Could pre-existing state from a previous run cause this? → Check if data/config is left over from a failed cleanup
10. Is `page.reload()` followed by `waitForLoadState('networkidle')`? → Missing this causes race conditions
11. Is the sidebar/panel content fully loaded before interaction? → Wait for a content-specific indicator element
12. Did UI text/labels change? → Ask user to open browser via Playwright MCP, navigate to the page, `browser_snapshot` to find current element text/role/testid, then update locators

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Fetch CI logs and identify failed tests", status: "in_progress", activeForm: "Fetching CI logs" },
  { content: "Analyze root causes of failures", status: "pending", activeForm: "Analyzing root causes" },
  { content: "Apply fixes to test code", status: "pending", activeForm: "Applying fixes" },
  { content: "Run tests locally to verify fixes", status: "pending", activeForm: "Running tests locally" },
  { content: "Report results", status: "pending", activeForm: "Reporting results" }
])
```

---


## Error Handling

| Scenario | Action |
|----------|--------|
| GitHub CLI not authenticated | Ask user to run `gh auth login` |
| Run ID not found | Ask user to verify the URL/ID |
| No test failures in logs | Report that all tests passed |
| Fix introduces new failures | Revert the change and try alternative approach |
| Tests require env vars not set locally | Warn user about missing `.env` configuration |
| Playwright browsers not installed | Run `npx playwright install chromium` |

---


## Self-Correction

1. **"Only fix specific tests"** -> Focus on the listed tests only
2. **"Don't run tests, just apply fixes"** -> Skip Step 3
3. **"Also create a PR"** -> After fixes, invoke `/exp-qa-agents:create-pr`
4. **"Revert changes to X file"** -> Revert specific file and re-run
5. **"The remaining failures are known bugs"** -> Mark them as app issues in the report
