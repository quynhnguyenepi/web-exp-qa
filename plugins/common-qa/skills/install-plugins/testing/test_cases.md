# Test Cases for install-plugins Skill

## TC-001: Fresh Install from HTTPS URL

**Input:** Run `/common-qa:install-plugins` with URL `https://github.com/episerver/claude-qa-skills.git`

**Expected:**
- Validates URL format as HTTPS with .git suffix
- Extracts marketplace name `claude-qa-skills`
- Clones repo to `~/.claude/plugins/marketplaces/claude-qa-skills/`
- Reads marketplace.json and discovers all plugins
- Presents plugin list for confirmation
- Installs and enables all plugins
- Updates all three settings files
- Reports results with restart instruction

**Pass Criteria:**
- Marketplace registered in `extraKnownMarketplaces` and `known_marketplaces.json`
- All plugins registered in `installed_plugins.json`
- All plugins enabled in `enabledPlugins`
- Cache directories created with plugin contents
- User informed to restart Claude Code

---

## TC-002: Fresh Install from SSH URL

**Input:** Run with URL `git@github.com:optimizely/claude-plugins.git`

**Expected:**
- Validates URL format as SSH
- Extracts marketplace name `claude-plugins`
- Clones repo using SSH protocol
- Completes full installation flow

**Pass Criteria:**
- SSH URL preserved in settings files (not converted to HTTPS)
- Marketplace name correctly extracted from SSH format
- Clone successful with SSH authentication

---

## TC-003: URL Without .git Suffix

**Input:** Run with URL `https://github.com/NeoLabHQ/context-engineering-kit`

**Expected:**
- Accepts URL without .git suffix
- Does NOT add .git suffix
- Extracts marketplace name `context-engineering-kit`
- Clones successfully

**Pass Criteria:**
- URL used as-is (no .git appended)
- Clone works without .git suffix
- Marketplace name correctly extracted

---

## TC-004: Marketplace Already Installed (Update)

**Input:** Run with a marketplace URL that is already installed

**Expected:**
- Detects marketplace in `known_marketplaces.json`
- Informs user it is already installed
- Asks: Update / Reinstall / Cancel
- If "Update": pulls latest, re-caches plugins
- Updates version and timestamps in installed_plugins.json

**Pass Criteria:**
- Detection message includes current install location
- Pull updates the repository
- Plugin versions updated in installed_plugins.json
- Settings preserved (not duplicated)

---

## TC-005: Select Specific Plugins

**Input:** User chooses "Select specific plugins" and picks only 1 of 3 available

**Expected:**
- Presents all plugins for selection
- Installs only the selected plugin(s)
- Enables only selected plugin(s) in enabledPlugins
- Skipped plugins NOT registered in installed_plugins.json

**Pass Criteria:**
- Only selected plugin(s) in enabledPlugins
- Non-selected plugins not in cache
- Marketplace still registered (even if not all plugins installed)

---

## TC-006: Invalid URL

**Input:** Run with URL `not-a-valid-url`

**Expected:**
- Detects invalid URL format
- Displays accepted formats (HTTPS, SSH)
- Asks user to provide corrected URL
- Does not attempt to clone

**Pass Criteria:**
- Clear error message about invalid format
- No clone attempt made
- User prompted for corrected URL

---

## TC-007: Repository Not Found (404)

**Input:** Run with URL `https://github.com/nonexistent-org/nonexistent-repo.git`

**Expected:**
- Clone attempt fails
- Displays error about repository not found
- Suggests verifying the URL
- Does not modify any settings files

**Pass Criteria:**
- Git clone error captured and displayed
- No changes to settings files
- Clean exit with actionable error message

---

## TC-008: No marketplace.json in Repository

**Input:** Run with a valid git URL that points to a repo without `.claude-plugin/marketplace.json`

**Expected:**
- Clone succeeds
- Detects missing marketplace.json
- Displays error explaining this is not a valid marketplace
- Cleans up cloned directory
- Does not modify settings files

**Pass Criteria:**
- Error message mentions `.claude-plugin/marketplace.json`
- Cloned repo cleaned up (or kept with warning)
- No settings files modified

---

## TC-009: Plugin Missing plugin.json

**Input:** Run with a marketplace where one plugin's directory is missing `plugin.json`

**Expected:**
- Detects missing plugin.json for that plugin
- Warns user about the invalid plugin
- Continues installing other valid plugins
- Does not abort entire installation

**Pass Criteria:**
- Warning message for the invalid plugin
- Other plugins installed successfully
- Partial success reported with details

---

## TC-010: User Cancels at Confirmation

**Input:** User chooses "Cancel" at the plugin confirmation step

**Expected:**
- No plugins installed
- No settings files modified (marketplace not registered)
- Clean exit with message "Installation cancelled. No changes made."
- Cloned repo may remain (for future use) or be cleaned up

**Pass Criteria:**
- Zero changes to settings files
- Clear cancellation message
- No cache directories created

---

## TC-011: Natural Language Input

**Input:** "Add the marketplace from https://github.com/episerver/claude-qa-skills.git and install everything"

**Expected:**
- Extracts URL from natural language
- Proceeds with full installation flow
- Installs all plugins (user said "install everything")

**Pass Criteria:**
- URL correctly extracted from sentence
- Full installation completed
- "Install all" inferred from "install everything"

---

## TC-012: URL with Trailing Slash

**Input:** Run with URL `https://github.com/episerver/claude-qa-skills.git/`

**Expected:**
- Strips trailing slash
- Proceeds normally with cleaned URL
- Marketplace name correctly extracted

**Pass Criteria:**
- URL normalized (no trailing slash in settings)
- Clone works with normalized URL
- Marketplace name is `claude-qa-skills` (not empty string)

---

## TC-013: Git Not Installed

**Input:** Invoke on a system without git installed

**Expected:**
- Detects git is not available
- Displays error with install instructions
- Exits gracefully

**Pass Criteria:**
- Clear error message about git not found
- No partial state or file modifications
- Installation instructions provided
