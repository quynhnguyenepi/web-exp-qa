# Test Cases for review-skills Skill

## TC-001: All Skills Pass All Checks

**Input:** Run `/common-qa:review-skills` on a repo where all skills are fully consistent

**Expected:**
- Discovers all skills under plugins/*/skills/
- Runs all 10 check categories against each skill
- All checks pass for all skills
- Generates report with 100% pass rate
- Skips "Offer to fix" step (nothing to fix)

**Pass Criteria:**
- Summary table shows PASS for all cells
- "All skills passed all consistency checks" message displayed
- No recommendations section
- Step 4 marked as "Skipped -- all checks passed"

---

## TC-002: Skill Missing guidelines.md Detected

**Input:** Run when one skill is missing `guidelines.md`

**Expected:**
- Check 2 (Structure) reports FAIL for that skill
- Other checks still run and report correctly
- Report lists the missing file specifically
- Recommendation includes creating guidelines.md

**Pass Criteria:**
- FAIL shown for the specific skill's Structure check
- Other skills unaffected
- Specific file path mentioned in findings

---

## TC-003: Wrong MCP Parameter Name Detected

**Input:** Run when a skill uses `issueKey` instead of `issue_key`

**Expected:**
- Check 5 (MCP Parameters) reports FAIL for that skill
- Shows file and line number where `issueKey` was found
- Recommendation includes the correct parameter name

**Pass Criteria:**
- FAIL shown for the specific skill's Params check
- Line number included in findings
- Fix recommendation shows `issue_key`

---

## TC-004: Inconsistent Frontmatter Detected

**Input:** Run when a skill has `name:` in frontmatter

**Expected:**
- Check 1 (Frontmatter) reports FAIL for that skill
- Shows the line number where `name:` was found
- Recommendation says to remove the field

**Pass Criteria:**
- FAIL shown for Frontmatter check
- Clear instruction to remove `name` field

---

## TC-005: Offer to Fix -- User Accepts

**Input:** Run with issues found, user selects "Fix all issues automatically"

**Expected:**
- Applies all fixes automatically
- Reports each fix applied with file and change description
- Suggests re-running to verify

**Pass Criteria:**
- All fixable issues are resolved
- Fix report lists each change
- Files are actually modified

---

## TC-006: Offer to Fix -- User Declines

**Input:** Run with issues found, user selects "Don't fix, keep report only"

**Expected:**
- No files are modified
- Report is displayed
- Exit message mentions the issue count

**Pass Criteria:**
- No file modifications
- Report still displayed
- Clean exit

---

## TC-007: Specific Skill Input

**Input:** `/common-qa:review-skills analyze-ticket`

**Expected:**
- Only reviews the specified skill (analyze-ticket)
- Other skills not scanned
- Report shows only the specified skill

**Pass Criteria:**
- Only 1 skill in the report
- All 10 checks run against that skill only

---

## TC-008: Self-Exclusion

**Input:** Run `/common-qa:review-skills` (review all)

**Expected:**
- The review-skills skill itself is NOT included in the review
- All other skills are reviewed

**Pass Criteria:**
- "review-skills" does not appear in the summary table
- Skill count is total skills minus 1
