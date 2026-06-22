# Lesson file format

## File path

```
docs/<lang3>/<level>/<YYYY-MM-DD>-<seq>.mdx
```

Example: `docs/arb/a2/2026-06-10-a.mdx`.

`<seq>` starts at `a` and increments for the second, third lesson of the
same day. List the directory before deciding.

## Frontmatter

```yaml
---
title: "<Polish title of the lesson>"
description: "<short description in Polish, often: 'Adaptacja artykułu BBC z YYYY-MM-DD: <source URL>'>"
---
```

`description` is plain prose. If the source has no URL (file/inline), use
a short Polish description without a URL.

## H1 heading

Right after the frontmatter, repeat the title as an H1 heading:

```mdx
# <Polish title of the lesson>
```

## Section order

Always in this order. Skip a section only when noted.

1. `vocabulary` code fence
2. `models` code fence
3. **Source content** — `<Text>` JSX **or** `dialog` code fence
   (no `as`, or `as=source`). Use `dialog` for
   conversation/interview/drama sources; `<Text>` for prose.
4. **Transcription** — `<Text as="transcription">` or
   `dialog as=transcription`, matching the shape of step 3.
   **Skip** when source script is `latn`, `cyrl`, or `grek`.
5. **Translation** (Polish) — `<Text as="translation">` or
   `dialog as=translation`. The two styles are interchangeable;
   pick whichever reads better.
6. **Questions** (optional) — `<Questions>` for open-ended
   comprehension/discussion prompts. Supports the same `as`
   attribute, so non-Latin lessons can mirror with
   `<Questions as="transcription">` and `<Questions as="translation">`.
   See `references/questions.md`.
7. Exercises — at least 4 `<Exercise>` blocks of mixed types.

Separate each section by a single blank line. See
`references/text.md` and `references/dialog.md` for the `as`
attribute reference.

## Skeleton

See `assets/lesson-template.mdx` for a copy-paste skeleton with
placeholders marked `<...>`.
