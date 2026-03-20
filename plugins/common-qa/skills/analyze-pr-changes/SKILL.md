---
description: Find PRs linked to a JIRA ticket, read diffs, classify code changes, and identify scope discrepancies between ticket AC and actual implementation. Use when you need to understand what code actually changed for a ticket.
---

## Dependencies

- **MCP Servers:** Atlassian, GitHub
- **Related Skills:** `/common-qa:read-jira-context`, `/exp-qa-agents:review-github-pr-cypress-js`

# Analyzing PR Changes

Find linked PRs for a JIRA ticket via JIRA development info and git log, fetch PR diffs, classify each changed file, identify changes beyond the acceptance criteria, and assess overall scope.

## When to Use

Invoke this skill when you need to:

- Find all PRs linked to a JIRA ticket
- Read and classify code diffs to understand what actually changed
- Identify changes beyond the ticket's acceptance criteria
- Assess scope of impact (isolated, moderate, broad)
- Find follow-up PRs that fix or extend the original change

## Workflow Overview

```
Pre-Flight -> Find PRs (JIRA + git log) -> Fetch PR Details -> Read & Classify Diffs -> Find Follow-ups -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:** Accept `issue_key`, `repo_owner`, `repo_name`.
   - If `repo_owner` and `repo_name` are not provided, they will be resolved from JIRA development info in Step 1
2. **Verify Atlassian MCP:** Attempt `mcp__atlassian__jira_get_issue_development_info`. If not available, warn and rely on git log only.
3. **Verify GitHub MCP:** Check if `mcp__github__get_pull_request` is available. If not, warn PR details will be limited to git log.

### Step 1: Find Linked PRs

**Via JIRA development info (primary):**
```
mcp__atlassian__jira_get_issue_development_info({ issue_key: "{ISSUE_KEY}" })
```

- Extract PR URLs from the development info response
- If `repo_owner`/`repo_name` were not provided in input, extract them from the PR URLs (e.g., `github.com/optimizely/app-ui/pull/123` -> `optimizely/app-ui`)
- **Do NOT fall back to `git remote get-url origin`** -- the current repo may not be the target repo

**Fallback via git log (only if current repo IS the target repo and no PRs from JIRA):**
```bash
git log --oneline --all --grep="{TICKET_ID}" -20
```

Also search by keywords from ticket title:
```bash
git log --oneline --all --grep="{KEYWORD}" -20
```

Extract PR numbers from commit messages using `(#NNN)` pattern.

**Note:** The git log fallback only works when the current working directory contains the target repo. If the repo_owner/repo_name doesn't match the current repo's remote, skip the git log fallback.

### Step 2+3: Fetch PR Details + Classify Diffs IN PARALLEL

For each PR, fetch details and diffs using **direct parallel MCP calls** (no Agent tool needed — each PR requires 2 MCP calls that can all be issued in a single message):

**Per PR:**

Fetch details:
```
mcp__github__get_pull_request({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  pull_number: {PR_NUMBER}
})
```

Extract: title, description, merge status, base branch.

Fetch file list (includes patches inline — use selectively):
```
mcp__github__get_pull_request_files({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  pull_number: {PR_NUMBER}
})
```

**Token optimization:** The response includes full patches for all files. Focus analysis on:
- **Implementation files** (`.ts`, `.tsx`, `.jsx`, stores, hooks, utils) — read patches carefully
- **Config/constant files** — read patches for new rules or flag changes
- **Test files** (`.test.*`) — only scan file names and additions count to understand dev coverage, do NOT analyze full test patches (they are verbose and rarely reveal new test scenarios beyond what the implementation already shows)
- **Skip patches** for: lock files, generated files, snapshot files, large test fixtures

Classify each changed file:

| File Pattern | Category | Test Impact |
|-------------|----------|-------------|
| `*.tsx`, `*.jsx` | Components | UI changes, verify rendering |
| `*Store.ts` | Stores | State changes, verify data flow |
| `*api/*.ts` | Services | API changes, verify integration |
| `constants.ts`, `enums.ts` | Config | Verify downstream usage |
| `*.test.*` | Tests | Understand what devs already tested |

**Identify changes beyond AC:**
- Refactored shared utilities (broad impact)
- Renamed event names or constants
- Removed parameters from function calls
- New function calls or events added
- Store behavior modifications

### Step 4: Find Follow-up PRs

Search git log for related commits after the main PR merge:
```bash
git log --oneline --all --grep="{KEYWORD1}\|{KEYWORD2}" -20
```

### Step 5: Assess Scope and Return Output

Compare ticket AC vs actual PR changes. Document discrepancies.

**Scope assessment:**
- **Isolated:** <5 files changed, single feature affected
- **Moderate:** 5-15 files, related features affected
- **Broad:** >15 files, shared utilities or cross-cutting changes

---

## Output Format

```markdown
### PRs Found ({count})

For each PR:
- **PR #{number}:** {title}
- **Status:** {merged/open}
- **Files changed:** {count} (+{additions}/-{deletions})
- **Classification:**
  - Components: {list}
  - Stores: {list}
  - Services: {list}
  - Config: {list}
  - Tests: {list}

### Changes Beyond AC
- {description of each change not in the ticket}

### Follow-up PRs ({count})
- PR #{number}: {title} -- {what it fixes/extends}

### Scope Assessment
- **Scope:** {Isolated/Moderate/Broad}
- **Justification:** {why}

### Discrepancies
- **AC asks for:** {X}
- **PRs implement:** {X + Y + Z}
- **Additional changes needing testing:** {list}
```

If no PRs found:
```markdown
### PRs Found (0)
No PRs found for {TICKET_ID}. Analysis limited to ticket AC only.
```

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
