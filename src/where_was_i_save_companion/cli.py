from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .comparison import compare_snapshots, comparison_html, comparison_markdown
from .core import build_report, load_cards, render_markdown
from .editor import render_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render private return-to-game cards.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--game")
    parser.add_argument("--include-private", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json", "html"), default="markdown")
    parser.add_argument("--share-safe", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--compare", type=Path, help="Previous card input; apply privacy rules before comparison"
    )
    args = parser.parse_args(argv)
    try:
        current = load_cards(args.input)
        if args.compare and args.game is not None:
            raise ValueError("snapshot comparison requires full card files without --game")
        report = build_report(current, args.game, args.include_private, args.share_safe)
        if args.compare:
            previous = build_report(
                load_cards(args.compare), None, args.include_private, args.share_safe
            )
            report["comparison"] = compare_snapshots(previous["cards"], report["cards"])
        rendered = (
            json.dumps(report, indent=2, ensure_ascii=False) + "\n"
            if args.format == "json"
            else render_markdown(report)
        )
        if args.format == "html":
            rendered = render_html(report)
        if args.compare and args.format == "markdown":
            rendered += comparison_markdown(report["comparison"])
        elif args.compare and args.format == "html":
            rendered = rendered.replace(
                "</html>", comparison_html(report["comparison"]) + "</html>"
            )
        if args.output:
            if args.output.exists():
                raise ValueError(f"output already exists: {args.output}")
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
