---
description: Fetch GitHub PR details including title, description, diff, file list, reviewers, and merge status. Use when any skill needs PR metadata and code changes before analysis.
---

## Dependencies

- **MCP Servers:** GitHub
- **Related Skills:** `/common-qa:analyze-pr-changes`, `/exp-qa-agents:review-github-pr-cypress-js`, `/exp-qa-agents:create-pr`

# Read PR Details

Fetch comprehensive GitHub Pull Request details: metadata (title, description, author, reviewers, status), changed files list, and full diff. Returns structured output for downstream skills to analyze.

## When to Use

Invoke this skill when you need to:

- Get PR metadata (title, description, author, reviewers, merge status)
- Fetch the list of changed files with additions/deletions counts
- Get the full diff for code review or classification
- Check PR size (file count, line count) for review readiness
- Verify PR has required reviewers assigned

## Workflow Overview

```
Pre-Flight -> Fetch PR Metadata -> Fetch Changed Files -> Fetch Diff -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:** Accept any of:
   - PR URL: `https://github.com/{owner}/{repo}/pull/{number}`
   - PR number + repo: `{ pr_number: 123, repo_owner: "optimizely", repo_name: "app-ui" }`
   - PR number only (resolve repo from caller-provided context or ask user)
2. **Extract PR details** from input:
   - Parse owner, repo, and PR number from URL if provided
   - If only PR number given, resolve repo:
     - First: use repo_owner/repo_name if provided by the calling skill
     - Fallback: `git remote get-url origin` (note: may not be the target repo if run from a different project)
     - If ambiguous, ask user via AskUserQuestion: "Which repository is this PR in?"
3. **Verify GitHub access:** Check if GitHub MCP is available via `mcp__github__get_pull_request`. If unavailable, fall back to `gh` CLI:
   ```bash
   gh auth status
   ```
   If neither available, exit with error:
   ```
   Error: GitHub access is not configured

   This skill requires GitHub MCP server or GitHub CLI (gh).

   Setup Instructions:
   1. Ensure .mcp.json exists with GitHub server configuration, OR
   2. Install and authenticate GitHub CLI: gh auth login

   See .mcp.json.template for detailed configuration.
   ```

### Step 1: Fetch PR Metadata

**Via GitHub MCP (preferred):**
```
mcp__github__get_pull_request({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  pull_number: {PR_NUMBER}
})
```

**Fallback via gh CLI:**
```bash
gh pr view {PR_NUMBER} --repo {OWNER}/{REPO} --json title,body,author,state,mergeable,reviewRequests,assignees,labels,baseRefName,headRefName,number,url,createdAt,updatedAt,mergedAt,additions,deletions,changedFiles
```

Extract: title, description, author, state (open/closed/merged), base branch, head branch, reviewers, labels, created/updated/merged dates, additions, deletions, changed file count.

### Step 2: Fetch Changed Files

**Via GitHub MCP:**
```
mcp__github__get_pull_request_files({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  pull_number: {PR_NUMBER}
})
```

**Fallback via gh CLI:**
```bash
gh pr diff {PR_NUMBER} --repo {OWNER}/{REPO} --stat
```

For each file, record: filename, status (added/modified/deleted/renamed), additions, deletions.

### Step 3: Fetch Full Diff

**Via gh CLI (most reliable for full diff):**
```bash
gh pr diff {PR_NUMBER} --repo {OWNER}/{REPO}
```

If diff is too large (>5000 lines), truncate and note:
```
Diff truncated at 5000 lines. Full diff available via: gh pr diff {PR_NUMBER}
```

---

## Output Format

```markdown
### PR #{number}: {title}

**URL:** {pr_url}
**Author:** {author}
**Status:** {open/merged/closed}
**Branch:** {head_branch} -> {base_branch}
**Created:** {date} | **Updated:** {date} | **Merged:** {date or N/A}
**Reviewers:** {list or "None assigned"}
**Labels:** {list or "None"}

### Size
- **Files changed:** {count}
- **Additions:** +{additions}
- **Deletions:** -{deletions}
- **Total lines:** {additions + deletions}
- **Size assessment:** {Small (<100 lines) | Medium (100-500) | Large (>500)}

### Changed Files ({count})

| # | File | Status | +/- |
|---|------|--------|-----|
| 1 | {path/to/file.ts} | Modified | +{add}/-{del} |
| 2 | {path/to/new-file.ts} | Added | +{add}/-0 |
| 3 | {path/to/old-file.ts} | Deleted | +0/-{del} |

### Diff
{full diff content or truncated with note}
```

---


## Guidelines

### Data Collection

1. **Prefer GitHub MCP** over `gh` CLI for structured data.
2. **Fall back to `gh` CLI** when MCP is unavailable.
3. **Truncate large diffs** at 5000 lines to avoid context overflow.

### Size Assessment

| Lines Changed | Assessment |
|---------------|-----------|
| <100 | Small |
| 100-500 | Medium |
| >500 | Large |

### Input Parsing

- PR URL: Extract owner, repo, PR number from `github.com/{owner}/{repo}/pull/{number}`
- PR number only: Resolve repo from `git remote get-url origin`

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
