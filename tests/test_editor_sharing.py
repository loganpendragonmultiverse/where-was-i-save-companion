import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from where_was_i_save_companion.cli import main
from where_was_i_save_companion.core import build_report, load_cards, render_markdown
from where_was_i_save_companion.editor import render_html


def test_generated_editor_javascript_parses(tmp_path: Path) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("JavaScript syntax acceptance requires Node.js")
    script = re.search(r"<script>(.*?)</script>", render_html(build_report(sample())), re.S)
    assert script is not None
    path = tmp_path / "editor.js"
    path.write_text(script.group(1), encoding="utf-8")
    result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
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
