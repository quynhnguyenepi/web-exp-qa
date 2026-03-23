# Test Standards — Web Experimentation Lane

> **Purpose**: Chuan format test case, priority, label cho Web Exp QA.
> **Source**: Tong hop tu CJS-9865 retrospective va learnings tu tung ticket.
> **Last Updated**: 2026-03-20

---

## Test Case Format

### Preconditions
- Liet ke environment, test data, trang thai he thong
- Dong cuoi LUON LA: `"User is logged in and navigated to the experiment"`
- KHONG dung: `"User is in Visual Editor"` (VE mo o Step 1)

### Parameters — KHONG them cac dong nay
- `Website: https://...` — redundant
- `Environment: Development` — global setting, khong can lap lai

### Step 1 (tat ca TCs co VE)
- Luon la: `"Open variation in Visual Editor"`
- Ngoai le: read-only TCs -> Step 1 la `"Confirm status shows [Running/Paused/etc]"`

### Button naming
- LUON them context: `"Click the + button at the bottom bar"`
- KHONG viet: `"Click the + button"` (khong ro o dau)

### Steps vs Expected Results
- Steps: CHI chua actions (khong co "Verify X" o cuoi step)
- `"Verify X"` o cuoi flow -> chuyen vao Expected Results
- `"Confirm X"` o dau step -> OK (pre-condition check)
- `"Observe X"` -> OK la step

---

## Priority Rules

| Priority | Dung cho |
|----------|---------|
| **Critical** | Full flow TC (chi 1 TC per document) |
| **High** | Core AC + Running status + settings quan trong + Monolith regression |
| **Normal** | Cac status khac, validation, edge cases, feature interactions |
| **Low** | Boundary values, special chars, minor UI |

---

## Label Convention

| Label set | Dung khi |
|-----------|---------|
| `new_ve, variation, web, smoke_suite` | Smoke TC (check JIRA truoc, neu da co smoke thi skip) |
| `new_ve, variation, web` | Regression TC |

**Luu y**: Kiem tra JIRA xem da co smoke TC chua truoc khi tao moi.
Neu smoke da ton tai -> tat ca TCs con lai = regression, KHONG tao smoke trung.

---

## Full Flow TC

- **Chi 1 TC per document** (Critical priority)
- **3 checkpoints bat buoc**:
  1. Preview variation (trong VE)
  2. Preview experiment (QA ball / snippet check)
  3. Live website verification
- KHONG them console/network verification cho tickets don gian
- Cac TCs khac: feature-focused, KHONG duplicate full flow

---

## Test Case Volume (theo complexity)

| Complexity | So TCs tieu bieu |
|-----------|-----------------|
| Low (1-2 files, 10-50 LOC) | 3-5 TCs |
| Medium (3-5 files, 50-200 LOC) | 6-10 TCs |
| High (5-10 files, 200-500 LOC) | 10-15 TCs |
| Very High (10+ files, 500+ LOC) | 15-20+ TCs |

---

## Status Coverage (D1 — bat buoc)

Moi tinh nang VE can co TC cho tung trang thai:

| Status | VE behavior | TC focus |
|--------|------------|---------|
| Draft | Edit OK, + button hien | Happy path |
| Running | Read-only, + button an | Verify restriction |
| Paused | Read-only, + button an | Verify restriction |
| Concluded | Read-only, + button an | Verify restriction |
| Concluded+Deployed | Read-only, + button an | Verify restriction |
| Archived | Read-only, + button an | Verify restriction |

---

## Variation API Names — Luu y dac biet

- Variations: **TEN + NUMERIC ID** (vi du: "Variation #2" -> ID: 6274013178101760)
- **KHONG** co snake_case API name cho variations
- Chi Events va Pages moi co snake_case API name
- Expected Result dung: `"listed by name with unique numeric variation ID"`

---

## MVT-Specific Rules

- Endpoint khac: `PUT /v2/experiments/sections/{sectionId}` (KHONG phai `/v2/experiments/{id}`)
- Monolith: Verify ca Sections tab VA Combinations tab
- Max 64 combinations (auto-generated tu sections)
- Orange dot indicator tren ca variation level VA combination level
