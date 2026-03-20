# Test Design Document: CJS-10765

**Ticket:** [CJS-10765 - Develop ChangeLog Component](https://optimizely-ext.atlassian.net/browse/CJS-10765)
**Epic:** CJS-9699 — Using Opal to build entire variations
**Product:** Web Experimentation - Visual Editor
**PRs:** [#411](https://github.com/optimizely/visual-editor/pull/411) (original) + [#432](https://github.com/optimizely/visual-editor/pull/432) (improvements)
**Created:** 2026-03-20

---

## Executive Summary

**Feature:** New ChangeLog component in Visual Editor bottom bar with 2 tabs:
- **Preview tab** — Opal unsaved changes (`isOpalManaged=true`, status `INITIAL` or `DIRTY`)
- **Saved tab** — ALL saved changes (Opal + non-Opal), status NOT `INITIAL`/`DIRTY`

**Entry points:** BottomBar "Changes" button + OpalPreviewBanner "X unsaved changes" link

**Key behaviors from PRs:**
- PR #432 reversal: When BOTH unsaved AND saved changes exist → **Saved tab is default** (NOT Preview)
- Changes button always visible even with 0 changes (CJS-11052 fix)
- Undo is now async with error recovery (PR #432)
- `currentlyEditingChange` is unset when that change is undone (prevents re-introduction)

**Open bugs (regression targets):**
- CJS-11070 (HIGH): Opal preview must NOT auto-save when manual VE change is saved
- CJS-11072: Changes button must NOT appear in Simplified VE

**As Designed behaviors:**
- CJS-11069: "Continue without save" → preview data lost = expected
- CJS-11071: Preview data lost on page navigation = expected (fix in CJS-10766)
- CJS-11051: Select All is intentionally out of scope

**Test Website:** https://www.zillow.com (with snippet)

---

## Test Cases Summary

| # | Title | Priority | Labels |
|---|-------|----------|--------|
| TC-01 | [CJS-10765] Full Flow — Opal Change, Preview, Publish, Verify on Live Site | Critical | new_ve,opal,web,smoke_suite |
| TC-02 | [CJS-10765] Verify ChangeLog Opens — BottomBar Changes Button | High | new_ve,opal,web |
| TC-03 | [CJS-10765] Verify ChangeLog Opens — OpalPreviewBanner Link | High | new_ve,opal,web |
| TC-04 | [CJS-10765] Verify Preview Tab Shows Only Opal Unsaved Changes | High | new_ve,opal,web |
| TC-05 | [CJS-10765] Verify Saved Tab Shows All Saved Changes (Opal + non-Opal) | High | new_ve,opal,web |
| TC-06 | [CJS-10765] Verify Save Single Opal Change — Moves to Saved Tab | High | new_ve,opal,web |
| TC-07 | [CJS-10765] Verify Undo Single Opal Change — Reverted on DOM | High | new_ve,opal,web |
| TC-08 | [CJS-10765] Verify Delete Single Saved Change — Removed from Experiment | High | new_ve,opal,web |
| TC-09 | [CJS-10765] Verify Default Tab — Saved When Both Tabs Have Content (PR #432) | High | new_ve,opal,web |
| TC-10 | [CJS-10765] Verify Segment Event — save_opal_changes with Required Properties | High | new_ve,opal,web |
| TC-11 | [CJS-10765] Verify Segment Event — undo_opal_changes with Required Properties | High | new_ve,opal,web |
| TC-12 | [CJS-10765] Verify Multi-Select Save — 2 of 3 Saved, 1 Stays in Preview | Normal | new_ve,opal,web |
| TC-13 | [CJS-10765] Verify Multi-Select Undo — 2 of 3 Reverted, 1 Stays in Preview | Normal | new_ve,opal,web |
| TC-14 | [CJS-10765] Verify Empty State — Preview Tab | Normal | new_ve,opal,web |
| TC-15 | [CJS-10765] Verify Empty State — Saved Tab | Normal | new_ve,opal,web |
| TC-16 | [CJS-10765] Verify Buttons Disabled When No Items Selected | Normal | new_ve,opal,web |
| TC-17 | [CJS-10765] Verify Delete Button Red When Enabled (PR #432) | Normal | new_ve,opal,web |
| TC-18 | [CJS-10765] Verify Spinner During Save Processing; Tab Switch Blocked | Normal | new_ve,opal,web |
| TC-19 | [CJS-10765] Verify Click Change Item — Navigates to Correct Editor; ChangeLog Closes | Normal | new_ve,opal,web |
| TC-20 | [CJS-10765] Verify Hover Change Item — Element Highlighted on Page | Normal | new_ve,opal,web |
| TC-21 | [CJS-10765] Verify "Build Variation" in Empty Preview — Opal Chat Opens | Normal | new_ve,opal,web |
| TC-22 | [CJS-10765] Verify Variation Switch Auto-Closes ChangeLog | Normal | new_ve,opal,web |
| TC-23 | [CJS-10765] Verify Page Switch Auto-Closes ChangeLog | Normal | new_ve,opal,web |
| TC-24 | [CJS-10765] Verify Undo Error Recovery — Toast and State Restored (PR #432) | Normal | new_ve,opal,web |
| TC-25 | [CJS-10765] [CJS-11070] Saving Manual VE Change — Opal Preview NOT Auto-Saved | Normal | new_ve,opal,web |
| TC-26 | [CJS-10765] [CJS-11072] Changes Button NOT Visible in Simplified VE | Normal | new_ve,web |
| TC-27 | [CJS-10765] Verify Undo Currently Editing Change — Stays Undone, NOT Re-Introduced | Normal | new_ve,opal,web |
| TC-28 | [CJS-10765] Verify Running Experiment — ChangeLog Accessible (isLayerReadOnly=false) | Normal | new_ve,opal,web |
| TC-29 | [CJS-10765] Verify Concluded/Archived — Create Variation Button Hidden | Low | new_ve,opal,web |
| TC-30 | [CJS-10765] Verify MVT — ChangeLog Save Uses /sections/{id} Endpoint | Low | new_ve,opal,web |
| TC-31 | [CJS-10765] Verify Default Tab — Preview When Only Unsaved Changes Exist | Normal | new_ve,opal,web |
| TC-32 | [CJS-10765] Verify Default Tab — Saved When Only Saved Changes Exist | Normal | new_ve,opal,web |
| TC-33 | [CJS-10765] Verify Tab Switch Preview→Saved Clears Selection | Normal | new_ve,opal,web |
| TC-34 | [CJS-10765] Verify DIRTY Status Opal Changes Appear in Preview Tab | Normal | new_ve,opal,web |
| TC-35 | [CJS-10765] Verify Save Failure — Error Toast; Changes Remain in Preview | Normal | new_ve,opal,web |
| TC-36 | [CJS-10765] Verify Opal + Manual Change Same Element — Both Preserved After Save | Normal | new_ve,opal,web |
| TC-37 | [CJS-10765] Verify Undo CUSTOM_CODE Change — Page Reloads | Normal | new_ve,opal,web |
| TC-38 | [CJS-10765] Verify "Continue Without Save" — Preview Data Lost (As Designed) | Normal | new_ve,opal,web |
| TC-39 | [CJS-10765] Verify Old ChangeSelectionBar Still Functional Alongside New ChangeLog | Normal | new_ve,opal,web |
| TC-40 | [CJS-10765] Verify Monolith History Tab Logs Save Action via ChangeLog | Low | new_ve,opal,web |
| TC-41 | [CJS-10765] Verify Bottom Bar Correct at 125% Zoom with ChangeLog Open (CJS-11059) | Low | new_ve,opal,web |

**Total:** 41 test cases
**Coverage Distribution:**
- **Critical:** 1 (2%)
- **High:** 10 (24%)
- **Normal:** 24 (59%)
- **Low:** 5 (12%)

---

## Detailed Test Cases

---

### TC-01: [CJS-10765] Full Flow — Opal Change, Preview, Publish, Verify on Live Site

**Priority:** Critical | **Labels:** new_ve,opal,web,smoke_suite

**Pre-condition:**
- Created a public website that has injected Optimizely snippet correctly
- Created A/B experiment with Variation #1, experiment in Draft status
- Opal Chat feature is enabled on the project
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome
- Enable Support for Dynamic Websites: OFF

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Build Variation" to open Opal Chat; submit prompt "Change the hero heading color to red"
3. Confirm Opal change appears in OpalPreviewBanner as "1 unsaved change"
4. Click "Changes" button → open ChangeLog → Preview tab → select the Opal change → click Save
5. Click Preview for Variation #1 in the bottom bar
6. Close preview; click the experiment-level Preview button (QA ball)
7. Close preview; click Publish/Start to publish the experiment
8. Open the website in a new incognito tab and force bucket into Variation #1

**Expected Results:**
5. Variation preview shows the hero heading in red color applied correctly
6. Experiment preview shows the hero heading in red color applied correctly
8. Hero heading displays in red on the live website after bucketing into Variation #1; ChangeLog change persisted through publish

---

### TC-02: [CJS-10765] Verify ChangeLog Opens — BottomBar Changes Button

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status with at least one saved change on Variation #1
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm "Changes" button is visible in the bottom bar (always visible per CJS-11052 fix)
3. Click the "Changes" button in the bottom bar

**Expected Results:**
3. ChangeLog panel opens showing both "Preview" and "Saved" tab labels; default tab shown based on change state

---

### TC-03: [CJS-10765] Verify ChangeLog Opens — OpalPreviewBanner Link

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal-generated change in INITIAL status (isOpalManaged=true)
- OpalPreviewBanner is displayed above the bottom bar
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner is displayed showing "X unsaved change(s)"
3. Click the "X unsaved changes" link in the OpalPreviewBanner

**Expected Results:**
3. ChangeLog panel opens with Preview tab active; Opal unsaved change(s) listed in Preview tab

---

### TC-04: [CJS-10765] Verify Preview Tab Shows Only Opal Unsaved Changes

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has BOTH: (a) one Opal-generated change (isOpalManaged=true, INITIAL status) AND (b) one manually-made change (isOpalManaged=false, INITIAL status — not yet saved)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Press Alt/Option → click an element → apply a style change via Element Change Manager (creates non-Opal change, do NOT save yet)
3. Click "Build Variation" → submit Opal prompt generating a DOM change (creates isOpalManaged=true INITIAL change)
4. Click "Changes" button → open ChangeLog → navigate to Preview tab
5. Observe the list of changes displayed in the Preview tab

**Expected Results:**
5. Preview tab contains ONLY the Opal-generated change (isOpalManaged=true); the manually-made non-Opal change does NOT appear in Preview tab

---

### TC-05: [CJS-10765] Verify Saved Tab Shows All Saved Changes (Opal + non-Opal)

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has BOTH: (a) at least one saved Opal-generated change (isOpalManaged=true, status NOT INITIAL/DIRTY) AND (b) at least one saved non-Opal change (isOpalManaged=false, status NOT INITIAL/DIRTY)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Saved tab
3. Observe the list of changes in Saved tab

**Expected Results:**
3. Saved tab contains ALL saved changes regardless of isOpalManaged value — both the Opal-generated saved change AND the manually-made non-Opal saved change appear in the list

---

### TC-06: [CJS-10765] Verify Save Single Opal Change — Moves to Saved Tab

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has exactly one Opal unsaved change (isOpalManaged=true, INITIAL) — no saved changes
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab
3. Confirm one Opal change is listed in Preview tab
4. Select (check) the Opal change item
5. Click the "Save" button
6. Observe Preview tab after save completes
7. Navigate to Saved tab and observe its contents

**Expected Results:**
6. The saved change is removed from Preview tab; Preview tab shows empty state
7. The Opal change now appears in Saved tab (status no longer INITIAL)

---

### TC-07: [CJS-10765] Verify Undo Single Opal Change — Reverted on DOM

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has one Opal unsaved change (isOpalManaged=true, INITIAL) applied to a visible element on the website
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Note the original appearance of the element modified by the Opal change (e.g., heading color before Opal applied red)
3. Click "Changes" button → open ChangeLog → navigate to Preview tab
4. Select (check) the Opal change item
5. Click the "Undo" button
6. Observe the target element on the website and the Preview tab

**Expected Results:**
6. The Opal change is removed from Preview tab; the target element reverts to its pre-Opal appearance on the page DOM; OpalPreviewBanner disappears (0 unsaved Opal changes)

---

### TC-08: [CJS-10765] Verify Delete Single Saved Change — Removed from Experiment

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one saved change (status NOT INITIAL/DIRTY) targeting a visible element on the website
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Saved tab
3. Confirm the target saved change is listed; note its element selector/description
4. Select (check) the target saved change item
5. Click the "Delete" button
6. Observe Saved tab after delete completes
7. Observe the target element on the website

**Expected Results:**
6. The deleted change is removed from Saved tab; no longer listed
7. The target element on the website reverts to its original state (change no longer applied)

---

### TC-09: [CJS-10765] Verify Default Tab — Saved When Both Tabs Have Content (PR #432)

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has BOTH: at least one Opal unsaved change (INITIAL, isOpalManaged=true) AND at least one saved change (NOT INITIAL/DIRTY)
- OpalPreviewBanner confirms unsaved Opal changes exist
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm at least one saved change exists (Saved tab has content) and OpalPreviewBanner shows at least 1 unsaved Opal change (Preview tab has content)
3. Click "Changes" button to open ChangeLog for the first time
4. Observe which tab is active by default

**Expected Results:**
4. **Saved tab is the default active tab** — NOT Preview tab; Saved tab label highlighted; saved changes list displayed immediately without user needing to click Saved tab

---

### TC-10: [CJS-10765] Verify Segment Event — save_opal_changes with Required Properties

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal unsaved change (INITIAL, isOpalManaged=true)
- Chrome DevTools open, Network tab filtered by "api.segment.io"
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab → select the Opal change → click "Save"
3. In Chrome DevTools Network tab, locate the POST request to api.segment.io triggered by the Save action
4. Inspect the request payload (Preview/Payload tab)

**Expected Results:**
4. Segment event name is `"EXP - VE - save_opal_changes"`; payload contains `account_id` (non-empty), `experiment_id` (non-empty), and `thread_id` (non-empty) as properties

---

### TC-11: [CJS-10765] Verify Segment Event — undo_opal_changes with Required Properties

**Priority:** High | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal unsaved change (INITIAL, isOpalManaged=true)
- Chrome DevTools open, Network tab filtered by "api.segment.io"
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab → select the Opal change → click "Undo"
3. In Chrome DevTools Network tab, locate the POST request to api.segment.io triggered by the Undo action
4. Inspect the request payload

**Expected Results:**
4. Segment event name is `"EXP - VE - undo_opal_changes"`; payload contains `account_id` (non-empty), `experiment_id` (non-empty), and `thread_id` (non-empty) as properties

---

### TC-12: [CJS-10765] Verify Multi-Select Save — 2 of 3 Saved, 1 Stays in Preview

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has exactly 3 Opal unsaved changes (INITIAL, isOpalManaged=true), each modifying a distinct element; none saved yet
- OpalPreviewBanner shows "3 unsaved changes"
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab; confirm all 3 Opal changes listed
3. Select (check) exactly 2 of the 3 change items; leave the 3rd unchecked
4. Click "Save" button
5. Observe Preview tab after save completes
6. Navigate to Saved tab and observe its contents

**Expected Results:**
5. Preview tab now shows exactly 1 remaining change (the unselected one); OpalPreviewBanner updates to "1 unsaved change"
6. Saved tab contains the 2 changes that were selected and saved; the 1 unselected change does NOT appear in Saved tab

---

### TC-13: [CJS-10765] Verify Multi-Select Undo — 2 of 3 Reverted, 1 Stays in Preview

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has exactly 3 Opal unsaved changes (INITIAL), each modifying a distinct visible element
- OpalPreviewBanner shows "3 unsaved changes"
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Note the original appearance of all 3 modified elements before undo
3. Click "Changes" button → open ChangeLog → navigate to Preview tab; confirm all 3 Opal changes listed
4. Select (check) exactly 2 of the 3 change items; leave the 3rd unchecked
5. Click "Undo" button
6. Observe the website DOM and Preview tab after undo completes

**Expected Results:**
6. The 2 selected changes are removed from Preview tab; their corresponding elements revert to original appearance on website; the 3rd unselected change remains in Preview tab and its element still shows the Opal modification; OpalPreviewBanner updates to "1 unsaved change"

---

### TC-14: [CJS-10765] Verify Empty State — Preview Tab

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has NO Opal unsaved changes (no isOpalManaged=true + INITIAL/DIRTY changes)
- OpalPreviewBanner is NOT displayed
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner is NOT visible
3. Click "Changes" button → open ChangeLog → navigate to Preview tab
4. Observe the empty state content in Preview tab

**Expected Results:**
4. Preview tab displays: message "No unsaved changes", a subtitle description, and a "Build Variation" button — all three visible; no change items listed

---

### TC-15: [CJS-10765] Verify Empty State — Saved Tab

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has NO saved changes (brand new variation, 0 saved changes)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Saved tab
3. Observe the empty state content in Saved tab

**Expected Results:**
3. Saved tab displays: message "No changes saved yet" and a subtitle description; the "Build Variation" button is NOT present (unlike Preview tab empty state)

---

### TC-16: [CJS-10765] Verify Buttons Disabled When No Items Selected

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal unsaved change (Preview tab non-empty) AND at least one saved change (Saved tab non-empty)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab
3. Confirm no checkboxes are checked (zero items selected)
4. Observe the state of Save and Undo buttons
5. Navigate to Saved tab; confirm no items selected
6. Observe the state of Delete button

**Expected Results:**
4. Save button is disabled (greyed out, not clickable); Undo button is disabled (greyed out, not clickable)
6. Delete button is disabled (greyed out, default styling — no red background)

---

### TC-17: [CJS-10765] Verify Delete Button Red When Enabled (PR #432)

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least two saved changes in Saved tab
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Saved tab → enter select mode
3. Confirm zero items selected; observe Delete button styling
4. Check the checkbox next to one saved change item
5. Observe Delete button styling with 1 item selected
6. Uncheck the checkbox (deselect all)
7. Observe Delete button styling with zero items selected

**Expected Results:**
3. Delete button has default styling (disabled; no red background; `--ax-colors-bg-error` NOT applied)
5. Delete button becomes enabled with red background (`--ax-colors-bg-error` applied via `.deleteButtonEnabled` class)
7. Delete button reverts to default styling (disabled; no red background)

---

### TC-18: [CJS-10765] Verify Spinner During Save Processing; Tab Switch Blocked

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal unsaved change (INITIAL/DIRTY) in Preview tab
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab
3. Select one Opal change item → click Save
4. Immediately while the save is in-flight: observe the Save button appearance
5. Immediately while save is in-flight: attempt to click the Saved tab to switch
6. Immediately while save is in-flight: attempt to click the Undo button
7. Wait for save operation to complete

**Expected Results:**
4. Save button displays a spinner/loading indicator (isSaving=true)
5. Tab switching is blocked — clicking Saved tab has no effect; Preview tab remains active
6. Undo button is disabled and cannot be clicked
7. After save completes: spinner disappears; tab switching re-enabled; button states return to normal

---

### TC-19: [CJS-10765] Verify Click Change Item — Navigates to Correct Editor; ChangeLog Closes

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one saved ATTRIBUTE change, one INSERT_HTML change, one REDIRECT change, and one CUSTOM_CODE change
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Saved tab
3. Click on an ATTRIBUTE change item; observe result
4. Re-open ChangeLog → click on an INSERT_HTML change item; observe result
5. Re-open ChangeLog → click on a REDIRECT change item; observe result
6. Re-open ChangeLog → click on a CUSTOM_CODE change item; observe result

**Expected Results:**
3. ChangeLog closes; ElementChangeManager opens scoped to the element matching the change selector; element highlighted on page
4. ChangeLog closes; Insert HTML editor opens; element selector populated
5. ChangeLog closes; Redirect editor opens
6. ChangeLog closes; Code editor (Monaco) opens

---

### TC-20: [CJS-10765] Verify Hover Change Item — Element Highlighted on Page

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one change with a valid CSS selector targeting a visible element on the website
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog (either tab with changes listed)
3. Move mouse cursor to hover over a change list item that has a CSS selector (ATTRIBUTE or INSERT_HTML type)
4. Observe the website while hovering
5. Move mouse cursor away from the change item

**Expected Results:**
3. No highlight yet
4. The corresponding element on the website is highlighted with a visible border (setHoveredSelector called with change.selector)
5. The element highlight is cleared; no border visible

---

### TC-21: [CJS-10765] Verify "Build Variation" in Empty Preview — Opal Chat Opens

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has NO Opal unsaved changes (Preview tab is empty)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab
3. Confirm Preview tab shows empty state with "Build Variation" button
4. Click "Build Variation" button
5. Observe the result

**Expected Results:**
5. ChangeLog closes; Opal Chat panel opens and is visible; ChangeLog does not re-appear on its own

---

### TC-22: [CJS-10765] Verify Variation Switch Auto-Closes ChangeLog

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status with at least 2 variations
- Variation #1 has at least one change so ChangeLog has content
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog; if available, check one item
3. Confirm ChangeLog is open
4. Click "Original" variation tab in the bottom bar to switch variation
5. Observe ChangeLog state after the switch

**Expected Results:**
5. ChangeLog panel is automatically closed; previously selected items are cleared; ChangeLog does not re-open on its own

---

### TC-23: [CJS-10765] Verify Page Switch Auto-Closes ChangeLog

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status targeting at least 2 saved pages (multi-page)
- Variation #1 has at least one change
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog; confirm it is open
3. Click the PageSwitcher dropdown in the bottom bar
4. Select a different page from the dropdown
5. Observe ChangeLog state after the page switch

**Expected Results:**
5. ChangeLog panel is automatically closed; all selections cleared; ChangeLog does not re-open after page switch

---

### TC-24: [CJS-10765] Verify Undo Error Recovery — Toast and State Restored (PR #432)

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one change in Preview tab
- Chrome DevTools can be used to block the change handler request
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → Preview tab → select one change
3. Block the `pushChangeHandlerRequest` call via Chrome DevTools (block the relevant API endpoint)
4. Click "Undo"
5. Observe toast notification area and Preview tab contents

**Expected Results:**
5. Toast notification appears: **"Failed to undo changes. Please try again."**; change reappears in Preview tab (store restored to original state); DOM restored to pre-undo appearance; "Please reload the page." toast does NOT appear for single failure

---

### TC-25: [CJS-10765] [CJS-11070] Saving Manual VE Change — Opal Preview NOT Auto-Saved

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Opal Chat feature enabled
- Variation #1: one Opal change (INITIAL, isOpalManaged=true) in Preview tab; no saved changes yet
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner shows "1 unsaved change" (Opal change in Preview tab)
3. Without saving the Opal change, press Alt/Option → click a DIFFERENT element → apply a manual CSS change (e.g., font-size) via Element Change Manager → click Save
4. Click "Changes" button → open ChangeLog; observe Preview tab and Saved tab

**Expected Results:**
4. **Opal change remains in Preview tab** — it does NOT auto-move to Saved tab; OpalPreviewBanner still shows "1 unsaved change"; Saved tab contains ONLY the manually saved element change; Saved tab does NOT contain the Opal change

---

### TC-26: [CJS-10765] [CJS-11072] Changes Button NOT Visible in Simplified VE

**Priority:** Normal | **Labels:** new_ve,web

**Pre-condition:**
- User has access to Implementation → Pages section in the Web project
- User is logged in and navigated to the project

**Parameters:**
- Experiment type: N/A (Simplified VE — page editor, not variation editor)
- Browser: Chrome

**Test Steps:**
1. Navigate to Implementation → Pages tab in the Web project
2. Click on any page name to open the Simplified VE
3. Wait for Simplified VE to fully load
4. Observe the bottom bar for the presence of a "Changes" button or ChangeLog component

**Expected Results:**
4. "Changes" button does **NOT** appear in the Simplified VE bottom bar; AttributeList (Events/Tags) IS visible (correct Simplified VE behavior); no JavaScript errors in console

---

### TC-27: [CJS-10765] Verify Undo Currently Editing Change — Stays Undone, NOT Re-Introduced

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has an Opal change in Preview tab
- That change can be opened in ElementChangeManager (ATTRIBUTE type)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click on an element on the page that has the Opal change — ElementChangeManager opens with that change as currentlyEditingChange
3. Confirm the change is loaded in ElementChangeManager panel
4. Open ChangeLog → Preview tab → select the same change → click "Undo"
5. Observe the ElementChangeManager panel
6. Observe the website DOM

**Expected Results:**
5. ElementChangeManager closes or becomes empty (currentlyEditingChange is unset in the store)
6. The change's visual effect is no longer visible on page; the change does NOT re-appear — applyCurrentlyEditingChange does not re-introduce the change because currentlyEditingChange was unset

---

### TC-28: [CJS-10765] Verify Running Experiment — ChangeLog Accessible (isLayerReadOnly=false)

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- A/B experiment in Running status with at least one saved change on Variation #1
- Note: `isLayerReadOnly()` returns false for Running — VE is NOT read-only for Running status
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Observe the variation tab row in the bottom bar
3. Click "Changes" button → open ChangeLog
4. Observe ChangeLog content
5. Observe the + (Create Variation) button

**Expected Results:**
2. The experiment status is Running (visible in Monolith before entering VE)
4. ChangeLog opens and displays saved changes; content is accessible and viewable
5. The + (Create Variation) button **IS visible** — isLayerReadOnly() returns false for Running status per experimentStore.ts

---

### TC-29: [CJS-10765] Verify Concluded/Archived — Create Variation Button Hidden

**Priority:** Low | **Labels:** new_ve,opal,web

**Pre-condition:**
- A/B experiment in Concluded or Archived status with at least one saved change on Variation #1
- Note: `isLayerReadOnly()` returns true for Concluded and Archived only
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Observe the variation tab row in the bottom bar
3. Click "Changes" button → open ChangeLog
4. Observe ChangeLog content

**Expected Results:**
2. The + (Create Variation) button is **NOT visible** — isLayerReadOnly() returns true for Concluded/Archived
4. ChangeLog opens; existing saved changes displayed; content visible (ChangeLog is not blocked by status)

---

### TC-30: [CJS-10765] Verify MVT — ChangeLog Save Uses /sections/{id} Endpoint

**Priority:** Low | **Labels:** new_ve,opal,web

**Pre-condition:**
- MVT experiment in Draft status with at least one section and variation
- Chrome DevTools open, Network tab ready, filter by "experiments"
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: Multivariate Test (MVT)
- Browser: Chrome

**Test Steps:**
1. Open a variation within a section in Visual Editor (MVT)
2. Press Alt/Option → click an element → apply a CSS change (e.g., font-size) → save change via Element Change Manager
3. Observe the Network tab for the outgoing PUT request triggered by the save
4. Click "Changes" button → open ChangeLog → navigate to Saved tab

**Expected Results:**
3. PUT request goes to `/v2/experiments/sections/{sectionId}` — **NOT** `/v2/experiments/{id}` (MVT-specific endpoint); request returns HTTP 200/202
4. ChangeLog Saved tab shows the newly saved change with correct selector and change type

---

---

### TC-31: [CJS-10765] Verify Default Tab — Preview When Only Unsaved Changes Exist

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has Opal unsaved changes (isOpalManaged=true, INITIAL) but ZERO saved changes (Saved tab is empty)
- OpalPreviewBanner confirms unsaved Opal changes exist
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner shows at least 1 unsaved Opal change; confirm no saved changes exist
3. Click "Changes" button to open ChangeLog for the first time
4. Observe which tab is active by default

**Expected Results:**
4. **Preview tab is the default active tab** — Preview tab label highlighted; Opal unsaved changes displayed immediately without user needing to click Preview tab

---

### TC-32: [CJS-10765] Verify Default Tab — Saved When Only Saved Changes Exist

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has saved changes (status NOT INITIAL/DIRTY) but ZERO Opal unsaved changes
- OpalPreviewBanner is NOT displayed
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner is NOT visible; confirm at least one saved change exists
3. Click "Changes" button to open ChangeLog for the first time
4. Observe which tab is active by default

**Expected Results:**
4. **Saved tab is the default active tab** — Saved tab label highlighted; saved changes displayed immediately without user needing to click Saved tab

---

### TC-33: [CJS-10765] Verify Tab Switch Preview→Saved Clears Selection

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has both Opal unsaved changes (Preview) and saved changes (Saved)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click "Changes" button → open ChangeLog → navigate to Preview tab
3. Check 1+ Opal change items; confirm selection count shows 1+ items selected
4. Click Saved tab to switch tabs
5. Observe checkboxes/selection state in Saved tab
6. Click back to Preview tab; observe state of checkboxes

**Expected Results:**
5. All selections cleared (empty Set()); no items checked in Saved tab; selection count = 0
6. Previously checked items in Preview tab are no longer checked — selections remain cleared after switching back

---

### TC-34: [CJS-10765] Verify DIRTY Status Opal Changes Appear in Preview Tab

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has an Opal change in INITIAL status (isOpalManaged=true)
- Note: `useUnsavedOpalChanges` hook filters for status `INITIAL` OR `DIRTY` — not INITIAL only
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm the Opal change (INITIAL) appears in OpalPreviewBanner and Preview tab
3. Click on the Opal change item to open its editor (ElementChangeManager for ATTRIBUTE type)
4. Manually edit a value in the editor (e.g., change a CSS property value) — this transitions the change status to DIRTY
5. Open ChangeLog → navigate to Preview tab
6. Observe whether the DIRTY status Opal change appears in Preview tab

**Expected Results:**
6. The DIRTY status Opal change is listed in Preview tab (both INITIAL and DIRTY are included per `useUnsavedOpalChanges`); Opal icon still displayed (isOpalManaged=true preserved); change is NOT in Saved tab

---

### TC-35: [CJS-10765] Verify Save Failure — Error Toast; Changes Remain in Preview

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least one Opal unsaved change (INITIAL/DIRTY) in Preview tab
- Chrome DevTools available to block the save API request
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Open Chrome DevTools → Network tab; add a block rule for `PUT /v2/experiments/{id}`
3. Click "Changes" button → open ChangeLog → Preview tab → select one Opal change → click Save
4. Observe toast notification area and Preview tab after save attempt fails
5. Remove the network block; retry Save on the same change

**Expected Results:**
4. Error toast notification appears; the failed change remains in Preview tab (NOT moved to Saved tab); Saved tab does NOT contain the failed change
5. After removing block and retrying Save, the change saves successfully and moves to Saved tab

---

### TC-36: [CJS-10765] Verify Opal + Manual Change Same Element — Both Preserved After Save

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Opal Chat feature enabled; Variation #1 accessible
- Note: `changeMerge.ts` `mergeChangesWithPriority` handles merge when both changes target same element
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Click on a specific element (e.g., heading h1) → apply a manual color change via Element Change Manager → click Save
3. Confirm the manual change appears in ChangeLog Saved tab
4. Open Opal Chat → submit a prompt generating a change on the SAME element (e.g., "Change the heading font size to 24px")
5. Confirm the Opal change appears in Preview tab (OpalPreviewBanner shows "1 unsaved change")
6. Select the Opal change in Preview tab → click Save
7. Observe Saved tab contents

**Expected Results:**
7. Saved tab shows BOTH changes: the original manual VE change AND the Opal-generated change targeting the same element; neither overwrites the other (`mergeChangesWithPriority` preserves both); Preview tab is empty (OpalPreviewBanner disappears)

---

### TC-37: [CJS-10765] Verify Undo CUSTOM_CODE Change — Page Reloads

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has an Opal-generated CUSTOM_CODE (custom JavaScript) change in Preview tab (isOpalManaged=true, INITIAL)
- Note: `hasChangesRequiringReload()` detects CUSTOM_CODE → triggers `window.location.reload()`
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm CUSTOM_CODE Opal change is in Preview tab; OpalPreviewBanner shows unsaved change
3. Click "Changes" button → open ChangeLog → Preview tab → select the CUSTOM_CODE change → click "Undo"
4. Observe browser and VE behavior after Undo

**Expected Results:**
4. Browser performs a full page reload (`window.location.reload()` called — this is expected behavior for undoing CUSTOM_CODE); after reload VE re-initializes and loads correctly; ChangeLog Preview tab no longer shows the CUSTOM_CODE change; OpalPreviewBanner not shown; no error toast appears

---

### TC-38: [CJS-10765] Verify "Continue Without Save" — Preview Data Lost (As Designed)

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status with at least 2 variations
- Variation #1 has Opal unsaved changes in Preview tab; Opal Chat enabled
- Note: "Continue without save" losing preview data is **As Designed** per Jett Sy (CJS-11069)
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Confirm OpalPreviewBanner shows at least 1 unsaved Opal change
3. WITHOUT saving, click "Original" variation tab to switch variation
4. "Unsaved changes" modal appears; click "Continue without saving"
5. Observe ChangeLog state after switching to Original variation

**Expected Results:**
5. Opal preview changes from Variation #1 are permanently discarded; they do NOT appear in ChangeLog for Original variation; OpalPreviewBanner not shown; **no error or recovery mechanism** — this is As Designed behavior (per Jett Sy comment on CJS-11069)

---

### TC-39: [CJS-10765] Verify Old ChangeSelectionBar Still Functional Alongside New ChangeLog

**Priority:** Normal | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status
- Variation #1 has at least 2 saved changes
- Both old ChangeList/ChangeSelectionBar (ellipsis … on variation tab) and new ChangeLog coexist in current build
- Note: Old ChangeSelectionBar will be removed in CJS-10948 — this is regression check while both coexist
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Hover over active Variation #1 tab in the bottom bar → click the ellipsis (…) button to open old ChangeList dropdown
3. Confirm old ChangeList shows saved changes with correct count
4. In old ChangeList: enter select mode → select one change → click Delete
5. Close old ChangeList dropdown
6. Click "Changes" button → open new ChangeLog → navigate to Saved tab
7. Observe Saved tab contents

**Expected Results:**
4. Delete via old ChangeSelectionBar works; change is removed from experiment and count updates
7. New ChangeLog Saved tab reflects the same post-delete state (both components share the same `changeStore`); the deleted change is NOT present in Saved tab; no state conflict or stale data between old and new UI

---

### TC-40: [CJS-10765] Verify Monolith History Tab Logs Save Action via ChangeLog

**Priority:** Low | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status; Variation #1 has no prior save actions in this session
- User's display name is known for verification in History tab
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome

**Test Steps:**
1. Open Variation #1 in Visual Editor
2. Press Alt/Option → click an element → apply a CSS change (e.g., background-color) → save via Element Change Manager
3. Click "Changes" button → open ChangeLog → confirm saved change in Saved tab
4. Close ChangeLog; exit VE (click Return to Experiment)
5. In Monolith: navigate to Settings (left sidebar) → History tab
6. Observe the most recent entry in the Change Summary table

**Expected Results:**
6. Most recent entry shows: description of the change (variation edit / style change), logged-in user's name/email, and a timestamp matching the time of the save action; no duplicate or missing entries for the ChangeLog-triggered save

---

### TC-41: [CJS-10765] Verify Bottom Bar Correct at 125% Zoom with ChangeLog Open (CJS-11059)

**Priority:** Low | **Labels:** new_ve,opal,web

**Pre-condition:**
- Experiment A/B test in Draft status; Variation #1 has at least one saved change (so ChangeLog has content)
- Browser zoom set to 125% before starting
- User is logged in and navigated to the experiment

**Parameters:**
- Experiment type: A/B Test
- Browser: Chrome at 125% zoom (Settings → Appearance → Page zoom: 125%)

**Test Steps:**
1. Set Chrome browser zoom to 125%
2. Open Variation #1 in Visual Editor
3. Observe overall bottom bar layout at 125% zoom (variation tabs, interaction bar, "Changes" button)
4. Click "Changes" button → open ChangeLog at 125% zoom
5. Observe ChangeLog panel: header, change entries, close (X) button, select mode footer
6. Close ChangeLog; restore zoom to 100%

**Expected Results:**
3. Bottom bar displays all controls without truncation — variation tabs, interaction bar buttons, "Changes" button all fully visible and clickable (no CJS-11059 regression introduced by ChangeLog)
5. ChangeLog opens correctly at 125% zoom — header, change entries, close button all visible and not overlapping; content area scrolls correctly; select mode footer (Delete button) fully visible without clipping

---

## Risk Items for Clarification

1. **TC-25 (CJS-11070)**: Confirm if PR #432 fixed this or still open for Cristhian
2. **TC-26 (CJS-11072)**: Confirm if a fix PR exists or still open
3. **TC-24 error recovery**: Confirm whether the failure scenario can be reproduced in Development (may require unit test only)
