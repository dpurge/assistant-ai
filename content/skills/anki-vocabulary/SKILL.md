---
name: anki-vocabulary
description: Generate and review Anki-style vocabulary flashcards stored as tab-separated CSV files of Phrase/Grammar/Transcription/Translation/Notes records, organized as a deck manifest (flashcard.yml) referencing one *.csv file per source. Use when the user invokes /anki-vocabulary, asks to create or expand vocabulary flashcards for a language, or wants to review/improve an existing vocabulary deck for learning words and phrases on a smartphone.
---

# Anki vocabulary flashcard generator

Produce and maintain vocabulary flashcards for a language, stored as tab-separated CSV records split by source and tied together by a deck manifest, `flashcard.yml`.

## Invocation

The user passes a directory (or an existing `flashcard.yml`/source file inside one) and either a source of vocabulary (a textbook, word list, topic, or pasted text) or an instruction to review/improve the existing deck. If no directory is given, ask before doing anything else — decks live under `dat/lang-vocabulary/<iso-code>/` (e.g. `dat/lang-vocabulary/spa/` for Spanish), one directory per language.

## Directory layout

A deck lives in its own directory, e.g. `dat/lang-vocabulary/spa/`:

```
dat/lang-vocabulary/spa/
  flashcard.yml                          <- deck manifest (see below)
  aula-2013-vocabulary-pol-latn.csv       <- vocabulary rows sourced from "Aula" (2013)
  lingo-2016-vocabulary-pol-latn.csv      <- vocabulary rows sourced from "Lingo" (2016)
  ...                                      <- one *.csv per source
```

Vocabulary is never dumped into one giant file. Each `*.csv` corresponds to one source (a textbook, course, or word list) so provenance stays traceable and a source can be extended in isolation. Filename convention: `<source-slug>-<year>-vocabulary-<translation-lang>-<transcription-script>.csv`, e.g. `ryding-2005-vocabulary-pol-latn.csv` — `pol` is the ISO 639-2 code of the translation language, `latn` is the ISO 15924 code of the script used in the `Transcription` column. Reuse whatever translation language and transcription script the deck's existing files already use.

Shared model assets (`_model/`, `_template/`) live one level up at `dat/lang-vocabulary/_model/` and `dat/lang-vocabulary/_template/` and are shared across every language deck — never duplicate them per-language.

## `flashcard.yml`: the deck manifest

