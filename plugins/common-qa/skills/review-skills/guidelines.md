# Skills Consistency Review Guidelines

Complete reference for all check categories, pass/fail criteria, and standard patterns to compare against.

## Check Categories

### Check 1: Frontmatter Format

**What to check:** The YAML frontmatter at the top of SKILL.md.

**Rules:**
- Must start with `---` on line 1
- Must contain `description:` field
- Must NOT contain `name:` field
- Must end with `---`

**PASS example:**
```yaml
---
description: Short description of what the skill does. Use when...
---
```

**FAIL examples:**
```yaml
---
name: my-skill
description: Description here
---
```
Reason: `name` field present — remove it.

```yaml
---
name: my-skill
---
```
Reason: `name` field present and `description` field missing.

---

### Check 2: Directory Structure Completeness

**What to check:** All required files and directories exist for each skill.

**Required structure:**
```
skill-name/
├── SKILL.md              (required)
├── guidelines.md         (required)
├── examples/             (required directory)
│   └── sample-*.md|*.js  (at least 1 file)
└── testing/              (required directory)
    ├── test_cases.md     (required)
    └── evaluations.json  (required)
```

**PASS:** All files and directories present.
**FAIL:** Any required file or directory missing. List which ones.

---

### Check 3: File Path References

**What to check:** File paths referenced in SKILL.md that the agent is instructed to read.

**Patterns to search for:**
- `Read .claude/...`
- `Read plugins/...`
- `Read cypress/...`
- Any explicit file path in code blocks

**PASS:** All referenced paths exist on disk, or use relative references like "from this skill's directory".
**FAIL:** A referenced path doesn't exist. Show the path and where it's referenced.

**Standard pattern:** Use `Read guidelines.md from this skill's directory` instead of absolute paths.

---

### Check 4: Skill Reference Format

**What to check:** How skills reference each other throughout all files.

**Valid format:** `/exp-qa-agents:skill-name` (colon separator)
**Invalid format:** `/exp-skill-name` (hyphen separator)

**Search pattern:** Look for `/exp-` anywhere in the skill's files.

**PASS:** No `/exp-` references found (all use `/exp-qa-agents:` format).
**FAIL:** Found `/exp-skill-name` pattern. Show file and line number.

**Exclusion:** The skill name itself (e.g., `exp-generate-test-scripts` in evaluation runner names) is acceptable as an internal identifier, but all invocation references must use colon format.

---

### Check 5: MCP Parameter Names

**What to check:** Parameter names used in MCP API call examples.

**Valid:** `issue_key` (snake_case, matches actual Atlassian MCP API)
**Invalid:** `issueKey` (camelCase) or `issueId`

**Search patterns:**
- `issueKey` in context of `mcp__atlassian__` calls
- `issueId` in context of `mcp__atlassian__` calls

**PASS:** All MCP call examples use `issue_key`.
**FAIL:** Found `issueKey` or `issueId`. Show file and line number.

**Note:** Only check within MCP call context. Variable names in JSON examples or test data structures are not checked.

---

### Check 6: Message Formatting

**What to check:** Consistency of status messages, progress updates, and error messages.

**Rules:**

1. **No emojis in status/progress messages:**
   - Pre-flight status: `Pre-flight checks passed` (not `✅ Pre-flight checks passed`)
   - Step progress: `Step 1: Gathered context` (not `✅ Step 1: Gathered context`)
   - Exception: Emojis in output templates meant for external display (e.g., PR review body posted to GitHub) are acceptable

2. **Error message format:**
   ```
   Error: {Description}

   This skill requires {tool/MCP} for {purpose}.

   Setup Instructions:
   1. {Step}
   2. {Step}
   3. {Step}

   See {reference} for detailed configuration.
   Cannot proceed without {requirement}.
   ```

**PASS:** No emojis in status messages, error format follows standard.
**FAIL:** Emojis found in status/progress messages, or error format deviates significantly.

**How to distinguish status vs output messages:**
- Status messages: Pre-flight reports, step progress updates, completion reports
- Output messages: PR review body, JIRA ticket descriptions, generated report content

---

### Check 7: Step Numbering

**What to check:** Sequential step numbering in the Execution Workflow section.

**Rules:**
1. Steps should start at Step 0 (pre-flight checks)
2. Steps should be sequential (0, 1, 2, 3...) with no gaps
3. No duplicate step numbers
4. Numbered sub-steps within a step should also be sequential with no duplicates
5. If pre-flight is delegated to another skill, a brief Step 0 noting the delegation is acceptable

