# Sample Analysis: CJS-10873 - Add thread ID as property

This is a real example of a ticket analysis produced by the analyze-ticket skill.

---

## Ticket Analysis: CJS-10873 - "Add thread ID as property"

### Summary

| Field | Value |
|-------|-------|
| **Epic** | CJS-9699 - "Using Opal to build entire variations" |
| **Status** | In Testing |
| **Type** | Story |
| **Assignee** | Md. Mahadi Sourav |
| **Label** | `Requires_QA` |

### What the ticket asks

Add `thread_id` as a property to these Segment tracking events:
- `EXP - VE - save_all_opal`
- `EXP - VE - undo_all_opal`

### What was actually implemented (3 merged PRs)

**PR #374** (direct ticket PR) - Added thread ID to the current thread on creation + fixed tracking strings (removed "Exp - VE -" prefix from individual event names since `EVENT_PREFIX` handles it)

**PR #382** (follow-up fix) - Centralized tracking properties via `globalProperties` in segmentStore. `experiment_id`, `project_id`, `variation_name`, `variation_id` are now set as global properties and auto-included in ALL events.

**PR #387** (latest follow-up) - Fixed `thread_id` not sent on `opal_thread_created` event, added `opal_apply_change` tracking in LLM tools, added environment-based Opal Chat URL configuration.

### Scope of changes: **Broad**

The PRs went significantly beyond the ticket AC:
1. Refactored the entire Segment tracking system (global properties pattern)
2. Changed event name prefixing across multiple components
3. Added new tracking events (`opal_apply_change`)
4. Modified store behavior (`setGlobalProperties` now merges instead of replaces)

---

### Test Cases

#### P0 - Core Acceptance Criteria

| # | Test Case | What to verify |
|---|-----------|----------------|
| 1 | **`save_all_opal` has `thread_id`** | Open Opal chat, get a suggestion, click "Save All" on OpalPreviewBanner. Verify the Segment event `EXP - VE - save_all_opal` includes `thread_id` property with a valid value |
| 2 | **`undo_all_opal` has `thread_id`** | Open Opal chat, get a suggestion, click "Undo All" on OpalPreviewBanner. Verify the Segment event `EXP - VE - undo_all_opal` includes `thread_id` property with a valid value |

#### P1 - Directly Related Functionality

| # | Test Case | What to verify |
|---|-----------|----------------|
| 3 | **`opal_thread_created` has `thread_id`** | Start a new Opal conversation. Verify `EXP - VE - opal_thread_created` event includes the `thread_id` |
| 4 | **Thread ID persists across interactions** | After creating a thread, interact with Opal (apply suggestion, save). Verify the same `thread_id` is consistently used across all events in that session |
| 5 | **New thread on variation switch** | Switch to a different variation. Verify a new thread is created and subsequent events use the new thread_id |

#### P2 - Broader Changes (Global Properties Refactor)

| # | Test Case | What to verify |
|---|-----------|----------------|
| 6 | **All events include `experiment_id`** | Trigger any Opal event. Verify `experiment_id` is automatically included as a property (via global properties) |
| 7 | **All events include `project_id`** | Same as above, verify `project_id` is present |
| 8 | **`variation_name` updates on switch** | Switch variation, trigger an event. Verify `variation_name` reflects the new variation |
| 9 | **`variation_id` updates on switch** | Same as above for `variation_id` |
| 10 | **`opal_apply_change` tracked** | Use Opal dev agent to apply a change. Verify `EXP - VE - opal_apply_change` fires with `changeType` and `threadId` |
| 11 | **Event name format correct** | Check events appear as `EXP - VE - save_all_opal` (not double prefix `EXP - VE - EXP - VE - save_all_opal`) |

#### P3 - Regression

| # | Test Case | What to verify |
|---|-----------|----------------|
| 12 | **`open_ask_opal` still works** | Click Opal CTA button. Verify event fires without errors |
| 13 | **`save_opal_change` still works** | Save an Opal-generated change. Verify event fires |
| 14 | **`apply_opal_suggestion` still works** | Click an Opal suggestion. Verify event fires |
| 15 | **Interactive mode events** | Toggle interactive mode. Verify `EXP - VE - Interactive_mode` fires correctly |
| 16 | **Device emulation events** | Switch to mobile/tablet view. Verify events fire correctly |

### How to verify

The best way to verify Segment events is through:
1. **Browser DevTools > Network tab**: Filter for `api.segment.io` requests
2. **Request payload inspection**: Click on the request, go to "Payload" or "Preview" tab, inspect the `properties` object
3. **Segment Debugger**: If available, use the Segment Debugger for real-time event monitoring

### Test Data Requirements

- An Optimizely account with Opal (AI) enabled (`use_opal` feature flag)
- A web experiment with at least 2 variations
- A target website that can be loaded in the Visual Editor
- CSP Unblock extension enabled

### Environment

- **Primary**: Integration (inte)
- **Secondary**: RC/Preproduction (prep) after inte passes

---

## Coverage Summary

| Priority | Count | % |
|----------|-------|---|
| P0 | 2 | 12% |
| P1 | 3 | 19% |
| P2 | 6 | 38% |
| P3 | 5 | 31% |
| **Total** | **16** | **100%** |

| Category | Count |
|----------|-------|
| Tracking/Analytics | 14 |
| State Management | 2 |

**Key insight**: This ticket is primarily about tracking/analytics changes, so most test cases focus on verifying Segment event payloads. The high P2 count reflects the significant refactoring that went beyond the original AC.
