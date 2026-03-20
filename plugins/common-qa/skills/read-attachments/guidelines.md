# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (verify Atlassian MCP, validate input)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "List attachments from ticket(s)", status: "pending", activeForm: "Listing attachments" },
  { content: "Download images + text files (parallel)", status: "pending", activeForm: "Processing attachments in parallel" },
  { content: "Return structured output", status: "pending", activeForm: "Returning output" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| No attachments found | Return empty summary, not an error |
| Image extraction fails | Log warning, continue with remaining |
| Base64 decode fails | Log warning, skip file |
| Attachment too large | Skip with warning |

---


## Self-Correction

1. **"Also check ticket X"** -> Add issue key to the list, re-process
2. **"Skip images, only text files"** -> Process only text category

---


## Notes

### MCP Requirements

| MCP Server | Required For | Fallback |
|------------|-------------|----------|
| Atlassian | Attachment download (REQUIRED) | No fallback |

### Supported Formats

| Format | Processing |
|--------|-----------|
| `.png`, `.jpg`, `.jpeg`, `.gif` | Visual analysis via `jira_get_issue_images` |
| `.md`, `.txt`, `.csv`, `.json`, `.yml`, `.yaml` | Base64 decode via `jira_download_attachments` |
| `.xlsx`, `.pdf`, `.zip`, `.docx` | Skipped with warning |
