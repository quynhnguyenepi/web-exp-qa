---
description: Update this repository's documentation (CLAUDE.md, README.md, plugin.json) to reflect current skills, versions, and architecture. Use when adding, removing, or modifying skills, or when bumping plugin versions.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/common-qa:review-skills`

# Update Repository Documentation

Scan the current state of the marketplace (plugins, skills, versions), compare against documentation files (CLAUDE.md, README.md, plugin.json), identify discrepancies, and apply updates with user approval.

## When to Use

Invoke this skill when you need to:

- Bump plugin versions after making changes to skills
- Add newly created skills to CLAUDE.md and README.md
- Remove deleted skills from documentation
- Update skill counts, architecture trees, and dependency chains
- Sync documentation after a batch of skill modifications
- Prepare documentation before committing and creating a PR

## Workflow Overview

```
Pre-Flight --> Scan Repo State --> Compare Against Docs --> Present Diff --> Apply Updates
```

## Execution Workflow

Follow these 5 sequential steps:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Scan actual repo state:**
   - List all plugin directories under `plugins/`
   - For each plugin, read `.claude-plugin/plugin.json` to get current name and version
   - List all skill directories under `plugins/*/skills/`
   - Only count directories containing a `SKILL.md` file as valid skills
   - Read each `SKILL.md` frontmatter to get the skill description

2. **Build repo state model:**
   ```
   {
     plugins: [
       {
         name: "exp-qa-agents",
         version: "2.0.0",
         path: "plugins/exp-qa-agents",
         skills: ["analyze-ticket", "create-bug-ticket", ...]
       },
       {
         name: "common-qa",
         version: "2.0.0",
         path: "plugins/common-qa",
         skills: ["analyze-pr-changes", "anthropics-claude-md-improver", ...]
       }
     ]
   }
   ```

3. **Check git status for context:**
   - Run `git status -u` to identify untracked skill directories
   - Flag untracked skills as "new (untracked)" in the model
   - This helps distinguish between committed skills and work-in-progress

4. **Check if user provided arguments:**
   - If user specified a version number, use it for the update
   - If user specified "version only", skip documentation updates
   - If no arguments, proceed with full scan

5. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Plugins found: {N}
      - exp-qa-agents: {N} skills (version {X.Y.Z})
      - common-qa: {N} skills (version {X.Y.Z})
      - New (untracked) skills: {list or "none"}

   Proceeding to compare against documentation...
   ```

---

### Step 1: Compare Against Documentation

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Compare repo state against docs" as `in_progress`.

1. **Read current documentation files:**
   - Read `CLAUDE.md` (project root)
   - Read `README.md` (project root)
   - Read `plugins/exp-qa-agents/.claude-plugin/plugin.json`
   - Read `plugins/common-qa/.claude-plugin/plugin.json`
   - Read `.claude-plugin/marketplace.json`

2. **Compare and identify discrepancies:**

   **Version checks:**
   - Current plugin.json versions vs what user wants (if version bump requested)

   **CLAUDE.md checks:**
   - Architecture tree: compare listed skills vs actual skill directories
   - Skill count in header comments (e.g., "8 agent-style skills")
   - Dependency chain: check if new skills need to be added
   - MCP server table: verify accuracy

   **README.md checks:**
   - Skill tables: compare listed skills vs actual
   - Total skill count line (e.g., "Total: 24 skills across 2 plugins")
   - Structure tree: compare listed directories vs actual
   - Skill command references

3. **Categorize discrepancies:**

   | Category | Example |
   |----------|---------|
   | **Missing skill** | Skill exists on disk but not in docs |
   | **Removed skill** | Skill listed in docs but not on disk |
   | **Wrong count** | "8 skills" but actually 10 |
   | **Version mismatch** | plugin.json says 2.0.0 but user wants 2.1.0 |
   | **Stale description** | Skill description changed in SKILL.md but not in README |

4. **Ask user about untracked skills:**
   - If untracked skill directories exist, ask via AskUserQuestion:
     - **"Include them"** -- Add to documentation (they're ready)
     - **"Skip them"** -- Exclude from updates (still in development)

---

### Step 2: Present Proposed Changes

**Todo:** Mark "Compare repo state against docs" as `completed`, mark "Present proposed changes" as `in_progress`.

1. **Present discrepancy report:**

   ```
   Documentation Discrepancies Found: {N}

   ## Version Updates
   - exp-qa-agents: {OLD} -> {NEW}
   - common-qa: {OLD} -> {NEW}

   ## CLAUDE.md Updates
   - Architecture tree: Add {skill_1}, {skill_2}
   - Skill count: "8 agent-style skills" -> "10 agent-style skills"
   - Dependency chain: Add entries for new skills

   ## README.md Updates
   - exp-qa-agents skill table: Add {skill_1}, {skill_2}
   - Total count: "24 skills" -> "26 skills"
   - Structure tree: Add {skill_1}/, {skill_2}/

   ## plugin.json Updates
   - exp-qa-agents version: {OLD} -> {NEW}
   - common-qa version: {OLD} -> {NEW}
   ```

2. **Ask user for confirmation via AskUserQuestion:**
   - **"Apply all changes" (Recommended)** -- Update all files
   - **"Let me choose which changes"** -- Select per-file
   - **"Cancel"** -- Exit without changes

---

### Step 3: Apply Updates

**Todo:** Mark "Present proposed changes" as `completed`, mark "Apply updates" as `in_progress`.

Apply changes to each file. Use the Edit tool for surgical updates.

#### plugin.json Updates

For each plugin with a version change:
```json
{
  "name": "exp-qa-agents",
  "version": "{NEW_VERSION}",
  ...
}
```

#### CLAUDE.md Updates

1. **Architecture tree:** Insert new skill entries alphabetically within the plugin section
   - Follow the existing annotation style (e.g., `# Comment describing the skill`)
   - Update the skill count in the header comment

2. **Dependency chain:** Add entries for new skills if they participate in the chain
   - Read each new skill's SKILL.md Dependencies section to determine placement

3. **Skill count in prose:** Update any mentions of skill counts

#### README.md Updates

1. **Skill tables:** Add rows for new skills in the correct table section
   - Use format: `| Skill Name | \`/plugin:skill-name\` | Description from SKILL.md frontmatter |`

2. **Total count line:** Update "Total: X skills across 2 plugins"

3. **Structure tree:** Add new skill directories in the correct position

4. **Workflow section:** Add new skills if they participate in the documented workflows

#### Final Report

```
Updates applied successfully

Files modified:
- CLAUDE.md: {N} changes
- README.md: {N} changes
- plugins/exp-qa-agents/.claude-plugin/plugin.json: version -> {NEW}
- plugins/common-qa/.claude-plugin/plugin.json: version -> {NEW}

Summary:
- Skills added to docs: {list}
- Skills removed from docs: {list}
- Version bumped: {OLD} -> {NEW}
```

**Todo:** Mark "Apply updates" as `completed`. All todos should now be `completed`.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
