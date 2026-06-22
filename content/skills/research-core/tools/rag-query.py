# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastembed>=0.4",
#   "faiss-cpu>=1.8",
#   "numpy>=1.26",
# ]
# ///
"""Query the FAISS index built by rag-index.py and return matching chunks.

Usage:
    uv run --script rag-query.py "<query>" [--top-k N] [--min-score F] [--tag TAG ...] [--knowledge-dir PATH]

Defaults:
    --knowledge-dir   $ASSISTANT_KNOWLEDGE_DIR or ~/.assistant/knowledge/
    --top-k           5
    --min-score       0.30

Output: JSON list on stdout, each element {id, file, headers, frontmatter, text, score}.

Exit code:
    0 if any hits returned (score >= --min-score after tag filtering)
    1 if no hits (use to branch into external fallback, e.g.
       `uv run --script rag-query.py "..." || uv run --script wikipedia-search.py "..."`)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

DEFAULT_KNOWLEDGE_DIR = Path.home() / ".assistant" / "knowledge"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path(os.environ.get("ASSISTANT_KNOWLEDGE_DIR", str(DEFAULT_KNOWLEDGE_DIR))),
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--min-score", type=float, default=0.30)
    parser.add_argument("--tag", action="append", default=[])
    args = parser.parse_args()

    knowledge_dir: Path = args.knowledge_dir.expanduser()
    index_dir = knowledge_dir / ".index"
    if not (index_dir / "index.faiss").exists():
        sys.stderr.write(f"no index at {index_dir} — run rag-index.py first\n")
        return 1

    manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
    model_name = manifest["model"]

    chunks: list[dict] = []
    with (index_dir / "chunks.jsonl").open("r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    if not chunks:
        return 1

    model = TextEmbedding(model_name=model_name)
    q_vec = np.array(list(model.embed([args.query])), dtype=np.float32)
    faiss.normalize_L2(q_vec)

    index = faiss.read_index(str(index_dir / "index.faiss"))
    # Search wider when tag-filtering so we still get top-k after filter.
    search_k = max(args.top_k * 4, args.top_k) if args.tag else args.top_k
    search_k = min(search_k, len(chunks))
    scores, ids = index.search(q_vec, search_k)

    results: list[dict] = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0 or score < args.min_score:
            continue
        chunk = chunks[idx]
        if args.tag:
            chunk_tags = set(chunk.get("frontmatter", {}).get("tags", []) or [])
            if not all(t in chunk_tags for t in args.tag):
                continue
        results.append({**chunk, "score": float(score)})
        if len(results) >= args.top_k:
            break

    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
