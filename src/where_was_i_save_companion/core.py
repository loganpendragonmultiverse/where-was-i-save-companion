from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

LIST_FIELDS = ("goals", "controls", "story_context", "loose_ends")
TEXT_FIELDS = ("id", "game", "updated", "location", "next_step")


def load_cards(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("card file must be a version 1 object")
    cards = data.get("cards")
    if not isinstance(cards, list):
        raise TypeError("cards must be a list")
    seen: set[str] = set()
    for card in cards:
        if not isinstance(card, dict):
            raise TypeError("each card must be an object")
        for field in TEXT_FIELDS:
            if not isinstance(card.get(field), str) or not card[field].strip():
                raise ValueError(f"each card requires non-empty text field: {field}")
        if card["id"] in seen:
            raise ValueError(f"duplicate card id: {card['id']}")
        seen.add(card["id"])
        for field in LIST_FIELDS:
            value = card.get(field, [])
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise TypeError(f"card {card['id']} field {field} must be a list of text")
        for field in (
            "spoiler_boundary",
            "private_note",
            "screenshot_reference",
            "save_catalog_id",
            "last_played",
        ):
            if field in card and not isinstance(card[field], str):
                raise TypeError(f"card {card['id']} field {field} must be text")
        if "last_played" in card:
            date.fromisoformat(card["last_played"])
    return data


def build_report(
    data: dict[str, Any],
    game: str | None = None,
    include_private: bool = False,
    share_safe: bool = False,
) -> dict[str, Any]:
    cards = [card.copy() for card in data["cards"] if game is None or card["game"] == game]
    if game is not None and not cards:
        raise ValueError(f"no card found for game: {game}")
    if share_safe and include_private:
        raise ValueError("share-safe cannot include private notes")
    omitted = {
        "private_notes": sum("private_note" in c for c in cards) if not include_private else 0,
        "screenshot_references": sum("screenshot_reference" in c for c in cards)
        if share_safe
        else 0,
        "unsupported_fields": 0,
    }
    if share_safe:
        allowed = set(
            TEXT_FIELDS + LIST_FIELDS + ("spoiler_boundary", "last_played", "save_catalog_id")
        )
        omitted["unsupported_fields"] = sum(
            len(set(c) - allowed - {"private_note", "screenshot_reference"}) for c in cards
        )
        cards = [{k: v for k, v in card.items() if k in allowed} for card in cards]
    elif not include_private:
        for card in cards:
            card.pop("private_note", None)
    return {
        "version": 1,
        "card_count": len(cards),
        "cards": cards,
        "share_review": {
            "share_safe": share_safe,
            "omitted": omitted,
            "note": "Review retained story, controls, goals and location text before sharing; no automatic anonymity guarantee",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Where Was I?", "", f"Return cards: **{report['card_count']}**", ""]
    lines += ["Share review: " + json.dumps(report.get("share_review", {})), ""]
    for card in report["cards"]:
        lines.extend(
            [
                f"## {card['game']}",
                "",
                f"- Updated: {card['updated']}",
                f"- Location: {card['location']}",
                f"- Next step: {card['next_step']}",
            ]
        )
        if card.get("spoiler_boundary"):
            lines.append(f"- Spoiler boundary: {card['spoiler_boundary']}")
        for key in ("last_played", "screenshot_reference", "save_catalog_id"):
            if card.get(key):
                lines.append(f"- {key.replace('_', ' ')}: {card[key]}")
        for field, heading in (
            ("goals", "Goals"),
            ("controls", "Controls"),
            ("story_context", "Story context"),
            ("loose_ends", "Loose ends"),
        ):
            if card.get(field):
                lines.extend(["", f"### {heading}", ""])
                lines.extend(f"- {item}" for item in card[field])
        if card.get("private_note"):
            lines.extend(["", "### Private note", "", card["private_note"]])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
