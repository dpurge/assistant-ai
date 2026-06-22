"""Generate Anki flashcards from a research report (stub).

Usage:
    python anki-export.py <report.md|report.mdx> [--out deck.csv]

Planned output: Anki-importable TSV/CSV (and later .apkg via genanki).

STUB: extraction logic and Anki schema not yet defined.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("anki-export (research): STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
