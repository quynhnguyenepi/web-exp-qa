# MCP Server Setup Guide

This repo includes a shared `.mcp.json.template` with MCP server configurations for the QA team. Copy it to `.mcp.json` for local use. Each server uses environment variable placeholders for credentials.

## Quick Setup

### 1. Set Environment Variables

Add these to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
# Required for Atlassian/JIRA MCP
export JIRA_URL="https://optimizely-ext.atlassian.net"
export JIRA_USERNAME="your.email@optimizely.com"
export JIRA_API_TOKEN="your_jira_api_token"

# Required for GitHub MCP
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_github_token"

# Optional - for Figma MCP
export FIGMA_PERSONAL_ACCESS_TOKEN="figd_your_figma_token"

# Optional - for Context7 MCP (works without key, but rate-limited)
export CONTEXT7_API_KEY="ctx7sk_your_context7_key"

# Required for Serena MCP - set to the project you want to index
export SERENA_PROJECT_PATH="/Users/your.name/Documents/GIT/your-project"

# macOS PATH fix - absolute paths for MCP binary resolution
# Find yours with: which npx && which uvx && ls /opt/homebrew/bin/python3.13
export NPX_PATH="$HOME/.nvm/versions/node/v22.18.0/bin/npx"       # or: which npx
export UVX_PATH="$HOME/.local/bin/uvx"                              # or: which uvx
export PYTHON3_PATH="/opt/homebrew/bin/python3.13"                  # or: which python3.13
export NODE_BIN_DIR="$HOME/.nvm/versions/node/v22.18.0/bin"        # dirname of npx
```

Then reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### 2. Get Your Tokens

| Token | Where to Get It |
|-------|-----------------|
| **JIRA API Token** | [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |
| **GitHub PAT** | [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens) |
| **Figma PAT** | [Figma Settings > Personal Access Tokens](https://www.figma.com/developers/api#access-tokens) |
| **Context7 Key** | [Context7](https://context7.com) (optional) |

### 3. GitHub PAT Required Scopes

When creating your GitHub Personal Access Token, select these scopes:
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)
- `admin:org` (Read org membership - for accessing optimizely repos)

## Available MCP Servers

| # | Server | Description | Credentials Required | Install Link |
|---|--------|-------------|---------------------|-------------|
| 1 | **atlassian** | JIRA integration - issues, transitions, test cases | JIRA_URL + JIRA_USERNAME + JIRA_API_TOKEN | [Install](https://github.com/mcp/com.atlassian/atlassian-mcp-server) |
| 2 | **github** | GitHub - repos, PRs, issues, code search | GITHUB_PERSONAL_ACCESS_TOKEN | [Install](https://github.com/mcp/github/github-mcp-server) |
| 3 | **figma** | Figma designs and components | FIGMA_PERSONAL_ACCESS_TOKEN | [Install](https://github.com/mcp/com.figma.mcp/mcp) |
| 4 | **chrome-devtools** | Browser automation with Chrome DevTools | None | [Install](https://github.com/mcp/ChromeDevTools/chrome-devtools-mcp) |
| 5 | **playwright** | E2E testing automation | None | [Install](https://github.com/mcp/microsoft/playwright-mcp) |
| 6 | **context7** | Documentation lookup for libraries | CONTEXT7_API_KEY (optional) | [Install](https://github.com/mcp/upstash/context7) |
| 7 | **serena** | Semantic code retrieval and editing | SERENA_PROJECT_PATH | [Install](https://github.com/mcp/oraios/serena) |

## Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| `JIRA_URL` | Yes | `https://optimizely-ext.atlassian.net` |
| `JIRA_USERNAME` | Yes | `your.email@optimizely.com` |
| `JIRA_API_TOKEN` | Yes | `ATATT3xFfGF0...` |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Yes | `ghp_...` |
| `FIGMA_PERSONAL_ACCESS_TOKEN` | Optional | `figd_...` |
| `CONTEXT7_API_KEY` | Optional | `ctx7sk-...` |
| `SERENA_PROJECT_PATH` | For Serena | `/absolute/path/to/project` |
| `NPX_PATH` | Yes (macOS) | `$HOME/.nvm/versions/node/v22.18.0/bin/npx` |
| `UVX_PATH` | Yes (macOS) | `$HOME/.local/bin/uvx` |
| `PYTHON3_PATH` | Yes (macOS) | `/opt/homebrew/bin/python3.13` |
| `NODE_BIN_DIR` | Yes (macOS) | `$HOME/.nvm/versions/node/v22.18.0/bin` |

