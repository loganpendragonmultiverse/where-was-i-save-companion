# Changelog

## 1.2.2 - 2026-10-17

- Block edited-card downloads with duplicate IDs and show how to correct them.
- Exercise editor input and download events, then reimport the corrected export.

## 1.2.1 - 2026-10-17

- Distinguish JSON booleans from numbers recursively in objects and arrays
- Retain numeric equality for 1 and 1.0, object key-order independence and list order
- Add regressions against the public comparison entry point

## 1.2.0 - 2026-10-17

- Show added, removed and changed cards by stable ID with unchanged IDs
- Apply private-note omission and share-safe filtering before generating any diff evidence
- Keep comparison reports local, deterministic and HTML-escaped

## 1.1.0 - 2026-09-07

- Add editable printable return-to-game cards, last-played and screenshot references, and explicit share-safe exports with omission previews.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.0.0 - 2026-07-26

- Added validated, portable return-to-game cards.
- Added game filtering and Markdown or JSON reports.
- Added opt-in private-note rendering and safe output handling.
