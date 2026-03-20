# Generating QA Test Cases - Test Cases

## Overview

Validation tests for the **generating-qa-test-cases** skill. These test cases verify that the skill correctly generates comprehensive test documentation from JIRA tickets with proper quality, coverage, and JIRA upload functionality.

## Test Categories

### 1. JIRA Analysis Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| jira-extract-ac | Extract Acceptance Criteria | JIRA ticket (DHK-4456) with AC section | Parses AC into 4+ testable scenarios |
| jira-parse-fields | Parse JIRA Fields | JIRA ticket | Extracts summary, description, type, component |

**Purpose:** Verify the skill can correctly fetch and parse JIRA tickets using MCP tools

---

### 2. Test Case Generation Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| generate-validation-cases | Validation Coverage | Form with required fields (email, password) | Generates 1+ P0 test case per required field |
| generate-priority-distribution | Priority Balance | Complex ticket with multiple flows | P0: 50-60%, P1: 30-40%, P2: 10-20% |
| quality-clear-titles | Clear Action-Oriented Titles | Any feature ticket | Titles start with verbs (Verify, Test, Check) |
| test-steps-specific | Specific Numbered Steps | Any feature ticket | Steps are numbered, specific, actionable |
| expected-results-verifiable | Verifiable Expected Results | Any feature ticket | Results are measurable, concrete outcomes |
| test-data-included | Test Data Specification | Form validation ticket | Includes valid/invalid test data examples |

**Purpose:** Verify the skill generates high-quality test cases following guidelines.md standards

---

### 3. JIRA Upload Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| jira-upload-confirmation | Upload Confirmation | Test design with 40 test cases | Requests user confirmation before creating JIRA tickets |
| jira-ticket-creation | Ticket Creation | Approved test cases | Creates linked Test tickets in JIRA project |
| jira-retry-logic | Failed Upload Retry | Partial upload failure (3 of 40 failed) | Offers retry for failed cases only |
| jira-link-validation | Ticket Linking | Created test tickets | All test tickets linked to parent ticket |

**Purpose:** Verify JIRA upload creates tickets correctly with proper linking and error handling

---

### 4. Coverage Summary Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| summary-calculate-total | Total Count Accuracy | 47 test cases | Summary shows "Total: 47" |
| summary-priority-breakdown | Priority Stats | Mixed P0/P1/P2 cases | Shows "P0: 30, P1: 14, P2: 3" |
| summary-category-breakdown | Category Counts | Labeled test cases | Shows counts for Functional, UI, Validation, etc. |
| summary-percentages | Percentage Calculation | Test cases with priorities | Calculates P0/P1/P2 percentages correctly |

**Purpose:** Verify coverage summary calculations are accurate and match actual test case counts

---

### 5. Integration Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| end-to-end-dhk4456 | Complete Workflow | DHK-4456 JIRA ticket | Generates 40-50 test cases, creates .md file, uploads to JIRA |
| end-to-end-bug | Bug Ticket Workflow | Bug JIRA ticket | Generates 5-10 test cases focused on reproduction + verification |
| performance-timing | Execution Speed | Any JIRA ticket | Completes in < 120 seconds |

**Purpose:** Verify the complete end-to-end workflow from JIRA ticket to deliverables

---

## Test Execution

To run these tests:

```bash
# Run all evaluations
/evaluation-runner run ALL evaluations for generating-qa-test-cases

# Run specific category
/evaluation-runner run ONLY jira-extract-ac for generating-qa-test-cases

# Run end-to-end integration test
/evaluation-runner run ONLY end-to-end-dhk4456 for generating-qa-test-cases
```

---

## Success Criteria

All evaluations must PASS for the skill to be considered production-ready:

- ✅ **JIRA Analysis:** Correctly extracts AC and parses ticket fields
- ✅ **Test Case Quality:** Titles, steps, results meet guidelines.md standards
- ✅ **Priority Distribution:** Balanced P0/P1/P2 percentages (50-60%, 30-40%, 10-20%)
- ✅ **JIRA Upload:** Creates linked tickets with confirmation and retry logic
- ✅ **Coverage Summary:** Accurate counts and percentages
- ✅ **Integration:** End-to-end workflow produces correct outputs in < 120s

---

## Known Limitations (v1)

- **JIRA-only analysis:** Does not integrate with Figma (but does read implementation code via CLAUDE.md)
- **Markdown-only export:** Only generates markdown files, no Excel/CSV export
- **No template customization:** Uses fixed test case table structure
- **No gap analysis:** Does not compare against existing test cases

These limitations are intentional for v1 scope and may be addressed in future versions.