`flashcard.yml` itself holds no vocabulary rows. It is boilerplate that:
- names the Anki deck (`deck.name`, using `::` for subdecks, e.g. `'Language::Romance::Spanish::Vocabulary'` — family comes from the deck's linguistic family, matching sibling decks)
- points at the shared card model/templates (copy this block verbatim from an existing `flashcard.yml` in a sibling language directory, changing only `model.name`, `model.style.css`, and `fields.Phrase.rtl` as needed)
- lists every source CSV under `data`, each tagged with its source slug

```yaml
deck:
  name: 'Language::Romance::Spanish::Vocabulary'

model:
  name: 'Spanish Vocabulary'
  kind: 'normal'
  style:
    css: ../_model/latn.css
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
      index: true
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
      merge: true
      description: Translation
    - name: Notes
      template: ../_template/Notes.txt
      format: markdown
      description: Notes

audio: []
video: []
image: []

data:
  - filename: ./aula-2013-vocabulary-pol-latn.csv
    tags: ['aula-2013']
  - filename: ./lingo-2016-vocabulary-pol-latn.csv
    tags: ['lingo-2016']
```

- `model.style.css` picks the shared CSS matching the language's writing system (`../_model/latn.css`, `arab.css`, `cyrl.css`, `hans.css`, `hant.css`, `hebr.css`, `deva.css`, `grek.css`, `kore.css`, `jpan.css`, ...). If the script isn't covered yet, ask before inventing a new one.
- Add `rtl: true` to the `Phrase` field when the language's script is right-to-left (Arabic, Hebrew, etc.), matching how `arb/flashcard.yml` does it.
- Every source file must have an entry under `data`, `filename` pointing at it and `tags` set to a single-element array naming the source slug (used for Anki tag filtering — keep it lowercase-hyphenated, matching the filename's `<source-slug>-<year>` prefix).
- When adding a new source file, add its `data` entry in the same edit — a source file with no manifest entry is invisible to the deck.
- Never put vocabulary rows inside `flashcard.yml` itself — that file's shape is fixed (deck/model/audio/video/image/data), and rows always live in the source CSVs it references.

## Source CSV format

Each source `*.csv` is tab-separated with a header row, optional numbered section-comment rows, and one row per vocabulary entry:

```
Phrase	Grammar	Transcription	Translation	Notes
# === 1 ===
la abuela	N		babcia	
el hermano	N		brat	
ser la oveja negra	VP		być czarną owcą	
```

- Columns, in order: `Phrase` (the word/phrase in the target language), `Grammar` (part-of-speech/grammar code), `Transcription` (romanization/pronunciation aid — leave blank if the phrase is already in Latin script or the deck doesn't use this column), `Translation` (meaning in the translation language; `;`-separate close synonyms), `Notes` (optional usage/context notes).
- `Phrase` and `Translation` are mandatory. `Grammar`, `Transcription`, and `Notes` are optional per row — leave the cell empty (still keep the tab) rather than guessing.
- `Grammar` uses short codes consistent within the deck: `N` noun, `V` verb, `Adj` adjective, `Adv` adverb, `NP`/`VP`/`AdjP` phrase variants, plus gender/number markers like `m`, `f`, `pl`, `sg` where the translation language marks them. Check the deck's existing files for the codes already in use before introducing a new one.
- `# === <n> ===` comment rows (or letter/level markers like `a1`, `a2`) group entries into the source's own chapters/lessons/levels — preserve the source material's structure so provenance and progression stay traceable back to the book.
- Keep rows sorted the way the source presents them (by chapter/lesson), not alphabetized — the deck mirrors how the material was originally taught.

## Workflow

1. Resolve the deck directory (ask if missing) and the source/topic (from the prompt, or ask if unclear).
2. If the deck already exists, read `flashcard.yml` first to see which source files exist and what each covers.
3. Decide which file the new vocabulary belongs in:
   - If it's more material from a source already in the deck, read that file fully first — new rows must not duplicate existing entries and should extend its existing chapter/section structure.
   - If it's a new source, create a new `*.csv` file following the filename convention and add a corresponding `data` entry (with `tags`) to `flashcard.yml` in the same turn. If this is the deck's first file, also create `flashcard.yml` from a sibling language's file, adjusting `deck.name`, `model.name`, and `model.style.css`.
4. Thoroughly derive vocabulary from the given source (textbook pages, pasted list, provided text) before drafting rows. Do not invent words, translations, or grammar codes not supported by the source.
5. Identify the translation language and transcription script already used by the deck (or agree on them with the user for a brand-new deck) and keep every row consistent with that choice.
6. Draft rows:
   - One word or fixed phrase per row — don't cram multiple senses into one `Phrase`.
   - Fill `Transcription` only when the deck's convention calls for it (e.g. non-Latin scripts); leave blank for decks where `Phrase` is already readable.
   - Use consistent `Grammar` codes matching the rest of the file/deck.
   - Preserve or add `# === <n> ===` section markers matching the source's chapter/lesson breakdown.
7. Append new rows to the end of the relevant source file's appropriate section (existing rows are never reordered or rewritten unless the user asks for a review pass). Create the file (and its `flashcard.yml` entry) if it doesn't exist yet.
8. When asked to review/improve rather than add: read the whole source file (or the whole deck), then propose concrete edits (fix wrong translations, correct grammar codes, remove duplicates, add missing transcriptions) and apply them — don't just add more rows on top of a flawed base.
9. Sources are expected to be expanded over multiple follow-up messages — treat each invocation as either growing coverage of an existing source, adding a new source file, or improving what's already there, not a one-shot dump.
