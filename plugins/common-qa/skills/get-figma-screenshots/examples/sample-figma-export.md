# Sample: Export Figma Screenshots with Page Filter

---

## Input

User request: "Export screenshots from the 'MVP Screens' page of this Figma file: https://www.figma.com/design/ABC123def/MyProject"

---

## Step 1: Gather Required Information

```
Figma URL: https://www.figma.com/design/ABC123def/MyProject
  - File key extracted: ABC123def

Personal Access Token:
  - FIGMA_PAT environment variable: set

Page filter: "MVP Screens"
Output directory: ./screenshots
Scale: 2 (default, high resolution)
Depth: 3 (default, top-level frames)
```

---

## Step 2: Locate the Export Script

```
Script found at: plugins/common-qa/skills/get-figma-screenshots/scripts/export_figma_screenshots.py
```

---

## Step 3: Run the Export Script

```
Command:
  python3 plugins/common-qa/skills/get-figma-screenshots/scripts/export_figma_screenshots.py \
    --url "https://www.figma.com/design/ABC123def/MyProject" \
    --page "MVP Screens" \
    --output "./screenshots"

Output:
  Fetching file structure for ABC123def...
  Found 4 pages: Cover, MVP Screens, Components, Archive
  Filtering to page: "MVP Screens"
  Found 12 frames at depth 3
  Requesting image exports...
  Downloading frame 1/12: fx/login-page.png
  Downloading frame 2/12: fx/dashboard.png
  Downloading frame 3/12: fx/settings-general.png
  ...
  Downloading frame 12/12: fx/error-404.png
  Creating metadata files...
  Creating README.md...
  Done! Exported 12 frames to ./screenshots/
```

---

## Step 4: Verify Output

```
Output directory contents:
  screenshots/
    file_structure.json           (245 KB)
    README.md                     (3.2 KB)
    fx_login-page.png             (89 KB)
    fx_login-page.yaml            (0.4 KB)
    fx_dashboard.png              (156 KB)
    fx_dashboard.yaml             (0.4 KB)
    fx_settings-general.png       (112 KB)
    fx_settings-general.yaml      (0.4 KB)
    ...
    fx_error-404.png              (34 KB)
    fx_error-404.yaml             (0.4 KB)

Verification:
  - 12 PNG files, all non-zero size
  - 12 YAML metadata files, all contain required fields
  - README.md generated with frame catalog

Export complete: 12 frames from "MVP Screens" page exported to ./screenshots/
```

---

## Sample Metadata File (fx_login-page.yaml)

```yaml
frame_number: 1
screenshot_file: fx_login-page.png
figma_file_url: https://www.figma.com/design/ABC123def/MyProject
figma_node_id: "123:456"
figma_node_url: https://www.figma.com/design/ABC123def/MyProject?node-id=123:456
node_name: fx/login-page
page: MVP Screens
frame_type: fx
description: Login page screen
```
