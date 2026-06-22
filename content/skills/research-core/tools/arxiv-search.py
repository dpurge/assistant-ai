"""arXiv search wrapper (stub).

Usage:
    python arxiv-search.py <query> [--limit N] [--category cs.LG]

Planned: query arXiv's public API (https://arxiv.org/help/api) and emit
a JSON list of {id, title, authors, abstract, published, pdf_url}.

STUB: not implemented.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("arxiv-search: STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
