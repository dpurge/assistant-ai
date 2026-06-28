# /// script
# requires-python = ">=3.11"
# ///
"""Web search via DuckDuckGo's HTML endpoint (key-free).

Usage:
    uv run --script web-search.py "<query>" [--limit N]

Emits a JSON list of {url, title, snippet} on stdout. No API key. This scrapes
html.duckduckgo.com, so it is best-effort: layout changes or rate limits can
yield []. Network I/O — verified by live run, not unit tests. Always exits 0;
on any failure it prints [] (with a note on stderr) so callers degrade
gracefully.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; assistant-ai-research/0.1)"
TIMEOUT = 10
ENDPOINT = "https://html.duckduckgo.com/html/"


def _unwrap(href: str) -> str:
    """DuckDuckGo wraps result links as /l/?uddg=<encoded-url>; unwrap them."""
    if "uddg=" in href:
        qs = urllib.parse.urlparse(href).query
        u = urllib.parse.parse_qs(qs).get("uddg")
        if u:
            return u[0]
    return href


class _Results(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict] = []
        self._mode: str | None = None  # "title" | "snippet"
        self._href = ""
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        cls = a.get("class") or ""
        if tag == "a" and "result__a" in cls:
            self._mode = "title"
            self._href = _unwrap(a.get("href") or "")
            self._buf = []
        elif "result__snippet" in cls:
            self._mode = "snippet"
            self._buf = []

    def handle_data(self, data: str) -> None:
        if self._mode:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._mode == "title" and tag == "a":
            self.results.append({"url": self._href, "title": "".join(self._buf).strip(), "snippet": ""})
            self._mode = None
        elif self._mode == "snippet":
            text = "".join(self._buf).strip()
            if self.results and not self.results[-1]["snippet"]:
                self.results[-1]["snippet"] = text
            self._mode = None


def search(query: str, limit: int) -> list[dict]:
    data = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request(ENDPOINT, data=data, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        html = resp.read().decode("utf-8", "replace")
    parser = _Results()
    parser.feed(html)
    return [r for r in parser.results if r["url"]][:limit]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()

    try:
        results = search(args.query, args.limit)
    except Exception as e:  # network/parse failure → graceful empty
        sys.stderr.write(f"web-search: {e}\n")
        results = []

    print(json.dumps(results, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
