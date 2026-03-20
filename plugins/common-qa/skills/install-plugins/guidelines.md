# Install Plugins Guidelines

Detailed reference material, verbose examples, and boilerplate content beyond the concise workflow in SKILL.md.

---

## Detailed Workflow Diagram

```
+------------------------------------------------------------------------------+
|                                                                              |
|  0. Pre-Flight Checks                                                       |
|     +-- Validate marketplace URL format                                     |
|     +-- Verify git is available                                             |
|     +-- Check Claude Code settings files exist                              |
|                                                                              |
|  1. Clone / Update Marketplace Repository                                   |
|     +-- Clone repo to ~/.claude/plugins/marketplaces/{name}/                |
|     +-- If already cloned, pull latest changes                              |
|     +-- Read .claude-plugin/marketplace.json                                |
|                                                                              |
|  2. Discover Plugins and Confirm                                            |
|     +-- Parse marketplace.json for plugin list                              |
|     +-- Present plugins with descriptions to user                           |
|     +-- Ask user to confirm installation (default: install all)             |
|                                                                              |
|  3. Install and Enable Plugins                                              |
|     +-- Register marketplace in settings.json (extraKnownMarketplaces)      |
|     +-- Register in known_marketplaces.json                                 |
|     +-- For each plugin: read plugin.json, cache, register                  |
|     +-- Enable each plugin in settings.json (enabledPlugins)                |
|                                                                              |
|  4. Verify and Report                                                       |
|     +-- Verify settings files updated correctly                             |
|     +-- List all installed plugins and their skills                         |
|     +-- Advise user to restart Claude Code                                  |
|                                                                              |
+------------------------------------------------------------------------------+
```

---

## Step 0: Detailed Pre-Flight Procedures

### URL Normalization Rules

Accept and normalize these formats:
- HTTPS with .git: `https://github.com/org/repo.git`
- HTTPS without .git: `https://github.com/org/repo` --> add `.git`
- SSH format: `git@github.com:org/repo.git`
- Strip trailing slashes

### Pre-Flight Report Template

```
Pre-flight checks passed
   - URL: {MARKETPLACE_URL}
   - Marketplace name: {MARKETPLACE_NAME}
   - Git: Available (version {VERSION})
   - Settings: Valid
   - Already installed: {Yes/No}

Proceeding to clone repository...
```

If already installed:
```
Marketplace "{name}" is already installed at {installLocation}.

Options:
1. Update existing marketplace (Recommended) -- Pull latest and reinstall plugins
2. Reinstall from scratch -- Remove and re-clone
3. Cancel -- Exit
```

---

## Step 1: Detailed Clone Procedures

### Clone Commands

**If NOT already cloned:**
```bash
git clone {MARKETPLACE_URL} ~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/
```

**If already cloned (update):**
```bash
cd ~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/ && git pull
```

**If reinstall from scratch:**
```bash
rm -rf ~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/
git clone {MARKETPLACE_URL} ~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/
```

### Clone Report Template

```
Repository cloned successfully
   - Location: {CLONE_PATH}
   - Marketplace: {MARKETPLACE_JSON_NAME}
   - Description: {DESCRIPTION}
   - Plugins found: {N}
   - Commit: {SHORT_SHA}

Proceeding to discover plugins...
```

---

## Step 2: Detailed Plugin Discovery

### Plugin Discovery Output Template

```
Marketplace: {MARKETPLACE_JSON_NAME}
Description: {DESCRIPTION}

Plugins to install:

1. {PLUGIN_1_NAME} (v{VERSION})
   {DESCRIPTION}
   Skills: {SKILL_1}, {SKILL_2}, {SKILL_3}

2. {PLUGIN_2_NAME} (v{VERSION})
   {DESCRIPTION}
   Skills: {SKILL_1}, {SKILL_2}

3. {PLUGIN_3_NAME} (v{VERSION})
   {DESCRIPTION}
   Skills: (none yet)

Total: {N} plugins, {M} skills
```

---

## Step 3: Detailed JSON Registration Templates

### settings.json: extraKnownMarketplaces Format

```json
{
  "extraKnownMarketplaces": {
    "{marketplace-name}": {
      "source": {
        "source": "git",
        "url": "{git-url}"
      }
    }
  }
}
```

**Rules:**
- Use the marketplace name from marketplace.json, NOT the repo name (they may differ)
- For git sources, always set `"source": "git"`
- Use the original URL provided by the user (preserve HTTPS/SSH format)

### settings.json: enabledPlugins Format

```json
{
  "enabledPlugins": {
    "{plugin-name}@{marketplace-name}": true
  }
}
```

**Rules:**
- Key format is `{plugin-name}@{marketplace-name}`
- Plugin name comes from the plugin's `plugin.json` `name` field
- Marketplace name comes from `marketplace.json` `name` field
- Set to `true` to enable, `false` to disable

### known_marketplaces.json Format

```json
{
  "{marketplace-name}": {
    "source": {
      "source": "git",
      "url": "{git-url}"
    },
    "installLocation": "/Users/{user}/.claude/plugins/marketplaces/{marketplace-name}",
    "lastUpdated": "2026-03-04T10:00:00.000Z"
  }
}
```

