# Sample Evaluation Report

## Input

```
/common-qa:evaluate-skills analyze-ticket
```

## Output

```
Evaluation Report

Skill: analyze-ticket
Mode: simulation
Date: 2026-03-07T10:30:00Z

Results: 14/16 passed (87.5%)

| Category | Total | Passed | Failed | Errors |
|----------|-------|--------|--------|--------|
| Pre-Flight | 3 | 3 | 0 | 0 |
| JIRA Analysis | 4 | 4 | 0 | 0 |
| PR Analysis | 3 | 2 | 1 | 0 |
| Synthesis | 4 | 3 | 0 | 1 |
| Output Format | 2 | 2 | 0 | 0 |

Failed Tests:
- TC-008: Expected "PR changes classified by category" but skill workflow does not define classification categories for edge cases with >20 files changed

Errors:
- TC-012: Cannot evaluate "Figma screenshots extracted" in simulation mode (requires Figma MCP)

Results saved to: plugins/exp-qa-agents/skills/analyze-ticket/testing/evaluations.json
```

## evaluations.json (excerpt)

```json
{
  "skill": "analyze-ticket",
  "version": "1.0.0",
  "last_evaluated": "2026-03-07T10:30:00Z",
  "mode": "simulation",
  "summary": {
    "total": 16,
    "passed": 14,
    "failed": 1,
    "errors": 1,
    "pass_rate": "87.5%"
  },
  "evaluations": [
    {
      "test_id": "TC-001",
      "test_name": "Valid JIRA ticket ID",
      "category": "Pre-Flight",
      "status": "pass",
      "expected": "Extracts ticket ID CJS-10873 from input",
      "actual": "Regex ([A-Z]+-\\d+) correctly matches CJS-10873",
      "error": null,
      "mode": "simulation",
      "timestamp": "2026-03-07T10:30:01Z"
    },
    {
      "test_id": "TC-008",
      "test_name": "Large PR classification",
      "category": "PR Analysis",
      "status": "fail",
      "expected": "PR changes classified by category for PRs with >20 files",
      "actual": "Skill workflow defines change categorization but does not specify handling for large PRs",
      "error": null,
      "mode": "simulation",
      "timestamp": "2026-03-07T10:30:15Z"
    }
  ]
}
```
