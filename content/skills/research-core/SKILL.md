---
name: research-core
description: Generic research workflow — accepts a topic as input and produces a structured, sourced report. Pulls from web search, arXiv, RAG, and any other knowledge source available. Supports iterative refinement based on user feedback. Use whenever the user asks to research a topic, summarize a field, prepare reading notes, or write a short report. Hands off to research-web (Docusaurus page), research-anki (flashcards), or research-typst (PDF).
---

# Research core

Given a topic, produce a sourced, structured report; revise on feedback. **Output-format-agnostic** — you don't write the final file; an output skill does.

## Quick reference

```bash
# 1. local knowledge base first
uv run --script tools/rag-query.py "<topic-relevant query>"
# stdout is a JSON list. [] = no local hits → use external sources. Otherwise use the hits.

# 2. external sources, in order, until you have enough
uv run --script tools/wikipedia-search.py "<topic>"
uv run --script tools/arxiv-search.py "<topic>"
uv run --script tools/web-search.py "<topic>"   # or your host's native web-search tool
```

Read `references/report-shape.md` before writing the report. Read `references/rag.md` only if you need to understand the knowledge-base layout.

## When invoked

1. **Receive the topic.** If audience, depth, or time horizon are ambiguous, ask once.
2. **Local knowledge base first.** Run `uv run --script tools/rag-query.py "<query>"`. Parse the JSON on stdout.
   - If the JSON array is **non-empty**, those chunks are your primary input. Each chunk has `file`, `headers`, `text`, `score`, `frontmatter`. Cite them as `[local:<file>]`.
   - If the JSON array is **`[]`** (empty), there is no local content — go to step 3.
3. **External sources, in this order**, until you have enough material:
   1. **Wikipedia** — `uv run --script tools/wikipedia-search.py "<topic>"`. Cite as `[wiki:<url>]`.
   2. **arXiv** — `uv run --script tools/arxiv-search.py "<topic>"`. Cite as `[arxiv:<id>]`.
   3. **Web search** — `uv run --script tools/web-search.py "<topic>"`, or use your agent host's native web-search/web-fetch tool if it has one. Cite as `[web:<url>]`.
   4. **GitHub / Atlassian** — via the agent host's MCP tools, if connected. Cite as `[github:...]` / `[jira:...]`.
4. **Write the report** following `references/report-shape.md` (load it first if you haven't). Use the citation markers above in the references list.
5. **Hand off to the output skill the user named:**
   - default: `research-web` (Docusaurus MDX page).
   - `research-anki` for flashcards.
   - `research-typst` for PDF source.
6. **Revise on feedback.** Track what is already cited, what was accepted, what was rejected. See `references/revision.md`.

## Output

The report itself is structured content (text). You do not write the final file — the output skill does. After hand-off, reply with a short confirmation naming the topic and the file written.

## Constraints

- **Cite everything.** A claim without a citation is a draft note; mark it as such.
- **Prefer primary sources.** Encyclopedia entries are starting points, not citations.
- **Be honest about uncertainty.** "I do not know based on the current evidence" is an acceptable answer.
- **Recency matters.** Note publication dates; flag claims that may be stale.

## References

- `references/rag.md` — local knowledge-base layout, chunking rules, index format.
- `references/sources.md` — knowledge-source catalog with selection guidance.
- `references/report-shape.md` — abstract report structure, citation format.
- `references/revision.md` — iterative refinement protocol.

## Sister skills

- `research-web` — render report as a Docusaurus MDX page. **Default output target.** The output filename is an argument the caller supplies.
- `research-anki` — export atomic facts as Anki flashcards (stub).
- `research-typst` — render report as a Typst `.typ` source for PDF compilation (stub).

## Tools

Invoke every tool via `uv run --script` so its [PEP 723](https://peps.python.org/pep-0723/) inline deps are resolved into uv's cache on first run.

**Real (with deps):**

- `tools/rag-index.py` — build the FAISS index from `$ASSISTANT_KNOWLEDGE_DIR` (default `~/.assistant/knowledge/`). Deps: `fastembed`, `faiss-cpu`, `pyyaml`, `numpy`. See `references/rag.md`.
- `tools/rag-query.py` — search the index. Same deps. Exit `0` if hits ≥ `--min-score`; exit `1` if not (chain into fallback via shell `||`).

**Real (stdlib only, key-free public APIs):**

- `tools/wikipedia-search.py` — MediaWiki search + REST summary → `[{title,url,summary,lang}]`.
- `tools/arxiv-search.py` — arXiv Atom API → `[{id,title,authors,abstract,published,pdf_url}]`.
- `tools/web-search.py` — DuckDuckGo HTML (best-effort, no key) → `[{url,title,snippet}]`; returns `[]` if blocked.
