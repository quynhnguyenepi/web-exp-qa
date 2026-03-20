# Cross-Repo Impact Index — Web Experimentation

> **Purpose**: Impact map XUYEN CA 3 REPO khi co thay doi.
> Khac voi `IMPACT_INDEX.md` (chi scope VE repo), file nay map impact tu VE -> Monolith -> Skills.
> **Last Updated**: 2026-03-20

---

## Cach dung

1. Tim component/file trong ticket
2. Doc "Impact trong VE" -> files can regression test
3. Doc "Impact tren Monolith" -> screens can verify sau khi save
4. Doc "Impact skills" -> skills co the can update neu behavior thay doi

---

## VE Components -> Monolith Impact

### `components/variations_list/VariationsList.tsx`

**Impact trong VE:**
- `experimentStore.ts` -> `changeStore.ts` -> `syncChanges()`
- `services/api/experiments.ts` -> `PUT /v2/experiments/{id}`

**Impact tren Monolith (verify sau khi save):**
| Monolith Screen | Verify gi |
|----------------|-----------|
| Design > Variations tab | Variation list cap nhat (ten, traffic %) |
| Plan > Summary | Variations section hien dung ten + % |
| Design > Traffic Allocation | Per-variation % slider cap nhat |
| Settings > API Names | Variation co numeric ID moi |
| Settings > History | Entry "variation created/modified" |

**Impact skills:**
- `web-analyze-ticket/guidelines.md` - D2 dimension
- `web-create-test-cases/guidelines.md` - variation TC format

---

### `stores/changeStore.ts`

**Impact trong VE:**
- Tat ca *Manager components (BackgroundManager, BorderManager, etc.)
- `modules/changes.ts` -> Customer DOM
- `services/api/experiments.ts` -> API save

**Impact tren Monolith:**
| Monolith Screen | Verify gi |
|----------------|-----------|
| Design > Variations tab | Orange dot indicator tren variation |
| Plan > Summary | CHANGED badge |
| Settings > History | Change log entries |

**Impact skills:** `web-analyze-ticket` (D1 Status, D2 Screens, D3 Feature Inter.)

---

### `services/api/experiments.ts`

**Impact trong VE:** experimentStore -> toan bo VE data load/save

**Impact tren Monolith:**
| Monolith Screen | Verify gi |
|----------------|-----------|
| Tat ca experiment tabs | Data hien dung sau khi VE save |
| Results page | Snippet push sau khi publish |
| History | API call tao log entry |

**MVT NOTE**: `/v2/experiments/sections/{sectionId}` khac endpoint vs A/B `/v2/experiments/{id}`

---

### `services/api/events.ts`

**Impact trong VE:** eventStore -> AttributeList, EventEditor

**Impact tren Monolith:**
| Monolith Screen | Verify gi |
|----------------|-----------|
| Implementation > Events tab | Event moi hien trong danh sach |
| Event detail page | API Name (snake_case), selector, type |
| Experiment > Metrics | Event available lam metric |

---

### `services/api/auth.ts` + `stores/authStore.ts`

**Impact trong VE:** Tat ca API calls (auth token bat buoc)

**Impact tren Monolith:** VE khong load duoc neu auth fail -> Monolith bao loi

**Impact skills:** Error scenario TCs (CSP, auth propagation)

---

### `modules/selectorator.ts`

**Impact trong VE:**
- Highlighter.tsx -> element selection
- SelectorDropdown.tsx -> selector editing
- AdvancedSelector.tsx -> selector tree

**Impact tren Monolith:** (khong truc tiep) but selector sai -> change khong apply -> customer website bi loi

---

## Monolith Components -> VE Impact

### Monolith: Experiment created/variation added

**Trigger**: Dev/PM tao experiment moi tren Monolith
**VE impact**: VE nhan experiment data qua `GET /v2/experiments/{id}` khi load

### Monolith: Editor iframe loading

**Files**: `modules/editor/`, `modules/editor_iframe/` (Monolith) <-> `modules/editor_client.js` (VE)
**Communication**: postMessage API
**Impact**: Token handshake -> VE khong load duoc neu Monolith khong pass token dung

---

## Skill Impact Index

| Thay doi | Skills can update |
|---------|-------------------|
| VE tao variation API moi | `web-analyze-ticket/guidelines.md` D5 |
| Monolith them screen moi | `web-analyze-ticket/guidelines.md` D2 + `docs/UI_Screenshots_Analysis.md` |
| VE them feature moi | `web-analyze-ticket/guidelines.md` D3 + `web-create-test-cases/guidelines.md` |
| Status flow thay doi | `web-analyze-ticket/guidelines.md` D1 |
| Test case format thay doi | `web-create-test-cases/guidelines.md` + `docs/test-standards.md` |

---

## Quick Blast Radius by Ticket Type (Cross-Repo)

| Ticket mo ta | VE files | Monolith screens | Skills |
|-------------|---------|-----------------|--------|
| Variation create/rename | VariationsList, experimentStore, experiments.ts | Variations tab, Summary, Traffic Alloc, API Names, History | D2 dimension |
| Element style change | changeStore, changes.ts, *Manager components | Variations tab (orange dot), Summary (CHANGED), History | D1, D3 |
| Click event | eventStore, EventEditor, events.ts | Implementation > Events, Experiment > Metrics | D2 events screen |
| Auth/token | authStore, auth.ts, client.ts | VE load error -> Monolith shows error | Error scenarios |
| Page switcher | viewStore, PageSwitcher, views.ts | Activation tab (saved pages) | D4 multi-page |
| MVT sections | experimentStore, experiments.ts (sections endpoint) | Variations Sections + Combinations tabs | D5 MVT |
| Opal Chat | opalChatStore, useOpalEvents, changeStore | Variations tab (orange dot after AI change) | D3 Opal inter. |
