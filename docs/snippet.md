# Optimizely Snippet Reference Guide

> **Purpose**: Document Optimizely snippet JSON structure, change types, verification methodology, and test data patterns. This guide enables QA engineers to analyze tickets and generate test cases with deep understanding of snippet composition and live site verification.

**Last Updated**: 2026-03-16  
**Audience**: QA Engineers (web-analyze-ticket, web-create-test-cases skills)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Snippet JSON Structure](#2-snippet-json-structure)
3. [Key Verification Points](#3-key-verification-points)
4. [Change Types Reference](#4-change-types-reference)
5. [Test Data Examples](#5-test-data-examples)
6. [Common Debugging Patterns](#6-common-debugging-patterns)

---

## 1. Overview

### Test Snippet URL
```
https://cdn.optimizely.com/js/4868003032989696.js
```

### Key Project IDs (Test Environment)
- **Project ID**: `4868003032989696`
- **Namespace**: `4868003032989696`
- **Service ID (DCP)**: `28237450667`

### What is a Snippet?
A **snippet** is the compiled JavaScript configuration file served via Optimizely CDN. It contains:
- All active experiments/campaigns for a project
- Variations with changes (CSS, HTML, custom code)
- Event tracking configuration
- Saved pages/views with targeting rules
- Audience data (DCP integration)
- Visitor attributes and dimensions

### When to Check Snippet
Use snippet verification when:
1. ✅ Testing live site changes after publishing a variation
2. ✅ Debugging why changes are not appearing on customer website
3. ✅ Verifying traffic allocation and experiment distribution
4. ✅ Confirming event tracking configuration
5. ✅ Validating page/view URL targeting

---

## 2. Snippet JSON Structure

### 2.1 Root Properties

| Property | Type | Description |
|----------|------|-------------|
| `accountId` | string | Optimizely account identifier |
| `projectId` | string | Project ID (matches namespace) |
| `namespace` | string | Unique project namespace |
| `revision` | string | Snippet revision number - **increments on each publish** |
| `anonymizeIP` | boolean | Privacy setting - mask visitor IP addresses |
| `enableForceParameters` | boolean | Allow force variation via URL param |
| `experimental` | object | Beta features (e.g., `trimPages: true`) |

**Key Verification Point**: Revision should increment when experiment is published from Visual Editor.

### 2.2 Layers Array

Each **layer** represents a campaign (experiment group).

```javascript
"layers": [{
    "id": "5129813690679296",              // Layer unique ID
    "name": null,                           // Layer name (nullable)
    "commitId": "6699817645113344",         // Version commit
    "groupId": null,
    "holdback": 0,                          // Holdback % (0 = no holdback)
    "activation": {},                       // Activation rules (mostly empty)
    "integrationSettings": {},
    "integrationStringVersion": 2,
    "experiments": [...],                   // See 2.3
    "policy": "single_experiment",          // Campaign policy
    "viewIds": ["6524733806608384"],        // Page IDs in this layer
    "weightDistributions": null,            // Layer-level traffic distribution
    "decisionMetadata": null,
    "concluded": false                      // Layer status
}]
```

### 2.3 Experiments Array (inside Layers)

Each **experiment** contains variations and traffic allocation.

```javascript
"experiments": [{
    "id": "6255713597521920",
    "audienceIds": null,
    "variations": [...],                    // See 2.4
    "weightDistributions": [{               // Traffic allocation
        "entityId": "6552372625801216",     // Variation ID
        "endOfRange": 10000                 // 10000 = 100%, 5000 = 50%
    }],
    "name": null,
    "bucketingStrategy": null,
    "experimentMetadata": {
        "allocationPolicy": "manual",       // Traffic allocation mode
        "layerId": "5129813690679296"       // Reference to parent layer
    },
    "deployed": false                       // Deployment status
}]
```

**Key Verification Points**:
- `weightDistributions[].endOfRange`: Verify traffic % matches experiment setup
- `deployed`: Should be `false` for draft, published experiments may have specific handling
- Variation IDs match those in `variations` array

### 2.4 Variations Array (inside Experiments)

```javascript
"variations": [{
    "id": "5589654464888832",              // Variation unique ID
    "name": null,
    "actions": [{                           // Per-page actions
        "viewId": "6524733806608384",       // Page ID
        "changes": []                       // Changes for this page
    }]
}, {
    "id": "6552372625801216",
    "name": null,
    "actions": [{
        "viewId": "6524733806608384",
        "changes": [...]                    // See 2.5
    }]
}]
```

### 2.5 Changes Array (inside Actions)

Each **change** is a DOM modification (CSS, HTML, custom code, etc.).

```javascript
"changes": [{
    "id": "36608CD5-6ACA-4B4C-9FE3-8E3D240CBD6C",
    "type": "custom_code",                  // See Section 4
    "dependencies": [],                     // IDs of changes this depends on
    "name": "",
    "isOpalManaged": false,                 // AI-generated flag
    "value": "function($) { ... }"          // Change value (code/HTML/CSS)
}, {
    "id": "7AFD79BD-4DB5-4A3D-96FB-61465556A6CE",
    "type": "attribute",                    // Inline CSS + HTML
    "dependencies": [],
    "name": "",
    "isOpalManaged": false,
    "selector": "body > div > div:nth-of-type(1) > p:nth-of-type(1)",
    "attributes": {},                       // HTML attributes to set
    "css": {
        "color": "rgba(48, 201, 109, 1)"    // Inline CSS
    }
}]
```

### 2.6 Views Array (Pages/URLs)

**Views** define which URLs the experiment targets.

```javascript
"views": [{
    "id": "5118466064121856",
    "category": "other",
    "apiName": "4868003032989696_levis",    // Unique API name
    "name": null,
    "staticConditions": ["and", ["or", {
        "match": "simple",                  // URL match type
        "type": "url",
        "value": "https://www.levi.com/US/en_US/levis-select-styles-deals/..."
    }]],
    "deactivationEnabled": false,
    "undoOnDeactivation": false,
    "tags": [],
    "activationType": "callback",           // How VE activates changes
    "activationCode": "function() { ... }"  // Generated by VE
}]
```

**Key Verification Point**: `staticConditions` must match the saved page URL you selected in VE.

### 2.7 Events Array

**Events** track user interactions (clicks, custom events).

```javascript
"events": [{
    "id": "4559142996672512",
    "viewId": "5143938005204992",           // Associated page ID
    "name": null,
    "category": "other",
    "apiName": "4868003032989696_click_donate",  // Unique API name
    "eventType": "click",                   // Type: click, custom, pageview
    "eventFilter": {
        "filterType": "target_selector",
        "selector": "body > div > div > p:nth-of-type(5)"  // Click target
    }
}, {
    "id": "4839532567199744",
    "viewId": null,                         // null = global custom event
    "apiName": "custom-event-1",
    "eventType": "custom",
    "eventFilter": null                     // No selector for custom events
}]
```

**Key Verification Points**:
- Click events must have valid `selector` matching element on page
- Global custom events have `viewId: null`
- Event IDs are referenced in experiment metrics

### 2.8 Visitor Attributes (DCP Integration)

```javascript
"visitorAttributes": [{
    "id": "28174530645",
    "datatype": "string",
    "dcp_datasource_id": "28254110388"      // Links to DCP datasource
}]
```

### 2.9 DCP Keyfield Locators (Audience Data)

Maps where to find audience attributes (cookies, JS variables, etc.).

```javascript
"dcpKeyfieldLocators": [{
    "dcp_datasource_id": "28254110388",
    "is_optimizely": false,
    "type": "cookie",                       // Source: cookie, js_variable, uid
    "name": "my_cookie"                     // Cookie/variable name
}, {
    "dcp_datasource_id": "29007540065",
    "is_optimizely": false,
    "type": "js_variable",
    "name": "userID"                        // JavaScript variable name
}]
```

### 2.10 Dimensions (Analytics)

```javascript
"dimensions": [{
    "id": "6604183780982784",
    "name": null,
    "apiName": "Custom1",                   // Dimension API name
    "segmentId": null
}]
```

---

## 3. Key Verification Points

### Essential Verification Checklist

Use this checklist when verifying that VE changes were correctly published to the snippet:

| # | Element | Verification Method | Common Issues |
|---|---------|-------------------|----------------|
| **1** | **project_id** | Open snippet in browser → `Ctrl+F "projectId"` → Match against JIRA/experiment | Mismatch = wrong project/namespace |
| **2** | **revision** | Before/after publish → revision # should increment | Missing increment = publish failed silently |
| **3** | **layer_id & experiment_id** | Variation detail page → API Names section → Copy IDs → Search in snippet | Not found = experiment not included in snippet |
| **4** | **variation_id & weightDistributions** | Search variation ID in snippet → Verify in `weightDistributions.entityId` → Check `endOfRange` % | Wrong % = traffic allocation failed |
| **5** | **changes array** | Find variation → Find action → Verify `changes[].id`, `type`, `selector`, value present | Missing changes = VE publish failed |
| **6** | **view_id & staticConditions** | Search page URL in snippet → Find matching `views[].staticConditions` | URL not found = page not targeting correctly |
| **7** | **event_id & selector** | Search event ID in snippet → Verify `eventFilter.selector` matches clicked element | Wrong selector = event won't track |
| **8** | **isOpalManaged flag** | Find changes → Check `isOpalManaged: true/false` | Inconsistent = Opal vs manual distinction unclear |
| **9** | **dependencies array** | Complex changes → Verify dependency IDs exist as other changes | Broken dependencies = async execution order wrong |

### Common Issues & Debugging

| Issue | Root Cause | How to Fix |
|-------|-----------|-----------|
| **Changes not appearing on page** | Selector invalid or changed DOM | 1. Verify selector matches element 2. Check element still exists in customer website 3. Test selector in browser DevTools |
| **Traffic allocation wrong** | `weightDistributions.endOfRange` incorrect | Edit experiment in Monolith → Verify % → Republish from VE |
| **Event not tracking** | Selector in `eventFilter` invalid | Click element in VE → Update event → Verify new selector in snippet |
| **Page not activating** | `staticConditions` URL mismatch | Check saved page URL → Update targeting → Republish experiment |
| **Revision not incrementing** | Publish failed or cached old version | 1. Manually refresh CDN cache 2. Check browser cache 3. Republish experiment |
| **Variation not in weightDistributions** | Variation created but not added to experiment | Add variation to experiment → Set traffic % → Publish |
| **isOpalManaged true but shouldn't be** | Opal AI created/modified change | Manually edit change in VE to override flag behavior |
| **Dependency chain broken** | Referenced change ID doesn't exist | Edit changes → Remove invalid dependencies → Test async execution |

---

## 4. Change Types Reference

### Overview of 5 Change Types

| Type | Purpose | Usage |
|------|---------|-------|
| **attribute** | Inline CSS + HTML modification | Text changes, style updates, small element mods |
| **append** | Insert CSS/HTML into specific selector | Add stylesheets into `<head>`, add elements after target |
| **custom_code** | Execute JavaScript function | Complex DOM manipulation, dynamic logic |
| **rearrange** | Move/reorder DOM elements | Drag-to-reorder layout changes |
| **remove** | Hide/delete elements | Remove elements with `attributes.remove: true` |

### 4.1 Attribute Change (Most Common)

**Use Case**: Inline CSS styling + HTML text changes

```javascript
{
    "id": "7AFD79BD-4DB5-4A3D-96FB-61465556A6CE",
    "type": "attribute",
    "dependencies": [],
    "name": "",
    "isOpalManaged": false,
    "selector": "body > div > div:nth-of-type(1) > p:nth-of-type(1)",
    "attributes": {
        "html": "New text content"          // Text/HTML to set
    },
    "css": {
        "color": "rgba(48, 201, 109, 1)",   // Green color
        "background-color": "rgba(155, 213, 219, 1)"  // Light cyan
    }
}
```

**VE Feature**: Element Change Manager → All *Manager components (StyleManager, BackgroundManager, TypographyEditor)

---

### 4.2 Custom Code Change

**Use Case**: Complex JavaScript logic, dynamic calculations, DOM traversal

```javascript
{
    "id": "36608CD5-6ACA-4B4C-9FE3-8E3D240CBD6C",
    "type": "custom_code",
    "dependencies": [],
    "name": "",
    "isOpalManaged": false,
    "value": "function($) {\n    var utils = window.optimizely.get('utils');\n    utils.waitForElement('body').then(function() {\n        $('body').css('background-color', 'grey');\n    });\n}"
}
```

**VE Feature**: Code Editor Panel → Full-page code editor

**Important**: Custom code executes **after** attribute changes.

---

### 4.3 Append Change

**Use Case**: Inject CSS into `<head>` or append HTML elements

```javascript
{
    "id": "9526DCBB-530F-4269-A1D4-A5D321F90B8A",
    "type": "append",
    "dependencies": [],
    "name": "",
    "isOpalManaged": false,
    "selector": "head",
    "value": "<style>h1{\n    color: red;\n}</style>"
}
```

**VE Feature**: Insert HTML → Insert mode = "append"

---

### 4.4 Rearrange Change

**Use Case**: Drag element to new position (via VE drag-and-drop)

```javascript
{
    "id": "7889A0E6-4151-4805-9DDE-7B4A450B44EF-rearrange",
    "type": "rearrange",
    "selector": "body > main > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2)",
    "insertSelector": "body > main > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(3)",
    "operator": "after",                    // "after" or "before"
    "dependencies": ["7889A0E6-4151-4805-9DDE-7B4A450B44EF"]  // Must depend on the element being moved
}
```

**VE Feature**: Layout Manager → Rearrange (drag to reorder)

---

### 4.5 Remove Change

**Use Case**: Hide element via CSS or remove from DOM

```javascript
{
    "id": "B77DE7BE-4C0D-44B1-9250-885EBE478FE6",
    "type": "attribute",
    "selector": "[data-props='null'] > div:nth-of-type(1)",
    "attributes": {
        "remove": true                      // Flag: element should be removed
    },
    "css": {}
}
```

**VE Feature**: Element Change Manager → Layout Manager → Visibility toggle

---

## 5. Test Data Examples

### Example 1: A/B Test with Attribute Changes

**Scenario**: Color change to H1 heading

```javascript
{
    "projectId": "4868003032989696",
    "revision": "1909",
    "layers": [{
        "id": "5851457308590080",
        "experiments": [{
            "id": "5192038094733312",
            "variations": [{
                "id": "5112256493518848",  // Control
                "actions": [{
                    "viewId": "5118466064121856",
                    "changes": []
                }]
            }, {
                "id": "6244622641397760",  // Variation
                "actions": [{
                    "viewId": "5118466064121856",
                    "changes": [{
                        "id": "6F1CEA0E-48D1-42AE-88F5-48379221313E",
                        "type": "attribute",
                        "selector": "h1",
                        "attributes": {
                            "html": "Men's Select Styles"
                        },
                        "css": {
                            "background-color": "rgba(155, 213, 219, 1)"
                        }
                    }]
                }]
            }],
            "weightDistributions": [{
                "entityId": "6244622641397760",
                "endOfRange": 10000  // 100% to variation
            }]
        }],
        "viewIds": ["5118466064121856"]
    }],
    "views": [{
        "id": "5118466064121856",
        "apiName": "4868003032989696_levis",
        "staticConditions": ["and", ["or", {
            "match": "simple",
            "type": "url",
            "value": "https://www.levi.com/US/en_US/levis-select-styles-deals/..."
        }]]
    }]
}
```

**Verification**: 
- ✅ Variation ID `6244622641397760` present in changes
- ✅ CSS color property matches design spec
- ✅ Selector `h1` valid and unique on page
- ✅ Page URL matches saved page targeting

---

### Example 2: Multi-Page Experiment with Events

```javascript
{
    "layers": [{
        "id": "5994052991057920",
        "viewIds": ["5118466064121856", "6009865366142976", "6261593835569152", "6728585629663232"]
    }],
    "views": [
        { "id": "5118466064121856", "staticConditions": [...] },
        { "id": "6009865366142976", "staticConditions": [...] },
        { "id": "6261593835569152", "staticConditions": [...] },
        { "id": "6728585629663232", "staticConditions": [...] }
    ],
    "events": [{
        "id": "6426184238497792",
        "viewId": "5118466064121856",
        "apiName": "4868003032989696_eventwomen",
        "eventType": "click",
        "eventFilter": {
            "filterType": "target_selector",
            "selector": "body > div > div > header > div > div > nav > div > div > div > div > div > div > li:nth-of-type(3) > button"
        }
    }]
}
```

**Verification**:
- ✅ All 4 pages in `viewIds` have corresponding entries in `views` array
- ✅ Event selector is specific to page 1 (`viewId: "5118466064121856"`)
- ✅ Click target element exists on live website

---

### Example 3: Campaign with Dependent Changes

```javascript
{
    "changes": [{
        "id": "7889A0E6-4151-4805-9DDE-7B4A450B44EF",
        "type": "attribute",
        "selector": "body > main > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2)",
        "attributes": { "html": "..." },
        "css": { "color": "green" }
    }, {
        "id": "7889A0E6-4151-4805-9DDE-7B4A450B44EF-rearrange",
        "type": "rearrange",
        "selector": "body > main > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2)",
        "insertSelector": "body > main > div > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(3)",
        "operator": "after",
        "dependencies": ["7889A0E6-4151-4805-9DDE-7B4A450B44EF"]  // Depends on style change
    }]
}
```

**Verification**:
- ✅ Rearrange change has `dependencies` pointing to the style change
- ✅ Both changes target the same element
- ✅ Async execution order preserved (style → rearrange)

---

## 6. Common Debugging Patterns

### Pattern 1: "Changes Not Visible on Live Site"

**Checklist**:
1. Verify revision incremented after publish
2. Clear browser cache: `Cmd+Shift+R` (hard refresh)
3. Check selector in browser DevTools:
   ```javascript
   document.querySelectorAll("body > div > div:nth-of-type(1) > p:nth-of-type(1)")
   // Should return 1 element if selector is valid
   ```
4. Verify element is visible (not `display: none`, `opacity: 0`, etc.)
5. Check if element is inside Shadow DOM (VE can't modify outside its iframe)

### Pattern 2: "Traffic Not Distributed Correctly"

**Check in snippet**:
```javascript
weightDistributions: [
    { entityId: "VARIATION_1", endOfRange: 5000 },  // 50%
    { entityId: "VARIATION_2", endOfRange: 10000 }  // 50%
]
// endOfRange values: 0-10000 range represents 0-100%
// Gaps = traffic not allocated
```

### Pattern 3: "Event Not Tracking"

**Debugging steps**:
1. Open browser DevTools → Network tab
2. Perform action that should trigger event
3. Search for API call containing event ID: `4559142996672512`
4. Verify selector still matches element: `document.querySelector("selector")`
5. If selector invalid → Event data in snippet is stale

### Pattern 4: "Opal AI-Generated Changes Inconsistent"

**Check**: `isOpalManaged` flag
```javascript
{ "id": "...", "type": "attribute", "isOpalManaged": true }  // AI-generated
{ "id": "...", "type": "attribute", "isOpalManaged": false } // Manual
```

If Opal changes behave unexpectedly → Manually edit in VE to flag as `isOpalManaged: false`

---

## References

See related documentation:
- [FULL_FLOW_SPEC.md](./FULL_FLOW_SPEC.md) — End-to-end VE testing flow
- [IMPACT_INDEX.md](./IMPACT_INDEX.md) — Component blast radius analysis
- [UI_Screenshots_Analysis.md](./UI_Screenshots_Analysis.md) — Monolith screen verification
- [CLAUDE.md](./CLAUDE.md) — Complete project architecture (Section 2 = snippet context)
- [API.md](./API.md) — API endpoints for experiments/events/views

---

## How to Use This Guide

### For QA Engineers Analyzing VE Tickets
1. **Read Section 1** (Overview) to understand snippet composition
2. **Read Section 2** (JSON Structure) to know what to search for in live snippet
3. **Read Section 3** (Verification Checklist) to write Expected Results for "live site verification" TCs
4. **Reference Section 4** (Change Types) when describing DOM modifications in test steps
5. **Use Section 5** (Test Data Examples) for sample IDs and property mappings

### For Debugging Snippet-Related Failures
1. Open snippet URL in browser
2. Search for keyword from test failure (selector, event ID, layer ID, etc.)
3. Reference Section 6 (Debugging Patterns) for root cause
4. Use Section 3 (Common Issues table) to determine fix strategy

### For Opal AI Integration
- When test case involves Opal AI variation building → Check `isOpalManaged` flag
- If AI changes behave inconsistently → Check change dependencies and async execution order
- Reference Section 4.1-4.5 for expected change type patterns from Opal

---

**Document Version**: 1.0  
**Status**: Active  
**Used By**: `/exp-qa-agents:web-analyze-ticket`, `/exp-qa-agents:web-create-test-cases`
