# Sample: Install Plugins from Marketplace

## User Request

"Install plugins from https://github.com/episerver/claude-qa-skills.git"

---

## Step 0: Pre-Flight Checks

```
TodoWrite([
  { content: "Run pre-flight checks (validate URL, verify git, check settings)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Clone or update marketplace repository", status: "pending", activeForm: "Cloning marketplace repository" },
  { content: "Discover plugins and confirm with user", status: "pending", activeForm: "Discovering plugins" },
  { content: "Install and enable all plugins", status: "pending", activeForm: "Installing and enabling plugins" },
  { content: "Verify installation and report results", status: "pending", activeForm: "Verifying installation" }
])
```

Validating input...

- URL: `https://github.com/episerver/claude-qa-skills.git`
- Format: HTTPS with .git suffix -- valid
- Marketplace name extracted: `claude-qa-skills`

Checking git...
```bash
git --version
# git version 2.43.0
```

Checking Claude Code settings...
- `~/.claude/settings.json` -- exists
- `~/.claude/plugins/known_marketplaces.json` -- exists
- `~/.claude/plugins/installed_plugins.json` -- exists

Checking if already installed...
- `claude-qa-skills` not found in known_marketplaces.json -- fresh install

```
Pre-flight checks passed
   - URL: https://github.com/episerver/claude-qa-skills.git
   - Marketplace name: claude-qa-skills
   - Git: Available (v2.43.0)
   - Settings: Valid
   - Already installed: No

Proceeding to clone repository...
```

---

## Step 1: Clone Marketplace Repository

```
TodoWrite: "Run pre-flight checks" -> completed, "Clone or update marketplace repository" -> in_progress
```

Cloning repository...
```bash
git clone https://github.com/episerver/claude-qa-skills.git ~/.claude/plugins/marketplaces/claude-qa-skills/
```

Verifying marketplace.json...
- `.claude-plugin/marketplace.json` found

Reading marketplace.json:
```json
{
  "name": "optimizely-qa",
  "description": "Optimizely QA skills marketplace",
  "plugins": [
    { "name": "exp-qa-agents", "source": "./plugins/exp-qa-agents", "description": "QA skills for Optimizely Experimentation" },
    { "name": "dxp-qa", "source": "./plugins/dxp-qa", "description": "QA skills for Optimizely DXP" },
    { "name": "common-qa", "source": "./plugins/common-qa", "description": "Common QA skills shared across products" }
  ]
}
```

Getting commit SHA:
```bash
cd ~/.claude/plugins/marketplaces/claude-qa-skills/ && git rev-parse HEAD
# 9c79925177774d5cbd73143a728a48e04a82e5ae
```

```
Repository cloned successfully
   - Location: ~/.claude/plugins/marketplaces/claude-qa-skills/
   - Marketplace: optimizely-qa
   - Description: Optimizely QA skills marketplace
   - Plugins found: 3
   - Commit: 9c79925

Proceeding to discover plugins...
```

---

## Step 2: Discover Plugins and Confirm

```
TodoWrite: "Clone or update marketplace repository" -> completed, "Discover plugins and confirm with user" -> in_progress
```

Reading plugin.json for each plugin...

**exp-qa-agents**: version 1.0.0, 7 skills found
**dxp-qa**: version 1.0.0, 0 skills found
**common-qa**: version 1.0.0, 8 skills found

```
Marketplace: optimizely-qa
Description: Optimizely QA skills marketplace

Plugins to install:

1. exp-qa-agents (v1.0.0)
   QA skills for Optimizely Experimentation
   Skills: analyze-ticket, create-bug-ticket, create-pr, create-test-cases,
           create-test-scripts-cypress-js, review-github-pr-cypress-js, execute-test-case

2. dxp-qa (v1.0.0)
   QA skills for Optimizely DXP
   Skills: (none yet)

3. common-qa (v1.0.0)
   Common QA skills shared across products
   Skills: anthropics-claude-md-improver, anthropics-mcp-integration, install-plugins,
           mass-update-jira-tickets, get-figma-screenshots, review-skills, update-claude, update-skills,
           verify-bug-simple

Total: 3 plugins, 16 skills
```

**AskUserQuestion:** "Which plugins do you want to install?"
- **"Install all plugins" (Recommended)**
- "Select specific plugins"
- "Cancel"

**User selects:** "Install all plugins"

---

## Step 3: Install and Enable Plugins

```
TodoWrite: "Discover plugins and confirm with user" -> completed, "Install and enable all plugins" -> in_progress
```

Backing up settings files...
```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak.1709553600
```

Reading current settings...

**Registering marketplace in settings.json:**
Added `optimizely-qa` to `extraKnownMarketplaces`

**Registering in known_marketplaces.json:**
Added `optimizely-qa` with source and install location

**Installing plugins:**

```
Installed: exp-qa-agents (v1.0.0) -- 7 skills
   Cache: ~/.claude/plugins/cache/optimizely-qa/exp-qa-agents/1.0.0/
   Enabled: exp-qa-agents@optimizely-qa = true

Installed: dxp-qa (v1.0.0) -- 0 skills
   Cache: ~/.claude/plugins/cache/optimizely-qa/dxp-qa/1.0.0/
   Enabled: dxp-qa@optimizely-qa = true

Installed: common-qa (v1.0.0) -- 8 skills
   Cache: ~/.claude/plugins/cache/optimizely-qa/common-qa/1.0.0/
   Enabled: common-qa@optimizely-qa = true
```

Writing updated settings files...

---

## Step 4: Verify and Report

```
TodoWrite: "Install and enable all plugins" -> completed, "Verify installation and report results" -> in_progress
```

Verifying settings files...
- settings.json: `optimizely-qa` in extraKnownMarketplaces -- OK
- settings.json: 3 plugins in enabledPlugins -- OK
- known_marketplaces.json: `optimizely-qa` registered -- OK
- installed_plugins.json: 3 plugins registered -- OK
- Cache directories: 3/3 verified -- OK

```
Installation complete!

Marketplace: optimizely-qa
Source: https://github.com/episerver/claude-qa-skills.git
Location: ~/.claude/plugins/marketplaces/claude-qa-skills/

Installed Plugins:
+-----+------------+---------+--------+
| #   | Plugin     | Version | Skills |
+-----+------------+---------+--------+
| 1   | exp-qa-agents    | 1.0.0   | 7      |
| 2   | dxp-qa     | 1.0.0   | 0      |
| 3   | common-qa  | 1.0.0   | 8      |
+-----+------------+---------+--------+

Total: 3 plugins installed, 15 skills available

Available Skills:
- /exp-qa-agents:analyze-ticket
- /exp-qa-agents:create-bug-ticket
- /exp-qa-agents:create-pr
- /exp-qa-agents:create-test-cases
- /exp-qa-agents:create-test-scripts-cypress-js
- /exp-qa-agents:review-github-pr-cypress-js
- /exp-qa-agents:execute-test-case
- /common-qa:anthropics-claude-md-improver
- /common-qa:anthropics-mcp-integration
- /common-qa:install-plugins
- /common-qa:mass-update-jira-tickets
- /common-qa:get-figma-screenshots
- /common-qa:review-skills
- /common-qa:update-claude
- /common-qa:update-skills
- /common-qa:verify-bug-simple

IMPORTANT: Restart Claude Code (close and reopen VS Code) for the new plugins to take effect.
After restart, the new skills will appear in the skill list and can be invoked with /{plugin}:{skill}.
```

```
TodoWrite: "Verify installation and report results" -> completed
```
