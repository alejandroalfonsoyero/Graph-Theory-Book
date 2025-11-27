import re
from pathlib import Path


def fix_latex_approx_in_table(file_path: Path):
    """
    Reads 04_arboles_expansion.md, finds the table, and fixes LaTeX escaping
    for \\approx within math environments.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        modified = False

        # Regex to find lines within the table that contain the problematic pattern
        # This will target the specific lines where $E \\\\approx V^2$ or $E \\\\approx V$ appears
        # We need to ensure it only matches within the table context.
        # A simpler approach is to replace globally, and if it causes issues elsewhere,
        # we can refine the regex to be more specific to table rows.

        # Pattern to replace \\\\approx with \\approx inside $...$
        # This is for Markdown that pandoc will convert to LaTeX.
        # Markdown source: `$\\\\approx$` should become `$\\approx$` in Pandoc's output.
        # If the input is actually `E \\\\approx V^2`, then in the raw string, it needs to be `E \\approx V^2`.
        # However, the previous `read_file` output shows `E \\\\approx V^2`.
        # This means the Python string literal contains `\\approx`.
        # When pandoc reads the Markdown, it sees `E \approx V^2`.
        # So the original problem was either the raw string itself had too many backslashes,
        # or pandoc is not handling the single backslash correctly in math mode within tables.
        # Let's assume the Markdown should contain `\\approx` for Pandoc to output `\approx`.
        # So we need to change `\\\\approx` (in markdown) to `\\approx` (in markdown).
        # This means changing `\\texttt{\\\\}` in the raw string to `\`.

        # Given the previous error `! LaTeX Error: Missing $ inserted. l.3121 \textbf{Grafo Ideal} & Densos (\\(E \\\\a`
        # This indicates that `\\\\` is being interpreted as `\` and `\\approx` is `\approx`
        # The problem is that the `\\` *outside* the math mode is also affecting it.
        #
        # Let's try to target the exact string `\\\\approx` and replace it with `\\approx`
        # in the raw Markdown content.

        for i, line in enumerate(lines):
            # Target the specific lines in the table (based on previous debug)
            if "Grafo Ideal" in line or "Complejidad Temporal" in line:
                # Replace \\\\approx with \\approx
                new_line = line.replace("\\\\\\\\approx", "\\\\approx")
                # Replace \\\\log with \\log
                new_line = new_line.replace("\\\\\\\\log", "\\\\log")

                if new_line != line:
                    lines[i] = new_line
                    modified = True

        if modified:
            file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"✓ Fixed LaTeX escaping in table for: {file_path.name}")
        else:
            print(
                f"No changes needed for LaTeX escaping in table for: {file_path.name}"
            )

    except Exception as e:
        print(f"✗ Error fixing {file_path.name}: {e}")


def main():
    script_dir = Path(__file__).parent
    target_file = script_dir / "capitulos" / "04_arboles_expansion.md"

    if not target_file.is_file():
        print(f"Error: Target file not found: {target_file}")
        return

    print(f"Starting to fix LaTeX escaping in table of {target_file.name}...")
    fix_latex_approx_in_table(target_file)
    print("Fix script completed.")


if __name__ == "__main__":
    main()
