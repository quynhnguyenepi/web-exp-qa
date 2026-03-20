# Sample: Deploy to Preproduction

## User Request

"Deploy flags to preproduction"

---

## Step 0: Pre-Flight Checks

```
TodoWrite([
  { content: "Run pre-flight checks", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Trigger deployment workflow", status: "pending", activeForm: "Triggering deployment workflow" },
  { content: "Wait for approval gate", status: "pending", activeForm: "Waiting for approval gate" },
  { content: "Approve deployment", status: "pending", activeForm: "Approving deployment" },
  { content: "Monitor deployment", status: "pending", activeForm: "Monitoring deployment" }
])
```

```
Pre-flight checks passed
   - Playwright MCP: Connected
   - Repository: optimizely/flags
   - Workflow: deploy-inte-prep.yaml
   - Branch: master
   - Environment: preproduction

Proceeding to trigger workflow...
```

---

## Step 1: Trigger Workflow

Navigating to: `https://github.com/optimizely/flags/actions/workflows/deploy-inte-prep.yaml`

Taking snapshot... Found "Run workflow" button.

Clicking "Run workflow" dropdown... Branch: master (default).

Clicking green "Run workflow" submit button...

```
Workflow triggered successfully
   - Run URL: https://github.com/optimizely/flags/actions/runs/12345678

Waiting for approval gate...
```

---

## Step 2: Wait for Approval Gate

Navigating to run page... Waiting for "Review deployments" to appear...

(~3 minutes later)

```
Workflow reached approval gate
   - Status: Waiting for review
   - Environment: preproduction

Proceeding to approve...
```

---

## Step 3: Approve Deployment

Clicking "Review deployments"... Approval dialog appeared.

Ticking "preproduction" checkbox...

Typing comment: "Approved via Claude Code /exp-qa-agents:deploy-preproduction skill"

Clicking "Approve and deploy"...

```
Deployment approved
   - Environment: preproduction
   - Comment: "Approved via Claude Code"

Monitoring deployment...
```

---

## Step 4: Monitor Until Complete

Waiting for deployment to finish...

(~5 minutes later)

Taking final screenshot...

```
Deployment to preproduction completed successfully!

Repository: optimizely/flags
Branch: master
Environment: preproduction
Workflow: deploy-inte-prep.yaml
Run URL: https://github.com/optimizely/flags/actions/runs/12345678

The preproduction environment is now updated.
```
