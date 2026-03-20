# Sample: Connect MCP in New Repo (Copy from Global)

## User Request

"Check MCP servers and connect them for this project"

---

## Step 0: Check MCP Package Installation

```
TodoWrite([
  { content: "Check MCP package installation (npx, uvx)", status: "in_progress", activeForm: "Checking MCP package installation" },
  { content: "Check .mcp.json in current repo", status: "pending", activeForm: "Checking .mcp.json in current repo" },
  { content: "Add .mcp.json if missing", status: "pending", activeForm: "Adding .mcp.json to repo" },
  { content: "Connect and test each MCP server", status: "pending", activeForm: "Testing MCP server connections" },
  { content: "Report connection status", status: "pending", activeForm: "Reporting connection status" }
])
```

```bash
npx --version    # 10.9.3
uvx --version    # uv 0.10.5
```

Checking MCP server installation...

```
MCP Package Check:

Package Managers:
- npx: 10.9.3 -- OK (github, figma, chrome-devtools, playwright, context7)
- uvx: uv 0.10.5 -- OK (atlassian, serena)

MCP Servers Installed: 7/7
- atlassian: installed
- github: installed
- figma: installed
- chrome-devtools: installed
- playwright: installed
- context7: installed
- serena: installed

All package managers available. All 7 MCP servers can be run.
```

---

# Sample 3: MCP Server Not Installed

## Step 0: Check MCP Package Installation

```bash
npx --version    # 10.9.3
uvx --version    # uv 0.10.5
```

Checking MCP server installation...

```
MCP Package Check:

Package Managers:
- npx: 10.9.3 -- OK
- uvx: uv 0.10.5 -- OK

MCP Servers Installed: 5/7

The following MCP servers are not installed:
- figma: Install from https://github.com/mcp/com.figma.mcp/mcp
- serena: Install from https://github.com/mcp/oraios/serena

Please install the missing servers from the links above, or continue with available servers only.
```

**AskUserQuestion:** "2 MCP servers are not installed. How would you like to proceed?"
- **"Continue with available servers only"**
- "Wait -- I'll install them first"

---

## Step 1: Check .mcp.json in Current Repo

```
TodoWrite: "Check MCP package installation" -> completed, "Check .mcp.json in current repo" -> in_progress
```

Detecting project root...
```bash
git rev-parse --show-toplevel
# /Users/dev/Documents/GIT/new-project
```

Checking for .mcp.json...
- `/Users/dev/Documents/GIT/new-project/.mcp.json` -- NOT FOUND

Checking global config...
- `~/.mcp.json` -- FOUND (6 servers)

```
No .mcp.json found in /Users/dev/Documents/GIT/new-project

Global config found at ~/.mcp.json with 6 servers:
- atlassian, github, figma, chrome-devtools, playwright, context7
```

**AskUserQuestion:** "How would you like to set up MCP for this repo?"
- **"Copy global config to this repo" (Recommended)**
- "Create fresh config"
- "Skip -- continue without .mcp.json"

**User selects:** "Copy global config to this repo"

---

## Step 2: Add .mcp.json

```
TodoWrite: "Check .mcp.json in current repo" -> completed, "Add .mcp.json if missing" -> in_progress
```

Reading `~/.mcp.json`...

Parsing 6 server configs:
- atlassian: uvx mcp-atlassian (token configured)
- github: npx @modelcontextprotocol/server-github (token configured)
- figma: npx mcp-figma (token configured)
- chrome-devtools: npx chrome-devtools-mcp@latest (no auth)
- playwright: npx @playwright/mcp@latest (no auth)
- context7: npx @upstash/context7-mcp (key configured)

No serena config in global -- skipping.

Writing to `/Users/dev/Documents/GIT/new-project/.mcp.json`...

Checking .gitignore...
- `.gitignore` exists
- `.mcp.json` not listed -- appending

```
.mcp.json copied to /Users/dev/Documents/GIT/new-project/.mcp.json

Servers configured: 6
.gitignore: .mcp.json added

Proceeding to test connections...
```

