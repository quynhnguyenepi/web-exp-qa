# Test Cases for anthropics-claude-md-improver Skill

## TC-001: Single File Audit

**Input:** Run `/common-qa:anthropics-claude-md-improver` on a repository with one `./CLAUDE.md` file.

**Expected:**
- Discovers 1 CLAUDE.md file
- Assesses quality against all 6 criteria
- Outputs quality report with score and grade
- Proposes targeted updates
- Asks for user confirmation before applying

**Pass Criteria:**
- Score is between 0-100 with correct grade mapping
- All 6 criteria have individual scores
- Report is displayed before any updates
- No changes made without user approval

---

## TC-002: Multi-File Repository

**Input:** Run on a monorepo with CLAUDE.md at root and 3 package-level CLAUDE.md files.

**Expected:**
- Discovers all 4 CLAUDE.md files
- Assesses each file independently
- Reports average score and per-file breakdown
- Proposes updates per file

**Pass Criteria:**
- All 4 files are found and assessed
- Summary shows correct file count and average score
- Each file has its own assessment section in the report
- Updates are grouped by file

---

## TC-003: Perfect Score File

**Input:** Run on a repository with a comprehensive, well-maintained CLAUDE.md scoring 90+.

**Expected:**
- Discovers the file
- Assesses quality and assigns score of 90-100 (Grade: A)
- Reports no significant issues
- Either proposes no updates or only minor suggestions

**Pass Criteria:**
- Score is 90 or above
- Grade is "A"
- Report acknowledges the file is well-maintained
- No unnecessary updates proposed

---

## TC-004: Poor Score File

**Input:** Run on a repository with a sparse CLAUDE.md containing only a project name and one line description.

**Expected:**
- Discovers the file
- Assesses quality and assigns score below 30 (Grade: F)
- Reports multiple missing sections
- Proposes substantial additions (commands, architecture, key files)

**Pass Criteria:**
- Score is below 30
- Grade is "F"
- Report lists specific missing sections
- Proposed updates cover at least commands and architecture
- Still asks for user approval before applying

---

## TC-005: User Cancels Update

**Input:** Run audit, then user declines to apply proposed updates.

**Expected:**
- Completes discovery and assessment
- Outputs quality report
- Proposes updates and asks for confirmation
- User says "No" or "Don't update"
- Skill exits cleanly without modifying any files

**Pass Criteria:**
- Quality report is still displayed (audit was useful)
- No files are modified
- Clean exit message confirms no changes were made
- TodoWrite shows "Apply targeted updates" as completed with no-op note

---

## TC-006: Monorepo with Many Files

**Input:** Run on a monorepo with 12 CLAUDE.md files across packages.

**Expected:**
- Discovers all 12 files
- Processes in batches if needed
- Produces a summary report covering all files
- Handles the volume without errors

**Pass Criteria:**
- All 12 files discovered and assessed
- Summary table includes all files
- Average score is computed correctly
- No timeout or processing errors

---

## TC-007: No CLAUDE.md Files Found

**Input:** Run on a repository with no CLAUDE.md files at any level.

**Expected:**
- Discovery phase finds 0 files
- Reports "No CLAUDE.md files found"
- Suggests creating a CLAUDE.md with a template
- Exits gracefully without errors

**Pass Criteria:**
- Clear message that no files were found
- Suggestion to create one is provided
- No assessment or update phases attempted
- TodoWrite updates reflect early termination

---

## TC-008: Read-Only File

**Input:** Run on a repository where CLAUDE.md has read-only permissions.

**Expected:**
- Discovers and assesses the file normally
- Quality report is generated
- When attempting to apply updates, detects read-only permission
- Warns user about the permission issue
- Suggests fixing permissions manually

**Pass Criteria:**
- Assessment and report complete successfully (read-only does not block reading)
- Clear warning message about write failure
- Suggestion to fix permissions provided
- No crash or unhandled error
