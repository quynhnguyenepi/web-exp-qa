# Test Execution Guidelines (Shared)

Shared reference for `/exp-qa-agents:execute-test-case` and `/exp-qa-agents:execute-test-suite`. Both skills read this file during pre-flight.

---

## Login Configuration

### Default Credentials

| Environment | Target URL | Username | Password | Login Method |
|-------------|-----------|----------|----------|-------------|
| RC (default) | `https://rc-app.optimizely.com/signin` | `bdd+test1752566905289@optimizely.com` | `asdfASDF1` | Direct email/password |
| Production | `https://app.optimizely.com` | `exp.auto+3@optimizely.com` | `ABtestingABtesting2022@@1` | OptiID (Okta SSO) via `https://login.optimizely.com` |
| Development | `https://develrc-app.optimizely.com` | `exp.auto+3@optimizely.com` | `ABtestingABtesting2022@@1` | OptiID (Okta SSO) via `https://prep.login.optimizely.com` |

### Feature-Environment Constraints

Some features require OptiID login and are NOT available on RC:

| Feature | Available Environments | Login Method |
|---------|----------------------|-------------|
| Opal Chat (all features) | Production, Development | OptiID (Okta SSO) |
| Brainstorm, Summarize Results, Review Experiment, Get Test Ideas, Generate Copy | Production, Development | OptiID (Okta SSO) |
| Standard Web/Edge/FX features | All (Production, RC, Development) | Per environment |

**Rule:** If test steps involve Opal or AI-powered features, use **Development** environment (not RC) with OptiID login flow.

### RC Login Flow (direct -- default)

1. `browser_navigate` to `https://rc-app.optimizely.com/signin`
2. Wait for login form to load (`browser_wait_for` email input field)
3. `browser_fill` email field with username
4. `browser_fill` password field with password
5. `browser_click` "Sign In" button
6. Wait for dashboard to fully load (verify URL no longer contains `/signin`)
7. `browser_take_screenshot` to confirm successful login
8. If login fails: ask user to resolve, then retry

### Production / Development Login Flow (OptiID)

1. `browser_navigate` to app URL
2. Wait for redirect to OptiID login portal (`browser_wait_for` email input field)
3. `browser_fill` email field with username
4. `browser_click` "Continue" button
5. Wait for OptiID (Okta) password page to load
6. `browser_fill` password field with password
7. `browser_click` "Sign In" button (Okta sign-in)
8. Wait for redirect back to Optimizely app
9. **Select experiment instance:** If an instance selector appears, select the target instance (ask user which instance if not specified)
10. Wait for Optimizely dashboard to fully load
11. `browser_take_screenshot` to confirm successful login
12. If login fails: ask user to resolve, then retry

**Note:** If test steps already include login as step 1, skip the automatic login to avoid double-login. Check if the first test step mentions "Login" or "Sign in" -- if yes, let the test steps handle login directly.

**Between test cases (suite mode only):** Check if session is still active. If redirected to login page, re-login with saved credentials using the appropriate login flow for the environment.

---

## Playwright MCP Action Mapping

This reference helps translate human-readable test steps into Playwright MCP tool calls.

## Action Mapping Reference

### Navigation Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Navigate to [URL]" / "Open [URL]" / "Go to [URL]" | `browser_navigate` | `url: "{URL}"` |
| "Go back" / "Navigate back" | `browser_navigate_back` | — |
| "Go forward" / "Navigate forward" | `browser_navigate_forward` | — |
| "Refresh page" / "Reload page" | `browser_navigate` | `url: "{CURRENT_URL}"` |

### Click Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Click [element]" / "Press [button]" / "Tap [link]" | `browser_click` | `element: "{description}", ref: "{ref_from_snapshot}"` |
| "Double-click [element]" | `browser_click` | `element: "{description}", ref: "{ref}", doubleClick: true` |
| "Right-click [element]" | `browser_click` | `element: "{description}", ref: "{ref}", button: "right"` |

### Text Input Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Type [text] in [field]" / "Enter [text]" | `browser_type` | `text: "{text}"` (after clicking the field) |
| "Fill form with [values]" | `browser_fill_form` | Multiple field-value pairs |
| "Clear [field]" | `browser_type` | Select all + delete, or `browser_press_key("Control+a")` then `browser_press_key("Delete")` |

