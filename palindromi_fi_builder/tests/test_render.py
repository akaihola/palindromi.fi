import re
from pathlib import Path
from typing import List

from click.testing import CliRunner

from palindromi_fi_builder.render import render


def test_render_copies_static_files(tmp_path: Path) -> None:
    (tmp_path / "database" / "palindromes").mkdir(parents=True)
    (tmp_path / "database" / "palindromes" / "a.yaml").write_text(
        "- text: Saippuakauppias\n"
        "  author: anonymous\n"
        "  translations:\n"
        "  - language: en\n"
        "    text: Soap vendor\n"
        "    author: anonymous\n"
        "  created: 2020-01-01\n"
    )

    result = CliRunner().invoke(
        render, [str(tmp_path / "database"), "-o", str(tmp_path / "html")]
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "html" / "static" / "main.css").is_file()


def test_render_writes_html_pages_with_html_links(tmp_path: Path) -> None:
    """Pages and their navigation links carry ``.html`` so hosting serves ``text/html``

    Extensionless pages made GitHub Pages respond with ``application/octet-stream``,
    which browsers download as ``<id>.bin`` when the page is tapped.

    """
    (tmp_path / "database" / "palindromes").mkdir(parents=True)
    (tmp_path / "database" / "palindromes" / "a.yaml").write_text(
        "- text: Saippuakauppias\n"
        "  author: anonymous\n"
        "  translations:\n"
        "  - language: en\n"
        "    text: Soap vendor\n"
        "    author: anonymous\n"
        "  created: 2020-01-01\n"
        "- text: Neulo taas niin saat oluen\n"
        "  author: anonymous\n"
        "  translations:\n"
        "  - language: en\n"
        "    text: Knit again and you get a beer\n"
        "    author: anonymous\n"
        "  created: 2020-01-02\n"
    )

    result = CliRunner().invoke(
        render, [str(tmp_path / "database"), "-o", str(tmp_path / "html")]
    )

    assert result.exit_code == 0, result.output
    pages = sorted(p for p in (tmp_path / "html").iterdir() if p.is_file())
    assert [p.suffix for p in pages] == [".html", ".html", ".html"]
    assert (tmp_path / "html" / "index.html") in pages
    link = re.compile(r'id="go-to-(?:previous|next)"\s+href="([^"]*)"')
    for page in pages:
        hrefs: List[str] = link.findall(page.read_text())
        assert len(hrefs) == 2
        assert all(href.endswith(".html") for href in hrefs)
