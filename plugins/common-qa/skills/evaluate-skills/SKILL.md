---
description: Run test cases against skills, populate evaluations.json with results. Use when validating skill behavior, running TDD red-green cycles, or performing regression checks after skill modifications.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/common-qa:review-skills`

# Evaluating Skills

Run test cases defined in `testing/test_cases.md` against skills by dispatching sub-agents to execute each test case in isolation, then record results in `testing/evaluations.json`.

## When to Use

Invoke this skill when you need to:

- Validate a skill works correctly after creation or modification
- Run a TDD red-green cycle: write test cases first, expect failures, build skill, expect passes
- Perform regression checks across all skills after a cross-cutting change
- Populate empty `evaluations.json` files with actual test results
- Verify a specific skill's behavior against its documented test cases

## Workflow Overview

```
Pre-Flight -> Parse Test Cases -> Execute Tests (parallel per category) -> Record Results -> Present Report
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Determine target scope:**
   - If user specifies a skill name: evaluate only that skill
   - If user specifies a plugin name: evaluate all skills in that plugin
   - If no input: ask user which skill(s) to evaluate
   - Never evaluate all skills without explicit user confirmation (can be expensive)

2. **Discover test cases:**
   - For each target skill, read `plugins/{plugin}/skills/{skill-name}/testing/test_cases.md`
   - Parse test case tables: extract ID, Name, Input, Expected Outcome
   - If `test_cases.md` is empty or missing: report error for that skill, skip it

3. **Read the skill's SKILL.md** to understand its workflow, inputs, and expected behavior

### Step 1: Execute Test Cases

For each skill being evaluated:

1. **Group test cases by category** (as defined in test_cases.md headers)

2. **Dispatch one Agent per category** with `run_in_background: true` and `model: "sonnet"`:
   - Each agent receives:
     - The skill's SKILL.md content
     - The test cases for its assigned category
     - Instructions to simulate the skill's workflow for each test case
   - Each agent executes each test case:
     - Set up the input conditions described in the test case
     - Simulate or invoke the skill's workflow steps
     - Compare actual behavior against Expected Outcome
     - Record: `pass`, `fail`, or `error` with details

3. **Test execution modes:**
   - **Simulation mode (default):** Agent walks through the skill's workflow logic and validates behavior against expected outcomes without calling external MCP servers
   - **Live mode (user must opt-in):** Agent actually invokes the skill and its MCP dependencies. Use for integration testing. Requires all MCP servers to be configured.

4. **For each test case, record:**
   ```json
   {
     "test_id": "TC-001",
     "test_name": "Test case name",
     "category": "Category name",
     "status": "pass | fail | error",
     "expected": "Expected outcome from test_cases.md",
     "actual": "What actually happened",
     "error": "Error message if status is error, null otherwise",
     "mode": "simulation | live",
     "timestamp": "ISO 8601 timestamp"
   }
   ```

### Step 2: Record Results

1. **Build evaluations.json** for each skill:
   ```json
   {
     "skill": "skill-name",
     "version": "1.0.0",
     "last_evaluated": "ISO 8601 timestamp",
     "mode": "simulation | live",
     "summary": {
       "total": 10,
       "passed": 8,
       "failed": 1,
       "errors": 1,
       "pass_rate": "80%"
     },
     "evaluations": [
       {
         "test_id": "TC-001",
         "test_name": "...",
         "category": "...",
         "status": "pass",
         "expected": "...",
         "actual": "...",
         "error": null,
         "mode": "simulation",
         "timestamp": "..."
       }
     ]
   }
   ```

2. **Write to** `plugins/{plugin}/skills/{skill-name}/testing/evaluations.json`
   - Overwrite previous results (evaluations.json is regenerated each run)

### Step 3: Present Report

Present a summary report to the user:

```
Evaluation Report

Skill: {skill-name}
Mode: {simulation | live}
Date: {timestamp}

Results: {passed}/{total} passed ({pass_rate}%)

| Category | Total | Passed | Failed | Errors |
|----------|-------|--------|--------|--------|
| Pre-Flight | 3 | 3 | 0 | 0 |
| Core Workflow | 5 | 4 | 1 | 0 |
| Error Handling | 2 | 1 | 0 | 1 |

Failed Tests:
- TC-005: Expected "analysis output saved" but got "no output generated"

Errors:
- TC-010: MCP server not available (simulation mode cannot test live MCP calls)

Results saved to: plugins/{plugin}/skills/{skill-name}/testing/evaluations.json
```

If multiple skills evaluated, present a cross-skill summary table first, then per-skill details.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
