# Full Flow Testing Specification

**Test Environment:** Visual Editor (New VE)
**Date Created:** 2026-03-16
**Status:** Active

---

## 1. Overview

This document describes the complete end-to-end testing flow for the Visual Editor feature, from experiment creation through live website verification. The full flow covers experiment setup, variation preview, publishing, and live site bucketing.

### Test Website
- **URL:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html
- **Type:** E-commerce website with donation buttons

### Experiment Details
- **Project ID:** 4868003032989696
- **Experiment ID:** 6255713597521920
- **Saved Page:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html

---

## Scope Matrix — Ticket → Phase & Checkpoint Mapping

> **Purpose**: Xác định Phase nào và Checkpoint nào cần regression khi analyze ticket.
> Claude đọc bảng này TRƯỚC khi đọc full flow sequence để filter context.

### Triggers per Phase (keyword matching)

| Phase | Triggers — nếu ticket chứa các keyword này → focus vào phase này |
|---|---|
| **Phase 1 — Setup** | events, metrics, saved page, create event, event name, click event, metric, implementation tab |
| **Phase 2 — VE Changes** | visual editor, changes, element, CSS, color, background, selector, interactive mode, VE, insert HTML, apply change, style |
| **Phase 3 — Preview** | preview variation, preview popup, preview button, preview API, changes visible in preview |
| **Phase 4 — Publish** | publish, start experiment, status Running, commit, status transition, go live, snippet push, CDN |
| **Phase 5 — Live Site** | live site, bucket, bucketing, snippet, CDN, changes not showing, event tracking, result page, visitor count, event count |

### Scope Matrix

| Ticket touches... | Focus Phases | Key CPs to verify | Other phases |
|---|---|---|---|
| Preview variation (button, popup, changes visible) | Phase 3 | CP-3, CP-4 | Verify Phase 2 baseline |
| Publish / start experiment | Phase 4 | CP-5, CP-6 | Verify Phase 3 baseline |
| Live site / snippet / CDN / changes not showing | Phase 5 | CP-7, CP-8 | Verify Phase 4 as baseline |
| Event tracking / result page / visitor count | Phase 5 | CP-9, CP-10 | — |
| VE changes / element editing / CSS / selector | Phase 2 | CP-3 | Phase 3 to verify preview still correct |
| Events / metrics setup | Phase 1 | CP-1, CP-2 | — |
| Status: Paused behavior | Phase 4 + Phase 5 | CP-5 + CP-7, CP-8 | Phase 3 as baseline |
| Status: Archived behavior | Phase 4 + Phase 5 | CP-5 + CP-7, CP-8 | Phase 3 as baseline |
| Status: Concluded behavior | Phase 4 + Phase 5 | CP-5 + CP-7, CP-8 | Phase 3 as baseline |
| Status: Concluded & Deployed | Phase 4 + Phase 5 | CP-5 + CP-7, CP-8 | Phase 3 as baseline |
| Multi-page saved pages | All phases | CP-1 through CP-10 | — |
| Interactive mode / cross-page element selection | Phase 2 + Phase 3 | CP-3, CP-4 | — |
| Enable Support for Dynamic Websites ON/OFF | Phase 5 | CP-7, CP-8 | — |
| Full regression / new feature | All phases | CP-1 through CP-10 | — |

### How Claude should use this

1. Extract ticket keywords → match against **Triggers per Phase** table above
2. Identify Focus Phases → read only those phase sections in detail (Section 2 below)
3. Map to Key CPs → use CP rows from **Section 3 (Critical Verification Checkpoints)** as Expected Results templates
4. State explicitly in output: `"Full Flow Focus: Phase 3 (CP-3, CP-4) | Skipping: Phase 1, 4, 5 — not touched by this ticket"`

---

## 2. Full Flow Sequence

### Phase 1: Test Setup (Pre-VE)

#### Step 1.1: Create Events
**Action:** Set up tracking events for donation buttons

- **Event 1:** Click-Donate2
  - Type: Click Event
  - Target: "Donate Today" button
  - Description: Tracks primary donation button clicks

- **Event 2:** Learn More Click
  - Type: Click Event
  - Target: "Learn More" button
  - Description: Tracks secondary CTA clicks

**Verification Points:**
- Events visible in Implementation > Events tab
- Events linked to the saved page
- Event names correctly configured in Monolith

---

#### Step 1.2: Create Experiment
**Action:** Create A/B test experiment with saved page targeting

