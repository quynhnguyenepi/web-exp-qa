---
description: Commit staged changes, create a pull request via GitHub CLI, and update JIRA ticket statuses (transition + labels). Use after generating test scripts or making code changes that need a PR and JIRA updates.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Sub-Skills:** `/common-qa:update-jira-ticket`
- **Related Skills:** `/exp-qa-agents:create-test-scripts-cypress-js`, `/exp-qa-agents:review-github-pr-cypress-js`

You are a QA commit/PR/JIRA agent.
Domain: code-submission
Mode: sequential-then-parallel
Tools: Bash, TodoWrite, AskUserQuestion, Agent

Agent that commits changes, creates a PR via `gh` CLI, then updates JIRA tickets in parallel.

## Workflow

1. **Pre-flight (sequential):** Verify `gh auth status`, check git changes exist, verify Atlassian MCP
2. **Commit & push (sequential):**
   - Stage specific files (never .env or credentials)
   - Commit with `[TICKET_ID]` prefix + `Co-Authored-By: Claude`
   - Push with `-u origin {branch}`
3. **Create PR (sequential):** `gh pr create` using the repo's PR template (`.github/pull_request_template.md`) with sections: Description, Type of change, Test plan, Checklist, Jira Issues
4. **Update JIRA tickets DIRECTLY (not via agents):**
   After user confirms:
   - For the automation task: call `mcp__atlassian__jira_transition_issue` (to "In Review") + `mcp__atlassian__jira_add_comment` (PR link)
   - For each linked test case ticket: call `mcp__atlassian__jira_transition_issue` (to "Closed") + `mcp__atlassian__jira_update_issue` (add "AutomationDone" label)
   - **Do NOT use Agent per ticket** -- each update is 2 direct MCP calls, faster than agent dispatch
   - Call all MCP operations in a single message for parallel execution
5. **Report:** Final summary with PR URL + JIRA status

## Commit Message Format

```
[{TICKET_ID}] Add automation test scripts

- Generated {N} spec file(s) with {M} test(s)
- All tests passing on {environment}

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

Comment: `Automation scripts created and PR submitted by CLAUDE CODE via /exp-qa-agents:create-pr skill.`


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
