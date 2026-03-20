# Test Cases: read-pr-details

## TC-01: Fetch PR by URL
- Input: Full GitHub PR URL
- Expected: Metadata, files, and diff returned

## TC-02: Fetch PR by number only
- Input: PR number (resolve repo from git remote)
- Expected: Repo resolved, PR details returned

## TC-03: PR not found
- Input: Non-existent PR number
- Expected: Error asking user to verify

## TC-04: Large diff truncation
- Input: PR with >5000 lines changed
- Expected: Diff truncated with note
