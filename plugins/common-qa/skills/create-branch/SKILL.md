---
description: Create a new git branch from the repo's default branch (main or master) following the team naming convention {username}/{TICKET-ID}-{short-description}. Use when starting work on a JIRA ticket and need a fresh branch.
---

## Dependencies

- **MCP Servers:** Atlassian (for ticket title lookup to generate branch name)
- **Related Skills:** `/exp-qa-agents:create-test-scripts-cypress-js`, `/exp-qa-agents:create-pr`

# Create Branch from JIRA Ticket

Checkout to the repo's default branch (main or master), pull latest changes, and create a new branch following the team naming convention: `{username}/{TICKET-ID}-{short-description}`.

## When to Use

Invoke this skill when you need to:

- Start work on a JIRA ticket and need a new branch
- Create a branch named after a ticket ID (e.g., `phanh/CJS-10886-apply-playwright-for-automation`)

## Branch Naming Convention

Branch names follow the pattern used in the team's repos:

```
{username}/{TICKET-ID}-{short-description-in-kebab-case}
```

**Examples from the codebase:**
- `cuongph/CJS-10777-campaign-pause-experience`
- `ngtu/APPX-12506-change-approval-tests-update-to-use-random-account`
- `phanh/CJS-10804-add-new-ve-part2`
- `thaopp/APPX-12361-create-scripts-for-duplicate-flag-part-1`
- `HoaVu/CJS-10803-update-element-change-regression-case`

**Rules:**
- `{username}`: git username (from `git config user.name` or first part of git email). If multi-word (e.g., "Phan Phuong Anh"), use a short alias — check git log for existing branch patterns to determine the user's preferred alias (e.g., `phanh`). If unclear, ask the user.
- `{TICKET-ID}`: JIRA ticket ID in uppercase (e.g., `CJS-10886`)
- `{short-description}`: ticket title converted to kebab-case, truncated to keep branch name reasonable length

## Workflow Overview

```
Parse Ticket ID -> Get Username + Ticket Title -> Detect Default Branch -> Checkout & Pull -> Create Branch -> Report
```

## Execution Workflow

### Step 0: Parse JIRA Ticket ID and Build Branch Name

1. **Accept input** in any of these formats:
   - JIRA URL: `https://optimizely-ext.atlassian.net/browse/CJS-10886`
   - Ticket ID: `CJS-10886`
   - Lowercase: `cjs-10886`

2. **Extract ticket ID** from the input:
   - From URL: parse the last path segment (e.g., `CJS-10886` from `.../browse/CJS-10886`)
   - From plain text: match pattern `[A-Z]+-[0-9]+` (case-insensitive)

3. **If no ticket ID can be parsed**, use AskUserQuestion:
   - "What is the JIRA ticket ID? (e.g., CJS-10886 or a JIRA URL)"

4. **Get the git username:**
   ```bash
   git config user.name
   ```
   - If not set, extract from email: `git config user.email` (take part before `@`)
   - If multi-word (e.g., "Phan Phuong Anh"), check existing branch names for the user's preferred alias:
     ```bash
     git branch -r | head -20
     ```
   - If still unclear, ask the user via AskUserQuestion for their preferred branch prefix
   - Use as-is for the `{username}` prefix (e.g., `phanh`, `cuongph`, `ngtu`)

5. **Fetch ticket title** via Atlassian MCP:
   ```
   jira_get_issue({ issue_key: "{TICKET_ID}" })
   ```
   - Extract the ticket summary/title
   - Convert to kebab-case: lowercase, replace spaces and special characters with hyphens, remove consecutive hyphens
   - If Atlassian MCP not available: use AskUserQuestion to ask for a short description

6. **Build branch name:**
   ```
   {username}/{TICKET_ID}-{kebab-case-title}
   ```
   - Example: `phanh/CJS-10886-apply-playwright-for-automation-tests`
   - Present to user for confirmation via AskUserQuestion with options:
     - **"Yes, proceed" (Recommended)** — use the generated branch name
     - **"Use different name"** — user provides a custom branch name (use their exact input)
   - If user provides a custom name via "Other" or edits the name, use their exact input without modification

### Step 1: Checkout Default Branch and Pull Latest

1. **Detect the repo's default branch** (main or master):
   ```bash
   git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
   ```
   - If the above fails, check which exists: `git branch -r | grep -E 'origin/(main|master)$'`
   - Use whichever the repo has (`main` or `master`)

2. **Check for uncommitted changes:**
   ```bash
   git status --porcelain
   ```
   - If there are uncommitted changes, warn the user via AskUserQuestion:
     - "You have uncommitted changes. What would you like to do before switching branches?" with options:
       - **"Stash changes" (Recommended)** -- `git stash`
       - **"Discard changes"** -- `git checkout -- . && git clean -fd`
       - **"Cancel"** -- exit without switching

3. **Checkout and pull:**
   ```bash
   git checkout {DEFAULT_BRANCH}
   git pull
   ```

### Step 2: Create and Checkout New Branch

1. **Check if branch already exists:**
   ```bash
   git branch --list "{BRANCH_NAME}"
   ```
   - If exists locally, ask user:
     - **"Switch to existing branch" (Recommended)** -- `git checkout {BRANCH_NAME}`
     - **"Delete and recreate"** -- `git branch -D {BRANCH_NAME}` then create fresh
     - **"Cancel"**

2. **Create and checkout the new branch:**
   ```bash
   git checkout -b {BRANCH_NAME}
   ```

3. **Report:**
   ```
   Branch created successfully
     - Branch: {BRANCH_NAME}
     - Based on: {DEFAULT_BRANCH} (latest)
     - Ticket: {TICKET_ID} - {TICKET_TITLE}

   Ready to start working on {TICKET_ID}.
   ```

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
