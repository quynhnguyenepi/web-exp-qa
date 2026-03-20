# Test Cases for update-repo-docs Skill

## TC-001: Add New Skills to Documentation

**Input:** Run `/common-qa:update-repo-docs` after adding 2 new skills to the repo.

**Expected:**
- Scans plugin directories and finds the new skills
- Compares against CLAUDE.md and README.md
- Identifies missing entries in architecture tree, skill tables, and counts
- Presents proposed changes
- Applies updates after confirmation

**Pass Criteria:**
- New skills appear in CLAUDE.md architecture tree
- New skills appear in README.md skill tables
- Skill counts updated in both files
- No existing content broken

---

## TC-002: Version Bump Only

**Input:** Run with instruction "Only bump version to 2.1.0".

**Expected:**
- Updates plugin.json version field for both plugins
- Does not modify CLAUDE.md or README.md
- Reports version change

**Pass Criteria:**
- Both plugin.json files updated to 2.1.0
- No documentation files modified
- Report confirms version-only change

---

## TC-003: Remove Deleted Skills from Docs

**Input:** Run after deleting a skill directory from disk.

**Expected:**
- Detects that a skill listed in docs no longer exists on disk
- Proposes removal from CLAUDE.md and README.md
- Updates skill counts after removal

**Pass Criteria:**
- Deleted skill removed from architecture tree
- Deleted skill removed from skill tables
- Counts decremented correctly
- Dependency chain updated if skill was referenced

---

## TC-004: Untracked Skills Handling

**Input:** Run when new skill directories exist but are untracked in git.

**Expected:**
- Identifies untracked skill directories
- Asks user whether to include or skip them
- If skip: excludes from documentation updates
- If include: adds to documentation

**Pass Criteria:**
- User is asked about untracked skills
- Decision is respected in the updates
- Untracked skills flagged in pre-flight report

---

## TC-005: No Discrepancies Found

**Input:** Run when all documentation is already up to date.

**Expected:**
- Scans repo and compares against docs
- Reports that no discrepancies were found
- Does not modify any files

**Pass Criteria:**
- Clear message: no updates needed
- No files modified
- Versions remain unchanged
