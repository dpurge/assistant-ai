# Local RAG (knowledge base)

`research-core` consults a local knowledge base **first** and falls back to external sources only when the local store has nothing relevant. The store lives at `~/.assistant/knowledge/` by default; override via `$ASSISTANT_KNOWLEDGE_DIR`.

## Directory layout

```
~/.assistant/knowledge/
├── biology/
│   ├── photosynthesis.md
│   └── neurons.md
├── cloud/
│   └── kubernetes-basics.md
├── personal-notes/
│   └── 2026-06-22-react-hooks.md
└── .index/                              # auto-managed by rag-index.py
    ├── index.faiss
    ├── chunks.jsonl
    └── manifest.json
```

Organize the subdirectory tree however you like — the indexer walks it recursively and preserves each file's path **relative to the knowledge root** as chunk metadata. So `cloud/kubernetes-basics.md` chunks know they're in `cloud/`, and a search for "kubernetes networking" can surface them specifically.

## Markdown file format

Each file is plain markdown with optional YAML frontmatter at the top:

```markdown
---
title: Photosynthesis
source: https://en.wikipedia.org/wiki/Photosynthesis
tags: [biology, plants]
date: 2026-06-22
language: en
---

# Photosynthesis

Intro paragraph (becomes the preamble chunk).

## Light-dependent reactions

Content for this chunk.

### ATP synthesis

Subheaders nest inside their parent chunk — they don't split further.

## Calvin cycle

Content for the Calvin-cycle chunk.
```

## Chunking rules

- Files are split at **H2** by default.
- If a file has no H2, fall back to **H1**. If neither, the whole body (after frontmatter) is one chunk.
- Subheaders (H3, H4, …) **stay inside the parent H2 chunk** — they don't split further.
- Content before the first split-level header becomes a **preamble chunk**.
- Each chunk inherits the file's YAML frontmatter as metadata.

## Per-chunk metadata

| Field | Type | Meaning |
|---|---|---|
| `file` | string | path relative to knowledge dir, e.g. `biology/photosynthesis.md` |
| `headers` | list of strings | breadcrumb from H1 (if any) down to the chunk's split-level header |
| `frontmatter` | dict | the file's YAML frontmatter, inherited |
| `text` | string | the raw chunk text (markdown) |

When indexing, the embedder sees:

```
Source: biology/photosynthesis.md
Section: Photosynthesis > Light-dependent reactions

## Light-dependent reactions

(actual chunk body)
```

So the embedding captures both location semantics and content.

## Index

The indexer (`tools/rag-index.py`) writes three artifacts under `<knowledge-dir>/.index/`:

- `index.faiss` — FAISS `IndexFlatIP` over L2-normalized vectors (cosine similarity).
- `chunks.jsonl` — one JSON record per chunk.
- `manifest.json` — `{model, dim, count, built_at, knowledge_dir}`.

Rebuild from scratch whenever you change knowledge files:

```
uv run --script tools/rag-index.py
```

## Query

```
uv run --script tools/rag-query.py "<query>" [--top-k 5] [--min-score 0.30] [--tag TAG]
```

- Returns top-k chunks as JSON on stdout (with `score` field).
- Exit code **0** if hits ≥ `--min-score`, **1** if not. Chain into fallback sources with shell `||`:

```
uv run --script tools/rag-query.py "kubernetes pod networking" \
  || uv run --script tools/wikipedia-search.py "kubernetes pod networking"
```

- `--tag` filters chunks whose frontmatter `tags` list contains that tag. Multiple `--tag` flags are AND-ed.

## Embedding model

Default: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (~225 MB, dim 384, multilingual incl. Polish). The exact model is fixed once an index is built (recorded in `manifest.json`) — `rag-query.py` uses whatever model the existing index was built with so query embeddings match. To switch models, override at index time via `--model` or `$ASSISTANT_RAG_MODEL` and rebuild. Any model fastembed supports (see `fastembed.TextEmbedding.list_supported_models()`) works.

## When the local store is empty / missing

The indexer exits non-zero if the knowledge dir doesn't exist or has no markdown files. The searcher exits non-zero if no `.index/` is present. Both cases mean the caller should fall straight through to external sources (Wikipedia, arXiv, web).
