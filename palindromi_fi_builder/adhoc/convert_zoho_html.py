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
    """Extract text from HTML with proper handling of <br/> and <div> tags"""

    def __init__(self):
        super().__init__()
        self.lines = []
        self.current_line = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "div"):
            # Handle <br/> and <div> tags as line breaks
            line_text = "".join(self.current_line).strip()
            self.lines.append(line_text)
            self.current_line = []

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
    """Process all YYYY-MM-DD.html files in zoho-history/"""
    zoho_dir = Path(__file__).parent.parent.parent / "zoho-history"

    # Find all main HTML files
    html_files = sorted(zoho_dir.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html"))

    if not html_files:
        print("No HTML files found")
        return

    print(f"Found {len(html_files)} HTML files\n")

    for html_file in html_files:
        date_str = html_file.stem
        print(f"Processing {date_str}...")
        try:
            text = extract_from_main_html(html_file)

            # Create output file
            output_path = zoho_dir / f"{date_str}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            lines = text.split("\n")
            print(f"  Extracted {len(lines)} lines → {output_path.name}")
            print(f"  First line: {lines[0][:60]}...")

        except Exception as e:
            print(f"  Error processing {date_str}: {e}")


if __name__ == "__main__":
    main()
