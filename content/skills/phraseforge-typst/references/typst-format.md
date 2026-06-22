# Typst format

`phraseforge-typst` emits a Typst source file (`.typ`) targeting the **dpurge-langnote** Typst package (https://github.com/dpurge/typst-lib, MIT). The package is purpose-built for language-learning notebooks and ships templates for `LangNote` (the document wrapper), `Lesson`, `Vocabulary`, `Dialog`, `Text`, `Models`, `Questions`, `Exercise`, `TitlePage`, and `TableOfContents`.

The tool itself is pure-Python string rendering — no Typst toolchain dependency at build time.

## Prerequisite: install `dpurge-langnote`

The generated `.typ` imports `@local/dpurge-langnote:0.0.1`. Typst looks up that name in your local-packages directory. Install the lib **once** before compiling any output:

- **Windows.** From the typst-lib README: create a symlink `%LOCALAPPDATA%\typst\packages\local\dpurge-langnote\0.0.1` pointing at the `langnote/` subdir of your local typst-lib clone.
- **macOS / Linux.** Typst expects local packages at:
  - macOS: `~/Library/Application Support/typst/packages/local/dpurge-langnote/0.0.1`
  - Linux: `~/.local/share/typst/packages/local/dpurge-langnote/0.0.1`

  Symlink (or copy) the `langnote/` subdir of a typst-lib clone there. The upstream README still says "Linux setup TODO", so verify against the latest README before automating.

Pin to a different version with `--package-version <ver>` once the lib bumps.

## JSON input schema (v1)

The tool reads a single JSON object on stdin (or `--in <path>`):

```json
{
  "version": 1,
  "title": "Bogini łowów Diana",
  "description": "Adaptacja artykułu o Dianie",
  "lang": "lat",
  "script": "latn",
  "level": "a1",
  "date": "2026-06-22",
  "author": null,
  "vocabulary": [
    {
      "headword": "Diana",
      "grammar": "N f sg",
      "transcription": null,
      "translation": "Diana",
      "notes": null
    }
  ],
  "models": ["Diana est dea.", "Diana silvas amat."],
  "source": {
    "kind": "text",
    "content": "Diana est dea silvarum et venationis."
  },
  "transcription": null,
  "translation": "Diana to bogini lasów i łowów.",
  "questions": ["Quis est Diana?"],
  "exercises": [
    {
      "type": "translation",
      "instruction": "Przetłumacz na polski:",
      "items": ["Diana est dea.", "Diana silvas amat."]
    }
  ]
}
```

### Required fields

- `title` — the lesson title (Polish by default).
- `lang` — 3-letter ISO 639-3 code of the foreign language.

Everything else is optional. The tool fills sensible defaults:
- `script` → `latn`
- `date` → today (UTC, year-month-day)
- `author` → `none` in Typst
- empty sections are omitted entirely

### Field details

| Field | Type | Notes |
|---|---|---|
| `version` | int | reserved; v1 is the current schema |
| `title` | string | rendered into `LangNote.with(title: ...)` and `Lesson` heading |
| `description` | string | not rendered today; reserved for metadata |
| `lang` | ISO 639-3 | feeds `LangNote.with(foreign-lang: ...)` and per-language styling in the lib |
| `script` | ISO 15924 (lowercase) | feeds `LangNote.with(foreign-script: ...)`; controls fonts & RTL |
| `level` | CEFR string | not rendered today; reserved |
| `date` | ISO `YYYY-MM-DD` | parsed into a Typst `datetime(year, month, day)` for `Lesson(date: ...)` |
| `author` | string \| null | `LangNote.with(author: ...)` |
| `vocabulary` | list of entry dicts | see below |
| `models` | list of `ModelEntry` | each entry becomes a `Models` list item rendered as `pattern [transcription] = translation` (transcription omitted for Latin scripts) |
| `source.kind` | `"text"` or `"dialog"` | drives whether `Text` or `Dialog` is used |
| `source.content` | string | **text only.** The adapted foreign-language prose. |
| `source.title` | string \| null | **dialog only.** Optional title; passed to `#Dialog(title: ...)`. |
| `source.items` | list of `Narration` \| `DialogTurn` | **dialog only.** Interleaved items, see below. |
| `transcription` | string \| null | rendered only when present and the script is non-Latin |
| `translation` | string | Polish prose; rendered via `Text(title: "Tłumaczenie")` |
| `questions` | list of strings \| null | rendered via `Questions` as enumerated list (`+`) |
| `exercises` | list of exercise dicts | one `Exercise` per entry; numbered 1..N |

### Vocabulary entry

```json
{
  "headword": "der Hund",
  "grammar": "N m sg",
  "transcription": null,
  "translation": "pies",
  "notes": null
}
```

Renders as one Typst list item using the dpurge-langnote inline-marker syntax: `headword`, then optionally `{grammar}`, `[transcription]`, `= translation`, `(notes)`.

**Multiple senses** in `translation` are separated by `; ` (semicolon + space):

```json
{"headword": "alle", "translation": "wszyscy; wszystkie"}
```

The tool passes the translation through verbatim — no special handling of the separator.

### Model entry

```json
{"pattern": "أنا سعيد", "transcription": "ʾanā saʿīd"}
```

For Latin-script lessons the transcription is omitted (or pass a bare string). For non-Latin scripts (Arabic, Farsi, Hebrew, CJK), include the transcription so the printed PDF carries both the original phrase and its romanized reading inline as `pattern [transcription]`. Multiple senses are not encoded here — keep them in the translation block.

A `models` list can mix bare strings and full entries:

```json
"models": [
  "Diana est dea.",
  {"pattern": "أنا سعيد", "transcription": "ʾanā saʿīd"}
]
```

### Dialog items

A `DialogSource` matches the phraseforge-web `dialog` code-fence parser model. Two item kinds are interleaved via `kind`:

```json
{"kind": "narration", "text": "Setting prose between turns."}
```

```json
{"kind": "turn", "speaker": "Anna", "paragraphs": ["First paragraph.", "Second paragraph."]}
```

- **`narration`** — non-speaker prose; renders as a list item with no speaker label in Typst, becomes a top-level paragraph in phraseforge-web MDX.
- **`turn`** with `speaker: null` — anonymous turn (em-dash speaker label; `--:` in phraseforge-web MDX).
- **`turn`** with `paragraphs` — each entry is one paragraph. Typst joins them with a space in the list-item body; phraseforge-web emits them as separate paragraphs within the turn body (blank line between).

The renderer for **Typst** uses dpurge-langnote's `Dialog()` template, which parses list items with `Speaker:` headers (no `@` prefix). The same JSON, fed to a phraseforge-web MDX renderer, would emit the `@Speaker:` / `--:` syntax that parser expects.

### Exercise entry

```json
{
  "type": "translation",
  "instruction": "Przetłumacz na polski:",
  "items": ["sentence 1", "sentence 2"]
}
```

Renders to:

```typst
#Exercise(number: "1")[
  #Instruction[Przetłumacz na polski:]
  - sentence 1
  - sentence 2
]
```

The `type` field is currently advisory only — every exercise renders the same way (instruction + bullet list). Future versions can route on `type` (`fill-gaps`, `word-order`, `multiple-choice`, etc.) to specialized layouts.

## dpurge-langnote mapping (summary)

| phraseforge concept | dpurge-langnote call |
|---|---|
| Document wrapper | `#show: LangNote.with(title, author, native-lang: "pol", foreign-lang, foreign-script)` |
| Cover page | `#TitlePage()` |
| Lesson container | `#Lesson(date: datetime(...))[ ... ]` |
| Vocabulary | `#Vocabulary[ - headword {gram} [transcription] = translation (notes) ]` |
| Models | `#Models(title: "Modele")[ - pattern ]` |
| Source prose | `#Text(title: "Tekst")[ ... ]` |
| Source dialog | `#Dialog(title: "<title or Dialog>")[ - Speaker: paragraphs joined / - — anon body / - narration text ]` |
| Transcription | `#Text(title: "Transkrypcja")[ ... ]` (only when non-Latin script) |
| Translation | `#Text(title: "Tłumaczenie")[ ... ]` |
| Questions | `#Questions(title: "Pytania")[ + q1 + q2 ]` |
| Exercises | `#Exercise(number: "<n>")[ #Instruction[...] - item1 - item2 ]` |
| TOC | `#TableOfContents()` |

Section titles are hard-coded Polish (`Tekst`, `Tłumaczenie`, …) — fine for the default workflow; could become JSON-driven later.

## More examples

### Example 2 — German, simple text source, no transcription

```json
{
  "version": 1,
  "title": "Pierwsza lekcja",
  "lang": "deu",
  "script": "latn",
  "date": "2026-07-01",
  "level": "a1",
  "vocabulary": [
    {"headword": "der Hund", "grammar": "N m sg", "translation": "pies"},
    {"headword": "die Katze", "grammar": "N f sg", "translation": "kot"}
  ],
  "source": {"kind": "text", "content": "Der Hund läuft. Die Katze schläft."},
  "translation": "Pies biegnie. Kot śpi."
}
```

### Example 3 — Farsi dialog with transcription (non-Latin)

```json
{
  "version": 1,
  "title": "Krótka rozmowa",
  "lang": "fas",
  "script": "arab",
  "date": "2026-07-04",
  "vocabulary": [
    {"headword": "خانه", "grammar": "N", "transcription": "xāne", "translation": "dom"}
  ],
  "models": [
    {"pattern": "سلام", "transcription": "salām"},
    {"pattern": "اسم من … است", "transcription": "esm-e man … ast"}
  ],
  "source": {
    "kind": "dialog",
    "title": "Krótka rozmowa",
    "items": [
      {"kind": "narration", "text": "Dwoje znajomych spotyka się na ulicy."},
      {"kind": "turn", "speaker": "Aḥmad", "paragraphs": ["Marḥabā!", "Kayfa ḥāluka?"]},
      {"kind": "turn", "speaker": "Sārah", "paragraphs": ["Ahlan wa-sahlan."]},
      {"kind": "turn", "speaker": null, "paragraphs": ["Pauza w tle."]}
    ]
  },
  "transcription": "Aḥmad: Marḥabā! Sārah: Ahlan wa-sahlan.",
  "translation": "Ahmad: cześć! Sara: witam serdecznie."
}
```

Note how `models` mixes object entries to carry transcription — required for Arabic-script content so the printed PDF shows both the foreign phrase and its romanization side-by-side.

## Validation behavior

Input is validated against the Pydantic `Lesson` model in `tools/lesson_schema.py`. The JSON Schema is committed at `references/lesson.schema.json` (generated via `tools/typst-export.py --print-schema`).

Validation errors look like:

```
1 validation error for Lesson
lang
  Field required [type=missing, input_value={'title': 'x'}, input_type=dict]
```

For a discriminated-union error (bad `source.kind`):

```
1 validation error for Lesson
source
  Input tag 'poem' found using 'kind' does not match any of the expected tags: 'text', 'dialog'
```

The error message points at the exact field path (`source`, `vocabulary.2.headword`, etc.). Fix that field and retry. Exit code is `1` on any validation failure.

## Compile to PDF

```bash
echo '<JSON>' | uv run --script tools/typst-export.py --out lesson.typ
typst compile lesson.typ lesson.pdf
```

Open `lesson.pdf` to verify. Failures usually point at a missing dpurge-langnote install — re-check the symlink.
