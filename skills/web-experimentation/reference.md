# Web Experimentation - Detailed Reference

**This file contains exhaustive tables, API details, examples, and edge cases. For core product knowledge, see SKILL.md.**

## Layer Model (Internal)

Internally, campaigns are called "layers". Layer types:
- `single_experiment`: A/B test
- `multivariate`: Multivariate test
- `ordered` / `equal_priority`: Personalization campaign
- `rollout`: Rollout

Layer policies control how traffic is distributed:
- `RANDOM`: Random bucketing (A/B testing)
- `ORDERED`: Sequential audience checking (personalization)
- `EQUAL_PRIORITY`: Equal distribution across audiences
- `MULTIVARIATE`: MVT distribution
- `SINGLE_EXPERIMENT`: Single experiment targeting
- `ROLLOUT`: Gradual traffic allocation

Layer status values: `NOT_STARTED`, `RUNNING`, `PAUSED`, `ARCHIVED`, `CONCLUDED`

Activation modes: `IMMEDIATE`, `MANUAL`, `CONDITIONAL`, `READY`, `TIMEOUT`

## Audience Condition Types (Full List)

- **Browser/Version** -- Target specific browsers (Chrome `gc`, Firefox `ff`, Safari, Edge, IE, Opera, UC Browser)
- **Device** -- Target device types (iPhone, iPad, mobile, tablet, desktop)
- **Platform/OS** -- Target operating systems (iOS, Android, Windows, macOS, Linux)
- **Location** -- Geo-target by country, state, city, DMA region (format: `US|CA|SANFRANCISCO`)
- **Language** -- Target by browser language setting
- **Cookie** -- Match cookie name/value with exact, substring, regex, or exists match types
- **Query Parameter** -- Match URL query parameters
- **Referrer URL** -- Match the referring URL
- **Traffic Source** -- Direct, Search, Referral, or Campaign
- **Ad Campaign** -- Match `utm_campaign` query parameter
- **Custom Attribute** -- Match custom attributes (Web supports string values with exact match only)
- **Custom Event** -- Match visitors who triggered a specific event
- **Custom JavaScript** -- Match when JavaScript code evaluates to truthy
- **Custom Tags** -- Match custom tag name/value pairs
- **Custom Dimension** -- Match dimension name/value
- **IP Address** -- Match visitor IP with exact, regex, CIDR, or prefix match
- **Time/Day of Visit** -- Target specific days and time ranges (format: `HH:MM_HH:MM_day1,day2,...`)
- **New/Returning Session** -- Target first-time or returning visitors

Condition JSON structure:
```json
["and", { "type": "browser_version", "value": "gc" }, { "type": "device", "value": "desktop" }]
["or", { "type": "location", "value": "US" }, { "type": "location", "value": "CA" }]
["not", { "type": "browser_version", "value": "ie" }]
```

## Event Tracking Details

Custom events are tracked by pushing to the Optimizely API:
```javascript
window.optimizely = window.optimizely || [];
window.optimizely.push({
  type: "event",
  eventName: "my_custom_event"
});
```

Events can include **tags** for additional metadata:
```javascript
window.optimizely.push({
  type: "event",
  eventName: "purchase",
  tags: {
    revenue: 9900,  // Revenue in cents
    category: "Electronics"
  }
});
```

Event tracking endpoints:
- Modern snippets use `POST` to `https://logx.optimizely.com/v1/events` (batched events)
- Older snippets use individual `GET` requests to the `/event` endpoint

## Campaigns (Personalization) Internal Model

Terminology mapping (UI vs internal):
- Campaign = Layer
- Experience = Experiment (with a single Variation)
- Experience changes = Actions (a set of changes for a specific page)

Important: Personalization campaigns and A/B experiments can execute in parallel. Be careful about dependencies between them or optimizing the same element in multiple campaigns/experiments.

## Visual Editor Change Types (Internal Model)

```
ATTRIBUTE      -- Modify element properties (class, style, text, html, src, srcset, href, hide, remove)
CUSTOM_CSS     -- Inject custom CSS rules targeting selector
CUSTOM_CODE    -- Execute JavaScript code in experiment context
INSERT_HTML    -- Insert HTML before/after/prepend/append to target element
INSERT_IMAGE   -- Upload and insert image with positioning
WIDGET         -- Insert pre-built widget template from template library
REDIRECT       -- Redirect page to URL (with option to preserve query parameters)
```

