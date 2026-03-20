# Guidelines — web-create-test-cases (Web Experimentation Override)

> **Purpose**: VE-specific format standards cho common skill `web-create-test-cases`.
> **Extends**: `episerver/claude-qa-skills` skill cung ten.
> **Last Updated**: 2026-03-20

---

## Test Case Format Standards

### Preconditions
- Dong cuoi LUON LA: `"User is logged in and navigated to the experiment"` (KHONG phai "in Visual Editor")
- Step 1 se mo VE — khong can noi trong preconditions

### Parameters — XOA cac dong nay
```
- Website: https://...         <- XOA (redundant)
- Environment: Development     <- XOA (global setting)
```

### Step 1 (tat ca TCs co VE)
```
Step 1: "Open variation in Visual Editor"
```
Ngoai le: read-only TCs -> Step 1 la `"Confirm status shows [Running/Paused/etc]"`

### Button naming (LUON co context)
```
Dung:   "Click the + button at the bottom bar"
Tranh:  "Click the + button"
```

### Steps vs Expected Results
```
Steps:           actions ONLY
                 "Verify X" o cuoi -> chuyen vao Expected Results
                 "Confirm X" o dau -> OK (pre-condition check)
                 "Observe X" -> OK la step

Expected Results: tat ca verify/confirm o cuoi flow
```

---

## Priority Assignment

| Priority | Dung cho |
|----------|---------|
| **Critical** | Full flow (chi 1 TC per ticket) |
| **High** | Core AC + Running status + settings quan trong + Monolith regression |
| **Normal** | Cac status khac, validation, edge cases, feature interactions |
| **Low** | Boundary values, special chars |

---

## Labels

| Label set | Khi nao |
|-----------|---------|
| `new_ve, variation, web, smoke_suite` | Smoke TC |
| `new_ve, variation, web` | Regression TC |

**QUAN TRONG**: Kiem tra JIRA co smoke TC chua truoc khi them smoke_suite label.
Neu smoke da ton tai -> xoa TC duplicate, tat ca con lai = regression.

---

## Full Flow TC

- **Chi 1 TC** (Critical priority) per ticket/document
- **3 checkpoints bat buoc**:
  1. Preview variation trong VE
  2. Preview experiment (QA ball / snippet check)
  3. Live website verification
- KHONG them console/network check cho tickets don gian
- Cac TCs khac: feature-focused, KHONG copy lai full flow

---

## Status TCs (D1 — bat buoc)

Viet 1 TC cho moi trang thai lien quan:

```
TC: [Feature] - Draft status (edit allowed)
TC: [Feature] - Running status (read-only, feature restricted)
TC: [Feature] - Paused status (read-only, feature restricted)
TC: [Feature] - Concluded status (read-only, feature restricted)
```

Khong can test tat ca 6 status neu ticket chi anh huong 1-2 status.
Nhung LUON PHAI xet xem trang thai nao bi anh huong.

---

## Monolith Regression TCs (D2 — High priority)

Sau moi VE action, them TC verify Monolith:

```
TC: [Feature] - Monolith Variations tab reflects changes
TC: [Feature] - Monolith Summary shows correct data
TC: [Feature] - Monolith History logs the action
```

Expected Result mau:
```
"Experiment Detail > Design > Variations tab: [variation name] appears with [traffic]%"
"Experiment Detail > Plan > Summary > Variations section: [name] shows [traffic]%"
"Experiment Detail > Settings > History: entry 'variation created' with timestamp"
```

---

## VE-Specific Expected Results

### Variation API Names
```
Dung:   "listed by name with unique numeric variation ID (e.g., ID: 6274013178101760)"
Tranh:  "variation_name in snake_case format"
```

### Traffic Allocation (Summary page)
```
Dung:   "Traffic Allocation section shows Distribution mode and overall visitor %"
Tranh:  "Traffic Allocation shows per-variation percentages"
        (per-variation % o TREN trang Summary > Variations, KHONG phai Traffic Allocation section)
```

### Orange Dot Indicator
```
Dung:   "Orange dot indicator appears on [Variation Name] tab"
Tranh:  "Change indicator shown" (khong ro la gi)
```

---

## Segment Events (neu ticket lien quan)

| Action | Event name |
|--------|-----------|
| Click + button | `variation_add_started` |
| Press Enter (create) | `variation_add_created` |
| Press Escape/X (cancel) | `variation_add_canceled` |
