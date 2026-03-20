# Test Cases for update-skills Skill

## TC-001: Update SKILL.md Workflow Step

**Input:** Run `/common-qa:update-skills` with learning: "Step 2 needs JQL validation before executing"

**Expected:**
- Identifies target skill
- Reads current SKILL.md
- Adds JQL validation sub-step to Step 2
- Presents change for review
- Applies after confirmation

**Pass Criteria:**
- Step 2 updated with new sub-step
- Step numbering remains sequential
- Workflow Overview diagram still matches steps

---

## TC-002: Add New Anti-Pattern to Guidelines

**Input:** Run with learning: "Never use issueKey parameter, always use issue_key"

**Expected:**
- Reads current guidelines.md
- Adds anti-pattern entry with Problem/Solution format
- Maintains formatting consistency

**Pass Criteria:**
- New anti-pattern follows existing format
- Problem and Solution both present
- No duplicate entries

---

## TC-003: Add New Example from Session

**Input:** Run with learning: "This interaction produced a great example of handling edge cases"

**Expected:**
- Creates new example file in examples/ directory
- Follows naming convention (sample-{description}.md)
- Includes Input, Steps, Output sections

**Pass Criteria:**
- New file created in examples/
- Content is realistic and complete
- Format matches existing examples

---

## TC-004: Add New Test Case

**Input:** Run with learning: "Need test for when JQL returns 0 results"

**Expected:**
- Reads current test_cases.md
- Determines next TC number (e.g., TC-014)
- Adds test case with Input, Expected, Pass Criteria

**Pass Criteria:**
- TC number follows sequence (no gaps or duplicates)
- Format matches existing test cases
- Covers the edge case described

---

## TC-005: Multiple Changes Across Files

**Input:** Run with 3 learnings affecting SKILL.md, guidelines.md, and test_cases.md

**Expected:**
- All 3 files are updated
- Changes are grouped and presented together
- User confirms all changes at once

**Pass Criteria:**
- All files modified correctly
- Changes don't conflict with each other
- Summary shows all modifications

---

## TC-006: Skill Not Found

**Input:** Run with skill name that doesn't exist (e.g., "nonexistent-skill")

**Expected:**
- Reports skill not found
- Lists available skills
- Asks user to choose correct skill

**Pass Criteria:**
- Clear error message
- Available skills listed
- No files modified

---

## TC-007: User Rejects Planned Changes

**Input:** User selects "Modify the plan" and removes some changes

**Expected:**
- Only applies user-approved changes
- Skipped changes are not applied
- Report reflects what was actually applied

**Pass Criteria:**
- Only approved changes in files
- Summary accurate
- No unapproved modifications

---

## TC-008: Cross-Plugin Skill Update

**Input:** Run on a skill in exp-qa-agents plugin from the common-qa context

**Expected:**
- Correctly locates skill in exp-qa-agents/skills/
- Updates files in the correct location
- References use correct plugin prefix (/exp-qa-agents:skill-name)

**Pass Criteria:**
- Files modified in correct plugin directory
- Skill references match the plugin (not common-qa)
