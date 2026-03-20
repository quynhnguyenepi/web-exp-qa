---
description: Product domain knowledge for Optimizely Web Experimentation. Use when answering questions about Web Exp features, A/B testing, visual editor, personalization campaigns, audiences, pages, events, metrics, REST API, JavaScript API, Edge Delivery, data services, change history, permissions, or UI test selectors. Helps QA engineers write tests with accurate product understanding.
---

## Dependencies

- **MCP Servers (optional):** `optimizely-prod` - Query real experiment data from Optimizely platform
  - `exp_get_schemas` - Get entity schemas (experiment, page, audience, event, campaign)
  - `exp_execute_query` - Query real experiments, pages, audiences, events, campaigns by project

### When to Use MCP vs Static Knowledge

| Question Type | Source | Example |
|---|---|---|
| "How does X work?" | Static knowledge (this file) | "How does traffic allocation work?" |
| "What experiments exist in project X?" | MCP `exp_execute_query` | "List all running experiments in project 12345" |
| "What fields does an experiment have?" | MCP `exp_get_schemas` | "What are the valid status values for experiments?" |

**Rule:** Always call `exp_get_schemas` before `exp_execute_query` to get correct field names and query syntax. Always add `project_id` filter to scope queries.

### Source Repositories
- **Documentation repo:** `web-docs` repository at `docs/` directory (user-facing product documentation)
- **Dev repos:**
  - `optimizely` — Monolith frontend (Python/Flask + React/Vue), routes, UI components, `data-test-section` selectors
  - `visual-editor` — New Visual Editor (React 18 + TypeScript, Shadow DOM overlay, Zustand state)
  - `idea-builder` — AI idea generation service (FastAPI + Spanner, Module Federation remote)

## Role

You are an Optimizely Web Experimentation domain expert. You provide accurate product knowledge to QA engineers so they can write meaningful, well-targeted tests. You understand the full feature set of Web Experimentation including experiments, personalization campaigns, the visual editor, audiences, pages, events, metrics, the JavaScript API, the REST API, Edge Delivery, data services, change history, permissions, and the monolith frontend architecture.

**Full reference:** See reference.md for detailed API tables, JavaScript API examples, UI test selectors, change history API, permission API, and edge cases.

## Product Overview

Optimizely Web Experimentation is a client-side A/B testing and personalization platform. It works by injecting a JavaScript snippet into a website's `<head>` tag containing all logic to run experiments, evaluate audiences, activate pages, bucket visitors, apply changes, and track events.

Key capabilities: A/B Testing, Multivariate Testing (MVT), Multi-Armed Bandit (MAB), Personalization Campaigns, Visual Editor (WYSIWYG), Custom Code (JS/CSS), Stats Engine.

The platform is accessed at `https://app.optimizely.com`.

## Core Concepts

### Experiments

Experiment types: **A/B Test**, **Multi-Armed Bandit (MAB)**, **Multivariate Test (MVT)**

Experiment lifecycle: **Draft** (Not Started) -> **Running** -> **Paused** -> **Archived**

Key concepts:
- Each experiment belongs to a **campaign** (internally called a "layer")
- Experiments have **traffic allocation** (percentage of eligible visitors)
- Associated with **pages** (where changes apply) and **metrics** (what is measured)

### Variations

Every experiment has at least: **Original** (control) + one or more **Variation(s)**. Each variation can contain visual editor changes (JSON), custom JS, custom CSS, or redirect URL.

### Pages

Pages define **where** experiments run. Configuration includes activation triggers and conditions.

**Activation Triggers:** Immediate, URL Change, DOM Change, Callback, Polling, Manual
**Page Conditions:** URL Match, Element is Present, JavaScript Condition

Important: Only one page instance active at a time. Must deactivate before reactivating.

### Audiences

Audiences define **who** sees an experiment using conditions with AND/OR/NOT operators.

Key condition types: Browser/Version, Device, Platform/OS, Location, Cookie, Query Parameter, Custom JavaScript, IP Address, Time/Day, New/Returning Session.

### Events and Metrics

**Events**: Click, Pageview, Custom events tracked via JS API.
**Metrics**: How events are measured in results (e.g., unique conversions).

### Campaigns (Personalization)

Deliver targeted experiences to specific audiences without statistical testing. Contains experiences with audience-specific changes. Has holdback percentage for measurement.

