# Test Cases: search-jira-duplicates

## TC-01: Find exact duplicate
- Input: Keywords matching an existing open bug
- Expected: High-relevance match returned

## TC-02: No duplicates found
- Input: Unique keywords with no matches
- Expected: Empty results with "Safe to create" message

## TC-03: Multiple relevance levels
- Input: Keywords that match some tickets partially
- Expected: Results ranked by High/Medium/Low relevance

## TC-04: Atlassian MCP not available
- Input: Any keywords
- Expected: Standard error message with .mcp.json.template reference
