# Research sources

Catalog of knowledge sources to consider, and when each is appropriate.

## Web search

**Use for:** current events, broad topics, programming docs, blog posts, recent product announcements, regulatory changes.

**Available via:** the agent host's native tools (Claude Code's `WebSearch`, `WebFetch`) or `tools/web-search.py` once implemented.

## arXiv

**Use for:** academic and preprint coverage in ML, math, physics, statistics, computer science, biology (q-bio), economics (q-fin).

**API:** https://arxiv.org/help/api — wrapped by `tools/arxiv-search.py` once implemented.

## RAG (Retrieval-Augmented Generation)

**Use when** the user has a personal/private knowledge store configured (notes, internal docs, code search).

**Target system TBD** — wrapped by `tools/rag-query.py` once implemented.

## GitHub

**Use for:** source-code questions, project documentation, issue/PR history, release notes.

**Available via** the agent host's GitHub MCP tools (read-only is fine).

## Official documentation sites

**Use for:** language references, framework guides, RFC / standards documents.

Prefer the canonical doc site over secondary blog posts.

## Atlassian (Confluence / Jira)

**Use when** the topic is organizational and the user has the Atlassian MCP server connected. Useful for internal runbooks, ADRs, tickets.

## Selection guidance

- Cast a wide net early; converge on the most authoritative source before citing.
- For each claim that survives synthesis, cite the most authoritative source you found — not the first one.
- For software: prefer the project's own docs over blog posts; prefer recent over old.
- For science: prefer peer-reviewed over preprints over blog posts.
- For breaking topics: web search is fine, but flag recency in the report.