### Selection Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Select [option] from [dropdown]" | `browser_select_option` | `selector: "{selector}", value: "{value}"` |

### Keyboard Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Press Enter" / "Submit form" | `browser_press_key` | `key: "Enter"` |
| "Press Tab" / "Move to next field" | `browser_press_key` | `key: "Tab"` |
| "Press Escape" / "Close dialog" | `browser_press_key` | `key: "Escape"` |
| "Press [key combination]" | `browser_press_key` | `key: "Control+c"`, `key: "Alt+F4"`, etc. |

### Verification Actions

| Test Step Pattern | Playwright MCP Tool | How to Verify |
|---|---|---|
| "Verify [text] is visible" / "Check [text] appears" | `browser_snapshot` | Search snapshot result for the expected text |
| "Verify [element] exists" / "Check [element] is present" | `browser_snapshot` | Search accessibility tree for element with matching role/name |
| "Verify page title contains [text]" | `browser_snapshot` | Check the page title in snapshot metadata |
| "Verify URL contains [path]" | `browser_snapshot` | Check current URL in snapshot metadata |
| "Verify [element] is NOT visible" | `browser_snapshot` | Confirm element is absent from accessibility tree |

### Wait Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Wait for [text] to appear" | `browser_wait_for` | `text: "{text}"` |
| "Wait for [text] to disappear" | `browser_wait_for` | `textGone: "{text}"` |
| "Wait [N] seconds" | `browser_wait_for` | `time: {N * 1000}` (milliseconds) |
| "Wait for page to load" | `browser_wait_for` | `text: "{expected_text_on_loaded_page}"` |

### File & Dialog Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Upload [file]" | `browser_file_upload` | File path |
| "Accept alert/dialog" | `browser_handle_dialog` | Accept |
| "Dismiss alert/dialog" | `browser_handle_dialog` | Dismiss |
| "Enter [text] in prompt dialog" | `browser_handle_dialog` | Accept with text |

### Screenshot Actions

| Test Step Pattern | Playwright MCP Tool | Parameters |
|---|---|---|
| "Take screenshot" / "Capture screen" | `browser_take_screenshot` | — |
| "Take full page screenshot" | `browser_take_screenshot` | `fullPage: true` |

---

## Verification Strategies

### Strategy 1: Snapshot-Based Verification (Preferred)

Use `browser_snapshot` to capture the accessibility tree and verify expected state:

```
1. Execute action (click, type, navigate)
2. Call browser_snapshot()
3. Parse the accessibility tree response
4. Check if expected text/element is present
5. If found → PASS, if not found → FAIL
```

**Best for:**
- Verifying text content on the page
- Checking element visibility
- Validating form field values
- Confirming navigation to correct page

### Strategy 2: Screenshot-Based Verification (Fallback)

Use `browser_take_screenshot` when snapshot is insufficient:

```
1. Execute action
2. Call browser_take_screenshot()
3. Analyze the visual screenshot
4. Compare with expected visual state
```

**Best for:**
- Visual layout verification
- CSS/styling checks
- Image/icon presence
- Recording failure evidence

### Recommended Approach

1. **Always try snapshot first** — it's faster and more reliable
2. **Use screenshot on failure** — to capture visual evidence for bug reports
3. **Combine both** — snapshot for verification, screenshot for documentation

---

## Common Test Patterns

### Pattern 1: Login Flow

```
Step 1: Navigate to login page
  → browser_navigate({ url: "https://app.example.com/login" })

Step 2: Enter email
  → browser_snapshot() → find email field ref
  → browser_click({ element: "email input", ref: "..." })
  → browser_type({ text: "user@example.com" })

Step 3: Enter password
  → browser_click({ element: "password input", ref: "..." })
  → browser_type({ text: "password123" })

Step 4: Click Login button
  → browser_click({ element: "Login button", ref: "..." })

Step 5: Verify dashboard loads
  → browser_wait_for({ text: "Dashboard" })
  → browser_snapshot() → verify "Dashboard" in response
```

### Pattern 2: Form Submission

