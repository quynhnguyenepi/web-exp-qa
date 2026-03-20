# Test Cases: read-confluence

## TC-001: Text with Confluence Links
- **Input:** Text containing 2 Confluence URLs
- **Expected:** Both pages fetched and summarized

## TC-002: Text with No Confluence Links
- **Input:** Text with no atlassian.net/wiki URLs
- **Expected:** "Confluence Pages (0)", no error

## TC-003: WebFetch Fails for a Page
- **Input:** Text with 1 valid and 1 invalid Confluence URL
- **Expected:** Valid page fetched, invalid logged as warning

## TC-004: Multiple Pages (Over Limit)
- **Input:** Text with 7 Confluence URLs
- **Expected:** First 5 processed, remaining 2 noted as skipped