## Enable/Disable Servers

In your project's `.claude/settings.local.json`:

```json
{
  "enableAllProjectMcpServers": true,
  "disabledMcpjsonServers": [
    "figma",
    "chrome-devtools"
  ]
}
```

## Serena Notes

Serena requires a **single absolute project path** -- it indexes one codebase for semantic code retrieval. To use it with different projects:

- Set `SERENA_PROJECT_PATH` to the project you're currently working on
- Change the variable and restart Claude Code when switching projects
- Or use per-project `.mcp.json` files (each with its own Serena path)

## Troubleshooting

- **MCP not loading?** Check env vars are set: `echo $GITHUB_PERSONAL_ACCESS_TOKEN`
- **Auth errors?** Regenerate your token and update the env var
- **Serena not connecting?** Verify path exists: `ls $SERENA_PROJECT_PATH`
- **Context7 rate limited?** Add a `CONTEXT7_API_KEY` for higher limits
- **Reload after changes:** Restart Claude Code or reload VSCode window

### macOS PATH Issues (Common)

On macOS, VSCode launched from Spotlight/Dock inherits a minimal PATH (`/usr/bin:/bin:/usr/sbin:/sbin`). This causes three failures:

1. **`npx` not found** -- lives in `~/.nvm/versions/node/.../bin/`
2. **`node` not found by npx** -- npx's `#!/usr/bin/env node` shebang can't resolve `node`
3. **System Python too old** -- macOS ships Python 3.9.6, but `mcp-atlassian` requires >= 3.10

**Fix:** The template uses absolute paths (`${NPX_PATH}`, `${UVX_PATH}`) and includes `PATH` env vars with the node directory. Set these env vars in your shell profile:

```bash
# Find your paths
which npx          # e.g., /Users/you/.nvm/versions/node/v22.18.0/bin/npx
which uvx          # e.g., /Users/you/.local/bin/uvx
which python3.13   # e.g., /opt/homebrew/bin/python3.13 (install via: brew install python@3.13)
```

**Alternative:** Launch VSCode from terminal (`code .`) to inherit your full PATH. But absolute paths in `.mcp.json` are more reliable.

## Skills That Use MCP

| Skill | Required MCP Servers |
|-------|---------------------|
| `/common-qa:connect-mcp` | (tests all servers) |
| `/exp-qa-agents:analyze-ticket` | atlassian, github (optional: figma) |
| `/exp-qa-agents:create-test-cases` | atlassian |
| `/exp-qa-agents:create-test-scripts-cypress-js` | atlassian |
| `/exp-qa-agents:create-bug-ticket` | atlassian |
| `/exp-qa-agents:create-pr` | github |
| `/exp-qa-agents:review-github-pr-cypress-js` | github |
| `/exp-qa-agents:execute-test-case` | playwright |
| `/exp-qa-agents:execute-test-suite` | playwright |
| `/exp-qa-agents:review-test-cases` | atlassian |
| `/exp-qa-agents:deploy-fresh-branch` | playwright |
| `/exp-qa-agents:inspect-and-create-page-objects-cypress-js` | playwright |
| `/common-qa:verify-bug-simple` | atlassian, playwright |
| `/common-qa:mass-update-jira-tickets` | atlassian |
| `/common-qa:get-figma-screenshots` | figma |

---
**Maintained by:** QA Team
