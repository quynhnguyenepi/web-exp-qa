# QA Pipeline - Guidelines

## Quality Guidelines

### Pipeline Mode Selection

- Always ask the user which mode to use if not specified (Mode A, B, or C)
- Mode A (Manual): Best for exploratory QA where human judgment is needed at execution
- Mode B (Automated): Best for creating automated test scripts from tickets
- Mode C (Full): Best for comprehensive QA combining both manual execution and automation
- Clearly explain the differences when the user is unsure

### Gate Management

- Every gate requires explicit user approval before proceeding
- Present concise but complete summaries at each gate
- Offer clear action options: approve, re-run, edit, abort
- Never proceed past a gate without user response
- If the user aborts at any gate, present a partial summary of completed stages

### Best Practices

- Pass context between stages -- each stage should receive the output of the previous stage
- When invoking sub-skills via Agent tool, include the full SKILL.md content
- Track pipeline progress in TodoWrite so the user always knows the current stage
- For Mode C, maximize parallelism by running manual execution and script generation simultaneously
- Always extract the ticket ID from user input using regex `([A-Z]+-\d+)`
- Check MCP connectivity for all required servers at pre-flight, not mid-pipeline

### Anti-Patterns

- Do NOT skip the pre-flight MCP connectivity check
- Do NOT proceed to execution without test cases being reviewed (Mode A/C)
- Do NOT file bug tickets for test cases that passed
- Do NOT create a PR without user reviewing the generated scripts first
- Do NOT run the full pipeline without any gates -- user control is essential
- Do NOT re-analyze the ticket in every stage -- pass the analysis context forward

### Stage Failure Recovery

- If a stage fails, offer to retry that specific stage, not the entire pipeline
- Preserve all successful stage outputs when retrying a failed stage
- Allow the user to skip a failed stage and continue with remaining stages
- Always report which stage failed and why in the error output

### Performance

- Minimize redundant API calls by passing context between stages
- In Mode C, launch execute-test-case/suite and generate-test-scripts in parallel
- Do not re-fetch JIRA ticket data that was already gathered in the analysis stage

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

```
TodoWrite([
  { content: "Pre-flight and mode selection", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Stage 1: Analyze ticket", status: "pending", activeForm: "Analyzing ticket" },
  { content: "Gate: Review analysis", status: "pending", activeForm: "Waiting for user review" },
  { content: "Stage 2: Generate test cases", status: "pending", activeForm: "Generating test cases" },
  { content: "Gate: Review generated test cases", status: "pending", activeForm: "Waiting for user review" },
  { content: "Stage 3: Review test cases (Mode A/C)", status: "pending", activeForm: "Reviewing test cases" },
  { content: "Gate: Review TC assessment", status: "pending", activeForm: "Waiting for user review" },
  { content: "Stage 4: Execute tests", status: "pending", activeForm: "Executing tests" },
  { content: "Gate: Review execution results", status: "pending", activeForm: "Waiting for user review" },
  { content: "Stage 5: File bugs (Mode A/C)", status: "pending", activeForm: "Filing bugs" },
  { content: "Gate: Review bug tickets", status: "pending", activeForm: "Waiting for user review" },
  { content: "Stage 6: Review PR (Mode B/C)", status: "pending", activeForm: "Reviewing PR" },
  { content: "Gate: Review PR assessment", status: "pending", activeForm: "Waiting for user review" },
  { content: "Present pipeline summary", status: "pending", activeForm: "Presenting pipeline summary" }
])
```


## Error Handling

| Error | Action |
|-------|--------|
| Any stage fails | Apply `on_failure` action from table above, save checkpoint |
| User rejects at gate | Allow modifications or abort pipeline, save checkpoint |
| MCP server unavailable mid-pipeline | Warn, skip dependent stages, report partial results with checkpoints |
| Timeout on browser execution | Capture partial results, save checkpoint, offer to continue remaining cases |


## Self-Correction

1. **"Skip test case generation"** -> Jump directly from analysis to execution with ad-hoc test cases
2. **"Re-run only failed tests"** -> Re-invoke execute-test-case with failed subset
3. **"Switch to automated mode"** -> Pivot from Mode A to Mode B mid-pipeline
4. **"Add another ticket"** -> Restart pipeline for new ticket, keep previous results
