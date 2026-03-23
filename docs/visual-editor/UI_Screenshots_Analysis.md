# UI Screenshots Analysis — Functional Tree Gap Assessment

**Date**: 2026-03-13
**Analyst**: Senior QA Lead
**Purpose**: Compare actual UI screenshots against Functional Tree (CLAUDE.md Section 8) to identify missing screens, features, and user flows.

---

## Screenshots Catalog

| # | Screen | Key UI Elements Observed |
|---|--------|------------------------|
| 1 | Edit Basic Snippet (Dialog) | Key field, Snippet Details, Visitor ID, jQuery Inclusion, Privacy settings, Cache Expiration TTL, Dynamic Websites, Trim Unused Pages, Shadow DOM, Cross-Origin Tracking, Optimizely X config |
| 2 | Settings > Implementation tab | Snippet list table (Name, Projects, ID, Revision, Size), Basic + Custom snippets, "Create Custom Snippet..." button |
| 3 | History page | Search by type:ID, Type/Date/Source filters, Change Summary table with user + time, "Hide/Show details" toggle, Diff view (before/after with line numbers and +/- highlighting) |
| 4 | Implementation > Catalogs > New Catalog dialog | Name, Description, Catalog Events (search + add page views), Assign Event Tags (Primary ID, Source URL), Indexing Rate (5000/min default) |
| 5 | Implementation > Templates tab | Template list (Name, Template Type, Optimizations, ID), Status + Creator filters, "Create Template..." dropdown: Duplicate existing / Use JSON / Use Editor |
| 6 | Implementation > Events > Create New Event dialog | Event type: Click / Custom / Pageview, Page selector (for Click type), "Create Event" button |
| 7 | Implementation > Events tab | Events grouped by Page, columns: Name, API Name, Experiments, ID, Type, Action menu (...): Settings / View Experiment Usage / Archive, Status filter, "Create New Event" button |
| 8 | Implementation > Pages > New Page dialog | Name, Editor URL, Description, Page Settings (Triggers dropdown, Conditions with URL Match), Advanced section (Deactivation and Undo, Override Page Trimming), Test URL(s) |
| 9 | Implementation > Pages tab | Page list (Name, API Name, ID, Experiments, Events, Tags), Status filter, "Create New Page" button, Action menu (...): Edit Page / View Experiment Usage / Archive |
| 10 | Audiences > Saved tab | Audience list (Name, Experiments, ID, Created, Modified), Status filter, "Create New Audience..." button, Action menu (...): View Experiment Usage / Archive |
| 11 | Create New Audience page | Name, Description, Audience Conditions (drag-and-drop), Code Mode toggle, Condition categories: Adaptive / Custom Attributes / Real-Time Segments (NEW!) / External Attributes / Visitor Behaviors / Standard (Ad Campaign, Browser, Cookie, Custom Javascript, Device, IP Address, Language, Location, New/Returning Session, Platform, Query Parameters, Referrer URL, Time/Day of Visit, Traffic Source) |
| 12 | Experiment Detail > Activation | Target By (Saved Pages / URL), page browser with search, "Create New Page" inline, Edit buttons per page, Revert/Save buttons |
| 13 | Experiment Detail > Summary | Collapsible sections: Activation (Target by, Pages), Audiences (Match Type), Variations (Original %, Variation #1 %, Stats Accelerator), Shared Code, Traffic Allocation (Distribution mode, Portion of visitors), Metrics (Primary), Stats Configuration, Integrations, Schedule. "Review Experiment" Opal button, Download icon |
| 14 | Optimizations > Experiments tab | Experiment list (Name, Type, Status, Primary Metric, Variations, Results), Status/Type filters, "Get Test Ideas" + "Create..." buttons, Action menu (...): Duplicate / Pause / Archive / Conclude, Results dropdown, Pagination |
| 15 | Optimizations > Overview tab + Show/Hide Columns panel | Combined exp+campaign list, column toggle panel: Name, Type, Status, Creator, Modified, First Published, Last Paused, Last Published, Primary Metric, Days Running, Variations, Pages, Audiences, Targeting Method, Experiment ID, Traffic Allocation, Distribution Mode, Results, Results Outcome, Journey |
| 16 | Optimizations > Overview tab (default) | Combined view with "Create..." dropdown, "Get Test Ideas" button, Action menus, "..." column toggle icon |
| 17 | Optimizations > Exclusion Groups > Create Exclusion Group dialog | Exclusion Group Name, Description, Experiments browser (search + add) |
| 18 | Campaign Detail > Experiences (status dropdown) | Status dropdown: Run / Conclude / Archive |
| 19 | Campaign Detail > Experiences (Edit dropdown) | Edit dropdown: "Edit with new editor" / "Edit with legacy editor" |
| 20 | Campaign Detail > Experiences (variation action menu) | Variation (...) menu: Rename / Duplicate / Generate Description (AI sparkle icon) |
| 21 | Campaign Detail > Experiences (experience action menu) | Experience (...) menu: Publish... / Settings... / Manage Schedule... / Duplicate... / Pause / Archive |
| 22 | Campaign Detail > Experiences (default view) | Experience list with Holdback + Variations, Total Traffic %, Preview/Upload/View/Edit buttons, "Summarize Variations" AI button, UNPUBLISHED badge, CAMPAIGN PAUSED status, "Add Variation..." link |
| 23 | Campaign Detail > Summary | Collapsible sections: Experiences (Holdback %, Variation %, Stats Accelerator), Activation (Target by, Pages), Integrations, Metrics (Primary + Secondary), Shared Code. Download icon |
| 24 | Optimizations > Personalization Campaigns tab | Campaign list (Name, Status, Primary Metric, Audiences, Results), "Create Personalization Campaign" button, "Get Test Ideas" button, Action menu (...): Duplicate / Start / Archive / Conclude |
| 25 | Optimizations > Overview tab (action menu) | Action menu (...): Duplicate / Start / Archive / Conclude |
| 26 | Optimizations > Experiments tab (clean view) | Clean experiment list with pagination (1-7 pages), columns: Name, Type, Status, Modified, Results |
| 27 | Campaign > Create New Experience dialog | Experience Name (optional), Audience (Everyone), Variations section: Distribution Mode (Manual/Auto), Variation names, Traffic Distribution %, Total Traffic %, "Add Variation", Holdback recommendation warning |
| 28 | Campaign > Prioritize Experiences dialog | Priority number, Experience name (drag to reorder), Traffic Percentage (Auto/manual) |
| 29 | Campaign Detail > Experiences (default, another view) | Same as #22 with Summarize Variations button, Edit dropdown |
| 30 | Create New Experience > Distribution Mode dropdown | 4 options: Manual, Automation section (Contextual Bandit, Multi-armed Bandit, Stats Accelerator), Holdback warning, "Advanced code editor" button |
| 31 | Experiment Detail > Variations (MVT) — Sections tab | Multivariate Test, 2 tabs (Sections/Combinations), "Create New Section...", Total Combinations: 4 Max: 64, Variation action menu (Rename/Delete/Generate Description AI), "Summarize Variations" AI button, Upload screenshot per variation, orange dot indicator, left sidebar navigation (Target/Design/Track) |
| 32 | Experiment Detail > Variations (MVT) — Sections tab (full sidebar) | Full left sidebar: Target (Activation, Audiences), Design (Variations CHANGED badge, Shared Code, Traffic Allocation, Stats Configuration), Track (Metrics, Integrations), Plan (Schedule, Summary), Settings (API Names, History) |
| 33 | Experiment Detail > Variations (MVT) — Combinations tab | Combinations list (AA, AB, AC...), auto-generated from sections, columns: Combination name + description + Traffic Allocation %, Combination action menu: Preview |

---

## Gap Analysis: Screenshots vs Functional Tree

### A. MISSING SCREENS

| Gap | Screenshot # | What's Missing in Functional Tree |
|-----|-------------|----------------------------------|
| A1 | 15, 16, 25 | **1.1.2 should be "Optimizations" not "Experiments List"** — The actual page title is "Optimizations" with 4 tabs: Overview, Experiments, Personalization Campaigns, Exclusion Groups. Current tree only describes "Experiments List". |
| A2 | 15, 16 | **Optimizations > Overview tab** — Combined view of all experiments + campaigns, Show/Hide Columns panel with 20+ column options, column toggle icon |
| A3 | 17 | **Optimizations > Exclusion Groups tab** — Exclusion group list + Create Exclusion Group dialog (Name, Description, experiment browser) |
| A4 | 3 | **History page** — Separate top-level screen in left sidebar navigation (not just experiment-level change history). Has search, Type/Date/Source filters, diff view |

### B. MISSING FEATURES (on existing screens)

#### B1. Optimizations > Experiments tab (Screenshot #14, 26)
- "Get Test Ideas" button (Opal AI)
- "Create..." dropdown (with sub-options)
- Results dropdown per experiment
- Pagination (1-7+ pages)
- Column: Primary Metric, Variations count

#### B2. Optimizations > Personalization Campaigns tab (Screenshot #24)
- Full campaign list with columns: Name, Status, Primary Metric, Audiences, Results
- "Create Personalization Campaign" button
- "Get Test Ideas" button (Opal AI)
- Action menu: Duplicate, Start, Archive, Conclude

#### B3. Experiment Detail > Activation (Screenshot #12)
- Target By dropdown: "Saved Pages" / "URL"
- Page browser with search
- "Create New Page" inline link
- Edit buttons per page
- Revert / Save buttons

#### B4. Experiment Detail > Summary (Screenshot #13)
- Full collapsible section structure: Activation, Audiences, Variations (with Stats Accelerator), Shared Code, Traffic Allocation, Metrics, Stats Configuration, Integrations, Schedule
- "Review Experiment" Opal AI button
- Download summary icon

#### B5. Campaign Detail > Experiences (Screenshot #18-22, 29)
- Status dropdown: Run / Conclude / Archive
- Edit dropdown: "Edit with new editor" / "Edit with legacy editor"
- Variation action menu (...): Rename / Duplicate / Generate Description (AI)
- Experience action menu (...): Publish / Settings / Manage Schedule / Duplicate / Pause / Archive
- "Summarize Variations" AI button
- UNPUBLISHED badge, CAMPAIGN PAUSED status
- Preview / Upload / View buttons per variation
- "Add Variation..." link

#### B6. Campaign Detail > Summary (Screenshot #23)
- Collapsible sections: Experiences (Holdback/Variation %), Activation, Integrations, Metrics (Primary + Secondary), Shared Code
- Download icon

#### B7. Create New Experience dialog (Screenshot #27)
- Experience Name (optional, defaults to audience name)
- Audience field
- Distribution Mode (Manual/Auto)
- Variation names with Traffic Distribution % + Total Traffic %
- "Add Variation" button
- Holdback recommendation warning

#### B8. Prioritize Experiences dialog (Screenshot #28)
- Drag-to-reorder experience priority
- Traffic Percentage (Auto or manual per experience)

#### B9. Implementation page (Screenshot #5, 7, 9)
- **5 tabs missing**: Pages, Events, Templates, Catalogs, Recommenders
- Current tree only mentions "Snippet code" and "Oasis implementation"

#### B10. Implementation > Pages tab (Screenshot #9)
- Page list with columns: Name, API Name, ID, Experiments, Events, Tags
- Status filter
- "Create New Page" button
- Action menu: Edit Page, View Experiment Usage, Archive

#### B11. New Page dialog (Screenshot #8)
- Name*, Editor URL*, Description
- Page Settings: Triggers (Immediately/etc), Conditions (URL Match with match type options)
- Advanced: Deactivation and Undo, Override Page Trimming
- Test URL(s) section

#### B12. Implementation > Events tab (Screenshot #7)
- Events grouped by Page
- Columns: Name, API Name, Experiments, ID, Type
- Event types visible: Custom, Click, Pageview
- Action menu: Settings, View Experiment Usage, Archive
- Status filter

#### B13. Create New Event dialog (Screenshot #6)
- Event type selection: Click / Custom / Pageview
- For Click: Page selector (required)
- "Create Event" button

#### B14. Implementation > Templates tab (Screenshot #5)
- Template list: Name, Template Type, Optimizations, ID
- Status + Creator (Custom) filters
- "Create Template..." dropdown: Duplicate an existing template / Use JSON / Use Editor

#### B15. Implementation > Catalogs (Screenshot #4)
- New Catalog dialog: Name, Description, Catalog Events (search + add), Assign Event Tags (Primary ID, Source URL), Indexing Rate

#### B16. Settings > Implementation tab (Screenshot #2)
- Snippet list table: Name, Projects, ID, Revision, Size
- "Create Custom Snippet..." button

#### B17. Edit Basic Snippet dialog (Screenshot #1)
- Key*, Snippet Details (Platform, Size, Project ID, Revision)
- Visitor ID (Identifier Type dropdown)
- Settings: jQuery Inclusion (3 options), Privacy (4 checkboxes), Cache Expiration TTL dropdown
- Enable Support for Dynamic Websites
- Trim Unused Pages
- Enable Support for Shadow DOM
- Cross-Origin Tracking
- Optimizely X (Enabled/Disabled, Snippet Configuration)

#### B18. Audiences page (Screenshot #10, 11)
- **Saved tab** + **Attributes tab** (2 tabs, not mentioned in tree)
- Audience list columns: Name, Experiments, ID, Created, Modified
- Action menu: View Experiment Usage, Archive
- **Create New Audience page** — Full condition builder with categories:
  - Adaptive, Custom Attributes, Real-Time Segments (NEW!), External Attributes, Visitor Behaviors
  - Standard: Ad Campaign, Browser, Cookie, Custom Javascript, Device, IP Address, Language, Location, New/Returning Session, Platform, Query Parameters, Referrer URL, Time/Day of Visit, Traffic Source
  - Code Mode toggle
  - Drag-and-drop conditions

#### B19. History page (Screenshot #3)
- Search by type:ID
- Filters: Type (Any), Date (Anytime), Source (Any)
- Change Summary table: description, By (user), Time
- Show/Hide details toggle per entry
- Diff view with line numbers, before/after comparison, +/- code highlighting

### C. MISSING UI ELEMENTS (Global)

| Element | Screenshot # | Description |
|---------|-------------|-------------|
| Left sidebar navigation | All | Projects, Optimizations, Audiences, Implementation, History, Settings (not "Experiments List" etc.) |
| Top navigation bar | All | Optimizely EXP Product dropdown, Organization (Experimentation/EXP - Jett Sy) dropdown, "Ask Opal" button, Help (?), User avatar |
| "Get Test Ideas" button | 14, 24 | AI-powered test idea generation (Opal) — appears on Experiments and Campaigns tabs |
| "Variation Development Agent" banner | 18-22 | Top promotional banner for new AI feature |
| "Summarize Variations" button | 22, 29 | AI sparkle icon — generates variation summaries |
| "Generate Description" menu item | 20 | AI sparkle icon in variation action menu |
| Emulate link | 10, 24 | User profile section shows "Emulate" link for admin impersonation |
| Slack Community / Help / Open Desktop App | 7, 10 | Footer links in left sidebar |

---

## Proposed Functional Tree Updates

See the updated sections below for recommended CLAUDE.md changes. Key structural changes:

1. **Rename 1.1.2** from "Experiments List" to "Optimizations" with 4 sub-tabs
2. **Add 1.1.2.1-4** for Overview, Experiments, Personalization Campaigns, Exclusion Groups tabs
3. **Expand 1.1.3** with Activation and Summary detail features
4. **Expand 1.1.4-5** Campaign Detail with full Experiences management features
5. **Restructure 1.1.6-7** as sub-tabs under Implementation (1.1.9)
6. **Add 1.1.15** History page as top-level screen
7. **Expand 1.1.8** Audiences with full builder detail
8. **Expand 1.1.9** Implementation with 5 tabs + dialogs
9. **Expand 1.1.10** Settings with Implementation tab + Edit Snippet dialog
10. **Add global UI elements** section

---

## Additional Gap Analysis (Screenshots #30-33)

### D. MISSING FEATURES (from new screenshots)

#### D1. Experiment Detail > Left Sidebar Navigation (Screenshot #31, 32)
- Structured collapsible sidebar with 5 sections:
  - **Target**: Activation, Audiences
  - **Design**: Variations (with CHANGED badge), Shared Code, Traffic Allocation, Stats Configuration
  - **Track**: Metrics (info icon), Integrations
  - **Plan**: Schedule, Summary
  - **Settings**: API Names, History
- Not documented in Functional Tree — only feature list exists, no sidebar navigation structure

#### D2. MVT Experiment — Sections/Combinations tabs (Screenshot #31, 32, 33)
- **Sections tab**: Section-based variation groups, "Create New Section..." button, Total Combinations counter (current / Max: 64)
- **Combinations tab**: Auto-generated combinations (AA, AB, AC...) from all sections, columns: Combination name + description + Traffic Allocation %, Combination action menu (...): Preview
- Currently not documented — Functional Tree only says "Variation list with traffic allocation"

#### D3. Experiment Variation action menu (Screenshot #31, 32)
- Per-variation (...): Rename, **Delete**, Generate Description (AI sparkle)
- Currently only documented for campaigns (Rename, Duplicate, Generate Description). Experiments have **Delete** instead of Duplicate

#### D4. Summarize Variations on Experiments (Screenshot #31, 32)
- "Summarize Variations" AI sparkle button also appears on Experiment Detail, not just Campaign Detail
- Currently only documented under Campaign Detail (1.1.5)

#### D5. Screenshot upload per variation (Screenshot #31, 32)
- "Upload" button in Screenshot column for each variation
- Not documented in Functional Tree

#### D6. Distribution Mode — 4 options (Screenshot #30)
- Current Functional Tree says "Distribution Mode (Manual/Auto)"
- Actual options: **Manual** | Automation: **Contextual Bandit** (AI traffic allocation), **Multi-armed Bandit** (optimize based on primary metric), **Stats Accelerator** (reach statistical significance faster)
- "Advanced code editor" button in Create Experience dialog

#### D7. Visual indicators (Screenshot #31, 32, 33)
- Orange dot on variations/combinations that have changes
- "CHANGED" badge on Variations nav item when modifications exist

---

## Monolith Screen Reference — Verified UI Behavior (CJS-9865, 2026-03-13)

> Verified from actual production UI (app.optimizely.com).
> Use when writing Expected Results for cross-repo Monolith screen tests.

### Design > Traffic Allocation (dedicated page)

**URL pattern:** `.../experiments/{id}/traffic_allocation`

**UI observed:**
- Section: "Traffic Allocation" → global % slider (e.g., 100%)
- Section: "Variation Traffic Distribution" → lists each variation by NAME with:
  - % input field (editable)
  - "Stop" button per variation
- Distribution Mode dropdown: Manual (default)

**Correct Expected Result format:**
> "Variation #2 appears in Variation Traffic Distribution with correct redistributed % (e.g., ~50%)"

**WRONG Expected Result (do not use):**
> "Traffic Allocation shows X%" ← too vague, unclear which section

---

### Plan > Summary

**URL pattern:** `.../experiments/{id}/summary`

**UI observed (collapsible sections):**
1. Activation (Target by, Triggers, Conditions)
2. Audiences (Match Type)
3. **Variations** → lists each variation by NAME + traffic % (e.g., Original 0%, Variation #1 50%, Variation #2 50%), Stats Accelerator
4. Shared Code
5. **Traffic Allocation** → Distribution mode (Manual) + Portion of visitors % (GLOBAL %, NOT per-variation)
6. Metrics (Primary metric)
7. Stats Configuration
8. Integrations
9. Schedule

**CRITICAL distinction — Summary has TWO traffic-related sections:**
- `Variations section` = per-variation NAME + %
- `Traffic Allocation section` = overall Distribution mode + Portion of visitors %

**Correct Expected Result for Variations section:**
> "Summary > Variations section: 'Hero Banner Change' listed with ~33% alongside Original and Variation #1"

**Correct Expected Result for Traffic Allocation section (if needed):**
> "Summary > Traffic Allocation section: Distribution mode = Manual, Portion of visitors = 100%"

---

### Settings > API Names

**URL pattern:** `.../experiments/{id}/api_names`

**UI observed:**
- Section: "Experiment Details" → Account ID, Project ID, Campaign ID, Experiment ID (all numeric)
- Section: "Exclusion Group"
- Section: **"Variations"** → lists each variation by NAME with its numeric ID
  - Example: "Original" → ID: 4677512966438912
  - Example: "Variation #1" → ID: 5867671489609728
  - Example: "Variation #2" → ID: 6274013178101760
- Section: "Pages" (page name + page ID + API name)
- Section: "Audiences"
- Section: "Events" (event name with snake_case API name e.g., "test-event-archive")

**CRITICAL FACT: Variations use NUMERIC IDs, NOT snake_case:**
- Variations: identified by NAME + numeric ID only
- Events: identified by NAME + snake_case API name (e.g., "test-event-archive")
- Pages: identified by NAME + numeric ID + snake_case API name

**Correct Expected Result:**
> "Settings > API Names: 'Hero Banner Change' is listed in the Variations section with a unique numeric variation ID"

**WRONG Expected Result (do not use):**
> "API name 'hero_banner_change' is auto-generated" ← INCORRECT, variations have no snake_case

---

### Design > Variations tab

**UI observed:**
- Table with columns: Prefix letter (A/B/C), Name, Total Traffic %, Screenshot (Upload button), Edit dropdown, Action menu (...)
- Action menu (...): Rename, Delete (experiments) or Rename, Duplicate (campaigns), Generate Description (AI)
- "Summarize Variations" AI button
- Orange dot indicator on variations with changes

**Correct Expected Result:**
> "Monolith Variations tab: 'Hero Banner Change' appears as 'C Hero Banner Change' with correct traffic %"
