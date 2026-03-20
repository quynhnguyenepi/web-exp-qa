---
description: Product domain knowledge for Optimizely Performance Edge and Edge Delivery SDK. Use when answering questions about Edge experiments, edge decider, micro-snippet, CDN proxy, edge vs web differences, edge JavaScript API, Edge Delivery SDK (Cloudflare Workers), edge-specific testing, change history, or permissions. Helps QA engineers write tests with accurate product understanding.
---

## Dependencies

- **MCP Servers (optional):** `optimizely-prod` - Query real experiment data from Optimizely platform
  - `exp_get_schemas` - Get entity schemas (experiment, page, audience)
  - `exp_execute_query` - Query real experiments in web projects (Edge experiments are web experiments with edge-specific settings)

**Rule:** Always call `exp_get_schemas` before `exp_execute_query`. Edge experiments are stored as regular experiments in web projects -- filter by edge-related fields.

### Source Repositories
- **Documentation repo:** `edge-docs` repository at `docs/` directory (user-facing product documentation)
- **Dev repos:**
  - `edge-delivery` — Edge Delivery SDK (TypeScript/Cloudflare Workers, npm `@optimizely/edge-delivery`)
  - `optimizely` — Monolith frontend (Edge experiment UI, project settings for Edge)

## Role

You are an Optimizely Performance Edge and Edge Delivery domain expert. You help QA engineers understand how Performance Edge works, what features it supports (and does not support), how it differs from Web Experimentation, how the Edge Delivery SDK works with Cloudflare Workers, and how to properly test Edge experiments.

**Full reference:** See reference.md for SDK configuration options, version history, full compatibility matrices, implementation details, JavaScript API examples, and troubleshooting guide.

## Product Overview

Performance Edge is a faster way to deliver client-side web experiments using a distributed CDN network. It improves performance by moving targeting and variation assignment out of the browser onto CDN edge servers. Uses a lightweight "microsnippet" instead of a full snippet.

## How It Works

Three components work together:

### 1. Edge Decider
Receives request from CDN -> fetches experiment config -> evaluates pages/experiments -> buckets visitor -> returns microsnippet.

API endpoint: `https://optimizely-edge.com/edge-client/v1/<accountId>/<projectId>` (HTTPS only, requires `Referer` header)

### 2. Microsnippet
Tailor-made JavaScript for each visitor/page. Synchronous phase: initializes APIs -> runs Project JS -> applies changes (experiment shared code runs before variation code).

### 3. Tracking Snippet
Sends events to Optimizely. No public JavaScript API.

## Edge Delivery SDK

npm package `@optimizely/edge-delivery` for Cloudflare Workers. Main method: `applyExperiments(request, ctx, options)`.

Key options: `snippetId` (required), `environment` (dev/prod), `kvNamespace` (Cloudflare KV), `logLevel`, `fixCSPForOptimizely`.

## Edge vs Web Experimentation

**Critical rule:** Cannot run Edge and Web experiments on the same page simultaneously.

### Supported Experiment Types
- A/B Tests: Yes
- Multi-page (funnel): Yes
- Multiple variation (A/B/n): Yes
- Mutually exclusive: Yes
- MVT, Stats Accelerator, MAB: **No**

### Supported Page Triggers
- Immediately, Manually, URL Change, DOM Change: Yes
- Polling, Callback: **No (incompatible)**

### Key Unsupported Audience Conditions
Referrer URL, Custom JavaScript, Traffic source, Language, Ad campaign, New/returning, Time of day, Custom attributes, Platform/OS: **No**

### Not Supported
Personalization campaigns, adaptive audiences, DCP, PCI snippet, preview mode (force variation works), analytics integrations

## Edge JavaScript API

Uses `window.optimizelyEdge` (NOT `window.optimizely`).

Key methods:
- `window.optimizelyEdge.get('state').getActiveExperiments()`
- `window.optimizelyEdge.get('state').getActivePages()`
- `window.optimizelyEdge.push({ type: "event", eventName: "..." })`
- Utils: only `observeSelector` available (reduced set vs Web)

## Dynamic Website / SPA Support

Enable "Support for Dynamic Websites" in project settings. Additional triggers: URL Change, DOM Change. Page deactivation supported. **Custom JavaScript cannot be reverted** on deactivation.

## Change History & Permissions

Same services as Web Experimentation. Edge entities tracked: experiment, audience, page, event, project. Same permission model (admin > publish > toggle > edit > view > none).

## Key Business Rules

1. **No Edge + Web on same page** simultaneously
2. **No cross-product mutual exclusivity**
3. **No sticky bucketing on traffic changes**
4. **Hashes (#) ignored** in URL targeting
5. **HTTPS only**
6. **Force parameters require published experiments** and must be enabled
7. **Do not use `optimizely_` prefix** for test query parameters
8. **Custom JavaScript cannot be reverted** on page deactivation
9. **`async` attribute must NOT be on Edge script tag**
10. **`referrerpolicy="no-referrer-when-downgrade"` required**

## Common Test Scenarios

1. Verify Edge experiment runs via `getActiveExperiments()`
2. Force specific variation with `?optimizely_x=<variationId>`
3. Test audience targeting (cookies, browser, device, IP, location, query params)
4. Test redirect experiments and `getRedirectInfo()`
5. Test custom event tracking via `window.optimizelyEdge.push()`
6. Test opt-out and disable behavior
7. Verify SPA support with URL/DOM change triggers
8. Verify flashing behavior across trigger/condition combinations
9. Verify cookie persistence
10. Test logging with `?optimizely_log=info`
11. Test bucketing consistency (same user = same variation)
12. Verify edge-applied changes (DOM, CSS, links, redirects) vs deferred browser changes
13. Verify entity-level permissions on Edge experiments
