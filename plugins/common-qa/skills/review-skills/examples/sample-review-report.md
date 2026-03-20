# Sample Review Report

This is an example of a review report produced by the review-skills skill, showing mixed results across 7 skills.

---

## Skills Consistency Review Report

**Date:** 2026-03-03
**Skills Reviewed:** 7
**Total Checks:** 70 (10 categories x 7 skills)
**Issues Found:** 5

### Summary

| Skill | Structure | Frontmatter | References | Params | Messages | Steps | JIRA | MCP Setup | Sections | Score |
|-------|:---------:|:-----------:|:----------:|:------:|:--------:|:-----:|:----:|:---------:|:--------:|:-----:|
| analyze-ticket | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | 9/9 |
| create-bug-ticket | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 7/9 |
| create-pr | FAIL | FAIL | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | 6/9 |
| create-test-cases | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 9/9 |
| create-test-scripts-cypress-js | PASS | PASS | FAIL | PASS | PASS | PASS | N/A | PASS | PASS | 8/9 |
| review-github-pr-cypress-js | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | 9/9 |
| execute-test-case | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 9/9 |

### Details

#### create-bug-ticket

**Score: 7/9**

Issues:
- [FAIL] Check 1 (Frontmatter): `name: create-bug-ticket` field present at SKILL.md:2 -- should be removed
- [FAIL] Check 2 (Structure): Missing `guidelines.md`, `examples/`, `testing/`

No issues:
- [PASS] Check 3, 4, 5, 6, 7, 9, 10
- [N/A] Check 8 (JIRA Comments) -- skill creates JIRA tickets, comment format verified

---

#### create-pr

**Score: 6/9**

Issues:
- [FAIL] Check 1 (Frontmatter): `name: create-pr` field present at SKILL.md:2 -- should be removed
- [FAIL] Check 2 (Structure): Missing `guidelines.md`, `examples/`, `testing/`
- [FAIL] Check 8 (JIRA Comments): Comment at SKILL.md:210 missing "skill." suffix -- `via /exp-qa-agents:create-pr.` should be `via /exp-qa-agents:create-pr skill.`

No issues:
- [PASS] Check 3, 4, 5, 6, 7, 9, 10

---

#### create-test-scripts-cypress-js

**Score: 8/9**

Issues:
- [FAIL] Check 3 (File References): Path `.claude/skills/exp-generate-test-scripts/guidelines.md` at SKILL.md:409 does not exist -- use `guidelines.md from this skill's directory` instead

No issues:
- [PASS] Check 1, 2, 4, 5, 6, 7, 9, 10

---

#### analyze-ticket, create-test-cases, review-github-pr-cypress-js, execute-test-case

**Score: 9/9 each**

No issues found. All checks passed.

---

### Recommendations

**High Priority:**
- create-bug-ticket: Add missing `guidelines.md`, `examples/`, `testing/` directories (Check 2)
- create-pr: Add missing `guidelines.md`, `examples/`, `testing/` directories (Check 2)
- create-test-scripts-cypress-js: Fix broken file path reference at SKILL.md:409 (Check 3)

**Medium Priority:**
- create-bug-ticket: Remove `name` field from frontmatter (Check 1)
- create-pr: Remove `name` field from frontmatter (Check 1)
- create-pr: Add "skill." suffix to JIRA comment at SKILL.md:210 (Check 8)

---

**Overall: 5 issues found across 3 skills. 4 skills are fully consistent.**
