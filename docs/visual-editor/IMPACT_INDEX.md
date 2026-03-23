# Impact Index — Visual Editor

> **Purpose**: Lookup table for blast radius analysis during ticket review.
> When a ticket mentions a component/file, find its entry here to instantly see what else is impacted.
>
> **Source of truth**: `CLAUDE.md` Section 7 (Functional Tree)
> **Scope**: `optimizely/visual-editor` repo only (Visual Editor micro-frontend)
> **Last Updated**: 2026-03-13

---

## How to Use

1. Find the component/file mentioned in the ticket
2. Read "If changed, impacts" → these are components that need regression testing
3. Read "Critical path" → these are the test flows that must pass
4. Check "Test file" to find existing tests to run
5. Check "Full Flow SCs" → cross-reference with `docs/FULL_FLOW_SPEC.md` Scope Matrix (top of file) to determine which Phases and Checkpoints apply to this ticket (only focus matched phases, skip the rest)

---

## Layer 1: Stores (Highest Impact — State Management)

---

### `stores/changeStore.ts`
- **Type**: Store
- **Purpose**: Central hub for all DOM change CRUD, currently editing state, CSS property values, pending change tracking, undo/redo
- **Key functions**: `applyChange()`, `removeChange()`, `setChanges()`, `syncChanges()`, `addOrUpdatePendingChange()`, `createAndSelectCustomCodeChange()`, `createAndSelectRedirectChange()`, `createNewHTMLChange()`, `createNewImageChange()`, `setPendingChangeStatus()`, `setDependenciesChange()`
- **If changed, impacts**:
  - **Components**: ElementChangeManager, BackgroundManager, BorderManager, DimensionManager, LayoutManager, StyleManager, TypographyEditor, TimingManager, LinkEditor, ImageUploader, CodeEditorInput, InsertHTML, InsertImage, DependencyChange, ChangeSelectionBar, ChangeOptionsMenu, CodeEditor, Redirect
  - **Stores/Hooks**: modules/changes.ts (consumer), hooks/useCssPropertyManager.tsx (all CSS managers)
  - **Opal**: useOpalEvents.ts (addChange, syncChanges)
  - **Variation flow**: VariationsList.tsx (syncChanges on switch)
- **Critical path**: Change Application, Change Persistence, Undo/Redo, Opal Chat Integration
- **Business rules**: Ordered application, unique IDs (GUID via utils/guid.ts), reversible, max 1000 changes/variation
- **Full Flow SCs**: SC-01 (steps 5, 7 — changes applied in preview & live website), SC-07 (interactive mode multi-page changes)
- **Test file**: `stores/changeStore.test.ts`

---

### `stores/experimentStore.ts`
- **Type**: Store
- **Purpose**: Experiment data, variations list, views/pages, save state, variation index
- **Key functions**: `getVariations()`, `setVariationIndex()`, `savingExperiment()`, `setViewIndex()`
- **If changed, impacts**:
  - **Components**: VariationsList.tsx, PageSwitcher.tsx, BottomBar.tsx, CodeEditor.tsx
  - **API**: services/api/experiments.ts (updateExperiment)
- **Critical path**: Change Persistence, Multi-Device Preview
- **Full Flow SCs**: SC-01 (steps 6–7 — publish experiment & snippet push), SC-02 (paused), SC-03 (archived), SC-04 (concluded), SC-05 (concluded & deployed)
- **Test file**: `stores/experimentStore.test.ts`

---

### `stores/selectorStore.ts`
- **Type**: Store
- **Purpose**: Currently selected DOM element, interactive mode toggle, selector dialog state, pending duplicate change
- **Key functions**: `setSelectorValue()`, `toggleInteractive()`, `openSelectorDialog()`, `closeSelectorDialog()`
- **If changed, impacts**:
  - **Components**: Highlighter.tsx, ElementChangeManager.tsx, SelectorDropdown.tsx, EventEditor.tsx, AdvancedSelector.tsx, ElementSelectorDialog
- **Critical path**: Element Selection
- **Full Flow SCs**: SC-07 (interactive mode element selection across pages)
- **Test file**: `stores/selectorStore.test.ts`

---

### `stores/eventStore.ts`
- **Type**: Store
- **Purpose**: Events list for current page, selected event, loading state
- **Key functions**: `addEvent()`, `updateEvent()`, `setSelectedEvent()`
- **If changed, impacts**:
  - **Components**: AttributeList.tsx, EventEditor.tsx
  - **API**: services/api/events.ts
- **Critical path**: Event Tracking
- **Full Flow SCs**: SC-01 (steps 2, 8 — event creation & result page event count)
- **Test file**: `stores/eventStore.test.ts`

---

### `stores/authStore.ts`
- **Type**: Store
- **Purpose**: OAuth2 tokens, user info, token refresh lifecycle
- **Key functions**: `authenticate()`, `refreshToken()`, `getOptiIdToken()`
- **If changed, impacts**:
  - **Init**: App.tsx (authentication on load)
  - **API**: All API services (auth token passed to every request)
