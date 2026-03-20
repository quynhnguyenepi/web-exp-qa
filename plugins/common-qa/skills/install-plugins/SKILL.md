---
description: Install a Claude Code plugin marketplace from a GitHub URL. Clones the repo, discovers all plugins, registers the marketplace, installs and enables all plugins. Use when adding a new marketplace or reinstalling plugins from a git URL.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/common-qa:review-skills`

# Install Plugins from Marketplace

Clone a Claude Code plugin marketplace repository from a GitHub URL, discover all plugins inside it, register the marketplace in Claude Code settings, install and enable every plugin, then report the results.

## When to Use

Invoke this skill when you need to:

- Install a new plugin marketplace from a GitHub URL (e.g., `https://github.com/org/repo.git`)
- Add all plugins from a marketplace repository to Claude Code in one step
- Re-install or update a previously installed marketplace and its plugins
- Set up a teammate's Claude Code with the same marketplace and plugins
- Migrate a marketplace URL (e.g., from SSH to HTTPS or vice versa)

## Workflow Overview

```
Pre-Flight --> Clone Repo --> Discover Plugins --> Install & Enable --> Verify & Report
```

**Detailed workflow, JSON templates, and verbose examples are in guidelines.md.**

## Execution Workflow

Follow these 5 sequential steps:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Validate user input** -- Ask for marketplace URL if not provided, normalize format (HTTPS/SSH, with/without .git)
2. **Extract marketplace name** from URL (last path segment without `.git`)
3. **Verify git is available** -- Run `git --version`, error if not installed
4. **Check Claude Code settings files exist** -- Verify `~/.claude/settings.json`, `~/.claude/plugins/` directory, `known_marketplaces.json`, `installed_plugins.json` (create if missing)
5. **Check if marketplace is already installed** -- Read `known_marketplaces.json`, offer update/reinstall/cancel if exists
6. **Report pre-flight status** -- URL, marketplace name, git status, settings validity, installation status

See guidelines.md for detailed normalization rules and pre-flight report template.

---

### Step 1: Clone / Update Marketplace Repository

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Clone or update marketplace repository" as `in_progress`.

1. **Determine clone target** -- `~/.claude/plugins/marketplaces/{MARKETPLACE_NAME}/`
2. **Clone or update:**
   - New: `git clone {URL} ~/.claude/plugins/marketplaces/{NAME}/`
   - Update: `cd ~/.claude/plugins/marketplaces/{NAME}/ && git pull`
   - Reinstall: Remove directory, then clone
3. **Verify clone successful** -- Check directory exists, `.claude-plugin/marketplace.json` exists
4. **Read marketplace.json** -- Extract name, description, owner, plugins array
5. **Get git commit SHA** -- `git rev-parse HEAD` for version tracking
6. **Report** -- Location, marketplace info, plugin count, commit SHA

See guidelines.md for detailed clone commands and report template.

---

### Step 2: Discover Plugins and Confirm

**Todo:** Mark "Clone or update marketplace repository" as `completed`, mark "Discover plugins and confirm with user" as `in_progress`.

1. **Parse plugin list** from marketplace.json (name, source, description)
2. **Read each plugin's plugin.json** -- Extract version, skills path
3. **Discover skills** for each plugin (read `skills/` directory, parse SKILL.md frontmatter)
4. **Present discovery results** -- List plugins with descriptions and skill counts
5. **Ask user for confirmation** via AskUserQuestion: Install all (default) / Select specific / Cancel
6. **If "Select specific"** -- Use multiSelect for plugin selection

See guidelines.md for detailed plugin discovery output template.

---

### Step 3: Install and Enable Plugins

**Todo:** Mark "Discover plugins and confirm with user" as `completed`, mark "Install and enable all plugins" as `in_progress`.

1. **Read current settings files** -- `settings.json`, `known_marketplaces.json`, `installed_plugins.json`
2. **Register marketplace in settings.json** -- Add to `extraKnownMarketplaces` with git source
3. **Register marketplace in known_marketplaces.json** -- Add entry with installLocation and timestamp
4. **For each plugin to install:**
   - Read plugin.json for version
   - Create cache directory: `~/.claude/plugins/cache/{MARKETPLACE}/{PLUGIN}/{VERSION}`
   - Copy plugin contents to cache (including `.claude-plugin/` directory)
   - Register in `installed_plugins.json` with scope, installPath, version, timestamps, gitCommitSha
   - Enable in `settings.json` `enabledPlugins` (set to `true`)
   - Report progress: "Installed: {PLUGIN} (v{VERSION}) -- {N} skills"
5. **Write all updated JSON files**

See guidelines.md for detailed JSON registration templates (settings.json, known_marketplaces.json, installed_plugins.json) and cache directory structure.

---

### Step 4: Verify and Report

**Todo:** Mark "Install and enable all plugins" as `completed`, mark "Verify installation and report results" as `in_progress`.

1. **Verify settings files** -- Re-read all JSON files and confirm marketplace and plugins registered correctly
2. **Verify cache directories** -- Check cache paths exist with `.claude-plugin/plugin.json` inside
3. **Present final report:**
   - Marketplace name, source URL, location
   - Table of installed plugins (name, version, skill count)
   - Total plugins and skills count
   - List of available skills with invocation format (`/{plugin}:{skill}`)
   - **IMPORTANT:** Restart Claude Code instruction
4. **Mark "Verify installation and report results" as `completed`**

See guidelines.md for detailed final report template and verification steps.

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, Notes, detailed JSON templates, verbose workflow diagrams, and directory structure details are in guidelines.md to reduce auto-loaded context size.
