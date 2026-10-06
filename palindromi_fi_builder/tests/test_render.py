from pathlib import Path

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
