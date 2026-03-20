# Skill Evaluation Guidelines

Reference for evaluating skills against their test cases.

## Test Case Parsing

### Expected Format in test_cases.md

Test cases are organized by category with markdown tables:

```markdown
### 1. Category Name
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Test name | Input description | Expected behavior |
```

### Parsing Rules

1. Categories are identified by `### N. Category Name` headings
2. Each table row after the header is one test case
3. The `Input` column describes setup conditions and inputs
4. The `Expected Outcome` column describes what should happen

## Simulation Mode

In simulation mode, the agent:

1. Reads the skill's SKILL.md workflow
2. For each test case, traces through the workflow logic with the given input
3. Determines if the skill's defined behavior matches the expected outcome
4. Does NOT call any MCP servers or external tools

### What Simulation Can Validate

- Workflow step ordering and logic
- Error handling paths (given error X, does the skill define action Y?)
- Pre-flight check completeness
- Input parsing and validation
- Output format compliance
- Dependency declarations

### What Simulation Cannot Validate

- Actual MCP server responses
- Browser automation behavior
- Network-dependent operations
- Timing and performance
- Concurrent execution behavior

## Live Mode

In live mode, the agent actually invokes the skill. This requires:

- All MCP servers configured and accessible
- Valid test data (JIRA tickets, GitHub repos, etc.)
- User must explicitly opt-in with `--live` flag

### Safety Rules

1. Never create or modify JIRA tickets in live mode without user confirmation
2. Never push code or create PRs in live mode without user confirmation
3. Prefer read-only operations for live validation
4. Use test/sandbox environments when available

## Evaluation Result Schema

```json
{
  "skill": "string - skill name",
  "version": "string - semver",
  "last_evaluated": "string - ISO 8601",
  "mode": "simulation | live",
  "summary": {
    "total": "number",
    "passed": "number",
    "failed": "number",
    "errors": "number",
    "pass_rate": "string - percentage"
  },
  "evaluations": [
    {
      "test_id": "string",
      "test_name": "string",
      "category": "string",
      "status": "pass | fail | error",
      "expected": "string",
      "actual": "string",
      "error": "string | null",
      "mode": "simulation | live",
      "timestamp": "string - ISO 8601"
    }
  ]
}
```

## Pass/Fail Criteria

### Pass
- Skill's defined workflow handles the input correctly
- Output matches expected outcome (semantic match, not exact string)
- Error handling covers the scenario described

### Fail
- Skill's workflow would produce incorrect output for the input
- Expected error handling path is missing
- Required step is skipped or misordered

### Error
- Test case cannot be evaluated (e.g., references MCP in simulation mode)
- Skill definition is ambiguous for the given scenario
- Test case itself is malformed

## Quality Checklist

Before presenting evaluation results:

- [ ] All test cases in scope were executed
- [ ] Results are deterministic (re-running produces same output)
- [ ] Failed tests have clear explanations
- [ ] Errors are distinguished from failures
- [ ] evaluations.json is valid JSON
- [ ] Summary counts match individual results

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (discover skills, parse test cases)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Execute test cases (parallel per category)", status: "pending", activeForm: "Executing test cases" },
  { content: "Record results to evaluations.json", status: "pending", activeForm: "Recording results" },
  { content: "Present evaluation report", status: "pending", activeForm: "Presenting report" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| test_cases.md missing or empty | **skip_continue**: Report error for that skill, continue with others |
| SKILL.md unreadable | **skip_continue**: Cannot evaluate without skill definition |
| Agent execution fails | **retry**: Re-dispatch agent once, then record as `error` |
| Live mode MCP unavailable | **ask_user**: Suggest switching to simulation mode |
| All test cases fail | Report all failures, suggest checking skill definition |

---


## Self-Correction

1. **"Run only failed tests"** -> Re-execute only test cases with `fail` or `error` status
2. **"Switch to live mode"** -> Re-run with actual MCP calls (requires configured servers)
3. **"Evaluate another skill"** -> Add skill to scope, run evaluation
4. **"Update test cases and re-run"** -> Read updated test_cases.md, re-execute

---


## Notes

### Key Principles

1. **Isolation**: Each test case runs in a separate agent to prevent state leakage
2. **Deterministic**: Simulation mode produces consistent results without external dependencies
3. **Non-destructive**: Simulation mode never calls MCP servers or modifies external state
4. **Incremental**: Can evaluate one skill at a time or batch multiple skills
5. **TDD-friendly**: Run evaluations before skill exists (expect all fail), then after (expect all pass)

### TDD Workflow

```
1. Write test_cases.md for new skill (define expected behavior)
2. Run /common-qa:evaluate-skills {skill-name} (expect all FAIL -- RED)
3. Create SKILL.md with workflow implementation
4. Run /common-qa:evaluate-skills {skill-name} (expect all PASS -- GREEN)
5. Refactor SKILL.md if needed
6. Run /common-qa:evaluate-skills {skill-name} (confirm still PASS -- REFACTOR)
```

### Input Flexibility

| Input Type | Example |
|------------|---------|
| Single skill | `/common-qa:evaluate-skills analyze-ticket` |
| Multiple skills | `/common-qa:evaluate-skills analyze-ticket, create-pr` |
| Full plugin | `/common-qa:evaluate-skills --plugin exp-qa-agents` |
| With mode | `/common-qa:evaluate-skills analyze-ticket --live` |
| Failed only | `/common-qa:evaluate-skills analyze-ticket --failed-only` |
