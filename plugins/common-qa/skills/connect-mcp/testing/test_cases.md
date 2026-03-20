# Test Cases for connect-mcp Skill

## TC-001: All Servers Connected (Happy Path)

**Input:** Run `/common-qa:connect-mcp` in a project with valid `.mcp.json` and all servers working.

**Expected:**
- Detects existing .mcp.json
- Skips Step 2 (adding config)
- Tests all servers
- All servers return "Connected"

**Pass Criteria:**
- All servers show "Connected" in status table
- Summary shows N/N connected
- Success message displayed
- No fix instructions needed

---

## TC-002: No .mcp.json in Repo, Global Exists

**Input:** Run in a repo without `.mcp.json`, but `~/.mcp.json` exists with 6 servers.

**Expected:**
- Detects missing project .mcp.json
- Finds global config
- Offers to copy
- After copy, tests all servers

**Pass Criteria:**
- Global config detected and listed
- User prompted for copy/create/skip
- After copy: .mcp.json exists in project root
- .mcp.json added to .gitignore
- All copied servers tested

---

## TC-003: No .mcp.json Anywhere

**Input:** Run in a repo without `.mcp.json`, and no `~/.mcp.json` exists.

**Expected:**
- Detects no config anywhere
- Offers to run /common-qa:connect-mcp or exit
- Does not attempt connection tests

**Pass Criteria:**
- Clear message about no config found
- Recommends /common-qa:connect-mcp
- No connection tests run
- No files modified

---

## TC-004: Copy Config with Serena Path Update

**Input:** Global `~/.mcp.json` includes serena with `--project /old/path`. Current project is `/new/path`.

**Expected:**
- Copies global config
- Updates serena `--project` argument to current project path
- Other server configs unchanged

**Pass Criteria:**
- Serena `--project` path is `/new/path` in new .mcp.json
- All other servers copied exactly as-is
- Updated path reported to user

---

## TC-005: Some Servers Fail Connection Test

**Input:** Run with valid .mcp.json but GitHub token is expired and Chrome is not running.

**Expected:**
- Tests all servers
- github returns "Failed (auth)"
- chrome-devtools returns "Failed (browser)"
- Other servers return "Connected"
- Fix instructions provided for each failure

**Pass Criteria:**
- Partial success reported (e.g., 5/7 connected)
- Failed servers have specific fix instructions
- Token regeneration link shown for github
- "Open Chrome" instruction for chrome-devtools
- Affected skills listed

---

## TC-006: npx Not Installed

**Input:** Run on system without Node.js/npx.

**Expected:**
- Detects npx missing in Step 0
- Warns about 5 affected servers
- Still checks uvx-based servers (atlassian, serena)
- Reports npx servers as "Unavailable"

**Pass Criteria:**
- Clear warning about npx
- Node.js install instructions provided
- uvx-based servers still tested
- npx-based servers marked "Unavailable"

---

## TC-007: uvx Not Installed

**Input:** Run on system without uv/uvx.

**Expected:**
- Detects uvx missing in Step 0
- Warns about 2 affected servers (atlassian, serena)
- Still checks npx-based servers
- Reports uvx servers as "Unavailable"

**Pass Criteria:**
- Clear warning about uvx
- Install command provided: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- npx-based servers still tested
- uvx-based servers marked "Unavailable"

---

## TC-008: Existing .mcp.json Has Invalid JSON

**Input:** Project .mcp.json exists but contains invalid JSON.

**Expected:**
- Detects parse error
- Backs up the invalid file
- Warns user about corruption
- Offers to copy from global or create fresh

**Pass Criteria:**
- Invalid JSON detected and reported
- Backup created (e.g., .mcp.json.bak)
- User given recovery options
- No crash or unhandled error

---

## TC-009: .gitignore Missing When Adding Config

**Input:** Copy global config to a repo that has no .gitignore file.

**Expected:**
- Creates `.gitignore` with `.mcp.json` as first line
- Proceeds normally

**Pass Criteria:**
- `.gitignore` created
- First line is `.mcp.json`
- Config file written successfully

---

## TC-010: .mcp.json Already in .gitignore

**Input:** Copy config to a repo that already has `.mcp.json` in `.gitignore`.

**Expected:**
- Detects `.mcp.json` is already gitignored
- Does NOT add duplicate entry
- Reports as "already protected"

**Pass Criteria:**
- No duplicate `.mcp.json` lines in .gitignore
- Status shows ".mcp.json protected"

---

## TC-011: User Cancels at Copy Prompt

**Input:** No project .mcp.json, global exists, user selects "Skip".

**Expected:**
- No config file created
- Tests whatever MCP is available (global config may still work)
- Reports status based on available servers

**Pass Criteria:**
- No files modified in project
- Connection tests may still run (using global config)
- Clear message about no project-level config

---

## TC-012: Re-test Failed Servers Only

**Input:** After initial run with 2 failed servers, user says "Re-test only the failed ones"

**Expected:**
- Keeps previous Connected results
- Only re-runs tests for failed servers
- Updates status table with new results

**Pass Criteria:**
- Previously connected servers not re-tested
- Failed servers re-tested
- Status table updated correctly
- Change report: "Server X: Failed --> Connected"

---

## TC-013: Merge New Config with Existing

**Input:** Project has .mcp.json with 3 servers. Global has 6 servers. User wants to merge.

**Expected:**
- Detects existing project config
- Identifies missing servers from global
- Offers to add missing servers
- Preserves existing project configs
- Adds new servers from global

**Pass Criteria:**
- Existing 3 servers unchanged
- Missing servers added from global
- Merged config has combined servers
- No credential conflicts

---

## TC-014: All Servers Fail

**Input:** Run with .mcp.json but all tokens are expired / services down.

**Expected:**
- Tests all servers
- All return "Failed"
- Fix instructions for each server
- Summary shows 0/N connected

**Pass Criteria:**
- Each failure has specific error and fix
- Recommend running /common-qa:connect-mcp to reconfigure
- No crash on total failure

---

## TC-015: MCP Server Package Not Installed

**Input:** Run `/common-qa:connect-mcp` on a system where npx/uvx are available but some MCP server packages are not installed.

**Expected:**
- Step 0 detects which MCP servers are not installed
- Provides GitHub MCP marketplace install link for each missing server
- Asks user whether to continue with available servers or wait
- If user continues, skips missing servers in connection tests

**Pass Criteria:**
- Each missing server listed with correct install link:
  - atlassian: https://github.com/mcp/com.atlassian/atlassian-mcp-server
  - github: https://github.com/mcp/github/github-mcp-server
  - figma: https://github.com/mcp/com.figma.mcp/mcp
  - chrome-devtools: https://github.com/mcp/ChromeDevTools/chrome-devtools-mcp
  - playwright: https://github.com/mcp/microsoft/playwright-mcp
  - context7: https://github.com/mcp/upstash/context7
  - serena: https://github.com/mcp/oraios/serena
- User prompted with continue/wait options
- Report shows `MCP servers installed: N/7`

---

## TC-016: Playwright Browser Not Installed

**Input:** Playwright MCP configured but browser binaries not downloaded.

**Expected:**
- Playwright test fails with browser-related error
- Specific fix: `npx playwright install`
- Other servers unaffected

**Pass Criteria:**
- Error correctly classified as "Browser Issue"
- Fix command `npx playwright install` displayed
- Other servers tested independently
