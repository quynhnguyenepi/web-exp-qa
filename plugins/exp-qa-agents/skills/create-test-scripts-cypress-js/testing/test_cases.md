# Generating Cypress Test Scripts - Test Cases

## Overview

Validation tests for the **exp-generate-test-scripts** skill. These test cases verify that the skill correctly generates Cypress test scripts from JIRA tickets, following all project coding conventions, builder patterns, page object patterns, and API-first setup practices.

## Test Categories

### 1. Pre-Flight Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| preflight-jira-check | Verify Atlassian MCP | Ticket ID with Atlassian MCP disabled | Clear error with enable instructions |
| preflight-git-status | Check Git Status | Dirty working tree | Warning with stash/cancel options |
| preflight-input-validation | Validate Input Format | JIRA URL, ticket ID, invalid input | Correct ticket ID extraction via regex |

**Purpose:** Verify the skill validates prerequisites before proceeding

---

### 2. JIRA Analysis Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| jira-read-linked-tests | Extract Linked Test Cases | JIRA ticket with linked Test tickets | Fetches and lists all linked Test tickets |
| jira-parse-embedded-tests | Parse Embedded Test Steps | JIRA ticket with steps in description | Extracts numbered steps and expected results |
| jira-no-tests-found | Handle No Test Cases | JIRA ticket with no tests | Suggests /exp-qa-agents:create-test-cases and exits |
| jira-detect-product-area | Detect Product Area | Ticket with Web/Flag/Edge component | Correct product area detection |

**Purpose:** Verify the skill correctly fetches and parses JIRA tickets and test cases

---

### 3. Branch Management Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| branch-naming-convention | Branch Naming Convention | QAK-14900 "AB test archive" | Branch: `{shortName}/QAK-14900-ab-test-archive` |
| branch-sync-master | Sync Latest Master | Any ticket | Fetches and checks out latest master before branching |
| branch-already-exists | Handle Existing Branch | Ticket with existing branch | Asks user to use existing or create new |
| branch-user-shortname | Get User Short Name | git config user.name result | Extracts/asks for short name correctly |

**Purpose:** Verify correct branch management following project conventions

---

### 4. Codebase Analysis Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| analyze-find-similar-tests | Find Similar Tests | Web AB test feature | Finds tests in regression/experiment_details/ab_test/ |
| analyze-identify-page-objects | Identify Page Objects | Web experiment feature | Identifies ExperimentListPage, WebLeftSideBar, etc. |
| analyze-identify-builders | Identify Builders | Web experiment feature | Identifies ExperimentBuilder, PageBuilder, etc. |
| analyze-read-docs | Read Project Docs | Any feature | Reads CLAUDE.md, coding-conventions.md, guidelines.md |
| analyze-determine-tags | Determine Tags | Web AB test | Selects WebTag.web, WebTag.campaign_ab, CommonTag.experiment_detail |

**Purpose:** Verify the skill correctly analyzes the codebase to match patterns and identify dependencies

---

### 5. Script Generation Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| generate-correct-imports | Correct Import Paths | Spec at depth 5 from cypress/ | Correct relative paths (../../../../..) |
| generate-builder-pattern | Uses Builder Pattern | Any web test | ExperimentBuilder/PageBuilder used in setup |
| generate-page-objects | Uses Page Object Pattern | Any test | No direct cy.get() in spec, page object methods used |
| generate-test-naming | Test Naming Convention | Linked test QAK-12345 | `[QAK-12345][Web][Module]_Description` format |
| generate-cleanup | Includes Cleanup | Any test | cy.deleteAccount() in after/afterEach |
| generate-max-five-tests | Max 5 Tests Per File | 8 test cases | Split into 2 spec files (5 + 3) |
| generate-tags | Appropriate Tags | Web AB test | WebTag.web, CommonTag.experiment_detail in tags array |
| generate-function-syntax | Function Not Arrow | Any test | describe/it/before/after use function() |
| generate-region-comments | Region Comments | Any test | #region Setup, #region Execution, #region Cleanup |
| generate-todo-selectors | TODO Selectors | New UI feature | cy.get('[data-test="TODO"]') with comment |

**Purpose:** Verify generated test scripts follow all project coding conventions

---

### 6. Lint & Review Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| lint-no-errors | No Lint Errors | Generated spec file | npm run lint:fix passes |
| lint-no-only | No .only() Calls | Generated spec file | No .only() in generated code |
| lint-no-pause | No .pause() Calls | Generated spec file | No .pause() in generated code |
| review-user-confirmation | User Confirmation | Generated files | Presents files with approve/change/skip options |
| review-skip-execution | Skip Test Execution | User selects "Skip" | Marks run step as skipped, shows summary |

**Purpose:** Verify linting and user review workflow

---