```
Step 1: Navigate to form page
  → browser_navigate({ url: "..." })

Step 2: Fill form fields
  → browser_snapshot() → identify all field refs
  → For each field: browser_click + browser_type

Step 3: Submit form
  → browser_click({ element: "Submit button", ref: "..." })

Step 4: Verify success message
  → browser_wait_for({ text: "Success" })
  → browser_snapshot() → verify success message
```

### Pattern 3: CRUD Operations

```
Create:
  → Navigate → Fill form → Submit → Verify item appears in list

Read:
  → Navigate → Verify item details visible

Update:
  → Navigate → Click Edit → Modify field → Save → Verify changes

Delete:
  → Navigate → Click Delete → Confirm dialog → Verify item removed
```

### Pattern 4: Navigation & Menu Testing

```
Step 1: Navigate to home page
  → browser_navigate({ url: "..." })

Step 2: Click menu item
  → browser_snapshot() → find menu element ref
  → browser_click({ element: "Menu item", ref: "..." })

Step 3: Verify submenu/page
  → browser_snapshot() → verify expected content
```

---

## Error Handling Patterns

### Element Not Found

If `browser_snapshot` doesn't show the expected element:
1. Try `browser_wait_for({ text: "..." })` first — element may still be loading
2. If still not found after wait, take screenshot and mark as FAILED
3. Record which element was expected but not found

### Action Failed

If `browser_click` or `browser_type` fails:
1. Take a snapshot to see current page state
2. Check if the element ref has changed (dynamic page)
3. If element is obscured, try scrolling: `browser_evaluate({ script: "window.scrollTo(0, 500)" })`
4. If still failing, take screenshot and mark as FAILED

### Page Load Timeout

If `browser_navigate` or `browser_wait_for` times out:
1. Take screenshot to see current state
2. Check if page partially loaded
3. Try refreshing: `browser_navigate({ url: current_url })`
4. If still failing, mark as FAILED with timeout error

### Dialog Interruption

If an unexpected dialog appears:
1. Use `browser_handle_dialog` to dismiss it
2. Resume test execution from the interrupted step
3. Note the dialog in the test report

---

## Bug Ticket Description Template

When creating JIRA bug tickets for failed test cases, use this template:

```
h3. Summary
Test case "{TEST_CASE_TITLE}" failed during automated execution via Playwright MCP.

h3. Steps to Reproduce
{For each step in the test case, list with pass/fail status:}
1. [PASS] {Step 1 description}
2. [PASS] {Step 2 description}
3. [FAIL] {Step 3 description} ← Failed here

h3. Expected Result
{Expected result from the test case for the failed step}

h3. Actual Result
{What was actually observed — from snapshot analysis or error message}

h3. Environment
- Target URL: {URL}
- Execution Date: {DATE}
- Browser: Chromium (via Playwright MCP)
- Executed By: Claude Code / /exp-qa-agents:execute-test-case skill

h3. Additional Context
- Source Test Case: {JIRA_KEY or "Manual input"}
- Failed at Step: {N}/{TOTAL}
- Pass Rate for Suite: {X}% ({PASSED}/{TOTAL} passed)

_Bug is created by CLAUDE CODE_
```

**IMPORTANT:** After creating each bug ticket, always add a comment to the new ticket:
```
mcp__atlassian__jira_add_comment({
  issue_key: "{NEW_BUG_KEY}",
  body: "Bug is created by CLAUDE CODE via /exp-qa-agents:execute-test-case skill."
})
```

---

## Best Practices

1. **Always snapshot before acting** — understand the page state before performing actions
2. **Use element descriptions, not selectors** — Playwright MCP uses the accessibility tree, so describe elements by their role and label (e.g., "Login button", "Email input")
3. **Wait after navigation** — always `browser_wait_for` after `browser_navigate` to ensure the page is loaded
4. **One action per step** — keep test steps atomic for clear pass/fail tracking
5. **Screenshot on every failure** — always capture visual evidence before moving to the next test case
6. **Reset between tests** — navigate to the target URL between test cases to ensure a clean state
7. **Handle dynamic content** — use `browser_wait_for` for content that loads asynchronously
8. **Ref values from snapshots** — always get element `ref` values from `browser_snapshot` before using them in `browser_click` or other actions; never hardcode refs
