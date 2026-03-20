# JIRA Workflow — Web Experimentation QA

> **Purpose**: Quy trinh day du tu JIRA ticket den test cases den PR.
> **Last Updated**: 2026-03-20

---

## Buoc 1: Doc JIRA Ticket

```
Skill: web-analyze-ticket
Input: JIRA ticket ID (vi du: CJS-11056)
```

**Thu tu doc bat buoc:**
1. CLAUDE.md Section 1 (Architecture — data flow)
2. CLAUDE.md Section 2 (Critical paths — map to test flows)
3. CLAUDE.md Section 3 (QA Standards — coverage)
4. CLAUDE.md Section 4 (JIRA mapping — complexity)
5. `docs/CROSS_REPO_IMPACT_INDEX.md` — blast radius
6. `docs/UI_Screenshots_Analysis.md` — Monolith screen behavior
7. `context/cross-repo-flows.md` — cross-repo verification

---

## Buoc 2: Phan Tich Ticket

### Xac dinh loai ticket
| Ticket type | Code areas | Files |
|-------------|-----------|-------|
| Bug Fix | Component -> Store -> Module | Component, store, tests |
| New Feature | Component moi + stores | Tao files, update stores |
| UI/UX | Component styling | .tsx + .scss |
| API | services/api/ | API client |

### Ap dung 5-Dimension Checklist
- [ ] D1: 6 statuses (Draft/Running/Paused/Concluded/Concluded+Deployed/Archived)
- [ ] D2: Cross-repo Monolith screens (Variations, Summary, History, API Names, Traffic)
- [ ] D3: VE feature interactions (interactive mode, page switcher, unsaved changes)
- [ ] D4: Multiple saved pages (single + 2+ pages)
- [ ] D5: Experiment types (A/B, MAB, MVT, Campaign)

---

## Buoc 3: Tao Test Cases

```
Skill: web-create-test-cases
Input: Phan tich tu Buoc 2
```

**Checklist truoc khi viet:**
- [ ] Kiem tra JIRA: da co smoke TC chua?
- [ ] Xac dinh priority (Critical = full flow, High = core AC, etc.)
- [ ] Xac dinh labels (smoke_suite hoac regression)
- [ ] Format preconditions dung chuan
- [ ] Step 1 = "Open variation in Visual Editor"
- [ ] Button naming = "Click X at the bottom bar"

---

## Buoc 4: Review Test Cases

```
Skill: web-review-test-cases
```

**Checklist sau khi viet:**
- [ ] Moi TC co: Preconditions, Test Data, Steps, Expected Results
- [ ] Full flow TC chi co 1 (Critical priority)
- [ ] Smoke label khong bi duplicate
- [ ] D1-D5 duoc cover day du
- [ ] Anti-patterns khong xuat hien

---

## Buoc 5: Upload len JIRA

- Tao Test Design document: `{TICKET-ID}_Test_Design.md`
- Luu vao `test-designs/2026/`
- Push len web-exp-qa repo
- Comment link test design vao JIRA ticket

---

## Buoc 6: Execute Tests

```
Skill: web-execute-test-suite (headless Playwright)
Hoac: execute-test-case (single TC)
```

---

## Buoc 7: Bug Reporting

```
Skill: create-bug-ticket (neu test fail)
```

**Truoc khi tao bug ticket:**
- [ ] Search JIRA duplicates (skill: search-jira-duplicates)
- [ ] Attach screenshots/evidence
- [ ] Link bug to parent ticket

---

## JIRA Labels Chuan

| Label | Nghia |
|-------|-------|
| `new_ve` | Test lien quan den New Visual Editor |
| `variation` | Test lien quan den variation management |
| `web` | Web Experimentation scope |
| `smoke_suite` | Smoke test (uu tien cao, chay truoc) |
| `regression` | Regression test |
| `mvt` | MVT-specific test |
| `campaign` | Campaign-specific test |

---

## Git Commit Convention

```bash
git commit -m "[CJS-12345] Add test design for XYZ feature"
git commit -m "sync: ve-CLAUDE.md updated with new component"
git commit -m "docs: update UI_Screenshots_Analysis with screen #34"
```
