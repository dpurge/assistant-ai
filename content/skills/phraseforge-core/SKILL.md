---
name: phraseforge-core
description: Core PhraseForge lesson-authoring workflow — output-format-agnostic. Use whenever the user asks to create, generate, write, or adapt a phraseforge lesson; or pastes/links a text and asks for vocabulary + exercises. Detects language and script, picks CEFR level, adapts the text, builds vocabulary/models/translation/transcription/questions/exercises, then hands off to an output skill (phraseforge-web for MDX/Docusaurus, phraseforge-anki for flashcards, phraseforge-typst for PDF).
---

# PhraseForge lesson author (core)

You produce the **conceptual content** of a PhraseForge lesson — adapted source text, vocabulary, models, translation, optional transcription, optional questions, exercises — and hand off to an output skill to render it. This skill itself does **not** write any file or care about the target format.

Lesson text and explanations are **in Polish by default**.

## When invoked

Follow these steps in order. Don't skip.

1. **Get the source** the user supplied:
   - Inline text → use directly.
   - URL → fetch it via the host's web-fetch tool. Strip nav/ads, keep the article body.
   - File path → read it with the host's file-read tool.
2. **Detect the foreign language.** Map to 3-letter ISO 639-3. Quick lookup for common cases:

   | Language | `lang` | `script` |
   |---|---|---|
   | German | `deu` | `latn` |
   | Spanish | `spa` | `latn` |
   | French | `fra` | `latn` |
   | Italian | `ita` | `latn` |
   | English | `eng` | `latn` |
   | Polish | `pol` | `latn` |
   | Russian | `rus` | `cyrl` |
   | Modern Greek | `ell` | `grek` |
   | Latin | `lat` | `latn` |
   | Arabic | `arb` | `arab` |
   | Hebrew | `heb` | `hebr` |
   | Mandarin (simplified) | `cmn` | `hans` |
   | Japanese | `jpn` | `jpan` |
   | Korean | `kor` | `kore` |

   For anything not above, load `references/languages.md` for the full table.
3. **Load the matching language skill** if one exists:
   - German → read `phraseforge-lang-deu/SKILL.md`.
   - Spanish → read `phraseforge-lang-spa/SKILL.md`.
   - Anything else → no language skill yet; proceed with general conventions and ask the user if a per-language quirk matters.

   Per-language skills carry: transcription system (if non-Latin), vocabulary shape (article + gender for nouns, conjugation hints for verbs), inflection-table format, formality defaults.
4. **Pick the CEFR level** (`a1`–`c2`, lowercase). Ask the user if unsure. Read `references/levels.md` for word-count and grammar targets.
5. **Adapt the source text** to the target level — simplify vocabulary and grammar to match. Aim for the word-count targets in `references/levels.md`. Keep the meaning. Stay in coherent prose (no bullet lists).
6. **Extract vocabulary** — 15–40 entries depending on level. Each entry: foreign headword, grammar tag, Polish gloss. The exact shape (article placement, gender markers, etc.) comes from the language skill loaded in step 3. **When an entry has multiple senses, separate them in the Polish translation with `; ` (semicolon + space)** — e.g. `"wszyscy; wszystkie"`, `"dzień dobry; cześć"`.
7. **Build models** — 3–6 progressive phrase patterns that illustrate the constructions used in the source.
8. **Compose translation** — Polish prose translation of the source.
9. **Compose transcription** if the script is non-Latin (`arab`, `hans`, `jpan`, `kore`, `hebr`, etc.) — using the transcription system the language skill specifies.
10. **Compose questions** (optional) — open-ended comprehension prompts in the foreign language.
11. **Compose exercises** — at least four, mixing types. Always include translation, fill-gaps, word-order, and multiple-choice; add matching, true-false, open-answer when the text supports them.
12. **Hand off to the output skill the user named.** Default: `phraseforge-web` (MDX). Other options: `phraseforge-anki` (flashcards), `phraseforge-typst` (PDF). The output skill owns the file path, format, and rendering details. For `phraseforge-typst` and `phraseforge-anki`, assemble the conceptual content into a JSON object (the lesson schema documented in each output skill's `references/`) and pipe it to the matching `tools/*-export.py`. The two output skills consume the **same JSON shape**, so build it once and route to whichever output the user asked for.

## Output

You don't write the lesson file yourself — the output skill does. After it returns, reply with a single short sentence naming the file(s) authored. Don't print the lesson content back to the user.

## Constraints

- `lang` is always a 3-letter ISO 639-3 code (`arb`, `cmn`, `deu`, `pol`…).
- `script` is always a 4-letter ISO 15924 code in lowercase (`arab`, `hans`, `latn`, `cyrl`, `grek`, `hebr`, `jpan`, `kore`…).
- All Polish text uses UTF-8 Polish letters (`ą ę ć ł ń ó ś ź ż`). Don't strip diacritics.
- Stay concise.

## References

- `references/languages.md` — language + script code tables (high-level index; per-language detail lives in the `phraseforge-lang-<iso>` skills).
- `references/levels.md` — CEFR levels and adaptation targets (word counts, grammar scope).

## Sister skills

- `phraseforge-lang-<iso>` — per-language conventions (transcription, vocab shape, inflection, formality). Always load the one matching the source language.
- `phraseforge-web` — render as MDX into the phraseforge-web Docusaurus repo. **Default output target.** Owns file path, MDX components, i18n mirror.
- `phraseforge-anki` — export vocabulary as Anki flashcards (stub).
- `phraseforge-typst` — export the lesson as a Typst `.typ` source for PDF (stub).

## Tools

Invoke every tool via `uv run --script` so its [PEP 723](https://peps.python.org/pep-0723/) inline deps are resolved into uv's cache on first run.

- `tools/ff-parser.py` — parse a `*.ff` PhraseForge source file and emit a `Lesson` JSON object compatible with the output skills.

  **Usage:**
  ```
  # Emit all chunks as a JSON array:
  uv run --script tools/ff-parser.py path/to/source.ff

  # Emit a single chunk (1-based) as a single Lesson JSON object:
  uv run --script tools/ff-parser.py path/to/source.ff --chunk 1

  # Write to a file instead of stdout:
  uv run --script tools/ff-parser.py path/to/source.ff --chunk 1 --out lesson.json

  # Print the Lesson JSON Schema and exit:
  uv run --script tools/ff-parser.py --print-schema
  ```

  **Field mapping from `.ff` to `Lesson`:**

  | `.ff` header field | `Lesson` field |
  |---|---|
  | `document` | `title` (chunk id appended as `/ <id>`) |
  | `description` | `description` |
  | `data.language` | `lang` |
  | `data.script` | `script` |
  | `translation.language` | `translation_lang` |
  | `translation.script` | `translation_script` |

  **Vocabulary items:** `phrase.text` → `headword`; `phrase.grammar.text` → `grammar`; `phrase.transcription` → `transcription`; `translations` joined with `"; "` → `translation`; `notes` joined with `"; "` → `notes`.

  **Dialog body:** The raw `@Speaker:` / `--:` / indented-body format is parsed into a structured `DialogSource` with typed `DialogTurn` and `Narration` items, matching the phraseforge-web remark plugin conventions.

  **Pipe output to an export tool:**
  ```
  uv run --script tools/ff-parser.py source.ff --chunk 1 \
    | uv run --script ../phraseforge-web/tools/mdx-export.py --out lesson.mdx
  ```
