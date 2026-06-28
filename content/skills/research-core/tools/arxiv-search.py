# /// script
# requires-python = ">=3.11"
# ///
"""arXiv search.

Usage:
    uv run --script arxiv-search.py "<query>" [--limit N] [--category cs.LG]

Queries arXiv's public Atom API (https://arxiv.org/help/api) and emits a JSON
list of {id, title, authors, abstract, published, pdf_url} on stdout. Network
I/O — verified by live run, not unit tests. Always exits 0; on any failure it
prints [] (with a note on stderr) so callers degrade gracefully.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "assistant-ai-research/0.1 (local)"
TIMEOUT = 10
ATOM = "{http://www.w3.org/2005/Atom}"


def search(query: str, limit: int, category: str | None) -> list[dict]:
    q = f"all:{query}"
    if category:
        q = f"({q}) AND cat:{category}"
    params = urllib.parse.urlencode(
        {"search_query": q, "start": 0, "max_results": limit}
    )
    req = urllib.request.Request(
        f"http://export.arxiv.org/api/query?{params}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        root = ET.fromstring(resp.read())

    out: list[dict] = []
    for entry in root.findall(f"{ATOM}entry"):
        abs_url = (entry.findtext(f"{ATOM}id") or "").strip()
        arxiv_id = abs_url.rsplit("/abs/", 1)[-1] if "/abs/" in abs_url else abs_url
        pdf_url = ""
        for link in entry.findall(f"{ATOM}link"):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
        authors = [
            (a.findtext(f"{ATOM}name") or "").strip() for a in entry.findall(f"{ATOM}author")
        ]
        out.append(
            {
                "id": arxiv_id,
                "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
                "authors": [a for a in authors if a],
                "abstract": " ".join((entry.findtext(f"{ATOM}summary") or "").split()),
                "published": (entry.findtext(f"{ATOM}published") or "").strip(),
                "pdf_url": pdf_url,
            }
        )
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--category", default=None)
    args = p.parse_args()

    try:
        results = search(args.query, args.limit, args.category)
    except Exception as e:  # network/parse failure → graceful empty
        sys.stderr.write(f"arxiv-search: {e}\n")
        results = []

    print(json.dumps(results, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
