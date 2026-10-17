"""Generate small synthetic browser fixtures with the installed package."""

import json
import sys
from pathlib import Path

from where_was_i_save_companion.comparison import compare_snapshots, comparison_html
from where_was_i_save_companion.core import build_report
from where_was_i_save_companion.editor import render_html

root = Path(sys.argv[1]).resolve()
root.mkdir(parents=True, exist_ok=True)
data = {
    "version": 1,
    "cards": [
        {
            "id": "one",
            "game": "Old Game",
            "updated": "2026-10-17",
            "location": "Town",
            "next_step": "Climb",
            "goals": ["First", "Second"],
            "private_note": "PRIVATE-NOTE-CANARY",
            "screenshot_reference": "PRIVATE-REF-CANARY",
            "extension": {"value": "PRIVATE-EXT-CANARY"},
        }
    ],
}
(root / "original-cards.json").write_text(json.dumps(data), encoding="utf-8")
for variant, options in [
    ("normal", {}),
    ("share", {"share_safe": True}),
    ("private", {"include_private": True}),
    ("empty", {}),
]:
    report = build_report(data if variant != "empty" else {"version": 1, "cards": []}, **options)
    (root / f"where-{variant}.html").write_text(render_html(report), encoding="utf-8")
report = build_report(data)
report["comparison"] = compare_snapshots([], report["cards"])
html = render_html(report).replace("</html>", comparison_html(report["comparison"]) + "</html>")
(root / "where-comparison.html").write_text(html, encoding="utf-8")
