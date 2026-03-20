# Update Skills Guidelines

Standards for capturing learnings from AI training sessions and updating skill files consistently.

## Change Categories

### Workflow Changes (SKILL.md)

Changes to the execution steps, ordering, or logic.

**When to modify:**
- A step is missing or needs to be reordered
- Error handling is incomplete
- Pre-flight checks need additions
- Self-correction options need updating

**How to modify:**
- Keep step numbering sequential (Step 0, 1, 2, ...)
- Update the Workflow Overview diagram to match
- Update the Simple Flow line
- Update the Progress Tracking todo list

### Guideline Changes (guidelines.md)

Changes to rules, patterns, or anti-patterns.

**When to modify:**
- A new rule was discovered
- An anti-pattern was identified
- Quality checklist needs new items
- Existing rules need refinement

**How to modify:**
- Add to the appropriate section
- Keep formatting consistent with existing entries
- Include the "Problem / Solution" format for anti-patterns

### Example Changes (examples/)

New or updated example outputs.

**When to add:**
- A session produced a particularly good output
- An edge case was handled well
- A new use case was demonstrated

**How to add:**
- Follow the naming convention: `sample-{description}.md`
- Include: Input, Step-by-step execution, Output
- Keep examples realistic (based on actual interactions)

### Test Case Changes (testing/)

New test cases from discovered scenarios.

**When to add:**
- An edge case was found that isn't covered
- A failure scenario was discovered
- A new use case needs validation

**How to add:**
- Continue the TC-XXX numbering from the last test case
- Follow the format: Input, Expected, Pass Criteria
- Include both happy path and error scenarios

---

## Consistency Rules

### 1. Skill Reference Format

All skill references must use the plugin:skill-name format:
- `/exp-qa-agents:create-test-cases` (correct)
- `/common-qa:mass-update-jira-tickets` (correct)
- `/exp-create-test-cases` (wrong — missing colon)

### 2. Frontmatter Format

SKILL.md must have only `description` in frontmatter:
```yaml
---
description: Brief description of what the skill does.
---
```

Never include `name` field in frontmatter.

### 3. MCP Parameter Names

Always use `issue_key` (snake_case), never `issueKey` (camelCase).

### 4. Step Numbering

Steps must start at Step 0 and be sequential with no gaps:
```
### Step 0: Pre-Flight Checks
### Step 1: Do Something
### Step 2: Do Next Thing
```

### 5. JIRA Comment Identification

Comments posted to JIRA must follow:
```
{Action} by CLAUDE CODE via /{plugin}:{skill-name} skill.
```

### 6. Required Sections in SKILL.md

Every SKILL.md must have:
- `## When to Use`
- `## Workflow Overview`
- `## Progress Tracking`
- `## Execution Workflow`
- `## Error Handling`
- `## Self-Correction`
- `## Notes`

---

## Capturing Learnings Process

### From Chat Context

Look for these signals in the conversation:

| Signal | What It Means |
|--------|--------------|
| User corrects Claude's output | The skill's instructions are unclear |
| Claude retries an action | Error handling or pre-validation missing |
| User says "that's not right" | The workflow or guidelines need updating |
| User provides a better approach | Update guidelines or workflow |
| User says "remember this" | Needs to be persisted in skill files |
| User asks "why did it do X?" | The skill's logic is unclear |

### From User Input

Ask structured questions:

1. **"What went wrong?"** → Identifies gaps in the workflow
2. **"What should it have done?"** → Identifies the correct behavior
3. **"Was there a specific step that failed?"** → Pinpoints the section to update
4. **"Would this apply to other skills too?"** → Cross-cutting change

---

## Quality Checklist

Before finalizing skill updates:

- [ ] Changes are consistent with the skill's existing style
- [ ] Step numbering is still sequential
- [ ] Skill references use the correct format
- [ ] New test cases follow the TC-XXX convention
- [ ] Examples are realistic and complete
- [ ] No placeholder content left
- [ ] Anti-patterns include both Problem and Solution
- [ ] Updated sections don't break other sections

---

## Anti-Patterns

### Changing Too Much at Once
**Problem**: Updating multiple unrelated things in one pass risks introducing inconsistencies
**Solution**: Group related changes, apply in logical batches

### Not Capturing the "Why"
**Problem**: Just changing the code without noting why leads to confusion later
**Solution**: Add comments or notes explaining the reasoning for changes

### Ignoring Other Skills
**Problem**: A change to one skill may affect how others reference it
**Solution**: Check cross-references with `/common-qa:review-skills` after updating

### Adding Examples Without Context
**Problem**: Examples without clear input/output context are hard to follow
**Solution**: Always include: what the user asked, what happened, what the output was

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (identify skill, verify structure)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Capture learnings from session", status: "pending", activeForm: "Capturing learnings from session" },
  { content: "Plan updates to skill files", status: "pending", activeForm: "Planning updates to skill files" },
  { content: "Apply updates to skill files", status: "pending", activeForm: "Applying updates to skill files" },
  { content: "Verify changes and report", status: "pending", activeForm: "Verifying changes and reporting" }
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
| Skill directory not found | Ask user for correct skill name, list available skills |
| SKILL.md is malformed | Warn user, suggest manual review before updating |
| No learnings provided | Ask user to describe what they want to change |
| Conflicting changes | Show conflict, ask user to resolve |
| File write fails | Report error, show the content that should be written |
| Skill not in any plugin | Ask user which plugin it belongs to |

---


## Self-Correction

When user requests adjustments:

1. **"I want to change a different skill"** → Restart with the new skill
2. **"Add more detail to the change"** → Expand the specific update
3. **"Don't change SKILL.md, only guidelines"** → Limit updates to specified files
4. **"Undo the last change"** → Revert the most recent file modification
5. **"Also update the evaluations"** → Update evaluations.json with new test scenarios
6. **"Show me a before/after diff"** → Display diff for each modified file

---


## Notes

### What Gets Updated

| File | Typical Updates |
|------|----------------|
| `SKILL.md` | Workflow steps, error handling, notes, integration references |
| `guidelines.md` | Rules, anti-patterns, quality checklists, best practices |
| `examples/*.md` | New example outputs from successful sessions |
| `testing/test_cases.md` | New test cases from discovered edge cases |
| `testing/evaluations.json` | New evaluation scenarios (if applicable) |

### When to Use This vs Manual Editing

| Scenario | Recommendation |
|----------|---------------|
| Small typo fix | Edit directly |
| Add one test case | Edit directly |
| Multiple changes from a training session | Use this skill |
| Restructure a skill's workflow | Use this skill |
| Add learnings from real-world usage | Use this skill |

### Integration with Other Skills

- **`/common-qa:review-skills`**: After updating, run review to verify consistency
- **`/common-qa:update-claude`**: If skill changes affect CLAUDE.md references, update that too
