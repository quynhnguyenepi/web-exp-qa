# Read JIRA Context - Guidelines

## Comment Filtering Rules

**Keep comments that contain:**
- Clarifications on acceptance criteria or requirements
- Edge cases or scenarios discussed by stakeholders
- Design decisions or technical constraints
- Bug reports or issues related to the feature
- Links to external resources (specs, designs, PRDs)

**Discard comments that are:**
- Status update bot messages (e.g., "Moved to In Progress")
- CI/CD notifications (build passed/failed)
- Automated workflow messages (Jira automation, GitHub integration)
- Duplicate/empty comments

## Linked Ticket Limits

- Max 5 linked tickets fetched
- If more exist, process first 5 by link type priority: Blocks > Relates to > Is tested by > Other
- Always note the total count even if not all are fetched

## Epic Children Relevance Signals

When listing epic children, highlight tickets that:
- Have `Requires_QA` label
- Are of type Bug (potential regressions)
- Are in "In Testing" or "In Review" status
- Share the same assignee as the primary ticket
- Have been updated in the last 7 days

## URL Extraction Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Confluence | `atlassian.net/wiki` | `https://org.atlassian.net/wiki/spaces/SPACE/pages/123/Title` |
| Figma | `figma.com/(file\|design\|proto)/` | `https://www.figma.com/design/ABC123/File-Name` |
| GitHub PR | `github.com/.*/pull/\d+` | `https://github.com/org/repo/pull/42` |

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify Atlassian MCP, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Fetch main ticket details", status: "pending", activeForm: "Fetching ticket details" },
  { content: "Parse and filter comments", status: "pending", activeForm: "Parsing comments" },
  { content: "Fetch parent + children + linked tickets with comments (parallel)", status: "pending", activeForm: "Fetching parent, children, and linked tickets" },
  { content: "Return structured output", status: "pending", activeForm: "Returning structured output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| JIRA ticket not found (404) | Display error with ticket ID, ask user to verify |
| Ticket has no description or AC | Check comments for context, then ask user |
| Parent ticket not found | Log "No parent ticket", skip parent section |
| Subtask/child fetch fails | Log warning, continue with remaining children |
| Linked ticket fetch fails | Log warning, continue with remaining |
| Non-Story/Bug children found | Skip them, only fetch Story and Bug types |
| Comment fetch fails for related ticket | Log warning, show ticket without comments |

---


## Self-Correction

1. **"Check another ticket too"** -> Fetch additional ticket, merge into output
2. **"Include all comments, not just relevant ones"** -> Remove comment filtering
3. **"The parent key is wrong"** -> Accept corrected parent key, re-fetch
4. **"Skip children comments"** -> Fetch children summary only, no comments
5. **"Also read siblings' comments"** -> Fetch comments for sibling tickets too

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Ticket details, linked tickets, epic (REQUIRED) | No fallback |

### Input Flexibility

| Input Type | Example |
|------------|---------|
| JIRA ticket ID | `CJS-10873` |
| JIRA URL | `https://optimizely-ext.atlassian.net/browse/CJS-10873` |
