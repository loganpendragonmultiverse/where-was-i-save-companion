# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.

## 1.2.0 acceptance

Compare return-card snapshots after applying the selected privacy rules to both inputs.

Verify Show added, removed and changed cards by stable ID with unchanged IDs; Apply private-note omission and share-safe filtering before generating any diff evidence; Keep comparison reports local, deterministic and HTML-escaped. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.2.1 acceptance

Report boolean-to-number changes accurately in JSON comparison evidence.

Verify Distinguish JSON booleans from numbers recursively in objects and arrays; Retain numeric equality for 1 and 1.0, object key-order independence and list order; Add regressions against the public comparison entry point. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.2.2 editor acceptance

Change the second card ID to match the first: download must be blocked with a useful message. Blank required fields must still block download. Correct the ID, download the edited JSON, and reimport it through the CLI. IDs use the same exact-text uniqueness rule as the CLI; valid unique ID edits remain supported.
