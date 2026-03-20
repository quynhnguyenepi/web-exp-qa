# Analyze PR Changes - Guidelines

## File Type Classification

| File Pattern | Category | Test Impact |
|-------------|----------|-------------|
| `*.tsx`, `*.jsx` | Components | UI rendering, visual regression |
| `*Store.ts`, `*store.ts` | Stores | State management, data flow |
| `*api/*.ts`, `*service*.ts` | Services | API integration, request/response |
| `constants.ts`, `enums.ts` | Config | Downstream usage, feature flags |
| `*.test.*`, `*.spec.*` | Tests | What devs already covered |
| `*.css`, `*.scss`, `*.styled.*` | Styles | Visual regression |
| `*.json` (non-test) | Config/Data | Settings, translations |
| `migrations/*` | Database | Data integrity |

## Hidden Change Detection

Look for these patterns in PR diffs that indicate changes beyond the AC:
- Refactored shared utilities (broad impact across features)
- Renamed event names or tracking constants
- Removed parameters from function calls (data moved elsewhere)
- New function calls or analytics events added
- Store behavior modifications (e.g., merge vs replace logic)
- Import path changes affecting multiple consumers
- Default value changes in configurations

## Scope Assessment Criteria

| Scope | File Count | Characteristics |
|-------|-----------|-----------------|
| **Isolated** | <5 files | Single feature, no shared code touched |
| **Moderate** | 5-15 files | Related features affected, some shared code |
| **Broad** | >15 files | Shared utilities, cross-cutting concerns, global properties |

## What Constitutes "Beyond AC"

A change is "beyond AC" if:
- The ticket AC does not mention it
- It modifies behavior in a different feature area
- It refactors code that other features depend on
- It adds/removes/renames things not described in the ticket
- It changes test infrastructure or shared utilities

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify MCP servers, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Find linked PRs via JIRA and git log", status: "pending", activeForm: "Finding linked PRs" },
  { content: "Fetch PR details and diffs", status: "pending", activeForm: "Fetching PR details" },
  { content: "Classify changes and assess scope", status: "pending", activeForm: "Classifying changes" },
  { content: "Return structured output", status: "pending", activeForm: "Returning output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| No PRs found (JIRA + git) | Return empty output with warning |
| GitHub MCP unavailable | Fall back to git log only, warn PR details limited |
| GitHub API rate limited | Wait 60 seconds, retry once |
| PR diffs too large | Summarize by file names and counts, note limitation |
| Atlassian dev info unavailable | Fall back to git log search |

---


## Self-Correction

1. **"Check another PR too"** -> Add PR number, fetch and classify
2. **"The scope should be broader"** -> Re-assess with user's reasoning
3. **"Use a different repo"** -> Accept new repo_owner/repo_name

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Find PRs via JIRA development info | Git log search |
| GitHub | Fetch PR details and diffs | Git log only (limited) |

### File Classification Reference

See guidelines.md for the complete file type classification table and hidden change detection patterns.

### Input Requirements

| Parameter | Required | Example |
|-----------|----------|---------|
| `issue_key` | Yes | `CJS-10873` |
| `repo_owner` | Yes | `optimizely` |
| `repo_name` | Yes | `app-ui` |
