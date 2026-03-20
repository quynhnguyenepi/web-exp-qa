# Sample: Fix Daily Run Failures for Playwright Tests

---

## Input

User request: "Fix the failures from this daily run: https://github.com/example-org/example-repo/actions/runs/22729053437"

---

## Step 0: Parse Input and Fetch CI Logs

```
Fetching logs for run 22729053437...

Test Summary:
  - Total: 48 tests
  - Passed: 42
  - Failed: 6

Failed tests identified:
  1. sidebar.spec.ts - "should toggle sidebar panel"
  2. sidebar.spec.ts - "should delete items from sidebar"
  3. sidebar.spec.ts - "should rename sidebar item"
  4. editor.spec.ts - "should save changes"
  5. editor.spec.ts - "should undo changes"
  6. cleanup (afterAll) - sidebar.spec.ts
```

---

## Step 1: Categorize Failures and Identify Root Causes

```
| # | Test File      | Error                          | Root Cause              |
|---|----------------|--------------------------------|-------------------------|
| 1 | sidebar.spec   | TimeoutError: click on toggle  | Toggle click not stable  |
| 2 | sidebar.spec   | TimeoutError: hover on nth(5)  | Item scrolled out of view |
| 3 | sidebar.spec   | TimeoutError: click on toggle  | Same as #1 (shared root) |
| 4 | editor.spec    | TimeoutError: click on save    | Button behind overlay    |
| 5 | editor.spec    | beforeAll failure cascade       | Depends on #4 setup      |
| 6 | sidebar.spec   | afterAll: panel not open        | Cleanup assumes test state |

Classification:
  - Test code issues: #1, #2, #3, #6 (fixable)
  - App issue: #4 (overlay not dismissed -- product bug)
  - Cascade from #4: #5 (will resolve if #4 is fixed or skipped)

Shared root causes:
  - #1 and #3: Same toggle click issue in SidebarPage.togglePanel()
  - #5: Cascade from #4 beforeAll failure
```

---

## Step 2: Apply Fixes

**Fix 1: SidebarPage.togglePanel() -- retry logic for toggle click**

File: `pages/sidebar.page.ts`

```typescript
// Before:
async togglePanel() {
  await this.toggleButton.click();
  await expect(this.panel).toBeVisible({ timeout: 120_000 });
}

// After:
async togglePanel() {
  for (let attempt = 0; attempt < 3; attempt++) {
    await this.toggleButton.click();
    try {
      await expect(this.panel).toBeVisible({ timeout: 15_000 });
      return;
    } catch {
      // Click didn't register, retry
    }
  }
  await this.toggleButton.click();
  await expect(this.panel).toBeVisible({ timeout: 30_000 });
}
```

**Fix 2: SidebarPage.deleteAllItems() -- use first() instead of nth(i)**

File: `pages/sidebar.page.ts`

```typescript
// Before:
async deleteAllItems() {
  const count = await this.items.count();
  for (let i = count - 1; i >= 0; i--) {
    await this.items.nth(i).hover();
    await this.deleteButton.click();
  }
}

// After:
async deleteAllItems() {
  let count = await this.items.count();
  while (count > 0) {
    const item = this.items.first();
    await item.scrollIntoViewIfNeeded();
    await item.hover();
    await this.deleteButton.click();
    count = await this.items.count();
  }
}
```

**Fix 3: sidebar.spec.ts afterAll -- ensure panel is open before cleanup**

File: `e2e/ui/sidebar.spec.ts`

```typescript
// Before:
test.afterAll(async () => {
  await sidebarPage.deleteAllItems();
});

// After:
test.afterAll(async () => {
  await sidebarPage.togglePanel();
  await sidebarPage.deleteAllItems();
});
```

Syntax check:
```
npx playwright test --list 2>&1 | head -20
  -> All 48 tests listed successfully, no syntax errors
```

---

## Step 3: Run Tests Locally

```
Running: npx playwright test e2e/ui --workers=1 --headed

Results:
  - Total: 48 tests
  - Passed: 46
  - Failed: 2 (editor.spec.ts tests -- app issue, not test code)
```

---

## Step 4: Report Results

```
| Test                              | CI (Before) | Local (After) | Status             |
|-----------------------------------|-------------|---------------|--------------------|
| sidebar: toggle panel             | FAIL        | PASS          | Fixed              |
| sidebar: delete items             | FAIL        | PASS          | Fixed              |
| sidebar: rename item              | FAIL        | PASS          | Fixed              |
| editor: save changes              | FAIL        | FAIL          | App issue (overlay)|
| editor: undo changes              | FAIL        | FAIL          | Cascade from above |
| sidebar: afterAll cleanup         | FAIL        | PASS          | Fixed              |

Changed files:
  - pages/sidebar.page.ts: Added retry logic to togglePanel(), refactored deleteAllItems() to use first()
  - e2e/ui/sidebar.spec.ts: afterAll now ensures panel is open before cleanup

Remaining failures (app issues):
  - editor.spec.ts: Save button is behind an overlay that does not auto-dismiss. This is a product bug.
```