## Visual Editor Change Status Lifecycle

```
INITIAL -> NEW -> DIRTY -> LIVE / MODIFIED / DRAFT / DELETED
```
- `INITIAL`: Before first save
- `NEW`: Saved, no live equivalent
- `DIRTY`: Currently being edited
- `LIVE`: Published, no draft
- `MODIFIED`: Published + draft exists
- `DRAFT`: UI simplification for NEW|MODIFIED
- `DELETED`: Marked for deletion on publish

## Change Application Order

Changes are applied synchronously in this order:
1. Project JavaScript
2. Campaign JavaScript
3. Campaign CSS
4. Experience/Experiment JavaScript
5. Experience/Experiment CSS
6. Visual editor changes

Within VE changes: CUSTOM_CODE -> CUSTOM_CSS -> REDIRECT -> rest

## Selector Generation (Selectorator)

The editor generates CSS selectors using a powerset algorithm:
- Tries combinations of (tag, ID, classes, attributes) up to 6 facets
- Finds shortest unique CSS selector
- Filters invalid selectors (Optimizely internal: `/^[#.]optimizely-/`, `/^[#.optly-/`)
- Detects CSS-in-JS hash-like classes (prefixes: `sc-`, `css-`, `jsx-`, `emotion-`, `styled-`, `svelte-`, `makeStyles-`, `jss`, `astro-`, `stitches-`, `linaria-`)
- Tests selector equivalence across page reloads

Blacklisted tags (cannot be edited): `HEAD`, `HTML`, `LINK`, `META`, `SCRIPT`, `STYLE`, `TITLE`, `OPTLYOVERLAY`

## Visual Editor Feature Flags

```
use_opal                    -- Enable Opal AI chat in editor
conditional_activation      -- Advanced targeting conditions UI
element_action_menu         -- Context menu on element selection
enabled_templates           -- Widget templates library
freeze_site_on_highlight    -- Freeze hover states during element inspection
```

## Visual Editor State Stores (Zustand)

| Store | Purpose | Key State |
|---|---|---|
| useChangeStore | All change management | changes[], currentlyEditingChange, pendingChangeStatus |
| useExperimentStore | Experiment metadata | experiment, variationIndex, viewIndex, isSaving |
| useSelectorStore | Element selection | selector, positions, isInteractive |
| useHighlighterStore | Hover overlay | selector, positions |
| useAuthStore | Authentication | oauthToken, optiIdToken, isLoggedOut |
| useOpalChatStore | AI assistant | isVisible, threads, selectorThreadMap, dockState |
| useNotificationStore | Toast notifications | notifications[] (max 3, auto-dismiss 10s) |
| useViewStore | Pages/views | views[], currentViewIndex |
| useEventStore | Click events | events[], isLoading |

## Visual Editor API Integration

```
GET  /api/v1/layer_experiments/{experimentId}                          // Fetch experiment
PUT  /api/v1/layer_experiments/{experimentId}/variations/{variationId}/views/{viewId}  // Save changes
GET  /api/v1/projects/{projectId}/events                               // Fetch events
POST /api/v1/projects/{projectId}/events                               // Create event
POST /api/v1/projects/{projectId}/files/upload                         // Upload image
```

## Visual Editor Query Parameters

```
optimizely_project_id          // Project ID
optimizely_experiment_id       // Layer Experiment ID
optimizely_section_id          // Section ID (personalization/MVT)
optimizely_variation_id        // Variation ID
optimizely_page_id             // Specific view ID
optimizely_embed_editor=true   // Enable editor mode
optimizely_use_shadow_dom      // Force shadow DOM
optimizely_device_mode         // Device emulation mode
optimizely_events_mode         // Events editor mode
```

## Device Emulation Breakpoints

| Name | Width |
|---|---|
| XS | 320px (Mobile) |
| SM | 430px (Larger mobile) |
| MD | 744px (Tablet) |
| LG | 834px (Large tablet) |
| XL | 1280px (Desktop) |
| 2XL | 1440px (Large desktop) |
| 3XL | 1920px (Extra large desktop) |

## Visual Editor LLM Tools Bridge

