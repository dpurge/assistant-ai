# /// script
# requires-python = ">=3.11"
# ///
"""Wikipedia search.

Usage:
    uv run --script wikipedia-search.py "<query>" [--limit N] [--lang en]

Queries the MediaWiki search API and the REST summary endpoint, emitting a JSON
list of {title, url, summary, lang} on stdout. Network I/O — verified by live
run, not unit tests. Always exits 0; on any failure it prints [] (with a note on
stderr) so callers degrade gracefully.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

UA = "assistant-ai-research/0.1 (https://github.com/; contact: local)"
TIMEOUT = 10


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search(query: str, limit: int, lang: str) -> list[dict]:
    api = f"https://{lang}.wikipedia.org/w/api.php"
    params = urllib.parse.urlencode(
        {"action": "query", "list": "search", "srsearch": query, "srlimit": limit, "format": "json"}
    )
    hits = _get_json(f"{api}?{params}").get("query", {}).get("search", [])

    out: list[dict] = []
    for hit in hits[:limit]:
        title = hit.get("title", "")
        try:
            rest = _get_json(
                f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/"
                + urllib.parse.quote(title.replace(" ", "_"), safe="")
            )
            summary = rest.get("extract", "")
        except Exception:
            summary = ""  # fall back to no summary; the search hit is still useful
        out.append(
            {
                "title": title,
                "url": f"https://{lang}.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                "summary": summary,
                "lang": lang,
            }
        )
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--lang", default="en")
    args = p.parse_args()

    try:
        results = search(args.query, args.limit, args.lang)
    except Exception as e:  # network/parse failure → graceful empty
        sys.stderr.write(f"wikipedia-search: {e}\n")
        results = []

    print(json.dumps(results, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
