---
description: Read a target repo's CLAUDE.md and documentation files (coding conventions, best practices, anti-patterns) via GitHub MCP. Use when any skill needs to understand the target repo's structure, patterns, and conventions before analysis or code generation.
---

## Dependencies

- **MCP Servers:** GitHub
- **Related Skills:** `/exp-qa-agents:analyze-ticket`, `/exp-qa-agents:review-github-pr-cypress-js`, `/exp-qa-agents:create-test-scripts-cypress-js`

# Read Repository Documentation

Fetch a target repository's CLAUDE.md and related documentation files via GitHub MCP to understand the repo's coding conventions, architecture, best practices, and anti-patterns. Returns structured documentation context for downstream skills.

## When to Use

Invoke this skill when you need to:

- Read a target repo's CLAUDE.md to understand its structure and conventions
- Fetch coding conventions before reviewing a PR or generating code
- Get best practices and anti-patterns before test script generation
- Understand a repo's architecture before analyzing ticket changes

## Workflow Overview

```
Pre-Flight -> Fetch CLAUDE.md -> Discover Doc Files -> Fetch Doc Files -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:**
   - `repo_owner`: GitHub org or user (e.g., `optimizely`) -- required
   - `repo_name`: repository name (e.g., `app-ui`) -- required
   - `branch`: branch to read from (optional, defaults to repo's default branch)
   - `specific_files`: list of specific file paths to fetch (optional)
2. **Verify GitHub access:** Check if GitHub MCP is available via `mcp__github__get_file_contents`. If unavailable, fall back to `gh` CLI. If neither available, exit with error:
   ```
   Error: GitHub access is not configured

   This skill requires GitHub MCP server or GitHub CLI (gh).

   Setup Instructions:
   1. Ensure .mcp.json exists with GitHub server configuration, OR
   2. Install and authenticate GitHub CLI: gh auth login

   See .mcp.json.template for detailed configuration.
   ```

### Step 1: Fetch CLAUDE.md

Try multiple possible locations for the project's CLAUDE.md:

**Via GitHub MCP:**
```
mcp__github__get_file_contents({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  path: "CLAUDE.md",
  branch: "{BRANCH}"
})
```

If not found at root, try:
- `.claude/CLAUDE.md`
- `docs/CLAUDE.md`

**Fallback via gh CLI:**
```bash
gh api repos/{OWNER}/{REPO}/contents/CLAUDE.md --jq '.content' | base64 -d
```

If no CLAUDE.md exists, log warning and continue to doc files.

### Step 2: Discover and Fetch Documentation Files

Look for common documentation directories and files:

**Via GitHub MCP:**
```
mcp__github__get_file_contents({
  owner: "{REPO_OWNER}",
  repo: "{REPO_NAME}",
  path: ".claude/docs",
  branch: "{BRANCH}"
})
```

**Standard doc file paths to check:**
- `.claude/docs/coding-conventions.md`
- `.claude/docs/best-practices.md`
- `.claude/docs/anti-patterns.md`
- `.claude/docs/architecture.md`
- `.claude/docs/configuration.md`

If `specific_files` provided, fetch only those instead.

**Fetch each discovered file IN PARALLEL** using direct `mcp__github__get_file_contents` calls (no Agent tool needed — each is 1 MCP call):
- Call all `get_file_contents` in a single response message for parallel execution
- Skip files that return 404

### Step 3: Return Structured Output

---

## Output Format

```markdown
### Repository Documentation: {repo_owner}/{repo_name}

**Branch:** {branch}
**CLAUDE.md:** {Found / Not found}
**Doc files found:** {count}

### CLAUDE.md
{full CLAUDE.md content, or "Not found in this repository"}

### Coding Conventions
{coding-conventions.md content, or "Not found"}

### Best Practices
{best-practices.md content, or "Not found"}

### Anti-Patterns
{anti-patterns.md content, or "Not found"}

### Architecture
{architecture.md content, or "Not found"}

### Additional Files
{any other doc files found, with their content}
```

---


## Guidelines

### File Discovery

1. **Try multiple CLAUDE.md locations**: root, `.claude/`, `docs/`
2. **Standard doc file paths** to check:
   - `.claude/docs/coding-conventions.md`
   - `.claude/docs/best-practices.md`
   - `.claude/docs/anti-patterns.md`
   - `.claude/docs/architecture.md`
   - `.claude/docs/configuration.md`

3. **Fetch in parallel**: Call all `mcp__github__get_file_contents` in a single message (no Agent overhead).

### Content Handling

- Skip files that return 404 silently
- Truncate files >100KB with a note
- Return structured output with each file's content under its own heading

### Access Priority

1. GitHub MCP (`mcp__github__get_file_contents`) -- preferred
2. `gh` CLI (`gh api repos/{owner}/{repo}/contents/{path}`) -- fallback

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
