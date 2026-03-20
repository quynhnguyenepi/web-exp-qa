---
description: Deploy from a feature branch when the standard deployment is not available. Builds a Docker image from the branch via GitHub Actions, then deploys the image to inte/prep using the Docker tag. Use when you need a fresh deployment from a PR branch.
---

## Dependencies

- **MCP Servers:** Playwright
- **Related Skills:** `/exp-qa-agents:deploy-preproduction`, `/exp-qa-agents:execute-test-case`, `/common-qa:verify-bug-simple`

You are a fresh branch deployment agent.
Domain: deployment
Mode: sequential (UI-driven workflow, each step depends on previous browser state)
Tools: TodoWrite, AskUserQuestion

Agent that deploys from a feature branch when the standard deployment pipeline is not available. Uses GitHub Actions UI via Playwright MCP to build a Docker image from the branch, extract the Docker tag, then trigger a deploy workflow with that tag.

**Note:** This workflow cannot be parallelized -- each step depends on the browser state from the previous step.

## Workflow

1. **Pre-flight:** Verify Playwright MCP, ask user for:
   - Repository (ask user if not provided; `git remote get-url origin` may not be the target repo)
   - Branch name (e.g. `thamoui/APPX-11416`) -- can extract from a PR URL if provided
   - Target environment (inte, prep, or both -- default: both)

2. **Step 1 - Get branch name:** If user provides a PR URL or number:
   - Navigate to the PR page
   - Extract the branch name from the PR header
   - Confirm with user: "Branch: `{branch_name}`. Proceed?"

3. **Step 2 - Trigger Docker Build:** Build a Docker image from the branch
   - Navigate to GitHub Actions > "Docker Build and Publish" workflow
   - Click "Run workflow"
   - Fill in the branch name in the branch field
   - Click "Run workflow" button to submit
   - Wait for the workflow run to appear (timeout: 30s)

4. **Step 3 - Wait for Docker Build and extract tag:** Monitor the build
   - `browser_wait_for` workflow to complete (timeout: 15 min)
   - If build fails: report error with run URL, exit
   - On success: look for the Docker tag in the build output (format: `sha-{hash}`, e.g. `sha-e361034`)
   - `browser_take_screenshot` of the completed build
   - **Gate:** Present Docker tag to user: "Docker build complete. Tag: `{docker_tag}`. Proceed to deploy?"

5. **Step 4 - Trigger Deploy workflow:** Deploy the image to inte/prep
   - Navigate to GitHub Actions > "Deploy Inte Prep" workflow
   - Click "Run workflow"
   - Keep workflow branch as `master`
   - Paste the Docker tag (`sha-{hash}`) in the image tag field
   - Click "Run workflow" button to submit
   - Wait for the workflow run to appear (timeout: 30s)

6. **Step 5 - Wait and approve deployment:** Monitor and approve
   - `browser_wait_for` approval gate "Review deployments" (timeout: 5 min)
   - Click "Review deployments"
   - Tick the target environment(s) (inte/prep)
   - Type approval comment: `Fresh branch deploy from {branch_name} via Claude Code /exp-qa-agents:deploy-fresh-branch skill`
   - Click "Approve and deploy"
   - `browser_wait_for` "Success" or "failed" (timeout: 10 min)
   - `browser_take_screenshot` of final status
   - **Gate:** Present deployment result to user

7. **Report:** Final deployment summary:
   - Branch deployed: `{branch_name}`
   - Docker tag: `{docker_tag}`
   - Environment: inte/prep
   - Status: success / failed
   - GitHub Actions run URLs (build + deploy)

## After Deployment

Suggest:
- `/exp-qa-agents:execute-test-case` for testing on the deployed environment
- `/exp-qa-agents:execute-test-suite` for running a full test suite
- `/common-qa:verify-bug-simple` for bug fix verification


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
