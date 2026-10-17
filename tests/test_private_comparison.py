import json
from pathlib import Path

from where_was_i_save_companion.cli import main
from where_was_i_save_companion.comparison import compare_snapshots


def card(identity, **values):
    return {
        "id": identity,
        "game": "Game",
        "updated": "2026-10-17",
        "location": "Tower",
        "next_step": "Climb",
        **values,
    }


def test_comparison_privacy_precedes_added_removed_and_changed(tmp_path: Path, capsys):
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    before.write_text(
        json.dumps(
            {
                "version": 1,
                "cards": [
                    card(
                        "a",
                        private_note="SECRET-OLD",
                        screenshot_reference="SECRET-SCREEN",
                        extension="SECRET-EXT",
                    ),
                    card("removed", private_note="SECRET-REMOVED"),
                ],
            }
        )
    )
    after.write_text(
        json.dumps(
            {
                "version": 1,
                "cards": [
                    card("a", location="Ridge", private_note="SECRET-NEW"),
                    card("added", private_note="SECRET-ADDED"),
                ],
            }
        )
    )
    for fmt in ["json", "markdown", "html"]:
        assert main([str(after), "--compare", str(before), "--share-safe", "--format", fmt]) == 0
        result = capsys.readouterr().out
        assert "SECRET-" not in result
        assert "comparison" in result.lower() and "Ridge" in result
    assert (
        main([str(after), "--compare", str(before), "--include-private", "--format", "json"]) == 0
    )
    assert "SECRET-OLD" in capsys.readouterr().out
    assert main([str(after), "--compare", str(before), "--game", "Game"]) == 2
    assert main([str(after), "--compare", str(before), "--share-safe", "--include-private"]) == 2


def test_unchanged_and_html_escaping(tmp_path: Path, capsys):
    assert compare_snapshots([card("a")], [card("a")])["unchanged_ids"] == ["a"]
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(
        json.dumps({"version": 1, "cards": [card("a", next_step="</script><img src=x>")]})
    )
    new.write_text(json.dumps({"version": 1, "cards": [card("a")]}))
    assert main([str(new), "--compare", str(old), "--format", "html"]) == 0
    assert "<img src=x>" not in capsys.readouterr().out
