# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Validate input and detect Confluence URLs", status: "in_progress", activeForm: "Detecting Confluence URLs" },
  { content: "Fetch Confluence pages via Atlassian MCP", status: "pending", activeForm: "Fetching Confluence pages" },
  { content: "Extract relevant context", status: "pending", activeForm: "Extracting context" },
  { content: "Return structured output", status: "pending", activeForm: "Returning output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| No Confluence URLs found | Return empty output, not an error |
| Atlassian MCP not configured | Error: Atlassian MCP is not configured. See .mcp.json.template for detailed configuration. |
| Page not found by search | Log warning with URL, try broader search terms |
| confluence_get_page fails | Log warning with page ID/URL, continue with remaining pages |
| Too many URLs (>5) | Process first 5, note remaining count |

---


## Self-Correction

1. **"Also check this URL"** -> Add URL to the list, fetch and extract
2. **"The page content is wrong"** -> Re-fetch with `convert_to_markdown: false` for raw HTML
3. **"Skip page X"** -> Remove from results

---


## Notes

### URL Detection Patterns

| Pattern | Example |
|---------|---------|
| Atlassian Cloud full URL | `https://org.atlassian.net/wiki/spaces/SPACE/pages/ID/Title` |
| Atlassian Cloud short URL | `https://org.atlassian.net/wiki/x/ShortCode` |
| Legacy on-prem URL | `https://confluence.sso.episerver.net/display/SPACE/Page+Title` |
| Embedded in markdown | `[Page Title](https://org.atlassian.net/wiki/...)` |

### Why Atlassian MCP Instead of WebFetch

Confluence pages require authentication. WebFetch will get redirected to the Atlassian login page and cannot access page content. The Atlassian MCP server has credentials configured in `.mcp.json` and can access all Confluence pages the user has permission to view.
