# Test Cases for create-branch Skill

## TC-001: Create Branch from Ticket ID

**Input:** Run `/common-qa:create-branch` with input "CJS-10886".

**Expected:**
- Extracts ticket ID: CJS-10886
- Resolves git username
- Fetches ticket title from JIRA
- Builds branch name in correct format
- Asks user for confirmation
- Creates branch from latest default branch

**Pass Criteria:**
- Branch name follows `{username}/{TICKET-ID}-{kebab-case-title}` format
- Branch is based on latest main/master
- Confirmation shown before creation

---

## TC-002: Create Branch from JIRA URL

**Input:** Run with input "https://optimizely-ext.atlassian.net/browse/APPX-12506".

**Expected:**
- Parses URL and extracts ticket ID: APPX-12506
- Proceeds with normal workflow

**Pass Criteria:**
- Ticket ID correctly extracted from URL
- Branch created with correct ticket ID prefix

---

## TC-003: Uncommitted Changes Present

**Input:** Run when the working directory has uncommitted changes.

**Expected:**
- Detects uncommitted changes via `git status --porcelain`
- Asks user: stash, discard, or cancel
- If stash: runs `git stash` then proceeds
- If cancel: exits without switching branches

**Pass Criteria:**
- Uncommitted changes are not silently lost
- User is given explicit choice
- Selected action is performed correctly

---

## TC-004: Branch Already Exists

**Input:** Run when a branch with the generated name already exists locally.

**Expected:**
- Detects existing branch
- Asks user: switch to existing, delete and recreate, or cancel
- Performs selected action

**Pass Criteria:**
- Existing branch is not silently overwritten
- User chooses the action
- If recreated, based on latest default branch

---

## TC-005: Atlassian MCP Not Available

**Input:** Run when the Atlassian MCP server is not configured or unreachable.

**Expected:**
- Detects MCP is unavailable
- Asks user for a short description via AskUserQuestion
- Uses provided description for branch name

**Pass Criteria:**
- Graceful fallback, no crash
- Branch created with user-provided description
- Format still follows naming convention
