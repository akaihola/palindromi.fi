# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4",
#     "lxml",
# ]
# ///
"""Deep analysis script for Zoho Notebook HTML exports.

Exploratory marker searches, not a verified version extractor. See
docs/zoho-import.md for the later distinction between selected historical
content and the live-note snapshot in each export. The existing converter is
unsafe to import from. These diagnostics decode as UTF-8 with replacement,
so they do not preserve the investigated Windows-1252 exports exactly.
"""

import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def extract_text_from_html(html_content: str) -> str:
    """Strip tags and each text line, discarding blank lines and script/style text."""
    soup = BeautifulSoup(html_content, "lxml")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text
    text = soup.get_text(separator="\n")

    # Normalize whitespace
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        # Skip empty lines and lines that are just whitespace/nbsp
        if line and line != "\xa0":
            lines.append(line)

    return "\n".join(lines)


def find_all_json_objects(content: str) -> None:
    """Find and analyze JSON object structures in the HTML."""
    print("\n" + "=" * 60)
    print("SEARCHING FOR VERSION DATA STRUCTURES")
    print("=" * 60)

    # Look for noteVersionData or similar
    patterns_to_check = [
        r'noteVersionData\s*=\s*',
        r'versionData\s*=\s*',
        r'allVersions\s*=\s*',
        r'versionList\s*=\s*',
        r'snapshots\s*=\s*',
        r'"versions"\s*:',
        r'"noteVersions"\s*:',
        r'"contentSnapshots"\s*:',
    ]

    for pattern in patterns_to_check:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        if matches:
            print(f"\n'{pattern}' found {len(matches)} times")
            for m in matches[:2]:
                ctx = content[m.start():m.start()+500].replace("\n", "\\n")
                print(f"  pos {m.start()}: {ctx}...")


def analyze_script_tags(filepath: Path) -> None:
    """Inspect scripts over 10,000 characters containing selected text markers."""
    print("\n" + "=" * 60)
    print("DEEP SCRIPT TAG ANALYSIS")
    print("=" * 60)

    content = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(content, "lxml")

    scripts = soup.find_all("script")

    for i, script in enumerate(scripts):
        script_content = script.string or ""
        if len(script_content) > 10000:
            # Check for palindrome content
            has_naksui = "Naksui" in script_content or "naksui" in script_content.lower()
            has_oudosti = "Oudosti" in script_content or "oudosti" in script_content.lower()
            has_naatti = "Naatti" in script_content or "naatti" in script_content.lower()

            if has_naksui or has_oudosti or has_naatti:
                print(f"\nScript {i} ({len(script_content):,} chars):")
                print(f"  Contains 'Naksui': {has_naksui}")
                print(f"  Contains 'Oudosti': {has_oudosti}")
                print(f"  Contains 'Naatti': {has_naatti}")

                # Count occurrences
                naksui_count = script_content.count("Naksui") + script_content.count("naksui")
                naatti_count = script_content.count("Naatti") + script_content.count("naatti")
                print(f"  'Naksui' count: {naksui_count}")
                print(f"  'Naatti' count: {naatti_count}")

                # Look for JSON-like structures
                # Find start of potential JSON objects
                json_starts = list(re.finditer(r'(\w+)\s*=\s*\{', script_content))
                print(f"\n  Variable assignments to objects:")
                for m in json_starts[:20]:
                    var_name = m.group(1)
                    # Check if this might be interesting
                    preview = script_content[m.start():m.start()+200].replace("\n", " ")
                    if any(kw in preview.lower() for kw in ["version", "content", "note", "history"]):
                        print(f"    {var_name} = ... ({preview[:100]})")


def find_version_content_blocks(filepath: Path) -> list[tuple[int, str]]:
    """Find candidate encoded blocks in scripts containing the Oudosti marker.

    Returns (character offset within the script, decoded HTML, has_naksui,
    has_naatti) tuples. Candidates are not verified distinct document versions.

    """
    content = filepath.read_text(encoding="utf-8", errors="replace")

    print("\n" + "=" * 60)
    print("FINDING VERSION CONTENT BLOCKS")
    print("=" * 60)

    # Pattern: quoted strings containing entity-encoded HTML with palindrome content
    # The content appears to be in format: "content":"<entity-encoded-html>"
    # or as values in JSON objects

    # Inspect scripts for candidate content; version identity is not established.
    soup = BeautifulSoup(content, "lxml")
    scripts = soup.find_all("script")

    version_contents = []

    for i, script in enumerate(scripts):
        script_content = script.string or ""
        if "Oudosti" not in script_content and "oudosti" not in script_content.lower():
            continue

        print(f"\nAnalyzing Script {i} for version data...")

        # Look for patterns like "content":"<escaped-html>"
        # Probe content-like strings; only HTML entities are decoded below.

        # Pattern 1: Direct content assignments
        content_pattern = r'"content"\s*:\s*"([^"]+)"'
        content_matches = list(re.finditer(content_pattern, script_content))
        print(f"  Found {len(content_matches)} 'content' fields")

        # Pattern 2: Look for entity-encoded blocks directly
        # These start with &lt;div and contain significant content
        entity_pattern = r'"(&lt;div[^"]{5000,}?)"'
        entity_matches = list(re.finditer(entity_pattern, script_content))
        print(f"  Found {len(entity_matches)} large entity-encoded blocks")

        for j, m in enumerate(entity_matches):
            encoded = m.group(1)
            # Decode
            decoded = html.unescape(encoded)

            has_naksui = "Naksui risukasa" in decoded
            has_naatti = "Naatti aittaan" in decoded

            print(f"    Block {j}: {len(decoded):,} chars, Naksui: {has_naksui}, Naatti: {has_naatti}")
            version_contents.append((m.start(), decoded, has_naksui, has_naatti))

        # Pattern 3: Look for JSON arrays containing version objects
        versions_array_pattern = r'"versions"\s*:\s*\[(.*?)\]'
        # This might be too greedy, let's try to find version-related structures

        # Pattern 4: Look for individual snapshot/version objects
        snapshot_pattern = r'\{\s*"[^"]*snapshot[^"]*"\s*:\s*"([^"]{1000,}?)"'
        snapshot_matches = list(re.finditer(snapshot_pattern, script_content, re.IGNORECASE))
        print(f"  Found {len(snapshot_matches)} snapshot fields")

    return version_contents