---

## Step 3: Connect and Test Each Server

```
TodoWrite: "Add .mcp.json if missing" -> completed, "Connect and test each MCP server" -> in_progress
```

Testing each server...

```
Testing atlassian...
  Call: mcp__atlassian__jira_get_all_projects
  Result: Connected (found 12 projects)

Testing github...
  Call: mcp__github__search_repositories (query: "test", perPage: 1)
  Result: Connected (search working)

Testing figma...
  Call: mcp__figma__check_api_key
  Result: Connected (API key valid)

Testing chrome-devtools...
  Call: mcp__chrome-devtools__list_pages
  Result: Connected (3 pages open)

Testing playwright...
  Call: mcp__playwright__browser_tabs (action: list)
  Result: Connected (browser ready)

Testing context7...
  Call: mcp__context7__resolve-library-id (libraryName: "react")
  Result: Connected (documentation lookup working)
```

All 6 tests completed.

---

## Step 4: Report Connection Status

```
TodoWrite: "Connect and test each MCP server" -> completed, "Report connection status" -> in_progress
```

```
MCP Server Connection Status

Project: /Users/dev/Documents/GIT/new-project
Config: /Users/dev/Documents/GIT/new-project/.mcp.json
.gitignore: .mcp.json protected

+-----+------------------+-----------+----------------------------------+
| #   | Server           | Status    | Details                          |
+-----+------------------+-----------+----------------------------------+
| 1   | atlassian        | Connected | Found 12 projects                |
| 2   | github           | Connected | Search working                   |
| 3   | figma            | Connected | API key valid                    |
| 4   | chrome-devtools  | Connected | 3 pages open                     |
| 5   | playwright       | Connected | Browser ready                    |
| 6   | context7         | Connected | Documentation lookup working     |
+-----+------------------+-----------+----------------------------------+

Summary: 6/6 servers connected

All MCP servers are connected and working!

Your Claude Code environment is fully set up.
All skills that depend on MCP servers will work correctly.
```

```
TodoWrite: "Report connection status" -> completed
```

---

# Sample 2: Partial Failure with Fix Instructions

## Step 4 (alternate): Some Servers Failed

```
MCP Server Connection Status

Project: /Users/dev/Documents/GIT/new-project
Config: /Users/dev/Documents/GIT/new-project/.mcp.json
.gitignore: .mcp.json protected

+-----+------------------+-----------+----------------------------------+
| #   | Server           | Status    | Details                          |
+-----+------------------+-----------+----------------------------------+
| 1   | atlassian        | Connected | Found 12 projects                |
| 2   | github           | Failed    | Auth failed (401 Unauthorized)   |
| 3   | figma            | Connected | API key valid                    |
| 4   | chrome-devtools  | Failed    | Chrome not running               |
| 5   | playwright       | Connected | Browser ready                    |
| 6   | context7         | Connected | Documentation lookup working     |
+-----+------------------+-----------+----------------------------------+

Summary: 4/6 servers connected, 2 failed

Fix Instructions for Failed Servers:

github (Failed: Auth failed - 401 Unauthorized)
  Your GitHub personal access token may be expired or invalid.
  1. Generate a new token: https://github.com/settings/tokens
  2. Required scopes: repo, read:org, read:user
  3. Update .mcp.json: replace GITHUB_PERSONAL_ACCESS_TOKEN value
  4. Restart Claude Code and run /common-qa:connect-mcp again

chrome-devtools (Failed: Chrome not running)
  Chrome DevTools MCP requires Chrome browser to be running.
  1. Open Google Chrome
  2. Restart Claude Code
  3. Run /common-qa:connect-mcp again

The following skills may not work until failed servers are fixed:
- /exp-qa-agents:review-github-pr-cypress-js (requires: github)
- /exp-qa-agents:create-pr (requires: github)

Run /common-qa:connect-mcp again after fixing to re-check.
```
