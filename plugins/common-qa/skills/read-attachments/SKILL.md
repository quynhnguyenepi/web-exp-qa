---
description: Download and parse JIRA ticket attachments including images and text files. Use when you need to extract visual requirements or text specifications from ticket attachments.
---

## Dependencies

- **MCP Servers:** Atlassian
- **Related Skills:** `/common-qa:read-jira-context`

# Reading JIRA Attachments

Download and parse attachments from one or more JIRA tickets. Processes images for visual context and text files for specifications. Skips unsupported formats with a warning.

## When to Use

Invoke this skill when you need to:

- Extract visual requirements from image attachments (mockups, wireframes, screenshots)
- Read text-based specifications from attached files (.md, .txt, .csv, .json, .yml)
- Process attachments from both a primary ticket and its linked tickets

## Workflow Overview

```
Pre-Flight -> List Attachments -> Download Images -> Download Text Files -> Return Output
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate input:** Accept a list of issue keys (primary + optionally linked tickets).
2. **Verify Atlassian MCP:** Attempt a test call. If not available, display standard error and exit.

### Step 1: List Attachments

For each issue key, check the ticket's attachment list. Categorize each attachment:

| Category | Extensions | Action |
|----------|-----------|--------|
| Image | `.png`, `.jpg`, `.jpeg`, `.gif` | Process in Step 2 |
| Text | `.md`, `.txt`, `.csv`, `.json`, `.yml`, `.yaml` | Process in Step 3 |
| Unsupported | `.xlsx`, `.pdf`, `.zip`, `.docx` | Log and skip |

**Limits:** Max 10 attachments from primary ticket. Max 5 total across linked tickets.

### Step 2+3: Download Images + Text Files IN PARALLEL

Call both MCP tools **directly in a single message** (no Agent tool needed — each is 1 MCP call):

**Call 1: Download Images**

```
mcp__atlassian__jira_get_issue_images({ issue_key: "{ISSUE_KEY}" })
```

For each image, extract: UI layout, component placement, expected states, visual requirements.

**Call 2: Download Text Files**

```
mcp__atlassian__jira_download_attachments({ issue_key: "{ISSUE_KEY}" })
```

Decode base64 content. Extract: requirements, specifications, test cases.

For unsupported formats, log: `Skipping attachment "{filename}" -- unsupported format`

**Key optimization:** Both calls are independent. Issue them in a single response message for parallel execution without Agent overhead.

### Step 4: Return Structured Output

---

## Output Format

```markdown
### Attachments Summary
- **Total found:** {count}
- **Images processed:** {count}
- **Text files processed:** {count}
- **Skipped (unsupported):** {count}

### Image Attachments
For each image:
- **Filename:** {name} | **Source:** {issue_key}
- **Visual context:** {extracted layout, component states, etc.}

### Text Attachments
For each text file:
- **Filename:** {name} | **Source:** {issue_key}
- **Content summary:** {extracted requirements/specs}
```

---


## Guidelines

### Supported Formats

| Category | Extensions | Processing Method |
|----------|-----------|-------------------|
| Image | `.png`, `.jpg`, `.jpeg`, `.gif` | `jira_get_issue_images` (visual analysis) |
| Text | `.md`, `.txt`, `.csv`, `.json`, `.yml`, `.yaml` | `jira_download_attachments` (base64 decode) |
| Unsupported | `.xlsx`, `.pdf`, `.zip`, `.docx` | Skip with warning message |

### Limits

- Primary ticket: max 10 attachments
- Linked tickets: max 5 attachments total across all linked tickets
- If limits exceeded, process in order of: images first, then text files

### Processing Rules

- Always log skipped files with filename and reason
- For images: extract UI layout, component states, visual requirements
- For text files: extract requirements, specifications, test cases
- Base64 decode may fail for binary files incorrectly categorized as text -- handle gracefully

---

**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
