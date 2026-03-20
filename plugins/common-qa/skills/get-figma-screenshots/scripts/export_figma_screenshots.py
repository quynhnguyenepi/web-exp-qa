#!/usr/bin/env python3
"""
Export screenshots from Figma via the Figma REST API.

This script fetches frame data from a Figma file and exports high-resolution
screenshots with metadata YAML files.

Usage:
    # Basic usage
    python3 scripts/export_figma_screenshots.py \
        --url "https://www.figma.com/design/FILE_KEY/NAME" \
        --pat "figd_..." \
        --output "path/to/output"

    # Filter by page
    python3 scripts/export_figma_screenshots.py \
        --url "https://www.figma.com/design/FILE_KEY/NAME" \
        --page "• Axiom 1 [MVP]" \
        --output "path/to/output"

    # Using environment variable for PAT
    export FIGMA_PAT="figd_..."
    python3 scripts/export_figma_screenshots.py \
        --url "https://www.figma.com/design/FILE_KEY/NAME" \
        --output "path/to/output"

Arguments:
    --url       Figma file URL (required)
    --pat       Figma Personal Access Token (optional, uses FIGMA_PAT env var if not provided)
    --page      Filter to specific page name (optional, exports all pages if not provided)
    --output    Output directory path (required)
    --scale     Export scale (default: 2 for high resolution)
    --depth     Frame depth level to export (default: 3 for top-level screens)
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("Error: 'pyyaml' library not found. Install with: pip install pyyaml")
    sys.exit(1)


def extract_file_key(figma_url: str) -> str:
    """Extract file key from Figma URL."""
    # Pattern: https://www.figma.com/design/FILE_KEY/...
    # or: https://figma.com/file/FILE_KEY/...
    match = re.search(r'figma\.com/(?:design|file)/([^/?]+)', figma_url)
    if not match:
        raise ValueError(f"Could not extract file key from URL: {figma_url}")
    return match.group(1)


def get_figma_pat(provided_pat: Optional[str]) -> str:
    """Get Figma PAT from argument or environment variable."""
    if provided_pat:
        return provided_pat

    pat = os.environ.get('FIGMA_PAT')
    if not pat:
        raise ValueError(
            "Figma PAT not provided. Either:\n"
            "  1. Pass --pat argument\n"
            "  2. Set FIGMA_PAT environment variable"
        )
    return pat


def fetch_file_structure(file_key: str, pat: str) -> Dict:
    """Fetch complete file structure from Figma API."""
    print(f"Fetching file structure for {file_key}...")

    response = requests.get(
        f"https://api.figma.com/v1/files/{file_key}",
        headers={"X-Figma-Token": pat},
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Figma API error: {response.status_code}\n{response.text}")

    return response.json()


def find_frames(node: Dict, frames: Optional[List] = None, depth: int = 0,
                page_name: Optional[str] = None, current_page: Optional[str] = None,
                target_depth: int = 3) -> List[Dict]:
    """
    Recursively find all frames in the Figma file.

    Args:
        node: Current node in the tree
        frames: Accumulated list of frames
        depth: Current depth in the tree
        page_name: Optional page name to filter by
        current_page: Name of the current page being traversed
        target_depth: Depth level to extract frames from (default 3 = top-level screens)

    Returns:
        List of frame dictionaries with id, name, page, and depth
    """
    if frames is None:
        frames = []

    node_type = node.get('type')
    node_id = node.get('id')
    node_name = node.get('name', 'Unnamed')

    # Track page names (depth 1 = CANVAS = page)
    if depth == 1 and node_type == 'CANVAS':
        current_page = node_name

    # Collect FRAME nodes at target depth
    if node_type == 'FRAME' and depth == target_depth:
        # Filter by page if specified
        if page_name is None or current_page == page_name:
            frames.append({
                'id': node_id,
                'name': node_name,
                'page': current_page,
                'depth': depth
            })

    # Recurse into children
    if 'children' in node:
        for child in node['children']:
            find_frames(child, frames, depth + 1, page_name, current_page, target_depth)

    return frames


def request_image_exports(file_key: str, pat: str, node_ids: List[str],
                         scale: int = 2) -> Dict[str, str]:
    """
    Request image export URLs from Figma API.

    Returns:
        Dictionary mapping node IDs to export URLs
    """
    print(f"Requesting export URLs for {len(node_ids)} frames...")

    response = requests.get(
        f"https://api.figma.com/v1/images/{file_key}",
        params={
            "ids": ",".join(node_ids),
            "format": "png",
            "scale": scale
        },
        headers={"X-Figma-Token": pat},
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Figma API error: {response.status_code}\n{response.text}")

    data = response.json()

    if data.get('err'):
        raise Exception(f"Figma API error: {data['err']}")

    return data.get('images', {})


def safe_filename(name: str) -> str:
    """Convert frame name to safe filename."""
    return name.replace('/', '_').replace(' ', '_').replace('\\', '_')


def get_unique_filename(base_name: str, used_names: set) -> str:
    """
    Generate a unique filename, appending a counter if the base name is already used.

    Args:
        base_name: The base filename (without extension)
        used_names: Set of already-used filenames

    Returns:
        A unique filename that isn't in used_names
    """
    if base_name not in used_names:
        used_names.add(base_name)
        return base_name

    # Find next available counter
    counter = 1
    while f"{base_name}_{counter:02d}" in used_names:
        counter += 1

    unique_name = f"{base_name}_{counter:02d}"
    used_names.add(unique_name)
    return unique_name


def download_screenshot(url: str, output_path: Path) -> None:
    """Download screenshot from URL to file."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        f.write(response.content)


