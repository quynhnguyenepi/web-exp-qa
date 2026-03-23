# API Reference - Visual Editor Full Flow

**Source:** API-fullFlow.xlsx
**Generated:** 2026-03-16
**Environment:** Visual Editor Testing
**Total API Endpoints:** 12

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Reference](#quick-reference)
3. [API Endpoints by Phase](#api-endpoints-by-phase)
4. [Request/Response Patterns](#requestresponse-patterns)
5. [Status Codes & Authentication](#status-codes--authentication)
6. [Error Scenarios & Handling](#error-scenarios--handling)
7. [Performance & Caching](#performance--caching)
8. [Related Documentation](#related-documentation)

---

## Overview

This document provides comprehensive API specifications for the Visual Editor testing flow, covering all 12 API calls across 3 phases:

1. **Phase 1: Preview Variation** (3 API calls)
2. **Phase 2: Publish / Start Experiment** (6 API calls)
3. **Phase 3: Live Site Verification** (3 API calls)

### Test Environment Details
- **Test Website:** https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html
- **Project ID:** 4868003032989696
- **Experiment ID:** 6255713597521920
- **Events Created:**
  - Click-Donate2 (Primary button click tracking)
  - Learn More (Secondary button click tracking)

### Testing Flow Summary
1. Create events on test page
2. Create A/B test experiment with saved page
3. Add metrics using created events
4. Make CSS/JS changes in Visual Editor
5. Preview individual variation
6. Publish/Start experiment
7. Visit live website and bucket into variation
8. Verify event tracking

---

## Quick Reference

### Summary Table

| # | Endpoint | Method | Status | Phase | Category |
|---|----------|--------|--------|-------|----------|
| 1 | `4868003032989696.js` | GET | 200 | Preview | Config |
| 2 | `preview_lay_data.js` | GET | 200 | Preview | Preview Data |
| 3 | `geo4.js` | GET | 200 | Preview | Geolocation |
| 4 | `commit.js` | POST | 201 | Publish | Commit |
| 5 | `Event` | POST | 204 | Publish | Analytics |
| 6 | `/live` | PUT | 202 | Publish | Live Push |
| 7 | `5129813690679290` | GET | 200 | Publish | State Fetch |
| 8 | `Event` | POST | 204 | Publish | Analytics |
| 9 | `Event` | POST | 204 | Publish | Analytics |
| 10 | `4868003032989696.js` | GET | 200 | Live | Config |
| 11 | `Event` | POST | 204 | Live | Analytics |
| 12 | `Event` | POST | 204 | Live | Analytics |

---

## API Endpoints by Phase

### PHASE 1: PREVIEW VARIATION
**Triggered when:** User clicks "Preview Variation" button in Visual Editor

---

#### 1.1 Experiment Configuration (4868003032989696.js)

**Endpoint Properties:**
- **Type:** JavaScript Config File
- **Method:** `GET`
- **HTTP Status:** `200 OK`
- **Purpose:** Fetch experiment config with applied VE changes
- **URL Pattern:** `https://cdn.optimizely.com/js/{projectId}.js`

**Expected Response Structure:**
```javascript
{
  "accountId": "21849171986",
  "namespace": "4868003032989696",
  "projectId": "4868003032989696",
  "revision": "1908",
  "anonymizeIP": true,
  "layers": [
    {
      "id": "{layerId}",
      "changes": [
        {
          "id": "9526DCBB-530F-4269-A1D4-A5D321F90B8A",
          "type": "append",
          "selector": "head",
          "value": "<style>h1{ color: red; }</style>"
        },
        {
          "id": "4E717DD3-5854-49B2-A135-02C49BE13D12",
          "type": "custom_code",
          "value": "function($) { /* button creation code */ }"
        }
      ]
    }
  ]
}
```

**Key Fields:**
- `accountId` — Optimizely account identifier
- `namespace` — Project namespace
- `revision` — Config version number
- `layers[].changes[]` — Array of DOM modifications
- `layers[].changes[].type` — Change type (append, custom_code, modify, remove)
- `layers[].changes[].selector` — CSS selector for target element
- `layers[].changes[].value` — Change content (HTML/CSS/JS code)

**VE-Specific Fields:**
- `isOpalManaged` — Whether change created by Opal AI
- `dependencies` — Change execution dependencies
- `name` — Human-readable change name

**Verification Points:**
- ✓ Config includes all VE changes (CSS + button creation)
- ✓ Revision number matches expected version
- ✓ Changes array is non-empty
- ✓ Selectors are valid CSS patterns
- ✓ Response time < 300ms

---

#### 1.2 Preview Layer Data (preview_lay_data.js)

**Endpoint Properties:**
- **Type:** JavaScript Data File
- **Method:** `GET`
- **HTTP Status:** `200 OK`
- **Purpose:** Fetch preview-specific layer and variation data
- **URL Pattern:** `https://p13ncore-ns.optimizely.com/preview_lay_data.js`

**Response Includes:**
- Variation assignment data
- Traffic allocation percentages (50/50 for A/B)
- Audience targeting information
- Preview-mode flags
- Visitor qualification rules

**Verification Points:**
- ✓ Data loads without errors
- ✓ Preview mode indicators present
- ✓ Variation data structure valid
- ✓ Traffic percentages sum to 100

---

#### 1.3 Geolocation & Targeting Data (geo4.js)

**Endpoint Properties:**
- **Type:** JavaScript Data File
- **Method:** `GET`
- **HTTP Status:** `200 OK`
- **Purpose:** Fetch geolocation and targeting rules
- **URL Pattern:** `https://cdn.optimizely.com/geo/4.js`

**Response Includes:**
- IP-based geolocation data
- Visitor location (country, region, city)
- Network information
- Targeting rule evaluation data

**Verification Points:**
- ✓ Geolocation data loaded
- ✓ Location data accurate for test environment
- ✓ Targeting rules properly formatted

---

### PHASE 2: PUBLISH / START EXPERIMENT
**Triggered when:** User clicks "Publish" or "Start" button in Monolith Experiment Detail

---

#### 2.1 Commit Changes (commit.js)

**Endpoint Properties:**
- **Type:** API Endpoint
- **Method:** `POST`
- **HTTP Status:** `201 Created`
- **Purpose:** Commit experiment changes to monolith backend
- **URL Pattern:** `https://api.optimizely.com/v2/experiments/{experimentId}/commit`

**Request Payload:**
```json
{
  "experimentId": "6255713597521920",
  "status": "running",
  "changes": [
    {
      "id": "9526DCBB-530F-4269-A1D4-A5D321F90B8A",
      "type": "append",
      "selector": "head",
      "value": "<style>h1{ color: red; }</style>"
    },
    {
      "id": "4E717DD3-5854-49B2-A135-02C49BE13D12",
      "type": "custom_code",
      "value": "function($) { /* button creation */ }"
    }
  ],
  "updatedAt": "2026-03-16T10:30:00Z"
}
```

**Success Response (201):**
```json
{
  "experimentId": "6255713597521920",
  "status": "success",
  "message": "Changes committed successfully",
  "timestamp": "2026-03-16T10:30:05Z"
}
```

**Verification Points:**
- ✓ HTTP status = 201 (indicates creation)
- ✓ Response includes experimentId confirmation
- ✓ Timestamp reflects exact API call time
- ✓ Status field = "success"

---

#### 2.2 Publish Events (Event POST calls) - 3 instances

**Endpoint Properties (all Event calls):**
- **Type:** Tracking/Analytics API
- **Method:** `POST`
- **HTTP Status:** `204 No Content`
- **Purpose:** Log publish actions and state transitions for analytics
- **URL Pattern:** `https://api.segment.com/v1/track` or `https://p13ncore-ns.optimizely.com/events`

**Event 1: Publish Action Log**
```json
{
  "eventName": "experiment_published",
  "experimentId": "6255713597521920",
  "projectId": "4868003032989696",
  "userId": "{userId}",
  "timestamp": "2026-03-16T10:30:05Z",
  "properties": {
    "status": "running",
    "variationCount": 2,
    "changeCount": 2,
    "source": "monolith"
  }
}
```

**Event 2: State Update Log**
```json
{
  "eventName": "experiment_state_updated",
  "experimentId": "6255713597521920",
  "previousStatus": "draft",
  "newStatus": "running",
  "timestamp": "2026-03-16T10:30:10Z"
}
```

**Event 3: Completion Log**
```json
{
  "eventName": "experiment_publish_complete",
  "experimentId": "6255713597521920",
  "duration": "12 seconds",
  "success": true,
  "timestamp": "2026-03-16T10:30:15Z"
}
```

**Verification Points (all Event calls):**
- ✓ HTTP status = 204 (no content return, logging only)
- ✓ Event names follow naming convention
- ✓ Timestamps chronologically ordered
- ✓ All required fields present
- ✓ Response time < 200ms

---

#### 2.3 Push to Live (/live)

**Endpoint Properties:**
- **Type:** API Endpoint
- **Method:** `PUT`
- **HTTP Status:** `202 Accepted`
- **Purpose:** Push experiment to live environment (async operation)
- **URL Pattern:** `https://api.optimizely.com/v2/experiments/{experimentId}/live`

**Request Payload:**
```json
{
  "experimentId": "6255713597521920",
  "action": "publish",
  "environment": "production",
  "async": true,
  "timestamp": "2026-03-16T10:30:05Z"
}
```

**Async Response (202):**
```json
{
  "status": "accepted",
  "taskId": "task-98765432",
  "message": "Experiment deployment initiated",
  "estimatedTime": "2-5 minutes",
  "pollUrl": "/v2/experiments/6255713597521920/tasks/task-98765432"
}
```

**⚠️ IMPORTANT: Async Processing**
- Status 202 means the operation is queued, NOT complete
- Use `taskId` to poll status
- Expected deployment time: 2-5 minutes
- Poll `/tasks/{taskId}` every 5 seconds

**Verification Points:**
- ✓ HTTP status = 202 (async accepted)
- ✓ taskId provided for polling
- ✓ estimatedTime within reasonable range
- ✓ pollUrl format correct

---

#### 2.4 Fetch Updated State (5129813690679290)

**Endpoint Properties:**
- **Type:** State/Config Fetch
- **Method:** `GET`
- **HTTP Status:** `200 OK`
- **Purpose:** Fetch updated experiment state after commit
- **URL Pattern:** `https://api.optimizely.com/v2/experiments/{projectId}`

**Expected Response:**
```json
{
  "experimentId": "6255713597521920",
  "status": "running",
  "variations": [
    {
      "id": "6274013178101760",
      "name": "Variation #1",
      "traffic": 50,
      "changes": [
        {
          "id": "9526DCBB-530F-4269-A1D4-A5D321F90B8A",
          "type": "append",
          "selector": "head",
          "value": "<style>h1{ color: red; }</style>"
        }
      ]
    },
    {
      "id": "6274013178101761",
      "name": "Control",
      "traffic": 50,
      "changes": []
    }
  ],
  "createdAt": "2026-03-16T09:00:00Z",
  "updatedAt": "2026-03-16T10:30:10Z"
}
```

**Verification Points:**
- ✓ Status changed to "running"
- ✓ Variations array populated with 2 entries (Control + Variation #1)
- ✓ Traffic allocation = 50/50
- ✓ Changes array in Variation #1 includes CSS + JS changes
- ✓ Control variation has empty changes array
- ✓ updatedAt timestamp recent (within last 1 minute)

---

### PHASE 3: LIVE SITE VERIFICATION
**Triggered when:** User visits website and interacts with bucketed variation

---

#### 3.1 Load Experiment Config (4868003032989696.js)

**Endpoint Properties:**
- **Type:** JavaScript Config File
- **Method:** `GET`
- **HTTP Status:** `200 OK`
- **Purpose:** Fetch live experiment config on website load
- **URL Pattern:** `https://cdn.optimizely.com/js/{projectId}.js`
- **Context:** Same as Phase 1 (section 1.1) but from live production environment

**Response:** Contains all VE changes (CSS color + button creation)

**Verification Points:**
- ✓ Config loads without errors
- ✓ Changes included in response
- ✓ User properly bucketed into variation
- ✓ h1 displays in red color on website
- ✓ "Extra Action" button visible below h1

---

#### 3.2 Visitor Assignment Tracking Event

**Endpoint Properties:**
- **Type:** Tracking/Analytics API
- **Method:** `POST`
- **HTTP Status:** `204 No Content`
- **Purpose:** Track visitor assignment to variation
- **URL Pattern:** `https://api.segment.com/v1/track`

**Request Payload:**
```json
{
  "eventName": "experiment_visitor_assigned",
  "experimentId": "6255713597521920",
  "visitorId": "{visitorId}",
  "variationId": "6274013178101760",
  "variationName": "Variation #1",
  "timestamp": "2026-03-16T10:35:00Z",
  "properties": {
    "traffic_allocation": 50,
    "audience_qualified": true
  }
}
```

**Verification Points:**
- ✓ Visitor ID captured
- ✓ Variation ID matches expected
- ✓ Timestamp reflects assignment time
- ✓ Event appears in tracking dashboard

---

#### 3.3 Conversion Event (Click-Donate2)

**Endpoint Properties:**
- **Type:** Tracking/Analytics API
- **Method:** `POST`
- **HTTP Status:** `204 No Content`
- **Purpose:** Track Click-Donate2 button click conversion
- **URL Pattern:** `https://api.segment.com/v1/track`

**Request Payload:**
```json
{
  "eventName": "Click-Donate2",
  "experimentId": "6255713597521920",
  "visitorId": "{visitorId}",
  "variationId": "6274013178101760",
  "timestamp": "2026-03-16T10:35:15Z",
  "properties": {
    "elementSelector": "button.donate-btn",
    "pageUrl": "https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html",
    "eventValue": 1,
    "revenue": null
  }
}
```

**Verification Points:**
- ✓ Event name matches "Click-Donate2" (created in Phase 1)
- ✓ Visitor ID and variation ID present
- ✓ Event timestamp follows assignment time
- ✓ Event appears in Results dashboard
- ✓ Metric data ingested within 24-48 hours

---

## Request/Response Patterns

### Pattern 1: Configuration Fetch (Cacheable)
```
CLIENT REQUEST:
GET https://cdn.optimizely.com/js/{projectId}.js
Headers:
  - Accept: application/javascript
  - If-None-Match: "{etag}"
  - Authorization: Bearer {token}

SERVER RESPONSE (200 OK):
Content-Type: application/javascript
ETag: "{etag}"
Cache-Control: max-age=300, public
Content-Length: {bytes}
{
  "projectId": "4868003032989696",
  "layers": [ { "changes": [...] } ]
}
```

**Cache Strategy:** 5-minute cache for config files
**Headers:** Accept ETag for 304 Not Modified responses

---

### Pattern 2: Tracking Event (Non-Cacheable)
```
CLIENT REQUEST:
POST https://api.segment.com/v1/track
Headers:
  - Content-Type: application/json
  - Authorization: Bearer {token}
  - X-Segment-Write-Key: {key}
Body:
{
  "eventName": "...",
  "experimentId": "...",
  "timestamp": "ISO-8601"
}

SERVER RESPONSE (204 No Content):
Content-Length: 0
Cache-Control: no-store, no-cache
(No body)
```

**Cache Strategy:** No caching (always fresh)
**Response:** Empty body with 204 status

---

### Pattern 3: Async Operation (202 Accepted)
```
CLIENT REQUEST:
PUT https://api.optimizely.com/v2/experiments/{id}/live
{ "action": "publish", "async": true }

SERVER RESPONSE (202 Accepted):
{
  "status": "accepted",
  "taskId": "task-12345",
  "pollUrl": "/v2/tasks/task-12345"
}

POLLING (every 5 seconds):
GET https://api.optimizely.com/v2/tasks/task-12345

FINAL RESPONSE (when complete):
{
  "status": "completed",
  "result": { "experimentId": "...", "status": "running" }
}
```

**Key Pattern:** Use taskId to poll until status = "completed"

---

## Status Codes & Authentication

### HTTP Status Codes Reference

| Status | Meaning | When Used | Handling |
|--------|---------|-----------|----------|
| `200` | OK | Successful GET/data retrieval | Process response |
| `201` | Created | Successful resource creation (POST) | Confirm creation |
| `202` | Accepted | Async operation initiated | Poll with taskId |
| `204` | No Content | Event logged successfully | Confirm (no body) |
| `304` | Not Modified | Cached response still valid | Use local cache |
| `400` | Bad Request | Invalid request payload | Fix request data |
| `401` | Unauthorized | OAuth token expired/invalid | Refresh token |
| `403` | Forbidden | User lacks permission | Check user role |
| `404` | Not Found | Endpoint/resource doesn't exist | Verify URL/ID |
| `500` | Server Error | Backend service failure | Retry with backoff |
| `502` | Bad Gateway | Upstream service unavailable | Retry later |
| `503` | Service Unavailable | Maintenance/overload | Retry with exponential backoff |

---

### Authentication & Headers

**Required Headers (All Endpoints):**
```
Authorization: Bearer {oauth_token}
Content-Type: application/json
X-Project-Id: 4868003032989696
X-Request-Id: {unique-request-id}
User-Agent: Optimizely-VE/1.0
```

**OAuth Token Management:**
- **Source:** Monolith auth service (OAuth2)
- **Expiry:** 1 hour from issue time
- **Refresh:** Automatic at 55 minutes
- **Storage:** sessionStorage (in VE iframe)
- **Refresh Mechanism:** authStore.ts auto-refresh

**Token Validation:**
```javascript
// In VE: src/stores/authStore.ts
const token = await refreshTokenIfNeeded();
// Automatically handles 401 responses
```

---

## Error Scenarios & Handling

### Scenario 1: 401 Unauthorized (Token Expired)

**Error Response:**
```json
{
  "error": "unauthorized",
  "message": "Token expired",
  "error_code": "TOKEN_EXPIRED",
  "refresh_required": true
}
```

**Root Causes:**
- OAuth token age ≥ 1 hour
- User session timeout
- Token revoked by admin

**Handling:**
```javascript
// Auto-handled by authStore.ts
const newToken = await authStore.refreshToken();
// Automatic retry of failed request
```

**Verification:**
- ✓ Page doesn't show errors to user
- ✓ New token fetched silently
- ✓ Original request retried

---

### Scenario 2: 202 Accepted (Async Task Hangs)

**Initial Response:**
```json
{
  "status": "accepted",
  "taskId": "task-12345",
  "estimatedTime": "2-5 minutes"
}
```

**Polling Response (stuck):**
```json
{
  "status": "processing",
  "taskId": "task-12345",
  "progress": 45,
  "estimatedRemaining": "3 minutes"
}
```

**Root Causes:**
- Heavy system load
- Large number of changes
- Backend service issues

**Handling:**
```javascript
// Poll every 5 seconds
const pollTask = async (taskId) => {
  while (true) {
    const response = await fetch(`/v2/tasks/${taskId}`);
    if (response.status === "completed") break;
    if (response.status === "failed") throw new Error(response.error);
    await wait(5000); // 5 second delay
  }
};
```

**Timeout Strategy:**
- Max polling time: 15 minutes
- If exceeds: Show user "still processing" message
- User can refresh page to check later

---

### Scenario 3: 404 Not Found

**Error Response:**
```json
{
  "error": "not_found",
  "message": "Experiment 6255713597521920 not found",
  "error_code": "EXPERIMENT_NOT_FOUND"
}
```

**Root Causes:**
- Experiment ID incorrect
- Experiment deleted
- Wrong project/environment

**Handling:**
- Verify experiment exists in Monolith first
- Check experiment ID in URL
- Confirm user has access to project

---

## Performance & Caching

### Response Time SLA

| Endpoint | Avg | P95 | P99 | SLA |
|----------|-----|-----|-----|-----|
| Config GET (4868003032989696.js) | 150ms | 300ms | 500ms | 95% < 300ms |
| Preview GET (preview_lay_data.js) | 200ms | 400ms | 600ms | 95% < 400ms |
| Geo GET (geo4.js) | 100ms | 200ms | 400ms | 95% < 200ms |
| Commit POST (commit.js) | 300ms | 600ms | 1s | 95% < 600ms |
| Event POST | 50ms | 100ms | 200ms | 95% < 100ms |
| Live PUT (/live) | 200ms | 500ms | 2s | 95% < 500ms |
| State GET (5129813690679290) | 100ms | 250ms | 400ms | 95% < 250ms |

**SLA Commitment:** 95% of requests complete within P95 time

---

### Caching Strategy

| Endpoint | Cache Duration | Cache Key | Invalidation |
|----------|----------------|-----------|--------------|
| 4868003032989696.js (Config) | 5 minutes | `project:{projectId}:v{revision}` | On publish |
| preview_lay_data.js (Preview) | 1 minute | `preview:{experimentId}` | On variation change |
| geo4.js (Geolocation) | 1 hour | `geo:global` | On IP change |
| Event POST (Tracking) | No cache | — | N/A (always fresh) |
| 5129813690679290 (State) | 2 minutes | `state:{experimentId}:v{revision}` | On status change |

**Cache Invalidation Rules:**
- On publish: Clear all project caches
- On variation edit: Clear preview caches
- On status change: Clear state caches
- On user IP change: Clear geo caches

**Browser Cache Headers:**
```
Config (cacheable):
  Cache-Control: max-age=300, public
  ETag: "{hash}"

Events (non-cacheable):
  Cache-Control: no-store, no-cache, must-revalidate
```

---

## Related Documentation

- **[FULL_FLOW_SPEC.md](./FULL_FLOW_SPEC.md)** — Complete end-to-end testing flow with verification steps
- **[CLAUDE.md Section 1](./CLAUDE.md)** — Architecture and data flow diagrams
- **[CLAUDE.md Section 2](./CLAUDE.md)** — Core logic and business rules
- **[API.md](./API.md)** — Raw API data extracted from Excel

---

## Summary

This API reference covers all 12 endpoints used in the Visual Editor testing flow:

- **Phase 1 (Preview):** 3 GET requests for config, preview data, and geolocation
- **Phase 2 (Publish):** 6 requests including commit, events, live push, and state fetch
- **Phase 3 (Live):** 3 requests for config loading and event tracking

Each endpoint includes:
- Purpose and trigger conditions
- Request/response payloads
- Verification points
- Expected status codes
- Error handling guidelines

For complete testing instructions, see **FULL_FLOW_SPEC.md**.

---

**Last Updated:** 2026-03-16
**Maintained By:** QA & Engineering Team
**Version:** 1.0
**Status:** Active
