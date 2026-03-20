# Test Cases for update-claude Skill

## TC-001: Create CLAUDE.md for Repo Without One

**Input:** Run `/common-qa:update-claude` on a repo that has no CLAUDE.md

**Expected:**
- Pulls latest code
- Analyzes codebase structure, tech stack, and patterns
- Generates complete CLAUDE.md with all sections
- Presents to user for review
- Writes CLAUDE.md to project root

**Pass Criteria:**
- CLAUDE.md is created at project root
- All sections present (Overview, Quick Reference, Architecture, Conventions)
- Commands listed are real (from package.json or Makefile)
- File paths listed actually exist

---

## TC-002: Update Existing CLAUDE.md

**Input:** Run on a repo that already has CLAUDE.md

**Expected:**
- Detects existing CLAUDE.md
- Analyzes current codebase state
- Updates outdated sections while preserving user-added content
- Shows what changed

**Pass Criteria:**
- User-customized sections preserved
- Outdated paths/commands updated
- New patterns detected and added

---

## TC-003: Detect Tech Stack from Config Files

**Input:** Run on a repo with package.json, tsconfig.json, and cypress.config.js

**Expected:**
- Identifies: Node.js, TypeScript, Cypress
- Extracts npm scripts as common commands
- Detects Cypress test patterns

**Pass Criteria:**
- Correct tech stack in Overview section
- npm scripts listed in Quick Reference
- Cypress patterns noted in Architecture

---

## TC-004: Handle Large Repository

**Input:** Run on a repo with >5000 files

**Expected:**
- Focuses on key directories (not deep scanning everything)
- Completes analysis within reasonable time
- Still produces accurate CLAUDE.md

**Pass Criteria:**
- Does not hang or timeout
- Key structure captured correctly
- Commands and conventions accurate

---

## TC-005: User Requests Edits Before Applying

**Input:** User selects "Review and edit" and requests changes

**Expected:**
- Accepts user's modifications
- Applies changes to the generated content
- Shows updated version for confirmation

**Pass Criteria:**
- User's changes are incorporated
- Final file includes modifications
- No content lost during editing

---

## TC-006: Git Pull Fails

**Input:** Run when git pull fails (merge conflicts or auth error)

**Expected:**
- Detects the failure
- Warns user about the issue
- Suggests resolution steps
- Does not proceed with outdated code

**Pass Criteria:**
- Clear error message
- No analysis on stale code
- Actionable resolution suggestion

---

## TC-007: Repository with No Config Files

**Input:** Run on a simple repo with just source files and no package.json/Makefile

**Expected:**
- Infers language from file extensions
- Skips commands section (or notes "no build tool detected")
- Still produces useful CLAUDE.md from directory structure

**Pass Criteria:**
- Language correctly inferred
- No fake commands listed
- Structure section still useful
