# Repos — Web Experimentation Lane

## 3 Source Repos

| Repo | URL | Mo ta | QA push duoc? |
|------|-----|-------|--------------|
| `optimizely/visual-editor` | https://github.com/optimizely/visual-editor | VE micro-frontend (React, TypeScript) | Khong |
| `optimizely/optimizely` | https://github.com/optimizely/optimizely | Monolith UI (Nuclear.js, React, Backbone) | Khong |
| `episerver/claude-qa-skills` | https://github.com/episerver/claude-qa-skills | Common QA skills | Co (neu la contributor) |
| `episerver/web-exp-qa` | https://github.com/episerver/web-exp-qa | **Repo nay** — QA workspace | Co |

---

## Clone Guide

```bash
# Repo chinh de lam viec hang ngay
git clone https://github.com/episerver/web-exp-qa
cd web-exp-qa

# Doc source code VE khi can trace implementation
git clone https://github.com/optimizely/visual-editor

# Doc source code Monolith khi can (optional)
git clone https://github.com/optimizely/optimizely

# Common skills (neu can chay skills offline)
git clone https://github.com/episerver/claude-qa-skills
```

---

## Branch Convention

```
# web-exp-qa repo
main                          <- Production branch
{username}/{TICKET-ID}-{desc} <- Feature branch

# Vi du
quynh/CJS-11056-auth-error-fix
quynh/CJS-10765-changelog-test-update
```

---

## Cach doc CLAUDE.md cua tung repo

| Ban muon biet gi | Mo Claude Code o dau |
|------------------|--------------------|
| QA workflow, test standards, cross-repo | `web-exp-qa/` |
| VE architecture, components, stores | `visual-editor/` |
| Monolith screens, sections | `optimizely/` |
| Common skills | `claude-qa-skills/` |

---

## Sync context files khi source repo thay doi

```bash
# Khi visual-editor/CLAUDE.md duoc update boi dev
cp ../visual-editor/CLAUDE.md context/ve-CLAUDE.md
# Them dong dau file:
# <!-- SOURCE: optimizely/visual-editor/CLAUDE.md -->
# <!-- LAST SYNCED: YYYY-MM-DD -->
git commit -m "sync: ve-CLAUDE.md updated with <mo ta>"

# Sync docs
cp ../visual-editor/docs/IMPACT_INDEX.md docs/IMPACT_INDEX.md
cp ../visual-editor/docs/UI_Screenshots_Analysis.md docs/UI_Screenshots_Analysis.md
```
