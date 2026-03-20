# Cross-Repo Flows — VE change -> Monolith verification

> **Purpose**: Khi QA thuc hien action trong Visual Editor, day la nhung gi can verify tren Monolith UI.
> Su dung file nay de khong bo sot Dimension D2 (Cross-Repo Monolith Screens).

---

## Flow 1: Tao/doi ten Variation trong VE

**Trigger**: User tao variation moi hoac doi ten variation
**VE action**: Click + button -> nhap ten -> Enter

**Verify tren Monolith:**
| Screen | URL path | Verify gi |
|--------|---------|-----------|
| Variations tab | `.../experiments/{id}#variations` | Variation moi hien trong danh sach voi ten dung |
| Summary > Variations | `.../experiments/{id}#summary` | Ten + traffic % hien chinh xac |
| Traffic Allocation | `.../experiments/{id}#traffic` | Variation xuat hien trong bang phan bo traffic |
| API Names | `.../experiments/{id}#api-names` | Ten + numeric ID (KHONG snake_case) |
| History | `.../experiments/{id}#history` | Entry "variation created/renamed" |

---

## Flow 2: Apply change cho element trong VE

**Trigger**: User chon element, thay doi style/text/attribute
**VE action**: Click element -> chinh sua -> Save

**Verify tren Monolith:**
| Screen | URL path | Verify gi |
|--------|---------|-----------|
| Variations tab | `#variations` | Orange dot indicator tren variation co change |
| Summary > Variations | `#summary` | CHANGED badge hien |
| History | `#history` | Entry mo ta change |

---

## Flow 3: Save/Publish variation

**Trigger**: User save changes va publish experiment
**VE action**: Save button -> Publish tren Monolith

**Verify tren Monolith:**
| Screen | URL path | Verify gi |
|--------|---------|-----------|
| Variations tab | `#variations` | Orange dot bien mat sau khi save |
| Results | `#results` | Snippet duoc push len CDN |
| History | `#history` | "Published" entry voi timestamp |

---

## Flow 4: Tao Click Event trong VE

**Trigger**: User tao event tracking cho element
**VE action**: Attributes button -> Create event -> Save

**Verify tren Monolith:**
| Screen | URL path | Verify gi |
|--------|---------|-----------|
| Implementation > Events | `/implementation/events` | Event moi hien trong danh sach |
| Event detail | `.../events/{id}` | API Name (snake_case), selector, type = Click |
| Experiment > Metrics | `#metrics` | Event co the duoc add lam metric |

---

## Flow 5: Redirect change

**Trigger**: User tao redirect URL cho variation
**VE action**: Redirect editor -> nhap URL -> Save

**Verify tren Monolith:**
| Screen | URL path | Verify gi |
|--------|---------|-----------|
| Variations tab | `#variations` | Variation hien "Redirect" badge/indicator |
| History | `#history` | "Redirect change added" entry |

---

## Flow 6: Chuyen trang (Page Switcher) trong VE

**Trigger**: User chuyen giua cac saved pages
**VE action**: Page Switcher dropdown -> chon page khac

**Verify:**
| Check | Mo ta |
|-------|-------|
| Changes isolation | Changes tren page A khong bi mat khi sang page B |
| Page indicator | Page switcher hien dung ten page hien tai |
| Activation tab | Monolith Activation tab hien pages da duoc assign |

---

## Monolith Screen Quick Reference

```
Experiment Detail URL: https://{env}.optimizely.com/v2/projects/{pid}/experiments/{eid}

Tab paths (append vao URL):
  Variations     : #variations
  Summary        : #summary (hoac /overview)
  Traffic Alloc  : #traffic
  API Names      : #settings (tab API Names)
  History        : #history
  Activation     : #activation
  Metrics        : #metrics
  Results        : #results
```

---

## Luu y quan trong

- **MVT**: Verify o Sections tab VÀ Combinations tab cua Monolith
- **Campaign**: Verify o Experiences tab (khac Experiments tab)
- **Running/Paused status**: Monolith show orange dot nhung KHONG cho phep edit
- **API Names cho variation**: Chi co numeric ID, KHONG co snake_case
