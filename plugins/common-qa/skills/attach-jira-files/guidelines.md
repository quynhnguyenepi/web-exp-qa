# Guidelines for attach-jira-files

## Credential Resolution (Priority Order)

1. **Environment variables** (checked first):
   - `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`
2. **MCP config fallback** (if env vars not set):
   - Parse `~/.mcp.json` for the `atlassian` MCP server entry
   - Extract `--jira-url`, `--jira-username`, `--jira-token` from the `args` array
   - This is the most common path since users typically configure the Atlassian MCP server but don't set separate env vars

## Upload Strategy

1. **Validate files before uploading**: Check existence, size, and readability.
2. **File discovery**: If user provides a partial filename, search `~/Desktop`, `~/Downloads`, `~/Documents` (maxdepth 3).
3. **Descriptive naming**: Use `rename_map` to give files meaningful names (e.g., `step-1-navigate.png`).
4. **Rate limiting**: Pause 500ms between uploads when more than 5 files.
5. **Large file handling**: Files up to ~250MB are supported by JIRA Cloud. For files >20MB, extend curl timeout to 5 minutes (`--max-time 300`).
6. **Error resilience**: Skip failed uploads, continue with remaining files, report all results.

## Authentication

Uses JIRA REST API v3 with Basic Auth:
- Credentials resolved from env vars OR `~/.mcp.json` (see priority order above)
- Uses `X-Atlassian-Token: no-check` header to bypass XSRF protection
- Base64-encodes `{username}:{token}` for the Authorization header

## Supported File Types

Screenshots (`.png`, `.jpg`, `.gif`), documents (`.pdf`, `.txt`, `.log`, `.csv`, `.json`, `.html`, `.xml`), archives (`.zip`), and videos (`.mov`, `.mp4`, `.webm`, `.avi`).

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Resolve JIRA credentials (env vars or MCP config)", status: "in_progress", activeForm: "Resolving JIRA credentials" },
  { content: "Find and validate files", status: "pending", activeForm: "Finding and validating files" },
  { content: "Upload files to JIRA ticket", status: "pending", activeForm: "Uploading files to JIRA ticket" },
  { content: "Report results", status: "pending", activeForm: "Reporting upload results" }
])
```

---


## Error Handling

| Error | Retryable? | Action |
|-------|:----------:|--------|
| JIRA credentials not found (env + MCP) | No | Exit with setup instructions for both methods |
| Ticket not found (404) | No | Stop retrying, ask user to verify ticket key |
| File not found | No | Search common locations (Desktop, Downloads, Documents); if still not found, ask user |
| File too large (>250MB) | No | Stop retrying, inform user of JIRA Cloud limit |
| Upload fails (401) | No | Stop retrying, check credentials source, suggest re-generating API token |
| Upload fails (403) | No | Stop retrying, ticket may not allow attachments, inform user |
| Upload fails (500/502/503) | Yes | Retry with exponential backoff until success. Ask user after 5 consecutive failures |
| Upload timeout | Yes | Retry with extended timeout (5 minutes) and exponential backoff until success |
| Network error / connection reset | Yes | Retry with exponential backoff until success. Ask user after 5 consecutive failures |
| Rate limited (429) | Yes | Wait for `Retry-After` header value (or 60s default), then retry until success |

---


## Self-Correction

1. **"Use different file names"** -> Accept new naming, re-upload
2. **"Attach to a different ticket"** -> Re-run with new issue_key
3. **"Only attach screenshots"** -> Filter file list by extension
4. **"Can't find the file"** -> Search Desktop, Downloads, Documents with broader pattern

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Verify ticket exists + credential extraction | Use env vars for credentials, skip verification |

### Credential Resolution

| Source | Priority | How |
|--------|----------|-----|
| Environment variables | 1st | `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` |
| MCP config file | 2nd | Parse `~/.mcp.json` > `mcpServers.atlassian.args` for `--jira-url`, `--jira-username`, `--jira-token` |

### Supported File Types

Any file type supported by JIRA: `.png`, `.jpg`, `.gif`, `.pdf`, `.txt`, `.log`, `.csv`, `.json`, `.html`, `.xml`, `.zip`, `.mov`, `.mp4`, `.webm`, `.avi`

### Input Flexibility

| Input Type | Example |
|------------|---------|
| Single file | `{ issue_key: "CJS-100", file_paths: ["/tmp/screenshot.png"] }` |
| Multiple files | `{ issue_key: "CJS-100", file_paths: ["/tmp/step-1.png", "/tmp/step-2.png"] }` |
| With renaming | `{ issue_key: "CJS-100", file_paths: ["/tmp/img1.png"], rename_map: {"img1.png": "login-page-error.png"} }` |
| Partial name | `{ issue_key: "DHK-4454", file_paths: ["Screen Recording 2026-03-11*"] }` |
| JIRA URL | `{ issue_key: "https://optimizely-ext.atlassian.net/browse/DHK-4454", file_paths: [...] }` |
