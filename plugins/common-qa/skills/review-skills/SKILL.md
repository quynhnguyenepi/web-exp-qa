---
description: Review all skills in the repository for consistency, completeness, and adherence to standards. Use when adding new skills, modifying existing ones, or performing periodic quality audits.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** None

# Reviewing Skills for Consistency

Automatically scan all skills in the repository, check for structural completeness, content consistency, and adherence to established patterns, then generate a detailed report with findings and offer to auto-fix issues.

## When to Use

Invoke this skill when you need to:

- Audit all skills after adding a new one to ensure consistency
- Verify that skill modifications didn't break conventions
- Run a periodic quality check across all skills
- Validate that a newly created skill follows the standard template
- Check for broken references, wrong parameter names, or missing files

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  0. Pre-Flight Checks                                                            │
│     ├─ Discover all skill directories under plugins/*/skills/                  │
│     └─ Validate at least 1 skill exists                                          │
│                                                                                  │
│  1. Scan Skills Structure                                                        │
│     ├─ For each skill, check directory completeness                              │
│     ├─ Verify SKILL.md, guidelines.md, examples/, testing/ exist                │
│     └─ Record missing files per skill                                            │
│                                                                                  │
│  2. Analyze Content Consistency                                                  │
│     ├─ Run all 10 check categories across all skills                            │
│     ├─ Check frontmatter, references, parameters, formatting                    │
│     ├─ Check step numbering, JIRA comments, MCP setup, sections                │
│     └─ Record pass/fail per skill per check                                      │
│                                                                                  │
│  3. Generate Report                                                              │
│     ├─ Build summary table (pass/fail per skill per check)                      │
│     ├─ List detailed findings with file:line references                         │
│     └─ Prioritize recommendations                                               │
│                                                                                  │
│  4. Offer to Fix                                                                 │
│     ├─ Present report to user                                                    │
│     ├─ Ask if user wants to auto-fix issues                                     │
│     ├─ If yes: apply fixes and report results                                   │
│     └─ If no: exit with report saved                                            │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Simple Flow:**
```
Pre-Flight → Scan Structure → Analyze Content → Generate Report → Offer to Fix
```

## Execution Workflow

Follow these 5 sequential steps to review all skills:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Discover all skill directories:**
   - Scan `plugins/*/skills/` for subdirectories
   - Each subdirectory containing a `SKILL.md` file is considered a skill
   - Collect skill names and paths
   - **Exclude** the `review-skills` skill itself from the review (this skill)

2. **Validate discovery results:**
   - If no skills found: display error and exit
     ```
     Error: No skills found

     Expected skills at: plugins/*/skills/*/SKILL.md
     Verify the skill directory structure exists.
     ```
   - If skills found: proceed

3. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Skills directory: plugins/*/skills/
      - Skills found: {N} skills
      - Skills: {comma-separated list of skill names}

   Proceeding to scan structure...
   ```

---

### Step 1+2: Scan Structure + Analyze Content IN PARALLEL per Skill

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Scan skills structure" as `in_progress`.

Launch one Agent per skill with `run_in_background: true` and `model: "sonnet"`. Each agent scans structure AND analyzes content for its assigned skill independently. All agents run simultaneously.

Each agent performs for its assigned skill:

1. **Check required files and directories:**

   | File/Directory | Required | Purpose |
   |----------------|:--------:|---------|
   | `SKILL.md` | Yes | Main skill definition |
   | `guidelines.md` | Yes | Implementation guidelines |
   | `examples/` | Yes | Example output directory |
   | `examples/*.md` or `examples/*.js` | Yes | At least 1 example file |
   | `testing/` | Yes | Test artifacts directory |
   | `testing/test_cases.md` | Yes | Test cases for the skill |
   | `testing/evaluations.json` | Yes | Evaluation scaffold |

2. **Record findings per skill:**
   - List of missing files/directories
   - List of present files/directories

**Part B: Read SKILL.md and guidelines.md, then run these 11 check categories:**

**CRITICAL**: Read the guidelines.md file in this skill's directory for the complete list of check rules, PASS/FAIL criteria, and examples before running checks.

**See guidelines.md** for detailed Check 1-11 definitions (Frontmatter, Structure, File References, Skill References, MCP Parameters, Message Formatting, Step Numbering, JIRA Comments, MCP Setup, Standard Sections, Dependencies).