- **Critical path**: Authentication
- **Business rules**: Token in query params → sessionStorage, refresh at 55min, 1hr expiry
- **Full Flow SCs**: SC-01 (foundation — required for all API calls across the full flow)
- **Test file**: `stores/authStore.test.ts`

---

### `stores/opalChatStore.ts`
- **Type**: Store
- **Purpose**: AI chat state, thread management, dock/panel visibility
- **If changed, impacts**:
  - **Components**: OpalCTA.tsx, lazy_opal_chat.tsx, useOpalEvents.ts, useOpalPromptQueue.ts
  - **Downstream**: changeStore (AI-generated changes applied via addChange/syncChanges)
- **Critical path**: Opal Chat Integration
- **Test file**: `stores/opalChatStore.test.ts`

---

### `stores/viewStore.ts`
- **Type**: Store
- **Purpose**: Pages/views list, current view selection
- **Key functions**: `setViews()`
- **If changed, impacts**: PageSwitcher.tsx, BottomBar.tsx
- **API**: services/api/views.ts
- **Critical path**: Multi-Device Preview (page switching)
- **Full Flow SCs**: SC-06 (multi-page saved pages), SC-07 (interactive mode page switching)

---

### `stores/notificationStore.ts`
- **Type**: Store
- **Purpose**: Toast notification queue
- **If changed, impacts**: NotificationPanel.tsx, EventEditor.tsx, AttributeList.tsx
- **Critical path**: —

---

### `stores/highlighterStore.ts`
- **Type**: Store
- **Purpose**: Hovered element selector for hover overlay
- **If changed, impacts**: Highlighter.tsx, HoverOverlay.tsx
- **Critical path**: Element Selection

---

### `stores/segmentStore.ts`
- **Type**: Store
- **Purpose**: Analytics event tracking (Segment)
- **If changed, impacts**: BottomBar.tsx, AttributeList.tsx, EventEditor.tsx
- **Critical path**: —

---

### `stores/templatesStore.ts`
- **Type**: Store
- **Purpose**: Available templates/plugins list
- **If changed, impacts**: TemplateEditor.tsx, TemplateSelector.tsx
- **API**: services/api/templates.ts
- **Critical path**: —

---

### `stores/accountStore.ts` / `stores/useProjectStore.ts`
- **Type**: Store
- **Purpose**: User account info, project data
- **If changed, impacts**: App.tsx, all API clients (project context)
- **Critical path**: Authentication

---

## Layer 2: Modules (Core Logic)

---

### `modules/changes.ts`
- **Type**: Module
- **Purpose**: Apply and revert DOM mutations — the engine that writes to the customer website DOM
- **Key functions**: `applyChangeToDOM()`, `applyInsertHTML()`, `applyStyleChange()`
- **If changed, impacts**:
  - **Direct consumers**: changeStore.ts, ElementChangeManager.tsx, CodeEditor.tsx, useOpalEvents.ts, TemplateEditor.tsx
  - **Downstream**: Every visible change on customer page
- **Critical path**: Change Application, Change Persistence
- **Business rules**: XSS-safe (insertAdjacentHTML), inline styles only, silent failure on DOM errors
- **Full Flow SCs**: SC-01 (steps 5, 7 — DOM change application in preview & live), SC-07 (interactive mode changes across pages)
- **Test file**: `modules/changes.test.ts`

---

### `modules/selectorator.ts`
- **Type**: Module
- **Purpose**: Generate unique CSS selectors from DOM elements
- **Key functions**: `getSelectorForElement()`, `isUniqueSelector()`
- **If changed, impacts**:
  - **Direct consumers**: Highlighter.tsx, SelectorDropdown.tsx, AdvancedSelector.tsx, HoverOverlay.tsx
  - **Downstream**: All element selection, all changes that target DOM elements
- **Critical path**: Element Selection
- **Business rules**: Prefer ID → class → nth-child, max 10 levels deep, must be unique in DOM
- **Full Flow SCs**: SC-07 (interactive mode element selection across multiple pages)
- **Test file**: `modules/selectorator.test.ts`

---

### `modules/editor_client.js`
- **Type**: Module
- **Purpose**: Editor initialization and postMessage communication with Monolith
- **If changed, impacts**: App.tsx (init flow), cross-repo communication
- **Critical path**: Authentication (token handshake), all init flows
- **Full Flow SCs**: SC-01 (initialization prerequisite for entire full flow)
- **Note**: This is the bridge between Monolith `editor_iframe/` and Visual Editor

---

### `modules/change_handler.js`
- **Type**: Module
- **Purpose**: Change application orchestration
- **If changed, impacts**: changeStore.ts
- **Critical path**: Change Application

---

### `modules/utils/query_selector.ts`
- **Type**: Module/Util
- **Purpose**: Safe querySelector wrapper (no throw on invalid selector)
- **If changed, impacts**: selectorator.ts, changes.ts
- **Critical path**: Element Selection, Change Application

---

### `modules/utils/enums.ts`
- **Type**: Module/Util
- **Purpose**: Shared enums: ChangeTypes, EditorTypes
- **If changed, impacts**: changeStore.ts, ElementChangeManager.tsx
- **Critical path**: Change Application

