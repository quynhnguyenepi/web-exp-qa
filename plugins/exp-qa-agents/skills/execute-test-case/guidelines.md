# Test Execution Guidelines (Shared)

Shared reference for `/exp-qa-agents:execute-test-case` and `/exp-qa-agents:execute-test-suite`. Both skills read this file during pre-flight.

---

## Login Configuration

### Default Credentials

| Environment | SSO URL (App URL) | OptiID URL | Username | Password | Login Method |
|-------------|-------------------|-----------|----------|----------|-------------|
| RC (default) | `https://rc-app.optimizely.com/signin` | N/A | `bdd+test1752566905289@optimizely.com` | `asdfASDF1` | Direct email/password |
| Production | `https://app.optimizely.com` | `https://login.optimizely.com` | `exp.auto+3@optimizely.com` | `ABtestingABtesting2022@@1` | SSO or OptiID |
| Development | `https://develrc-app.optimizely.com` | `https://prep.login.optimizely.com` | `exp.auto+3@optimizely.com` | `ABtestingABtesting2022@@1` | SSO or OptiID |

### Feature-Environment Constraints

Some features require OptiID login and are NOT available on RC:

| Feature | Available Environments | Login Method |
|---------|----------------------|-------------|
| Opal Chat (all features) | Production, Development | OptiID |
| Brainstorm, Summarize Results, Review Experiment, Get Test Ideas, Generate Copy | Production, Development | OptiID |
| Standard Web/Edge/FX features | All (Production, RC, Development) | Per environment |

**Rule:** If test steps involve Opal or AI-powered features, use **Production** environment (not RC) with OptiID login flow. Production URL: `https://login.optimizely.com`. Development (`https://prep.login.optimizely.com`) also supports these features but Production is the default.

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

1. `browser_navigate` to the **login URL directly**:
   - Production: `https://login.optimizely.com`
   - Development: `https://prep.login.optimizely.com`
2. Wait for OptiID login page to load (`browser_wait_for` email input field)
3. `browser_fill` email field with username
4. `browser_click` "Next" button
5. Wait for "Verify with your password" page to load
6. `browser_fill` password field with password
7. `browser_click` "Verify" button
8. Wait for redirect to Optimizely app
9. **Select experiment instance:** If an instance selector appears, select "Experimentation" (or ask user which instance if not specified)
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
| "Take screenshot" / "Capture screen" | `browser_take_screenshot` | `filename: "{TC_folder}/step-{N}.png"` |
| "Take full page screenshot" | `browser_take_screenshot` | `fullPage: true, filename: "{TC_folder}/step-{N}-full.png"` |

**Screenshot Folder Convention:**
- Each test case saves screenshots into `{TC_ID} Result/` folder (use TC ID only, not the full title)
- Always use the `filename` parameter to specify the relative path
- Examples:
  - Single TC: `TC-P0-01 Result/step-1.png`
  - Suite TC: `TC-P0-03 Result/step-3.png`

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

### Screenshot Policy (STRICT — Cost Control)

**This policy is NON-NEGOTIABLE. Capturing extra screenshots wastes significant cost.**

Only capture `browser_take_screenshot` for the **last 2 steps** of each test case AND at **any step that fails**. All other steps execute without screenshots.

- **Steps 1 to N-2 (early/middle steps):** Execute action ONLY. Use `browser_snapshot` ONLY when needed to find element refs for interaction (e.g., `browser_click`). Do NOT call `browser_take_screenshot`. No .png files saved for these steps.
- **Steps N-1 and N (last 2 steps):** MUST capture `browser_snapshot` + `browser_take_screenshot` for evidence.
- **ANY step that FAILS (MANDATORY):** IMMEDIATELY capture `browser_snapshot` + `browser_take_screenshot` at the failure point, regardless of step position. Save to `{TC_ID} Result/step-{N}-FAIL.png`.
- **Login/setup steps:** NEVER capture screenshots during login flow or navigation to test starting point. These are setup, not test evidence.

**Screenshot budget per test case:**
- TC PASSES: exactly **2 screenshots** (step N-1 and step N)
- TC FAILS at step K: exactly **1 screenshot** at the failure step (`step-{K}-FAIL.png`)

**FORBIDDEN (most common mistakes from real executions):**
- Capturing screenshots for steps 1 through N-2 (early/middle steps that pass)
- Capturing screenshots during login flow (entering email, clicking Next, etc.)
- Capturing multiple screenshots for the same step (e.g., `step-15.png` AND `step-15-expanded.png`)
- Capturing "extra evidence" or "documentation" screenshots beyond the budget
- Capturing screenshots for ALL steps of a test case (e.g., 7 screenshots for a 7-step TC)

