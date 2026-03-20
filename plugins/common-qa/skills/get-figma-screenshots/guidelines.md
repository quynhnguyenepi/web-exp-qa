# Get Figma Screenshots Guidelines

Standards for exporting Figma frames as PNG screenshots with metadata via the Figma REST API.

## Required Information

### Always Gather Before Running

| Parameter | Required | Source |
|-----------|----------|--------|
| Figma URL | Yes | User provides the file URL |
| Personal Access Token | Yes | `FIGMA_PAT` env var or user input |
| Output directory | Yes | User specifies or defaults to `screenshots/` |
| Page filter | No | User specifies a page name to narrow scope |
| Scale | No | Defaults to 2 (high resolution) |
| Depth | No | Defaults to 3 (top-level frames) |

### Token Validation

- Token must start with `figd_`
- If token is invalid or expired, report the specific API error
- Never log or echo the token value in output

---

## Script Execution

### Locating the Script

The export script is at `scripts/export_figma_screenshots.py` relative to this skill's directory. Use Glob if the exact path is uncertain.

### Dependencies

Before running the script, verify these Python packages are available:
- `requests` -- for Figma API calls
- `pyyaml` -- for metadata file generation

If missing, instruct the user to install: `pip install requests pyyaml`

### Environment Setup

- Set `FIGMA_PAT` via `export FIGMA_PAT="figd_..."` before running
- Alternatively pass `--pat` flag directly to the script
- Never hardcode tokens in command strings that get logged

---

## Output Verification

### Expected Output Structure

```
output-directory/
  file_structure.json     # Complete Figma file tree
  README.md               # Auto-generated frame catalog
  frame_name.png          # Screenshot (one per frame)
  frame_name.yaml         # Metadata (one per frame)
```

### Metadata File Contents

Each YAML file must contain:
- `frame_number`: Sequential index
- `screenshot_file`: Corresponding PNG filename
- `figma_file_url`: Source file URL
- `figma_node_id`: Exact node ID from Figma
- `figma_node_url`: Direct link to node in Figma
- `node_name`: Frame name from Figma
- `page`: Page name containing the frame

### Post-Export Checks

- Verify PNG files are non-zero size
- Verify YAML files have all required fields
- Report total count of exported frames

---

## Error Handling

### Common Issues

| Error | Resolution |
|-------|-----------|
| 403 Forbidden | Token lacks access to the file -- verify permissions |
| 404 Not Found | File key is incorrect -- check the URL |
| No frames found | Check page name spelling, try without page filter |
| Timeout on large files | Script uses 120s timeout -- this is expected for large files |
| Python not found | Ensure `python3` is available in PATH |

---

## Anti-Patterns

### Exporting Without Page Filter on Large Files

**Problem:** Exporting all frames from a file with hundreds of pages takes very long and produces excessive output.
**Solution:** Ask the user which page to export from, or list available pages first.

### Using Depth 1 or 2

**Problem:** Depth 1 exports pages (canvases), depth 2 exports sections -- neither is useful as screenshots.
**Solution:** Default to depth 3 for top-level frames. Only change if user explicitly requests it.

### Not Verifying Output

**Problem:** Assuming the export succeeded without checking file sizes or counts.
**Solution:** Always verify at least one PNG is non-zero size and report the total count.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (validate Figma URL, PAT)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Locate and validate export script", status: "pending", activeForm: "Locating export script" },
  { content: "Run Figma export", status: "pending", activeForm: "Exporting screenshots" },
  { content: "Report results", status: "pending", activeForm: "Reporting results" }
])
```


## Error Handling

| Error | Action |
|-------|--------|
| Figma PAT not provided | Ask user for PAT or check `FIGMA_PAT` env var |
| Timeout on large files | Script uses 120s timeout, suggest smaller page filter |
| Missing Python dependencies | Display `pip install requests pyyaml` |
| No frames found | List available pages, suggest checking page name spelling |
| Authentication error (401) | Verify PAT is valid, not expired, starts with `figd_` |
| Figma MCP not available | Exit with error: "Figma MCP is not configured. See .mcp.json.template for detailed configuration." |


## Self-Correction

1. **"Wrong page name"** -> List available pages from file structure, let user pick
2. **"Export at different scale"** -> Re-run with `--scale` parameter
3. **"Include deeper frames"** -> Re-run with higher `--depth` value
4. **"Export from different file"** -> Accept new Figma URL, re-run


## Notes

### Script Reference

### scripts/export_figma_screenshots.py

Comprehensive Figma screenshot export tool with features:

- **File structure discovery**: Recursively traverses Figma document tree
- **Intelligent filtering**: Filters by page name and frame depth
- **Batch export**: Requests multiple frame exports in single API call
- **Metadata generation**: Creates YAML files with accurate node IDs
- **Documentation**: Auto-generates README with frame catalog
- **Error handling**: Clear messages for common issues

**Key functions:**
- `extract_file_key()`: Parses file key from Figma URL
- `fetch_file_structure()`: Gets complete file structure from API
- `find_frames()`: Recursively discovers frames with filtering
- `request_image_exports()`: Requests export URLs from API
- `download_screenshot()`: Downloads PNG from export URL
- `create_property_file()`: Generates YAML metadata
- `create_readme()`: Creates documentation README

