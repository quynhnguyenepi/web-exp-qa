# Deploy Preproduction Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## GitHub Actions UI Navigation

### Key URLs

| Page | URL Pattern |
|------|------------|
| Workflow list | `https://github.com/{owner}/{repo}/actions/workflows/{workflow-file}` |
| Specific run | `https://github.com/{owner}/{repo}/actions/runs/{run-id}` |

### UI Elements to Find

These are the key elements the skill interacts with via Playwright snapshots:

1. **"Run workflow" dropdown** -- Usually a button on the right side of the workflow page
2. **Branch selector** -- Dropdown inside the "Run workflow" popover
3. **Green "Run workflow" button** -- Submit button inside the popover
4. **"Review deployments" button** -- Appears on the run page when waiting for approval
5. **Environment checkbox** -- Inside the approval dialog (e.g., "preproduction")
6. **Comment textarea** -- Inside the approval dialog
7. **"Approve and deploy" button** -- Green button inside the approval dialog

### Handling UI Changes

GitHub occasionally updates their Actions UI. If an element can't be found:
1. Take a screenshot to see the current state
2. Take a verbose snapshot: `browser_snapshot({ verbose: true })`
3. Look for similar elements by text content
4. If the UI has fundamentally changed, report to user and suggest manual action

---

## Timing and Polling

### Wait Durations

| Phase | Typical Duration | Max Wait |
|-------|-----------------|----------|
| Workflow queued to running | 5-30 seconds | 2 minutes |
| Running to approval gate | 2-10 minutes | 5 minutes |
| Approval to deployment start | 5-15 seconds | 1 minute |
| Deployment running | 2-15 minutes | 10 minutes |

### Polling Strategy

- Use `browser_wait_for` with appropriate timeout instead of manual polling loops
- If `wait_for` times out, take a snapshot to check current state
- Never poll more than once per 15 seconds (avoid rate limiting)

---

## Authentication Handling

### If Not Logged Into GitHub

The Playwright browser session may not be logged into GitHub. Signs:
- Page shows "Sign in" button
- Redirected to `github.com/login`
- "Run workflow" button is not visible (permissions issue)

**Action:** Ask the user to log in manually:
```
GitHub login required.

Please log into GitHub in the Playwright browser:
1. I'll navigate to github.com/login
2. Enter your credentials
3. Tell me when you're done

After login, I'll retry the deployment.
```

---

## Anti-Patterns

### Clicking Without Snapshot
**Problem:** Guessing element selectors without taking a snapshot first
**Solution:** Always take a snapshot, find the element ref, then click

### Not Waiting for Page Load
**Problem:** Clicking immediately after navigation before page renders
**Solution:** Use `wait_for` with expected text before interacting

### Hardcoding Element Refs
**Problem:** Using refs from a previous session
**Solution:** Always take a fresh snapshot for each interaction

### Polling Too Aggressively
**Problem:** Checking every 5 seconds, burning through rate limits
**Solution:** Use `wait_for` with generous timeouts (30s+)

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| Playwright MCP not available | Exit with error: "Playwright MCP is not configured. See .mcp.json.template for detailed configuration." |
| GitHub login required | Ask user to log in via browser |
| Workflow fails before approval | Report with run URL, exit |
| Deployment times out | Report with run URL |


## Self-Correction

1. **"Use a different branch"** → Re-trigger with specified branch
2. **"Skip the approval"** → Just monitor, don't approve
3. **"Cancel the deployment"** → Navigate to run and cancel
