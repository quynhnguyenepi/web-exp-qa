# Multi-Agents - Guidelines

## Quality Guidelines

### Task Planning

- Always parse ALL tasks from user input before dispatching any agents
- Present the task plan to the user for confirmation before execution
- Assign clear task IDs (T1, T2, T3) for tracking and reference
- Identify dependencies between tasks -- never run dependent tasks in parallel

### Parallel Execution Rules

- Only parallelize tasks that are truly independent (no shared state)
- Browser-dependent tasks (execute-test-case, execute-test-suite, deploy-*, inspect-*) must run sequentially -- only one browser session at a time
- Git-dependent tasks (create-pr) must run sequentially to avoid conflicts
- API-only tasks (analyze-ticket, create-test-cases, review-test-cases, review-github-pr) are safe to parallelize
- Limit concurrent agents to avoid context window exhaustion

### Best Practices

- Present results for review as each agent completes, do not wait for all to finish
- When mixing parallel and sequential tasks, launch parallel tasks first
- If more than 10 tasks are requested, warn the user about context limits and suggest batching
- Always include the skill SKILL.md content when dispatching agents so they execute correctly
- Track each agent's status in TodoWrite for visibility

### Anti-Patterns

- Do NOT launch browser-dependent agents in parallel -- they will conflict
- Do NOT skip the task plan confirmation step
- Do NOT dispatch agents without mapping them to a specific skill
- Do NOT silently drop tasks that fail -- always report failures in the summary
- Do NOT re-run failed agents automatically without user consent

### Result Consolidation

- Group results by agent in the final report
- Include status for every task: approved, re-run, failed, or skipped
- Highlight cross-ticket insights when multiple tickets were analyzed
- Include links to all created artifacts (bug tickets, PRs, test designs)

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

```
TodoWrite([
  { content: "Parse and plan tasks", status: "in_progress", activeForm: "Parsing tasks from input" },
  { content: "Confirm task plan with user", status: "pending", activeForm: "Confirming task plan" },
  { content: "T1: [skill] [target]", status: "pending", activeForm: "Running T1" },
  { content: "Review T1 results with user", status: "pending", activeForm: "Reviewing T1" },
  { content: "T2: [skill] [target]", status: "pending", activeForm: "Running T2" },
  { content: "Review T2 results with user", status: "pending", activeForm: "Reviewing T2" },
  { content: "T3: [skill] [target]", status: "pending", activeForm: "Running T3" },
  { content: "Review T3 results with user", status: "pending", activeForm: "Reviewing T3" },
  { content: "Present consolidated results", status: "pending", activeForm: "Presenting results" }
])
```


## Error Handling

| Error | Action |
|-------|--------|
| One task fails | **skip_continue**: Log error, continue other tasks, report failure in summary |
| All tasks fail | **ask_user**: Report all errors, suggest checking MCP connectivity |
| User cancels mid-execution | **skip_continue**: Wait for running tasks to finish, skip pending ones, save completed results |
| Too many tasks (>10) | **ask_user**: Warn user about context limits, suggest batching |


## Self-Correction

1. **"Also do X for ticket Y"** -> Add new task to active list, dispatch immediately
2. **"Cancel task T2"** -> Cannot cancel running agents, but skip reporting its results
3. **"Re-run T1"** -> Dispatch a new agent for that task
4. **"Run these sequentially instead"** -> Switch to sequential execution order
