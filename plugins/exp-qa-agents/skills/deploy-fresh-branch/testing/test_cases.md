# Deploy Fresh Branch - Test Cases

## TC-001: Deploy from PR URL to both environments

**Preconditions:** Playwright MCP is connected. User is logged into GitHub in the browser. A valid PR exists with a buildable branch.

**Steps:**
1. Invoke skill with a PR URL (e.g., `https://github.com/episerver/optly-cms/pull/1234`)
2. Skill extracts the branch name from the PR page
3. Skill triggers Docker Build workflow with the extracted branch
4. Wait for Docker build to complete and extract the Docker tag
5. Confirm Docker tag with user at the gate
6. Trigger Deploy Inte Prep workflow with the Docker tag
7. Approve deployment to both inte and prep
8. Wait for deployment to complete

**Expected Results:**
- Branch name is correctly extracted from PR
- Docker build completes successfully
- Docker tag is in `sha-{hash}` format
- User is prompted at each gate before proceeding
- Deployment completes successfully to both environments
- Final summary includes branch, tag, environments, status, and run URLs

## TC-002: Deploy with user-provided branch name (no PR URL)

**Preconditions:** Playwright MCP is connected. User is logged into GitHub.

**Steps:**
1. Invoke skill without a PR URL
2. Skill asks for the branch name
3. User provides branch name directly (e.g., `feature/my-branch`)
4. Skill skips PR extraction and triggers Docker Build directly
5. Continue through remaining workflow steps

**Expected Results:**
- Skill accepts direct branch name input
- Step 1 (Get branch name from PR) is skipped
- Docker build is triggered with the provided branch name
- Workflow continues normally from Step 2

## TC-003: Docker build failure

**Preconditions:** Playwright MCP is connected. User provides a branch with a known build issue.

**Steps:**
1. Invoke skill with a branch that will fail to build
2. Wait for Docker build to complete
3. Build fails

**Expected Results:**
- Skill detects the build failure
- Reports the error with the GitHub Actions run URL
- Does NOT proceed to deploy
- Suggests user check the build logs

## TC-004: User skips Docker build with existing tag

**Preconditions:** Playwright MCP is connected. User already has a Docker tag from a previous build.

**Steps:**
1. Invoke skill
2. User says "Skip Docker build, I already have the tag"
3. User provides the tag: `sha-abc1234`
4. Skill skips to Step 4 (Trigger Deploy workflow)

**Expected Results:**
- Skill accepts the self-correction command
- Skips Steps 2-3 entirely
- Proceeds to deploy with the user-provided Docker tag
- Final summary reflects the provided tag

## TC-005: Deploy to single environment

**Preconditions:** Playwright MCP is connected. User wants to deploy to inte only.

**Steps:**
1. Invoke skill
2. User specifies target environment as "inte only"
3. Complete Docker build and tag extraction
4. At deploy approval, only select inte environment

**Expected Results:**
- Only inte is selected during approval
- Deployment completes for inte only
- Final summary shows environment as "inte"
