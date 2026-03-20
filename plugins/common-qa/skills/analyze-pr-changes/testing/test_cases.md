# Test Cases: analyze-pr-changes

## TC-001: Ticket with Linked PRs
- **Input:** Ticket ID with 2 merged PRs
- **Expected:** Both PRs fetched, diffs classified, scope assessed

## TC-002: Ticket with No PRs
- **Input:** Ticket ID with no linked PRs (JIRA or git log)
- **Expected:** "PRs Found (0)" with warning

## TC-003: Large Diff PR
- **Input:** PR with 50+ changed files
- **Expected:** Files classified, scope marked as "Broad"

## TC-004: PR with Follow-up Fixes
- **Input:** Ticket with main PR + follow-up fix PR
- **Expected:** Both listed, follow-up noted separately

## TC-005: GitHub MCP Unavailable
- **Input:** Valid ticket but GitHub MCP not connected
- **Expected:** Warning, falls back to git log only
