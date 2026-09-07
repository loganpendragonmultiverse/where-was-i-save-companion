import json
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

from where_was_i_save_companion.cli import main
from where_was_i_save_companion.core import build_report, load_cards, render_markdown
from where_was_i_save_companion.editor import render_html


def test_generated_editor_javascript_parses(tmp_path: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("JavaScript syntax acceptance requires Node.js")

    class ScriptReader(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.in_script = False
            self.parts: list[str] = []

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            self.in_script = tag == "script" and dict(attrs).get("type", "text/javascript") in {
                "text/javascript",
                "module",
            }

        def handle_endtag(self, tag: str) -> None:
            if tag == "script":
                self.in_script = False

        def handle_data(self, data: str) -> None:
            if self.in_script:
                self.parts.append(data)

    parser = ScriptReader()
    parser.feed(render_html(build_report(sample())))
    assert parser.parts
    path = tmp_path / "editor.js"
    path.write_text("\n".join(parser.parts), encoding="utf-8")
    result = subprocess.run(
        [node, "--check", str(path)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


def sample() -> dict:
    return {
        "version": 1,
        "cards": [
            {
                "id": "a",
                "game": "Fictional",
                "updated": "2026-09-07",
                "location": "Town",
                "next_step": "Explore",
                "private_note": "PRIVATE-CANARY",
                "screenshot_reference": "PRIVATE-PATH-CANARY",
                "unknown": "EXTENSION-CANARY",
                "last_played": "2026-09-01",
                "save_catalog_id": "chosen-record",
                "goals": ["Visit library"],
            }
        ],
    }


def test_all_share_formats_omit_private_values(tmp_path: Path) -> None:
    data = sample()
    report = build_report(data, share_safe=True)
    assert report["share_review"]["omitted"] == {
        "private_notes": 1,
        "screenshot_references": 1,
        "unsupported_fields": 1,
    }
    for text in (json.dumps(report), render_markdown(report), render_html(report)):
        for secret in ("PRIVATE-CANARY", "PRIVATE-PATH-CANARY", "EXTENSION-CANARY"):
            assert secret not in text
        assert "chosen-record" in text
    assert data["cards"][0]["private_note"] == "PRIVATE-CANARY"
    source = tmp_path / "cards.json"
    source.write_text(json.dumps(data), encoding="utf-8")
    for fmt in ("json", "markdown", "html"):
        target = tmp_path / (fmt + ".txt")
        assert main([str(source), "--share-safe", "--format", fmt, "--output", str(target)]) == 0
        assert "PRIVATE-CANARY" not in target.read_text(encoding="utf-8")
    assert main([str(source), "--share-safe", "--include-private"]) == 2


def test_local_editor_reference_date_and_xss(tmp_path: Path) -> None:
    data = sample()
    data["cards"][0]["next_step"] = "</script><img src=x>"
    source = tmp_path / "cards.json"
    source.write_text(json.dumps(data), encoding="utf-8")
    report = build_report(load_cards(source), include_private=True)
    html = render_html(report)
    assert "</script><img" not in html
    assert "PRIVATE-PATH-CANARY" in html and 'src="PRIVATE-PATH-CANARY"' not in html
    assert "Print cards" in html and "Download edited cards" in html
    data["cards"][0]["last_played"] = "not a date"
    source.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        load_cards(source)
