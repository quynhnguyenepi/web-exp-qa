# Connect MCP Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## MCP Server Installation Check Table

For Step 0, item 5 -- verify each package is installed and provide install links if missing:

| Server | Check Command | Install Link (if not installed) |
|--------|--------------|-------------------------------|
| atlassian | `uvx mcp-atlassian --help 2>/dev/null` | https://github.com/mcp/com.atlassian/atlassian-mcp-server |
| github | `npx -y @modelcontextprotocol/server-github --help 2>/dev/null` | https://github.com/mcp/github/github-mcp-server |
| figma | `npx -y mcp-figma --help 2>/dev/null` | https://github.com/mcp/com.figma.mcp/mcp |
| chrome-devtools | `npx -y chrome-devtools-mcp --help 2>/dev/null` | https://github.com/mcp/ChromeDevTools/chrome-devtools-mcp |
| playwright | `npx -y @playwright/mcp --help 2>/dev/null` | https://github.com/mcp/microsoft/playwright-mcp |
| context7 | `npx -y @upstash/context7-mcp --help 2>/dev/null` | https://github.com/mcp/upstash/context7 |
| serena | `uvx serena --help 2>/dev/null` | https://github.com/mcp/oraios/serena |

If any server is not installed, display:
```
The following MCP servers are not installed:
- {server_name}: Install from {install_link}
```

Ask user to install missing servers before proceeding, or continue with available servers only.

---

## Bash Commands for Finding npx/uvx/Python (Step 0)

### Find npx (Node.js)
```bash
# Try PATH first, then common locations
which npx 2>/dev/null || \
ls ~/.nvm/versions/node/*/bin/npx 2>/dev/null | tail -1 || \
ls /opt/homebrew/bin/npx 2>/dev/null || \
ls /usr/local/bin/npx 2>/dev/null || \
echo "NOT_FOUND"
```
- Record the **absolute path** to npx (e.g., `/Users/user/.nvm/versions/node/v22.18.0/bin/npx`)
- Record the **node directory** (dirname of npx) -- needed for PATH env fix later
- If not found: warn user, record as missing

