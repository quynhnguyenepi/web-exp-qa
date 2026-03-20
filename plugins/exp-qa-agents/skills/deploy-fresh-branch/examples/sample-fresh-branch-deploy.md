# Sample: Deploy Fresh Branch

## User Request

> Deploy from PR #1234 to inte and prep

## Execution

### Pre-flight

```
Playwright MCP: Connected
Repository: episerver/optly-cms (from git remote)
```

**User prompt:** "What branch should I deploy?"
**User response:** "PR https://github.com/episerver/optly-cms/pull/1234"

### Step 1: Get Branch Name

- Navigated to PR #1234
- Extracted branch name: `thamoui/APPX-11416`
- Confirmed with user: "Branch: `thamoui/APPX-11416`. Proceed?"
- User approved

### Step 2: Trigger Docker Build

- Navigated to GitHub Actions > "Docker Build and Publish"
- Clicked "Run workflow"
- Entered branch: `thamoui/APPX-11416`
- Submitted workflow
- Workflow run appeared within 10 seconds

### Step 3: Wait for Docker Build

- Waited 8 minutes for build to complete
- Build status: Success
- Docker tag extracted: `sha-e361034`
- Screenshot captured

**Gate:** "Docker build complete. Tag: `sha-e361034`. Proceed to deploy?"
**User:** "Yes"

### Step 4: Trigger Deploy Workflow

- Navigated to GitHub Actions > "Deploy Inte Prep"
- Clicked "Run workflow"
- Workflow branch: `master`
- Image tag: `sha-e361034`
- Submitted workflow

### Step 5: Wait and Approve Deployment

- Approval gate appeared after 2 minutes
- Clicked "Review deployments"
- Selected environments: inte, prep
- Approval comment: "Fresh branch deploy from thamoui/APPX-11416 via Claude Code /exp-qa-agents:deploy-fresh-branch skill"
- Clicked "Approve and deploy"
- Deployment completed in 6 minutes
- Final status: Success
- Screenshot captured

## Deployment Summary

| Field | Value |
|-------|-------|
| Branch | `thamoui/APPX-11416` |
| Docker tag | `sha-e361034` |
| Environment | inte, prep |
| Status | Success |
| Build URL | https://github.com/episerver/optly-cms/actions/runs/12345 |
| Deploy URL | https://github.com/episerver/optly-cms/actions/runs/12346 |

## Suggested Next Steps

- `/exp-qa-agents:execute-test-case` for testing on the deployed environment
- `/exp-qa-agents:execute-test-suite` for running a full test suite
- `/common-qa:verify-bug-simple` for bug fix verification
