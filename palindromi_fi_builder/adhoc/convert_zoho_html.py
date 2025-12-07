#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Convert Zoho Notebook HTML exports to plaintext.

Extracts palindrome content from entity-encoded `parsed-html` attributes
in the main HTML files. Each export contains a snapshot of the document
at export time.

Preserves blank lines between palindromes to maintain document structure,
while collapsing consecutive empty lines that result from nested HTML tags.

Usage:
    uv run python -m palindromi_fi_builder.adhoc.convert_zoho_html
"""

import html
import re
from pathlib import Path
from html.parser import HTMLParser


class ContentExtractor(HTMLParser):
    """Extract text from HTML with proper handling of <br/> and <div> tags.

    Handles two HTML variants:
    - text</div><div>text (no <br> between lines)
    - text<br></div><div>text<br> (with <br> between lines)

    Both <br> and <div> can mark line boundaries, but we only flush when
    there's content to avoid duplicate blank lines.
    """

    def __init__(self):
        super().__init__()
        self.lines = []
        self.current_line = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "div"):
            if self.current_line:
                # Flush accumulated content as a line
                line_text = "".join(self.current_line).strip()
                self.lines.append(line_text)
                self.current_line = []
            elif tag == "br":
                # Empty <br> creates a blank line (separator between palindromes)
                self.lines.append("")

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        # Strip leading/trailing whitespace but preserve internal spacing
        text = data.strip()
        if text and text != "\xa0":
            self.current_line.append(text)

    def get_text(self):
        """Return plaintext preserving single blank lines between palindromes"""
        # Flush any remaining content
        line_text = "".join(self.current_line).strip()
        self.lines.append(line_text)
        self.current_line = []
        # Remove only leading/trailing empty lines, preserve internal blank lines
        while self.lines and not self.lines[0]:
            self.lines.pop(0)
        while self.lines and not self.lines[-1]:
            self.lines.pop()
        # Collapse consecutive empty lines into single blank lines
        result = []
        prev_empty = False
        for line in self.lines:
            if not line:
                if not prev_empty:
                    result.append("")
                prev_empty = True
            else:
                result.append(line)
                prev_empty = False
        return "\n".join(result)


def extract_from_main_html(html_path: Path) -> str:
    """Extract content from entity-encoded blocks in the main HTML file."""
    # Try UTF-8 first, fall back to Windows-1252 (declared charset)
    raw_bytes = html_path.read_bytes()
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content = raw_bytes.decode("windows-1252")

    # Find entity-encoded content blocks (parsed-html attribute)
    pattern = r'parsed-html="([^"]+)"'
    match = re.search(pattern, content)

    if match:
        encoded = match.group(1)
        decoded = html.unescape(encoded)

        extractor = ContentExtractor()
        extractor.feed(decoded)
        return extractor.get_text()

    return ""


def main():
    """Process all YYYY-MM-DD.html files in zoho-history/, outputting only new palindromes"""
    zoho_dir = Path(__file__).parent.parent.parent / "zoho-history"

    # Find all main HTML files
    html_files = sorted(zoho_dir.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html"))

    if not html_files:
        print("No HTML files found")
        return

    print(f"Found {len(html_files)} HTML files\n")

    seen_palindromes = set()

    for html_file in html_files:
        date_str = html_file.stem
        print(f"Processing {date_str}...")
        try:
            text = extract_from_main_html(html_file)

            # Parse palindromes (separated by blank lines)
            # Group consecutive non-empty lines as a single palindrome
            all_palindromes = []
            current_lines = []
            for line in text.split("\n"):
                if line.strip():
                    current_lines.append(line)
                else:
                    if current_lines:
                        all_palindromes.append("\n".join(current_lines))
                        current_lines = []
            if current_lines:
                all_palindromes.append("\n".join(current_lines))

            # Filter to only new palindromes
            new_palindromes = [p for p in all_palindromes if p not in seen_palindromes]

            # Add new ones to seen set
            seen_palindromes.update(new_palindromes)

            # Create or delete output file based on whether there are new palindromes
            output_path = zoho_dir / f"{date_str}.txt"
            if new_palindromes:
                output_text = "\n\n".join(new_palindromes) + "\n"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(output_text)
                print(f"  Extracted {len(all_palindromes)} total, {len(new_palindromes)} new → {output_path.name}")
                print(f"  First new: {new_palindromes[0][:60]}...")
            else:
                if output_path.exists():
                    output_path.unlink()
                print(f"  Extracted {len(all_palindromes)} total, 0 new (file deleted)")

        except Exception as e:
            print(f"  Error processing {date_str}: {e}")


if __name__ == "__main__":
    main()