def count_palindrome_markers(filepath: Path) -> None:
    """Count marker occurrences; repeated copies need not be distinct versions."""
    content = filepath.read_text(encoding="utf-8", errors="replace")

    print("\n" + "=" * 60)
    print("PALINDROME MARKER ANALYSIS")
    print("=" * 60)

    markers = [
        ("Naksui risukasa", "should be in all ~100 versions"),
        ("Naatti aittaan", "should only be in newest version"),
        ("Oudosti ksenon", "first palindrome, all versions"),
        ("Tieto mita", "another test marker"),
    ]

    for marker, desc in markers:
        count = content.count(marker)
        # Also count entity-encoded version
        encoded = html.escape(marker)
        encoded_count = content.count(encoded)
        print(f"\n'{marker}' ({desc}):")
        print(f"  Raw occurrences: {count}")
        print(f"  HTML-escaped occurrences: {encoded_count}")
        print(f"  Total: {count + encoded_count}")

    # Find unique positions
    print("\n--- All 'Naatti aittaan' positions ---")
    start = 0
    positions = []
    search_term = "Naatti aittaan"
    while True:
        pos = content.find(search_term, start)
        if pos == -1:
            break
        # Get surrounding context to understand structure
        ctx_start = max(0, pos - 200)
        ctx_end = min(len(content), pos + 200)
        context = content[ctx_start:ctx_end].replace("\n", "\\n")
        positions.append((pos, context))
        start = pos + 1

    for pos, ctx in positions:
        print(f"\nPos {pos}:")
        print(f"  ...{ctx[:300]}...")


def extract_from_large_script(filepath: Path) -> None:
    """Summarize quoted HTML candidates in scripts containing the Oudosti marker."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(content, "lxml")

    print("\n" + "=" * 60)
    print("EXTRACTING FROM LARGE SCRIPT")
    print("=" * 60)

    scripts = soup.find_all("script")

    for i, script in enumerate(scripts):
        script_content = script.string or ""
        if "Oudosti" not in script_content:
            continue

        print(f"\nFound content in Script {i} ({len(script_content):,} chars)")

        # The content appears to be stored in quoted strings
        # Let's find all quoted strings that start with <div and are large

        # First, let's understand the structure better by looking at the JSON-like data
        # Find variable assignments
        var_pattern = r'(\w+)\s*=\s*(\{|\[)'
        var_matches = list(re.finditer(var_pattern, script_content))

        print(f"\nVariable assignments found: {len(var_matches)}")

        # Try to extract as JSON
        # Look for the main data object
        note_data_pattern = r'var\s+(\w*[Nn]ote\w*)\s*=\s*'
        note_matches = list(re.finditer(note_data_pattern, script_content))
        print(f"Note-related variables: {[m.group(1) for m in note_matches]}")

        # Find all strings that look like HTML content
        html_string_pattern = r'"(&lt;div[^"]+)"'
        html_matches = list(re.finditer(html_string_pattern, script_content))
        print(f"\nHTML-encoded strings found: {len(html_matches)}")

        # Extract and analyze each
        versions_found = []
        for j, m in enumerate(html_matches):
            encoded_html = m.group(1)
            decoded = html.unescape(encoded_html)

            # Check markers
            has_old = "Naksui risukasa" in decoded
            has_new = "Naatti aittaan" in decoded

            line_count = decoded.count("<div>")
            versions_found.append({
                'index': j,
                'position': m.start(),
                'length': len(decoded),
                'has_old_marker': has_old,
                'has_new_marker': has_new,
                'div_count': line_count,
            })

        print(f"\nVersions found: {len(versions_found)}")
        print("\nVersion summary:")
        for v in versions_found:
            print(f"  {v['index']}: pos={v['position']}, len={v['length']:,}, "
                  f"old={v['has_old_marker']}, new={v['has_new_marker']}, divs={v['div_count']}")


if __name__ == "__main__":
    html_path = Path("zoho-history/2025-11-27.html")

    count_palindrome_markers(html_path)
    analyze_script_tags(html_path)
    find_all_json_objects(html_path.read_text(encoding="utf-8", errors="replace"))
    extract_from_large_script(html_path)