---

### `modules/utils/shadow_dom.js`
- **Type**: Module/Util
- **Purpose**: Shadow DOM utilities for UI isolation
- **If changed, impacts**: App.tsx, Highlighter.tsx
- **Critical path**: All (Shadow DOM is the root isolation layer)

---

## Layer 3: Services / API

---

### `services/api/experiments.ts`
- **Type**: Service
- **Purpose**: Fetch and update experiment data
- **Endpoints**: `GET /v2/experiments/{id}`, `PUT /v2/experiments/{id}` (variations, traffic)
- **If changed, impacts**: experimentStore.ts → VariationsList, PageSwitcher, BottomBar, CodeEditor
- **Critical path**: Change Persistence (saving), Authentication
- **Full Flow SCs**: SC-01 (steps 6–7 — publish experiment & snippet push to CDN), SC-02 (paused API), SC-03 (archived API), SC-04 (concluded API), SC-05 (concluded & deployed API)
- **Test file**: `services/api/experiments.test.ts`

---

### `services/api/events.ts`
- **Type**: Service
- **Purpose**: Fetch, create, update (archive) events
- **Endpoints**: `GET /api/v1/projects/{id}/events`, `POST`, `PUT`
- **If changed, impacts**: eventStore.ts → AttributeList.tsx, EventEditor.tsx
- **Critical path**: Event Tracking
- **Full Flow SCs**: SC-01 (steps 2, 8 — event creation & result page event count verification)
- **Test file**: `services/api/events.test.ts`

---

### `services/api/auth.ts`
- **Type**: Service
- **Purpose**: OAuth2 token management, token refresh
- **If changed, impacts**: authStore.ts → App.tsx → All API services
- **Critical path**: Authentication
- **Test file**: `services/api/auth.test.ts`

---

### `services/api/views.ts`
- **Type**: Service
- **Purpose**: Fetch and update pages/views
- **Endpoints**: `GET/PUT /api/v1/views`
- **If changed, impacts**: viewStore.ts → PageSwitcher.tsx, BottomBar.tsx
- **Critical path**: Multi-Device Preview

---

### `services/api/editor.ts`
- **Type**: Service
- **Purpose**: Image upload and metadata
- **If changed, impacts**: ImageUploader.tsx, InsertImage.tsx
- **Critical path**: —

---

### `services/api/templates.ts`
- **Type**: Service
- **Purpose**: Fetch templates/plugins
- **If changed, impacts**: templatesStore.ts → TemplateEditor.tsx
- **Critical path**: —

---

### `services/api/client.ts`
- **Type**: Service
- **Purpose**: Base HTTP client (axios) — auth headers, error handling
- **If changed, impacts**: ALL API services (auth, experiments, events, views, editor, templates, account, projects)
- **Critical path**: Authentication, Change Persistence, all API flows
- **Risk**: Very high — change here breaks all API calls
- **Full Flow SCs**: SC-01 through SC-05 (all status flows depend on API client for every request)

---

## Layer 4: Hooks (Shared Logic)

---

### `hooks/useCssPropertyManager.tsx`
- **Type**: Hook
- **Purpose**: CSS property get/set with changeStore integration and dirty state tracking
- **If changed, impacts**:
  - BackgroundManager, BorderManager, DimensionManager, LayoutManager, StyleManager, TypographyEditor
  - (All 6 CSS property manager components)
- **Critical path**: Change Application (CSS changes)

---

### `hooks/useBreakpoints.ts`
- **Type**: Hook
- **Purpose**: Responsive breakpoint detection
- **If changed, impacts**: DeviceSelector.tsx
- **Critical path**: Multi-Device Preview

---

### `hooks/useDebounce.ts`
- **Type**: Hook
- **Purpose**: Debounced value updates (prevents excessive re-renders/API calls)
- **If changed, impacts**: SelectorDropdown.tsx, all search inputs
- **Critical path**: Element Selection

---

### `hooks/useElementDragAndDrop.ts`
- **Type**: Hook
- **Purpose**: Drag-and-drop element rearrangement in DOM
- **If changed, impacts**: LayoutManager.tsx
- **Critical path**: Change Application (layout changes)

---

### `hooks/useTimingDropdown.ts`
- **Type**: Hook
- **Purpose**: Timing dropdown state management
- **If changed, impacts**: TimingManager.tsx, TimingDropdown.tsx
- **Critical path**: Change Application (async timing)

---

### `hooks/useSiteFreeze.ts`
- **Type**: Hook
- **Purpose**: Freeze customer page scroll/interaction during editing
- **If changed, impacts**: App.tsx
- **Critical path**: All (UX baseline)

---

## Layer 5: Key Components (UI)

---

### `components/element_change_manager/ElementChangeManager.tsx`
- **Type**: Component (Hub — 612 lines)
- **Purpose**: Right panel hub when element is selected — renders all property managers
- **If changed, impacts**:
  - BackgroundManager, BorderManager, DimensionManager, LayoutManager, StyleManager, TypographyEditor, TimingManager, LinkEditor, ImageUploader, InsertHTML, InsertImage, SelectorDropdown, NameEditor, AdvancedSelector
