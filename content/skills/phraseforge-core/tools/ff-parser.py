"""Parse a *.ff PhraseForge source file and emit structured data.

Usage:
    python ff-parser.py <path/to/source.ff>

Planned output: JSON on stdout with keys {texts, vocabulary, metadata}.

STUB: input format and parsing logic not yet defined.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("ff-parser: STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
