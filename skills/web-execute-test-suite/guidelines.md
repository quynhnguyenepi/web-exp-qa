# Run Test Suite - Guidelines

**Shared reference:** For login configuration, Playwright action mapping, verification strategies, common test patterns, and error handling patterns, read `../execute-test-case/guidelines.md`. This file covers suite-specific rules only.

## Quality Guidelines

### Test Case Preparation

- Every step must have a concrete, verifiable expected outcome before execution begins
- Collect all unclear expected outcomes at once and present them to the user in a single prompt
- Do not accept vague outcomes like "it works", "page loads", or "verify" without specifics
- Validate that test cases have numbered steps, not paragraph descriptions

### Execution Rules

- Run in headless mode -- no visible browser window
- Capture screenshot AND snapshot after EVERY step, regardless of pass/fail
- On step failure: record evidence and continue to next step (do NOT stop)
- If a step failure makes subsequent steps impossible, mark remaining steps as SKIPPED
- Between test cases: navigate back to target URL and wait for page load before starting next TC
- Never ask the user mid-suite -- all clarifications happen before execution starts

### Best Practices

- Present the full suite summary to the user before execution starts
- Allow the user to select specific test cases or run all
- Display brief progress updates after each test case completes: `TC-{N}: {PASS|FAIL} ({passed}/{total} steps)`
- Reset browser state between test cases by navigating to the target URL
- Take a fresh snapshot before starting each test case to verify clean state

### Anti-Patterns

- Do NOT pause on failure and ask the user -- this is headless mode, continue automatically
- Do NOT skip screenshot capture for passed steps -- evidence is needed for all steps
- Do NOT run multiple browser sessions in parallel -- sequential execution only
- Do NOT merge results from different test cases -- each TC has its own verdict
- Do NOT report a TC as PASS if any step was SKIPPED (report as SKIPPED instead)
- Do NOT start execution without validating all expected outcomes first

### Report Standards

- Suite report must include: overall result, per-TC breakdown, pass rate, and failed steps summary
- Failed steps summary collects all failures across all TCs in one table
- Include screenshot references for every step (pass and fail)
- Offer follow-up actions: create bug tickets, re-run failed TCs, re-run specific TC in interactive mode

### Error Recovery

- If browser crashes mid-suite: restart browser and resume from the next test case
- If login is required: ask user for credentials, complete login, then resume
- If a test case has no parseable steps: log warning and skip to next TC
- If target URL is unreachable: report error and abort suite
