# Test Cases for get-figma-screenshots Skill

## TC-001: Export All Frames from File

**Input:** Run `/common-qa:get-figma-screenshots` with a valid Figma URL, no page filter.

**Expected:**
- Extracts file key from URL
- Fetches file structure from Figma API
- Discovers all frames at depth 3
- Exports PNGs and generates YAML metadata for each
- Creates file_structure.json and README.md

**Pass Criteria:**
- All frames exported as PNG files
- Each PNG has a corresponding YAML metadata file
- YAML contains all required fields (frame_number, screenshot_file, figma_node_id, etc.)
- file_structure.json and README.md generated

---

## TC-002: Export with Page Filter

**Input:** Run with `--page "MVP Screens"` to filter to a specific page.

**Expected:**
- Only exports frames from the specified page
- Ignores frames on other pages
- Reports which page was filtered

**Pass Criteria:**
- Only frames from "MVP Screens" page are exported
- Frame count matches the number of depth-3 frames on that page
- Other pages' frames are not present in output

---

## TC-003: Invalid or Expired Token

**Input:** Run with an expired or invalid `FIGMA_PAT` token.

**Expected:**
- API returns 403 Forbidden
- Script reports authentication error
- Suggests verifying the token

**Pass Criteria:**
- Clear error message about authentication failure
- No partial output files created
- Token value is not logged or displayed

---

## TC-004: Page Name Not Found

**Input:** Run with `--page "Nonexistent Page"` that does not match any page in the file.

**Expected:**
- Script lists available page names
- Reports that the specified page was not found
- Does not export anything

**Pass Criteria:**
- Available pages listed for user reference
- Clear message: page not found
- No files created in output directory

---

## TC-005: Custom Scale and Depth

**Input:** Run with `--scale 3 --depth 4` for higher resolution and deeper frame discovery.

**Expected:**
- Exports at 3x scale (larger PNG files)
- Discovers frames at depth 4 instead of default 3
- May find more or different frames than default

**Pass Criteria:**
- PNG files are larger than default 2x exports
- Frames at depth 4 are discovered and exported
- Metadata reflects correct depth level
