# Web Experimentation QA — Lane Workspace

> **Purpose**: QA workflow context cho Web Experimentation lane.
> Đây KHÔNG phải mô tả source code — đọc `context/` để có architecture context từng repo.

**Last Updated**: 2026-03-20
**Lane**: Web Experimentation (VE + Monolith)
**Team**: QA Engineers

---

## Source Repos (architecture context)

| Repo | CLAUDE.md | IMPACT_INDEX.md | Muc dich |
|------|-----------|-----------------|---------|
| `optimizely/visual-editor` | xem `context/ve-CLAUDE.md` | xem `docs/IMPACT_INDEX.md` (VE scope) | VE micro-frontend |
| `optimizely/optimizely` | xem `context/monolith-CLAUDE.md` | xem `docs/CROSS_REPO_IMPACT_INDEX.md` | Monolith UI |
| `episerver/claude-qa-skills` | xem `context/skills-CLAUDE.md` | — | Common skills |

> Clone guide va repo links: xem `context/repos.md`

---

## QA Workflow Nhanh

### Khi nhan ticket moi
1. Doc `context/repos.md` -> xac dinh ticket thuoc repo nao
2. Chay skill `web-analyze-ticket` -> phan tich JIRA
3. Kiem tra `docs/CROSS_REPO_IMPACT_INDEX.md` -> blast radius
4. Tham khao `docs/test-standards.md` -> format test case
5. Xem `docs/jira-workflow.md` -> quy trinh day du

### Cross-repo impact (bat buoc kiem tra)
VE change -> verify: xem `context/cross-repo-flows.md`

---

## Key Facts (quick reference)

### Experiment Statuses (6 trang thai)
```
Draft           -> edit OK, + button hien
Running         -> read-only, + button an
Paused          -> read-only, + button an
Concluded       -> read-only, + button an
Concluded+Deployed -> read-only, + button an
Archived        -> read-only, + button an
```

### API Endpoints
```
A/B, MAB, Campaign : PUT /v2/experiments/{id}
MVT                : PUT /v2/experiments/sections/{sectionId}  <- KHAC ENDPOINT
Events             : GET/POST/PUT /api/v1/projects/{id}/events
Views              : GET/PUT /api/v1/views
```

### 5-Dimension Checklist (bat buoc moi ticket VE)
```
D1 - Status Coverage   : Test ca 6 trang thai
D2 - Monolith Screens  : Variations tab, Summary, History, API Names, Traffic Allocation
D3 - VE Feature Inter  : Interactive mode, Page switcher, Unsaved changes warning
D4 - Multiple Pages    : Single page + 2+ saved pages
D5 - Experiment Types  : A/B | MAB | MVT | Campaign
```

### Monolith Screen References (sau khi VE action)
| Screen | Duong dan | Verify gi |
|--------|-----------|-----------|
| Variations tab | Experiment Detail > Design > Variations | Name, traffic %, orange dot |
| Summary | Experiment Detail > Plan > Summary | Variation names + % |
| Traffic Allocation | Experiment Detail > Design > Traffic Allocation | Per-variation % slider |
| API Names | Experiment Detail > Settings > API Names | Numeric ID (KHONG snake_case) |
| History | Experiment Detail > Settings > History | Change log entry |

---

## Anti-Patterns (TUYET DOI TRANH)
1. KHONG tin JIRA screenshots -> doc *.tsx source code
2. KHONG dung tai API call -> trace forward den Monolith screens
3. KHONG viet status TCs tu bo nho -> enum tu Section tren
4. KHONG test isolation -> doc D3 (feature interactions)
5. KHONG assume single-page -> luon them multi-page TC
6. KHONG viet "snake_case API name" cho variation -> chi numeric ID

---

## Files trong repo nay

```
context/
  repos.md              <- Clone guide, branch convention
  ve-CLAUDE.md          <- Architecture VE (sync tu visual-editor/CLAUDE.md)
  monolith-CLAUDE.md    <- Architecture Monolith (sync tu optimizely/CLAUDE.md)
  skills-CLAUDE.md      <- Common skills (sync tu claude-qa-skills/CLAUDE.md)
  cross-repo-flows.md   <- VE change -> verify gi o Monolith
  environments.md       <- inte/prep/prod URLs

docs/
  CROSS_REPO_IMPACT_INDEX.md  <- Impact map XUYEN 3 repo
  IMPACT_INDEX.md             <- Impact map VE only (sync tu visual-editor/docs/)
  UI_Screenshots_Analysis.md  <- Verified Monolith screen behavior
  test-standards.md           <- Format, priority, label rules
  jira-workflow.md            <- Ticket -> test case -> PR

test-designs/2026/
  CJS-*.md              <- Historical test designs

skills/
  web-analyze-ticket/guidelines.md    <- VE-specific: 5-dim, anti-patterns
  web-create-test-cases/guidelines.md <- VE format standards
```
