---
description: Attach files (screenshots, logs, documents, videos) to a JIRA ticket via REST API. Use when you need to upload evidence files, screenshots, or any attachments to a JIRA issue.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** `/exp-qa-agents:create-bug-ticket`, `/exp-qa-agents:execute-test-case`

# Attach Files to JIRA Ticket

Upload one or more files (screenshots, logs, documents, videos) to a JIRA ticket using the JIRA REST API. Handles authentication with automatic credential discovery, file validation, and descriptive naming.

## When to Use

Invoke this skill when you need to:

- Attach screenshots from test execution to a bug ticket
- Upload log files, error reports, or screen recordings to a JIRA issue
- Attach any evidence files to a ticket after creation
- Bulk-attach multiple files to a single ticket

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Resolve Credentials → Validate Files → Upload Files → Report        │
│  (env vars or MCP)     (exist, size)    (REST API v3)   Results      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Simple Flow:**
```
Resolve Credentials → Find & Validate Files → Upload via JIRA REST API → Report Results
```

## Execution Workflow

### Step 0: Resolve JIRA Credentials

**Todo:** Mark "Resolve JIRA credentials" as `in_progress`.

1. **Validate input:**
   - `issue_key`: JIRA ticket key (e.g., `CJS-10873`, `DHK-4454`) -- required
   - `file_paths`: list of absolute file paths to attach -- required (can also be partial file names to search for)
   - `rename_map`: optional map of `{original_name: new_name}` for descriptive naming

2. **Resolve JIRA credentials** using this priority order:

   **Priority 1: Environment variables**
   ```
   JIRA_URL (e.g., https://optimizely-ext.atlassian.net)
   JIRA_USERNAME (email)
   JIRA_API_TOKEN
   ```

   **Priority 2: Extract from MCP config (`~/.mcp.json`)**
   If env vars are not set, extract credentials from the Atlassian MCP server config:
   ```bash
   python3 -c "
   import json
   d = json.load(open('$HOME/.mcp.json'))
   s = d['mcpServers']['atlassian']
   args = s.get('args', [])
   for i, a in enumerate(args):
       if a == '--jira-url': print(f'URL={args[i+1]}')
       if a == '--jira-username': print(f'USER={args[i+1]}')
       if a == '--jira-token': print(f'TOKEN={args[i+1]}')
   "
   ```
   Store the extracted values for use in the upload step.

   **If neither source has credentials**, exit with error:
   ```
   Error: JIRA credentials not found

   Checked:
   1. Environment variables: JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN (not set)
   2. MCP config: ~/.mcp.json > mcpServers > atlassian (not found)

   To fix: Configure the Atlassian MCP server or set environment variables.
   See .mcp.json.template for configuration details.
   ```

3. **Verify the ticket exists** via Atlassian MCP:
   ```
   mcp__atlassian__jira_get_issue({ issue_key: "{ISSUE_KEY}", fields: "summary" })
   ```

**Todo:** Mark "Resolve JIRA credentials" as `completed`, mark "Find and validate files" as `in_progress`.

### Step 1: Find and Validate Files

1. **Locate files:**
   - If full absolute paths are provided, use them directly
   - If partial names or filenames are provided, search common locations:
     ```bash
     find ~/Desktop ~/Downloads ~/Documents -maxdepth 3 -name "{filename_pattern}" 2>/dev/null
     ```
   - If multiple matches found, prefer the most recent file

2. **Validate each file:**
   - Check the file exists: `ls -la "{file_path}"`
   - Check file size (JIRA Cloud limit: ~250MB per file; warn if >100MB as upload may be slow)
   - If a file doesn't exist, log warning and skip it
   - If `rename_map` provided, map original filenames to descriptive names

**Todo:** Mark "Find and validate files" as `completed`, mark "Upload files to JIRA ticket" as `in_progress`.

### Step 2: Upload Files

For each valid file, upload via JIRA REST API v3 with retry-until-success:

```bash
curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: Basic $(echo -n '{USERNAME}:{API_TOKEN}' | base64)" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@{file_path}" \
  "{JIRA_URL}/rest/api/3/issue/{ISSUE_KEY}/attachments"
```

**Retry-Until-Success Logic (CRITICAL):**

For each file, repeat upload until it succeeds:

1. **Attempt upload** and capture HTTP status code from response
2. **If HTTP 200**: Upload succeeded. Log success, move to next file.
3. **If upload fails** (any non-200 status or network error):
   - Log the failure: `"Attempt {N} failed for {filename}: HTTP {status_code} - {error_message}"`
   - Apply exponential backoff: wait `min(2^attempt * 1s, 30s)` (1s, 2s, 4s, 8s, 16s, 30s, 30s...)
   - **Retry the same file** -- do NOT skip to the next file
   - After **5 consecutive failures for the same file**, ask the user via AskUserQuestion:
     ```
     Upload failed 5 times for "{filename}":
     Last error: HTTP {status_code} - {error_message}

     Options:
     1. Keep retrying (Recommended)
     2. Skip this file and continue with others
     3. Abort all uploads
     ```
   - If user selects "Keep retrying": reset attempt counter, continue retrying
   - If user selects "Skip": mark file as skipped, move to next file
   - If user selects "Abort": stop all uploads, report partial results

**Exception -- Do NOT retry these errors (they won't resolve with retries):**
- **HTTP 401**: Bad credentials. Stop retrying, ask user to check API token.
- **HTTP 404**: Ticket not found. Stop retrying, ask user to verify ticket key.
- **HTTP 403**: Permission denied. Stop retrying, inform user.
- **File >250MB**: JIRA Cloud hard limit. Stop retrying, inform user.

**Notes:**
- If `rename_map` provided, add `;filename={display_name}` to the `-F` parameter
- Default naming convention for screenshots: `step-{N}-{action}.png`
- Rate limit: pause 500ms between uploads if more than 5 files
- For large files (>20MB), use `--max-time 300` to allow up to 5 minutes for upload
- A successful upload returns HTTP 200 with JSON containing attachment metadata (id, filename, size)
- Use `-w "\n%{http_code}"` in curl to capture the HTTP status code for retry decisions

**Todo:** Mark "Upload files to JIRA ticket" as `completed`, mark "Report results" as `in_progress`.

### Step 3: Report Results

```markdown
### Attachment Results for {ISSUE_KEY}

| # | File | Status | Size | Attempts |
|---|------|--------|------|:--------:|
| 1 | step-1-navigate.png | Uploaded | 245KB | 1 |
| 2 | screen-recording.mov | Uploaded | 41.3MB | 3 |
| 3 | error-log.txt | Skipped (user) | 15KB | 5 |

**Uploaded:** {success_count}/{total_count} files
**Retried:** {retry_count} file(s) required retries
**Ticket:** https://optimizely-ext.atlassian.net/browse/{ISSUE_KEY}
```

**Todo:** Mark "Report results" as `completed`.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
