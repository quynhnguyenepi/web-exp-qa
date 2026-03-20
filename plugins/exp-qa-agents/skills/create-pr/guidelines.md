# PR Creation & JIRA Update Guidelines

Standards for committing changes, creating pull requests, and updating JIRA ticket statuses consistently.

## Commit Message Format

### Structure

```
[{TICKET_ID}] {Brief description of changes}

- {Detail line 1}
- {Detail line 2}
- {Detail line 3}

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### Good Examples

```
[QAK-14900] Add automation test scripts for AB test archive

- Generated 1 spec file with 5 tests
- Test cases from linked JIRA tickets: QAK-14901, QAK-14902, QAK-14903
- All tests passing on integration environment

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### Bad Examples

```
update tests                     # No ticket ID, too vague
[QAK-14900] stuff                # Not descriptive
Added some files for automation  # No ticket reference, vague
```

---

## PR Body Format

**IMPORTANT:** Always use the repository's PR template (`.github/pull_request_template.md`) as the structure. Fill in each section as follows:

```markdown
### Description
- {What was generated/changed}
- {Scope: N spec file(s) with M test(s)}
- {Status: All tests passing on {environment}}
- {List of JIRA test case ticket IDs with titles}

Generated with [Claude Code](https://claude.com/claude-code) via /exp-qa-agents:create-pr

### Type of change

- [x] Add new script
- [ ] Fix failed daily run
- [ ] Refactor code
- [ ] Optimization
- [ ] Add/change config
- [ ] Add/change workflow

### Test plan
- All tests pass on {environment} environment
- {Attach test results if available}

### Checklist

- [x] Create automation ticket, assignee is the script writer, link test cases to automation ticket
- [x] Follow coding convention sheet
- [x] Always pull the latest code before push PR
- [x] Keep consistency in coding
- [x] Avoid to duplicate code
- [x] All tests must be passed
- [x] Remove all ".only()" and ".pause()" before push PR
- [ ] If refactor code, need to re-run all related test scripts
- [ ] Change status of automation ticket to In Review
- [ ] Add label AutomationDone and close test case as Done
- [ ] Update list automated test cases to automation file
- [ ] When defining new tag value, must add it to Confluence page and tag list file; if it is for Flags, must add it to respective Daily Run FX workflow
- [x] Ensure test cases include 100% preconditions, test data, steps, and expected results

### Jira Issues

[QAK-{ISSUE_ID}](https://jira.sso.episerver.net/browse/QAK-{ISSUE_ID})
```

### Filling Rules

- **Type of change:** Check only the applicable type(s). Default for new test scripts is "Add new script"
- **Checklist:** Check items that are confirmed done. Leave unchecked items the user must verify post-PR (e.g., updating automation file, JIRA transitions)
- **Jira Issues:** Replace `{ISSUE_ID}` with the actual automation ticket number (e.g., `QAK-14900`)

---

## File Staging Rules

### Always Stage
- Generated spec files (`cypress/e2e/**/*.spec.js`)
- New/modified page objects (`cypress/pages/**/*.js`)
- New/modified builders (`cypress/support/builders/**/*.js`)
- Updated tag lists (`cypress/support/resources/tagList.js`)

### Never Stage
- `.env` files
- Credentials or API tokens
- `.claude/settings.local.json`
- `node_modules/`
- OS files (`.DS_Store`)

---

## JIRA Transition Rules

### Automation Task Transition

**Target status:** "In Review"

**Search for transition names (try in order):**
1. "In Review"
2. "Review"
3. "Ready for Review"
4. "Submit for Review"

If no matching transition found, report to user and skip.

### Test Case Ticket Transitions

**Target status:** "Closed" or "Done"

**Search for transition names (try in order):**
1. "Closed"
2. "Done"
3. "Close"
4. "Resolve"

**Additional action:** Add `AutomationDone` label to each test case ticket.

### Comment Identification

Always add an identification comment to the automation task:
```
Automation scripts created and PR submitted by CLAUDE CODE via /exp-qa-agents:create-pr skill.
```

---

## Branch Naming

### Format

```
{shortName}/{TICKET_ID}-{sanitized-title}
```

### Rules
- `shortName`: User's abbreviated name (e.g., "phanh", "cuongph")
- `TICKET_ID`: JIRA ticket ID in uppercase (e.g., "QAK-14900")
- `sanitized-title`: Lowercase, hyphens instead of spaces, no special chars

### Examples
- `phanh/QAK-14900-ab-test-archive-functionality`
- `cuongph/APPX-5570-delete-variations-rule`

---

## Anti-Patterns

### Staging Sensitive Files
**Problem**: Credentials or local config pushed to remote
**Solution**: Only stage specific files, never use `git add -A`

### Missing Co-Authored-By
**Problem**: No attribution for AI-generated code
**Solution**: Always include `Co-Authored-By` in commit message

### Force Pushing
**Problem**: Overwrites upstream history
**Solution**: Never force push; if push fails, investigate and resolve

### Skipping Test Execution Note
**Problem**: PR says "all tests passing" but tests weren't run
**Solution**: If tests were skipped, note it in the PR body

---

## Quality Checklist

Before creating the PR:

- [ ] Only relevant files are staged (no credentials, no .env)
- [ ] Commit message includes ticket ID and Co-Authored-By
- [ ] PR title follows `[{TICKET_ID}] {description}` format
- [ ] PR body follows repo template: Description, Type of change, Test plan, Checklist, Jira Issues
- [ ] Branch pushed with `-u` flag
- [ ] JIRA automation task transitioned to "In Review" (if applicable)
- [ ] Test case tickets closed with "AutomationDone" label (if applicable)
- [ ] Identification comment added to JIRA task

---

## References

This guidelines document should be read during PR creation to ensure consistency. SKILL.md references these patterns when committing, pushing, and updating JIRA.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| `gh` not authenticated | Display `gh auth login` instructions |
| No changes to commit | Ask user what to stage |
| JIRA transition not found | List available, skip gracefully |


## Self-Correction

1. **"Use a different PR title"** → `gh pr edit`
2. **"Don't close test case X"** → Skip that ticket
