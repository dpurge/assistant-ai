# assistant-ai

A cross-platform plugin that bundles personal-learning skills for multiple AI coding agents — Claude Code, OpenCode, Pi. The skills know how to author language lessons (PhraseForge) and how to research topics across web / arXiv / RAG and produce sourced reports. Everything is rendered to multiple output formats (MDX for Docusaurus, TSV for Anki, Typst for PDF) from a single lesson-JSON contract.

Two skill families today:

- **`phraseforge-*`** — language-lesson authoring for the [phraseforge-web](https://github.com/dpurge/phraseforge-web) Docusaurus site.
- **`research-*`** — topic research and write-up, with RAG-first / external-fallback source ordering.

Single source of truth under `content/`; per-target zip artifacts built on demand.

---

## Quick start

```bash
# 1. Build the zips
just build

# 2. Install into your AI host (claude | opencode | pi)
just install claude

# 3. Open the host and invoke a skill — e.g. /phraseforge-web in Claude Code,
#    or describe what you want and let the host pick the right skill.
```

Prereqs: [`just`](https://github.com/casey/just) and [`uv`](https://github.com/astral-sh/uv) on your `$PATH`. `uv` will fetch Python if you don't have it.

---

## Skill families

### `phraseforge-*` — language-lesson authoring

| Skill | User-invocable | Purpose |
|---|---|---|
| `phraseforge-core` | — | Output-agnostic lesson workflow. Loaded by the others. |
| `phraseforge-web` | ✓ `/phraseforge-web` | Render lesson as MDX for the phraseforge-web Docusaurus site. **Default output.** |
| `phraseforge-anki` | ✓ `/phraseforge-anki` | Render vocabulary as TSV for the [dpurge/anki-flashcards](https://github.com/dpurge/anki-flashcards) repo. |
| `phraseforge-typst` | ✓ `/phraseforge-typst` | Render lesson as Typst source via the [dpurge/typst-lib](https://github.com/dpurge/typst-lib) `langnote` package. |
| `phraseforge-lang-deu` | — | German conventions (codes, vocab format, formality). |
| `phraseforge-lang-spa` | — | Spanish conventions. |

Add new `phraseforge-lang-<iso>` skills by copying one of the existing ones — they're small (~70 lines of conventions per language).

### `research-*` — topic research

| Skill | User-invocable | Purpose |
|---|---|---|
| `research-core` | — | Topic-driven workflow. Queries local RAG first; falls back to Wikipedia / arXiv / web. Iterative revision. |
| `research-web` | ✓ `/research-web` | Render report as a Docusaurus MDX page (output path is an argument). |
| `research-anki` | ✓ `/research-anki` | Export key facts as Anki flashcards. *(stub)* |
| `research-typst` | ✓ `/research-typst` | Render report as Typst PDF source. *(stub)* |

The topic is an argument to `research-core` — there are intentionally **no per-topic sub-skills**.

---

## Using the skills

### Author a PhraseForge lesson

In your AI host, say something like:

> "Write a phraseforge lesson at level A1 from this Latin text: *Diana est dea silvarum et venationis.*"

What happens:

1. `phraseforge-core` is triggered by description match. It detects the language (Latin → `lat`), script (Latin → `latn`), and loads the language skill if one exists.
2. It builds the conceptual content: vocabulary, models, translation, exercises.
3. By default it hands off to `phraseforge-web` which renders to MDX in your phraseforge-web clone.
4. If you said "and also as a PDF", it routes to `phraseforge-typst`; "and Anki cards" routes to `phraseforge-anki`. Same lesson JSON, three renderings.

The conceptual content is the **lesson JSON** (schema: `content/_shared/lesson_schema.py`). All three output tools consume the same JSON shape — see [Architecture: the lesson JSON contract](#architecture-the-lesson-json-contract).

### Research a topic

> "Research the history of fast inverse square root and write me a short report."

What happens:

1. `research-core` is triggered. It runs `tools/rag-query.py` against your local knowledge base first.
2. If the local store has hits above the threshold, those chunks are the primary input.
3. Otherwise (or in addition), it pulls from Wikipedia, arXiv, web search — depending on the topic.
4. It synthesizes a sourced report (claims with inline citations).
5. Hands off to the requested output skill — default `research-web` (Docusaurus page); `research-anki` for cards; `research-typst` for PDF.

The local RAG is at `~/.assistant/knowledge/`. Drop markdown files there, run `uv run --script content/skills/research-core/tools/rag-index.py` once, then queries hit the index. See [Local knowledge base](#local-knowledge-base-rag).

### Add a new language

1. Copy one of the existing `phraseforge-lang-*/SKILL.md` files to `content/skills/phraseforge-lang-<iso>/SKILL.md`.
2. Replace the per-language facts (codes, script, transcription system, vocabulary entry shape, formality conventions). The German file is the most fleshed-out template.
3. `just build` — the new skill is auto-discovered.

No code changes required.

---

## Targets

| Host | Notes |
|---|---|
| **Claude Code** | full plugin via `.claude-plugin/plugin.json` |
| **OpenCode** | original `opencode-ai/opencode` (archived) or a community fork — **not Crush** |
| **Pi** | [earendil-works/pi](https://github.com/earendil-works/pi), MIT — filesystem-only skill discovery |

All three consume the [Agent Skills standard](https://agentskills.io/specification) (`SKILL.md` with YAML frontmatter); the content layer is bit-for-bit identical across them. **Pi**'s TypeScript extension mechanism is out of scope — we ship Python tools.

---

## Code map

```
assistant-ai/
├── content/                              # SINGLE SOURCE OF TRUTH
│   ├── _shared/
│   │   └── lesson_schema.py              # Pydantic models — the lesson JSON contract
│   └── skills/
│       ├── phraseforge-core/             # one dir per skill, all the same shape:
│       │   ├── SKILL.md                  #   front-matter (name, description, user-invocable)
│       │   │                             #   + body (the instructions the agent reads)
│       │   ├── references/*.md           #   detail loaded on demand by the agent
│       │   ├── assets/*                  #   copy-paste skeletons (templates, examples)
│       │   └── tools/                    #   Python tools the agent invokes via `uv run --script`
│       │       ├── *.py
│       │       └── templates/*.j2        #     Jinja2 templates for rendering tools
│       ├── phraseforge-anki/             # … etc, same shape
│       ├── phraseforge-web/
│       ├── phraseforge-typst/
│       ├── phraseforge-lang-deu/
│       ├── phraseforge-lang-spa/
│       ├── research-core/
│       ├── research-anki/
│       ├── research-web/
│       └── research-typst/
│
├── plugins/
│   └── claude/.claude-plugin/
│       └── plugin.json                   # Claude-specific plugin manifest
│
├── scripts/                              # build/install/test infrastructure
│   ├── _common.py                        # TARGETS table, shared-file injection map
│   ├── build.py                          # produces dist/assistant-*.zip
│   ├── install.py                        # build then unpack into the host's install dir
│   ├── uninstall.py                      # remove only the skills we own (shared dirs are safe)
│   ├── clean.py                          # rm -rf dist/
│   └── bump_version.py                   # rewrites plugin.json version + prints release commands
│
├── tests/                                # pytest suite (NOT shipped in zips)
│   ├── conftest.py                       # tool paths, subprocess runner
│   ├── test_export.py                    # golden-output + validation tests for the 3 exporters
│   ├── test_lesson_schema.py             # unit tests on the Pydantic models
│   ├── fixtures/                         # sample lesson JSON inputs
│   └── golden/                           # expected outputs (.typ, .tsv, .mdx)
│
├── .github/workflows/release.yml         # tag-push → test + build + GitHub Release
├── justfile                              # build / install / uninstall / clean / test / bump-version
├── .gitignore
└── dist/                                 # gitignored — built zips land here
```

### Where to look when you want to…

| Task | Files to touch |
|---|---|
| Add a new language skill | `content/skills/phraseforge-lang-<iso>/SKILL.md` (copy an existing one) |
| Change MDX output formatting | `content/skills/phraseforge-web/tools/templates/lesson.mdx.j2` + `mdx-export.py` |
| Change Typst output formatting | `content/skills/phraseforge-typst/tools/templates/lesson.typ.j2` + `typst-export.py` |
| Change the lesson JSON contract | `content/_shared/lesson_schema.py` — single source; regenerate sidecar schemas with `--print-schema` |
| Change install behavior | `scripts/install.py`, `scripts/_common.py` (TARGETS table) |
| Change what's bundled in a zip | `scripts/build.py` and `SHARED_BY_SKILL` in `scripts/_common.py` |
| Add a test | `tests/test_*.py`; goldens at `tests/golden/` |
| Change the release flow | `.github/workflows/release.yml` |

---

## Architecture: the lesson JSON contract

`phraseforge-core` doesn't write any file. Its job is to produce a **structured lesson** as a Python/JSON object that downstream output skills consume. The shape lives in [`content/_shared/lesson_schema.py`](content/_shared/lesson_schema.py) and looks like:

```python
class Lesson(BaseModel):
    title: str                      # required
    lang: str                       # required — ISO 639-3
    script: str = "latn"            # ISO 15924
    date: str | None = None         # ISO YYYY-MM-DD
    vocabulary: list[VocabularyEntry] = []
    models: list[ModelEntry] = []   # each entry: pattern + translation (+ transcription)
    source: TextSource | DialogSource | None = None   # discriminated by `kind`
    transcription: str | None = None
    translation: str | None = None
    questions: list[str] | None = None
    exercises: list[Exercise] = []
```

**One Pydantic schema, three exporters.** Each output tool (`mdx-export.py`, `typst-export.py`, `anki-export.py`) consumes the same JSON; the build step injects a copy of `lesson_schema.py` next to each one. Sidecar JSON Schemas (`<skill>/references/lesson.schema.json`) are generated via `tool --print-schema` and committed to the repo so structured-output features in some hosts can use them. All three sidecars are byte-identical — `tests/test_export.py::test_schemas_are_identical_across_tools` enforces this.

### Tool invocation

Every tool is a single-file PEP-723 script with inline dependencies. The agent runs them via:

```
uv run --script content/skills/<skill>/tools/<tool>.py [args]
```

uv reads the `# /// script` block at the top, materializes a cached venv with the listed deps, and runs the script. No `requirements.txt`, no project venv. First run downloads deps; subsequent runs are cache-hits.

### Why no symlinks?

Cross-platform (Windows) compatibility. The shared `lesson_schema.py` lives once at `content/_shared/`. `scripts/build.py` injects a copy into each consuming skill's `tools/` directory at zip-build time. A dev-time `sys.path` hack in each tool locates the shared dir when running from source.

---

## Development

```bash
just            # list recipes
just build      # build zips into dist/
just install <claude|opencode|pi>
just uninstall <claude|opencode|pi>
just clean      # rm -rf dist/
just test       # pytest -v tests/
just bump-version 0.2.0     # rewrites plugin.json, prints git commands
```

### Tests

```bash
just test
```

Runs the pytest suite under `tests/`. The tests exercise the actual CLIs via subprocess (not by importing internals), so behavior changes in the renderers are caught. Golden outputs live in `tests/golden/`; when you intentionally change a renderer, regenerate the affected golden with:

```bash
uv run --script content/skills/phraseforge-web/tools/mdx-export.py \
  --in tests/fixtures/diana.json --out tests/golden/diana.mdx
```

### Cutting a release

```bash
just bump-version 0.2.0
# follow the printed git commit / tag / push commands
```

The release workflow at `.github/workflows/release.yml` triggers on `v*` tag push: it runs `just test`, runs `just build`, verifies the tag matches `plugin.json`'s version, and creates a GitHub Release with the two zips attached and auto-generated notes. Manual dispatch (Actions → release → Run workflow) does the same test + build but uploads to a 14-day workflow artifact instead of cutting a release.

**Before your first tagged release:** fill in `author.name` and `author.email` in `plugins/claude/.claude-plugin/plugin.json`. They're `TODO_AUTHOR_NAME` / `TODO_AUTHOR_EMAIL` today and would ship inside every released zip.

---

## Reference

### Install destinations

| Target | Default | Override | Mode |
|---|---|---|---|
| `claude` | `~/.claude/plugins/assistant/` | `ASSISTANT_CLAUDE_DIR` | **exclusive** — install dir wiped on reinstall |
| `opencode` | `~/.config/opencode/skills/` | `ASSISTANT_OPENCODE_DIR` | **shared** — only owned skills are touched |
| `pi` | `~/.pi/agent/skills/` | `ASSISTANT_PI_DIR` | **shared** — only owned skills are touched |

`ASSISTANT_FORCE=1` overrides safety checks (Claude only — overwrites a non-empty install dir that doesn't look like a previous assistant install).

### Built zip layouts

`just build` emits two zips:

- **`assistant-claude-<ver>.zip`** — full Claude Code plugin (manifest + `skills/<name>/` prefix).
- **`assistant-skills-<ver>.zip`** — bare Agent Skills bundle (each skill at top level, no manifest). Used by both `opencode` and `pi` installs; the content is identical, only the install destination differs.

### Local knowledge base (RAG)

`research-core` queries a local FAISS index over markdown files at `~/.assistant/knowledge/` (override with `ASSISTANT_KNOWLEDGE_DIR`). Files are split at H2 (fallback H1; whole-file otherwise) with the file path and header breadcrumb preserved as chunk context. See `content/skills/research-core/references/rag.md` for layout details.

Stack: **FAISS** (BSD, Meta) for the index, **fastembed** (Apache-2.0, Qdrant) with `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (~225 MB on first download; multilingual incl. Polish). Override the model via `ASSISTANT_RAG_MODEL`.

Rebuild the index after editing knowledge files:

```bash
uv run --script content/skills/research-core/tools/rag-index.py
```

### Output targets

- **Typst PDF** — `phraseforge-typst` emits Typst sources targeting the [dpurge-langnote](https://github.com/dpurge/typst-lib) package (MIT). Install the package locally per `content/skills/phraseforge-typst/references/typst-format.md` before compiling.
- **Anki TSV** — `phraseforge-anki` emits TSV for the [dpurge/anki-flashcards](https://github.com/dpurge/anki-flashcards) repo. Drop the file into `dat/lang-vocabulary/<iso>/`, register it in that language's `flashcard.yml`, and run `task clean build` in the anki-flashcards clone to produce `.apkg`.
- **MDX (Docusaurus)** — `phraseforge-web` and `research-web` emit MDX. For phraseforge-web specifically, the format matches the upstream parser's `dialog` / `vocabulary` / `models` code fences and `<Text>` / `<Questions>` / `<Exercise>` JSX components.

### Tool dependencies (PEP-723)

Each tool declares its deps inline:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2.6", "jinja2>=3.1"]
# ///
```

Real-tool dep stack today:

| Tool | Deps |
|---|---|
| `phraseforge-{typst,anki,web}/tools/*-export.py` | `pydantic>=2.6`, `jinja2>=3.1` |
| `research-core/tools/rag-index.py`, `rag-query.py` | `fastembed`, `faiss-cpu`, `pyyaml`, `numpy` |
| `pytest` (test harness only) | injected via `uv run --with pytest` |

All other tools are stubs with no external deps yet.

### License & status

- Version: `0.1.0` (per `plugins/claude/.claude-plugin/plugin.json`).
- Author identity in `plugin.json`: placeholder — fill in before the first tagged release.
- No remote configured yet — set one with `git remote add origin git@github.com:<you>/assistant-ai.git` before the workflow has anywhere to push.
