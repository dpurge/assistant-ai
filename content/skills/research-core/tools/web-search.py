"""Web search wrapper (stub).

Usage:
    python web-search.py <query> [--limit N]

Planned: pass the query to an available web-search backend (Claude Code's
WebSearch tool, DuckDuckGo, SearXNG, etc.) and emit a JSON list of
{url, title, snippet}.

STUB: not implemented.
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write("web-search: STUB — not implemented yet\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
