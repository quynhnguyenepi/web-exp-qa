# Test Design Document: CJS-9865

**Ticket:** [CJS-9865 - Creating variations within new VE](https://optimizely-ext.atlassian.net/browse/CJS-9865)
**Epic:** CJS-10559 - Visual Editor Rebuild (M5)
**Product:** Web Experimentation - Visual Editor
**Created:** 2026-03-12

---

## Executive Summary

**Feature:** Variation creation via + button in Visual Editor

**Acceptance Criteria:**
- ✅ AC1: Add a + button after the variation list
- ✅ AC2: Clicking the + button should create a new variation

**Implementation:**
- + button UI component
- Inline name input with suggested names ("Variation #1", "#2", etc.)
- Name validation (required, unique, max 500 chars)
- Keyboard shortcuts (Enter to create, Escape to cancel)
- Automatic traffic redistribution among non-archived variations
- Auto-selection of newly created variation
- Segment event tracking

**Test Site:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html (Commerce site with snippet injected)

---

## Test Cases Summary

| # | Title | Priority | Labels | Type |
|---|-------|----------|--------|------|
| TC-01 | [CJS-9865] Full Flow - Create Variation, Preview, Publish, and Verify on Site (A/B Test) | Critical | new_ve,variation,web | Regression / Full Flow |
| ~~TC-02~~ | ~~Removed — covered by smoke test [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015)~~ | — | — | — |
| TC-03 | [CJS-9865] Verify Variation Creation - Create 3 Consecutive Variations (Campaign) | High | new_ve,variation,web | Regression |
| TC-04 | [CJS-9865] Verify Traffic Redistribution - 100% to 50/50 Split (MVT) | High | new_ve,variation,web | Regression |
| TC-05 | [CJS-9865] Verify Validation - Empty Variation Name Error | High | new_ve,variation,web | Regression |
| TC-06 | [CJS-9865] Verify Validation - Duplicate Variation Name Error | High | new_ve,variation,web | Regression |
| TC-07 | [CJS-9865] Verify Validation - 501-Character Name Error | Normal | new_ve,variation,web | Regression |
| TC-08 | [CJS-9865] Verify Validation - Whitespace-Only Name Error | Normal | new_ve,variation,web | Regression |
| TC-09 | [CJS-9865] Verify Cancellation - Escape Key During Creation | Normal | new_ve,variation,web | Regression |
| TC-10 | [CJS-9865] Verify Cancellation - Click X Button During Creation | Normal | new_ve,variation,web | Regression |
| TC-11 | [CJS-9865] Verify Edge Case - Create with 500-Character Name (Boundary) | Normal | new_ve,variation,web | Regression |
| TC-12 | [CJS-9865] Verify Edge Case - Create with Special Characters in Name | Low | new_ve,variation,web | Regression |
| TC-13 | [CJS-9865] Verify Edge Case - Create When Archived Variation Exists | Normal | new_ve,variation,web | Regression |
| TC-14 | [CJS-9865] Verify Edge Case - Gaps in Variation Numbering | Low | new_ve,variation,web | Regression |
| TC-15 | [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Running | High | new_ve,variation,web | Regression |
| TC-16 | [CJS-9865] Verify Dynamic Websites Support ON - Variation Created Successfully | High | new_ve,variation,web | Regression |
| TC-17 | [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Paused | Normal | new_ve,variation,web | Regression |
| TC-18 | [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Concluded (Only) | Normal | new_ve,variation,web | Regression |
| TC-19 | [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Concluded + Deployed | Normal | new_ve,variation,web | Regression |
| TC-20 | [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Archived | Normal | new_ve,variation,web | Regression |
| TC-21 | [CJS-9865] Verify Monolith Reflection - New Variation Appears Correctly on All Experiment Detail Screens | High | new_ve,variation,web | Regression |
| TC-22 | [CJS-9865] Verify Multi-Page - Create Variation When Experiment Targets Multiple Saved Pages | Normal | new_ve,variation,web | Regression |
| TC-23 | [CJS-9865] Verify Feature Interaction - Unsaved Changes Warning Shown When Switching to New Variation | Normal | new_ve,variation,web | Regression |
| TC-24 | [CJS-9865] Verify Feature Interaction - Create Variation While Interactive Mode Is Active | Normal | new_ve,variation,web | Regression |
| TC-25 | [CJS-9865] Verify Snippet Updated - New Variation in weightDistributions, variations[], and revision After Publish | High | new_ve,variation,web | Regression |

> **Note:** TC-02 (basic variation creation, custom name, MAB) is covered by smoke test [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015) and removed from this document to avoid duplication. All cases in this document are **regression cases** — smoke testing is handled by [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015).

**Total Test Cases:** 24 (all regression)
**Coverage Distribution:**
- **Critical:** 1 (4%)
- **High:** 7 (29%)
- **Normal:** 14 (58%)
- **Low:** 2 (8%)

**Test Type Distribution:**
- **Regression / Full Flow:** 1 test case (4%) — TC-01 (complete end-to-end verification)
- **Regression:** 22 test cases (96%) — TC-03 to TC-24

---

## Detailed Test Cases

---

### TC-01: [CJS-9865] Full Flow - Add Variation, Change Element, Preview, Publish, and Verify on Site (A/B Test)

**Priority:** Critical | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type that has variations: Original, Variation #1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar after the last variation tab and press Enter to create "Variation #2"
3. Set traffic allocation: Variation #2 = 100%, Original = 0%, Variation #1 = 0%
4. Click on a visible element (e.g., hero banner heading), change its text to "Test Heading - Variation #2", then Save
5. Click Preview for "Variation #2"
6. Close preview, return to Visual Editor
7. Click the experiment-level Preview button (QA ball)
8. Close preview, return to Visual Editor and click Publish
9. Open the website in a new incognito tab and force bucket into "Variation #2"

**Expected Results:**
5. Variation preview shows "Test Heading - Variation #2" applied correctly
7. Experiment preview shows "Test Heading - Variation #2" applied correctly
9. "Test Heading - Variation #2" is visible on the live website after bucketing into "Variation #2"

---

> **TC-02 removed** — Basic variation creation (custom name, MAB) is covered by smoke test [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015).

---

### TC-03: [CJS-9865] Verify Variation Creation - Create 3 Consecutive Variations (Campaign)

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created campaign that has two experiences: experience#1 with holdback 5% and variation#1: 95%
- Campaign is in Draft status
- User is logged in and navigated to Experience #1

**Parameters:**
- Experiment type: Personalization Campaign
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar, press Enter to accept "Variation #2"
3. Click the + button at the bottom bar again, press Enter to accept "Variation #3"
4. Click the + button at the bottom bar again, press Enter to accept "Variation #4"
5. Observe the traffic allocation across all variations

**Expected Results:**
5. Final traffic: Original ~20%, Variation #1 ~20%, Variation #2 ~20%, Variation #3 ~20%, Variation #4 ~20%

---

### TC-04: [CJS-9865] Verify Traffic Redistribution - 100% to 50/50 Split (MVT)

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created MVT experiment with at least two sections
- Section 1 has only Original variation with 100% traffic
- Experiment is in Draft status
- User is logged in and navigated to Section 1

**Parameters:**
- Experiment type: Multivariate Test (MVT)
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Confirm Original variation shows 100% traffic allocation
3. Click the + button at the bottom bar after Original variation
4. Press Enter to accept suggested name "Variation #1"
5. Observe the traffic allocation

**Expected Results:**
5. Traffic allocation: Original 50%, Variation #1 50%

---

### TC-05: [CJS-9865] Verify Validation - Empty Variation Name Error

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar after the last variation
3. Clear all text from the input field (delete suggested name)
4. Press Enter key with empty input
5. Observe the error notification that appears

**Expected Results:**
5. Error notification: "Please choose a name for your variation."
6. No new variation tab is created

---

### TC-06: [CJS-9865] Verify Validation - Duplicate Variation Name Error

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment MAB test type with variations: original, "Test Variation"
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: Multi-Armed Bandit
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Confirm existing variation named "Test Variation" exists
3. Click the + button at the bottom bar to create a new variation
4. Clear the suggested name and type "Test Variation" (exact match to existing)
5. Press Enter key
6. Observe the error notification

**Expected Results:**
6. Error notification: "Please choose a unique name for your variation."
7. No duplicate "Test Variation" tab is created

---

### TC-07: [CJS-9865] Verify Validation - 501-Character Name Error

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF
- Test Data: 501-character string = "a" repeated 501 times

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Clear the suggested name
4. Paste a 501-character string (e.g., "a" repeated 501 times) into the input field
5. Press Enter key
6. Observe the error notification

**Expected Results:**
6. Error notification: "Variation name must be no longer than 500 characters."

---

### TC-08: [CJS-9865] Verify Validation - Whitespace-Only Name Error

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created campaign with experience#1: holdback 5%, variation#1: 95%
- Campaign is in Draft status
- User is logged in and navigated to Experience #1

**Parameters:**
- Experiment type: Personalization Campaign
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF
- Test Data: "   " (3 spaces)

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Clear the suggested name and enter only whitespace characters (e.g., "   ")
4. Press Enter key
5. Observe the error notification

**Expected Results:**
5. Error notification: "Please choose a name for your variation." (whitespace-only treated as empty)

---

### TC-09: [CJS-9865] Verify Cancellation - Escape Key During Creation

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment MVT with at least one section
- Experiment is in Draft status
- User is logged in and navigated to Section 1

**Parameters:**
- Experiment type: Multivariate Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Observe the input field with suggested name
4. Press Escape key

**Expected Results:**
4. Input field closes; no new variation tab is created

---

### TC-10: [CJS-9865] Verify Cancellation - Click X Button During Creation

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Observe the input field with X button on the right
4. Click the X button (cancel button)

**Expected Results:**
4. Input field closes; no new variation tab is created

---

### TC-11: [CJS-9865] Verify Edge Case - Create with 500-Character Name (Boundary)

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment MAB test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: Multi-Armed Bandit
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF
- Test Data: 500-character string (exactly 500 "a" characters)

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Clear suggested name and paste exactly 500 characters (e.g., "a" repeated 500 times)
4. Press Enter key

**Expected Results:**
4. New variation tab is created with 500-character name; traffic redistributed

---

### TC-12: [CJS-9865] Verify Edge Case - Create with Special Characters in Name

**Priority:** Low | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF
- Test Data: "Test <>&\"'@#$%^* Variation"

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar
3. Clear suggested name and type: "Test <>&\"'@#$%^* Variation"
4. Press Enter key

**Expected Results:**
4. Variation tab displays: "Test <>&\"'@#$%^* Variation" (special characters rendered correctly, not escaped)

---

### TC-13: [CJS-9865] Verify Edge Case - Create When Archived Variation Exists

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original (100% traffic), archived_variation (0% traffic, archived=true)
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Confirm Original shows 100% traffic, archived variation shows 0% and is hidden/grayed
3. Click the + button at the bottom bar
4. Press Enter to accept "Variation #1"
5. Observe the traffic allocation

**Expected Results:**
5. Traffic: Original 50%, Variation #1 50% — archived variation remains at 0%, excluded from redistribution

---

### TC-14: [CJS-9865] Verify Edge Case - Gaps in Variation Numbering

**Priority:** Low | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, "Variation #1", "Variation #5" (note: #2, #3, #4 were deleted)
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Confirm existing variations: Original, "Variation #1", "Variation #5"
3. Click the + button at the bottom bar
4. Observe the suggested name in the input field
5. Press Enter to accept the suggested name

**Expected Results:**
4. Input field suggests "Variation #6" (highest number + 1, not first gap #2)
5. New variation "Variation #6" is created

---

### TC-15: [CJS-9865] Verify Read-Only Mode - + Button Hidden in Published Experiment

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Running status (published)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Verify experiment status shows "Running"
2. Open variation in Visual Editor
3. Wait for Visual Editor to load
4. Observe the variation tabs area
5. Observe the variation tabs area for the + button

**Expected Results:**
5. + button is NOT visible (read-only mode for Running status)

---

### TC-16: [CJS-9865] Verify Dynamic Websites Support ON - Variation Created Successfully

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- Project settings: "Enable Support for Dynamic Websites" is ON
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: ON

**Test Steps:**
1. Confirm "Enable Support for Dynamic Websites" toggle is ON in Project Settings
2. Open variation in Visual Editor
3. Click the + button at the bottom bar after the last variation
4. Press Enter to accept suggested "Variation #2"

**Expected Results:**
4. "Variation #2" is created and selected; traffic redistributed correctly

---

### TC-17: [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Paused

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment has been Started then Paused (status: Paused)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Experiment status: Paused

**Test Steps:**
1. Verify experiment status shows "Paused"
2. Open variation in Visual Editor
3. Wait for Visual Editor to load
4. Observe the variation tabs area
5. Observe the variation tabs area for the + button

**Expected Results:**
5. + button is NOT visible (read-only mode for Paused status)

---

### TC-18: [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Concluded (Only)

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment was Concluded without ever being published/deployed (concluded from Draft or Paused)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Experiment status: Concluded (never deployed to production)

**Test Steps:**
1. Verify experiment status shows "Concluded"
2. Verify experiment has no published snippet (was never Running)
3. Open variation in Visual Editor
4. Wait for Visual Editor to load
5. Observe the variation tabs area
6. Observe the variation tabs area for the + button

**Expected Results:**
6. + button is NOT visible (read-only mode for Concluded status — never deployed)

---

### TC-19: [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Concluded + Deployed

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment was Running (published to CDN) then Concluded — snippet.js is still live on CDN
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Experiment status: Concluded (was previously Running/deployed)

**Test Steps:**
1. Verify experiment status shows "Concluded"
2. Verify experiment was previously Running (has a published revision in History)
3. Open variation in Visual Editor
4. Wait for Visual Editor to load
5. Observe the variation tabs area
6. Observe the variation tabs area for the + button

**Expected Results:**
6. + button is NOT visible (read-only mode for Concluded + Deployed status)

---

### TC-20: [CJS-9865] Verify Read-Only Mode - + Button Hidden When Experiment is Archived

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment has been Archived
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Experiment status: Archived

**Test Steps:**
1. Verify experiment status shows "Archived"
2. Open variation in Visual Editor
3. Wait for Visual Editor to load
4. Observe the variation tabs area
5. Observe the variation tabs area for the + button

**Expected Results:**
5. + button is NOT visible (read-only mode for Archived status)

---

### TC-21: [CJS-9865] Verify Monolith Reflection - New Variation Appears Correctly on All Experiment Detail Screens

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click the + button at the bottom bar and create new variation named "Hero Banner Change"
3. Press Enter to confirm the name
4. Navigate to Monolith experiment detail → Variations tab
5. Navigate to experiment Summary tab
6. Navigate to Design → Traffic Allocation section
7. Navigate to Settings → API Names tab
8. Navigate to History tab

**Expected Results:**
4. Monolith Variations tab: "Hero Banner Change" appears as "C Hero Banner Change" with correct traffic %
5. Summary > Variations section: "Hero Banner Change" is listed with correct redistributed traffic % (e.g., Original 0%, Variation #1 ~33%, Hero Banner Change ~33%)
6. Design > Traffic Allocation: "Hero Banner Change" appears in Variation Traffic Distribution with correct % slider value alongside other variations
7. Settings > API Names > Variations section: "Hero Banner Change" is listed by name with its unique numeric variation ID
8. History: variation creation logged with correct user and timestamp

---

### TC-22: [CJS-9865] Verify Multi-Page - Create Variation When Experiment Targets Multiple Saved Pages

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment targets 2 saved pages: "Homepage" (https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html) and "Products Page" (another URL)
- Both pages are configured in Activation tab
- Experiment is in Draft status
- User is logged in and navigated to the experiment on "Homepage"

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Saved pages: 2 pages (Homepage + Products Page)
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Confirm Page Switcher shows "Homepage" as current page
3. Click the + button at the bottom bar, press Enter to create "Variation #2"
4. Use Page Switcher to switch to "Products Page"
5. Observe the variation tabs on Products Page

**Expected Results:**
5. Variation tabs on Products Page show: A Original, B Variation #1, C Variation #2 (variation available across all pages)

---

### TC-23: [CJS-9865] Verify Feature Interaction - Unsaved Changes Warning Shown When Switching to New Variation

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Click on "Variation #1" tab to make it active
3. Click on an element and make a change (e.g., change text) — do NOT click Save
4. Click the + button at the bottom bar to create a new variation
5. Observe what appears
6. Click "Discard" in the warning dialog

**Expected Results:**
5. Unsaved changes warning dialog appears with "Save" and "Discard" options
6. After discarding: new variation input field appears; unsaved change is gone

---

### TC-24: [CJS-9865] Verify Feature Interaction - Create Variation While Interactive Mode Is Active

**Priority:** Normal | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly
- Created experiment A/B test type with variations: original, variation#1
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open variation in Visual Editor
2. Hold Alt key (or click interactive mode toggle) to activate interactive mode
3. While interactive mode is active, click the + button at the bottom bar
4. Observe what appears
5. Press Enter to accept the suggested name

**Expected Results:**
4. Input field appears (+ button is accessible while interactive mode is active)
5. "Variation #2" is created and selected

---

### TC-25: [CJS-9865] Verify Snippet Updated - New Variation in weightDistributions, variations[], and revision After Publish

**Priority:** High | **Labels:** new_ve,variation,web

**Pre-condition:**
- Created a public website that has injected snippet correctly (snippet URL: `https://cdn.optimizely.com/js/{projectId}.js`)
- Created experiment A/B test type with variations: Original (100% traffic), Variation #1 (0% traffic)
- Experiment is in Draft status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open the test website in a new tab, open DevTools > Network tab, filter for `{projectId}.js`
2. Note the current `project_code_revision` value from the snippet JSON response (call it revision R)
3. Open Variation #1 in Visual Editor
4. Click the + button at the bottom bar, press Enter to create "Variation #2"
5. Set traffic allocation: Variation #2 = 100%, Original = 0%, Variation #1 = 0%
6. Click on a visible element, change its text to "Snippet Verify Heading", Save
7. Click Publish
8. Wait 30 seconds, then hard-refresh the test website
9. In DevTools > Network, inspect the refreshed snippet JSON response — check 3 fields: `project_code_revision`, experiment `weightDistributions`, experiment `variations[]`

**Expected Results:**
9a. `project_code_revision` = R+1 (revision incremented after publish)
9b. Experiment `weightDistributions`:
    - "Variation #2": `endOfRange` = 10000 (100%)
    - "Variation #1": `endOfRange` = 0 (0%)
    - "Original": `endOfRange` = 0 (0%)
9c. Experiment `variations[]` contains a new entry with:
    - ID matching the numeric variation ID shown in Monolith > Settings > API Names > Variations
    - Name = "Variation #2" (total variations count = 3)

---

## Test Execution Notes

### TC-01 Full Flow Verification Points

**3 checkpoints to verify the change is applied:**
1. **Preview variation** (step 4) — change visible in VE variation preview
2. **Preview experiment** (step 6) — change visible via QA ball experiment preview
3. **Live website** (step 9) — change visible after bucketing on published site

**Force bucketing method:**
- Use the Optimizely QA URL parameter or the QA ball to force bucket into "Variation #2"
- Verify in browser that the variation is active before checking the change

### Traffic Redistribution Formula
When creating a new variation:
- **Current variations (non-archived):** N
- **New variation count:** N + 1
- **Multiplier:** N / (N + 1)
- **Each existing variation's new weight:** `oldWeight * multiplier`
- **New variation's weight:** `10000 - sum(existing weights)`

Examples:
- 1 → 2 variations: 10000 → 5000/5000
- 2 → 3 variations: 5000/5000 → 3333/3333/3334
- 3 → 4 variations: 3333/3333/3334 → 2500/2500/2500/2500

### Known Limitations
1. Variation name truncation in UI if exceeds ~50 characters (full name saved in backend)
2. + button hidden when experiment is in any read-only status: Running, Paused, Concluded (only), Concluded + Deployed, or Archived
3. MVT uses different API endpoint: `/sections/{sectionId}` instead of `/experiments/{id}`
4. "Concluded (only)" = concluded without ever running/deploying; "Concluded + Deployed" = was Running before being concluded (snippet still on CDN)

---

## Coverage Summary

### By Test Type
- **Regression / Full Flow:** 1 test case (4%) — TC-01 (complete end-to-end, preview, publish, live site)
- **Regression:** 22 test cases (96%) — TC-03 to TC-24

> TC-02 removed — covered by smoke test [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015). All cases in this document are regression.

### By Priority
- **Critical:** 1 test case (4%) — TC-01 (Full Flow)
- **High:** 7 test cases (29%) — TC-03, TC-04, TC-05, TC-06, TC-15, TC-16, TC-21, TC-25
- **Normal:** 14 test cases (58%) — TC-07 to TC-14, TC-17 to TC-20, TC-22 to TC-24
- **Low:** 2 test cases (8%) — TC-12, TC-14

### By Experiment Type
- **A/B Test:** 16 test cases
- **MAB:** 2 test cases
- **MVT:** 3 test cases
- **Campaign:** 2 test cases

### Functional Coverage
✅ **Core Functionality:**
- Create variation with default name
- Create variation with custom name
- Create 3 consecutive variations
- Traffic redistribution (100% → 50/50, evenly across 3+)
- MVT section support (different API endpoint)
- Auto-selection of new variation

✅ **Validation:**
- Empty name error
- Duplicate name error
- 501-character name error
- Whitespace-only name error

✅ **User Experience:**
- Escape key cancellation
- X button cancellation
- Keyboard shortcuts (Enter/Escape)

✅ **Edge Cases:**
- 500-character boundary
- Special characters in name
- Archived variations present
- Gaps in variation numbering

✅ **Read-Only Status Coverage (ALL 5 statuses):**
- Running → TC-15
- Paused → TC-17
- Concluded (only, never deployed) → TC-18
- Concluded + Deployed (was Running) → TC-19
- Archived → TC-20

✅ **Cross-Repo Monolith Screens (D2):**
- Variations tab: name, traffic %, prefix (A/B/C) → TC-21
- Summary > Variations section: name + redistributed traffic % → TC-21
- Design > Traffic Allocation: variation listed in Variation Traffic Distribution with % slider → TC-21
- Settings > API Names: variation listed by name + unique numeric ID → TC-21
- History tab: action logged with user and timestamp → TC-21

✅ **VE Feature Interactions (D3):**
- Unsaved changes warning on tab switch → TC-23
- Interactive mode active while creating variation → TC-24

✅ **Multiple Saved Pages (D4):**
- Experiment with 2+ saved pages → TC-22
- Page switching verification → TC-22

✅ **Project Settings:**
- Dynamic Websites ON/OFF → TC-16

✅ **Full End-to-End Flow (TC-01):**
- Create variation → Change element → Preview → Publish → Verify on live site
- Console log verification
- Network request verification
- Segment event tracking
- CDN snippet upload
- Live site bucketing and change application

✅ **Snippet-Level Verification (TC-25):**
- New variation ID present in snippet `variations[]` array (ID matches Monolith API Names)
- Snippet `weightDistributions` reflects correct `endOfRange` values (scale 0–10000)
- Snippet `project_code_revision` incremented after publish

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Traffic redistribution bug (incorrect %) | Low | High | TC-01, TC-03, TC-04 test all redistribution scenarios |
| Race condition (rapid creation) | Low | Medium | Not covered - recommend manual exploratory test |
| Session expiry during creation | Low | Low | Not covered - out of scope |
| Special char encoding in API | Low | Medium | TC-12 covers XSS-prone characters |
| MVT section API difference | Low | High | TC-04 specifically tests MVT |

---

## Test Environment

**Application URL:** https://develrc-app.optimizely.com
**Login:** OptiID (Okta SSO) via https://prep.login.optimizely.com
**Test Website:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html
**Browser:** Chrome (latest)
**Project:** Visual Editor Test Project
**Instance:** QA Test Instance

**Note:** Test cases assume user is already logged in and navigated to the experiment. Login steps (1-4) are removed to streamline test execution.

---

## Next Steps

1. ✅ **Review test cases** - Optimized with user feedback
2. ⏳ **Upload to JIRA** - Create test case tickets linked to CJS-9865
3. ⏳ **Execute tests** - Run test cases against Development environment
4. ⏳ **Log bugs** - Create bug tickets for any failures
5. ⏳ **Update status** - Mark CJS-9865 as "Tested" after execution

---

**Document Version:** 1.6
**Last Updated:** 2026-03-13
**Author:** Claude Code (exp-qa-agents:web-analyze-ticket)
**Optimizations:** v1.1 — Removed login steps, consolidated console/network checks to TC-01 full flow only. v1.2 — Added TC-17 to TC-24 based on 5-Dimension Cross-Impact Checklist. v1.3 — TC-02 removed (covered by [CJS-11015](https://optimizely-ext.atlassian.net/browse/CJS-11015)); TC-16 priority → High. v1.4 — All cases converted to regression (smoke handled by CJS-11015); removed Website and Environment lines from all Parameters; removed URL from pre-conditions
