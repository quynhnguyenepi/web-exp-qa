# Example: Attach JIRA Files Output

## Example 1: Multiple screenshots

### Input
- Issue key: `CJS-10873`
- Files: `["/tmp/step-1.png", "/tmp/step-2.png", "/tmp/error-log.txt"]`

### Output

### Attachment Results for CJS-10873

| # | File | Status | Size |
|---|------|--------|------|
| 1 | step-1-navigate.png | Uploaded | 245KB |
| 2 | step-2-click-save.png | Uploaded | 312KB |
| 3 | error-log.txt | Uploaded | 15KB |

**Uploaded:** 3/3 files
**Ticket:** https://optimizely-ext.atlassian.net/browse/CJS-10873

---

## Example 2: Video file with MCP config credentials

### Input
- Issue key: `DHK-4454` (provided as URL: `https://optimizely-ext.atlassian.net/browse/DHK-4454`)
- Files: `["Screen Recording 2026-03-11 at 14.12.07.mov"]` (partial name, found on Desktop)
- Credentials: Extracted from `~/.mcp.json` (env vars not set)

### Output

### Attachment Results for DHK-4454

| # | File | Status | Size |
|---|------|--------|------|
| 1 | Screen Recording 2026-03-11 at 14.12.07.mov | Uploaded | 41.3MB |

**Uploaded:** 1/1 files
**Ticket:** https://optimizely-ext.atlassian.net/browse/DHK-4454
