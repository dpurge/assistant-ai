# Anki format

`phraseforge-anki` produces **TSV (tab-separated)** source files for the [`dpurge/anki-flashcards`](https://github.com/dpurge/anki-flashcards) repo. That repo's `anki-build` Python tool (https://github.com/dpurge/anki-flashcards#build) compiles TSV + per-language `flashcard.yml` configs into `.apkg` packages.

The tool here only emits the **source TSV**. Building the `.apkg` is `task clean build` in a clone of the upstream repo.

## Downstream repo conventions (summary)

- Each language has its own directory under `dat/lang-vocabulary/<iso639-3>/` (e.g. `dat/lang-vocabulary/deu/` for German).
- Each directory holds:
  - **One `flashcard.yml`** — model/template/deck config, references the data files.
  - **One or more `*.csv` data files** (tab-separated, despite the `.csv` extension).
- Filename convention for data files: `<source>-vocabulary-<target>-<script>.csv` where
  `<source>` is the textbook/series slug, `<target>` is the translation language (ISO 639-3, usually `pol`), and `<script>` is the translation's script (usually `latn`).
- Within each TSV: header row, then `# === N ===` (or any `# === ... ===`) section markers separating batches, then data rows.

## TSV schema

The header row (must match the model's field order in `flashcard.yml`):

```
Phrase	Grammar	Transcription	Translation	Notes
```

| Field | Required | Notes |
|---|---|---|
| `Phrase` | yes | Foreign-language headword. For nouns, include the article (e.g. `der Hund`). Indexed by anki-build for note lookup (deduplication). |
| `Grammar` | no | Short part-of-speech / inflection hint. Upstream uses single-letter shorthands (e.g. `a` for adjective). PhraseForge JSON ships `N m sg` etc.; pass through verbatim. Empty string if absent. |
| `Transcription` | no | Romanized form. Required for non-Latin scripts (Arabic, Hebrew, CJK, Cyrillic-romanizations). Empty for Latin-script languages. |
| `Translation` | yes | Polish gloss. **Multiple senses separated by `; ` (semicolon + space)** — e.g. `"wszyscy; wszystkie"`, `"dzień dobry; cześć"`. The tool passes this string through verbatim. |
| `Notes` | no | Markdown-formatted extra context. Usually empty. |

Encoding: **UTF-8**. Delimiter: **`\t`**. No quoting; tabs/newlines inside fields are replaced by spaces by the tool.

## JSON input (subset of phraseforge lesson schema)

The tool reads the same JSON shape `phraseforge-typst` consumes. Only `vocabulary` is read; `date` and `title` are used to compose the section marker comment.

```json
{
  "title": "Bogini łowów Diana",
  "date": "2026-06-22",
  "lang": "lat",
  "script": "latn",
  "vocabulary": [
    {
      "headword": "Diana",
      "grammar": "N f sg",
      "transcription": null,
      "translation": "Diana",
      "notes": null
    }
  ]
}
```

Each `vocabulary[]` entry becomes one TSV row. Entries with empty `headword` are skipped (the Phrase field is indexed and Anki rejects empty indexed fields).

## Section marker

A `# === <slug> ===` comment line is emitted after the header. By default the slug is `<date> <title>` (whichever are present); override with `--source SLUG`.

```
Phrase	Grammar	Transcription	Translation	Notes
# === 2026-06-22 Bogini łowów Diana ===
Diana	N f sg		Diana	
dea	N f sg		bogini	
```

## Workflow (drop into the dpurge/anki-flashcards repo)

1. Generate the TSV:
   ```bash
   echo '<lesson-json>' | uv run --script tools/anki-export.py --out lat-cards.csv
   ```
2. Move the file into the right language directory:
   ```bash
   mv lat-cards.csv ~/path/to/anki-flashcards/dat/lang-vocabulary/lat/phraseforge-2026-06-22-pol-latn.csv
   ```
3. Open `dat/lang-vocabulary/lat/flashcard.yml` and add the file to the `data:` list:
   ```yaml
   data:
     - filename: phraseforge-2026-06-22-pol-latn.csv
       tags: ['phraseforge']
   ```
4. Build:
   ```bash
   cd ~/path/to/anki-flashcards && task clean build
   ```
   The compiled `.apkg` lands in `out/`.

## flashcard.yml shape (for bootstrapping a new language directory)

This tool does **not** generate `flashcard.yml` in v0.1 — you write it once by hand per language. Reference template (paths are relative to the language directory):

```yaml
deck:
  name: 'Language::<Family>::<Language>::Vocabulary'   # e.g. Language::Italic::Latin::Vocabulary

model:
  name: '<Language> Vocabulary'                         # e.g. Latin Vocabulary
  kind: 'normal'
  style:
    css: ../_model/latn.css                             # or arab.css for RTL scripts
  templates:
    - name: Recognize
      qfmt: ../_model/recognize-qfmt.html
      afmt: ../_model/recognize-afmt.html
    - name: Recall
      qfmt: ../_model/recall-qfmt.html
      afmt: ../_model/recall-afmt.html
  fields:
    - name: Phrase
      template: ../_template/Phrase.txt
      index: true                                       # +rtl: true for Arabic/Hebrew/Farsi
      description: Phrase
    - name: Grammar
      template: ../_template/Grammar.txt
      index: true
      description: Grammar
    - name: Transcription
      template: ../_template/Transcription.txt
      description: Transcription
    - name: Translation
      template: ../_template/Translation.txt
      merge: true                                       # append on update, don't overwrite
      description: Translation
    - name: Notes
      template: ../_template/Notes.txt
      format: markdown
      description: Notes

data:
  - filename: <source>-vocabulary-pol-latn.csv
    tags: ['<source>']
```

For non-Latin scripts, change `css: ../_model/latn.css` to the matching script CSS (e.g. `arab.css`) and add `rtl: true` under the `Phrase` field (the upstream Farsi sample is the reference).

## More examples

### Example 2 — German, simple vocabulary

```json
{
  "version": 1,
  "title": "Pierwsza lekcja",
  "lang": "deu",
  "script": "latn",
  "date": "2026-07-01",
  "vocabulary": [
    {"headword": "der Hund", "grammar": "N m sg", "translation": "pies"},
    {"headword": "die Katze", "grammar": "N f sg", "translation": "kot"},
    {"headword": "klein", "grammar": "Adj", "translation": "mały"}
  ]
}
```

Run with `--source gute-reise-1982` to override the section comment for grouping under an existing textbook tag:

```bash
echo '<above-json>' | uv run --script tools/anki-export.py --source gute-reise-1982
```

### Example 3 — Farsi with transcription (non-Latin)

```json
{
  "version": 1,
  "title": "Rozmowa",
  "lang": "fas",
  "script": "arab",
  "vocabulary": [
    {"headword": "خانه", "grammar": "N", "transcription": "xāne", "translation": "dom"},
    {"headword": "کجا", "grammar": "Pron", "transcription": "kojā", "translation": "dokąd; gdzie"}
  ]
}
```

Multiple senses in the translation are separated by `; ` (semicolon + space).

## Validation behavior

Input is validated against the Pydantic `Lesson` model in `tools/lesson_schema.py`. The JSON Schema is committed at `references/lesson.schema.json` (generated via `tools/anki-export.py --print-schema`).

Validation errors look like:

```
1 validation error for Lesson
lang
  Field required [type=missing, input_value={'title': 'x'}, input_type=dict]
```

For a vocabulary-entry error:

```
1 validation error for Lesson
vocabulary.2.headword
  Field required [type=missing, ...]
```

The error path tells you which entry is broken. Fix the field and retry. Exit code is `1` on any validation failure.

## Notes

- `phraseforge-anki` is scoped to vocabulary. Models, dialogs, exercises, and questions are not exported to Anki (they don't fit the flashcard schema). If you want a sentence-mining variant later, add a separate notetype.
- The dpurge/anki-flashcards repo has **no LICENSE file** at the time of writing. Confirm the user's intent if redistributing built `.apkg`s.
- The Pydantic `Lesson` model is **shared with phraseforge-typst** (same `lesson_schema.py` content). Build the JSON once and route to either output.
- The `models` field accepts both bare strings (`"models": ["..."]`) and structured entries (`"models": [{"pattern": "...", "transcription": "..."}]`). Anki ignores `models` entirely — only `vocabulary` is exported — but the schema matches phraseforge-typst's so the same JSON validates against both tools.
