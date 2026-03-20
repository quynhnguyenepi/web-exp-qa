# Test Design Document - CJS-10872

**Ticket:** [CJS-10872 - [VE Events] Events list popup](https://optimizely-ext.atlassian.net/browse/CJS-10872)
**Epic:** [CJS-10559 - Visual Editor Rebuild (M5)](https://optimizely-ext.atlassian.net/browse/CJS-10559)
**Product Domain:** Web Experimentation - Visual Editor
**Status:** In Testing
**Generated:** 2026-03-09
**Total Test Cases:** 35

---

## Test Case Summary

| # | Title | Priority | Labels |
|---|-------|----------|--------|
| TC-01 | [CJS-10872] Verify Events List - Open Popup from Bottom Bar | High | Functional, UI |
| TC-02 | [CJS-10872] Verify Events List - Click Event to Edit | High | Functional, Navigation |
| TC-03 | [CJS-10872] Verify Events List - Archive Single Event | High | Functional, State Management |
| TC-04 | [CJS-10872] Verify Events List - Archive Multiple Events (Bulk) | High | Functional, Bulk Operations |
| TC-05 | [CJS-10872] Verify Events List - Empty State Display | High | UI, State Management |
| TC-06 | [CJS-10872] Verify Events List - Create Event from Empty State | Normal | Functional, Navigation |
| TC-07 | [CJS-10872] Verify Events List - Loading State | Normal | UI, State Management |
| TC-08 | [CJS-10872] Verify Events List - Select All Functionality | Normal | UI, Bulk Operations |
| TC-09 | [CJS-10872] Verify Events List - Deselect All Functionality | Normal | UI, Bulk Operations |
| TC-10 | [CJS-10872] Verify Events List - Toggle Select Mode | Normal | UI, State Management |
| TC-11 | [CJS-10872] Verify Events List - Close Popup | Normal | UI, Navigation |
| TC-12 | [CJS-10872] Verify Events List - Click Event in Select Mode | Normal | UI, State Management |
| TC-13 | [CJS-10872] Verify Archive Dialog - Single Event Warning Message | Normal | Validation, UI |
| TC-14 | [CJS-10872] Verify Archive Dialog - Bulk Event List Display | Normal | Validation, UI |
| TC-15 | [CJS-10872] Verify Archive Dialog - Cancel Action | Normal | Functional, Validation |
| TC-16 | [CJS-10872] Verify Archive Dialog - Loading State | Normal | UI, State Management |
| TC-17 | [CJS-10872] Verify API - Archived Events Excluded from Fetch | High | Integration, API |
| TC-18 | [CJS-10872] Verify API - Events Filtered by View ID | High | Integration, API |
| TC-19 | [CJS-10872] Verify Analytics - Attributes Opened Event Tracking | Normal | Analytics, Tracking |
| TC-20 | [CJS-10872] Verify Analytics - Archived Event Tracking | Normal | Analytics, Tracking |
| TC-21 | [CJS-10872] Verify Notifications - Archive Success Single Event | Normal | UI, Feedback |
| TC-22 | [CJS-10872] Verify Notifications - Archive Success Bulk Events | Normal | UI, Feedback |
| TC-23 | [CJS-10872] Verify Notifications - Archive Error Handling | Normal | Error Handling, UI |
| TC-24 | [CJS-10872] Verify Race Condition - Bulk Archive Loading State | Normal | State Management, API |
| TC-25 | [CJS-10872] Verify Events List - Refresh After Archive | Normal | State Management, API |
| TC-26 | [CJS-10872] Verify Event Editor - Archive Button Exists | Normal | UI, Integration |
| TC-27 | [CJS-10872] Verify Event Editor - Archive from Editor | Normal | Functional, Integration |
| TC-28 | [CJS-10872] Verify Event Editor - Refresh After Save | Normal | State Management, API |
| TC-29 | [CJS-10872] Verify Popover - Scroll Behavior with Many Events | Low | UI, UX |
| TC-30 | [CJS-10872] Verify Regression - Event Creation Still Works | High | Regression, Functional |
| TC-31 | [CJS-10872] Verify Regression - Event Editing Still Works | High | Regression, Functional |
| TC-32 | [CJS-10872] Verify Regression - Event Selector Highlighting | Normal | Regression, Visual Editor |
| TC-33 | [CJS-10872] Verify Regression - Bottom Bar Layout Intact | Normal | Regression, UI |
| TC-34 | [CJS-10872] Verify Regression - Segment Analytics Integration | Normal | Regression, Analytics |
| TC-35 | [CJS-10872] Verify Regression - Notifications System | Low | Regression, UI |

---

## Coverage Summary

| Priority | Count | Percentage |
|----------|-------|------------|
| High | 10 | 28.6% |
| Normal | 23 | 65.7% |
| Low | 2 | 5.7% |
| **Total** | **35** | **100%** |

| Category | Count |
|----------|-------|
| Functional | 15 |
| UI | 18 |
| State Management | 12 |
| API / Integration | 8 |
| Analytics | 3 |
| Validation | 4 |
| Error Handling | 2 |
| Regression | 5 |

---

## Detailed Test Cases

---

### TC-01: [CJS-10872] Verify Events List - Open Popup from Bottom Bar

**Priority:** High | **Labels:** Functional, UI

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with at least one event created for the current page
- User has edit permissions for the experiment

**Parameters:**
- Environment: RC
- Browser: Chrome
- Experiment type: A/B

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page
4. Open experiment "Homepage A/B Test" (Running status)
5. Click on "Variation #1" to open Visual Editor
6. Wait for Visual Editor to fully load (bottom bar visible)
7. Observe the Events icon button in the bottom bar
8. Click the Events icon button (list icon)

**Expected Results:**
1. Login succeeds and dashboard loads with project list
2. Web project page displays with experiment list
3. Experiments page loads showing list of experiments
4. Experiment details page opens with Summary tab displayed
5. Visual Editor loads with target page rendered and bottom bar visible
6. Bottom bar displays with Events icon button visible alongside other controls
7. Events icon button is clickable and labeled with list icon
8. Attributes popover opens with "Attributes" header, Events tab is active by default, and events list is displayed

---

### TC-02: [CJS-10872] Verify Events List - Click Event to Edit

**Priority:** High | **Labels:** Functional, Navigation

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list popup open
- At least one event "Clicked Shop Now" exists with selector `.shop-now`

**Parameters:**
- Environment: RC
- Experiment type: A/B

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click the Events icon in bottom bar to open Events list
7. Observe the event row "Clicked Shop Now" with type "Click"
8. Click anywhere on the "Clicked Shop Now" event row

**Expected Results:**
1. Login succeeds and dashboard loads
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads with target page
5. Bottom bar displays with all controls
6. Attributes popover opens with Events tab active
7. Event row displays with event icon, name "Clicked Shop Now", and type "Click"
8. Event Editor popup opens with event details loaded (name, description, selector `.shop-now` populated), and the matching element on page is highlighted

---

### TC-03: [CJS-10872] Verify Events List - Archive Single Event

**Priority:** High | **Labels:** Functional, State Management

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list popup open
- At least one event "Clicked Shop Now" exists

**Parameters:**
- Environment: RC
- Experiment type: A/B

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click the Events icon in bottom bar to open Events list
7. Click the ellipsis menu (3 dots) in the top right of the popover
8. Click "Select" option from the menu
9. Observe checkboxes appear next to each event
10. Click the checkbox next to "Clicked Shop Now" event
11. Click the "Archive" button that appears
12. Read the archive confirmation dialog message
13. Click the "Archive Event" button in the dialog

**Expected Results:**
1. Login succeeds and dashboard loads
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads with target page
5. Bottom bar displays
6. Attributes popover opens with Events tab active
7. Ellipsis menu opens showing options
8. Select mode is activated
9. Checkboxes appear to the left of each event row
10. Checkbox for "Clicked Shop Now" is checked, checkbox counter updates
11. Archive confirmation dialog opens
12. Dialog shows warning: "Are you sure you want to archive the click event **Clicked Shop Now**? This event will no longer be tracked. If this event is a tracked metric on a running experiment, its results may become inaccurate."
13. Archive API PUT call to `/api/v1/events/{id}` with `{"archived": true}` completes, success notification "Event 'Clicked Shop Now' archived" appears, event is removed from the list, and dialog closes

---

### TC-04: [CJS-10872] Verify Events List - Archive Multiple Events (Bulk)

**Priority:** High | **Labels:** Functional, Bulk Operations

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list popup open
- At least 3 events exist: "Clicked Shop Now", "Form Submitted", "Add to Cart"

**Parameters:**
- Environment: RC
- Experiment type: A/B

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click the Events icon in bottom bar to open Events list
7. Click ellipsis menu (3 dots)
8. Click "Select" to enter select mode
9. Click checkbox for "Clicked Shop Now"
10. Click checkbox for "Form Submitted"
11. Click "Archive" button
12. Read the bulk archive dialog message
13. Click "Archive 2 Events" button

**Expected Results:**
1. Login succeeds and dashboard loads
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens with Events list
7. Ellipsis menu opens
8. Select mode activated, checkboxes appear
9. "Clicked Shop Now" checkbox checked
10. "Form Submitted" checkbox checked, counter shows "2 selected"
11. Archive dialog opens for bulk action
12. Dialog shows: "Are you sure you want to archive the following events?" followed by bulleted list showing "Clicked Shop Now" and "Form Submitted", and warning about impact on running experiments
13. Multiple API PUT calls execute (Promise.all), success notification "2 events archived" appears, both events removed from list, dialog closes

---

### TC-05: [CJS-10872] Verify Events List - Empty State Display

**Priority:** High | **Labels:** UI, State Management

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded on a page with no events created yet

**Parameters:**
- Environment: RC
- Experiment type: A/B

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click the Events icon in bottom bar

**Expected Results:**
1. Login succeeds and dashboard loads
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens showing empty state with heading "No events created yet", description "Start creating events on this page", and "Create Event" button displayed

---

### TC-06: [CJS-10872] Verify Events List - Create Event from Empty State

**Priority:** Normal | **Labels:** Functional, Navigation

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list showing empty state

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list (empty state)
7. Click "Create Event" button in empty state

**Expected Results:**
1. Login succeeds and dashboard loads
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens showing empty state
7. Event Editor popup opens in create mode, Segment event `Click_Create_EVENT` is tracked, Events list popup closes

---

### TC-07: [CJS-10872] Verify Events List - Loading State

**Priority:** Normal | **Labels:** UI, State Management

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loading events from API (simulate slow network)

**Parameters:**
- Environment: RC
- Network: Throttled to Slow 3G

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Open browser DevTools Network tab and enable "Slow 3G" throttling
6. Wait for Visual Editor to load
7. Click Events icon to open Events list
8. Observe the Events tab content while fetchEvents API call is in progress

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor begins loading
5. Network throttling applied
6. Visual Editor loads with bottom bar visible
7. Events list popover opens
8. Spinner is displayed in the Events tab content area, no event rows shown while loading

---

### TC-08: [CJS-10872] Verify Events List - Select All Functionality

**Priority:** Normal | **Labels:** UI, Bulk Operations

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open
- At least 3 events exist

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click ellipsis menu (3 dots)
8. Observe "Select All" option in menu
9. Click "Select All"

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Ellipsis menu opens
8. "Select All" option is visible
9. All event checkboxes become checked, select mode is activated, counter shows total count, menu label changes to "Deselect All"

---

### TC-09: [CJS-10872] Verify Events List - Deselect All Functionality

**Priority:** Normal | **Labels:** UI, Bulk Operations

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open in select mode
- All events currently selected (via Select All)

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click ellipsis menu and select "Select All"
8. Observe all checkboxes are checked
9. Click ellipsis menu again
10. Click "Deselect All"

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode activated, all events selected
8. All checkboxes checked, counter shows total
9. Ellipsis menu opens showing "Deselect All"
10. All checkboxes become unchecked, counter shows "0 selected", menu label changes back to "Select All", select mode remains active

---

### TC-10: [CJS-10872] Verify Events List - Toggle Select Mode

**Priority:** Normal | **Labels:** UI, State Management

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open
- Select mode currently active with 2 events selected

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 2 events
8. Click ellipsis menu (3 dots)
9. Click "Select" option (to toggle off select mode)

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 2 events selected
8. Ellipsis menu opens
9. Checkboxes disappear from event rows, selections cleared, list returns to normal view (events are clickable to edit)

---

### TC-11: [CJS-10872] Verify Events List - Close Popup

**Priority:** Normal | **Labels:** UI, Navigation

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list popup open
- Select mode active with some events selected

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 1 event
8. Click the X (close) button in the popover header

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 1 event selected
8. Popover closes, select mode is reset (checkbox selections cleared), next time popover opens it is in normal view mode

---

### TC-12: [CJS-10872] Verify Events List - Click Event in Select Mode

**Priority:** Normal | **Labels:** UI, State Management

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open in select mode

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click ellipsis menu and activate "Select" mode
8. Observe checkboxes next to events
9. Click anywhere on an event row (not on checkbox)

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode activated
8. Checkboxes visible next to all events
9. Checkbox for that event row toggles (checked becomes unchecked or vice versa), Event Editor popup does NOT open

---

### TC-13: [CJS-10872] Verify Archive Dialog - Single Event Warning Message

**Priority:** Normal | **Labels:** Validation, UI

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open
- 1 event selected for archive

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select event "Clicked Shop Now"
8. Click "Archive" button
9. Read the dialog header
10. Read the dialog body text

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 1 event selected
8. Archive dialog opens
9. Dialog header reads "Archive Event"
10. Dialog body contains: "Are you sure you want to archive the click event **Clicked Shop Now**? This event will no longer be tracked. If this event is a tracked metric on a running experiment, its results may become inaccurate."

---

### TC-14: [CJS-10872] Verify Archive Dialog - Bulk Event List Display

**Priority:** Normal | **Labels:** Validation, UI

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open
- 3 events selected for archive: "Event A", "Event B", "Event C"

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 3 events
8. Click "Archive" button
9. Read the dialog header
10. Read the dialog body text and observe the event list

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 3 events selected
8. Archive dialog opens
9. Dialog header reads "Archive Events"
10. Dialog body shows "Are you sure you want to archive the following events?" followed by bulleted list with "Event A", "Event B", "Event C", followed by warning "These events will no longer be tracked. If any of these events are tracked metrics on a running experiment, its results may become inaccurate."

---

### TC-15: [CJS-10872] Verify Archive Dialog - Cancel Action

**Priority:** Normal | **Labels:** Functional, Validation

**Pre-condition:**
- Product: Web Experimentation
- Archive dialog open for 1 event

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode, select 1 event, click "Archive"
8. Observe "Cancel" button in dialog
9. Open browser DevTools Network tab
10. Click "Cancel" button

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Archive dialog opens
8. "Cancel" button visible in dialog footer
9. Network tab ready to capture API calls
10. Dialog closes, no PUT requests to `/api/v1/events/{id}` made, events remain visible in list

---

### TC-16: [CJS-10872] Verify Archive Dialog - Loading State

**Priority:** Normal | **Labels:** UI, State Management

**Pre-condition:**
- Product: Web Experimentation
- Archive dialog open ready to archive event

**Parameters:**
- Environment: RC
- Network: Throttled to simulate API delay

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode, select 1 event, click "Archive"
8. Enable Network throttling in DevTools (Slow 3G)
9. Click "Archive Event" button
10. Observe button state during API call

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Archive dialog opens
8. Network throttling applied
9. "Archive Event" button clicked
10. Button shows spinner, button is disabled (not clickable), spinner visible until API completes

---

### TC-17: [CJS-10872] Verify API - Archived Events Excluded from Fetch

**Priority:** High | **Labels:** Integration, API

**Pre-condition:**
- Product: Web Experimentation
- Project has 5 events total, 2 of which are archived

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Open browser DevTools Network tab
7. Click Events icon to open Events list
8. Observe the API call in Network tab

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Network tab ready to capture requests
7. Attributes popover opens
8. GET request to `/api/v1/projects/{projectId}/events?filter=archived:false` is made, response contains only 3 non-archived events, archived events not included

---

### TC-18: [CJS-10872] Verify API - Events Filtered by View ID

**Priority:** High | **Labels:** Integration, API

**Pre-condition:**
- Product: Web Experimentation
- Project has multiple pages (view_id) with events
- Currently on page with view_id: 12345

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor on specific page
5. Wait for Visual Editor to fully load
6. Note the page ID in URL query parameter
7. Open browser DevTools Network tab
8. Click Events icon to open Events list
9. Observe the API call in Network tab

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads on target page
5. Bottom bar displays
6. Page ID visible in query params (e.g., `pageId=12345`)
7. Network tab ready
8. Attributes popover opens
9. GET request to `/api/v1/projects/{projectId}/events?filter=archived:false&filter=view_id:12345` is made, response contains only events for current page (view_id: 12345)

---

### TC-19: [CJS-10872] Verify Analytics - Attributes Opened Event Tracking

**Priority:** Normal | **Labels:** Analytics, Tracking

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Segment analytics enabled

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Open browser Console and filter for "segment" or "analytics"
7. Click Events icon in bottom bar

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Console ready to capture Segment events
7. Segment analytics event `Attributes_Opened` is tracked and logged in console

---

### TC-20: [CJS-10872] Verify Analytics - Archived Event Tracking

**Priority:** Normal | **Labels:** Analytics, Tracking

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded with Events list open, 1 event selected for archive

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode, select 1 event
8. Open browser Console and filter for analytics
9. Click "Archive" button
10. Click "Archive Event" in dialog

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 1 event selected
8. Console ready
9. Archive dialog opens
10. Segment analytics event `Archived_Event` is tracked and logged in console before API call

---

### TC-21: [CJS-10872] Verify Notifications - Archive Success Single Event

**Priority:** Normal | **Labels:** UI, Feedback

**Pre-condition:**
- Product: Web Experimentation
- Archive completed successfully for event "Clicked Shop Now"

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select event "Clicked Shop Now"
8. Click "Archive" button
9. Click "Archive Event" in dialog
10. Wait for API to complete

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, event selected
8. Archive dialog opens
9. Archive button clicked, API call initiates
10. Green success notification appears with message "Event 'Clicked Shop Now' archived"

---

### TC-22: [CJS-10872] Verify Notifications - Archive Success Bulk Events

**Priority:** Normal | **Labels:** UI, Feedback

**Pre-condition:**
- Product: Web Experimentation
- Bulk archive completed successfully for 3 events

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 3 events
8. Click "Archive" button
9. Click "Archive 3 Events" in dialog
10. Wait for API calls to complete

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 3 events selected
8. Archive dialog opens
9. Bulk archive initiates
10. Green success notification appears with message "3 events archived"

---

### TC-23: [CJS-10872] Verify Notifications - Archive Error Handling

**Priority:** Normal | **Labels:** Error Handling, UI

**Pre-condition:**
- Product: Web Experimentation
- Archive API will fail (simulate 500 error or network failure)

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 1 event
8. Open DevTools and set breakpoint or use Network tab to simulate API failure (500 error)
9. Click "Archive" button
10. Click "Archive Event" in dialog
11. Wait for API to fail

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 1 event selected
8. DevTools ready to simulate failure
9. Archive dialog opens
10. Archive initiated
11. Warning notification appears with message "Could not archive event. {error message}"

---

### TC-24: [CJS-10872] Verify Race Condition - Bulk Archive Loading State

**Priority:** Normal | **Labels:** State Management, API

**Pre-condition:**
- Product: Web Experimentation
- About to archive 5 events simultaneously

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Enter select mode and select 5 events
8. Click "Archive" button
9. Observe the UI during archive process
10. Click "Archive 5 Events" in dialog
11. Observe global loading state and dialog loading state

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Select mode active, 5 events selected
8. Archive dialog opens
9. UI ready for observation
10. Archive initiates
11. No global loading spinner appears (race condition prevented by `skipGlobalLoading: true`), only archive dialog shows spinner in button, multiple PUT requests execute in parallel (Promise.all)

---

### TC-25: [CJS-10872] Verify Events List - Refresh After Archive

**Priority:** Normal | **Labels:** State Management, API

**Pre-condition:**
- Product: Web Experimentation
- Events list has 3 events, about to archive 1

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Observe 3 events in list
8. Enter select mode, select 1 event, archive it
9. Open DevTools Network tab
10. Confirm archive in dialog
11. Wait for archive to complete
12. Observe Events list and Network tab

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. 3 events displayed
8. Select mode active, archive initiated
9. Network tab ready
10. Archive completes
11. Dialog closes
12. fetchEvents API call is made (GET `/api/v1/projects/{id}/events?filter=archived:false`), Events list updates to show 2 remaining events

---

### TC-26: [CJS-10872] Verify Event Editor - Archive Button Exists

**Priority:** Normal | **Labels:** UI, Integration

**Pre-condition:**
- Product: Web Experimentation
- Event Editor open for existing event

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click on an existing event to edit
8. Observe Event Editor popup

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Event Editor opens with event details
8. "Archive" button is visible in Event Editor UI (along with Save/Cancel buttons)

---

### TC-27: [CJS-10872] Verify Event Editor - Archive from Editor

**Priority:** Normal | **Labels:** Functional, Integration

**Pre-condition:**
- Product: Web Experimentation
- Event Editor open for event "Clicked Shop Now"

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon, click event "Clicked Shop Now"
7. Event Editor opens
8. Click "Archive" button in Event Editor
9. Confirm in archive dialog

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Event Editor opens
7. Event details displayed
8. Archive dialog opens
9. Event is archived via PUT API, Event Editor closes, event removed from Events list, success notification shown

---

### TC-28: [CJS-10872] Verify Event Editor - Refresh After Save

**Priority:** Normal | **Labels:** State Management, API

**Pre-condition:**
- Product: Web Experimentation
- Event Editor open for existing event

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon, click an event to edit
7. Modify event name
8. Open DevTools Network tab
9. Click "Save" button
10. Wait for save to complete

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Event Editor opens
7. Event name modified
8. Network tab ready
9. Save initiates
10. PUT API call completes, Event Editor closes, fetchEvents API call is made, Events list refreshes with updated event name

---

### TC-29: [CJS-10872] Verify Popover - Scroll Behavior with Many Events

**Priority:** Low | **Labels:** UI, UX

**Pre-condition:**
- Product: Web Experimentation
- Events list has 15+ events

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Observe the popover with 15+ events
8. Scroll within the Events list using mouse wheel
9. Try scrolling to bottom of list

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Events list displays with scrollable area
8. List scrolls smoothly within popover container
9. Scrolling works without closing popover, all events accessible via scroll

---

### TC-30: [CJS-10872] Verify Regression - Event Creation Still Works

**Priority:** High | **Labels:** Regression, Functional

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click on a button element on the page
7. Select "Create Click Event" from context menu
8. Enter event name "New Click Event"
9. Click "Save"

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Element highlighted
7. Event creation popup opens
8. Event name entered
9. Event created successfully (POST `/api/v1/events`), success notification shown, event appears in Events list

---

### TC-31: [CJS-10872] Verify Regression - Event Editing Still Works

**Priority:** High | **Labels:** Regression, Functional

**Pre-condition:**
- Product: Web Experimentation
- At least one event exists

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click on an existing event
8. Change event name to "Updated Event Name"
9. Click "Save"

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Event Editor opens
8. Event name modified
9. Event updated successfully (PUT `/api/v1/events/{id}`), success notification shown, updated name reflected in Events list

---

### TC-32: [CJS-10872] Verify Regression - Event Selector Highlighting

**Priority:** Normal | **Labels:** Regression, Visual Editor

**Pre-condition:**
- Product: Web Experimentation
- Event with selector `.shop-now` exists

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Click Events icon to open Events list
7. Click on event with selector `.shop-now`
8. Observe the target page

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Attributes popover opens
7. Event Editor opens
8. Element matching selector `.shop-now` is highlighted on the page with blue border

---

### TC-33: [CJS-10872] Verify Regression - Bottom Bar Layout Intact

**Priority:** Normal | **Labels:** Regression, UI

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded

**Parameters:**
- Environment: RC
- Viewport: 1920x1080 (desktop), 768x1024 (tablet), 375x667 (mobile)

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Observe bottom bar layout at desktop viewport
7. Resize to tablet viewport (768px width)
8. Resize to mobile viewport (375px width)

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays with all buttons
6. Events button fits properly alongside Changes button and other controls, no layout breaks
7. Bottom bar adapts to tablet width, buttons remain accessible
8. Bottom bar adapts to mobile width, all buttons visible (may stack or compress)

---

### TC-34: [CJS-10872] Verify Regression - Segment Analytics Integration

**Priority:** Normal | **Labels:** Regression, Analytics

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Open browser Console and filter for Segment events
7. Perform various actions: open Events list, create event, archive event
8. Observe console logs

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Console ready to capture Segment events
7. Actions performed
8. Segment events are tracked correctly: `Attributes_Opened`, `Click_Create_EVENT`, `Archived_Event` logged with correct event properties

---

### TC-35: [CJS-10872] Verify Regression - Notifications System

**Priority:** Low | **Labels:** Regression, UI

**Pre-condition:**
- Product: Web Experimentation
- Visual Editor loaded

**Parameters:**
- Environment: RC

**Test Steps:**
1. Navigate to https://rc-app.optimizely.com/signin and login with test credentials
2. Navigate to the Web project "QA Test Project"
3. Go to Experiments page and open experiment "Homepage A/B Test"
4. Click on "Variation #1" to open Visual Editor
5. Wait for Visual Editor to fully load
6. Trigger a success notification (e.g., archive event successfully)
7. Observe notification appears
8. Wait for auto-dismiss
9. Trigger multiple notifications in sequence

**Expected Results:**
1. Login succeeds
2. Web project page displays
3. Experiment details page opens
4. Visual Editor loads
5. Bottom bar displays
6. Success notification appears at top/corner of screen
7. Notification displays with correct message and green color
8. Notification auto-dismisses after 3-5 seconds
9. Multiple notifications stack vertically without overlapping, each dismisses independently

---

## Notes

- **Environment:** All test cases use RC (https://rc-app.optimizely.com) as default testing environment unless Opal features are tested
- **Test Data:** Use project "QA Test Project" and experiment "Homepage A/B Test" for consistency
- **Browser:** Default to Chrome; cross-browser testing (Firefox, Safari, Edge) recommended for P0 cases
- **API Verification:** Use DevTools Network tab to verify API calls and payloads
- **Analytics Verification:** Use Browser Console to verify Segment event tracking

---

**Test Case Document Generated by:** Claude Code via `/exp-qa-agents:generate-test-cases` skill
**Review Status:** Pending User Approval
**JIRA Upload Status:** Not uploaded yet
