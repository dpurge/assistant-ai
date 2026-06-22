---
name: phraseforge-web
description: Render a PhraseForge lesson as an MDX file in the phraseforge-web Docusaurus repo at /Users/jprusaczyk/Documents/src/phraseforge-web (upstream https://github.com/dpurge/phraseforge-web). Handles file-path conventions, the MDX section order, the registered MDX component vocabulary, and the optional English i18n mirror. This is the default output target for phraseforge-core.
user-invocable: true
---

# PhraseForge-Web lesson target

Render a PhraseForge lesson (produced by `phraseforge-core` + the matching `phraseforge-lang-<iso>`) as a single MDX file in the **phraseforge-web** Docusaurus site at `/Users/jprusaczyk/Documents/src/phraseforge-web`.

This skill owns all MDX/Docusaurus-specific concerns:

- File path under `docs/<lang3>/<level>/<YYYY-MM-DD>-<seq>.mdx`.
- MDX section order and component vocabulary.
- The optional English i18n mirror at `i18n/en/docusaurus-plugin-content-docs/current/<lang3>/<level>/<same-filename>.mdx`.
- The `assets/lesson-template.mdx` skeleton.

## Skeleton (section order — fill in the placeholders)

```mdx
---
title: <Polish title>
description: <Polish one-liner>
---

# <Polish title>

```vocabulary lang=<lang3> script=<script>
<headword> {<grammar tag>} — <Polish gloss>
... (15–40 entries)
```

```models lang=<lang3> script=<script>
<phrase pattern 1>
... (3–6 groups, 20–60 lines total)
```

<Text as="source" lang="<lang3>" script="<script>">
<adapted source text>
</Text>

<!-- Transcription block: only if script is non-Latin (not latn/cyrl/grek). -->
<Text as="transcription" lang="<lang3>" script="latn" system="<DIN31635|Pinyin|Hepburn|...>">
<romanized text>
</Text>

<Text as="translation" lang="pol" script="latn">
<Polish translation>
</Text>

<!-- Optional. -->
<Questions lang="<lang3>" script="<script>">
1. <question 1>
2. <question 2>
</Questions>

<Exercise type="translation" lang="<lang3>" script="<script>">
<Instruction>Przetłumacz na polski:</Instruction>
- <foreign sentence 1>
- <foreign sentence 2>
</Exercise>

<!-- 3 more <Exercise> blocks: fill-gaps, word-order, multiple-choice. Add matching/true-false/open-answer if the text supports them. -->
```

For dialog source content, use a `dialog` code fence instead of `<Text as="source">` (same `as=` attribute supported for transcription / translation). See `references/dialog.md`.

## When invoked

1. Get the conceptual lesson content from `phraseforge-core` (adapted text, vocabulary, models, translation, transcription, questions, exercises).
2. Apply the matching `phraseforge-lang-<iso>` for per-language conventions.
3. **Build the lesson JSON object** matching the schema in `references/lesson.schema.json` (same shape as `phraseforge-typst` and `phraseforge-anki` consume). Required: `title`, `lang`; common optional: `script`, `date`, `description`, `vocabulary`, `models`, `source`, `transcription`, `translation`, `questions`, `exercises`.
4. **Pick the file path** per `references/lesson-file.md`. List the directory first to find a free letter for the day. Create the level directory if it doesn't exist; don't invent a `_category_.json`.
5. **Run `mdx-export.py`** to render the JSON as MDX:
   ```bash
   echo '<lesson-json>' | uv run --script tools/mdx-export.py --out <full-path>.mdx
   ```
   Or from a file:
   ```bash
   uv run --script tools/mdx-export.py --in lesson.json --out <full-path>.mdx
   ```
6. If the user requested an **English mirror**, build a second JSON with Polish strings translated to English and `lang: "eng"` for the translation block, then render to the i18n mirror path per `references/english-i18n.md`.

## Tool

```
uv run --script tools/mdx-export.py [--in lesson.json] [--out lesson.mdx]
uv run --script tools/mdx-export.py --print-schema       # dump the JSON Schema
```

- `--in PATH` — JSON input path; default stdin (`-`).
- `--out PATH` — `.mdx` output path; default stdout (`-`).
- `--print-schema` — print the JSON Schema generated from the Pydantic model and exit.

PEP-723 deps: `pydantic>=2.6`, `jinja2>=3.1` (cached after first run).

**Validation**: input JSON is parsed against the Pydantic `Lesson` model in `tools/lesson_schema.py` — the same model `phraseforge-typst` and `phraseforge-anki` use. Bad input exits `1` with a path-aware `ValidationError` on stderr.

**Rendering**: section order and MDX component vocabulary are produced by `tools/templates/lesson.mdx.j2`. Dialog code-fence body (narration, `@Speaker:`, `--:`, multi-paragraph turns) is composed in the Python driver since Jinja whitespace control can't reliably preserve the 2-space indentation phraseforge-web's parser requires.

## Output

The tool writes a single `.mdx` file (plus an i18n mirror if you render one). Reply with a one-line confirmation of the file path(s). Don't print the lesson content back to the user.

## Constraints

Only use MDX components registered in the phraseforge-web repo at `src/components/LessonElement/`:

- `<Text>` — with optional `as="source"`, `as="transcription"`, `as="translation"`.
- `<Questions>` — same `as` attribute.
- `<Exercise>`, `<Instruction>`, `<L>`, `<N>`, `<Hint>`, `<WordBank>`, `<Match>`, `<Column>`.
- Code fences: `vocabulary`, `models`, `dialog` (`dialog` supports the same `as` attribute).

Don't invent new components.

## References

- `references/workflow.md` — full step-by-step rendering walkthrough.
- `references/lesson-file.md` — file path, naming, frontmatter, section order.
- `references/english-i18n.md` — English mirror conventions.
- `references/vocabulary.md` — vocabulary code-fence format.
- `references/models.md` — models code-fence format.
- `references/text.md` — `<Text>` component (prose), covers `as="source"`, `"transcription"`, `"translation"`.
- `references/dialog.md` — `dialog` code fence (conversations), same `as` attribute.
- `references/questions.md` — `<Questions>` block for open-ended comprehension prompts.
- `references/exercises.md` — all 7 exercise types and their components.
- `assets/lesson-template.mdx` — copy-paste skeleton with placeholders.
