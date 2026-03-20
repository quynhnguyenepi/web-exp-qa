# Deploy Fresh Branch - Guidelines

## Quality Guidelines

### Pre-Deployment Checks

- Always confirm the branch name with the user before triggering a Docker build
- Verify the repository URL matches the intended target
- Never skip the user confirmation gate after extracting the Docker tag
- Always capture screenshots at key milestones (build complete, deploy complete)

### Best Practices

- Default to deploying to both inte and prep unless the user specifies otherwise
- Always use the approval comment format: `Fresh branch deploy from {branch_name} via Claude Code /exp-qa-agents:deploy-fresh-branch skill`
- Present the Docker tag explicitly so the user can verify it matches expectations
- Include GitHub Actions run URLs in the final report for traceability
- If the user provides a PR URL, extract the branch name from it rather than asking again

### Timeout Management

- Docker build timeout: 15 minutes -- if exceeded, report with run URL
- Deploy workflow appearance: 30 seconds
- Approval gate appearance: 5 minutes
- Deployment completion: 10 minutes
- Always report the run URL when a timeout occurs so the user can check manually

### Anti-Patterns

- Do NOT proceed past a gate without explicit user approval
- Do NOT trigger the deploy workflow with the wrong branch (keep workflow branch as `master`, only the Docker tag changes)
- Do NOT attempt to parallelize steps -- this is a strictly sequential browser workflow
- Do NOT retry a failed Docker build automatically -- report and let the user decide
- Do NOT assume the user wants to deploy to both environments without confirming

### Error Recovery

- If GitHub requires login, ask the user to complete authentication in the browser
- If the Docker tag cannot be found in build output, ask the user to locate and paste it manually
- If a deploy fails, provide the run URL and suggest checking the workflow logs
- Always offer follow-up skills after deployment: execute-test-case, execute-test-suite, verify-bug-simple

### Security

- Never store or log credentials
- Use the browser session the user has already authenticated
- Do not modify repository settings or workflow files

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

```
TodoWrite([
  { content: "Pre-flight and input collection", status: "in_progress", activeForm: "Collecting deployment info" },
  { content: "Step 1: Get branch name", status: "pending", activeForm: "Extracting branch name" },
  { content: "Step 2: Trigger Docker Build", status: "pending", activeForm: "Triggering Docker build" },
  { content: "Step 3: Wait for build and extract tag", status: "pending", activeForm: "Waiting for Docker build" },
  { content: "Gate: Review Docker tag", status: "pending", activeForm: "Waiting for user review" },
  { content: "Step 4: Trigger Deploy workflow", status: "pending", activeForm: "Triggering deploy" },
  { content: "Step 5: Wait and approve deployment", status: "pending", activeForm: "Waiting for approval gate" },
  { content: "Gate: Review deployment result", status: "pending", activeForm: "Waiting for user review" },
  { content: "Present deployment summary", status: "pending", activeForm: "Presenting summary" }
])
```


## Error Handling

| Error | Action |
|-------|--------|
| Playwright MCP not available | Exit with error: "Playwright MCP is not configured. See .mcp.json.template for detailed configuration." |
| GitHub login required | Ask user to log in via browser |
| Branch not found | Ask user to verify branch name |
| Docker build fails | Report with run URL, ask user to check build logs |
| Docker tag not found in output | Ask user to manually find and paste the tag |
| Deploy workflow fails before approval | Report with run URL, exit |
| Deployment times out | Report with run URL |


## Self-Correction

1. **"Use a different branch"** -> Re-start from Step 2 with new branch
2. **"Use this tag instead"** -> Skip to Step 4 with user-provided Docker tag
3. **"Deploy to inte only"** -> Adjust environment selection in Step 5
4. **"Cancel the deployment"** -> Navigate to run and cancel
5. **"Skip Docker build, I already have the tag"** -> Skip to Step 4, ask for tag
