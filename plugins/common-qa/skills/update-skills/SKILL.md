---
description: Capture learnings from a chat or training session with AI and update skill files accordingly. Use after refining a skill through conversation, discovering better prompts, or training Claude on new patterns.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/common-qa:review-skills`

# Update Skills After Training Session

After a chat session where you've refined how a skill should work — discovered better prompts, fixed edge cases, or trained Claude on new patterns — this skill captures those learnings and updates the skill files (SKILL.md, guidelines.md, examples, tests) to persist the improvements.

## When to Use

Invoke this skill when you need to:

- Persist improvements discovered during a chat session into skill files
- Update a skill after finding that Claude handles a scenario incorrectly
- Add new examples from a successful interaction to the skill's examples directory
- Capture edge cases or gotchas discovered during real usage
- Refine skill prompts or workflow steps based on observed behavior
- Add new test cases based on real-world failures or successes

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  0. Pre-Flight Checks                                                            │
│     ├─ Identify which skill to update                                           │
│     └─ Verify skill directory structure exists                                   │
│                                                                                  │
│  1. Capture Learnings                                                            │
│     ├─ Ask user what was learned / what to change                               │
│     ├─ Review conversation context for insights                                 │
│     └─ Categorize changes (workflow, guidelines, examples, tests)               │
│                                                                                  │
│  2. Plan Updates                                                                 │
│     ├─ Read current skill files                                                 │
│     ├─ Identify sections to modify                                              │
│     └─ Draft changes for user review                                            │
│                                                                                  │
│  3. Apply Updates                                                                │
│     ├─ Update SKILL.md (workflow, steps, error handling)                        │
│     ├─ Update guidelines.md (rules, patterns, anti-patterns)                   │
│     ├─ Add/update examples (from successful interactions)                       │
│     ├─ Add/update test cases (from edge cases found)                           │
│     └─ Present summary of changes                                               │
│                                                                                  │
│  4. Verify & Report                                                              │
│     ├─ Review all modified files for consistency                                │
│     └─ Suggest running /common-qa:review-skills                                 │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Simple Flow:**
```
Pre-Flight → Capture Learnings → Plan Updates → Apply Updates → Verify & Report
```

## Execution Workflow

Follow these 5 sequential steps:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Identify which skill to update:**
   - If user specifies a skill name: validate it exists
   - If not specified, ask the user via AskUserQuestion:
     - "Which skill do you want to update?"
     - List available skills from `plugins/*/skills/` directories

2. **Verify skill directory structure:**
   - Check that the skill directory contains:
     - `SKILL.md` — main skill definition
     - `guidelines.md` — implementation guidelines
     - `examples/` — example outputs
     - `testing/` — test cases and evaluations
   - If any files are missing, note them (they may need to be created)

3. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Skill: {SKILL_NAME}
      - Plugin: {PLUGIN_NAME}
      - Path: plugins/{PLUGIN_NAME}/skills/{SKILL_NAME}/
      - Files found: SKILL.md, guidelines.md, examples/, testing/

   Proceeding to capture learnings...
   ```

---

### Step 1: Capture Learnings

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Capture learnings from session" as `in_progress`.

1. **Ask user what was learned or needs to change:**

   Use AskUserQuestion to gather input. The user may provide one or more of:

   | Learning Type | Example |
   |--------------|---------|
   | **Workflow change** | "Step 3 should come before Step 2" |
   | **New edge case** | "When ticket has no description, the skill crashes" |
   | **Better prompt** | "The search query should include status filter" |
   | **Missing step** | "Need to check for duplicate tickets before creating" |
   | **New example** | "This interaction went perfectly, save it as an example" |
   | **Anti-pattern** | "Never use issueKey, always use issue_key" |
   | **Test case** | "Need a test for when JQL returns 0 results" |

2. **Review conversation context (if available):**
   - Look at the current conversation for patterns that worked well
   - Identify any corrections the user made during the session
   - Note any retries or workarounds that indicate a skill gap

3. **Categorize changes by file:**
   ```
   Learnings captured:

   SKILL.md changes:
   - {change_1}
   - {change_2}

   guidelines.md changes:
   - {change_3}

   New examples:
   - {example_1}

   New test cases:
   - {test_1}
   ```

---

### Step 2: Plan Updates

**Todo:** Mark "Capture learnings from session" as `completed`, mark "Plan updates to skill files" as `in_progress`.

1. **Read current skill files:**
   - Read SKILL.md to understand current workflow
   - Read guidelines.md to understand current rules
   - List existing examples
   - Read test_cases.md to understand existing coverage

2. **Identify sections to modify:**
   - For each learning, identify which section of which file needs updating
   - Determine if it's an edit (modify existing content) or an addition (new content)

3. **Draft changes for user review:**
   ```
   Planned Updates:

   1. SKILL.md
      - Section: "Step 2: Search Tickets"
      - Change: Add pre-validation of JQL query before executing
      - Reason: Discovered that invalid JQL causes unclear errors

   2. guidelines.md
      - Section: "Anti-Patterns" (new entry)
      - Change: Add "Never use raw JQL without validation"
      - Reason: Session showed this causes confusing errors

   3. examples/
      - New file: sample-edge-case.md
      - Content: Example of handling empty search results

   4. testing/test_cases.md
      - New test: TC-XXX: Handle empty JQL results
      - Content: Verify graceful handling when JQL returns 0 results
   ```

4. **Ask user for confirmation via AskUserQuestion:**
   - **"Apply all planned updates" (Recommended)** — Apply all changes
   - **"Let me review each change"** — Show each change for approval
   - **"Modify the plan"** — Let user adjust what to update

---

### Step 3: Apply Updates

**Todo:** Mark "Plan updates to skill files" as `completed`, mark "Apply updates to skill files" as `in_progress`.

1. **Apply changes to each file:**

   **SKILL.md updates:**
   - Modify workflow steps (add, remove, reorder)
   - Update error handling table
   - Add/modify self-correction options
   - Update notes and integration sections

   **guidelines.md updates:**
   - Add new rules or patterns
   - Add new anti-patterns
   - Update quality checklist
   - Refine existing guidelines

   **examples/ updates:**
   - Create new example files from successful interactions
   - Update existing examples if they're outdated

   **testing/ updates:**
   - Add new test cases to test_cases.md
   - Follow the existing TC-XXX numbering convention

2. **Maintain consistency:**
   - Ensure skill references use correct format (e.g., `/exp-qa-agents:skill-name`, `/common-qa:skill-name`)
   - Keep formatting consistent with existing content
   - Don't break existing structure

3. **Report changes applied:**
   ```
   Updates Applied:

   Modified files:
   - SKILL.md: Updated Step 2 (added JQL validation)
   - guidelines.md: Added new anti-pattern entry
   - examples/sample-edge-case.md: Created new example
   - testing/test_cases.md: Added TC-014

   Lines changed: +{ADDED} / -{REMOVED}
   ```

---

### Step 4: Verify & Report

**Todo:** Mark "Apply updates to skill files" as `completed`, mark "Verify changes and report" as `in_progress`.

1. **Quick consistency check:**
   - Verify no broken references in modified files
   - Ensure new test case numbers don't conflict with existing ones
   - Check that examples follow the standard format

2. **Final report:**
   ```
   Skill update complete!

   Skill: {SKILL_NAME}
   Plugin: {PLUGIN_NAME}

   Changes:
   - SKILL.md: {N} sections updated
   - guidelines.md: {N} entries added/modified
   - examples/: {N} files created/updated
   - testing/: {N} test cases added

   Recommendations:
   - Run /common-qa:review-skills to verify consistency across all skills
   - Test the updated skill with the new edge cases
   ```

3. **Mark "Verify changes and report" as `completed`.** All todos should now be `completed`.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