**Rules:**
- `installLocation` must be the absolute path (expand `~` to full home directory)
- `lastUpdated` must be ISO 8601 format with timezone
- Use `new Date().toISOString()` equivalent for timestamp

### installed_plugins.json Format

```json
{
  "version": 2,
  "plugins": {
    "{plugin-name}@{marketplace-name}": [
      {
        "scope": "user",
        "installPath": "/Users/{user}/.claude/plugins/cache/{marketplace-name}/{plugin-name}/{version}",
        "version": "{version}",
        "installedAt": "{ISO_TIMESTAMP}",
        "lastUpdated": "{ISO_TIMESTAMP}",
        "gitCommitSha": "{full-sha}"
      }
    ]
  }
}
```

**Rules:**
- Always use `"version": 2` at the top level
- `scope` is always `"user"` for user-level installations
- `installPath` must be the absolute path to the cached plugin directory
- `version` comes from the plugin's `plugin.json` `version` field
- `gitCommitSha` is the full 40-character SHA of the cloned repo HEAD
- If a plugin already exists in the list, replace the array entry (do not append)

### Cache Directory Creation

```bash
# Create cache dir
mkdir -p ~/.claude/plugins/cache/{marketplace}/{plugin}/{version}

# Copy plugin contents including hidden directories
cp -r {clone-path}/{plugin-source}/. ~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/
```

**IMPORTANT**: Use `/.` at the end of the source path to copy contents including hidden files/directories.

---

## Step 4: Detailed Verification and Final Report

### Final Report Template

```
Installation complete!

Marketplace: {MARKETPLACE_NAME}
Source: {MARKETPLACE_URL}
Location: ~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/

Installed Plugins:
+-----+------------------+---------+--------+
| #   | Plugin           | Version | Skills |
+-----+------------------+---------+--------+
| 1   | {PLUGIN_1_NAME}  | {VER}   | {N}    |
| 2   | {PLUGIN_2_NAME}  | {VER}   | {N}    |
| 3   | {PLUGIN_3_NAME}  | {VER}   | {N}    |
+-----+------------------+---------+--------+

Total: {N} plugins installed, {M} skills available

Available Skills:
- /{PLUGIN_1}:{SKILL_A}
- /{PLUGIN_1}:{SKILL_B}
- /{PLUGIN_2}:{SKILL_C}
...

IMPORTANT: Restart Claude Code (close and reopen VS Code) for the new plugins to take effect.
After restart, the new skills will appear in the skill list and can be invoked with /{plugin}:{skill}.
```

---

## settings.json Editing Rules

**CRITICAL**: The `~/.claude/settings.json` file may contain sensitive data (API keys, tokens). Handle with care.

1. **Always read before writing** -- Never overwrite without reading current content
2. **Preserve all existing keys** -- Only add/update specific keys, never remove existing ones
3. **Use JSON merge strategy** -- Merge new data with existing data, do not replace entire objects
4. **Back up before modifying** -- Create a backup: `cp settings.json settings.json.bak.{timestamp}`

---

## Clone and Cache Strategy

### Clone Location

All marketplace repos are cloned to:
```
~/.claude/plugins/marketplaces/{marketplace-name}/
```

### Cache Location

Each plugin is cached at:
```
~/.claude/plugins/cache/{marketplace-name}/{plugin-name}/{version}/
```

### Copy Strategy

When caching a plugin:
1. Create the cache directory
2. Copy all contents from the plugin source directory
3. Ensure `.claude-plugin/` directory is included (it starts with `.` so may be missed by simple cp)
4. Verify `plugin.json` exists in the cached `.claude-plugin/` directory

---

## Safety Rules

### Before Modifying Settings

1. **Back up settings.json**: Always create a backup before modifying
2. **Validate JSON**: After modifications, validate the JSON is well-formed
3. **Atomic writes**: Write to a temp file first, then move into place
4. **Preserve permissions**: Maintain original file permissions

### Conflict Handling

| Scenario | Action |
|----------|--------|
| Marketplace name already exists in extraKnownMarketplaces | Update the URL, preserve other settings |
| Plugin name already exists in enabledPlugins | Keep existing enabled/disabled state unless user says otherwise |
| Plugin already in installed_plugins.json | Update version, installPath, SHA |
| Cache directory already exists | Remove old cache, create fresh copy |
| settings.json has conflicting marketplace name | Ask user which to keep |

### Rollback Plan

If installation fails mid-way:
1. Restore settings.json from backup
2. Restore known_marketplaces.json from backup
3. Restore installed_plugins.json from backup
4. Remove partially cloned repository
5. Report what failed and what was rolled back

---

## Marketplace Validation

### marketplace.json Schema

```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "owner": {
    "name": "string (optional)",
    "email": "string (optional)"
  },
  "plugins": [
    {
      "name": "string (required)",
      "source": "string (required, relative path)",
      "description": "string (optional)"
    }
  ]
}
```

### plugin.json Schema

