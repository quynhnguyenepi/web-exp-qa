# Test Cases: read-repo-docs

## TC-01: Fetch CLAUDE.md from root
- Input: Repo with CLAUDE.md at root
- Expected: CLAUDE.md content returned

## TC-02: No CLAUDE.md found
- Input: Repo without CLAUDE.md
- Expected: Warning logged, continues with other doc files

## TC-03: Fetch specific files
- Input: Repo + specific_files list
- Expected: Only specified files fetched

## TC-04: GitHub access not configured
- Input: No GitHub MCP or gh CLI
- Expected: Standard error with .mcp.json.template reference
