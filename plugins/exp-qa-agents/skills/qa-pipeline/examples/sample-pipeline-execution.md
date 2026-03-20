# Sample: QA Pipeline Execution (Mode A - Manual)

## User Request

> Run the QA pipeline for CJS-200

## Execution

### Pre-flight

```
Ticket: CJS-200
MCP Connectivity:
  - Atlassian: Connected
  - Playwright: Connected
  - GitHub: Connected (not required for Mode A)
```

**User prompt:** "Which mode? A (Manual), B (Automated), or C (Full)?"
**User response:** "Mode A"

### Stage 1: Analyze Ticket

Dispatched `/exp-qa-agents:analyze-ticket` with CJS-200.

**Analysis Summary:**
- Title: "Add bulk edit for experiment metrics"
- Type: Feature
- 4 acceptance criteria
- Linked Confluence page: "Bulk Edit Design Spec"
- Figma design: 2 screens (list view, bulk edit dialog)
- PR: #67 (14 files changed)

**Gate:** "Analysis complete. 4 ACs, Confluence spec, Figma design, PR #67. Proceed to test case generation?"
**User:** "Yes, proceed"

### Stage 2: Generate Test Cases

Dispatched `/exp-qa-agents:create-test-cases` with CJS-200 + analysis context.

**Test Cases Generated:**
- P0: 3 test cases (core bulk edit flow)
- P1: 4 test cases (validation, permissions)
- P2: 3 test cases (edge cases, UI states)
- Total: 10 test cases, 47 steps

**Gate:** "10 test cases generated (3 P0, 4 P1, 3 P2). Proceed to review?"
**User:** "Yes"

### Stage 3: Review Test Cases

Dispatched `/exp-qa-agents:review-test-cases` with generated test cases + requirements.

**Review Results:**
- Quality: 80% complete (8/10 at Grade A or B)
- Coverage: 90% of ACs covered (1 gap found)
- Gap: No test case for "bulk edit with 100+ metrics" (performance edge case)
- 2 test cases need more specific test data

**Gate:** "Quality 80%, coverage 90%. 1 gap: bulk edit at scale. Approve / regenerate / edit / abort?"
**User:** "Approve, we can add the edge case later"

### Stage 4: Execute Tests

**User prompt:** "Run single test case or full test suite?"
**User response:** "Full suite"

Dispatched `/exp-qa-agents:execute-test-suite` with 10 test cases + target URL.

**Execution Results:**
- 8/10 test cases PASSED
- 2/10 test cases FAILED
  - TC-005: "Bulk edit with no metrics selected" -- error dialog did not appear
  - TC-008: "Cancel bulk edit" -- changes were not reverted

**Gate:** "8 passed, 2 failed. Proceed to bug filing?"
**User:** "Yes, file bugs for both failures"

### Stage 5: File Bugs

Dispatched `/exp-qa-agents:create-bug-ticket` twice (one per failure).

**Bug Tickets Created:**
- BUG-301: "Bulk edit: no error when zero metrics selected" (linked to CJS-200)
- BUG-302: "Bulk edit: cancel does not revert changes" (linked to CJS-200)

**Gate:** "2 bug tickets created: BUG-301, BUG-302. Finalize pipeline?"
**User:** "Approved"

### Pipeline Summary

```
QA Pipeline Report -- CJS-200

| Stage | Status | Key Output |
|-------|--------|------------|
| 1. Analyze | Complete | 4 ACs, Confluence, Figma, PR #67 |
| 2. Generate TC | Complete | 10 test cases (3 P0, 4 P1, 3 P2) |
| 3. Review TC | Complete | 80% quality, 90% coverage |
| 4. Execute | Complete | 8 passed, 2 failed |
| 5. File Bugs | Complete | BUG-301, BUG-302 |

Pass Rate: 80% (8/10)
Bugs Filed: 2
Total Duration: ~25 minutes
```
