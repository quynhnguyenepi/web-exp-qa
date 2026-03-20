# Bug Ticket Creation Guidelines

Standards for searching existing bugs, creating JIRA bug tickets from test failures, and avoiding duplicate tickets.

## Duplicate Detection

### 1. Keyword Extraction

**Extract 2-3 key terms from the failure:**

| Source | What to Extract | Example |
|--------|----------------|---------|
| Test case title | Core action/feature nouns | "Verify login with invalid credentials" → `login invalid credentials` |
| Failure description | Error/behavior terms | "Page redirected instead of showing error" → `redirect error login` |
| Component/module | Feature area | "Authentication" → `authentication` |

**Remove common words:** the, a, is, to, for, in, on, with, and, or, that, this, it

### 2. JQL Search Strategy

**Search for existing bugs in the same project:**

```
project = {PROJECT} AND issuetype = Bug AND status != Done AND text ~ "{keywords}"
```

**If too many results (>10):** Narrow the search:
```
project = {PROJECT} AND issuetype = Bug AND status != Done AND summary ~ "{keywords}"
```

**If no results:** Try broader keywords or individual terms:
```
project = {PROJECT} AND issuetype = Bug AND status != Done AND text ~ "{keyword1}" AND text ~ "{keyword2}"
```

### 3. Duplicate Assessment

| Signal | Likely Duplicate | Action |
|--------|:----------------:|--------|
| Same summary and same component | Yes | Skip or comment on existing |
| Similar error message, same area | Probably | Present to user for decision |
| Same feature area, different error | No | Create new bug |
| Different feature area entirely | No | Create new bug |

---

## Bug Ticket Quality

### Title Format

**Pattern:** `[Test Failure] {Descriptive test case title}`

**Good Examples:**
- `[Test Failure] Verify login with invalid credentials shows error message`
- `[Test Failure] Dashboard experiment card displays correct status`

**Bad Examples:**
- `Bug found` (too vague)
- `Test failed` (not descriptive)
- `TC-002 failed` (ID only, no context)

### Description Structure

**Always use this structure:**

```
h3. Summary
Test case "{TEST_CASE_TITLE}" failed during automated execution.

h3. Steps to Reproduce
1. {Step 1 from test case}
2. {Step 2 from test case}
3. {Step 3 — FAILED HERE}

h3. Expected Result
{Expected result from test case for the failed step}

h3. Actual Result
{Actual result observed during execution}

h3. Environment
- Target URL: {TARGET_URL}
- Execution Date: {DATE}
- Browser: Chromium (Playwright)

h3. Additional Context
- Source Test Case: {JIRA_KEY or "Manual input"}
- Failed at Step: {STEP_NUMBER}/{TOTAL_STEPS}
```

### Priority Mapping

| Test Case Priority | Bug Priority | Rationale |
|-------------------|:------------:|-----------|
| High | High | Core functionality broken |
| Normal | Normal | Important but not blocking |
| Low | Low | Edge case or minor issue |

---

## Linking Rules

### Link Type

Use `"relates to"` link type between the new bug and the original test case ticket.

### Comment Identification

Always add an identification comment after creating each bug:
```
Bug is created by CLAUDE CODE via /exp-qa-agents:create-bug-ticket skill.
```

---

## Anti-Patterns

### Creating Without Searching
**Problem**: Duplicate bugs clutter the backlog
**Solution**: Always search before creating, even if you think it's new

### Vague Bug Descriptions
**Problem**: Developer can't reproduce
**Solution**: Include exact steps, expected vs actual, environment details

### Wrong Priority
**Problem**: Everything marked as High, or critical bugs marked Low
**Solution**: Map from the test case priority; adjust based on impact

### Missing Link to Test Case
**Problem**: No traceability between test case and bug
**Solution**: Always link the bug to the source test case ticket

---

## Quality Checklist

Before creating each bug ticket:

- [ ] Searched for existing related bugs in the project
- [ ] Title is descriptive and prefixed with `[Test Failure]`
- [ ] Description includes all required sections (Summary, Steps, Expected, Actual, Environment)
- [ ] Steps to reproduce clearly mark the failing step
- [ ] Priority is mapped from the test case priority
- [ ] Bug is linked to the source test case ticket
- [ ] Identification comment is added after creation

---

## References

This guidelines document should be read during bug ticket creation to ensure quality and consistency. SKILL.md references these patterns when creating JIRA tickets.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| Atlassian MCP not available | Exit with error: "Atlassian MCP is not configured. See .mcp.json.template for detailed configuration." |
| Bug creation fails | Log error, continue with remaining |
| No failures provided | Ask user for details |


## Self-Correction

1. **"Change priority to Critical"** → Update before creation
2. **"Don't create for TC-003"** → Remove from creation list
3. **"Create in a different project"** → Ask for correct project key
