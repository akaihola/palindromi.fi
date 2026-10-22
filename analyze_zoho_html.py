# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""Analyze Zoho Notebook HTML export structure.

Exploratory diagnostics, not an importer. The later findings and current import
plan are in docs/zoho-import.md. The existing converter loses empty-div block
separators and orders exports by unreliable filenames; its output is unsafe to
import. These diagnostics decode as UTF-8 with replacement, so they do not
preserve the investigated Windows-1252 exports exactly.
"""

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def analyze_html(filepath: Path) -> None:
    """Parse and analyze the HTML file structure."""
    print(f"Analyzing: {filepath}")
    print(f"File size: {filepath.stat().st_size:,} bytes\n")

    content = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(content, "lxml")

    # Look for script tags that might contain revision data
    print("=" * 60)
    print("SCRIPT TAGS ANALYSIS")
    print("=" * 60)
    scripts = soup.find_all("script")
    print(f"Found {len(scripts)} script tags\n")

    for i, script in enumerate(scripts):
        script_content = script.string or ""
        if len(script_content) > 100:
            # Look for interesting patterns
            preview = script_content[:200].replace("\n", " ")
            print(f"Script {i}: {len(script_content):,} chars - {preview}...")

            # Check for revision-related keywords
            if any(kw in script_content.lower() for kw in ["revision", "version", "history", "delta", "patch"]):
                print(f"  ^ Contains revision-related keywords!")

            # Check for JSON data
            if script_content.strip().startswith("{") or "JSON" in script_content:
                print(f"  ^ May contain JSON data")

    # Look for data attributes
    print("\n" + "=" * 60)
    print("DATA ATTRIBUTES ANALYSIS")
    print("=" * 60)
    elements_with_data = soup.find_all(attrs={"data-version": True})
    print(f"Elements with data-version: {len(elements_with_data)}")

    # Search for elements with revision in attribute names manually
    revision_elements = []
    for tag in soup.find_all(True):
        if any("revision" in attr.lower() for attr in tag.attrs.keys()):
            revision_elements.append(tag)
    print(f"Elements with revision attrs: {len(revision_elements)}")

    # Look for hidden inputs or elements
    print("\n" + "=" * 60)
    print("HIDDEN/META ELEMENTS")
    print("=" * 60)
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    print(f"Hidden inputs: {len(hidden_inputs)}")
    for inp in hidden_inputs[:10]:
        print(f"  - {inp.get('name', 'unnamed')}: {str(inp.get('value', ''))[:100]}")

    meta_tags = soup.find_all("meta")
    print(f"\nMeta tags: {len(meta_tags)}")
    for meta in meta_tags:
        print(f"  - {meta.get('name', meta.get('property', 'unnamed'))}: {meta.get('content', '')[:100]}")

    # Search for revision patterns in raw content
    print("\n" + "=" * 60)
    print("PATTERN SEARCH IN RAW HTML")
    print("=" * 60)

    patterns = [
        (r'"revision[s]?":\s*[\[\{]', "revision JSON"),
        (r'"version[s]?":\s*[\[\{"\d]', "version JSON"),
        (r'"history":\s*[\[\{]', "history JSON"),
        (r'"delta[s]?":\s*[\[\{]', "delta JSON"),
        (r'"ops?":\s*\[', "ops array (Quill delta format)"),
        (r'data-\w*version', "data-version attributes"),
        (r'data-\w*revision', "data-revision attributes"),
    ]

    for pattern, desc in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Found {len(matches)} matches for {desc}")
            # Show context around first match
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 200)
                context = content[start:end].replace("\n", " ")
                print(f"  Context: ...{context}...")

    # Look for large JSON blobs
    print("\n" + "=" * 60)
    print("LARGE JSON BLOB SEARCH")
    print("=" * 60)

    # Find potential JSON objects
    json_pattern = r'\{[^{}]{1000,}'
    json_matches = re.finditer(json_pattern, content)
    for i, match in enumerate(json_matches):
        if i >= 5:
            print("  (showing first 5 only)")
            break
        blob = match.group()[:300]
        print(f"Large JSON at pos {match.start()}: {blob}...")

    # Check the _tiedostot directory for additional assets
    print("\n" + "=" * 60)
    print("ASSETS DIRECTORY ANALYSIS")
    print("=" * 60)
    assets_dir = filepath.parent / f"{filepath.stem}_tiedostot"
    if assets_dir.exists():
        files = list(assets_dir.iterdir())
        print(f"Found {len(files)} files in {assets_dir.name}/")

        # Group by extension
        by_ext: dict[str, list[Path]] = {}
        for f in files:
            ext = f.suffix.lower()
            by_ext.setdefault(ext, []).append(f)

        for ext, ext_files in sorted(by_ext.items()):
            print(f"  {ext or '(no ext)'}: {len(ext_files)} files")
            # Show some examples
            for ef in ext_files[:3]:
                print(f"    - {ef.name} ({ef.stat().st_size:,} bytes)")

        # Check JS files for revision logic
        js_files = by_ext.get(".js", [])
        for js_file in js_files:
            js_content = js_file.read_text(encoding="utf-8", errors="replace")
            if any(kw in js_content.lower() for kw in ["revision", "history", "delta", "version"]):
                print(f"\n  {js_file.name} contains revision-related code!")
                # Find relevant snippets
                for kw in ["revision", "history", "delta"]:
                    for m in re.finditer(rf'.{{0,50}}{kw}.{{0,100}}', js_content, re.IGNORECASE):
                        print(f"    ...{m.group()}...")
                        break


def extract_script_data(filepath: Path) -> None:
    """Inspect scripts over 100,000 characters for possible revision data."""
    print("\n" + "=" * 60)
    print("DETAILED SCRIPT ANALYSIS")
    print("=" * 60)

    content = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(content, "lxml")

    scripts = soup.find_all("script")
    for i, script in enumerate(scripts):
        script_content = script.string or ""
        if len(script_content) > 100000:  # Large scripts
            print(f"\nAnalyzing Script {i} ({len(script_content):,} chars):")

            # Look for noteData or similar
            patterns_to_find = [
                r'(noteData|cardData|documentData|editorData)\s*=\s*',
                r'(revisions?|versions?|history)\s*[=:]\s*\[',
                r'(deltas?|ops)\s*[=:]\s*\[',
                r'"content"\s*:\s*"',
                r'"html"\s*:\s*"',
                r'"text"\s*:\s*"',
            ]

            for pat in patterns_to_find:
                matches = list(re.finditer(pat, script_content, re.IGNORECASE))
                if matches:
                    print(f"\n  Pattern '{pat}' found {len(matches)} times:")
                    for m in matches[:3]:
                        start = m.start()
                        end = min(start + 500, len(script_content))
                        context = script_content[start:end]
                        # Clean up for display
                        context = context.replace("\n", "\\n")[:300]
                        print(f"    pos {start}: {context}...")

            # Look for JSON-like structures with content
            print("\n  Looking for embedded document content...")
            # Find patterns like {"ops":[ or "delta":{"ops":[
            ops_pattern = r'"ops"\s*:\s*\['
            ops_matches = list(re.finditer(ops_pattern, script_content))
            print(f"  Found {len(ops_matches)} 'ops' arrays (Quill delta format)")

            if ops_matches:
                # Extract and analyze first few ops arrays
                for j, m in enumerate(ops_matches[:5]):
                    start = m.start()
                    # Try to find the matching closing bracket
                    depth = 0
                    end = start
                    in_string = False
                    escape_next = False
                    for k, c in enumerate(script_content[start:start+10000]):
                        if escape_next:
                            escape_next = False
                            continue
                        if c == '\\':
                            escape_next = True
                            continue
                        if c == '"' and not escape_next:
                            in_string = not in_string
                        if not in_string:
                            if c == '[':
                                depth += 1
                            elif c == ']':
                                depth -= 1
                                if depth == 0:
                                    end = start + k + 1
                                    break
                    if end > start:
                        ops_str = script_content[start:end]
                        print(f"\n    ops array {j} at pos {start}, length {len(ops_str)}")
                        # Try to parse as JSON
                        try:
                            ops_json = json.loads("{" + ops_str + "}")
                            ops = ops_json.get("ops", [])
                            print(f"      Contains {len(ops)} operations")
                            # Show first few ops
                            for op in ops[:3]:
                                op_str = str(op)[:100]
                                print(f"        {op_str}...")
                        except json.JSONDecodeError:
                            print(f"      (Could not parse as JSON)")
                            print(f"      Preview: {ops_str[:200]}...")


def find_document_content(filepath: Path) -> None:
    """Search for the actual document content structure."""
    print("\n" + "=" * 60)
    print("DOCUMENT CONTENT SEARCH")
    print("=" * 60)

    content = filepath.read_text(encoding="utf-8", errors="replace")

    # Search for Finnish palindrome text to find where content is stored
    finnish_patterns = [
        r'saippuakauppias',  # Famous Finnish palindrome
        r'[äöÄÖ]',  # Finnish characters
        r'palindromi',
    ]

    for pat in finnish_patterns:
        matches = list(re.finditer(pat, content, re.IGNORECASE))
        if matches:
            print(f"\nPattern '{pat}' found {len(matches)} times")
            for m in matches[:5]:
                start = max(0, m.start() - 100)
                end = min(len(content), m.end() + 100)
                context = content[start:end].replace("\n", "\\n")
                print(f"  pos {m.start()}: ...{context}...")


if __name__ == "__main__":
    html_path = Path("zoho-history/2025-11-27.html")
    analyze_html(html_path)
    extract_script_data(html_path)
    find_document_content(html_path)
