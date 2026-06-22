---
name: research-anki
description: Export atomic facts from a research report (produced by research-core) as Anki-importable flashcards. Use when the user mentions Anki, .apkg, flashcards, spaced repetition, or asks to make cards from research notes.
user-invocable: true
---

# Research → Anki flashcards

Extract atomic facts from a research report and emit an Anki-importable file.

## Status

Stub. The tool driver is `tools/anki-export.py` (not yet implemented). Invoke it as:

```
uv run --script tools/anki-export.py <report.md|report.mdx> [--out deck.csv]
```

`uv run --script` honors the tool's PEP-723 inline dependency block (see [PEP 723](https://peps.python.org/pep-0723/)); the current stub uses stdlib only. Card schema in `references/anki-format.md`.

## Planned behavior

**Inputs:** a research report (text or file path).

**Outputs:** an Anki-importable file. v0.1 target format: TSV/CSV (no external deps); `.apkg` via `genanki` later.

## References

- `references/anki-format.md` — Anki notetype / field schema for research cards.
