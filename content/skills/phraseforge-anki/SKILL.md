---
name: phraseforge-anki
description: Generate Anki flashcard source files (TSV) from a PhraseForge lesson, targeting the dpurge/anki-flashcards repo (https://github.com/dpurge/anki-flashcards). The upstream repo's anki-build tool then compiles the TSV files into .apkg packages. Use when the user mentions Anki, flashcards, spaced repetition, dpurge/anki-flashcards, or asks to export a lesson's vocabulary to Anki.
user-invocable: true
---

# PhraseForge Anki exporter

Generate **TSV source files** for the [`dpurge/anki-flashcards`](https://github.com/dpurge/anki-flashcards) repository, one row per vocabulary entry. The upstream repo's `anki-build` tool (Python + Click + PyYAML, runs via `task clean build`) compiles those TSV files plus a per-language `flashcard.yml` into `.apkg` packages.

This skill emits the **source TSV only**. Compiling the `.apkg` and updating the language directory's `flashcard.yml` is a manual step in the upstream repo clone.

## When invoked

1. Get the conceptual lesson content from `phraseforge-core` (specifically the `vocabulary` block).
2. Assemble it into a **JSON object** matching the phraseforge lesson schema. Required: `vocabulary` (list of `{headword, grammar, transcription, translation, notes}`). Useful: `date`, `title`, `lang`, `script` (used to compose the section marker).
3. Pipe the JSON into `anki-export.py`:
   ```bash
   echo '<lesson-json>' | uv run --script tools/anki-export.py --out cards.csv
   ```
   Or from a file:
   ```bash
   uv run --script tools/anki-export.py --in lesson.json --out cards.csv
   ```
4. Move the TSV into the right language directory of an `anki-flashcards` clone:
   `dat/lang-vocabulary/<iso639-3>/<source>-vocabulary-pol-latn.csv`.
5. Register the new file in that directory's `flashcard.yml` under `data:` (you do this once; subsequent rebuilds reuse the same registration).
6. Tell the user to run `task clean build` in the anki-flashcards clone to produce the `.apkg`.

## Tool

```
uv run --script tools/anki-export.py [--in lesson.json] [--out cards.csv] [--source SLUG]
uv run --script tools/anki-export.py --print-schema       # dump the JSON Schema
```

- `--in PATH` — JSON input; default stdin (`-`).
- `--out PATH` — TSV output; default stdout (`-`).
- `--source SLUG` — override the `# === <slug> ===` section marker; defaults to `<date> <title>` derived from JSON.
- `--print-schema` — print the JSON Schema generated from the Pydantic model and exit (used to refresh `references/lesson.schema.json`).

PEP-723 deps: `pydantic>=2.6`, `jinja2>=3.1` (cached after first run).

**Validation**: input JSON is parsed against the Pydantic `Lesson` model in `tools/lesson_schema.py` — the same model `phraseforge-typst` uses. Bad input exits `1` with a path-aware `ValidationError` on stderr (e.g. `lang: Field required`, `vocabulary.2.headword: Field required`). The JSON Schema sidecar at `references/lesson.schema.json` is byte-identical to `phraseforge-typst/references/lesson.schema.json`.

**Rendering**: the actual TSV output is produced by a Jinja2 template at `tools/templates/cards.tsv.j2`. A warning is still emitted to stderr if the input has no `vocabulary` entries (the output then contains only the header + section marker).

## What the output looks like

```
Phrase	Grammar	Transcription	Translation	Notes
# === 2026-06-22 Bogini łowów Diana ===
Diana	N f sg		Diana	
dea	N f sg		bogini	
silva	N f sg		las	
```

Tab-separated, UTF-8, no quoting. Tabs/newlines inside fields are collapsed to spaces by the tool (Anki TSV import doesn't handle multi-line fields without explicit quoting).

## Constraints

- This skill is scoped to **vocabulary** only. Models, dialogs, exercises, and comprehension questions are not exported (they don't fit the flashcard notetype). A sentence-mining variant would need a separate notetype and a different export.
- The downstream repo (`dpurge/anki-flashcards`) has **no LICENSE file** at the time of writing. Confirm the user's intent before redistributing built `.apkg`s.
- The tool does **not** generate `flashcard.yml`. That config is written once per language directory; see `references/anki-format.md` for the template.

## References

- `references/anki-format.md` — full TSV schema, JSON input shape, flashcard.yml template, end-to-end workflow into the anki-flashcards clone.
