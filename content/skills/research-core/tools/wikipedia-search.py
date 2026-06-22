"""Wikipedia search wrapper (stub).

Usage:
    uv run --script wikipedia-search.py "<query>" [--limit N] [--lang en]

Planned: query Wikipedia (https://en.wikipedia.org and equivalents in other
languages) and emit a JSON list of {title, url, summary, lang}.

Likely future deps (to declare in a PEP-723 block when implementing):
    "wikipedia-api>=0.6"   # https://github.com/martin-majlis/Wikipedia-API (MIT)

STUB: not implemented yet.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("wikipedia-search: STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