```json
{
  "name": "string (required)",
  "version": "string (required, semver)",
  "description": "string (optional)",
  "skills": ["string (required, path to skills directory)"]
}
```

### Plugin Validation

Each plugin referenced in marketplace.json must have:
- A directory at the path specified by `source`
- `.claude-plugin/plugin.json` inside that directory
- A `skills/` directory (may be empty)

---

## Home Directory Expansion

**CRITICAL**: When writing paths to JSON files, always expand `~` to the full home directory path.

```bash
# Get the home directory
echo $HOME
# or
echo ~
```

Use the expanded path in all JSON files:
- `/Users/username/.claude/plugins/...` (macOS)
- `/home/username/.claude/plugins/...` (Linux)

---

## Restart Requirement

After installing plugins, Claude Code must be restarted for changes to take effect. Always inform the user:

```
IMPORTANT: Restart Claude Code for the new plugins to take effect.
- VS Code: Close and reopen VS Code
- CLI: Exit and restart the claude command

After restart, new skills will be available with /{plugin-name}:{skill-name} syntax.
```

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (validate URL, verify git, check settings)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Clone or update marketplace repository", status: "pending", activeForm: "Cloning marketplace repository" },
  { content: "Discover plugins and confirm with user", status: "pending", activeForm: "Discovering plugins" },
  { content: "Install and enable all plugins", status: "pending", activeForm: "Installing and enabling plugins" },
  { content: "Verify installation and report results", status: "pending", activeForm: "Verifying installation" }
])
```

**Update rules:**
- Mark current step as `in_progress` when starting it
- Mark step as `completed` immediately when finished (do not batch)
- Only ONE step should be `in_progress` at any time

---


## Error Handling

| Error | Action |
|-------|--------|
| Invalid URL format | Display accepted formats, ask user for corrected URL |
| Git not installed | Display install instructions, exit |
| Git clone fails (auth) | Suggest checking SSH keys or using HTTPS URL |
| Git clone fails (not found) | Display error, ask user to verify URL |
| No marketplace.json in repo | Display error, explain this is not a valid marketplace |
| marketplace.json has invalid JSON | Display parse error, exit |
| Plugin directory not found | Warn and skip that plugin, continue with others |
| plugin.json missing for a plugin | Warn and skip that plugin, continue with others |
| settings.json is read-only | Display permissions error, suggest fix |
| settings.json has invalid JSON | Back up and create fresh settings structure |
| Plugin already installed (different version) | Update to new version |
| Disk space issue | Display error, suggest cleanup |

---


## Self-Correction

When user requests adjustments:

1. **"Use SSH instead of HTTPS"** --> Re-clone with SSH URL format
2. **"Only install plugin X"** --> Install only the specified plugin(s)
3. **"Don't enable plugin Y"** --> Install but set `enabledPlugins` to `false` for that plugin
4. **"Install to a different location"** --> Use custom path instead of default
5. **"Update the marketplace"** --> Pull latest changes and re-install plugins
6. **"Remove a plugin"** --> Set `enabledPlugins` to `false` and optionally remove from cache
7. **"Use a specific branch"** --> Clone with `--branch {branch}` flag

---


## Notes

### Supported URL Formats

| Format | Example |
|--------|---------|
| HTTPS with .git | `https://github.com/org/repo.git` |
| HTTPS without .git | `https://github.com/org/repo` |
| SSH | `git@github.com:org/repo.git` |
| GitHub URL | `https://github.com/org/repo` |

### Key File Locations

| File | Purpose |
|------|---------|
| `~/.claude/settings.json` | User settings: `extraKnownMarketplaces`, `enabledPlugins` |
| `~/.claude/plugins/known_marketplaces.json` | Marketplace registry with install locations |
| `~/.claude/plugins/installed_plugins.json` | Plugin install records with versions and paths |
| `~/.claude/plugins/marketplaces/{name}/` | Cloned marketplace repositories |
| `~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/` | Cached plugin installations |

### Marketplace Repository Structure

A valid marketplace repository must have:
```
.claude-plugin/
  marketplace.json          # Required: marketplace definition
plugins/
  {plugin-name}/
    .claude-plugin/
      plugin.json           # Required: plugin definition
    skills/
      {skill-name}/
        SKILL.md            # Required: skill definition
        guidelines.md       # Optional: implementation guidelines
        examples/           # Optional: usage examples
        testing/            # Optional: test cases
```

### Input Flexibility

| Input Type | Example |
|------------|---------|
| HTTPS URL | `https://github.com/episerver/claude-qa-skills.git` |
| SSH URL | `git@github.com:episerver/claude-qa-skills.git` |
| Short form | `https://github.com/episerver/claude-qa-skills` |
| Natural language | "Install plugins from https://github.com/episerver/claude-qa-skills.git" |

### Integration with Other Skills

- **`/common-qa:review-skills`**: After installing, review all new skills for consistency
- **`/common-qa:update-claude`**: Update CLAUDE.md to include new skill references
- **`/common-qa:anthropics-mcp-integration`**: If new plugins require MCP servers, use this skill to configure them