The editor exposes tools for AI-assisted editing via WebSocket:
- `elementRead`, `elementTree`, `elementGlob`, `elementGrep`
- `applyChange`, `revertChange`, `listPendingChanges`
- `getSelector`, `getChangeSchema`, `validateChange`

## Timing Considerations for Custom Code

Custom code runs immediately, often before DOM is ready. To delay execution:

```javascript
// Wait for DOM ready (may cause flashing)
$(document).ready(function() { /* code */ });

// Wait for specific element (no flash) - PREFERRED
var utils = window.optimizely.get('utils');
utils.waitForElement('body').then(function() { /* code */ });

// Use CSS for styling changes (no timing issues)
// CSS changes append a <style> tag to <head>
```

## JavaScript API (Full Reference)

### GET API

Access data after Optimizely has initialized (not available in Project JavaScript):

```javascript
window["optimizely"].get('data');     // Get all saved project data
window["optimizely"].get('visitor');  // Get current visitor information
window["optimizely"].get('state');    // Get current state of campaigns/experiments
window.optimizely.get('jquery');      // Get jQuery instance
window.optimizely.get('utils');       // Get utility functions
```

### PUSH API

Push events and commands:

```javascript
window.optimizely = window.optimizely || [];
window.optimizely.push({ type: "event", eventName: "my_event" });
window.optimizely.push({ type: "event", eventName: "purchase", tags: { revenue: 9900 } });
window.optimizely.push({ type: "page", pageName: "checkout_stage_1" });
window.optimizely.push({ type: "page", pageName: "checkout_stage_1", isActive: false });
window.optimizely.push({ type: "disable" });
```

### State API

```javascript
var activeCampaigns = optimizely.get('state').getCampaignStates({ isActive: true });
var decision = optimizely.get('state').getDecisionObject({ campaignId: campaignId });
var pages = optimizely.get('state').getPageStates();
```

### Utility Functions

```javascript
var utils = window.optimizely.get('utils');
utils.waitForElement('button').then(function(element) { /* element is ready */ });
var cancelPolling = utils.poll(function() { /* check condition */ }, 1000);
```

### Query Parameters

| Parameter | Purpose |
|---|---|
| `?optimizely_disable=true` | Disable Optimizely on the page |
| `?optimizely_x={{variation_ids}}` | Force specific variations (comma-separated). Disables tracking. |
| `?optimizely_x_audiences={{audience_ids}}` | Impersonate audiences (comma-separated) |
| `?optimizely_opt_out=true` | Remove visitor from tracking (persists via cookie) |
| `?optimizely_force_tracking=true` | Send tracking events even in preview mode |
| `?optimizely_log=info` | Enable console logging (OFF, ERROR, WARN, INFO, DEBUG, ALL) |
| `?optimizely_token=PUBLIC` | View draft or paused experiments for QA |

## REST API (Full Reference)

### Authentication

Two methods:
1. **Personal Tokens** -- For internal tools and exploration. Generated at `app.optimizely.com/v2/profile/api`. Server-to-server only, never share.
2. **OAuth 2.0** -- For customer-facing applications.

```
Authorization: Bearer {token}
```

### Base URL

```
https://api.optimizely.com/v2/
```

### Key Endpoints

| Resource | List | Get | Create | Update | Delete |
|---|---|---|---|---|---|
| Projects | `GET /projects` | `GET /projects/{id}` | `POST /projects` | `PATCH /projects/{id}` | `DELETE /projects/{id}` |
| Experiments | `GET /experiments` | `GET /experiments/{id}` | `POST /experiments` | `PATCH /experiments/{id}` | `DELETE /experiments/{id}` |
| Campaigns | `GET /campaigns` | `GET /campaigns/{id}` | `POST /campaigns` | `PATCH /campaigns/{id}` | -- |
| Pages | `GET /pages` | `GET /pages/{id}` | `POST /pages` | `PATCH /pages/{id}` | `DELETE /pages/{id}` |
| Events | `GET /events` | `GET /events/{id}` | `POST /events` | `PATCH /events/{id}` | `DELETE /events/{id}` |
| Audiences | `GET /audiences` | `GET /audiences/{id}` | `POST /audiences` | `PATCH /audiences/{id}` | -- |
| Results | `GET /experiments/{id}/results` | -- | -- | -- | -- |

### API Conventions

