# Where Was I? Save Companion

[![CI](https://github.com/loganpendragonmultiverse/where-was-i-save-companion/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/where-was-i-save-companion/actions/workflows/ci.yml)

Where Was I? Save Companion turns a small local JSON file into private return-to-game cards. Each card keeps the practical context that save files usually omit: current location, immediate goals, controls worth remembering, story context, loose ends, and the next action.

## Three-minute start

```bash
python -m pip install .
where-was-i examples/cards.json
where-was-i examples/cards.json --game "North Road" --format json
```

Cards can carry a spoiler boundary and a private note. Markdown reports omit private notes unless `--include-private` is explicitly supplied. Existing output files are never replaced.

The tool does not inspect game saves, synchronize accounts, infer story state, or verify that a note remains accurate. The JSON file is the source of truth and may contain spoilers or personal notes, so store and share it accordingly. Requires Python 3.10 or newer.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.1.0: reviewed improvements

Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

```bash
where-was-i examples/cards.json --format html --output return-cards.html
```

HTML edits card fields and downloads a new version 1 input; print layout includes full field values. last_played is an ISO date, screenshot_reference is a text attachment reference, and save_catalog_id optionally points to an operator-chosen catalog record. Neither images nor saves are opened. --share-safe works with Markdown, JSON and HTML: it omits private notes, screenshot references and unsupported extension fields, reporting counts without copying omitted values. Retained location, goals and story text still need review before sharing. --include-private is incompatible with --share-safe. Default reports continue to omit private_note. Source files and existing outputs remain unchanged.
