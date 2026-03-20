# Export Figma Screenshots Skill

Export high-resolution screenshots from Figma files via the REST API with automatic metadata generation.

## Purpose

This skill provides a reusable workflow for exporting Figma frames as PNG screenshots with accompanying YAML metadata files. It's designed for:

- **Documentation**: Export UI mockups for technical documentation
- **Design handoff**: Generate screenshots with accurate Figma node references
- **Archival**: Create snapshots of design work with metadata
- **Automation**: Programmatically export frames filtered by page or criteria

## Use Cases

1. **Project Documentation**: Export all screens from a specific Figma page to include in markdown docs
2. **Design Reviews**: Batch export frames with metadata for review processes
3. **Version Control**: Archive design iterations with accurate node IDs for traceability
4. **Multi-Project**: Reuse the same script across multiple Figma files with different filters

## Quick Start

### Prerequisites

1. **Figma Personal Access Token (PAT)**:
   - Go to Figma → Settings → Personal Access Tokens
   - Create a new token
   - Copy the token (starts with `figd_`)

2. **Python Dependencies**:
   ```bash
   pip install requests pyyaml
   ```

### Basic Usage

```bash
# Set your PAT as environment variable
export FIGMA_PAT="figd_your_token_here"

# Export all frames from a file
python3 <path-to-script>/export_figma_screenshots.py \
    --url "https://www.figma.com/design/FILE_KEY/FILE_NAME" \
    --output "screenshots"
```

### With Page Filter

```bash
# Export only frames from specific page
python3 <path-to-script>/export_figma_screenshots.py \
    --url "https://www.figma.com/design/FILE_KEY/FILE_NAME" \
    --page "• Axiom 1 [MVP]" \
    --output "mvp-screenshots"
```

## Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--url` | Yes | Figma file URL | - |
| `--pat` | No* | Personal Access Token | Uses `FIGMA_PAT` env var |
| `--page` | No | Filter to specific page name | All pages |
| `--output` | Yes | Output directory path | - |
| `--scale` | No | Export scale (1-4) | 2 (high resolution) |
| `--depth` | No | Frame depth level | 3 (top-level screens) |

*Required if `FIGMA_PAT` environment variable is not set

## Expected Output

The script generates:

### 1. PNG Screenshots
High-resolution (2x by default) images with safe filenames:
- Slashes replaced with underscores
- Spaces replaced with underscores
- Example: `fx/create-field` → `fx_create-field.png`

### 2. YAML Metadata Files
One YAML file per screenshot containing:

```yaml
frame_number: 1
screenshot_file: fx_fields.png
figma_file_url: https://www.figma.com/design/5qdtB9r8HDUeWLHzgfdu4H/Custom-Fields
figma_node_id: "13709:32283"
figma_node_url: https://www.figma.com/design/5qdtB9r8HDUeWLHzgfdu4H/Custom-Fields?node-id=13709-32283
node_name: fx/fields
page: • Axiom 1 [MVP]
frame_type: fx
description: Figma frame: fx/fields
```

### 3. Documentation README
Auto-generated `README.md` with:
- Export details (date, scale, page filter)
- Organized listing of all frames by page
- Links to view each frame in Figma
- Usage examples

### 4. File Structure JSON
Complete Figma file structure saved as `file_structure.json` for reference.

## Using with Claude Code

Simply trigger the skill when you need to export Figma screenshots:

**Example prompts:**
- "Export screenshots from this Figma file: [URL]"
- "Export frames from the 'MVP' page in Figma"
- "Get all Figma screenshots with metadata"

Claude will:
1. Ask for missing information (PAT, output directory)
2. Run the export script
3. Report results and output location

## Troubleshooting

### "No frames found"
- Check page name spelling (must match exactly)
- Script will list available pages if filter doesn't match
- Try without `--page` parameter to see all pages

### "Authentication required"
- Verify PAT is valid and not expired
- Ensure token has access to the file
- Check token format starts with `figd_`

### Timeout errors
- Script uses 120s timeout (increased from default 30s)
- Large files may take longer
- Export happens in batches to manage load

### Missing dependencies
```bash
# Install required libraries
pip install requests pyyaml
```

## Examples

### Example 1: Documentation Screenshots

```bash
export FIGMA_PAT="figd_..."

# Export all screens from "User Flows" page
python3 <path-to-script>/export_figma_screenshots.py \
    --url "https://www.figma.com/design/ABC123/App-Design" \
    --page "User Flows" \
    --output "docs/screenshots/user-flows"
```

Result: All frames from "User Flows" page exported to `docs/screenshots/user-flows/`

### Example 2: High-Resolution Export

```bash
# Export at 3x scale for print quality
python3 <path-to-script>/export_figma_screenshots.py \
    --url "https://www.figma.com/design/ABC123/Marketing" \
    --scale 3 \
    --output "print-quality"
```

Result: 3x resolution screenshots suitable for print materials

### Example 3: Component Library Export

```bash
# Export component library (depth 4 for nested components)
python3 <path-to-script>/export_figma_screenshots.py \
    --url "https://www.figma.com/design/ABC123/Components" \
    --depth 4 \
    --output "component-screenshots"
```

Result: Deeper frame level captured for component documentation

## Integration with Documentation

Use the exported screenshots in markdown:

```markdown
![Custom Fields Page](screenshots/fx_fields.png)

[View in Figma](https://www.figma.com/design/...?node-id=13709-32283)
```

The YAML metadata files can be programmatically read to auto-generate documentation.

## Skill Location

```
plugins/opti-exp-standards/skills/utils-figma-screenshots/
├── SKILL.md                          # Skill instructions
├── README.md                         # This file
└── scripts/
    └── export_figma_screenshots.py   # Main export script
```

## Updates and Improvements

This skill can be updated using the `update-skill` skill:

```
Use Skill(update-skill) to improve this skill
```

If you encounter issues or need additional features, provide feedback and the skill can be enhanced.
