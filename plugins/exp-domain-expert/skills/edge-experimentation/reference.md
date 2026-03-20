# Edge Experimentation - Detailed Reference

**This file contains exhaustive compatibility tables, SDK version history, implementation details, and full API examples. For core product knowledge, see SKILL.md.**

## Edge Delivery SDK Full Configuration

```typescript
import { applyExperiments, Options } from '@optimizely/edge-delivery';

const options: Options = {
  snippetId: "29061560280",           // Required: Optimizely project snippet ID
  environment: "prod",                // "dev" | "prod"
  dev_host: "https://example.com/",   // Target website URL (dev only)
  devUrl: "https://example.com/",     // Alternative to dev_host
  control: controlResponse,           // Optional: pre-fetched Response
  kvNamespace: kvNamespace,           // Optional: Cloudflare KV for config
  logLevel: "debug",                  // "debug" | "info" | "warn" | "error" (v1.0.6+)
  fixCSPForOptimizely: true           // Beta: CSP auto-fix (v1.0.6+)
};

return await applyExperiments(request, ctx, options);
```

## SDK Execution Flow (Detailed)

1. **Fetch Configuration**: Retrieve manifest from CDN (using snippetId) or KV store
2. **Parse Request**: Extract visitor info (cookies, user agent, referrer, IP)
3. **Evaluate Audiences**: Match visitor against targeting rules
4. **Bucketing Decisions**: Assign variation based on visitor ID, audience, traffic allocation
5. **Apply Edge Changes**: DOM/CSS/link changes executable at edge
6. **Defer Browser Changes**: Package non-edge-executable changes (custom JS, layer code)
7. **Inject Head Script**: Inject activation script into `<head>` for browser-side execution
8. **Return Response**: Return modified HTML

## Edge vs Browser Change Execution

| Change Type | Edge? | Browser? | Notes |
|---|---|---|---|
| HTML/DOM mutations | Yes | Limited | Inline changes at edge |
| CSS/style changes | Yes | Limited | Inline styles at edge |
| Link href/src/srcset | Yes | -- | Applied at edge (v1.0.3+) |
| Redirects | Yes | -- | 302 redirects at edge (v1.0.1+) |
| Custom JavaScript | No | Yes | Deferred, injected in `<head>` |
| Layer custom code | No | Yes | Fixed in v1.0.4+ |
| Analytics tracking | Yes/No | Yes | ODP queries at edge, event tracking in browser |

## Cloudflare Worker Configuration

```toml
# wrangler.toml
name = "edge-delivery-starter"
main = "src/index.ts"
compatibility_flags = ["nodejs_compat"]

[env.dev.vars]
SNIPPET_ID = "29061560280"
environment = 'dev'
dev_host = 'example.com'

[env.prod.vars]
environment = 'prod'
SNIPPET_ID = "your-snippet-id"

[[kv_namespaces]]
binding = "EDGE_DELIVERY_CONFIGS"
id = "your-kv-namespace-id"
```

## SDK Version History

| Version | Key Features | Notable Fixes |
|---|---|---|
| 1.0.6 | `logLevel` option, CSP autocompletion (beta), jQuery loading | KV webhook updates |
| 1.0.5 | CSP nonce extraction | User agent blockage removed, cookie updates, redirect filtering |
| 1.0.4 | CMAB monitoring | Layer custom code, Visual Editor links, ShadowDOM |
| 1.0.3 | -- | IP audiences, GA4 tracking, srcset changes, event properties |
| 1.0.2 | New Visual Editor support | Cookie size reduction |
| 1.0.1 | -- | 302 redirects, nonce validation, DOM trigger dedup |

## Supported Audience Conditions (Full Matrix)

| Condition | Supported? |
|---|---|
| Cookie | Yes |
| Device | Yes |
| Browser/version | Yes |
| Query Parameter | Yes |
| IP Address | Yes |
| Location (geotargeting) | Yes |
| Referrer URL | **No** |
| Custom JavaScript | **No** |
| Traffic source | **No** |
| Language | **No** |
| Ad campaign | **No** |
| New vs. returning visitors | **No** |
| Time of day | **No** |
| Custom attributes | **No (incompatible)** |
| Platform/OS | **No** |

## Features Not Supported in Performance Edge

- Personalization campaigns
- Adaptive audiences/recommendations
- Dynamic customer profile
- PCI compliant snippet
- Preview mode (no preview widget, but force variation IDs work)
- Out-of-box one-click analytics integrations
- Multivariate testing (MVT)
- Stats Accelerator
- Multi-armed bandit
- Polling page trigger
- Callback page trigger

## Implementation Methods (Full Details)

### Method 1: Edge Subdomain (Recommended)

Add CNAME record aliasing subdomain to `cname.optimizely-edge.com`, then add script tag:
```html
<script src="https://optimizely.customer.com/edge-client/v1/<account_id>/<project_id>"
        referrerpolicy="no-referrer-when-downgrade"></script>
```

**Important:** `referrerpolicy` attribute required. Place at **top** of `<head>`. Do **not** include `async` attribute.

### Method 2: CDN Proxy

Supported CDNs: Akamai, Cloudflare, CloudFront (AWS), Fastly.