- **Depends on**: changeStore, selectorStore, hooks/useCssPropertyManager.tsx
- **Critical path**: Change Application, Element Selection
- **Full Flow SCs**: SC-01 (step 5 — apply changes via VE), SC-07 (interactive mode cross-page element editing)
- **Test file**: `ElementChangeManager.test.tsx`

---

### `components/highlighter/Highlighter.tsx`
- **Type**: Component
- **Purpose**: Hover/click overlay on customer page for element selection
- **If changed, impacts**: HoverOverlay.tsx, ElementActionMenu.tsx
- **Depends on**: selectorStore, highlighterStore, modules/selectorator.ts
- **Critical path**: Element Selection
- **Full Flow SCs**: SC-01 (step 5 — element selection in VE for applying changes), SC-07 (interactive mode element hover/click across pages)
- **Test file**: `highlighter.test.tsx`

---

### `components/variations_list/VariationsList.tsx`
- **Type**: Component
- **Purpose**: Variation tabs — switch between experiment variations
- **If changed, impacts**: Save flow (syncChanges on tab switch)
- **Depends on**: experimentStore, changeStore
- **Critical path**: Change Persistence (auto-save on switch)
- **Full Flow SCs**: SC-01 (step 5 — variation switching while editing), SC-06 (multi-page variation behavior)
- **Test file**: `VariationsList.test.tsx`

---

