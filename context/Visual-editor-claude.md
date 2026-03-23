# Visual Editor - Claude Code Context

> **Optimizely Visual Editor** - A micro-frontend for editing web content to create variations for customer websites. This micro-frontend is loaded via snippet injection into customer websites and provides a WYSIWYG editing experience with AI-powered assistance.

**Last Updated**: 2026-03-13
**Repository**: https://github.com/optimizely/visual-editor

---

## Table of Contents

1. [Architecture & Directory Structure](#1-architecture--directory-structure)
2. [Core Logic & Business Rules](#2-core-logic--business-rules)
3. [QA & Testing Standards](#3-qa--testing-standards)
4. [JIRA Analysis Context](#4-jira-analysis-context)
5. [Functional Tree (UI to Code Map)](#5-functional-tree-ui-to-code-map)

---

## 1. Architecture & Directory Structure

### Architecture & Data Flow

```
Customer Website → Optimizely Snippet → Visual Editor (Shadow DOM)
                                         ├─ Bottom Bar UI
                                         ├─ Highlighters
                                         └─ Opal Chat (Federated)
                                              │
                ┌─────────────────────────────┼─────────────────┐
                ▼                             ▼                 ▼
          Monolith API                  Frontdoor API     Opal Backend
```

**Flow**: Init (OAuth2 → fetch config) → User interacts (hover/click → modify) → Save (JSON → API) → Opal Chat (AI generates changes → apply)

### Directory Structure

```
src/
├── components/          # UI (background_manager, border_manager, editors, highlighter, etc.)
├── stores/             # Zustand stores (⭐changeStore, authStore, experimentStore, etc.)
├── services/api/       # API clients (auth, experiments, events, projects)
├── modules/            # Core logic (⭐changes.ts, ⭐selectorator.ts)
├── hooks/              # Custom hooks (useAuth, useBreakpoints, useFeatureFlag, etc.)
├── utils/              # Helpers (⭐testUtils, dom, formatter, codeTemplates)
├── types/              # TypeScript definitions
├── ⭐constants.ts      # App constants
└── ⭐App.tsx           # Root component

⭐ = Critical files
```

---

## 2. Core Logic & Business Rules

### Critical Modules

| Module | Purpose | Key Functions | Business Rules |
|--------|---------|--------------|----------------|
| **changeStore.ts** (24KB) | Change management | `applyChange()`, `removeChange()`, `setChanges()` | Ordered application, unique IDs (GUID), reversible, max 1000/variation |
| **changes.ts** (19KB) | DOM manipulation | `applyChangeToDOM()`, `applyInsertHTML()`, `applyStyleChange()` | XSS-safe (`insertAdjacentHTML`), inline styles, silent failure |
| **selectorator.ts** (23KB) | CSS selector gen | `getSelectorForElement()`, `isUniqueSelector()` | Prefer ID → class → nth-child, max 10 levels, must be unique |
| **experiments.ts** (10KB) | API client | `fetchExperiment()`, `updateVariation()` | OAuth2 token, 1hr expiry, endpoints: `/v2/experiments/*` |
| **auth.ts** (7KB) | OAuth2 auth | `authenticate()`, `refreshToken()`, `getOptiIdToken()` | Token in query params → sessionStorage, refresh @ 55min |

**Critical Path**: User action → changeStore → changes.ts → Customer DOM → API (save)

---

### Business Rules

**Selector Uniqueness** (selectorator.ts) | **Ordered Changes** (changeStore.ts) | **Reversible** (changes.ts) | **XSS-safe** (insertAdjacentHTML) | **Shadow DOM** (App.tsx) | **Token 1hr** (auth.ts) | **Feature Flags** (constants.ts, useFeatureFlag)

---

## 3. QA & Testing Standards

### Test Commands

```bash
npm test                  # Run all tests
npm test -- <file>        # Run specific file
npm test -- --watch       # Watch mode
npm test -- --coverage    # Coverage report
npm run lint              # Linter
npm run format            # Prettier
```

### Test Standards

**Structure**: `*.test.ts` co-located | `describe()` blocks | `data-test-section` attributes

**Requirements**:
- ✅ Use actual Zustand stores (NO mocking)
- ✅ Test isolation (`beforeEach` reset)
- ✅ Feature flag paths (ON/OFF via `mockFeatureFlag()`)
- ✅ Descriptive names (behavior, not implementation)

### Critical Paths (Must Test on Every Change)

| Path | Description | Files to Test |
|------|-------------|---------------|
| **Change Application** | User creates change → DOM updated | `changeStore.test.ts`, `changes.test.ts` |
| **Change Persistence** | User saves changes → API call successful | `experiments.test.ts`, `changeStore.test.ts` |
| **Element Selection** | User clicks element → Selector generated → Element highlighted | `selectorator.test.ts`, `highlighter.test.tsx` |
| **Authentication** | User loads editor → Token validated → User info fetched | `auth.test.ts`, `authStore.test.ts` |
| **Opal Chat Integration** | User sends prompt → Changes generated → Changes applied | `opalChatStore.test.ts`, `changeStore.test.ts` |
| **Multi-Device Preview** | User switches device → Viewport resized → Changes still work | `device_selector.test.tsx` |
| **Change Undo/Redo** | User undoes change → DOM reverted → User redoes → DOM restored | `changeStore.test.ts` |

**Coverage**: Critical modules (changeStore, changes, selectorator, auth) = 90% | UI components = 70% | Utils = 80%

**CI/CD**: Auto-run on PRs (`.github/workflows/pr-pipeline.yaml`), Cypress E2E, deployments (inte/prep/prod)

---

## 4. JIRA Analysis Context

### JIRA Ticket Mapping

| Ticket Type | Code Areas | Example Files |
|-------------|-----------|---------------|
| Bug Fix | Component → Store → Module | Component, store, tests |
| New Feature | New component + stores | Create files, update stores |
| UI/UX | Component styling | `.tsx` + `.scss` |
| API | `services/api/` | API client |
| Performance | Bundle/rendering | Webpack, memoization |

**Workflow**: Identify type → Extract requirements → Map to files → Create test cases from acceptance criteria

| Requirement | Location |
|-------------|----------|
| "Add style editor" | `components/X_manager/` |
| "Fix change not saving" | `changeStore.ts` + `experiments.ts` |
| "Selector generation" | `selectorator.ts` |
| "Auth issue" | `auth.ts` |
| "Opal Chat" | `opalChatStore.ts` + federated |
| "Responsive" | `.scss` + `useBreakpoints.ts` |
| "Feature flag" | `constants.ts` + `useFeatureFlag.ts` |

**Complexity**: Low (1-2 files, 10-50 LOC) | Medium (3-5 files, 50-200 LOC) | High (5-10 files, 200-500 LOC) | Very High (10+ files, 500+ LOC)

**Git**: `git checkout -b feature/TICKET-123` | `git commit -m "[TICKET-123] description"`

---

## Working with Claude Code

**Common Tasks**:
- New editor: `components/[property]_manager/` → `changeStore.ts` → `BottomBar.tsx` → tests
- Fix change not applying: Check `changes.ts` → `selectorator.ts` → browser console
- New API: `services/api/[domain].ts` → types → store → tests
- Feature flag: `constants.ts` (enum) → `useFeatureFlag()` → Optimizely UI

**Pre-Push Checklist**: Tests pass ✓ | Lint clean ✓ | Formatted ✓ | JIRA ref in commit ✓ | No console.log ✓ | Types added ✓ | Coverage ≥70% ✓

**See**: [DEVELOPMENT_STANDARDS.md](./DEVELOPMENT_STANDARDS.md) | [README.md](./README.md) | [.github/workflows/](./.github/workflows/)

---

## 5. Functional Tree (UI to Code Map)

> Maps every UI screen, feature, and function to its source code across **2 repos**:
> - **Monolith** (`optimizely/optimizely`) — App UI: dashboard, experiment/campaign management, settings
> - **Visual Editor** (`optimizely/visual-editor`) — Micro-frontend: WYSIWYG editing, loaded inside monolith via iframe/snippet

### 1. Screens (Cấp độ 1: Màn hình)

#### 1.1. Web Project (Monolith repo: `optimizely/optimizely`)

Base path: `src/www/frontend/src/js/bundles/p13n/`

- **1.1.1. Account Dashboard** (home page after login)
  - `sections/account_dashboard/` | `sections/welcome/`
- **1.1.2. Optimizations** (main optimization management page — 4 tabs)
  - `sections/layers/` | `components/entity_dashboard/` | `components/entity_search_table/`
  - **1.1.2.1. Overview tab** — Combined experiments + campaigns list, Show/Hide Columns panel (20+ columns), column toggle
  - **1.1.2.2. Experiments tab** — Experiment list (Name, Type, Status, Primary Metric, Variations, Results), Status/Type filters, "Get Test Ideas" (Opal AI), "Create..." dropdown, pagination, Action menu (...): Duplicate/Pause/Archive/Conclude
  - **1.1.2.3. Personalization Campaigns tab** — Campaign list (Name, Status, Primary Metric, Audiences, Results), "Create Personalization Campaign", "Get Test Ideas", Action menu (...): Duplicate/Start/Archive/Conclude
  - **1.1.2.4. Exclusion Groups tab** — Exclusion group list, Create Exclusion Group dialog (Name, Description, experiment browser)
- **1.1.3. Experiment Detail** (A/B, MVT, MAB experiment editor)
  - `sections/oasis_experiment_manager/` | `sections/ab_experiment_editor/`
  - **Left sidebar navigation** — Collapsible sections: Target (Activation, Audiences), Design (Variations + CHANGED badge, Shared Code, Traffic Allocation, Stats Configuration), Track (Metrics, Integrations), Plan (Schedule, Summary), Settings (API Names, History)
  - **1.1.3.1. Summary** — Collapsible sections: Activation, Audiences, Variations (Stats Accelerator), Shared Code, Traffic Allocation, Metrics, Stats Configuration, Integrations, Schedule. "Review Experiment" Opal AI button, download icon — `components/experiment_overview/` | `components/layer_name_holdback_detail/`
  - **1.1.3.2. Variations** — `components/experience_manager/` | `components/traffic_allocation/`
    - Variation table: Name (A/B/C/D), Total Traffic %, Screenshot (Upload), Edit dropdown, action menu (...)
    - Variation action menu (...): Rename, Delete, Generate Description (AI sparkle)
    - "Summarize Variations" AI button, "Add Variation..." link
    - Orange dot indicator on changed variations
    - **MVT only**: 2 tabs (Sections | Combinations), "Create New Section...", Total Combinations counter (current / Max: 64)
    - **MVT Combinations tab**: Auto-generated combinations (AA, AB, AC...), Traffic Allocation %, action menu (...): Preview
    - Click variation → **opens Visual Editor** (see 1.3 below)
  - **1.1.3.3. Metrics** — `sections/metrics/` | `components/metrics/` | `components/flags_events_and_metrics_builder/`
  - **1.1.3.4. Audiences** — `sections/audiences/` | `components/audience_selector/` | `components/audience_combinations_builder/`
  - **1.1.3.5. Results** — `sections/results/` | `modules/results_api/`
  - **1.1.3.6. Change History** — `sections/change_history/` | `components/change_history/`
  - **1.1.3.7. Settings (Experiment)** — `components/layer_settings/` | `components/schedule_experience/`
  - **1.1.3.8. Status/Actions** — `components/layer_action_buttons/` | `components/status_switcher/` (Start, Pause, Archive, Conclude)
  - **1.1.3.9. Activation** — Target By (Saved Pages / URL), page browser with search, Create New Page inline, Edit per page, Revert/Save — `components/targeting/`
- **1.1.4. Campaign List** (personalization campaigns — also accessible via 1.1.2.3 tab)
  - `sections/campaign_overview/` | `components/campaign_manager/`
- **1.1.5. Campaign Detail** (personalization campaign editor)
  - `components/campaign_manager/` | `components/experience_manager/`
  - **1.1.5.1. Summary** — Collapsible: Experiences (Holdback/Variation %), Activation, Integrations, Metrics (Primary + Secondary), Shared Code. Download icon
  - **1.1.5.2. Experiences** — Experience list with Holdback + Variations, Traffic %, Preview/Upload/View/Edit buttons, "Summarize Variations" AI, UNPUBLISHED badge, "Add Variation..." link
    - Status dropdown: Run / Conclude / Archive
    - Edit dropdown: "Edit with new editor" / "Edit with legacy editor"
    - Variation menu (...): Rename / Duplicate / Generate Description (AI)
    - Experience menu (...): Publish / Settings / Manage Schedule / Duplicate / Pause / Archive
    - Click variation Edit → **opens Visual Editor** (see 1.3 below)
  - **1.1.5.3. Create New Experience dialog** — Experience Name, Audience, Distribution Mode (Manual / Contextual Bandit / Multi-armed Bandit / Stats Accelerator), Variation names + Traffic %, holdback warning, "Advanced code editor" button
  - **1.1.5.4. Prioritize Experiences dialog** — Drag-to-reorder priority, Traffic Percentage (Auto/manual)
  - **1.1.5.5. Activation** — Same as 1.1.3.9
  - **1.1.5.6. Metrics** — Primary + Secondary metrics
  - **1.1.5.7. Shared Code** — Shared code editor
  - **1.1.5.8. Integrations** — Third-party integrations
- **1.1.6. Audiences** (2 tabs: Saved, Attributes)
  - `sections/audiences/` | `components/audience_combination_builder_v3/`
  - **1.1.6.1. Saved tab** — Audience list (Name, Experiments, ID, Created, Modified), Status filter, Action menu: View Experiment Usage / Archive
  - **1.1.6.2. Attributes tab** — Custom attributes list
  - **1.1.6.3. Create New Audience page** — Name, Description, Audience Conditions (drag-and-drop), Code Mode toggle. Categories: Adaptive, Custom Attributes, Real-Time Segments, External Attributes, Visitor Behaviors, Standard (Ad Campaign, Browser, Cookie, Custom Javascript, Device, IP Address, Language, Location, New/Returning Session, Platform, Query Parameters, Referrer URL, Time/Day of Visit, Traffic Source)
- **1.1.7. Implementation** (5 tabs: Pages, Events, Templates, Catalogs, Recommenders)
  - `sections/implementation/` | `sections/oasis_implementation/` | `components/snippets/`
  - **1.1.7.1. Pages tab** — Page list (Name, API Name, ID, Experiments, Events, Tags), Status filter, "Create New Page", Action menu: Edit Page / View Experiment Usage / Archive — `sections/views/`
  - **1.1.7.2. New Page dialog** — Name*, Editor URL*, Description, Triggers, Conditions (URL Match), Advanced (Deactivation/Undo, Override Page Trimming), Test URL(s) — `components/configure_view_smart/`
  - **1.1.7.3. Events tab** — Events grouped by Page (Name, API Name, Experiments, ID, Type: Custom/Click/Pageview), Action menu: Settings / View Experiment Usage / Archive — `sections/web_events/` | `components/event_properties/`
  - **1.1.7.4. Create New Event dialog** — Event type: Click / Custom / Pageview. Click requires Page selector
  - **1.1.7.5. Templates tab** — Template list (Name, Template Type, Optimizations, ID), Status/Creator filters, "Create Template..." dropdown: Duplicate existing / Use JSON / Use Editor
  - **1.1.7.6. Catalogs tab** — Catalog list, New Catalog dialog (Name, Description, Catalog Events, Event Tags, Indexing Rate)
  - **1.1.7.7. Recommenders tab** — Recommenders list
- **1.1.8. History** (project-level change history)
  - `sections/change_history/` | `components/change_history/`
  - Search by type:ID, Type/Date/Source filters, Change Summary table (description, user, time), Show/Hide details, Diff view (before/after with +/- highlighting)
- **1.1.9. Settings** (7 tabs: Implementation, Webhooks, Integrations, JavaScript, Collaborators, Labs, Advanced)
  - `sections/project_settings/`
  - **1.1.9.1. Implementation tab** — Snippet list (Name, Projects, ID, Revision, Size), "Create Custom Snippet..." button
  - **1.1.9.2. Edit Basic Snippet dialog** — Key, Snippet Details (Platform, Size, Project ID, Revision), Visitor ID, jQuery Inclusion, Privacy settings, Cache Expiration TTL, Dynamic Websites, Trim Unused Pages, Shadow DOM support, Cross-Origin Tracking, Optimizely X config — `components/snippets/` | `modules/snippet_configuration/`
  - **1.1.9.3. Webhooks tab** — Webhook configuration
  - **1.1.9.4. Integrations tab** — Third-party integrations (GA4, etc.) — `components/google_analytics_4/`
  - **1.1.9.5. JavaScript tab** — Project-level JavaScript
  - **1.1.9.6. Collaborators tab** — User access management
  - **1.1.9.7. Labs tab** — Experimental features
  - **1.1.9.8. Advanced tab** — Advanced project settings — `components/data_layer/` | `components/stats_config/`
- **1.1.10. Features (Flags)** — `sections/features/` | `components/feature_form/`
- **1.1.11. Idea Builder (Opal)** — `sections/idea_builder/`
- **1.1.12. Opal Review Experiment** — `components/opal_review_experiment/` | `components/opal_attention_banner/`
- **1.1.13. Plugin Builder** — `sections/plugin_builder/`

**Shared Monolith modules:** `modules/current_layer/` | `modules/dashboard/` | `modules/editor/` | `modules/editor_iframe/` | `modules/metrics_manager/` | `modules/results_api/` | `modules/campaign_manager/`

**Shared Monolith components:** `components/dialogs/` | `components/targeting/` | `components/custom_code/` | `components/data_layer/` | `components/concurrency/`

#### 1.2. Performance Edge (Monolith repo: `optimizely/optimizely`)

Same monolith UI as Web Project. Edge experiments use the same `sections/` and `components/` with Edge-specific API endpoints and experiment types handled by `modules/current_layer/`.

- Same screens as 1.1.2 through 1.1.10 above (filtered by project type = Edge)

#### 1.3. Visual Editor (Visual Editor repo: `optimizely/visual-editor`)

Loaded when user clicks a **variation** in an experiment (1.1.3.2 / 1.2). Renders as a micro-frontend inside customer website via iframe + snippet injection (Shadow DOM).

Base path: `src/`

- **1.3.1. Bottom Bar** (main editor container, always visible)
  - **1.3.1.1. Variation Row** (top section — variation tabs)
  - **1.3.1.2. Interaction Bar** (main control row — page switcher, device selector, tools)
  - **1.3.1.3. Code Editor Panel** (full-screen variation code editor)
  - **1.3.1.4. Element Change Manager** (right panel when element selected)
  - **1.3.1.5. Event Editor** (right panel for event tracking)
  - **1.3.1.6. Redirect Overlay** (redirect URL configuration)
- **1.3.2. Highlighter** (hover/click element selection overlay on customer page)
  - **1.3.2.1. Hover Overlay** (element boundary highlight on hover)
  - **1.3.2.2. Element Action Menu** (context menu on selected element)
- **1.3.3. Attribute List Popup** (events/tags popover from bottom bar)
- **1.3.4. Conditional Activation Dialog** (modal — activation conditions)
- **1.3.5. Element Selector Dialog** (modal — advanced CSS selector picker)
- **1.3.6. Device Selector Popup** (popup window — multi-device preview)
- **1.3.7. Notification Panel** (toast notifications at top)
- **1.3.8. Opal Chat Panel** (AI assistant — federated module)

---

### 2. Features & Code — Monolith (Cấp độ 2 + 3)

> **Repo:** `optimizely/optimizely` | **Base path:** `src/www/frontend/src/js/bundles/p13n/`
> **Tech Stack:** Nuclear.js (Flux), React, Backbone models, AngularJS (legacy), SCSS

#### 1.1.1. Account Dashboard

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| Project list | Display all projects (Web, Edge, FX) | `sections/account_dashboard/` | `optly/modules/current_project/` |
| Create project | Create new Web/Edge/FX project | `sections/project_creation/` | `optly/modules/current_project/` |
| Welcome screen | Onboarding for new users | `sections/welcome/` | — |

#### 1.1.2. Optimizations (4 tabs)

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| **Overview tab** | Combined experiments + campaigns list, sorted by Modified | `sections/layers/`, `components/entity_dashboard/` | `modules/dashboard/` |
| Show/Hide Columns | Toggle 20+ columns: Name, Type, Status, Creator, Modified, First/Last Published, Last Paused, Primary Metric, Days Running, Variations, Pages, Audiences, Targeting Method, Experiment ID, Traffic Allocation, Distribution Mode, Results, Results Outcome, Journey | `components/entity_dashboard/` | — |
| **Experiments tab** | Experiment list (Name, Type, Status, Primary Metric, Variations, Results), pagination | `sections/layers/`, `components/entity_search_table/` | `modules/dashboard/` |
| **Personalization Campaigns tab** | Campaign list (Name, Status, Primary Metric, Audiences, Results) | `sections/campaign_overview/` | `modules/campaign_manager/` |
| **Exclusion Groups tab** | Exclusion group list, Create Exclusion Group dialog (Name, Description, experiment browser) | `components/entity_dashboard/` | — |
| Entity search | Search by name, key, description | `components/entity_search_table/`, `components/entity_search/` | — |
| Status/Type filters | Filter by Active/Archived status, All/A/B Test/MVT/Campaign type | `components/entity_dashboard/` | `modules/dashboard/` |
| Create experiment | "Create..." dropdown: A/B Test, Multivariate Test, Personalization Campaign | `sections/layers/` | `modules/current_layer/` |
| Get Test Ideas | Opal AI-powered test idea generation | `sections/idea_builder/` | — |
| Experiment action menu | Per-row (...): Duplicate, Start/Pause, Archive, Conclude | `components/table_actions/` | `modules/publish_status/` |
| Campaign action menu | Per-row (...): Duplicate, Start, Archive, Conclude | `components/table_actions/` | `modules/campaign_manager/` |

#### 1.1.3. Experiment Detail

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| **Summary** | Collapsible sections: Activation, Audiences, Variations (Stats Accelerator), Shared Code, Traffic Allocation, Metrics, Stats Configuration, Integrations, Schedule. Download icon | `sections/oasis_experiment_manager/`, `components/experiment_overview/` | `modules/currently_editing_experiment/` |
| Review Experiment (Opal) | AI-powered experiment review button | `components/opal_review_experiment/` | — |
| **Activation** | Target By (Saved Pages / URL), page browser with search, Create New Page inline, Edit per page, Revert/Save | `components/targeting/` | — |
| **Left sidebar navigation** | Collapsible sections: Target (Activation, Audiences), Design (Variations + CHANGED badge, Shared Code, Traffic Allocation, Stats Configuration), Track (Metrics, Integrations), Plan (Schedule, Summary), Settings (API Names, History) | `sections/oasis_experiment_manager/` | — |
| Variations | Variation table (Name A/B/C/D, Total Traffic %, Screenshot Upload, Edit dropdown) | `components/experience_manager/`, `components/traffic_allocation/` | `modules/current_layer/` |
| Variation action menu | Per-variation (...): Rename, Delete, Generate Description (AI sparkle) | `components/experience_manager/` | — |
| Summarize Variations | AI sparkle button — generates variation summaries | `components/experience_manager/` | — |
| Screenshot upload | Upload screenshot per variation | `components/experience_manager/` | — |
| Add Variation | "Add Variation..." link | `components/experience_manager/` | — |
| Orange dot indicator | Visual indicator on variations with changes | `components/experience_manager/` | — |
| **MVT: Sections tab** | Section-based variation groups, "Create New Section...", Total Combinations counter (current / Max: 64) | `components/experience_manager/` | `modules/current_layer/` |
| **MVT: Combinations tab** | Auto-generated combinations (AA, AB...), Traffic Allocation %, Combination action menu (...): Preview | `components/experience_manager/` | `modules/current_layer/` |
| Open Visual Editor | Click variation → load VE in iframe | `components/editor_iframe/`, `components/editor/` | `modules/editor/`, `modules/editor_iframe/` |
| Shared Code | Project-level shared JS/CSS | `components/custom_code/` | — |
| Traffic Allocation | Distribution mode (Manual / Contextual Bandit / Multi-armed Bandit / Stats Accelerator), visitor % | `components/traffic_allocation/` | `modules/current_layer/` |
| Stats Configuration | Stats engine settings | `components/stats_config/` | — |
| Metrics | Add/edit metrics (events + goals) | `sections/metrics/`, `components/metrics/` | `modules/metrics_manager/` |
| Audiences | Configure audience targeting | `sections/audiences/`, `components/audience_selector/` | — |
| Results | View experiment results & stats | `sections/results/` | `modules/results_api/` |
| API Names | View/edit API names | — | — |
| History | View experiment change log | `sections/change_history/`, `components/change_history/` | — |
| Schedule | Set start/end dates | `components/schedule_experience/` | — |
| Settings | Holdback, stats engine | `components/layer_settings/`, `components/stats_config/` | `modules/layer_settings/` |
| Status actions | Start, Pause, Archive, Conclude via dropdown + Publish button | `components/layer_action_buttons/`, `components/status_switcher/` | `modules/publish_status/` |
| Concurrency | Multi-user editing conflict detection | `components/concurrency/` | `modules/concurrency/` |

#### 1.1.4–5. Campaign List & Detail

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| Campaign list | Display personalization campaigns (also via 1.1.2.3 tab) | `sections/campaign_overview/` | `modules/campaign_manager/` |
| **Campaign Summary** | Collapsible: Experiences (Holdback/Variation %, Stats Accelerator), Activation, Integrations, Metrics (Primary + Secondary), Shared Code. Download icon | `components/campaign_manager/` | `modules/campaign_manager/` |
| **Experiences management** | Experience list with Holdback + Variations, Total Traffic %, Preview/Upload/View/Edit buttons, UNPUBLISHED badge, CAMPAIGN PAUSED status | `components/experience_manager/` | — |
| Summarize Variations | AI sparkle button — generates variation summaries | `components/experience_manager/` | — |
| Edit variation | "Edit" dropdown: "Edit with new editor" / "Edit with legacy editor" → opens VE | `components/experience_manager/` | `modules/editor/` |
| Variation action menu | Per-variation (...): Rename, Duplicate, Generate Description (AI) | `components/experience_manager/` | — |
| Experience action menu | Per-experience (...): Publish, Settings, Manage Schedule, Duplicate, Pause, Archive | `components/experience_manager/` | `modules/campaign_manager/` |
| Add Variation | "Add Variation..." link to add variation to experience | `components/experience_manager/` | — |
| Create New Experience | Dialog: Experience Name, Audience (Everyone), Distribution Mode (Manual / Contextual Bandit / Multi-armed Bandit / Stats Accelerator), Variation names + Traffic %, holdback warning, "Advanced code editor" button | `components/experience_manager/` | `modules/campaign_manager/` |
| Prioritize Experiences | Dialog: Drag-to-reorder priority, Traffic Percentage (Auto/manual) | `components/experience_manager/` | `modules/campaign_manager/` |
| Campaign status | Status dropdown: Run / Conclude / Archive. "Publish Campaign" button | `components/campaign_manager/` | `modules/campaign_manager/` |
| Activation | Target By (Saved Pages / URL), page browser | `components/targeting/` | — |
| Metrics | Primary + Secondary metrics | `components/metrics/` | `modules/metrics_manager/` |
| Shared Code | Campaign-level shared JS/CSS | `components/custom_code/` | — |
| Integrations | Third-party integrations | — | — |
| API Names | View/edit API names | — | — |
| History | Campaign change log | `sections/change_history/` | — |

#### 1.1.6. Audiences (2 tabs: Saved, Attributes)

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| **Saved tab** | Audience list (Name, Experiments, ID, Created, Modified) | `sections/audiences/` | `modules/audience_usage/` |
| Status filter | Filter by Active/Archived | `sections/audiences/` | — |
| Audience action menu | Per-row (...): View Experiment Usage, Archive | `sections/audiences/` | — |
| **Attributes tab** | Custom attributes list | `sections/audiences/` | — |
| **Create New Audience** | Full-page: Name*, Description, Audience Conditions (drag-and-drop), Code Mode toggle | `components/audience_combination_builder_v3/` | — |
| Condition categories | Adaptive, Custom Attributes, Real-Time Segments (NEW!), External Attributes, Visitor Behaviors | `components/audience_combination_builder_v3/` | — |
| Standard conditions | Ad Campaign, Browser, Cookie, Custom Javascript, Device, IP Address, Language, Location, New/Returning Session, Platform, Query Parameters, Referrer URL, Time/Day of Visit, Traffic Source | `components/audience_combination_builder_v3/` | — |
| Audience search picker | Search & select audiences (used in experiment/campaign) | `components/audience_search_picker/` | — |

#### 1.1.7. Implementation (5 tabs: Pages, Events, Templates, Catalogs, Recommenders)

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| **Pages tab** | Page list (Name, API Name, ID, Experiments, Events, Tags), Status filter | `sections/views/` | — |
| Page action menu | Per-row (...): Edit Page, View Experiment Usage, Archive | `sections/views/` | — |
| Create New Page | "Create New Page" button → New Page dialog | `sections/views/`, `components/configure_view_smart/` | — |
| New Page dialog | Name*, Editor URL*, Description, Triggers (Immediately/etc), Conditions (URL Match with match types: Simple Match/etc), Advanced (Deactivation and Undo, Override Page Trimming), Test URL(s) | `components/configure_view_smart/` | — |
| **Events tab** | Events grouped by Page (Name, API Name, Experiments, ID, Type: Custom/Click/Pageview), Status filter | `sections/web_events/` | `modules/current_event/` |
| Event action menu | Per-row (...): Settings, View Experiment Usage, Archive | `sections/web_events/`, `components/event_properties/` | — |
| Create New Event | Dialog: Event type (Click/Custom/Pageview). Click requires Page selector | `sections/web_events/` | `modules/current_event/` |
| **Templates tab** | Template list (Name, Template Type, Optimizations, ID), Status/Creator filters | `sections/implementation/` | — |
| Create Template | "Create Template..." dropdown: Duplicate existing, Use JSON, Use Editor | `sections/implementation/` | — |
| **Catalogs tab** | Catalog list with Status filter | `sections/implementation/` | — |
| New Catalog dialog | Name*, Description, Catalog Events (search + add page views), Assign Event Tags (Primary ID, Source URL), Indexing Rate (5000/min default) | `sections/implementation/` | — |
| **Recommenders tab** | Recommenders list | `sections/implementation/` | — |
| Track clicks | Configure click event tracking | — | `modules/track_clicks_change/` |

#### 1.1.8. History (project-level)

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| Change history list | Change Summary table: description, user, time | `sections/change_history/`, `components/change_history/` | — |
| Search | Search by type:ID | `sections/change_history/` | — |
| Filters | Type (Any), Date (Anytime), Source (Any) | `sections/change_history/` | — |
| Show/Hide details | Expand entry to see diff | `components/change_history/` | — |
| Diff view | Before/after code comparison with line numbers, +/- highlighting | `components/change_history/` | — |

#### 1.1.9. Settings (7 tabs: Implementation, Webhooks, Integrations, JavaScript, Collaborators, Labs, Advanced)

| Feature | Description | Code (Sections/Components) | Code (Modules) |
|---------|-------------|---------------------------|----------------|
| **Implementation tab** | Snippet list (Name, Projects, ID, Revision, Size), "Create Custom Snippet..." button | `sections/project_settings/`, `components/snippets/` | `modules/snippet_configuration/` |
| Edit Basic Snippet | Dialog: Key, Snippet Details (Platform, Size, Project ID, Revision), Visitor ID (Identifier Type), jQuery Inclusion (3 options), Privacy (mask names, disable force variation, anonymize IP), Cache Expiration TTL, Dynamic Websites, Trim Unused Pages, Shadow DOM support, Cross-Origin Tracking, Optimizely X config | `components/snippets/` | `modules/snippet_configuration/` |
| **Webhooks tab** | Webhook configuration | `sections/project_settings/` | — |
| **Integrations tab** | Third-party integrations (GA4, etc.) | `components/google_analytics_4/` | — |
| **JavaScript tab** | Project-level JavaScript | `sections/project_settings/` | — |
| **Collaborators tab** | User access management | `sections/project_settings/` | — |
| **Labs tab** | Experimental features | `sections/project_settings/` | — |
| **Advanced tab** | Data layer, stats config, advanced settings | `components/data_layer/`, `components/stats_config/`, `components/ssrm_modal/` | `modules/data_layer/` |

#### 1.1.10–13. Other Monolith Screens

| Screen | Code (Sections) | Description |
|--------|-----------------|-------------|
| Features (Flags) | `sections/features/`, `components/feature_form/` | Feature flag management |
| Idea Builder | `sections/idea_builder/` | AI-powered test idea generation (Opal) |
| Plugin Builder | `sections/plugin_builder/` | Create custom VE plugins/templates |
| Rollouts | `sections/rollouts/` | Feature rollout management |
| Metrics Hub | `sections/metrics_hub/` | Cross-experiment metrics dashboard |
| Profile | `sections/profile/` | User profile settings |
| Live Variables | `sections/live_variables/` | Live variable management |

---

### 3. Features & Code — Visual Editor (Cấp độ 2 + 3)

> **Repo:** `optimizely/visual-editor` | **Base path:** `src/`
> **Tech Stack:** React 18, TypeScript, Zustand, Webpack, Module Federation

#### 1.3.1.1. Variation Row

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Display variation tabs | TabNav showing all experiment variations | `components/variations_list/VariationsList.tsx` | `experimentStore.ts` → `getVariations()` | — |
| Switch variation | Click tab to switch active variation | `VariationsList.tsx` | `experimentStore.ts` → `setVariationIndex()` | — |
| Create new variation | Add variation with name validation + traffic redistribution | `VariationsList.tsx` | `experimentStore.ts`, `services/api/experiments.ts` → `updateExperiment()` | — |
| Save changes on switch | Auto-save pending changes before switching | `VariationsList.tsx` | `changeStore.ts` → `syncChanges()`, `experimentStore.ts` → `savingExperiment()` | — |

**Files:** `components/variations_list/VariationsList.tsx`, `components/variations_list/VariationsList.test.tsx`, `components/variations_list/VariationsList.module.scss`

---

#### 1.3.1.2. Interaction Bar

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Return to experiment | Navigate back to experiment setup page | `components/common/return_link/ReturnLink.tsx` | `utils/editorExit.ts` | — |
| Page switcher | Dropdown to switch pages/views | `components/page_switcher/PageSwitcher.tsx` | `viewStore.ts` → `setViews()`, `experimentStore.ts` → `setViewIndex()`, `services/api/views.ts` → `fetchViews()` | — |
| Device selector | Open popup for mobile/tablet preview | `components/device_selector/DeviceSelector.tsx`, `components/device_selector/Overlay.tsx` | `hooks/useBreakpoints.ts` | — |
| Interactive mode toggle | Alt/Option key to activate element selection | `BottomBar.tsx` | `selectorStore.ts` → `toggleInteractive()` | — |
| Opal CTA button | "Build Variation" AI button | `components/common/opal-chat/OpalCTA.tsx` | `opalChatStore.ts`, `utils/opalChatConfig.ts` | — |
| Variation code editor button | Open full-page code editor | `BottomBar.tsx` | `changeStore.ts` → `createAndSelectCustomCodeChange()` | — |
| Create component button | Create new component | `components/create_component/CreateComponent.tsx` | `changeStore.ts` | — |
| Changes list | Show/manage all changes for current variation | `components/changes/ChangeSelectionBar.tsx`, `components/changes/ChangeOptionsMenu.tsx` | `changeStore.ts` → `changes`, `deleteChange()` | `hooks/useChangeDelete.ts` |
| Attributes button | Open events/tags popup | `components/attribute_list/AttributeList.tsx` | `eventStore.ts` → `events`, `segmentStore.ts` | — |

**Files:** `components/BottomBar.tsx`, `components/BottomBar.test.jsx`, `components/BottomBar.module.scss`

---

#### 1.3.1.3. Code Editor Panel

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Custom JS editor | Monaco editor for variation-level JavaScript | `components/editors/code_editor/CodeEditor.tsx` | `changeStore.ts` → `createAndSelectCustomCodeChange('custom_code')` | — |
| Custom CSS editor | Monaco editor for variation-level CSS | `components/editors/code_editor/CodeEditor.tsx` | `changeStore.ts` → `createAndSelectCustomCodeChange('custom_css')` | — |
| Save/Apply code | Save custom code change | `CodeEditor.tsx` | `changeStore.ts` → `addOrUpdatePendingChange()`, `modules/changes.ts` → `applyChangeToDOM()` | — |

**Files:** `components/editors/code_editor/CodeEditor.tsx`, `CodeEditor.test.tsx`, `CodeEditor.module.scss`

---

#### 1.3.1.4. Element Change Manager

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Selector dropdown | Edit/validate CSS selector for selected element | `components/common/selector-dropdown/SelectorDropdown.tsx` | `selectorStore.ts` → `setSelectorValue()`, `modules/selectorator.ts` → `getSelectorForElement()` | — |
| Selector missing popup | Alert when selector no longer matches DOM | `components/common/selector-missing-popup/SelectorMissingPopup.tsx` | `selectorStore.ts` → `elementCount` | — |
| Name editor | Edit element display name | `components/common/name-editor/NameEditor.tsx` | `changeStore.ts` → `currentlyEditingChange` | — |
| Style manager | Inline CSS editor (Monaco) + class editor | `components/style-manager/StyleManager.tsx` | `changeStore.ts` → `getCssValueFromCurrentlyEditingChange()` | `hooks/useCssPropertyManager.tsx` |
| Background manager | Background color/image editor | `components/background_manager/BackgroundManager.tsx` | `changeStore.ts` → `getCurrentCssValue('background')` | `hooks/useCssPropertyManager.tsx`, `components/common/color-picker/` |
| Border manager | Border width/style/color/radius editor | `components/border_manager/BorderManager.tsx` | `changeStore.ts` → `getCurrentCssValue('border')` | `hooks/useCssPropertyManager.tsx`, `components/common/color-picker/` |
| Dimension manager | Width/height/margin/padding editor | `components/dimension_manager/DimensionManager.tsx` | `changeStore.ts` → `getCurrentCssValue()` | `hooks/useCssPropertyManager.tsx` |
| Layout manager | Visibility, rearrange, position | `components/layout-manager/LayoutManager.tsx` | `changeStore.ts` → `getCurrentCssValue('display')` | `hooks/useCssPropertyManager.tsx` |
| Typography editor | Font family/size/weight/color/alignment | `components/common/typography_editor/TypographyEditor.tsx` | `changeStore.ts` → `getCurrentCssValue('font-*')` | `hooks/useCssPropertyManager.tsx`, `components/common/color-picker/` |
| Timing manager | Async execution + change dependencies | `components/timing_manager/TimingManager.tsx`, `components/common/timing_dropdown/TimingDropdown.tsx` | `changeStore.ts` → `setDependenciesChange()` | `hooks/useTimingDropdown.ts`, `components/common/dependency_change/DependencyChange.tsx` |
| Link editor | Edit hyperlink href/target | `components/common/link-editor/LinkEditor.tsx` | `changeStore.ts` → `getCurrentAttributeValue('href')` | — |
| Image uploader | Upload/change image src | `components/common/image-uploader/ImageUploader.tsx` | `changeStore.ts`, `services/api/editor.ts` → `uploadImage()`, `getImageData()` | — |
| Code editor input | Inline code snippet editor | `components/common/code_editor_input/CodeEditorInput.tsx` | `changeStore.ts` → `setEditingChangeHtml()` | — |
| Dependency change | Manage change dependencies | `components/common/dependency_change/DependencyChange.tsx` | `changeStore.ts` → `dependencies` | — |
| Insert HTML | Insert custom HTML before/after element | `components/editors/insert-html/InsertHTML.tsx` | `changeStore.ts` → `createNewHTMLChange()`, `modules/changes.ts` → `applyInsertHTML()` | `components/common/insert-dropdown/InsertDropdown.tsx` |
| Insert image | Insert image via URL/upload | `components/editors/insert_image/InsertImage.tsx` | `changeStore.ts` → `createNewImageChange()`, `services/api/editor.ts` | `components/common/insert-dropdown/InsertDropdown.tsx` |
| Advanced selector | DOM tree selector picker | `components/common/advanced_selector/AdvancedSelector.tsx` | `selectorStore.ts`, `modules/selectorator.ts` | `components/common/selector-tree/SelectorTree.tsx` |
| Dirty state tracking | Track unsaved property changes | `ElementChangeManager.tsx` | `changeStore.ts` → `setPendingChangeStatus()`, `clearPendingChangeStatus()` | — |
| Duplicate element handling | Handle pending duplicate change | `ElementChangeManager.tsx` | `selectorStore.ts` → `pendingDuplicateChangeId` | — |

**Files:** `components/element_change_manager/ElementChangeManager.tsx` (612 lines, hub component), `ElementChangeManager.test.tsx`, `ElementChangeManager.module.scss`

**Impacts:** All property manager components depend on `changeStore.ts` and `hooks/useCssPropertyManager.tsx`. Changes in `changeStore` state shape affect all managers.

---

#### 1.3.1.5. Event Editor

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Create click event | New event with name, description, selector | `components/event_editor/EventEditor.tsx` | `eventStore.ts` → `addEvent()`, `services/api/events.ts` → `createEvent()` | — |
| Edit existing event | Modify event name/description/selector | `EventEditor.tsx` | `eventStore.ts` → `updateEvent()`, `services/api/events.ts` → `updateEvent()` | — |
| Event selector picker | Select target element for event | `EventEditor.tsx` | `selectorStore.ts` → `setSelectorValue()` | — |
| Archive event | Archive event from editor | `EventEditor.tsx` | `services/api/events.ts` → `updateEvent(event, {archived: true})` | `components/common/archive_event_dialog/ArchiveEventDialog.tsx` |
| Validation | Event name max 400 chars, required fields | `EventEditor.tsx` | — | — |

**Files:** `components/event_editor/EventEditor.tsx`, `EventEditor.test.tsx`, `EventEditor.module.scss`

---

#### 1.3.1.6. Redirect Overlay

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Redirect URL input | Configure redirect destination URL | `components/editors/redirect/Redirect.tsx` | `changeStore.ts` → `createAndSelectRedirectChange()` | — |
| Redirect overlay | Positioning overlay for redirect editor | `components/editors/redirect/Overlay.tsx` | — | — |

**Files:** `components/editors/redirect/Redirect.tsx`, `Redirect.test.tsx`, `Redirect.module.scss`, `Overlay.tsx`, `Overlay.test.tsx`

---

#### 1.3.2. Highlighter

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Hover highlight | Show element boundary on mouse hover | `components/highlighter/hover-overlay/HoverOverlay.tsx` | `highlighterStore.ts`, `modules/selectorator.ts` → `getSelectorForElement()` | — |
| Element action menu | Context menu on click (edit text, styles, etc.) | `components/highlighter/element-action-menu/ElementActionMenu.tsx` | `selectorStore.ts` → `setSelectorValue()`, `changeStore.ts` → `createAndSelectNewChange()` | — |
| Click-to-select | Click element to open Element Change Manager | `components/highlighter/Highlighter.tsx` | `selectorStore.ts` → `setSelectorValue()`, `toggleInteractive()` | `modules/selectorator.ts` |

**Files:** `components/highlighter/Highlighter.tsx`, `Highlighter.module.scss`

---

#### 1.3.3. Attribute List Popup

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Events tab | List all events for current page | `components/attribute_list/AttributeList.tsx` | `eventStore.ts` → `events`, `services/api/events.ts` → `fetchEvents()` | — |
| Select mode | Multi-select events with checkboxes | `AttributeList.tsx` | `eventStore.ts` | — |
| Select All / Deselect All | Batch select/deselect events | `AttributeList.tsx` | — | — |
| Archive events (bulk) | Archive selected events | `AttributeList.tsx` | `services/api/events.ts` → `updateEvent()` (Promise.all) | `components/common/archive_event_dialog/ArchiveEventDialog.tsx` |
| Create event from empty state | Open Event Editor when no events | `AttributeList.tsx` | `eventStore.ts` → `setSelectedEvent()` | — |
| Tags tab | Visual tags placeholder (disabled) | `AttributeList.tsx` | — | — |

**Files:** `components/attribute_list/AttributeList.tsx`, `AttributeList.test.tsx`, `AttributeList.module.scss`

**Dependencies:** `services/api/events.ts` → `GET /api/v1/projects/{projectId}/events?filter=archived:false`

---

#### 1.3.4. Conditional Activation Dialog

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Activation conditions | Set triggers: Clicked, Scrolled, Hovered, Element presence, Exit intent, Time on page | `components/conditional_activation/ConditionalActivation.tsx` | `utils/conditional_activation.ts`, `types/conditional_activation_types.ts` | — |
| Feature flagged | Behind feature flag | `ConditionalActivation.tsx` | `constants.ts` → `FeatureFlags` | — |

**Files:** `components/conditional_activation/ConditionalActivation.tsx`, `ConditionalActivation.test.tsx`, `ConditionalActivation.module.scss`

---

#### 1.3.5. Element Selector Dialog

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Advanced selector UI | Modal with DOM tree + CSS selector input | `components/common/element-selector-dialog/` | `selectorStore.ts` → `selectorDialog`, `openSelectorDialog()`, `closeSelectorDialog()` | `components/common/selector-tree/SelectorTree.tsx`, `components/common/advanced_selector/AdvancedSelector.tsx` |

**Files:** `components/common/element-selector-dialog/ElementSelectorDialog.module.scss`

---

#### 1.3.6. Device Selector Popup

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Device emulation | Open popup window with resized viewport | `components/device_selector/DeviceSelector.tsx` | `hooks/useBreakpoints.ts` | — |
| Device overlay | Overlay showing device frame | `components/device_selector/Overlay.tsx` | — | — |

**Files:** `components/device_selector/DeviceSelector.tsx`, `DeviceSelector.test.tsx`, `DeviceSelector.module.scss`, `Overlay.tsx`, `Overlay.test.tsx`

---

#### 1.3.7. Notification Panel

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Toast notifications | Display success/warning/error toasts | `components/notification_panel/NotificationPanel.tsx` | `notificationStore.ts` | — |
| Auto-dismiss | Notifications auto-dismiss after timeout | `NotificationPanel.tsx` | `notificationStore.ts` | — |

**Files:** `components/notification_panel/NotificationPanel.tsx`, `NotificationPanel.test.tsx`, `NotificationPanel.module.scss`

---

#### 1.3.8. Opal Chat Panel

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| AI chat interface | Federated module — chat with Opal AI | `components/common/opal-chat/lazy_opal_chat.tsx` | `opalChatStore.ts`, `utils/opalChatConfig.ts` | `utils/initFederationReactAndShare.ts` |
| Opal CTA button | "Build Variation" trigger | `components/common/opal-chat/OpalCTA.tsx` | `opalChatStore.ts` | — |
| Opal events | Handle AI-generated changes | `components/common/opal-chat/useOpalEvents.ts` | `changeStore.ts` → `addChange()`, `syncChanges()` | — |
| Opal prompt queue | Queue prompts for processing | `components/common/opal-chat/useOpalPromptQueue.ts` | `opalChatStore.ts` | — |
| Opal preview banner | Preview banner for AI changes | `components/common/opal-chat/OpalPreviewBanner.module.scss` | — | — |

**Files:** `components/common/opal-chat/OpalCTA.tsx`, `lazy_opal_chat.tsx`, `useOpalEvents.ts`, `useOpalPromptQueue.ts`, `constants.ts`

---

#### Template Editor (Sub-screen of Element Change Manager)

| Feature | Description | Code (Components) | Code (Stores/Modules/API) | Shared |
|---------|-------------|-------------------|--------------------------|--------|
| Template selector | Choose from available templates/plugins | `components/editors/template_editor/TemplateSelector.tsx` | `templatesStore.ts`, `services/api/templates.ts` → `fetchTemplates()` | — |
| Template field editor | Edit template fields (text, color, URL) | `components/editors/template_editor/TemplateField.tsx` | — | — |
| Template change editor | Multi-change template editing | `components/editors/template_editor/TemplateChangeEditor.tsx` | `changeStore.ts` | — |
| Template preview | Live preview of template changes | `components/editors/template_editor/TemplateEditor.tsx` | `modules/changes.ts` → `applyChangeToDOM()` | `components/editors/template_editor/helper.ts` |

**Files:** `components/editors/template_editor/TemplateEditor.tsx`, `TemplateSelector.tsx`, `TemplateField.tsx`, `TemplateChangeEditor.tsx`, `helper.ts`

---

### 4. Shared Code Dependencies — Visual Editor

#### Stores (State Management)

| Store | Purpose | Used By |
|-------|---------|---------|
| `stores/changeStore.ts` | Change CRUD, currently editing state, CSS values | ElementChangeManager, all *Manager components, CodeEditor, InsertHTML, Highlighter, OpalEvents |
| `stores/experimentStore.ts` | Experiment data, variations, views, save state | VariationsList, PageSwitcher, BottomBar, CodeEditor |
| `stores/selectorStore.ts` | Selected element, interactive mode, selector dialog | Highlighter, ElementChangeManager, SelectorDropdown, EventEditor |
| `stores/eventStore.ts` | Events list, selected event, loading state | AttributeList, EventEditor |
| `stores/viewStore.ts` | Pages/views, current view | PageSwitcher, BottomBar |
| `stores/authStore.ts` | OAuth tokens, user info | App.tsx (init), API clients |
| `stores/notificationStore.ts` | Toast notification queue | NotificationPanel, EventEditor, AttributeList |
| `stores/highlighterStore.ts` | Hovered element selector | Highlighter, HoverOverlay |
| `stores/opalChatStore.ts` | AI chat state, thread, dock | OpalCTA, lazy_opal_chat, useOpalEvents |
| `stores/segmentStore.ts` | Analytics event tracking | BottomBar, AttributeList, EventEditor |
| `stores/accountStore.ts` | User account info | App.tsx |
| `stores/useProjectStore.ts` | Project data | App.tsx, API clients |
| `stores/templatesStore.ts` | Available templates | TemplateEditor |

#### Modules (Core Logic)

| Module | Purpose | Used By |
|--------|---------|---------|
| `modules/changes.ts` | Apply/revert DOM changes | changeStore, ElementChangeManager, CodeEditor, OpalEvents |
| `modules/selectorator.ts` | Generate CSS selectors from DOM elements | Highlighter, SelectorDropdown, AdvancedSelector |
| `modules/experiments.ts` | Experiment API client | experimentStore |
| `modules/editor_client.js` | Editor initialization & messaging | App.tsx |
| `modules/change_handler.js` | Change application orchestration | changeStore |
| `modules/utils/query_selector.ts` | Safe querySelector wrapper | selectorator, changes |
| `modules/utils/shadow_dom.js` | Shadow DOM utilities | App.tsx, Highlighter |
| `modules/utils/enums.ts` | Shared enums (ChangeTypes, EditorTypes) | changeStore, ElementChangeManager |

#### Services/API

| Service | Endpoints | Used By |
|---------|-----------|---------|
| `services/api/auth.ts` | OAuth2 token management | authStore |
| `services/api/experiments.ts` | `/v2/experiments/*` — fetch, update, save | experimentStore |
| `services/api/events.ts` | `/api/v1/events` — fetch, create, update (archive) | eventStore, AttributeList, EventEditor |
| `services/api/views.ts` | `/api/v1/views` — fetch, update | viewStore |
| `services/api/editor.ts` | Image upload, image metadata | ImageUploader |
| `services/api/templates.ts` | Fetch templates/plugins | templatesStore |
| `services/api/account.ts` | User account info | accountStore |
| `services/api/projects.ts` | Project data | useProjectStore |
| `services/api/client.ts` | Base HTTP client (axios) | All API services |

#### Hooks (Reusable Logic)

| Hook | Purpose | Used By |
|------|---------|---------|
| `hooks/useCssPropertyManager.tsx` | CSS property get/set with change tracking | BackgroundManager, BorderManager, DimensionManager, LayoutManager, StyleManager, TypographyEditor |
| `hooks/useBreakpoints.ts` | Responsive breakpoint detection | DeviceSelector |
| `hooks/useDebounce.ts` | Debounced value updates | SelectorDropdown, search inputs |
| `hooks/useDraggable.ts` | Draggable panel behavior | DraggableCard |
| `hooks/useResizable.ts` | Resizable panel behavior | ElementChangeManager |
| `hooks/useSiteFreeze.ts` | Freeze customer page scroll/interaction | App.tsx |
| `hooks/useElementDragAndDrop.ts` | Drag-and-drop element rearrangement | LayoutManager |
| `hooks/useMenuPosition.ts` | Context menu positioning | ElementActionMenu |
| `hooks/useTimingDropdown.ts` | Timing dropdown state management | TimingManager |
| `hooks/useDependencyChange.ts` | Change dependency management | DependencyChange |

#### Utils (Helpers)

| Util | Purpose | Used By |
|------|---------|---------|
| `utils/dom.ts` | DOM manipulation helpers | changes.ts, selectorator.ts |
| `utils/formatter.ts` | CSS/HTML formatting | StyleManager, CodeEditor |
| `utils/codeTemplates.ts` | Code snippet templates | CodeEditor |
| `utils/helpers.ts` | General utility functions | Multiple components |
| `utils/params.ts` | URL query parameter parsing | App.tsx, viewStore |
| `utils/url.ts` | URL validation/manipulation | Redirect, PageSwitcher |
| `utils/guid.ts` | GUID generation for change IDs | changeStore |
| `utils/variations.ts` | Variation helpers | VariationsList |
| `utils/changeList.ts` | Change list formatting | ChangeSelectionBar |
| `utils/editorExit.ts` | Editor close/exit logic | ReturnLink, BottomBar |
| `utils/conditional_activation.ts` | Conditional activation helpers | ConditionalActivation |
| `utils/eventEmitter.ts` | Custom event emitter | Cross-component communication |
| `utils/rum.ts` | Datadog RUM integration | App.tsx |
| `utils/testUtils.ts` | Test helpers (render, mockFeatureFlag) | All test files |

### 5. Cross-Repo Connection Map

```
optimizely/optimizely (Monolith)                    optimizely/visual-editor (Micro-frontend)
─────────────────────────────────                    ─────────────────────────────────────────
1.1.1 Account Dashboard
  └─ Select project
1.1.2 Optimizations (4 tabs)
  ├─ 1.1.2.1 Overview (all experiments + campaigns)
  ├─ 1.1.2.2 Experiments tab
  │   └─ Click experiment name
  ├─ 1.1.2.3 Personalization Campaigns tab
  │   └─ Click campaign name
  └─ 1.1.2.4 Exclusion Groups tab
1.1.3 Experiment Detail
  ├─ 1.1.3.1 Summary (Review Experiment - Opal AI)
  ├─ 1.1.3.2 Variations
  │   └─ Click variation ──── iframe ────→  1.3.1 Visual Editor (Bottom Bar)
  │       editor_iframe/ loads VE             ├─ 1.3.1.1 Variation Row
  │       via customer website URL            ├─ 1.3.1.2 Interaction Bar
  │       with OAuth token in params          ├─ 1.3.1.4 Element Change Manager
  │                                           ├─ 1.3.2 Highlighter
  │                                           ├─ 1.3.3 Attribute List (Events)
  │                                           └─ 1.3.8 Opal Chat Panel
  ├─ 1.1.3.9 Activation (Target By: Saved Pages / URL)
  ├─ 1.1.3.3 Metrics
  ├─ 1.1.3.4 Audiences
  └─ 1.1.3.5 Results
1.1.5 Campaign Detail
  ├─ 1.1.5.1 Summary
  ├─ 1.1.5.2 Experiences
  │   └─ Edit variation ──── iframe ────→  1.3.1 Visual Editor
  │       "Edit with new editor" / "Edit with legacy editor"
  ├─ 1.1.5.5 Activation
  └─ 1.1.5.6 Metrics
1.1.6 Audiences (Saved / Attributes tabs)
1.1.7 Implementation (Pages / Events / Templates / Catalogs / Recommenders tabs)
1.1.8 History (project-level change log with diff view)
1.1.9 Settings (Implementation / Webhooks / Integrations / JavaScript / Collaborators / Labs / Advanced)
```

**Communication:** Monolith `editor_iframe/` ↔ Visual Editor `editor_client.js` via `postMessage()` API
**Auth:** Monolith passes OAuth token via URL query params → VE stores in `authStore.ts` → `sessionStorage`
**Data:** VE reads/writes experiment data via Frontdoor API (`/v2/experiments/*`) using the same token

### 6. Global UI Elements (Monolith)

| Element | Description | Location |
|---------|-------------|----------|
| **Left sidebar navigation** | Projects, Optimizations, Audiences, Implementation, History, Settings | All monolith pages |
| **Top navigation bar** | Optimizely EXP Product dropdown, Organization selector (Experimentation), "Ask Opal" AI button, Help (?), User avatar | All monolith pages |
| **"Get Test Ideas" button** | Opal AI — generates experiment ideas | Optimizations > Experiments tab, Personalization Campaigns tab |
| **"Variation Development Agent" banner** | Top promotional banner for AI variation building | Campaign Detail > Experiences |
| **"Summarize Variations" button** | AI sparkle icon — generates variation summaries | Campaign Detail > Experiences |
| **"Generate Description" menu** | AI sparkle icon in variation action menu | Campaign Detail > Experiences > Variation (...) menu |
| **"Review Experiment" button** | Opal AI experiment review | Experiment Detail > Summary |
| **Emulate link** | Admin impersonation feature | User profile section in sidebar footer |
| **Sidebar footer links** | Slack Community, Help, Open Desktop App | All monolith pages |
