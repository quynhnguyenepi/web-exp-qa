# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify GitHub access, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Fetch PR metadata", status: "pending", activeForm: "Fetching PR metadata" },
  { content: "Fetch changed files and diff", status: "pending", activeForm: "Fetching changed files" },
  { content: "Return structured output", status: "pending", activeForm: "Returning output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| GitHub MCP not available | Fall back to `gh` CLI |
| `gh` CLI not authenticated | Display `gh auth login` instructions, exit |
| PR not found (404) | Ask user to verify PR number and repo |
| Diff too large | Truncate at 5000 lines, note limitation |
| Rate limited | Wait 60 seconds, retry once |

---


## Self-Correction

1. **"Use a different repo"** -> Accept new repo_owner/repo_name, re-fetch
2. **"Show only specific files"** -> Filter changed files list
3. **"Get review comments too"** -> Fetch via `mcp__github__get_pull_request_comments`

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| GitHub | PR metadata, changed files | `gh` CLI |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| PR URL | `https://github.com/optimizely/app-ui/pull/123` |
| PR number + repo | `{ pr_number: 123, repo_owner: "optimizely", repo_name: "app-ui" }` |
| PR number only | `123` (resolves repo from git remote) |