- **Pagination**: Default 25 items per page, max 100. Use `?page=N&per_page=M`.
- **Rate Limiting**: Headers `X-RATELIMIT-LIMIT`, `X-RATELIMIT-REMAINING`, `X-RATELIMIT-RESET`. 429 on limit exceeded.
- **Errors**: 4xx includes `message`, `uuid`, `code` fields.

## Monolith Frontend UI Test Selectors

### Campaign Overview
```
campaign-overview-experiments-create
campaign-overview-experiments-experiment-list
campaign-overview-prioritize-experiences
campaign-overview-settings-holdback-input
campaign-overview-settings-holdback-error
campaign-overview-settings-holdback-warning
campaign-overview-sidebar-campaign-start
campaign-overview-settings-save
experiment-panel-add-variation-link
experiment-panel-add-variation-input-save
experiment-card-priority-group-index
experiment-card-dropdown
experiment-card-menu-unarchive
variation-table-row-link
variation-table-row-edit-holdback
variation-running-status-indicator
variation-unpublished-changes-status-indicator
campaign-custom-code
name-input
```

### Layers Dashboard
```
layer-table-row-name
layer-table-row-status
layer-table-row-type
layer-table-row-modified
layer-table-row-description
layer-table-row-results
layer-table-row-dropdown-{layer_id}
layer-table-row-dropdown-start
layer-table-row-dropdown-pause
layer-table-row-dropdown-archive
layer-table-row-dropdown-duplicate
layer-table-row-dropdown-unarchive
layers-create-new-dropdown
layers-create-new-experiment
layers-create-new-mvt
layers-create-button
toggle-field
tabs-menu
empty-state
```

### Audiences
```
tabs-menu
audience-dashboard-tab
attributes-dashboard-tab
external-attribute-menu-open-button-{id}
create-attribute-dropdown
list-attribute-menu-open-button-{id}
attributes-datasource-card
attribute-dashboard-empty-state
custom-attributes-table
custom-attributes-card
create-custom-attribute-button
list-attributes-table
```

### Experiment Editor
```
audience-search-picker-input
audience-search-picker-audience-add-button
save-experiment-button
select-traffic-allocation-policy-dropdown
user-attributes-section
variation-menu-delete-{variation_id}
```

## Change History Service (Full API)

### Service URLs

| Environment | URL |
|---|---|
| Integration | `https://inte.change-history.optimizely.com` |
| RC | `https://prep.change-history.optimizely.com` |
| Production | `https://change-history.optimizely.com` |

### API Endpoints

**POST /v1/changes** -- List changes (preferred)
```json
{
  "project_id": 12345,
  "account_id": 54321,
  "page": 1,
  "per_page": 25,
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-31T23:59:59Z",
  "user": ["user@company.com"],
  "entity_type": ["experiment", "experiment:a/b", "campaign"],
  "entities": [{"type": "experiment", "id": 123}],
  "user_showable": true,
  "source": "ui"
}
```

### Supported Entity Types

`attribute`, `audience`, `campaign`, `custom_field`, `environment`, `event`, `experiment` (with subtypes: `a/b`, `multivariate`, `multiarmed_bandit`, `personalization`), `extension`, `feature`, `flag`, `group`, `list_attribute`, `metric`, `metric_set`, `page`, `project`, `rule`, `ruleset`, `section`, `tag`, `variable`, `variation`, `permission`, `team`, `report`

### Change Types

`create`, `update`, `delete`, `archive`, `unarchive`, `publish`, `migration`

### Key Business Rules

- `start_time` is inclusive (>=), `end_time` is exclusive (<)
- Entity type supports subtypes: `experiment:a/b`
- Source filter: `ui`, `api`, `migration`
- `user_showable`: hides system changes when true
- Pagination: default 25, max 101. Total in `X-Record-Total` header
- Non-personalization campaigns are filtered out (only `personalization` type tracked)
- `publish` change type has no diff (always shown without change details)

### UI URL Patterns for Entities

| Entity Type | UI URL |
|---|---|
| experiment (a/b) | `/v2/projects/{project_id}/experiments/{entity_id}` |
| experiment (multivariate) | `/v2/projects/{project_id}/multivariate/{entity_id}` |
| experiment (personalization) | `/v2/projects/{project_id}/campaigns/{campaign_id}` |
| audience | `/v2/projects/{project_id}/audiences` |
| page | `/v2/projects/{project_id}/implementation/pages/{entity_id}` |
| event | `/v2/projects/{project_id}/implementation/events` |
| flag | `/v2/projects/{project_id}/flags/manage/{flag_key}` |