### 7. Test Execution Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| run-tests-correct-command | Correct Command | Integration environment | npm run cy:run-local-spec:inte -- "path" |
| run-tests-rc-environment | RC Environment | RC selected | npm run cy:run-local-spec:prep -- "path" |
| run-tests-handle-failure | Handle Test Failures | Failing test | Analyzes error, applies fix, re-runs (max 3 attempts) |
| run-tests-fix-rerun | Fix & Re-Run Loop | Test fails on first run | Fixes issue, re-runs, proceeds to commit on pass |
| run-tests-max-attempts | Max Fix Attempts | Test fails 3 times | Stops after 3 attempts, asks user for help |
| run-tests-all-pass | All Tests Pass | Passing tests | Proceeds to commit & PR step |

**Purpose:** Verify test execution using correct Cypress commands with fix & re-run logic

---

### 8. Commit & Pull Request Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| commit-create-pr | Create Commit and PR | All tests passing | Stages files, commits, pushes, creates PR via `gh` |
| commit-message-format | Commit Message Format | QAK-14900 ticket | Commit: `[QAK-14900] Add automation test scripts` |
| commit-staged-files | Correct Files Staged | Generated spec + page objects | Only stages relevant files, no unrelated changes |
| pr-body-format | PR Body Format | Generated PR | Body has Summary, linked tickets, spec files, test results |
| pr-title-format | PR Title Format | QAK-14900 ticket | Title includes ticket ID and is under 70 chars |
| pr-push-branch | Push Branch to Remote | New branch | `git push -u origin {branch}` before PR creation |

**Purpose:** Verify correct git commit, push, and PR creation workflow

---

### 9. JIRA Update Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| jira-transition-task | Transition Task to In Review | Automation task ticket | `mcp__atlassian__jira_transition_issue` to "In Review" |
| jira-close-test-cases | Close Test Case Tickets | 3 linked test tickets | Each transitioned to "Closed" |
| jira-add-label | Add AutomationDone Label | 3 linked test tickets | "AutomationDone" label added to each via `mcp__atlassian__jira_update_issue` |
| jira-add-comment | Add Automation Comment | Task ticket | Comment with PR link and spec file paths |
| jira-partial-failure | Handle Partial JIRA Failures | 1 ticket already closed | Continues with remaining tickets, reports partial success |
| jira-transition-fallback | Handle Unknown Transition | Non-standard workflow | Tries alternative status names, reports if unable |

**Purpose:** Verify JIRA ticket transitions, label updates, and comment additions after PR creation

---

### 10. Integration Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| end-to-end-web | Complete Web Test | Web JIRA ticket with 3 linked tests | Full workflow: JIRA → branch → scripts → lint → review → run → commit → PR → JIRA update |
| end-to-end-flag | Complete Flag Test | Flag JIRA ticket with 2 linked tests | Uses createFlagsAccount, FlagTag, flag builders, creates PR, updates JIRA |
| end-to-end-embedded | Embedded Test Steps | Ticket with description-only test steps | Parses from description, generates spec, full post-test workflow |
| end-to-end-fix-rerun | Complete With Fix & Re-Run | Ticket where test initially fails | Full workflow including auto-fix, re-run, then commit/PR/JIRA |

**Purpose:** Verify the complete end-to-end workflow from JIRA ticket to PR creation and JIRA updates

---

## Test Execution

To run these tests:

```bash
# Run all evaluations
/evaluation-runner run ALL evaluations for exp-generate-test-scripts

# Run specific category
/evaluation-runner run ONLY preflight-jira-check for exp-generate-test-scripts

# Run end-to-end integration test
/evaluation-runner run ONLY end-to-end-web for exp-generate-test-scripts
```

---

## Success Criteria

All evaluations must PASS for the skill to be considered production-ready:

- **Pre-Flight:** Validates Atlassian MCP, git status, and input correctly
- **JIRA Analysis:** Extracts linked test cases or parses embedded steps
- **Branch Management:** Creates branch following `{shortName}/{TICKET_ID}-{title}` convention
- **Codebase Analysis:** Finds similar tests, identifies page objects/builders/tags
- **Script Generation:** Follows all coding conventions (imports, builders, page objects, naming, cleanup, tags, max 5 tests)
- **Lint & Review:** Passes lint, no .only()/.pause(), presents for user review
- **Test Execution:** Uses correct Cypress commands, handles pass/fail with fix & re-run (max 3 attempts)
- **Commit & PR:** Creates correct commit message, pushes branch, creates PR with proper body
- **JIRA Updates:** Transitions task to "In Review", closes test cases with "AutomationDone" label
- **Integration:** End-to-end workflow from JIRA ticket to PR creation and JIRA updates

---

## Known Limitations (v1)

- **TODO selectors:** New UI features may require placeholder selectors that need manual investigation
- **Complex API setup:** Some features require multi-step API orchestration not available via existing commands
- **Cross-test dependencies:** Tests sharing state require careful ordering with testIsolation: false
- **New page objects:** If no existing page objects cover the feature, basic ones are created with TODO selectors
- **JIRA format variations:** Test case parsing depends on consistent JIRA ticket formatting

These limitations are intentional for v1 scope and may be addressed in future versions.
