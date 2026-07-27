import json
from pathlib import Path

import pytest

from where_was_i_save_companion.cli import main
from where_was_i_save_companion.core import build_report, load_cards, render_markdown


def cards() -> dict[str, object]:
    return {
        "version": 1,
        "cards": [
            {
                "id": "north",
                "game": "North Road",
                "updated": "2026-07-26",
                "location": "Observatory",
                "goals": ["Repair relay"],
                "controls": ["Open tool wheel"],
                "story_context": ["Signal disabled"],
                "loose_ends": ["Return notes"],
                "next_step": "Take the east stair",
                "spoiler_boundary": "Observatory",
                "private_note": "Quiet route",
            }
        ],
    }


def write_cards(path: Path, data: dict[str, object] | None = None) -> None:
    path.write_text(json.dumps(data or cards()), encoding="utf-8")


def test_private_notes_and_rendering() -> None:
    public = build_report(cards())
    assert "private_note" not in public["cards"][0]
    private = build_report(cards(), "North Road", True)
    assert private["cards"][0]["private_note"] == "Quiet route"
    assert "Story context" in render_markdown(private)
    with pytest.raises(ValueError, match="no card"):
        build_report(cards(), "Missing")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda data: data.update(version=2), "version 1"),
        (lambda data: data.update(cards="bad"), "cards must"),
        (lambda data: data["cards"].append("bad"), "must be an object"),
        (lambda data: data["cards"][0].update(game=""), "field: game"),
        (lambda data: data["cards"].append(data["cards"][0].copy()), "duplicate"),
        (lambda data: data["cards"][0].update(goals="bad"), "list of text"),
        (lambda data: data["cards"][0].update(private_note=4), "must be text"),
    ],
)
def test_validation(tmp_path: Path, change: object, message: str) -> None:
    data = cards()
    change(data)  # type: ignore[operator]
    path = tmp_path / "cards.json"
    write_cards(path, data)
    with pytest.raises((TypeError, ValueError), match=message):
        load_cards(path)


def test_cli_json_and_safe_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "cards.json"
    write_cards(path)
    assert main([str(path), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["card_count"] == 1
    output = tmp_path / "card.md"
    assert main([str(path), "--output", str(output)]) == 0
    assert main([str(path), "--output", str(output)]) == 2