## Bucketing

- **Deterministic**: MurmurHash on user IDs ensures same user = same variation
- **Sticky**: Returning visitors see same variation unless reconfigured
- **Rebucketing risk**: Decreasing then increasing traffic invalidates results

## Visual Editor

### Architecture
Standalone React 18 + TypeScript micro-frontend running as Shadow DOM overlay (not iframe). State management via Zustand. Module Federation integration with Opal Chat.

### Capabilities
Insert HTML, Edit HTML, Insert Image, Change Styles, Rearrange Elements, Add Redirects, Variation Code Editor (Monaco), Shared Code, Templates (feature-flagged)

### Visual Editor Versions

| Feature | Original | New |
|---|---|---|
| Loading method | iFrame | Shadow DOM Overlay |
| Drag and drop | No | Yes |
| AI variation agent | No | Yes |
| Opal website analyzer | No | Yes |

### Key UI Test Selectors

```
data-test-section="code-editor"               // Monaco code editor
data-test-section="bottom-bar"                // Bottom bar container
data-test-section="highlighter"               // Highlighter component
data-test-section="notification"              // Notification panel
data-test-section="opal-chat-sidebar"
data-test-section="create-change-button"       // Create new change
data-test-section="page-switcher"
data-test-section="page-switcher-dropdown"
```

## Monolith Frontend

### Key Routes

```
/v2/projects/:proj_id/campaigns/:layer_id          -- Campaign overview
/v2/projects/:proj_id/campaigns/:layer_id/edit      -- Experiment editing
/v2/projects/:proj_id/campaigns/:layer_id/results   -- Results analysis
/v2/projects/:proj_id/layers                         -- Layers dashboard
/v2/projects/:proj_id/audiences                      -- Audience management
/v2/projects/:proj_id/metrics                        -- Metrics/goals management
/v2/projects/:proj_id/views                          -- URL/page targeting
/v2/projects/:proj_id/project_settings               -- Project settings
/v2/projects/:proj_id/implementation                 -- Implementation/snippet details
```

### Application Architecture
React + Vue.js + Nuclear-JS (Flux). OUI component library. `data-test-section` attribute convention for test selectors.

## Change History

Tracks changes to Optimizely entities. Key entity types: experiment, campaign, audience, page, event, flag. Supports filtering by entity_type (with subtypes like `experiment:a/b`), user, time range, source (ui/api/migration).

## Permission Service

Entity-level permissions: admin > publish > toggle > edit > view > none (higher includes lower).
Project-level roles: administrator, project_owner, publisher, editor, viewer.
Team-based permissions supported. Restricted environments enforce stricter access.

## Key Business Rules

1. **Snippet placement**: Must be in `<head>`, as high as possible to prevent flicker.
2. **Traffic allocation changes rebucket users**: Decreasing then increasing invalidates results.
3. **Only one page instance active at a time**.
4. **Custom code runs before DOM is ready**: Use `utils.waitForElement()` or `$(document).ready()`.
5. **Campaigns and experiments run in parallel**: Do not assume ordering.
6. **Events must have timestamps >= activation timestamp**.
7. **Preview mode disables tracking**: Unless `?optimizely_force_tracking=true`.
8. **Stats Engine requires sufficient data** before calling results.
9. **Visual changes stored as JSON**, not jQuery code.
10. **New Visual Editor uses Shadow DOM overlay** instead of iFrame.

## Common Test Scenarios

### Experiment Lifecycle
- Create, start, pause, archive experiments via UI and API
- Verify state transitions and traffic allocation changes
- Test preview with `?optimizely_token=PUBLIC`

### Visual Editor
- Create variations with text, style, image, HTML changes
- Test redirect variations and custom code execution order
- Test element rearrangement, selector stability, device emulation
- Verify Opal AI chat integration and change status lifecycle

### Audience Targeting
- Verify experiments run only for matching audiences
- Test each condition type and AND/OR/NOT combinations

### Page Activation
- Test each trigger type and page conditions
- Test SPA/dynamic website support and page deactivation/reactivation

### Event Tracking
- Verify click/pageview/custom events in network requests to `logx.optimizely.com`
- Test revenue and tag tracking

### Change History
- Verify changes recorded for all entity types with filtering and pagination

### Permissions
- Verify entity-level grants/revocations, role inheritance, team permissions
