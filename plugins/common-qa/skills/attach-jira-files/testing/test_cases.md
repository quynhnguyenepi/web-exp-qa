# Test Cases: attach-jira-files

## TC-01: Upload single file
- Input: One screenshot path + valid issue key
- Expected: File uploaded successfully, results table shown

## TC-02: Upload multiple files
- Input: 3 file paths + valid issue key
- Expected: All 3 uploaded with results table

## TC-03: File not found
- Input: Non-existent file path
- Expected: Warning logged, file skipped

## TC-04: Missing JIRA credentials (env vars)
- Input: Any file + missing env vars but valid `~/.mcp.json`
- Expected: Credentials extracted from MCP config, upload succeeds

## TC-05: Missing all credentials
- Input: Any file + no env vars + no MCP config
- Expected: Error message listing both credential sources checked

## TC-06: Partial filename search
- Input: Partial filename (e.g., `Screen Recording 2026-03-11*`) + valid issue key
- Expected: File found in Desktop/Downloads/Documents, uploaded successfully

## TC-07: Large video file upload
- Input: Video file >20MB (e.g., `.mov` screen recording) + valid issue key
- Expected: File uploaded with extended timeout, results show correct file size

## TC-08: JIRA URL as issue key
- Input: Full JIRA URL (e.g., `https://optimizely-ext.atlassian.net/browse/DHK-4454`) instead of issue key
- Expected: Issue key extracted from URL, upload proceeds normally
