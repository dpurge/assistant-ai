# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastembed>=0.4",
#   "faiss-cpu>=1.8",
#   "pyyaml>=6",
#   "numpy>=1.26",
# ]
# ///
"""Build a FAISS index from markdown files under the knowledge directory.

Usage:
    uv run --script rag-index.py [--knowledge-dir PATH] [--model NAME]

Defaults:
    --knowledge-dir   $ASSISTANT_KNOWLEDGE_DIR or ~/.assistant/knowledge/
    --model           $ASSISTANT_RAG_MODEL or intfloat/multilingual-e5-small

Markdown files are split into chunks at H2 (fallback H1; whole file if neither
present). Subheaders (H3+) stay inside their parent chunk. Each chunk inherits
the file's YAML frontmatter; the relative file path and header breadcrumb are
preserved as context.

Artifacts written to <knowledge-dir>/.index/:
    index.faiss     FAISS IndexFlatIP over L2-normalized embeddings (cosine sim)
    chunks.jsonl    one JSON per chunk: {id, file, headers, frontmatter, text}
    manifest.json   {model, dim, count, built_at, knowledge_dir}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import faiss
import numpy as np
import yaml
from fastembed import TextEmbedding

DEFAULT_KNOWLEDGE_DIR = Path.home() / ".assistant" / "knowledge"
DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)
HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def split_frontmatter(content: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}, content
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            fm = {}
    except yaml.YAMLError:
        fm = {}
    return fm, content[m.end():]


def parse_chunks(rel_path: str, content: str) -> list[dict]:
    fm, body = split_frontmatter(content)
    lines = body.split("\n")

    headers: list[tuple[int, str, int]] = []
    for i, line in enumerate(lines):
        m = HEADER_RE.match(line)
        if m:
            headers.append((len(m.group(1)), m.group(2).strip(), i))

    levels = {h[0] for h in headers}
    if 2 in levels:
        split_level = 2
    elif 1 in levels:
        split_level = 1
    else:
        text = body.strip()
        return [{"file": rel_path, "headers": [], "frontmatter": fm, "text": text}] if text else []

    split_points = [h for h in headers if h[0] == split_level]

    def breadcrumb_at(line_idx: int, include_self: str | None = None) -> list[str]:
        stack: list[tuple[int, str]] = []
        for level, title, idx in headers:
            if idx >= line_idx:
                break
            if level >= split_level:
                continue
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
        crumb = [t for _, t in stack]
        if include_self is not None:
            crumb.append(include_self)
        return crumb

    chunks: list[dict] = []

    first_split = split_points[0][2]
    preamble = "\n".join(lines[:first_split]).strip()
    if preamble:
        chunks.append({
            "file": rel_path,
            "headers": breadcrumb_at(first_split),
            "frontmatter": fm,
            "text": preamble,
        })

    for i, (_level, title, line_idx) in enumerate(split_points):
        next_idx = split_points[i + 1][2] if i + 1 < len(split_points) else len(lines)
        text = "\n".join(lines[line_idx:next_idx]).strip()
        if not text:
            continue
        chunks.append({
            "file": rel_path,
            "headers": breadcrumb_at(line_idx, include_self=title),
            "frontmatter": fm,
            "text": text,
        })

    return chunks


def text_for_embedding(chunk: dict) -> str:
    crumb = " > ".join(chunk["headers"]) if chunk["headers"] else "(no header)"
    return f"Source: {chunk['file']}\nSection: {crumb}\n\n{chunk['text']}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path(os.environ.get("ASSISTANT_KNOWLEDGE_DIR", str(DEFAULT_KNOWLEDGE_DIR))),
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("ASSISTANT_RAG_MODEL", DEFAULT_MODEL),
    )
    args = parser.parse_args()

    knowledge_dir: Path = args.knowledge_dir.expanduser()
    if not knowledge_dir.exists():
        sys.stderr.write(f"knowledge dir does not exist: {knowledge_dir}\n")
        return 1

    index_dir = knowledge_dir / ".index"
    index_dir.mkdir(exist_ok=True)

    md_files: list[Path] = []
    for p in sorted(knowledge_dir.rglob("*.md")):
        rel_parts = p.relative_to(knowledge_dir).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        md_files.append(p)

    if not md_files:
        sys.stderr.write(f"no markdown files under {knowledge_dir}\n")
        return 1

    print(f"scanning {len(md_files)} file(s) under {knowledge_dir}")

    all_chunks: list[dict] = []
    for md in md_files:
        rel = md.relative_to(knowledge_dir).as_posix()
        try:
            content = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            sys.stderr.write(f"  skipping (not UTF-8): {rel}\n")
            continue
        chunks = parse_chunks(rel, content)
        all_chunks.extend(chunks)
        print(f"  {rel}: {len(chunks)} chunk(s)")

    if not all_chunks:
        sys.stderr.write("no chunks extracted\n")
        return 1

    print(f"embedding {len(all_chunks)} chunk(s) with {args.model} ...")
    model = TextEmbedding(model_name=args.model)
    texts = [text_for_embedding(c) for c in all_chunks]
    vecs = np.array(list(model.embed(texts)), dtype=np.float32)
    faiss.normalize_L2(vecs)
    dim = int(vecs.shape[1])

    index = faiss.IndexFlatIP(dim)
    index.add(vecs)

    faiss.write_index(index, str(index_dir / "index.faiss"))
    with (index_dir / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for i, c in enumerate(all_chunks):
            f.write(json.dumps({"id": i, **c}, ensure_ascii=False) + "\n")
    manifest = {
        "model": args.model,
        "dim": dim,
        "count": len(all_chunks),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "knowledge_dir": str(knowledge_dir),
    }
    (index_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"built {index_dir.relative_to(knowledge_dir.parent)}/: {len(all_chunks)} chunks, dim={dim}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