def create_property_file(frame: Dict, screenshot_file: str, figma_url: str,
                        frame_number: int, output_path: Path) -> None:
    """Create YAML property file for a screenshot."""
    node_id = frame['id']
    node_name = frame['name']

    props = {
        'frame_number': frame_number,
        'screenshot_file': screenshot_file,
        'figma_file_url': figma_url,
        'figma_node_id': node_id,
        'figma_node_url': f"{figma_url}?node-id={node_id.replace(':', '-')}",
        'node_name': node_name,
        'page': frame.get('page', 'Unknown'),
        'frame_type': node_name.split('/')[0] if '/' in node_name else node_name,
        'description': f"Figma frame: {node_name}"
    }

    with open(output_path, 'w') as f:
        yaml.dump(props, f, default_flow_style=False, sort_keys=False)


def create_readme(frames: List[Dict], output_dir: Path, figma_url: str,
                 page_filter: Optional[str], scale: int) -> None:
    """Create README.md documenting the exported screenshots."""

    # Group by page
    frames_by_page = {}
    for frame in frames:
        page = frame.get('page', 'Unknown')
        if page not in frames_by_page:
            frames_by_page[page] = []
        frames_by_page[page].append(frame)

    content = f"""# Figma Screenshots Export

Exported from: {figma_url}

## Export Details

- **Total screenshots**: {len(frames)}
- **Page filter**: {page_filter or 'All pages'}
- **Export scale**: {scale}x
- **Export date**: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Contents

"""

    # Track used filenames to match actual exported files
    used_filenames = set()

    for page, page_frames in sorted(frames_by_page.items()):
        content += f"\n### {page} ({len(page_frames)} frames)\n\n"

        for frame in sorted(page_frames, key=lambda x: x['name']):
            safe_name = safe_filename(frame['name'])
            unique_name = get_unique_filename(safe_name, used_filenames)
            screenshot_file = f"{unique_name}.png"
            yaml_file = f"{unique_name}.yaml"
            node_url = f"{figma_url}?node-id={frame['id'].replace(':', '-')}"

            content += f"- **{frame['name']}** (node: {frame['id']})\n"
            content += f"  - Screenshot: `{screenshot_file}`\n"
            content += f"  - Properties: `{yaml_file}`\n"
            content += f"  - [View in Figma]({node_url})\n\n"

    content += """
## Property File Format

Each YAML file contains:
```yaml
frame_number: 1
screenshot_file: example.png
figma_file_url: https://www.figma.com/design/...
figma_node_id: "12345:67890"
figma_node_url: https://www.figma.com/design/...?node-id=12345-67890
node_name: example/frame
page: Page Name
frame_type: example
description: Figma frame: example/frame
```

## Usage

```markdown
![Frame Name](path/to/screenshot.png)

[View in Figma](https://www.figma.com/design/...?node-id=...)
```
"""

    readme_path = output_dir / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(content)

    print(f"✓ Created README.md")


