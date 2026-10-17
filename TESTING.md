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

## 1.3.0 acceptance

- Create, duplicate and remove cards in the local editor, including an empty collection, with unique IDs and required-field guards.
- Update screen/print headings during game edits and preserve actual line-separated list fields.
- Warn before leaving unsaved edits without storing notes in the browser; downloading saves a new file and printing keeps the warning active.
- Preserve privacy modes during card authoring and hide stale comparison evidence after edits.

Run the complete source gates and installed built-wheel tests. Run `tests/browser_fixtures.py` with the installed package and a fresh private output directory, then `tests/browser_acceptance.mjs` in Chromium, Firefox and WebKit. These fixtures are synthetic. Protected CI and independent exact-head review remain required before release.

With Playwright and its three browser engines available, use:

```bash
python tests/browser_fixtures.py /tmp/fresh-browser-fixtures
FIXTURE_DIR=/tmp/fresh-browser-fixtures node tests/browser_acceptance.mjs
```

For an external Playwright installation, set `PLAYWRIGHT_MODULE` to its absolute `index.mjs` path. Browser JSON receipts and downloaded test artifacts stay in the fixture directory. Use a new directory for another run so output protection remains exercised. Reimport the downloaded JSON through `where-was-i` and verify privacy omission and card IDs.
