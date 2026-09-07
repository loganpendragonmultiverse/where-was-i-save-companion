# Development

Use src and the regression suite. Protected CI must pass before release.

## 1.1.0 improvement session

Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

HTML edits card fields and downloads a new version 1 input; print layout includes full field values. last_played is an ISO date, screenshot_reference is a text attachment reference, and save_catalog_id optionally points to an operator-chosen catalog record. Neither images nor saves are opened. --share-safe works with Markdown, JSON and HTML: it omits private notes, screenshot references and unsupported extension fields, reporting counts without copying omitted values. Retained location, goals and story text still need review before sharing. --include-private is incompatible with --share-safe. Default reports continue to omit private_note. Source files and existing outputs remain unchanged.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.