### Find uvx (uv/Python)
```bash
which uvx 2>/dev/null || \
ls ~/.local/bin/uvx 2>/dev/null || \
ls /opt/homebrew/bin/uvx 2>/dev/null || \
echo "NOT_FOUND"
```
- Record the **absolute path** to uvx
- If not found: warn user, provide install command (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Check Python Version
```bash
python3 --version 2>/dev/null
# Search for newer Python via Homebrew
ls /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 /opt/homebrew/bin/python3.11 2>/dev/null | head -1
```
- If system Python < 3.10, record the **Homebrew Python path** (e.g., `/opt/homebrew/bin/python3.13`)
- This will be used as `--python` flag for uvx commands in `.mcp.json`

### Check macOS PATH State
```bash
echo "PATH=$PATH"
```
- If PATH is minimal (`/usr/bin:/bin:/usr/sbin:/sbin` only), set `NEEDS_PATH_FIX=true`
- This determines whether `.mcp.json` needs absolute paths and PATH env vars

---

## Auto-Fix Procedure (Step 2)

### Detailed Steps

1. **Read and parse `.mcp.json`**

2. **For each server entry, check and fix the `command` field:**

   **npx servers** (github, figma, chrome-devtools, playwright, context7):
   - If `command` is `"npx"` (relative), replace with absolute path found in Step 0
   - Add/update `env.PATH` to include the node directory so `node` is findable:
     ```json
     "env": {
       "PATH": "{NODE_DIR}:/usr/bin:/bin:/usr/sbin:/sbin",
       ...existing env vars...
     }
     ```

   **uvx servers** (atlassian, serena):
   - If `command` is `"uvx"` (relative), replace with absolute path found in Step 0
   - If Python < 3.10, add `"--python", "{HOMEBREW_PYTHON_PATH}"` as the first two args (before the package name)
   - Check if `--python` already exists in args to avoid duplicating

3. **Write the fixed `.mcp.json`**

4. **Apply same fixes to `~/.mcp.json` (global config)** so future repos inherit the fix

5. **Report:**
   ```
   Auto-fix applied to .mcp.json:
   - npx commands: absolute path + PATH env ({N} servers fixed)
   - uvx commands: absolute path + Python 3.13 ({N} servers fixed)
   - Global ~/.mcp.json: also updated
   ```

### Example of a Fixed Server Entry

```json
"github": {
  "command": "/Users/user/.nvm/versions/node/v22.18.0/bin/npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_...",
    "PATH": "/Users/user/.nvm/versions/node/v22.18.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
  }
}
```

---

## ToolSearch Batch Call (Step 3, Phase 1)

Load all MCP tools at once:
```
ToolSearch("select:mcp__atlassian__jira_get_all_projects,mcp__github__search_repositories,mcp__figma__check_api_key,mcp__playwright__browser_tabs,mcp__context7__resolve-library-id,mcp__chrome-devtools__list_pages,mcp__serena__list_dir")
```

- If a tool is NOT found, that server is `Failed` (not loaded by Claude Code)
- If a tool IS found, proceed to Phase 2

---

## Server Test Table (Step 3, Phase 2)

Call each loaded tool directly (all in parallel):

| Server | Test Call | Success Criteria |
|--------|----------|-----------------|
| atlassian | `mcp__atlassian__jira_get_all_projects()` | Returns project data (may be large) |
| github | `mcp__github__search_repositories(query: "optimizely", perPage: 1)` | Returns `total_count` > 0 |
| figma | `mcp__figma__check_api_key()` | Returns "API key is configured" |
| chrome-devtools | `mcp__chrome-devtools__list_pages()` | Returns page list (empty OK) |
| playwright | `mcp__playwright__browser_tabs(action: "list")` | Returns tab list |
| context7 | `mcp__context7__resolve-library-id(query: "react library", libraryName: "react")` | Returns library results |
| serena | `mcp__serena__list_dir(relative_path: ".", recursive: false)` | Returns directory listing |

---

## Detailed Report Template (Step 4)

```
MCP Server Connection Status

Project: {PROJECT_ROOT}
Config: {PROJECT_ROOT}/.mcp.json
.gitignore: .mcp.json protected

+-----+------------------+-------------+------------------------------------------+
| #   | Server           | Status      | Details                                  |
+-----+------------------+-------------+------------------------------------------+
| 1   | atlassian        | Connected   | Returned projects                        |
| 2   | github           | Connected   | Search returned results                  |
| 3   | figma            | Connected   | API key valid (figd_...****)              |
| 4   | chrome-devtools  | Connected   | DevTools ready                           |
| 5   | playwright       | Connected   | Browser tab ready                        |
| 6   | context7         | Connected   | Documentation lookup returned results    |
| 7   | serena           | Connected   | Project directory listing returned       |
+-----+------------------+-------------+------------------------------------------+

Summary: 7/7 servers connected
```

---

## Error-Fix Table (Step 4, Item 3)

If SOME servers failed, provide fix instructions per error type:

| Error | Fix |
|-------|-----|
| Package manager not found | Install npx (Node.js) or uvx (`curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| Authentication failed | Regenerate token, update .mcp.json |
| Connection timeout | Check network, firewall, proxy settings |
| Server not configured | Add to .mcp.json or run `/common-qa:connect-mcp` |
| Server not installed | Install from GitHub MCP marketplace (see links in "MCP Server Installation Check Table" above) |
| Chrome not running | Open Chrome browser |
| Browser not installed | Run `npx playwright install` |
| Token expired | Generate new token and update .mcp.json |
| Python too old for uvx | Install Python 3.13 via Homebrew: `brew install python@3.13` |
| Config just updated | Restart Claude Code, then re-run `/common-qa:connect-mcp` |

---

## Serena Path Replacement Rules

When copying global config to a project, the serena `--project` argument must be updated.

### What to Copy As-Is

These server configs are identical across projects:
- **atlassian** -- credentials are user-level, not project-specific
- **github** -- PAT works across all repos
- **figma** -- PAT works across all files
- **chrome-devtools** -- no credentials, universal
- **playwright** -- no credentials, universal
- **context7** -- API key works globally

### What to Update

- **serena** -- the `--project` argument must be updated to the current project path

**Serena path replacement:**
```json
// Before (from global config):
"--project", "/Users/user/Documents/GIT/other-project"

// After (updated for current project):
"--project", "/Users/user/Documents/GIT/current-project"
```

**Detection rule:** In the serena `args` array, find the element after `"--project"` and replace it with the current project root path.

---

## Connection Test Error Classification

### Handling Test Results

**Connected:** Test call succeeded, server is operational.

**Failed:** Test call returned an error. Classify the error:

| Error Pattern | Classification | User-Friendly Message |
|--------------|---------------|----------------------|
| `not configured` / `not available` | Not Configured | Server not found in .mcp.json |
| `401` / `403` / `authentication` | Auth Failed | Token expired or invalid |
| `timeout` / `ETIMEDOUT` | Timeout | Network issue or server down |
| `ECONNREFUSED` | Not Running | Server process not started |
| `command not found` / `npx`/`uvx` | Package Missing | Package manager not installed |
| MCP package not found / not installed | Not Installed | Install from GitHub MCP marketplace (see decision tree) |
| Browser-specific errors | Browser Issue | Chrome not running / browsers not installed |

### Browser-Specific Considerations

**Chrome DevTools:**
- Requires Chrome to be open with remote debugging
- May return empty page list (that's OK -- still means connected)
- If Chrome is not running, classify as "Browser Not Running" not "Failed"
- Fix: "Open Chrome browser, then retry"

**Playwright:**
- May need browser binaries installed first
- First-time use may trigger browser download
- Fix: `npx playwright install`

---

## Error Diagnosis Decision Tree

```
Server test failed
  |
  +-- Is the package manager (npx/uvx) installed?
  |     +-- No --> "Package Missing: install Node.js / uv"
  |     +-- Yes --> continue
  |
  +-- Is the MCP server package installed?
  |     +-- No --> "Not Installed: install from GitHub MCP marketplace"
  |     |         atlassian:      https://github.com/mcp/com.atlassian/atlassian-mcp-server
  |     |         github:         https://github.com/mcp/github/github-mcp-server
  |     |         figma:          https://github.com/mcp/com.figma.mcp/mcp
  |     |         chrome-devtools: https://github.com/mcp/ChromeDevTools/chrome-devtools-mcp
  |     |         playwright:     https://github.com/mcp/microsoft/playwright-mcp
  |     |         context7:       https://github.com/mcp/upstash/context7
  |     |         serena:         https://github.com/mcp/oraios/serena
  |     +-- Yes --> continue
  |
  +-- Is the server in .mcp.json?
  |     +-- No --> "Not Configured: add server to .mcp.json"
  |     +-- Yes --> continue
  |
  +-- Does the error mention auth/token/credentials?
  |     +-- Yes --> "Auth Failed: regenerate token"
  |     +-- No --> continue
  |
  +-- Does the error mention timeout/connection?
  |     +-- Yes --> "Connection Issue: check network"
  |     +-- No --> continue
  |
  +-- Is it a browser-based server?
  |     +-- chrome-devtools --> "Open Chrome with debugging"
  |     +-- playwright --> "Run: npx playwright install"
  |     +-- No --> continue
  |
  +-- Generic error
        +-- "Unknown Error: [error details]"
```

---

## Token Regeneration Links

Always provide these when auth fails:

| Server | Regeneration URL |
|--------|-----------------|
| atlassian | https://id.atlassian.com/manage-profile/security/api-tokens |
| github | https://github.com/settings/tokens |
| figma | Figma app > Settings > Account > Personal access tokens |
| context7 | https://context7.com |

---

## Skill Dependencies Mapping

When reporting failed servers, map them to skills that will be affected:

| MCP Server | Required By |
|-----------|------------|
| atlassian | `/common-qa:verify-bug-simple`, `/common-qa:mass-update-jira-tickets`, `/exp-qa-agents:create-bug-ticket`, `/exp-qa-agents:analyze-ticket`, `/exp-qa-agents:create-test-cases` |
| github | `/exp-qa-agents:review-github-pr-cypress-js`, `/exp-qa-agents:create-pr` |
| figma | `/common-qa:get-figma-screenshots` |
| playwright | `/common-qa:verify-bug-simple`, `/exp-qa-agents:execute-test-case` |
| chrome-devtools | (browser automation tasks) |
| context7 | (documentation lookup, not a hard dependency for any skill) |
| serena | (code navigation, not a hard dependency for any skill) |

---

## Re-test Strategy

When user asks to re-test only failed servers:

1. Keep the results from previously successful tests
2. Only re-run test calls for servers that were `Failed` or `Unavailable`
3. Update the status table with new results
4. Report changes: "Server X: Failed --> Connected"

---

## Output Formatting

### Status Indicators

Use text-based indicators (no emojis):

| Status | Indicator |
|--------|-----------|
| Connected | `Connected` |
| Auth Failed | `Failed (auth)` |
| Timeout | `Failed (timeout)` |
| Not Configured | `Not Configured` |
| Package Missing | `Unavailable` |
| Browser Issue | `Failed (browser)` |

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Check MCP package installation (npx, uvx)", status: "in_progress", activeForm: "Checking MCP package installation" },
  { content: "Check and configure .mcp.json", status: "pending", activeForm: "Checking .mcp.json" },
  { content: "Auto-fix macOS PATH issues in .mcp.json", status: "pending", activeForm: "Auto-fixing macOS PATH issues" },
  { content: "Connect and test each MCP server", status: "pending", activeForm: "Testing MCP server connections" },
  { content: "Report connection status", status: "pending", activeForm: "Reporting connection status" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| npx not found anywhere | Warn, list affected servers, provide nvm install instructions |
| uvx not found anywhere | Warn, provide install command |
| No Python >= 3.10 | Warn, suggest `brew install python@3.13` |
| .mcp.json not found | Offer to run `/common-qa:connect-mcp` |
| .mcp.json has invalid JSON | Back up file, warn user, offer to recreate |
| Server test call fails (auth) | Report "Auth Failed", show token regeneration link |
| Server test call fails (timeout) | Report "Timeout", suggest checking network |
| ToolSearch returns no MCP tools | Config was likely just updated; instruct restart |
| MCP server package not installed | Suggest install from GitHub MCP marketplace link (see Step 0, item 5) |
| .gitignore missing or unwritable | Warn user, show line to add manually |
| Serena project path wrong | Detect and auto-fix to current project path |

---


## Self-Correction

1. **"Re-test only the failed servers"** --> Re-run only failed server tests
2. **"Fix the token for github"** --> Open .mcp.json, update just the github token
3. **"Don't copy serena config"** --> Copy all servers except serena
4. **"Use a different global config path"** --> Accept custom path instead of `~/.mcp.json`
5. **"Skip the test, just copy the config"** --> Copy without running connection tests
6. **"Add a server that's not in global config"** --> Manually add the server entry
7. **"Remove a broken server"** --> Remove the server entry from .mcp.json

---


## Notes

### Key macOS Lessons (from real troubleshooting)

**Problem:** On macOS, VSCode launched from Spotlight/Dock inherits a minimal PATH (`/usr/bin:/bin:/usr/sbin:/sbin`). This causes three cascading failures:

1. **`npx` not found** -- it lives in `~/.nvm/versions/node/.../bin/`
2. **`node` not found by npx** -- even with absolute npx path, the `#!/usr/bin/env node` shebang in spawned scripts can't find `node` because the child process PATH is still minimal
3. **System Python too old** -- macOS ships Python 3.9.6, but `mcp-atlassian` requires >= 3.10

**Solution:** The auto-fix in Step 2 addresses all three:
- Absolute path for `command` (fixes #1)
- `PATH` env var with node directory (fixes #2)
- `--python /opt/homebrew/bin/python3.13` for uvx (fixes #3)

### MCP Server Test Calls

| Server | Test Call | What It Verifies |
|--------|----------|-----------------|
| atlassian | `jira_get_all_projects` | Auth token valid, Jira accessible |
| github | `search_repositories` (1 result) | PAT valid, API accessible |
| figma | `check_api_key` | PAT configured and valid |
| chrome-devtools | `list_pages` | DevTools connection established |
| playwright | `browser_tabs` (list) | Browser automation ready |
| context7 | `resolve-library-id` | API accessible, key valid |
| serena | `list_dir` (project root) | Server running, project indexed |

### Integration with Other Skills

- **`/common-qa:install-plugins`**: After connecting MCP, install plugins that use them
- **`/common-qa:verify-bug-simple`**: Requires atlassian + playwright to be connected
- **`/common-qa:mass-update-jira-tickets`**: Requires atlassian to be connected
- **`/exp-qa-agents:execute-test-case`**: Requires playwright to be connected
- **`/exp-qa-agents:create-bug-ticket`**: Requires atlassian to be connected
