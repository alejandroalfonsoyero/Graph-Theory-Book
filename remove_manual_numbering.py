import re
from pathlib import Path


def remove_manual_numbering(file_path: Path):
    """
    Reads a Markdown file, removes manual numbering from headers (H1, H2, H3),
    and writes the modified content back to the file.
    Assumes headers follow patterns like '# 1. Title', '## 1.1. Subtitle', etc.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        modified = False

        # Regex to match Markdown headers with optional leading spaces
        # and then a numerical pattern (e.g., 1., 1.1., 1.1.1.)
        # and capture the hash marks and the rest of the title.
        # Example: '### 1.2.3. My Title' -> '### My Title'
        header_pattern = re.compile(r"^(#+\s*)(\d+\.?\s*)+\s*(.*)$")

        for line in lines:
            match = header_pattern.match(line)
            if match:
                # Reconstruct the line without the numerical part
                new_line = f"{match.group(1)}{match.group(3).strip()}"
                if new_line != line:
                    new_lines.append(new_line)
                    modified = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        if modified:
            file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            print(f"✓ Removed manual numbering from headers in: {file_path.name}")
        else:
            print(f"No manual numbering found in headers for: {file_path.name}")

    except Exception as e:
        print(f"✗ Error processing {file_path.name}: {e}")


def main():
    root_dir = Path(__file__).parent
    capitulos_dir = root_dir / "capitulos"

    if not capitulos_dir.is_dir():
        print(f"Error: Directory not found: {capitulos_dir}")
        return

    markdown_files = list(capitulos_dir.glob("*.md"))
    if not markdown_files:
        print(f"No Markdown files found in {capitulos_dir}")
        return

    print(
        f"Removing manual numbering from headers in {len(markdown_files)} Markdown files..."
    )
    for md_file in sorted(markdown_files):  # Process in order
        remove_manual_numbering(md_file)
    print("Manual numbering removal complete.")


if __name__ == "__main__":
    main()
