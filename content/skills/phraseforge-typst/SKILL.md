---
name: phraseforge-typst
description: Generate a Typst source file (.typ) for a PhraseForge lesson, suitable for `typst compile` to PDF. Uses the dpurge-langnote Typst package (https://github.com/dpurge/typst-lib, MIT) — a language-learning notebook template. Use when the user mentions Typst, PDF output, printable lesson, or asks to typeset a lesson.
user-invocable: true
---

# PhraseForge Typst exporter

Generate a Typst (`.typ`) source file for a PhraseForge lesson, then compile it to PDF.

**Output target:** the [`dpurge-langnote`](https://github.com/dpurge/typst-lib) Typst package — a language-learning notebook template (MIT licensed). The generated `.typ` imports `@local/dpurge-langnote:0.0.1` and produces a standalone single-lesson document with title page, lesson body, and table of contents.

## Prerequisites

Install **`dpurge-langnote`** into Typst's local-packages directory **once** before compiling any output. See `references/typst-format.md` ("Prerequisite: install dpurge-langnote") for OS-specific paths. The tool itself does **not** install the package.

## When invoked

1. Get the conceptual lesson content from `phraseforge-core` and the matching `phraseforge-lang-<iso>`.
2. Assemble the content into a **JSON object** matching the schema in `references/typst-format.md`. Required fields: `title`, `lang`. Common optional fields: `script`, `date`, `vocabulary`, `models`, `source`, `transcription`, `translation`, `questions`, `exercises`.
3. Pipe the JSON to `typst-export.py`:
   ```bash
   echo '<lesson-json>' | uv run --script tools/typst-export.py --out lesson.typ
   ```
   Or write the JSON to a file first:
   ```bash
   uv run --script tools/typst-export.py --in lesson.json --out lesson.typ
   ```
4. Compile to PDF (the user runs this, or you run it via Bash if you have Typst installed):
   ```bash
   typst compile lesson.typ lesson.pdf
   ```
5. Confirm with a one-line message naming the `.typ` (and `.pdf` if compiled).

## Tool

```
uv run --script tools/typst-export.py [--in lesson.json] [--out lesson.typ] [--package-version 0.0.1]
uv run --script tools/typst-export.py --print-schema       # dump the JSON Schema
```

- `--in PATH` — JSON input path; default stdin (`-`).
- `--out PATH` — `.typ` output path; default stdout (`-`).
- `--package-version VER` — dpurge-langnote version pin; default `0.0.1`.
- `--print-schema` — print the JSON Schema generated from the Pydantic model and exit (used to refresh `references/lesson.schema.json`).

PEP-723 deps: `pydantic>=2.6`, `jinja2>=3.1` (cached after first run).

**Validation**: input JSON is parsed against the Pydantic `Lesson` model in `tools/lesson_schema.py`. Bad input exits `1` with a path-aware `ValidationError` on stderr (e.g. `lang: Field required`, `vocabulary.2.headword: Field required`, `source: tag 'poem' does not match expected tags 'text' / 'dialog'`). Read the path, fix the JSON, retry. The JSON Schema sidecar at `references/lesson.schema.json` is byte-identical to `phraseforge-anki/references/lesson.schema.json` — the same model serves both output skills.

**Rendering**: the actual `.typ` output is produced by a Jinja2 template at `tools/templates/lesson.typ.j2`. Edit that file to change formatting; the Python driver is intentionally thin.

## What the output looks like

```typst
#import "@local/dpurge-langnote:0.0.1": (
  LangNote, Lesson, Vocabulary, Models, Text, Dialog, Questions,
  Exercise, Instruction, TitlePage, TableOfContents,
)

#show: LangNote.with(
  title: "Bogini łowów Diana",
  author: none,
  native-lang: "pol",
  foreign-lang: "lat",
  foreign-script: "latn",
)

#TitlePage()

#Lesson(date: datetime(year: 2026, month: 6, day: 22))[
  #Vocabulary[ - Diana {N f sg} = Diana ]
  #Models(title: "Modele")[ - Diana est dea. ]
  #Text(title: "Tekst")[ Diana est dea silvarum et venationis. ]
  #Text(title: "Tłumaczenie")[ Diana to bogini lasów i łowów. ]
  #Exercise(number: "1")[
    #Instruction[Przetłumacz na polski:]
    - Diana est dea.
  ]
]

#TableOfContents()
```

## Constraints

- The tool emits source only. **Compilation** (`typst compile ...`) is a separate step and requires the user's local `typst` binary + `dpurge-langnote` installed.
- Section titles in the output are **Polish** by default (`Tekst`, `Tłumaczenie`, `Pytania`, …). Localized variants are a future enhancement.
- The tool **does not parse MDX** — it expects structured JSON. If you only have an MDX file, parse it back into JSON first, or hand the conceptual content from `phraseforge-core` directly into the tool.

## References

- `references/typst-format.md` — full JSON schema, dpurge-langnote function mapping, install instructions, compile-to-PDF walkthrough.
