"""Generate a Typst source file (.typ) from a research report (stub).

Usage:
    python typst-export.py <report.md|report.mdx> [--out report.typ]

Pair the output with `typst compile report.typ report.pdf` to produce a PDF.

STUB: report -> Typst conversion logic not yet defined.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("typst-export (research): STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
