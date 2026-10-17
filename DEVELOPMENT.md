# Development

Use src and the regression suite. Protected CI must pass before release.

## 1.1.0 improvement session

Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

HTML edits card fields and downloads a new version 1 input; print layout includes full field values. last_played is an ISO date, screenshot_reference is a text attachment reference, and save_catalog_id optionally points to an operator-chosen catalog record. Neither images nor saves are opened. --share-safe works with Markdown, JSON and HTML: it omits private notes, screenshot references and unsupported extension fields, reporting counts without copying omitted values. Retained location, goals and story text still need review before sharing. --include-private is incompatible with --share-safe. Default reports continue to omit private_note. Source files and existing outputs remain unchanged.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## 1.2.0 acceptance

Compare return-card snapshots after applying the selected privacy rules to both inputs.

Use `where-was-i current.json --compare previous.json --share-safe --format html --output comparison.html`. Both files must be version 1 card inputs. Comparison covers full files and cannot be combined with --game. Default comparisons omit private notes; --share-safe additionally removes screenshot references and unsupported fields from both sides, including removed and added cards. --include-private is explicit and incompatible with --share-safe. Retained goals, location and story text still need review. Changing an ID appears as removal/addition; neither input is modified.
