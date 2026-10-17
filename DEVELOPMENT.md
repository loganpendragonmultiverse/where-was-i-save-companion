# Development

Use src and the regression suite. Protected CI must pass before release.

## 1.1.0 improvement session

Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

HTML edits card fields and downloads a new version 1 input; print layout includes full field values. last_played is an ISO date, screenshot_reference is a text attachment reference, and save_catalog_id optionally points to an operator-chosen catalog record. Neither images nor saves are opened. --share-safe works with Markdown, JSON and HTML: it omits private notes, screenshot references and unsupported extension fields, reporting counts without copying omitted values. Retained location, goals and story text still need review before sharing. --include-private is incompatible with --share-safe. Default reports continue to omit private_note. Source files and existing outputs remain unchanged.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## 1.2.0 acceptance

Compare return-card snapshots after applying the selected privacy rules to both inputs.

Use `where-was-i current.json --compare previous.json --share-safe --format html --output comparison.html`. Both files must be version 1 card inputs. Comparison covers full files and cannot be combined with --game. Default comparisons omit private notes; --share-safe additionally removes screenshot references and unsupported fields from both sides, including removed and added cards. --include-private is explicit and incompatible with --share-safe. Retained goals, location and story text still need review. Changing an ID appears as removal/addition; neither input is modified.

## 1.2.1 acceptance

Report boolean-to-number changes accurately in JSON comparison evidence.

JSON true differs from 1 and false differs from 0, including inside nested metadata. Numeric 1 and 1.0 compare equally; object key order does not matter, while array order does. Existing field-presence and privacy rules still apply.

## Gold Star review — October 17, 2026

Save notes about where you left off in a game, and make a copy with private details removed when you want to share it.

Logan considers this project complete. Continue fixes and maintenance, and consider good new ideas. The catalog records the reviewed release.

Definition: https://www.loganpendragonforge.com/open-source/?gold=1

## 1.2.2 editor acceptance

Change the second card ID to match the first: download must be blocked with a useful message. Blank required fields must still block download. Correct the ID, download the edited JSON, and reimport it through the CLI. IDs use the same exact-text uniqueness rule as the CLI; valid unique ID edits remain supported.