**Search pattern:** `### Step N:` headings in SKILL.md

**PASS:** Sequential numbering starting at 0, no gaps, no duplicates.
**FAIL:** Gaps in numbering, duplicate numbers, or missing Step 0. Show where.

---

### Check 8: JIRA Comment Identification

**What to check:** Identification comments added to JIRA tickets created by the skill.

**Standard template:**
```
{Action} by CLAUDE CODE via /exp-qa-agents:{skill-name} skill.
```

**Examples:**
- `Bug is created by CLAUDE CODE via /exp-qa-agents:create-bug-ticket skill.`
- `Test case is created by CLAUDE CODE via /exp-qa-agents:create-test-cases skill.`
- `Automation scripts created and PR submitted by CLAUDE CODE via /exp-qa-agents:create-pr skill.`

**PASS:** Comment text follows template, ends with "skill.", uses `/exp-qa-agents:` format.
**FAIL:** Missing "skill." suffix, uses `/exp-` format, or significantly deviates from template.

**N/A:** Skill does not create JIRA tickets or add identification comments.

---

### Check 9: MCP Setup Instructions

**What to check:** Error messages shown when a required MCP server is unavailable.

**Standard format:**
```
Error: {MCP name} is not configured

This skill requires {MCP name} server for {purpose}.

Setup Instructions:
1. Ensure .mcp.json exists in project root with {MCP} server configuration
2. Restart Claude Code
3. Verify access with: {verification command}

See .mcp.json for detailed configuration.
Cannot proceed without {MCP} configuration.
```

**Key elements:**
- Uses "not configured" (not "not enabled")
- References `.mcp.json` (not `.claude/settings.local.json`)
- Includes 3 setup steps
- Ends with "Cannot proceed" statement

**PASS:** Error message follows standard format.
**FAIL:** Uses different file reference, different wording, or missing elements.

**N/A:** Skill does not require any MCP servers.

---

### Check 10: Standard Sections Present

**What to check:** Required sections in SKILL.md.

**Required sections:**

| Section | Heading Pattern |
|---------|----------------|
| When to Use | `## When to Use` |
| Workflow Overview | `## Workflow Overview` |
| Progress Tracking | `## Progress Tracking` |
| Execution Workflow | `## Execution Workflow` |
| Error Handling | `## Error Handling` |
| Self-Correction | `## Self-Correction` |
| Notes | `## Notes` |

**PASS:** All 7 required sections present.
**FAIL:** Any section missing. List which ones.

---

### Check 11: Dependency Consistency

**What to check:** Dependencies declared in SKILL.md match actual usage and CLAUDE.md dependency chain.

**Rules:**
1. Every skill referenced as a Sub-Skill must exist under `plugins/*/skills/`
2. Sub-Skills must use the correct `/{plugin}:{skill-name}` format (verified by Check 4, but this check validates existence)
3. Dependencies should be classified as `(required)`, `(optional)`, or `(conditional)` for orchestrator skills
4. MCP Servers should be classified as `(required)`, `(recommended)`, or `(optional)` for orchestrator skills
5. Sub-Skills listed in SKILL.md should match what's documented in CLAUDE.md's Skill Dependency Chain section

**Verification steps:**
1. Parse the `## Dependencies` section of SKILL.md
2. Extract all `/plugin:skill-name` references from Sub-Skills lines
3. For each reference, verify that `plugins/{plugin}/skills/{skill-name}/SKILL.md` exists
4. For orchestrator skills (Mode: orchestrator), check that dependencies are classified with `(required)` / `(optional)` / `(conditional)`
5. Cross-reference with CLAUDE.md Skill Dependency Chain -- warn if a sub-skill is listed in SKILL.md but missing from CLAUDE.md (or vice versa)

**PASS:**
- All referenced sub-skills exist on disk
- Orchestrator skills classify dependencies
- CLAUDE.md dependency chain matches SKILL.md declarations

**FAIL:**
- Referenced sub-skill doesn't exist (show which reference and expected path)
- Orchestrator skill has unclassified dependencies (flat list without `(required)`/`(optional)`)
- CLAUDE.md dependency chain is missing a declared sub-skill

**N/A:** Skill has no Sub-Skills declared (standalone skill).

---

## Adding New Checks

To add a new check category:

1. Add the check definition to this guidelines.md with:
   - Check number (next sequential)
   - What to check
   - Rules (specific, testable criteria)
   - PASS/FAIL criteria with examples
   - N/A conditions (when the check doesn't apply)

2. Add the check to SKILL.md:
   - Add to Step 2 under a new `#### Check N:` heading
   - Add to the Check Categories Reference table in Notes
   - Update the summary table column count

3. Update the report template in Step 3 to include the new column.

---

## Quality Checklist

Before finalizing a review report:

- [ ] All skills discovered (none accidentally skipped)
- [ ] Each check category run against each skill
- [ ] N/A correctly applied (not counted as FAIL)
- [ ] File paths and line numbers included for FAIL findings
- [ ] Recommendations prioritized (High/Medium/Low)
- [ ] Report is clear and actionable
- [ ] This skill (review-skills) excluded from the review

---

## References

This guidelines document should be read during Step 2 (Analyze Content Consistency) to ensure all checks are applied correctly. SKILL.md references these patterns when evaluating each skill.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (discover skills, validate structure)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Scan structure + analyze content (parallel per skill)", status: "pending", activeForm: "Scanning and analyzing all skills in parallel" },
  { content: "Generate review report", status: "pending", activeForm: "Generating review report" },
  { content: "Present report and offer to fix", status: "pending", activeForm: "Presenting report" }
])
```

**Update rules:**
- Mark current step as `in_progress` when starting it
- Mark step as `completed` immediately when finished (do not batch)
- Only ONE step should be `in_progress` at any time
- If all checks pass, mark Step 4 as `completed` with content "Skipped -- all checks passed"

---


## Error Handling

| Error | Action |
|-------|--------|
| Skills directory not found | Display error with expected path, exit |
| No skills discovered | Display error, suggest checking directory structure |
| SKILL.md unreadable or malformed | Log warning for that skill, continue with others |
| Fix fails (file write error) | Log error, continue with remaining fixes, report at end |
| Skill has no MCP calls to check | Mark MCP-related checks as N/A, not FAIL |

---


## Self-Correction

When user requests adjustments:

1. **"Check only specific skills"** -- Re-run checks on specified skills only
2. **"Add a new check category"** -- Update guidelines.md with the new check, re-run
3. **"Ignore check X for skill Y"** -- Skip that check/skill combination, note in report
4. **"Re-run after fixes"** -- Execute the full review again to verify fixes
5. **"Show me the details for skill X"** -- Display detailed findings for one skill

---


## Notes

### Key Principles

1. **Non-destructive by default**: Report issues without fixing unless user confirms
2. **Complete coverage**: Check ALL skills, not just recently changed ones
3. **Specific findings**: Always include file paths and line numbers for issues
4. **Prioritized recommendations**: High/Medium/Low based on impact
5. **Self-exclusion**: This skill excludes itself from the review to avoid circular checks

### Integration with Other Skills

This is a **meta-skill** that reviews other skills. It is not part of the QA workflow chain.

- **All skills**: This skill reviews all skills under `plugins/*/skills/` for consistency
- **`/exp-qa-agents:create-test-cases`**, **`/exp-qa-agents:analyze-ticket`**, etc.: These are the skills being reviewed, not invoked

### Input Flexibility

| Input Type | Example |
|------------|---------|
| No input (review all) | `/common-qa:review-skills` |
| Specific skill | `/common-qa:review-skills analyze-ticket` |
| Multiple skills | `/common-qa:review-skills analyze-ticket, create-pr` |

### Check Categories Reference

| # | Check | What It Verifies |
|---|-------|-----------------|
| 1 | Frontmatter | `description` only, no `name` field |
| 2 | Structure | SKILL.md, guidelines.md, examples/, testing/ all present |
| 3 | File References | Referenced file paths exist |
| 4 | Skill References | Uses `/exp-qa-agents:skill-name` not `/exp-skill-name` |
| 5 | MCP Parameters | Uses `issue_key` not `issueKey`/`issueId` |
| 6 | Message Formatting | No emojis in status messages, standard error format |
| 7 | Step Numbering | Starts at Step 0, sequential, no duplicates |
| 8 | JIRA Comments | Identification comment ends with "skill." |
| 9 | MCP Setup | Standard error format with .mcp.json reference |
| 10 | Standard Sections | All required sections present in SKILL.md |
| 11 | Dependencies | Sub-skills exist, orchestrators classify deps, CLAUDE.md chain matches |
