---
description: Check MCP server installation status, verify .mcp.json exists in the current repo, copy it from global config if missing, auto-fix macOS PATH issues, then connect and test every MCP server. Use when onboarding a new repo, troubleshooting MCP connectivity, or verifying all servers are working.
---

## Dependencies

- **MCP Servers:** Atlassian, GitHub, Figma, Chrome DevTools, Playwright, Context7
- **Related Skills:** `/common-qa:connect-mcp`

# Connect MCP Servers

Diagnose and connect all MCP servers for the current repository. Checks if MCP packages are installed, verifies `.mcp.json` exists, copies global config if missing, auto-fixes macOS PATH issues, then connects and tests each server to confirm they are operational.

## When to Use

Invoke this skill when you need to:

- Check if all MCP servers are properly configured in the current repo
- Verify MCP connectivity after setting up a new project
- Troubleshoot "MCP server not available" errors
- Copy the `.mcp.json` from your global config (`~/.mcp.json`) to a new repo
- Confirm all MCP servers are working before running other skills
- Onboard a new repository so all Claude Code skills work immediately
- Diagnose which MCP servers are connected vs disconnected
- Auto-fix macOS PATH issues preventing MCP servers from starting

## Workflow Overview

```
Check Packages --> Check .mcp.json --> Add if Missing --> Auto-Fix Config --> Test Connections --> Report
```

## Execution Workflow

### Step 0: Check MCP Package Installation

**Todo:** Mark "Check MCP package installation" as `in_progress`.

1. **Find npx (Node.js)** -- search PATH, then common locations (`~/.nvm/versions/node/*/bin/npx`, `/opt/homebrew/bin/npx`, `/usr/local/bin/npx`). Record absolute path and node directory (needed for PATH env fix).

2. **Find uvx (uv/Python)** -- search PATH, then common locations (`~/.local/bin/uvx`, `/opt/homebrew/bin/uvx`). Record absolute path. If not found, provide install command.

3. **Check Python version for uvx servers (CRITICAL)** -- `mcp-atlassian` requires Python >= 3.10. macOS system Python is often 3.9.6. Search for Homebrew Python (`/opt/homebrew/bin/python3.13`, `python3.12`, `python3.11`). Record Homebrew Python path for use as `--python` flag in `.mcp.json`.

4. **Check macOS PATH state** -- if minimal (`/usr/bin:/bin:/usr/sbin:/sbin` only), set `NEEDS_PATH_FIX=true`.

5. **Check MCP server installation status** -- verify each package is installed. If not installed, provide GitHub MCP marketplace link. See **guidelines.md Section "MCP Server Installation Check Table"** for check commands and install links.

6. **Report package status:**
   ```
   MCP Package Check:
   - npx: {VERSION} at {ABSOLUTE_PATH}
   - uvx: {VERSION} at {ABSOLUTE_PATH}
   - Python: {VERSION} (Homebrew: {HOMEBREW_PYTHON_PATH})
   - PATH: {minimal / full}
   - Auto-fix needed: {yes / no}
   - MCP servers installed: {N}/7
   - Missing servers: {list with install links}
   ```

---

### Step 1: Check and Configure .mcp.json

**Todo:** Mark step as `in_progress`.

1. **Detect project root:** `git rev-parse --show-toplevel`

2. **Check for .mcp.json in project root.** If it exists, read and parse it, list configured servers. Skip to Step 2.

3. **If .mcp.json DOES NOT EXIST:**
   - Check for global config at `~/.mcp.json`
   - If global exists, ask user: Copy to repo (Recommended) | Create fresh | Skip
   - If no global either, ask: Set up now (run `/common-qa:connect-mcp`) | Skip

4. **When copying global config to project:**
   - Update Serena `--project` argument to current project path
   - Ensure `.mcp.json` is in `.gitignore`
   - Apply auto-fix (Step 2) before writing

---

### Step 2: Auto-Fix macOS PATH Issues in .mcp.json (CRITICAL)

**Todo:** Mark step as `in_progress`.

**IMPORTANT:** This step prevents the most common macOS failure mode. On macOS, Claude Code's VSCode extension often runs with a minimal PATH (`/usr/bin:/bin:/usr/sbin:/sbin`). MCP servers configured with bare `npx` or `uvx` commands will fail to start because:
1. `npx` is not in PATH (it's in `~/.nvm/versions/node/.../bin/`)
2. `uvx` is not in PATH (it's in `~/.local/bin/`)
3. Even with absolute path to npx, the spawned process uses `#!/usr/bin/env node` which can't find `node`
4. System Python 3.9.6 is too old for `mcp-atlassian` (requires >= 3.10)

**Auto-fix procedure** (see **guidelines.md Section "Auto-Fix Procedure"** for detailed steps and JSON examples):

1. Read and parse `.mcp.json`

2. For each server entry:
   - **npx servers** (github, figma, chrome-devtools, playwright, context7): Replace `"npx"` with absolute path, add `env.PATH` with node directory
   - **uvx servers** (atlassian, serena): Replace `"uvx"` with absolute path, add `--python {HOMEBREW_PYTHON_PATH}` if Python < 3.10

3. Write the fixed `.mcp.json`

4. Apply same fixes to `~/.mcp.json` (global config)

5. Report applied fixes

6. **If NEEDS_PATH_FIX is false** (PATH already has nvm/uvx), skip this step entirely.

---

### Step 3: Connect and Test All Servers

**Todo:** Mark step as `in_progress`.

**IMPORTANT: Use ToolSearch + direct MCP calls, NOT background agents.** Background agents cannot access MCP tools (they run in isolated contexts).

**Phase 1 -- Load all MCP tools via ToolSearch:**

Batch call to load all MCP tools at once. See **guidelines.md Section "ToolSearch Batch Call"** for the exact query.

**Phase 2 -- Call each loaded tool directly (all in parallel):**

See **guidelines.md Section "Server Test Table"** for test calls and success criteria for each server.

**Record results:**

| Status | Meaning |
|--------|---------|
| `Connected` | ToolSearch found it AND Phase 2 call succeeded |
| `Failed` | ToolSearch did not find the tool (server not loaded) |
| `Tool Available but Not Working` | ToolSearch found it but Phase 2 call returned error |
| `Not Configured` | Server not in .mcp.json |

**If servers are `Failed` after auto-fix was applied:** Config was just written and requires a Claude Code restart. Report: "Config updated. Restart Claude Code, then run `/common-qa:connect-mcp` again."

---

### Step 4: Report Connection Status

**Todo:** Mark step as `in_progress`.

1. **Build the status report** -- see **guidelines.md Section "Detailed Report Template"** for the full table format.

2. **If ALL connected:** "All MCP servers are connected and working!"

3. **If SOME failed** -- see **guidelines.md Section "Error-Fix Table"** for fix instructions per error type (package manager not found, authentication failed, connection timeout, server not configured, server not installed, Chrome not running, browser not installed, token expired, Python too old, config just updated).

4. **Mark step as `completed`.**

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
