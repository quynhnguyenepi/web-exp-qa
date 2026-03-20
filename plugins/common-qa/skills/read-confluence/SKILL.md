---
description: Find and read Confluence pages linked from JIRA tickets. Use when you need to extract specifications, requirements, or design documents from Confluence.
---

## Dependencies

- **MCP Servers:** Atlassian (`mcp-atlassian`) -- for `confluence_search` and `confluence_get_page`
- **Related Skills:** `/common-qa:read-jira-context`

# Reading Confluence Pages

Detect Confluence URLs in text content (typically from JIRA ticket description and comments), fetch each page using the Atlassian MCP Confluence tools, and extract relevant context for test analysis.

## When to Use

Invoke this skill when you need to:

- Read Confluence pages linked from a JIRA ticket
- Extract feature specifications or requirements from Confluence
- Gather technical design documents, user flows, or API contracts
- Find test strategy or test plan references from Confluence

## Workflow Overview

```
Pre-Flight -> Detect URLs / Extract Page IDs -> Fetch Pages via MCP -> Extract Context -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:** Accept either:
   - Text content (ticket description + comments) to scan for Confluence URLs
   - A direct Confluence URL provided by the user
2. **MCP server required:** Atlassian MCP (`mcp-atlassian`). Confluence pages require authentication -- the built-in `WebFetch` tool will fail with login redirects.

### Step 1: Detect Confluence URLs and Extract Page IDs

Scan the input text for URLs matching any of these patterns:

| Pattern | Example | How to Extract Page ID |
|---------|---------|----------------------|
| Atlassian Cloud (with ID in path) | `https://optimizely-ext.atlassian.net/wiki/spaces/EXPENG/pages/12345/Page+Title` | Extract `12345` from URL path |
| Atlassian Cloud (short link) | `https://org.atlassian.net/wiki/x/AbCdEf` | Cannot extract ID -- search by title instead |
| Legacy on-prem URL | `https://confluence.sso.episerver.net/display/EXPENG/Page+Title` | Cannot extract ID -- search by space + title |
| Embedded in markdown | `[Page Title](https://org.atlassian.net/wiki/...)` | Parse URL from markdown link |

**When page ID is available** (extracted from URL path): Use `confluence_get_page` directly.

**When page ID is NOT available** (legacy URLs, short links): Use `confluence_search` to find the page first:

```
confluence_search({
  query: "title~\"{page_title}\"",
  spaces_filter: "{SPACE_KEY}",
  limit: 5
})
```

Extract the space key and page title from the URL:
- Legacy URL `confluence.sso.episerver.net/display/EXPENG/Page+Title` -> space: `EXPENG`, title: `Page Title`
- For short links, search using keywords from surrounding context

If no URLs found, return empty output (not an error).

**Limits:** Max 5 pages. Prioritize URLs from the ticket description over those in comments.

### Step 2: Fetch Pages IN PARALLEL

If multiple pages found (up to 5), launch one Agent per page with `run_in_background: true`. Each agent fetches and extracts context for one page independently.

For each page, use the Atlassian MCP tool:

```
confluence_get_page({
  page_id: "{PAGE_ID}",
  include_metadata: true,
  convert_to_markdown: true
})
```

If you only have title and space (no page ID), first search then fetch:

```
confluence_search({
  query: "{search_terms}",
  spaces_filter: "{SPACE_KEY}",
  limit: 5
})
```

Then use the `id` from the search result to call `confluence_get_page`.

### Step 3: Extract Relevant Context

From each fetched page, extract:
- Feature specifications and requirements
- Technical design documents
- User flows and interaction patterns
- API contracts or data models
- Test strategy or test plan references
- TODO items or open questions
- Code samples and implementation details

---

## Output Format

```markdown
### Confluence Pages ({count})

For each page:
- **Title:** {page_title}
- **URL:** {url}
- **Space:** {space_key} ({space_name})
- **Key content:** {specifications, requirements, flows, etc.}
```

If no Confluence URLs found:
```markdown
### Confluence Pages (0)
No Confluence URLs found in ticket content.
```

---


## Guidelines

### URL Detection

Scan text for URLs containing `atlassian.net/wiki`. Common patterns:
- Full page URL: `https://org.atlassian.net/wiki/spaces/SPACE/pages/ID/Title`
- Short URL: `https://org.atlassian.net/wiki/x/ShortCode`
- Markdown links: `[Title](https://org.atlassian.net/wiki/...)`

### Content Extraction Priorities

When reading a Confluence page, extract in this order:
1. Feature specifications and requirements
2. Acceptance criteria and user stories
3. Technical design documents and architecture
4. User flows and interaction patterns
5. API contracts or data models
6. Test strategy or test plan references

### Handling Failures

- If WebFetch returns an error, log the URL and continue
- If the page requires authentication, note it for manual review
- Do not retry failed fetches more than once
- Prioritize description links over comment links when hitting the 5-page limit

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
