# Where Was I? Save Companion

> ⭐ **Gold Star Project**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Save notes about where you left off in a game, and make a copy with private details removed when you want to share it.

## What you can do

- Keep local cards with progress, reminders and return-to-game notes.
- Edit cards in the browser and save them as a new file.
- Compare saved cards after applying the chosen privacy settings.


## Current release 1.2.2

The browser editor blocks duplicate card IDs before download and explains how to correct them. Required fields must remain nonblank. After correcting an ID, download the edited cards and reopen them with the CLI.

## Updates in 1.2.1

Comparisons now tell the difference between booleans and numbers, even inside nested values.

JSON true differs from 1 and false differs from 0, including inside nested metadata. Numeric 1 and 1.0 compare equally; object key order does not matter, while array order does. Existing field-presence and privacy rules still apply.

## Updates in 1.2.0

Compare two saved sets of game cards using the same privacy settings for both.

Use `where-was-i current.json --compare previous.json --share-safe --format html --output comparison.html`. Both files must be version 1 card inputs. Comparison covers full files and cannot be combined with --game. Default comparisons omit private notes; --share-safe additionally removes screenshot references and unsupported fields from both sides, including removed and added cards. --include-private is explicit and incompatible with --share-safe. Retained goals, location and story text still need review. Changing an ID appears as removal/addition; neither input is modified.

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

## Updates in 1.1.0

Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

```bash
where-was-i examples/cards.json --format html --output return-cards.html
```

HTML edits card fields and downloads a new version 1 input; print layout includes full field values. last_played is an ISO date, screenshot_reference is a text attachment reference, and save_catalog_id optionally points to an operator-chosen catalog record. Neither images nor saves are opened. --share-safe works with Markdown, JSON and HTML: it omits private notes, screenshot references and unsupported extension fields, reporting counts without copying omitted values. Retained location, goals and story text still need review before sharing. --include-private is incompatible with --share-safe. Default reports continue to omit private_note. Source files and existing outputs remain unchanged.

The local card editor requires unique card IDs before download. If an edit duplicates another card ID, correct it and download again; required fields must also remain nonblank.
