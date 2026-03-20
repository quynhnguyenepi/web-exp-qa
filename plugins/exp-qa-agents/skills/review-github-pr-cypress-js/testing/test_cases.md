# GitHub PR Review Skill - Test Cases

## Overview

Validation tests for the **exp-review-github-pullrequest** skill. These test cases verify that the skill correctly performs pre-flight checks, fetches PR details, analyzes code, generates structured reviews, and posts them to GitHub.

## Test Categories

### 1. Pre-Flight Check Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| preflight-gh-installed | Verify gh CLI Detection | System with `gh` installed | Reports "GitHub CLI: Authenticated" in pre-flight status |
| preflight-gh-missing | Handle Missing gh CLI | System without `gh` | Displays install instructions and exits gracefully |
| preflight-gh-unauth | Handle Unauthenticated gh | `gh` installed but not logged in | Displays "gh auth login" instructions and exits gracefully |
| preflight-pr-not-found | Handle Invalid PR Number | PR #99999 (nonexistent) | Reports "PR not found" error with the PR number |
| preflight-pr-url | Extract PR from URL | `https://github.com/optimizely/qa_cypress/pull/369` | Extracts PR number 369 correctly |
| preflight-pr-number | Accept Direct PR Number | `369` or `#369` | Accepts and strips `#` prefix if present |

**Purpose:** Verify pre-flight checks catch tool and input issues before starting the review workflow

---

### 2. Documentation Sync Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| sync-no-checkout | Verify No Branch Switch | Any PR review request | Does NOT run `git checkout master` — preserves user's current branch |
| sync-fetch-only | Fetch Without Checkout | Any PR review request | Runs `git fetch origin master` only |
| sync-reads-docs | Read All Documentation | Any PR review request | Reads CLAUDE.md, coding-conventions.md, best-practices.md, anti-patterns.md |

**Purpose:** Verify documentation sync does not destroy user's working branch or uncommitted changes

---

### 3. PR Fetch Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| fetch-pr-details | Fetch PR Metadata | Valid PR number | Extracts title, author, files, commits from `gh pr view` |
| fetch-pr-diff | Get PR Diff | Valid PR number | Retrieves diff using `gh pr diff` |
| fetch-large-pr | Handle Large PR | PR with 50+ changed files | Warns user about large scope, prioritizes test files over config |
| fetch-error-handling | Handle Fetch Failure | Network error during `gh pr view` | Reports specific error, does not silently continue |

**Purpose:** Verify PR details are fetched correctly with proper error handling

---

### 4. Code Analysis Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| analyze-page-objects | Detect Page Object Usage | PR with direct `cy.get()` calls | Flags missing Page Object pattern usage |
| analyze-builder-pattern | Detect Builder Pattern | PR with object literal test data | Suggests using Builder pattern |
| analyze-cleanup | Detect Missing Cleanup | PR without `afterEach` cleanup | Flags missing `cy.deleteAccount()` in afterEach |
| analyze-only-pause | Detect .only() and .pause() | PR with `.only()` or `.pause()` calls | Flags as critical issue |
| analyze-naming | Check Test Naming | PR with test names | Validates `[TICKET-ID][Product][Module]_Description` format |
| analyze-duplication | Detect Code Duplication | PR with repeated setup code | Suggests consolidation into beforeEach or helper |

**Purpose:** Verify code analysis catches common convention violations in Cypress test files

---

### 5. Review Generation Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| review-structure | Verify Review Format | Any analyzed PR | Review contains: Score, Positives, Issues, Questions sections |
| review-score-approve | Score for Clean PR | PR with no issues | Score 8-10/10, action: Approve |
| review-score-changes | Score for Problematic PR | PR with critical issues | Score below 7/10, action: Request Changes |
| review-score-comment | Score for Educational | PR with minor suggestions | Score 7/10, action: Comment |
| review-code-snippets | Include Code Examples | PR with fixable issues | Review includes current code + suggested improvement |
| review-file-references | Include File References | PR with issues | Review references file paths and line numbers |

**Purpose:** Verify review generation produces well-structured, actionable feedback

---

### 6. User Confirmation Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| confirm-present-review | Present Before Posting | Any completed review | Shows full review to user before posting |
| confirm-post-asis | Handle "Post as-is" | User selects "Post review as-is" | Proceeds to post review to GitHub |
| confirm-edit | Handle "Edit first" | User selects "Let me edit the review first" | Asks for changes, updates review, re-presents |
| confirm-cancel | Handle "Cancel" | User selects "Cancel - Don't post" | Saves review locally, exits without posting |

**Purpose:** Verify user always has control before review is posted publicly

---

### 7. Review Posting Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| post-body-file | Use --body-file Method | Any approved review | Writes to temp file, posts via `--body-file`, cleans up |
| post-no-body-var | Never Use --body "$VAR" | Any approved review | Does NOT use `--body "$REVIEW_BODY"` — always uses file |
| post-approve | Post Approve Review | Score 9/10 review | Runs `gh pr review N --approve --body-file ...` |
| post-request-changes | Post Request Changes | Score 5/10 review | Runs `gh pr review N --request-changes --body-file ...` |
| post-comment | Post Comment Review | Score 7/10 review | Runs `gh pr review N --comment --body-file ...` |
| post-error-handling | Handle Post Failure | Network error during posting | Saves review locally, reports error, offers retry |
| post-confirm-success | Confirm Successful Post | Successful post | Shows PR URL and confirms review visible |

**Purpose:** Verify review posting uses safe file-based approach and handles errors gracefully

---

### 8. Test Case ↔ Script Mapping Tests

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| mapping-match | Matching Steps | PR with `it('[CJS-9525]...')` and matching JIRA steps | Reports all test cases as PASS in mapping results |
| mapping-mismatch-explained | Mismatch with Explanation | PR with mismatched steps + JIRA comment explaining | Reports PASS with note, includes JIRA comment text |
| mapping-mismatch-fail | Mismatch Without Explanation | PR with mismatched steps, no JIRA explanation comment | Reports FAIL, lists missing steps, deducts score |
| mapping-no-test-cases | No Linked Test Cases | PR with no JIRA ticket IDs in `it()` names | Skips mapping check gracefully, proceeds to analysis |
| mapping-no-test-files | PR Has No Test Files | PR with only page objects or support files | Skips mapping check gracefully |
| mapping-partial | Mixed Results | PR with some matching and some mismatched test cases | Reports mixed results with correct per-case status and summary |

**Purpose:** Verify test case ↔ script mapping correctly identifies matches, handles mismatches with/without JIRA explanations, and skips gracefully when not applicable

---

## Test Execution

To run these tests:

```bash
# Run all evaluations
/evaluation-runner run ALL evaluations for exp-review-github-pullrequest

# Run specific category
/evaluation-runner run ONLY preflight-gh-installed for exp-review-github-pullrequest

# Run posting tests only
/evaluation-runner run ONLY post-body-file for exp-review-github-pullrequest
```

---

## Success Criteria

All evaluations must PASS for the skill to be considered production-ready:

- **Pre-Flight Checks:** Validates tools and input before starting
- **Documentation Sync:** Fetches docs without switching branches
- **PR Fetching:** Retrieves PR data with error handling
- **Code Analysis:** Catches convention violations accurately
- **Review Generation:** Produces structured, scored reviews
- **User Confirmation:** Always gets approval before posting
- **Review Posting:** Uses --body-file safely, handles errors
