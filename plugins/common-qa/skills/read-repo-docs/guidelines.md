# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify GitHub access, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Fetch CLAUDE.md from target repo", status: "pending", activeForm: "Fetching CLAUDE.md" },
  { content: "Discover and fetch documentation files", status: "pending", activeForm: "Fetching documentation files" },
  { content: "Return structured output", status: "pending", activeForm: "Returning output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| GitHub MCP not available | Fall back to `gh` CLI |
| `gh` CLI not authenticated | Display `gh auth login` instructions, exit |
| Repo not found (404) | Ask user to verify repo owner/name |
| CLAUDE.md not found | Log warning, continue with other doc files |
| No documentation found at all | Return empty output with warning |
| File too large (>100KB) | Truncate content, note limitation |
| Rate limited | Wait 60 seconds, retry once |

---


## Self-Correction

1. **"Check a different branch"** -> Re-fetch from specified branch
2. **"Also read file X"** -> Fetch additional file, append to output
3. **"Use a different repo"** -> Accept new repo_owner/repo_name, re-fetch

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| GitHub | Fetch file contents from remote repo | `gh` CLI |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| Repo owner + name | `{ repo_owner: "optimizely", repo_name: "app-ui" }` |
| With branch | `{ repo_owner: "optimizely", repo_name: "app-ui", branch: "feature-x" }` |
| Specific files | `{ repo_owner: "optimizely", repo_name: "app-ui", specific_files: [".eslintrc.json", "tsconfig.json"] }` |