- **Type:** A/B Test
- **Name:** Visual Editor Variation Test
- **Saved Page Target:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html
- **Status:** Draft

**Verification Points:**
- Experiment appears in Optimizations > Experiments tab
- Saved page configured in Activation tab
- Experiment in Draft status

---

#### Step 1.3: Add Metrics
**Action:** Configure experiment metrics using created events

- **Primary Metric:** Click-Donate2 event
  - Source: Custom event
  - Goal Type: Count

- **Secondary Metric:** Learn More Click event
  - Source: Custom event
  - Goal Type: Count

**Verification Points:**
- Metrics configured in Track > Metrics section
- Event data flowing from page tracking

---

### Phase 2: Variation Creation (In VE)

#### Step 2.1: Open Visual Editor
**Action:** Open first variation in Visual Editor

**Navigation Path:**
1. Go to Experiment Detail
2. Click Variations tab
3. Click variation row to open VE

**VE Loading Verification:**
- Visual Editor loads in Shadow DOM
- Bottom bar visible with variation tabs
- Website content renders inside VE frame
- Interactive mode ready (Alt key toggle)

---

#### Step 2.2: Make Visual Changes
**Action:** Edit element styling in Visual Editor

**Changes Made:**
1. **Color Change**
   - Element: Heading (h1)
   - CSS Property: color
   - New Value: red
   - Change Type: Custom CSS
   - Selector: head
   - Implementation: `<style>h1{ color: red; }</style>`

2. **Create New Button Element**
   - Element: Insert after h1
   - Type: Button
   - Class: extra-btn
   - Text: "Extra Action"
   - Implementation: Custom JavaScript code in VE

**Verification Points (in VE):**
- Changes appear in Changes list
- Live preview shows styled element
- Change count increments correctly
- Unsaved changes warning appears

---

### Phase 3: Variation Preview (VE UI)

#### Step 3.1: Preview Variation in VE
**Action:** Click Preview button for single variation

**Network Calls Expected:**
- GET `4868003032989696.js` (Config with changes)
- GET `preview_lay_data.js` (Preview data)
- GET `geo4.js` (Geolocation/targeting data)

**Verification Points:**
- Preview popup opens showing the website
- All CSS changes visible: h1 is red
- New button visible: "Extra Action"
- Preview is read-only (cannot interact with elements)

**Expected Results:**
1. h1 element displays in red color
2. "Extra Action" button appears below h1
3. Element styling matches VE editor preview

---

### Phase 4: Publish & Go Live

#### Step 4.1: Publish Experiment
**Action:** Click Publish/Start button to go live

**Network Calls Triggered:**

| Step | API Call | Method | Status | Purpose |
|------|----------|--------|--------|---------|
| 4.1.1 | commit.js | POST | 201 | Commit changes to monolith |
| 4.1.2 | Event | POST | 204 | Log publish event |
| 4.1.3 | /live | PUT | 202 | Push experiment to live |
| 4.1.4 | 5129813690679290 | GET | 200 | Fetch updated experiment state |
| 4.1.5 | Event | POST | 204 | Log state update event |
| 4.1.6 | Event | POST | 204 | Log completion event |

**Monolith Verification:**
- Experiment status changes from Draft to Running
- Variations tab shows both Control and Variation with changes
- History tab logs publish action with user and timestamp
- Traffic allocation shows 50/50 split (default A/B)
- API Names section shows numeric variation IDs
- Results page ready for data collection

**Verification Points:**
1. Experiment status in monolith = Running
2. No edit capabilities available (read-only mode)
3. Publish confirmation shown
4. All network calls complete (202 indicates async processing)

---

### Phase 5: Live Site Verification

#### Step 5.1: Visit Website & Bucket into Variation
**Action:** Open website in incognito mode and force bucketing

**Network Calls:**
- GET `4868003032989696.js` (Fetch experiment config with changes)
- Event POST (User assignment tracking)

**Bucketing Method:**
- Use Optimizely admin tools or URL parameter to force bucket into variation
- Alternative: Visit multiple times to naturally bucket

**Verification Points:**
1. Website loads experiment config
2. User bucketed into variation group
3. Changes applied to live page:
   - h1 displays in red color
   - "Extra Action" button visible below h1

---

#### Step 5.2: Verify Event Tracking
**Action:** Interact with page and verify event firing

**User Actions:**
1. Click "Donate Today" button
2. Verify Click-Donate2 event fires

**Network Call Expected:**
- Event POST (Event tracking request)
- Status: 204 No Content