def main():
    parser = argparse.ArgumentParser(
        description='Export screenshots from Figma via REST API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--url', required=True, help='Figma file URL')
    parser.add_argument('--pat', help='Figma Personal Access Token (or use FIGMA_PAT env var)')
    parser.add_argument('--page', help='Filter to specific page name')
    parser.add_argument('--output', required=True, help='Output directory path')
    parser.add_argument('--scale', type=int, default=2, help='Export scale (default: 2)')
    parser.add_argument('--depth', type=int, default=3, help='Frame depth to export (default: 3)')

    args = parser.parse_args()

    try:
        # Get Figma PAT
        pat = get_figma_pat(args.pat)

        # Extract file key from URL
        file_key = extract_file_key(args.url)
        print(f"File key: {file_key}")

        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_dir}")

        # Fetch file structure
        file_data = fetch_file_structure(file_key, pat)

        # Find frames
        frames = find_frames(
            file_data['document'],
            page_name=args.page,
            target_depth=args.depth
        )

        if not frames:
            print(f"\n❌ No frames found")
            if args.page:
                print(f"   Page filter: '{args.page}'")
                print("\nAvailable pages:")
                # Show available pages
                pages = set()
                def collect_pages(node, depth=0):
                    if depth == 1 and node.get('type') == 'CANVAS':
                        pages.add(node.get('name', 'Unnamed'))
                    if 'children' in node:
                        for child in node['children']:
                            collect_pages(child, depth + 1)
                collect_pages(file_data['document'])
                for page in sorted(pages):
                    print(f"   - {page}")
            return 1

        print(f"\n✓ Found {len(frames)} frames")
        if args.page:
            print(f"  Page filter: '{args.page}'")

        # Request image exports
        node_ids = [f['id'] for f in frames]
        image_urls = request_image_exports(file_key, pat, node_ids, args.scale)

        print(f"✓ Got {len(image_urls)} export URLs\n")

        # Download screenshots and create property files
        downloaded = 0
        used_filenames = set()  # Track used filenames to handle duplicates

        for idx, frame in enumerate(sorted(frames, key=lambda x: x['name']), 1):
            node_id = frame['id']
            name = frame['name']
            url = image_urls.get(node_id)

            if not url:
                print(f"  ✗ {name} - No export URL")
                continue

            try:
                safe_name = safe_filename(name)
                unique_name = get_unique_filename(safe_name, used_filenames)
                screenshot_file = f"{unique_name}.png"
                yaml_file = f"{unique_name}.yaml"

                # Download screenshot
                screenshot_path = output_dir / screenshot_file
                download_screenshot(url, screenshot_path)

                # Create property file
                yaml_path = output_dir / yaml_file
                create_property_file(frame, screenshot_file, args.url, idx, yaml_path)

                downloaded += 1
                print(f"  ✓ {idx:2d}. {name}")

                time.sleep(0.15)  # Be nice to Figma's servers

            except Exception as e:
                print(f"  ✗ {name} - Error: {e}")

        print(f"\n✓ Downloaded {downloaded}/{len(frames)} screenshots")

        # Create README
        create_readme(frames, output_dir, args.url, args.page, args.scale)

        print(f"\n✅ Export complete! Output: {output_dir}/")
        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
