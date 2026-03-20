# Example: Search JIRA Duplicates Output

## Input
- Keywords: `["visual editor", "font size", "not saving"]`
- Project: `CJS`
- Issue type: `Bug`

## Output

### Duplicate Search Results (3 found)

| # | Key | Summary | Status | Relevance | Updated |
|---|-----|---------|--------|-----------|---------|
| 1 | CJS-10234 | Visual Editor font size changes lost on save | Open | High | 2026-02-15 |
| 2 | CJS-9876 | VE typography changes not persisting | In Progress | Medium | 2026-01-20 |
| 3 | CJS-8901 | Editor font settings reset after page reload | Done | Low | 2025-11-10 |

### Recommendation
- **1 high-relevance match** -- review before creating a new ticket
- **1 medium-relevance match** -- may be related
- **1 low-relevance match** -- likely different issue
