# Guidelines — web-analyze-ticket (Web Experimentation Override)

> **Purpose**: VE-specific additions cho common skill `web-analyze-ticket`.
> **Extends**: `episerver/claude-qa-skills` skill cung ten.
> **Last Updated**: 2026-03-20

---

## Reading Workflow (bat buoc theo thu tu)

1. Doc `context/ve-CLAUDE.md` Section 1 (Architecture — data flow path)
2. Doc `context/ve-CLAUDE.md` Section 2 (Critical paths — map ticket to test flows)
3. Doc `context/ve-CLAUDE.md` Section 3 (QA Standards — coverage requirements)
4. Doc `context/ve-CLAUDE.md` Section 4 (JIRA mapping — complexity assessment)
5. Doc `docs/CROSS_REPO_IMPACT_INDEX.md` — trace 4 directions per component
6. Doc `docs/UI_Screenshots_Analysis.md` — correct Monolith screen expected results
7. Doc `context/cross-repo-flows.md` — cross-repo verification flows
8. Apply 5-Dimension checklist (xem ben duoi)

---

## 5-Dimension Checklist (BAT BUOC moi ticket VE)

### D1 — Status Coverage (6 trang thai)
```
Draft              -> edit OK, + button hien
Running            -> read-only, + button an
Paused             -> read-only, + button an
Concluded          -> read-only, + button an
Concluded+Deployed -> read-only, + button an
Archived           -> read-only, + button an
```
Moi tinh nang moi can TC cho CA 6 trang thai.

### D2 — Cross-Repo Monolith Screens (sau VE -> API -> Monolith)
Sau khi VE action, verify tren cac screens nay:
- Variations tab (1.1.3.2): variation list, orange dot, traffic %
- Summary > Variations (1.1.3.1): ten + %
- Design > Traffic Allocation: per-variation % slider
- Settings > API Names: numeric ID (KHONG snake_case cho variation)
- Settings > History: change log entry

### D3 — VE Feature Interactions
- Interactive mode (Alt/Option key) on/off
- Page switcher khi co multiple pages
- Unsaved changes warning khi switch variation
- Changes list (ellipsis tren active tab)

### D4 — Multiple Saved Pages
- TC voi 1 page (single page experiment)
- TC voi 2+ saved pages (page switching behavior)

### D5 — Experiment Types
- A/B Test
- MAB (Multi-Armed Bandit)
- MVT (khac endpoint: `/v2/experiments/sections/{sectionId}`)
- Campaign (Experiences, khong phai Variations)

---

## Anti-Patterns (TUYET DOI TRANH)

1. **KHONG** tin JIRA screenshots lam proof of implementation -> doc `*.tsx` source code
2. **KHONG** dung tai API call -> trace forward den Monolith display screens (D2)
3. **KHONG** viet status TCs tu bo nho -> enum tu D1 tren
4. **KHONG** test features in isolation -> doc D3 (Interaction Bar interactions)
5. **KHONG** assume single-page -> luon them multi-page TC khi VariationsList/PageSwitcher involved
6. **KHONG** viet "auto-generated snake_case API name" cho variations -> numeric IDs only

---

## Key Facts VE (khong can tra lai)

### VariationsList.tsx
- CreateVariation: + button -> inline input (fake TabNav.Tab) -> Enter/Escape/X
- `verifyAction()` goi truoc khi CREATE hoac SWITCH variation (unsaved changes warning)
- `isLayerReadOnly()` an + button khi: Running/Paused/Concluded/Archived
- `isSaving` hien Spinner thay the tat ca variation tabs
- Segment events: `variation_add_started` (click +), `variation_add_created` (Enter), `variation_add_canceled` (Escape/X)
- ChangeList.tsx: ellipsis tren active tab = Changes dropdown (KHONG phai Rename/Duplicate/Delete)

### API Endpoints
```
A/B, MAB, Campaign : PUT /v2/experiments/{id}
MVT                : PUT /v2/experiments/sections/{sectionId}  <- KHAC
Events             : GET/POST/PUT /api/v1/projects/{id}/events
Views              : GET/PUT /api/v1/views
```

### Monolith Screen Facts (verified tu UI_Screenshots_Analysis.md)

**Design > Traffic Allocation (dedicated page):**
- Liet ke tung variation theo TEN voi % input + "Stop" button
- Expected Result: "Hero Banner Change appears in Variation Traffic Distribution with correct %"

**Plan > Summary:**
- Variations section: TEN + traffic % per variation
- Traffic Allocation section: Distribution mode + overall visitor % ONLY (KHONG per-variation)
- Day la 2 sections KHAC NHAU tren cung 1 trang

**Settings > API Names:**
- Variations: TEN + numeric ID (vi du: "Variation #2" -> ID: 6274013178101760)
- KHONG co snake_case API name cho variations
- Chi Events va Pages moi co snake_case
