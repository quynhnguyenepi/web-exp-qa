# Sample PR Creation: QAK-14900 AB Test Archive

This is an example of the commit + PR + JIRA update flow produced by the create-pr skill.

---

## Input

From `/exp-qa-agents:create-test-scripts-cypress-js` context:
- Ticket: QAK-14900 - "AB test archive functionality"
- Branch: `phanh/QAK-14900-ab-test-archive-functionality`
- Generated files: 1 spec file with 5 tests
- Linked test cases: QAK-14901, QAK-14902, QAK-14903

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - GitHub CLI: Authenticated
   - Atlassian MCP: Connected
   - Git: 1 new file, 1 modified file

Proceeding to commit and push...
```

---

## Step 1: Commit & Push

**Staged files:**
```
cypress/e2e/web/regression/experiment_details/ab_test/ab_test_archive.spec.js
cypress/pages/web/experiment_details/ExperimentDetailsPage.js
```

**Commit message:**
```
[QAK-14900] Add automation test scripts for AB test archive

- Generated 1 spec file with 5 tests
- Test cases from linked JIRA tickets: QAK-14901, QAK-14902, QAK-14903
- All tests passing on integration environment

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**Push:**
```
git push -u origin phanh/QAK-14900-ab-test-archive-functionality
```

---

## Step 2: Create Pull Request

**PR created via `gh pr create`:**

```
Pull request created!

PR: https://github.com/optimizely/qa_cypress/pull/400
Branch: phanh/QAK-14900-ab-test-archive-functionality → master
Files: 2 files changed
```

---

## Step 3: Update JIRA Tickets

User confirmed: "Yes, update JIRA tickets"

```
JIRA tickets updated!

Automation task:
─────────────────
QAK-14900: Transitioned to "In Review"
QAK-14900: Comment added with PR link

Test case tickets:
─────────────────
QAK-14901: Closed + AutomationDone label
QAK-14902: Closed + AutomationDone label
QAK-14903: Closed + AutomationDone label
```

---

## Final Summary

```
══════════════════════════════════════════════════
Complete!
══════════════════════════════════════════════════

JIRA Ticket:  QAK-14900 → In Review
Branch:       phanh/QAK-14900-ab-test-archive-functionality
PR:           https://github.com/optimizely/qa_cypress/pull/400
Test Cases:   3 tickets closed with AutomationDone label
══════════════════════════════════════════════════
```