**Verification Points:**
1. Click-Donate2 event captured in network tab
2. Event payload includes:
   - User ID / Visitor ID
   - Experiment ID: 6255713597521920
   - Variation ID
   - Event name: Click-Donate2
   - Timestamp
3. Event processing status: 204 (success)

**Results Dashboard:**
- Event appears in Experiment Results
- Conversion tracked for Click-Donate2 metric
- Data visible in 24-48 hours

---

## 3. Critical Verification Checkpoints

| Checkpoint | Phase | Verification | Expected Result |
|-----------|-------|-------------|-----------------|
| **CP-1** | Setup | Events created | Events visible in Implementation tab |
| **CP-2** | Setup | Metrics added | Metrics configured in Track section |
| **CP-3** | VE | Changes applied | Live preview in VE shows red h1 + new button |
| **CP-4** | VE | Variation preview | Preview popup shows all changes correctly |
| **CP-5** | Publish | Status transition | Experiment status = Running in Monolith |
| **CP-6** | Publish | Variations displayed | Both variations visible in Monolith Variations tab |
| **CP-7** | Live | Config loaded | Website receives experiment config with changes |
| **CP-8** | Live | Element changes visible | Red h1 + "Extra Action" button visible on live site |
| **CP-9** | Live | Event tracking | Click-Donate2 event fires and tracked |
| **CP-10** | Live | Results collection | Event appears in experiment results dashboard |

---

## 4. Network Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│              PHASE 1: Setup (Monolith)                  │
├─────────────────────────────────────────────────────────┤
│  - Create Events (Click-Donate2, Learn More)            │
│  - Create Experiment (A/B Test)                         │
│  - Add Metrics                                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 2-3: VE & Preview                    │
├─────────────────────────────────────────────────────────┤
│  - Open VE (iframe)                                     │
│  - Make changes (CSS + JS)                              │
│  - Preview Variation                                    │
│    └─ GET 4868003032989696.js (config + changes)       │
│    └─ GET preview_lay_data.js                          │
│    └─ GET geo4.js                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 4: Publish                           │
├─────────────────────────────────────────────────────────┤
│  - POST commit.js (201)                                 │
│  - POST Event (204)                                     │
│  - PUT /live (202) ◄─ Async processing                  │
│  - GET 5129813690679290 (200)                           │
│  - POST Event x2 (204)                                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 5: Live Verification                 │
├─────────────────────────────────────────────────────────┤
│  - GET 4868003032989696.js (live config)                │
│  - POST Event (assignment tracking)                     │
│  - Verify visual changes on website                     │
│  - Click button → POST Event (204)                      │
│  - Verify event in results dashboard                    │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Troubleshooting Guide

### Issue: Changes not visible in VE preview
- **Check:** CSS selector matches target element
- **Check:** Change order in changeStore (CSS must apply before visual check)
- **Fix:** Re-generate selector or adjust change dependencies

### Issue: Publish fails (404 on commit.js)
- **Check:** Network connectivity
- **Check:** OAuth token validity (auth.ts token expiry)
- **Fix:** Refresh page, re-authenticate

### Issue: Live site doesn't show changes
- **Check:** Config loaded correctly (check 4868003032989696.js response)
- **Check:** User properly bucketed into variation
- **Check:** Browser cache (use incognito mode)
- **Fix:** Force refresh, check bucketing logic

### Issue: Event not firing on click
- **Check:** Event selector is still valid on live site
- **Check:** Element exists and is clickable
- **Check:** Network tab shows Event POST call
- **Fix:** Verify selector in EventEditor, check element DOM structure

---

## 6. Test Data Reference

| Item | Value | Notes |
|------|-------|-------|
| Test Domain | quynhnguyenepi.github.io | E-commerce site |
| Project ID | 4868003032989696 | Optimizely project |
| Experiment ID | 6255713597521920 | A/B test experiment |
| Event 1 | Click-Donate2 | Primary button click |
| Event 2 | Learn More | Secondary button click |
| CSS Change | color: red | h1 element styling |
| JS Change | Create button | Insert "Extra Action" button |
| Default Traffic | 50/50 | Control vs Variation |

---

## 7. Related Documentation

- `API_ENDPOINTS.md` — Detailed API endpoint specifications
- `CLAUDE.md` Section 5 — Functional tree (Monolith screens)
- `docs/API.md` — Generated from API-fullFlow.xlsx

---

**Last Updated:** 2026-03-16
**Maintained By:** QA Team
**Version:** 1.0