### MANDATORY Evidence Capture Rules (Lessons Learned)

These rules are NON-NEGOTIABLE. Violations were observed in real executions and must be prevented:

**Rule 1: At MINIMUM 2 screenshots per test case, plus 1 for each failed step.**
- Before executing the last 2 steps, calculate: `last_2 = [total_steps - 1, total_steps]`
- If the test case PASSES: exactly 2 screenshots (last 2 steps)
- If the test case FAILS at step K (before last 2): at minimum 1 screenshot at the failure step (`step-{K}-FAIL.png`). If the last 2 steps are reached, also capture those.
- After completing a TC, self-verify: "Did I capture a screenshot for every failed step AND for the last 2 steps I reached?"
- If you captured fewer screenshots than required, you MUST go back and capture the missing screenshots before moving to the next TC

**Rule 2: Screenshot naming MUST use the folder convention.**
- Format: `{TC_ID} Result/step-{N}.png`
- Example: `TC-P0-01 Result/step-15.png`
- NEVER use arbitrary names like `tc-p0-01-step15.png` or `screenshot-1.png`
- ALWAYS pass the `filename` parameter to `browser_take_screenshot`

**Rule 3: Create all result folders BEFORE execution starts.**
- Before executing the first test case, create ALL result folders for every TC in the suite
- Use `mkdir -p "{TC_ID} Result/"` for each test case
- This prevents file-not-found errors during screenshot saving

**Rule 4: Quality must NOT degrade across test cases.**
- Common failure pattern: First TC is done correctly, but later TCs get rushed with missing evidence
- Treat EVERY test case with the same rigor as the first one
- After each TC completes, perform this checklist:
  - [ ] If TC PASSED: 2 screenshots saved (last 2 steps)?
  - [ ] If TC FAILED: screenshot saved at the failure step (`step-{K}-FAIL.png`)?
  - [ ] All screenshots in `{TC_ID} Result/` folder with correct naming?

**Rule 5: ALWAYS capture a screenshot when a step FAILS — this is the most important screenshot.**
- A failure without a screenshot means the user must re-run the entire test case just to see what went wrong
- On failure, IMMEDIATELY capture: `browser_take_screenshot(filename: "{TC_ID} Result/step-{N}-FAIL.png")`
- Also capture `browser_snapshot` to record the accessibility tree state at failure
- This rule takes HIGHEST PRIORITY — even if you skip other screenshots, NEVER skip a failure screenshot

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

1. **Screenshot budget is strict** — exactly 2 screenshots for passing TCs (last 2 steps), exactly 1 for failing TCs (failure step). No more. For early steps, only use `browser_snapshot` when you need element refs for interaction. NEVER capture screenshots during login or setup steps
2. **Save screenshots in TC folder** — always use `filename: "{TC_ID} Result/step-{N}.png"` to organize screenshots by test case. Never save screenshots in the root directory. After each TC, verify screenshot count matches the budget
3. **Use element descriptions, not selectors** — Playwright MCP uses the accessibility tree, so describe elements by their role and label (e.g., "Login button", "Email input")
3. **Wait after navigation** — always `browser_wait_for` after `browser_navigate` to ensure the page is loaded
4. **One action per step** — keep test steps atomic for clear pass/fail tracking
5. **Screenshot on failure** — always capture visual evidence on failure regardless of step position
6. **Reset between tests** — navigate to the target URL between test cases to ensure a clean state
7. **Handle dynamic content** — use `browser_wait_for` for content that loads asynchronously
8. **Ref values from snapshots** — always get element `ref` values from `browser_snapshot` before using them in `browser_click` or other actions; never hardcode refs

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| playwrightA MCP not available | Exit with error: "playwrightA MCP is not configured. See .mcp.json.template for detailed configuration." |
| No test steps provided | Ask user to provide test steps (text, image, or file) |
| Unclear expected outcome | Ask user to clarify before executing that step |
| Element not found | Screenshot + snapshot, mark step FAIL, ask user to continue/retry/stop |
| Browser crashes | Report error, offer to restart browser and resume from last step |
| Login fails (wrong credentials, MFA) | Ask user to provide correct credentials or resolve MFA, retry login |
| Session expired mid-test | Re-login with saved credentials, resume from current step |


## Self-Correction

1. **"Page needs more time"** -> Add `browser_wait_for` before re-checking
2. **"Use different credentials"** -> Ask for new username/password, re-login
3. **"Retry step {N}"** -> Re-execute just that step with fresh snapshot
4. **"The expected outcome should be X"** -> Update expected, re-evaluate verdict
5. **"Use a different browser"** -> Close current, relaunch with new browser