Must forward: `Accept-Encoding`, required cookies (`optimizelyEndUserId`, `optimizelyRedirectData`, `optimizelyDomainTestCookie`, `optimizelyOptOut`), `Referer`, `X-Forwarded-For` headers.

### Method 3: Backend Proxy (Not Recommended)

Poor performance due to lack of geographical proximity.

## Edge JavaScript API (Full Reference)

### State Module

```javascript
window.optimizelyEdge.get('state').getActiveExperiments()  // Active experiments with variation info
window.optimizelyEdge.get('state').getActivePages()         // Active pages
window.optimizelyEdge.get('state').getRedirectInfo()        // Redirect info from previous page
```

### Event Tracking

```javascript
window.optimizelyEdge.push({
  type: "event",
  eventName: "watchedVideo",
  tags: { title: "Funny Cats", duration: 30, revenue: 5000 }
});
```

### Listeners

```javascript
window.optimizelyEdge.push({
  type: "addListener",
  filter: { type: "lifecycle", name: "activated" },
  handler: function(event) { /* ... */ }
});
```

Available: `initialized`, `activated`, `campaignDecided`, `pageActivated`, `originsSynced`, `trackEvent`

### Utils Module

Only `observeSelector` available (reduced set vs Web):
```javascript
let unobserve = window.optimizelyEdge.get("utils").observeSelector("#cta", function(el) {
  el.innerText = "Click me!";
  unobserve();
});
```

### Cookie Management

```javascript
window.optimizelyEdge.push({ type: "cookieDomain", cookieDomain: "www.example.com" });
window.optimizelyEdge.push({ type: "cookieExpiration", cookieExpirationDays: 365 });
window.optimizelyEdge.push({ type: "optOut", isOptOut: true });
window.optimizelyEdge.push({ type: "holdEvents" });
window.optimizelyEdge.push({ type: "sendEvents" });
window.optimizelyEdge.push({ type: "log", level: "INFO" });
```

## Dynamic Website / SPA Support (Full Details)

Enable "Support for Dynamic Websites" in project settings.

**Additional triggers:** URL Change, DOM Change
**Additional conditions:** Element is Present, JavaScript Condition

**Flashing behavior:**
- No flashing: trigger=Immediately + condition=URL Match + rendering=Immediate Render
- "When DOM changes" + "Element is present" at Delayed Render = no flashing
- Most SPA trigger/condition combos may cause flashing

**Page deactivation:**
- Enable "Automatically deactivate this page when conditions are false"
- Option "Undo changes when page deactivates" reverts VE changes and CSS
- **Custom JavaScript cannot be reverted** on deactivation

## QA and Troubleshooting

### Preview Variations

```
?optimizely_x=VARIATIONID
```
- Only works on **published and running** experiments
- Force parameters must be enabled in project settings
- Find Variation ID: experiment > Manage Experiment > API Names

### Testing Approaches

1. `?optimizely_log=info` for detailed logs
2. `?optimizely_x=VARIATIONID` to force variations
3. URL targeting with test parameter (do NOT use `optimizely_` prefix)
4. Cookie audience condition for testing
5. `?optimizely_disable=true` to disable Edge

### Verifying Implementation

1. Load page with Edge script
2. Run `optimizelyEdge` in console (should be defined)
3. Confirm `optimizelyEndUserId` cookie persists across refreshes

### Common Errors

1. **"Target page URL is null"** -- `Referer` header not forwarded
2. **403 Forbidden** -- Wrong URL format or using Web project ID instead of Edge
3. **Cookie audience not qualifying** -- Cookies not forwarded to Edge Decider

## Edge Delivery SDK Test Scenarios (Detailed)

- Test bucketing consistency (same user = same variation)
- Test audience targeting at edge (URL, referrer, device, IP)
- Verify edge-applied changes (DOM, CSS, links, redirects)
- Test deferred browser changes (custom JS, layer code)
- Verify CSP nonce handling (v1.0.5+) and auto-fix (v1.0.6+)
- Test with/without KV namespace (CDN fallback)
- Test with pre-fetched control Response
- Test different logLevel values
- Verify cookie updates from origin response (v1.0.5+)

## Change History & Permissions for Edge

### Change History
Edge entities tracked: `experiment` (subtype varies), `audience`, `page`, `event`, `project`

Service URLs:
- Integration: `https://inte.change-history.optimizely.com`
- RC: `https://prep.change-history.optimizely.com`
- Production: `https://change-history.optimizely.com`

### Permissions
Same permission model as Web Experimentation:
- Entity-level permissions: admin, publish, toggle, edit, view, none
- Project-level roles inherited from monolith
- Team-based permissions supported
- Restricted environments enforce stricter access

## Reference Links

- **Documentation source**: `edge-docs` repository at `docs/` directory
- **Edge Delivery SDK repo**: `optimizely/edge-delivery`
- **Edge Delivery npm**: https://www.npmjs.com/package/@optimizely/edge-delivery
- **Performance Edge docs**: https://docs.developers.optimizely.com/experimentation/v50.0.0-performance-edge
- **Edge Decider API**: https://docs.developers.optimizely.com/experimentation/v50.0.0-performance-edge/reference
- **JavaScript API global**: `window.optimizelyEdge` (NOT `window.optimizely`)
- **Monolith repo**: `optimizely/optimizely`