## Permission Service (Full API)

### Permission Levels (Entity-Level)

| Level | Hierarchy | Description |
|---|---|---|
| admin | 5 (highest) | Full control including managing permissions |
| publish | 4 | Can publish changes to live entities |
| toggle | 3 | Can enable/disable entities |
| edit | 2 | Can modify entity settings |
| view | 1 | Can read/view entity details |
| none | 0 (lowest) | No permission (access denied) |

Higher permission includes all capabilities of lower permissions.

### Project-Level Roles (Inherited)

| Role | Default Permission |
|---|---|
| administrator | admin (all entities) |
| project_owner | admin |
| publisher | publish (env/flag) / edit (audience) |
| editor | edit |
| viewer | view |

### Key Permission API Endpoints

```
GET    /projects/{project_id}/{entity_type}/{entity_id}/users   -- Users with permissions on entity
GET    /projects/{project_id}/{entity_type}/{entity_id}/teams   -- Teams with permissions on entity
PATCH  /projects/{project_id}/{entity_type}/{entity_id}         -- Change permissions (requires admin)
```

PATCH operations:
- `replace`: `/users/{user_id}/role` or `/teams/{team_id}/role` with value
- `remove`: `/users/{user_id}/role` or `/teams/{team_id}/role`

### Team Management

```
GET    /accounts/{account_id}/teams              -- List teams
POST   /accounts/{account_id}/teams              -- Create team (requires account admin)
PATCH  /accounts/{account_id}/teams/{team_id}    -- Update team
DELETE /accounts/{account_id}/teams/{team_id}    -- Delete team (cascades permissions)
```

### Key Business Rules

- Environment permissions: restricted environments limit publisher role to edit
- Audience permissions are context-dependent (determined by flag/environment using the audience)
- Team names must be unique per account
- Team deletion cascades to all team permission records
- Default team role for environments: "view", for other entities: "none"
- Invited users (status="INVITED") are excluded from team membership

## Edge Delivery (Full Reference)

### How It Works

- Experiments are applied server-side at the CDN edge before the page reaches the browser
- Uses the same experiment configuration as Web Experimentation (same snippet ID)
- Changes that cannot be applied at the edge are packaged and added to `<head>` for browser execution
- The Edge Delivery SDK is installed via npm: `@optimizely/edge-delivery`

### Key Concepts

- **Snippet ID** -- The same ID used for the Web Experimentation snippet
- **Control** -- The original response from the origin server
- **applyExperiments** -- The main SDK method that evaluates bucketing decisions and applies variations

```javascript
import { applyExperiments } from '@optimizely/edge-delivery';
await applyExperiments(request, ctx, options);
```

### Prerequisites

- Cloudflare account with Workers enabled
- Website routed through Cloudflare
- Optimizely Web Experimentation account with experiments configured
- Wrangler CLI installed

## Event API (Full Reference)

### Endpoint

```
POST https://logx.optimizely.com/v1/events
Content-Type: application/json
```

No authorization token is required. Returns `204` on success. Max `10 MB` per JSON object.

## Data Services

### Dynamic Customer Profiles (DCP)

DCP stores customer attributes for audience targeting and analysis. Uses v1 API with classic tokens.

### Enriched Events Export

Provides access to experiment event data via Amazon S3. Data is deduplicated and enriched before export. Available within one day of receipt.

## Reference Links

- **Documentation source**: `web-docs` repository at `docs/` directory
- **Live docs**: https://docs.developers.optimizely.com/web-experimentation
- **API reference**: https://docs.developers.optimizely.com/web-experimentation/reference/overview
- **Swagger/OpenAPI spec**: https://api.optimizely.com/v2/swagger.json
- **Application URL**: https://app.optimizely.com
- **Edge Delivery SDK**: https://www.npmjs.com/package/@optimizely/edge-delivery
- **Visual Editor repo**: `optimizely/visual-editor`
- **Monolith repo**: `optimizely/optimizely`
- **Idea Builder repo**: `optimizely/idea-builder`