### `components/BottomBar.tsx`
- **Type**: Component (Root UI container)
- **Purpose**: Main editor container — always visible, renders all sub-panels
- **If changed, impacts**: All VE UI (it's the shell)
- **Depends on**: changeStore, selectorStore, experimentStore, viewStore, segmentStore
- **Critical path**: All
- **Full Flow SCs**: SC-01 (all VE interactions), SC-07 (interactive mode toggle), SC-08 (Enable Support for Dynamic Websites setting)
- **Test file**: `BottomBar.test.jsx`

---

### `components/common/opal-chat/useOpalEvents.ts`
- **Type**: Hook/Component
- **Purpose**: Handle AI-generated changes from Opal Chat and apply to changeStore
- **If changed, impacts**: changeStore (addChange, syncChanges) → DOM
- **Depends on**: opalChatStore, changeStore, modules/changes.ts
- **Critical path**: Opal Chat Integration
- **Test file**: `opalChatStore.test.ts`

---

### `components/attribute_list/AttributeList.tsx`
- **Type**: Component
- **Purpose**: Events/tags popup — list, select, archive events
- **If changed, impacts**: Event archive flow (bulk operations)
- **Depends on**: eventStore, services/api/events.ts, notificationStore, segmentStore
- **Critical path**: Event Tracking
- **Full Flow SCs**: SC-01 (step 2 — events list for page)
- **Test file**: `AttributeList.test.tsx`

---

### `components/event_editor/EventEditor.tsx`
- **Type**: Component
- **Purpose**: Create/edit individual click events with selector
- **If changed, impacts**: eventStore, services/api/events.ts
- **Depends on**: eventStore, selectorStore, notificationStore, segmentStore
- **Critical path**: Element Selection, Event Tracking
- **Full Flow SCs**: SC-01 (steps 2, 8 — event creation & result page event tracking)
- **Test file**: `EventEditor.test.tsx`

---

### `components/device_selector/DeviceSelector.tsx`
- **Type**: Component
- **Purpose**: Multi-device preview popup
- **If changed, impacts**: Overlay.tsx
- **Depends on**: hooks/useBreakpoints.ts
- **Critical path**: Multi-Device Preview
- **Test file**: `DeviceSelector.test.tsx`

---

### `components/page_switcher/PageSwitcher.tsx`
- **Type**: Component
- **Purpose**: Page/view switcher dropdown in Interaction Bar
- **Depends on**: viewStore, experimentStore, services/api/views.ts
- **Critical path**: Multi-Device Preview, page-level changes
- **Full Flow SCs**: SC-06 (multi-page saved pages), SC-07 (interactive mode cross-page element selection)

---

### `components/editors/code_editor/CodeEditor.tsx`
- **Type**: Component
- **Purpose**: Monaco editor for custom JS/CSS per variation
- **Depends on**: changeStore, modules/changes.ts
- **Critical path**: Change Application (custom code)
- **Test file**: `CodeEditor.test.tsx`

---

### `components/conditional_activation/ConditionalActivation.tsx`
- **Type**: Component
- **Purpose**: Set activation conditions (Click, Scroll, Hover, etc.)
- **Depends on**: constants.ts (FeatureFlags), utils/conditional_activation.ts
- **Critical path**: Feature flag gated
- **Test file**: `ConditionalActivation.test.tsx`

---

### `components/editors/template_editor/TemplateEditor.tsx`
- **Type**: Component
- **Purpose**: Template/plugin selector and field editor
- **Depends on**: templatesStore, services/api/templates.ts, changeStore, modules/changes.ts
- **Critical path**: Change Application (template-based changes)

---

### `components/variations_list/MVTSectionsEditor.tsx` (Inferred)
- **Type**: Component
- **Purpose**: MVT Sections tab editor — manage section-based variation groups, display Total Combinations counter (current / Max: 64)
- **Depends on**: experimentStore, changeStore, services/api/experiments.ts (endpoint: `/v2/experiments/sections/{sectionId}`)
- **Related screenshots**: UI_Screenshots_Analysis.md #31, #32
- **UI elements**: "Create New Section..." button, section list, Total Combinations counter, orange dot indicator (CHANGED badge)
- **Critical path**: Change Application (MVT-specific)
- **Note**: MVT uses different API endpoint (`/v2/experiments/sections/{sectionId}`) vs A/B/MAB (`/v2/experiments/{id}`)

---

### `components/variations_list/MVTCombinationsTab.tsx` (Inferred)
- **Type**: Component
- **Purpose**: MVT Combinations tab — display auto-generated combinations (AA, AB, AC...) from all sections
- **Depends on**: experimentStore, services/api/experiments.ts
- **Related screenshots**: UI_Screenshots_Analysis.md #33
- **UI elements**: Combinations list (name + description + Traffic Allocation %), Combination action menu (...): Preview
- **Critical path**: Change Application (MVT preview)
- **Business rule**: Combinations auto-generated from sections, max 64 combinations total

---

### `components/LeftSidebarNavigation.tsx` (Inferred)
- **Type**: Component
- **Purpose**: Left sidebar navigation panel with 5 collapsible sections (Target, Design, Track, Plan, Settings)
- **Related screenshots**: UI_Screenshots_Analysis.md #32
- **Structure**:
  - **Target**: Activation, Audiences
  - **Design**: Variations (with CHANGED badge), Shared Code, Traffic Allocation, Stats Configuration
  - **Track**: Metrics (info icon), Integrations
  - **Plan**: Schedule, Summary
  - **Settings**: API Names, History
- **UI elements**: Collapsible sections, CHANGED badge indicator on Variations item
- **Depends on**: experimentStore, changeStore
- **Critical path**: Navigation, feature discoverability

---

### `components/variations_list/VariationOrangeDotIndicator.tsx` (Inferred)
- **Type**: Component
- **Purpose**: Visual indicator (orange dot) on variations/combinations that have pending changes
- **Related screenshots**: UI_Screenshots_Analysis.md #31, #32, #33
- **Depends on**: changeStore (list of pending changes per variation)
- **UI context**: Appears on variation row, combination row, and "CHANGED" badge on Variations sidebar item
- **Critical path**: Change tracking, UI feedback

---

## Layer 6: Utils (Helpers)

---

### `utils/testUtils.ts`
- **Type**: Util
- **Purpose**: Test helpers — `render()` wrapper, `mockFeatureFlag()`
- **If changed, impacts**: ALL test files
- **Critical path**: Testing infrastructure
- **Risk**: Change here breaks all unit tests

---

### `constants.ts`
- **Type**: Config
- **Purpose**: App constants including FeatureFlags enum
- **If changed, impacts**: Any component behind a feature flag, useFeatureFlag hook consumers
- **Critical path**: Feature flag gated features (ConditionalActivation, etc.)
- **Full Flow SCs**: SC-08 (Enable Support for Dynamic Websites — controlled via feature flag/setting in constants)

---

### `utils/guid.ts`
- **Type**: Util
- **Purpose**: GUID generation for change IDs
- **If changed, impacts**: changeStore.ts (every new change gets a GUID)
- **Business rule**: Change IDs must be unique — GUID collision = data corruption

---

### `utils/dom.ts`
- **Type**: Util
- **Purpose**: DOM manipulation helpers
- **If changed, impacts**: modules/changes.ts, modules/selectorator.ts
- **Critical path**: Change Application, Element Selection

---

### `utils/formatter.ts`
- **Type**: Util
- **Purpose**: CSS/HTML formatting
- **If changed, impacts**: StyleManager.tsx, CodeEditor.tsx

---

### `utils/editorExit.ts`
- **Type**: Util
- **Purpose**: Editor close/exit logic
- **If changed, impacts**: ReturnLink.tsx, BottomBar.tsx
- **Critical path**: Session cleanup

---

### `utils/rum.ts`
- **Type**: Util
- **Purpose**: Datadog RUM integration for monitoring
- **If changed, impacts**: App.tsx (init)

---

## Critical Path Summary

| Path | Key Files (in order of flow) |
|------|------------------------------|
| **Change Application** | Highlighter → selectorStore → ElementChangeManager → useCssPropertyManager → changeStore → changes.ts → Customer DOM |
| **Change Persistence** | changeStore.saveChanges → services/api/experiments.ts → Frontdoor API |
| **Element Selection** | Highlighter → selectorator.ts → selectorStore → ElementChangeManager |
| **Authentication** | App.tsx → services/api/auth.ts → authStore → sessionStorage → all API services |
| **Opal Chat** | OpalCTA → opalChatStore → lazy_opal_chat → useOpalEvents → changeStore → changes.ts → DOM |
| **Multi-Device Preview** | DeviceSelector → useBreakpoints → Overlay (popup window) |
| **Change Undo/Redo** | BottomBar → changeStore.undo/redo → changes.ts → DOM |
| **MVT Sections** (screenshot #31, #32) | MVTSectionsEditor → experimentStore → services/api/experiments.ts (endpoint: `/v2/experiments/sections/{sectionId}`) → LeftSidebarNavigation shows CHANGED badge |
| **MVT Combinations Preview** (screenshot #33) | MVTCombinationsTab → experimentStore → services/api/experiments.ts → Preview action |

---

## Quick Blast Radius by Ticket Type

| Ticket mentions... | Check these files |
|--------------------|------------------|
| CSS property / style | changeStore, useCssPropertyManager, BackgroundManager/BorderManager/DimensionManager/LayoutManager/StyleManager/TypographyEditor, changes.ts |
| Selector / element picking | selectorStore, selectorator.ts, Highlighter, SelectorDropdown, AdvancedSelector |
| Save / persist changes | changeStore (syncChanges), services/api/experiments.ts, experimentStore |
| Event tracking | eventStore, EventEditor, AttributeList, services/api/events.ts |
| Opal / AI | opalChatStore, useOpalEvents, OpalCTA, changeStore |
| Auth / token | authStore, services/api/auth.ts, services/api/client.ts, App.tsx |
| Feature flag | constants.ts, useFeatureFlag, ConditionalActivation |
| Image / upload | ImageUploader, InsertImage, services/api/editor.ts, changeStore |
| Redirect | Redirect.tsx, Overlay.tsx, changeStore |
| Template | TemplateEditor, templatesStore, services/api/templates.ts |
| Timing / async | TimingManager, TimingDropdown, useTimingDropdown, changeStore |
| Device / responsive | DeviceSelector, useBreakpoints, Overlay |
| Notification / toast | notificationStore, NotificationPanel |
| Code editor (JS/CSS) | CodeEditor, changeStore, changes.ts |
| MVT sections / combinations | experimentStore, services/api/experiments.ts (endpoint: `/v2/experiments/sections/{sectionId}`), MVTSectionsEditor, MVTCombinationsTab |
| Left sidebar navigation | LeftSidebarNavigation, experimentStore, changeStore (CHANGED badge tracking) |
| Orange dot indicator | VariationOrangeDotIndicator, changeStore |

---

## Monolith Screen References — MVT Specific (from Screenshots #31-33)

### Design > Variations (MVT — Sections tab)

**URL pattern:** `.../experiments/{id}/variations?tab=sections`

**UI observed (Screenshot #31, #32):**
- Left sidebar navigation visible with 5 collapsible sections: Target, Design (Variations with CHANGED badge), Track, Plan, Settings
- Main tab area: "Variations" section with 2 tabs → **Sections tab** (active)
- Sections list: Section name + Section editor interface
- **"Create New Section..."** button
- **Total Combinations counter**: "4" (current) / "Max: 64"
- Per-variation action menu (...): Rename, Delete, Generate Description (AI sparkle)
- **"Summarize Variations"** AI button
- **Upload** button in Screenshot column per variation
- Orange dot indicator on variations/sections with CHANGED status
- **CHANGED badge** on Variations nav item (left sidebar) when modifications exist

**Correct Expected Result format:**
> "Experiment Detail > Variations (Sections tab): 'Section 1' appears with Total Combinations showing '4 / Max: 64'"

---

### Design > Variations (MVT — Combinations tab)

**URL pattern:** `.../experiments/{id}/variations?tab=combinations`

**UI observed (Screenshot #33):**
- Main tab area: "Variations" section with 2 tabs → **Combinations tab** (active)
- Combinations list: Auto-generated from all sections (AA, AB, AC, BB, etc.)
- Columns per combination: Combination name + description (auto-generated) + Traffic Allocation % (editable)
- Per-combination action menu (...): Preview
- Orange dot indicator on combinations with CHANGED status

**Critical fact:** Combinations are **auto-generated from sections**, not manually created

**Correct Expected Result format:**
> "Experiment Detail > Variations (Combinations tab): Combination 'AB' appears with auto-generated description and traffic % field"

---

### Settings > API Names — Variations (MVT section)

**Note:** Same as A/B experiments (screenshot #15 reference in UI_Screenshots_Analysis.md)
- Variations listed by NAME + numeric ID
- **NO snake_case API names for variations** — only Events and Pages have snake_case
- Example: "Section 1" → ID: 4677512966438912

---

## Global Context & Side-Effects

> **Scope**: Cross-repo — Visual Editor (`optimizely/visual-editor`), Monolith (`optimizely/optimizely`), Opal Tools (`opal-tools`)
> **Last Updated**: 2026-03-23

### Visual Editor — Browser Globals

| Global / API | Defined In | Purpose | Side-Effects | Interacts With |
|---|---|---|---|---|
| `window.optimizely` | Customer website (snippet) | Optimizely SDK object — provides `get('utils')`, `get('client-change-applier')` | Read-only from VE; used to apply changes via `change_handler.js` | `modules/change_handler.js`, `modules/changes.ts` |
| `window.React` / `window.ReactDOM` | `utils/initFederationReactAndShare.ts` | Shared via Module Federation (`provideToShareScope`) — prevents duplicate React instances | Overrides customer site React if not already present; may conflict if customer already has React | `lazy_opal_chat.tsx`, Module Federation config |
| `window.requestIdleCallback` | `App.tsx` | Mounts VE render root with 2s timeout fallback | Polyfilled if absent; delays VE mount on low-power devices | `App.tsx` (init) |
| `window.sessionStorage` | `services/api/auth.ts` | Stores OAuth2 token after handshake | Token persists across page navigations within session; cleared on browser close | `authStore.ts`, all API services |
| `window.localStorage` | `components/common/opal-chat/` | Stores Opal Chat URLs (endpoint config) | Persists across sessions; stale URLs cause Opal to fail silently | `opalChatStore.ts`, `lazy_opal_chat.tsx` |
| `window.dispatchEvent` | Multiple VE components | Custom events: Opal response events, VE lifecycle events | Fires cross-component events that bypass React state — hard to trace in tests | `useOpalEvents.ts`, `useOpalPromptQueue.ts` |
| `window.getComputedStyle` | `modules/changes.ts`, style managers | Reads computed CSS values from customer DOM | Read-only; fails silently if element removed from DOM | `StyleManager`, `BackgroundManager`, `BorderManager` |
| `window.scrollTo` / `window.scrollY` | `hooks/useDraggable.ts`, element scroll | Scrolls customer page during element drag / selector targeting | Modifies customer page scroll position directly | `LayoutManager`, element targeting |
| `window.screen` | `components/device_selector/Overlay.tsx` | Positions device preview popup window | Opens new browser window — blocked by popup blockers | `DeviceSelector.tsx` |
| `#opti-frozen-styles` (DOM element) | `hooks/useSiteFreeze.ts` | Injects `<style>` tag to freeze customer page scroll/interaction | Mutates customer page `<head>` — may conflict with customer CSS | `App.tsx` (useSiteFreeze) |
| Shadow DOM root (`#optimizely-editor`) | `App.tsx` | Isolates VE UI from customer page styles | Creates Shadow DOM boundary — some CSS selectors fail across boundary | All VE UI components |

### Monolith — Browser Globals & postMessage

| Global / API | Defined In | Purpose | Side-Effects | Interacts With |
|---|---|---|---|---|
| `window.postMessage` | `modules/editor_iframe/` | Sends messages from Monolith to VE iframe | Cross-origin; origin must match — mismatch causes silent failure | `modules/editor_client.js` (VE receiver) |
| `window.postMessage` (VE → Monolith) | `modules/editor_client.js` | VE sends save/exit/status back to Monolith | Async — Monolith must be listening; missed messages = UI out of sync | `editor_iframe_store.js` (Monolith receiver) |

### Opal Tools — Server-Side Side-Effects

| Function / Endpoint | File | Purpose | Side-Effects | Interacts With |
|---|---|---|---|---|
| `POST /interactions/save-changes` | `src/` interaction handlers | Opal applies AI-generated changes to experiment variation | Writes directly to Frontdoor API — bypasses VE change validation | `changeStore.ts` (VE applies result), `services/api/experiments.ts` |
| `POST /api/v1/query` | OpenSearch query engine | Queries experiment/analytics data for AI context | Read-only; slow queries timeout silently | Opal chat context builder |
| `POST /interactions/design-improvement` | Opal agent | AI generates HTML/CSS variation changes | Returns code injected via `applyInsertHTML()` — XSS risk if not sanitized | `modules/changes.ts` (`insertAdjacentHTML`) |
| `POST /interactions/flag-variation` / `flag-variable` | Opal agent | AI suggests feature flag variation values | Modifies flag data via Frontdoor API | FX repo, Experimentation Client |
| `POST /interactions/refined-test-idea` | Opal agent | AI generates A/B test ideas | Read-only suggestions | Idea Builder (Monolith) |
| WebSocket `/ws` | `src/` websocket handler | Real-time Opal chat streaming | Keeps connection alive; reconnect on drop may duplicate messages | `lazy_opal_chat.tsx`, `useOpalPromptQueue.ts` |
| BigQuery program reporting | `src/` analytics | Queries experiment results for AI summaries | External GCP dependency; failures degrade Summarize Variations feature | Monolith Results page |

---

## DOM Interaction Map

> **Scope**: Selectors actively written, read, or mutated by VE codebase on customer website DOM.

| Selector / Element | Operation | Module / Component | Risk | Notes |
|---|---|---|---|---|
| `[data-optly-{changeId}]` | Add attribute → Read → Remove | `modules/changes.ts` | Medium | Marks currently editing element; persists if VE crashes mid-edit |
| `[data-optly-{changeId}-rearrange]` | Add → Remove | `modules/changes.ts` | Medium | Marks rearranged element; cleanup required after undo |
| `#opti-frozen-styles` | Create `<style>` → Remove | `hooks/useSiteFreeze.ts` | High | Injected into customer `<head>` — conflicts with customer CSS resets or CSP |
| `#${rootId}` (Shadow DOM host) | Create → Mount React app | `App.tsx` | Critical | VE root; removal = full editor crash |
| `host.shadowRoot#${bottomBarId}` | Read height | `BottomBar.tsx` | Low | Used for layout calculation; fails gracefully if null |
| `#${changeListDropdownId}` | Read (click-outside detection) | `BottomBar.tsx` | Low | Closes dropdown on outside click |
| Dynamic user selector (from `selectorator.ts`) | Read (querySelectorAll) | `modules/selectorator.ts`, `modules/changes.ts` | High | Applies all changes on page load; invalid selector = silent skip |
| `document` (via `insertAdjacentHTML`) | Insert HTML before/after/replace | `modules/changes.ts` (`applyInsertHTML`) | Critical | XSS vector if HTML not sanitized; affects all elements matching selector |
| Inline `style` attribute on matched elements | Set / Remove | `modules/changes.ts` (`applyStyleChange`) | Medium | Overrides customer inline styles; not reversible without VE undo |
| `window` (custom events) | `dispatchEvent` | `useOpalEvents.ts`, VE lifecycle | Medium | Event names must be unique to avoid collision with customer site events |

---

## Experiment Interaction Matrix

> **Scope**: Cross-repo interaction pairs — VE ↔ Monolith ↔ Opal. Identifies conflict zones for QA regression.

| Interaction Pair | Type | Conflict Scenario | Severity | Test Strategy |
|---|---|---|---|---|
| **VE change apply** ↔ **Opal save-changes** | Race condition | User edits element in VE while Opal simultaneously POSTs `/interactions/save-changes` → `changeStore` receives two conflicting change sets | High | Test: Apply manual change, trigger Opal change same element, verify last-write-wins and no duplicate changes |
| **window.React (VE)** ↔ **Customer site React** | Module Federation conflict | Customer site already loads React; VE `provideToShareScope` overwrites `window.React` → customer React components re-render or break | High | Test: Load VE on customer site with React; verify customer components still render after VE mount |
| **window.optimizely.get()** ↔ **Snippet load timing** | Timing / null ref | VE `change_handler.js` calls `window.optimizely.get('client-change-applier')` before snippet finishes loading → `TypeError: Cannot read properties of undefined` | Critical | Test: Slow network snippet load; verify VE handles null gracefully |
| **postMessage (Monolith → VE)** ↔ **CSP policy** | Origin mismatch | Customer site CSP blocks iframe postMessage from Monolith origin → VE never receives init token → auth fails | Critical | Test: Customer site with strict CSP; verify error message shown (CJS-11056 CSP detection) |
| **sessionStorage token** ↔ **Opal save-changes** | Auth expiry | OAuth token expires during long Opal session (>55 min); `save-changes` POST returns 401 → changes lost | High | Test: Mock token expiry mid-Opal session; verify retry or user prompt shown |
| **#opti-frozen-styles** ↔ **Customer CSS animations** | DOM mutation conflict | VE injects `overflow: hidden` freeze style → customer page CSS animations/transitions freeze mid-state | Medium | Test: Customer page with CSS scroll animations; verify VE freeze/unfreeze restores state |
| **selectorator.ts selector** ↔ **Dynamic customer DOM** | DOM instability | Customer page re-renders via SPA framework (React/Vue/Angular) after VE generates selector → selector no longer matches → change not applied | High | Test: SPA customer site (React Router); navigate between pages, verify changes persist on correct elements |
| **insertAdjacentHTML** ↔ **Customer site scripts** | XSS / script injection | HTML change contains `<script>` tag → inserted into customer DOM → executes in customer context | Critical | Test: Attempt to insert `<script>alert(1)</script>` via InsertHTML editor; verify blocked or sanitized |
| **VE undo/redo** ↔ **Opal-applied changes** | State mismatch | User undoes Opal-generated change after VE applies it → `changeStore` removes change but Opal `save-changes` already persisted to API → UI and API out of sync | High | Test: Opal applies change → user undoes → verify API synced (change removed from variation) |
| **window.localStorage (Opal URLs)** ↔ **Environment switch** | Stale config | QA switches from `inte` to `prep` environment; localStorage retains old Opal URL → Opal connects to wrong environment | Medium | Test: Switch environment; verify Opal Chat connects to correct endpoint |
| **Shadow DOM VE root** ↔ **Customer site document.querySelector** | Selector isolation | Customer site analytics script calls `document.querySelector('.opti-*')` → fails to find VE elements inside Shadow DOM → analytics events not fired | Low | Test: Customer site with analytics selectors for VE elements; verify graceful miss |
| **MVT sections API** (`/sections/{id}`) ↔ **VE changeStore** | Wrong endpoint | A/B experiment logic accidentally calls A/B endpoint for MVT section change → 404 or wrong data written | High | Test: MVT experiment; verify all changes use `/v2/experiments/sections/{sectionId}` not `/v2/experiments/{id}` |
| **Opal WebSocket** ↔ **VE page navigation** | Connection drop | User switches page in VE (PageSwitcher) during active Opal streaming → WebSocket drops → partial AI response applied | Medium | Test: Start Opal generation → switch page mid-stream → verify no partial/corrupt changes applied |
