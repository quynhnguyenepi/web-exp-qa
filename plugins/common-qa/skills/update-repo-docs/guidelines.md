# Update Repo Docs Guidelines

Standards for updating repository documentation (CLAUDE.md, README.md, plugin.json) to reflect current skills and architecture.

## Scan Accuracy

### What Counts as a Valid Skill

- A directory under `plugins/*/skills/` that contains a `SKILL.md` file
- Directories without `SKILL.md` are not skills and should not be counted
- Untracked directories (shown by `git status`) should be flagged separately

### Version Sources of Truth

- `plugins/*/plugin.json` contains the current version
- User may specify a target version -- use that instead
- Never auto-increment versions without user direction

---

## Documentation Update Rules

### CLAUDE.md

- **Architecture tree:** Skills listed alphabetically within each plugin section
- **Skill counts:** Match the number in comments (e.g., "8 agent-style skills") to actual count
- **Dependency chain:** Only add skills that participate in the chain (have sub-skills or are sub-skills)
- **MCP server table:** Only update if a new server is added or an existing one removed

### README.md

- **Skill tables:** One row per skill, format: `| Skill Name | \`/plugin:skill-name\` | Description |`
- **Total count line:** Must match actual total across both plugins
- **Structure tree:** Reflect actual directory structure
- **Descriptions:** Pull from SKILL.md frontmatter `description` field

### plugin.json

- Only update the `version` field
- Never change `name`, `description`, or other fields unless explicitly asked

---

## Version Bump Convention

| Change Type | Bump | Example |
|-------------|------|---------|
| New skills added | Minor (X.Y+1.0) | 2.0.0 -> 2.1.0 |
| Skill content updated | Patch (X.Y.Z+1) | 2.0.0 -> 2.0.1 |
| Breaking skill changes | Major (X+1.0.0) | 2.0.0 -> 3.0.0 |
| Documentation-only fixes | No bump | 2.0.0 -> 2.0.0 |

---

## Safety Rules

### Do

- Always present proposed changes before applying
- Use the Edit tool for surgical updates to existing files
- Verify counts by actually counting, not by reading existing numbers
- Ask about untracked skills before including them

### Do Not

- Apply changes without user confirmation
- Modify files outside the documented scope (CLAUDE.md, README.md, plugin.json, marketplace.json)
- Guess at skill descriptions -- read them from SKILL.md frontmatter
- Remove skills from docs that still exist on disk
- Add skills to docs that only exist as empty directories

---

## Anti-Patterns

### Counting Without Verifying

**Problem:** Trusting the existing count in docs instead of recounting from disk.
**Solution:** Always list directories, filter for those with SKILL.md, and count.

### Updating Selectively

**Problem:** Updating README.md but forgetting to update CLAUDE.md (or vice versa).
**Solution:** Always update all documentation files together for consistency.

### Including Work-in-Progress Skills

**Problem:** Adding untracked/incomplete skills to documentation.
**Solution:** Ask the user whether untracked skills should be included or skipped.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (scan plugins and skills)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Compare repo state against documentation", status: "pending", activeForm: "Comparing repo state against docs" },
  { content: "Present discrepancies and proposed changes", status: "pending", activeForm: "Presenting proposed changes" },
  { content: "Apply updates with user approval", status: "pending", activeForm: "Applying updates" }
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
| CLAUDE.md not found | Create minimal CLAUDE.md from template, warn user |
| README.md not found | Warn user, skip README updates |
| plugin.json malformed | Display parse error, ask user to fix manually |
| Skill has no SKILL.md | Skip that directory, it's not a valid skill |
| Edit tool fails | Display error, show the intended change so user can apply manually |
| Git not available | Skip git status check, proceed without untracked file detection |

---


## Self-Correction

When user requests adjustments:

1. **"Only bump version"** -> Update plugin.json files only, skip doc changes
2. **"Don't include skill X"** -> Exclude specific skill from documentation updates
3. **"Use version X.Y.Z"** -> Override version number
4. **"Also update MCP_SETUP.md"** -> Include MCP setup doc in the update scope
5. **"Show me what changed"** -> Display git diff after updates are applied
6. **"Revert changes"** -> Run `git checkout` on modified files to undo

---


## Notes

### Files Updated by This Skill

| File | What Gets Updated |
|------|-------------------|
| `CLAUDE.md` | Architecture tree, skill counts, dependency chain |
| `README.md` | Skill tables, total counts, structure tree, workflows |
| `plugins/*/plugin.json` | Version field |
| `.claude-plugin/marketplace.json` | Only if plugin names/descriptions change |

### Version Bump Convention

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| New skills added | Minor (X.Y+1.0) | 2.0.0 -> 2.1.0 |
| Skill content updated | Patch (X.Y.Z+1) | 2.0.0 -> 2.0.1 |
| Breaking skill changes | Major (X+1.0.0) | 2.0.0 -> 3.0.0 |
| Documentation-only fixes | No bump | 2.0.0 -> 2.0.0 |

### Integration with Other Skills

- **`/common-qa:review-skills`**: Run after this skill to verify consistency of updated docs
- **`/exp-qa-agents:create-pr`**: Run after this skill to commit and create a PR with the doc updates
