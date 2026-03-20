# Sample: Update create-test-cases Skill After Training Session

---

## Input

User request: "I just spent a session training Claude on how to handle tickets with no description. Update the create-test-cases skill with what we learned."

Learnings from session:
1. When a JIRA ticket has no description, Claude should look at the ticket's comments and linked tickets for context
2. Should ask the user for a brief description if nothing is available
3. Should not generate test cases from only the title

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - Skill: create-test-cases
   - Plugin: exp-qa
   - Path: plugins/exp-qa-agents/skills/create-test-cases/
   - Files found: SKILL.md, guidelines.md, examples/, testing/

Proceeding to capture learnings...
```

---

## Step 1: Capture Learnings

```
Learnings captured:

SKILL.md changes:
- Step 1 (Analyze Ticket): Add fallback logic when description is empty

guidelines.md changes:
- Add rule: "Tickets without descriptions need alternative context sources"
- Add anti-pattern: "Generating test cases from title only"

New test cases:
- TC-XXX: Handle ticket with no description
```

---

## Step 2: Plan Updates

```
Planned Updates:

1. SKILL.md
   - Section: "Step 1: Analyze Ticket"
   - Change: Add sub-steps for empty description handling:
     a. Check ticket comments for context
     b. Check linked tickets for related context
     c. If still no context, ask user via AskUserQuestion
   - Reason: Session showed Claude generates poor test cases from title alone

2. guidelines.md
   - Section: "Anti-Patterns" (new entry)
   - Change: Add "Generating from Title Only" anti-pattern
   - Reason: Discovered during session that title-only generation produces vague tests

3. testing/test_cases.md
   - New test: TC-015: Handle ticket with no description
   - Content: Verify fallback to comments/linked tickets, then user input
```

User selected: "Apply all planned updates"

---

## Step 3: Apply Updates

```
Updates Applied:

Modified files:
- SKILL.md: Updated Step 1 (added empty description handling)
- guidelines.md: Added "Generating from Title Only" anti-pattern
- testing/test_cases.md: Added TC-015

Lines changed: +24 / -0
```

---

## Step 4: Verify & Report

```
Skill update complete!

Skill: create-test-cases
Plugin: exp-qa

Changes:
- SKILL.md: 1 section updated (Step 1: Analyze Ticket)
- guidelines.md: 1 anti-pattern added
- testing/: 1 test case added (TC-015)

Recommendations:
- Run /common-qa:review-skills to verify consistency across all skills
- Test the updated skill with a ticket that has no description
```
