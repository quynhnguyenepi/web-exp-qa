# Sample: Update Repository Documentation After Adding New Skills

---

## Input

User request: "Update the docs -- I just added 2 new skills (create-branch and fix-daily-run-playwright-ts). Bump versions to 2.1.0."

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - Plugins found: 2
   - exp-qa-agents: 9 skills (version 2.0.0)
   - common-qa: 17 skills (version 2.0.0)
   - New (untracked) skills: create-branch (common-qa), fix-daily-run-playwright-ts (exp-qa-agents)

Proceeding to compare against documentation...
```

---

## Step 1: Compare Against Documentation

```
Discrepancies found:

CLAUDE.md:
  - Architecture tree: missing create-branch, fix-daily-run-playwright-ts
  - Skill count: "8 agent-style skills" should be "9 agent-style skills"
  - Skill count: "16 skills" should be "17 skills"

README.md:
  - exp-qa-agents table: missing fix-daily-run-playwright-ts row
  - common-qa table: missing create-branch row
  - Total count: "24 skills" should be "26 skills"

plugin.json:
  - exp-qa-agents: 2.0.0 -> 2.1.0
  - common-qa: 2.0.0 -> 2.1.0

Include untracked skills in documentation?
  User selected: "Include them"
```

---

## Step 2: Present Proposed Changes

```
Documentation Discrepancies Found: 8

## Version Updates
- exp-qa-agents: 2.0.0 -> 2.1.0
- common-qa: 2.0.0 -> 2.1.0

## CLAUDE.md Updates
- Architecture tree: Add create-branch (common-qa), fix-daily-run-playwright-ts (exp-qa-agents)
- Skill count: "8 agent-style skills" -> "9 agent-style skills"
- Skill count: "16 skills" -> "17 skills"

## README.md Updates
- exp-qa-agents table: Add fix-daily-run-playwright-ts
- common-qa table: Add create-branch
- Total: "24 skills" -> "26 skills"

## plugin.json Updates
- exp-qa-agents version: 2.0.0 -> 2.1.0
- common-qa version: 2.0.0 -> 2.1.0
```

User selected: "Apply all changes"

---

## Step 3: Apply Updates

```
Updates applied successfully

Files modified:
- CLAUDE.md: 3 changes (architecture tree, skill counts)
- README.md: 3 changes (skill tables, total count)
- plugins/exp-qa-agents/.claude-plugin/plugin.json: version -> 2.1.0
- plugins/common-qa/.claude-plugin/plugin.json: version -> 2.1.0

Summary:
- Skills added to docs: create-branch, fix-daily-run-playwright-ts
- Skills removed from docs: none
- Version bumped: 2.0.0 -> 2.1.0
```
