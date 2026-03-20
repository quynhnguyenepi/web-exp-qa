# Sample: Create Branch from JIRA Ticket

---

## Input

User request: "Create a branch for CJS-10886"

---

## Step 0: Parse JIRA Ticket ID and Build Branch Name

```
Parsing input: "CJS-10886"
  - Ticket ID: CJS-10886

Getting git username:
  - git config user.name: "Phan Phuong Anh"
  - Checking remote branches for existing pattern...
  - Found: phanh/CJS-10804-add-new-ve-part2
  - Username resolved: phanh

Fetching ticket title via Atlassian MCP:
  - jira_get_issue({ issue_key: "CJS-10886" })
  - Title: "Apply Playwright for Automation Tests in CMS Repository"

Building branch name:
  - phanh/CJS-10886-apply-playwright-for-automation-tests

Confirming with user:
  > Branch name: phanh/CJS-10886-apply-playwright-for-automation-tests
  > Options: [Yes, proceed (Recommended)] [Use different name]

User selected: "Yes, proceed"
```

---

## Step 1: Checkout Default Branch and Pull Latest

```
Detecting default branch:
  - git symbolic-ref refs/remotes/origin/HEAD -> refs/remotes/origin/main
  - Default branch: main

Checking for uncommitted changes:
  - git status --porcelain -> (empty, no changes)

Checking out and pulling:
  - git checkout main
  - git pull
  - Already up to date.
```

---

## Step 2: Create and Checkout New Branch

```
Checking if branch exists:
  - git branch --list "phanh/CJS-10886-apply-playwright-for-automation-tests" -> (not found)

Creating branch:
  - git checkout -b phanh/CJS-10886-apply-playwright-for-automation-tests

Branch created successfully
  - Branch: phanh/CJS-10886-apply-playwright-for-automation-tests
  - Based on: main (latest)
  - Ticket: CJS-10886 - Apply Playwright for Automation Tests in CMS Repository

Ready to start working on CJS-10886.
```