**Progress Update:**
```
Step 2/4: Analyzed content consistency

Check Results Summary:
- Frontmatter: {PASS_COUNT}/{TOTAL} passed
- Structure: {PASS_COUNT}/{TOTAL} passed
- File References: {PASS_COUNT}/{TOTAL} passed
- Skill References: {PASS_COUNT}/{TOTAL} passed
- MCP Parameters: {PASS_COUNT}/{TOTAL} passed
- Message Formatting: {PASS_COUNT}/{TOTAL} passed
- Step Numbering: {PASS_COUNT}/{TOTAL} passed
- JIRA Comments: {PASS_COUNT}/{TOTAL} passed
- MCP Setup: {PASS_COUNT}/{TOTAL} passed
- Standard Sections: {PASS_COUNT}/{TOTAL} passed
- Dependencies: {PASS_COUNT}/{TOTAL} passed

Total Issues: {TOTAL_ISSUES}

Proceeding to generate report...
```

---

### Step 3: Generate Report

**Todo:** Mark "Analyze content consistency" as `completed`, mark "Generate review report" as `in_progress`.

1. **Build the summary table:**

   ```markdown
   ## Skills Consistency Review Report

   **Date:** {CURRENT_DATE}
   **Skills Reviewed:** {TOTAL_SKILLS}
   **Total Checks:** {TOTAL_CHECKS} (10 categories x {TOTAL_SKILLS} skills)
   **Issues Found:** {TOTAL_ISSUES}

   ### Summary

   | Skill | Structure | Frontmatter | References | Params | Messages | Steps | JIRA | MCP Setup | Sections | Deps | Score |
   |-------|:---------:|:-----------:|:----------:|:------:|:--------:|:-----:|:----:|:---------:|:--------:|:----:|:-----:|
   | {skill_1} | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 10/10 |
   | {skill_2} | FAIL | PASS | PASS | FAIL | PASS | PASS | N/A | PASS | PASS | PASS | 8/10 |
   | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | .../10 |
   ```

   **Notes:**
   - Use `N/A` when a check doesn't apply (e.g., skill has no JIRA comment calls)
   - `N/A` counts as passing in the score

2. **List detailed findings per skill:**

   ```markdown
   ### Details

   #### {skill_name}

   **Score: {X}/9**

   Issues:
   - [FAIL] Check 2 (Structure): Missing `guidelines.md`
   - [FAIL] Check 5 (MCP Params): `issueKey` found at SKILL.md:207 — should be `issue_key`

   No issues:
   - [PASS] Check 1, 3, 4, 6, 7, 8, 9, 10
   ```

3. **Prioritize recommendations:**

   ```markdown
   ### Recommendations

   **High Priority:**
   - {skill_name}: Add missing guidelines.md (Check 2)
   - {skill_name}: Fix MCP parameter name at SKILL.md:207 (Check 5)

   **Medium Priority:**
   - {skill_name}: Standardize error message format (Check 9)

   **Low Priority:**
   - {skill_name}: Add Step 0 pre-flight delegation note (Check 7)
   ```

4. **If all checks pass:**
   ```
   All {TOTAL_SKILLS} skills passed all 10 consistency checks.
   No issues found. Skills are consistent and well-structured.
   ```

---

### Step 4: Offer to Fix

**Todo:** Mark "Generate review report" as `completed`, mark "Present report and offer to fix" as `in_progress`.

1. **Present the report to the user** (display the full report from Step 3).

2. **If issues were found, ask user via AskUserQuestion:**
   - **"Fix all issues automatically" (Recommended)** -- Apply all fixes
   - **"Let me choose which issues to fix"** -- Present issues one by one
   - **"Don't fix, keep report only"** -- Exit with report displayed

3. **Handle user response:**

   **If "Fix all issues automatically":**
   - For each issue, apply the appropriate fix:
     - Missing files → Create from template (use existing skills as reference)
     - Wrong frontmatter → Remove `name` field
     - Wrong references → Replace `/exp-` with `/exp-qa-agents:`
     - Wrong MCP params → Replace `issueKey`/`issueId` with `issue_key`
     - Wrong message format → Standardize to established pattern
     - Duplicate step numbers → Fix sequential numbering
     - Wrong JIRA comment → Add "skill." suffix
     - Wrong MCP setup → Replace with standard template
   - Report what was fixed:
     ```
     Applied {FIX_COUNT} fixes:

     - {skill_name}: Created guidelines.md
     - {skill_name}: Fixed issueKey → issue_key at SKILL.md:207
     - ...

     Re-run /common-qa:review-skills to verify all issues are resolved.
     ```

   **If "Let me choose which issues to fix":**
   - Present each issue with AskUserQuestion:
     - **"Fix this issue"** -- Apply the fix
     - **"Skip this issue"** -- Leave as-is
   - Report results after all issues processed

   **If "Don't fix, keep report only":**
   - Display final message:
     ```
     Review complete. {TOTAL_ISSUES} issue(s) found across {AFFECTED_SKILLS} skill(s).

     You can fix these manually or re-run /common-qa:review-skills later.
     ```

**Todo:** Mark "Present report and offer to fix" as `completed`. All todos should now be `completed`.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
