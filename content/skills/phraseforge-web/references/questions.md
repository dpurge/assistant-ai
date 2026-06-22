# Questions section

`<Questions>` renders an open-ended question list — comprehension or
discussion prompts about the source content. Optional. Sits between
Translation and Exercises in the lesson order. Use it when you want
the reader to engage with the text in their own words, not when you
want a structured exercise.

For graded production practice, prefer `<Exercise type="open-answer">`
(see `references/exercises.md`) — those have `<Hint>` slots and
formal instructions. `<Questions>` is the lighter-weight "now stop
and think" block.

## Shape

JSX wrapper with a real Markdown ordered list inside. Blank lines
around the opening and closing tags are required so MDX parses the
embedded list as Markdown.

```mdx
<Questions lang="<lang3>" script="<script>">

1. <First question.>
2. <Second question.>
3. <Third question.>

</Questions>
```

Markdown formatting (`**bold**`, `*italic*`, links, inline `<L>` /
`<N>`) works inside list items.

## The `as` attribute

Same vocabulary as `<Text>` and `dialog`:

| `as` value         | Role                                      | Shell label   |
| ------------------ | ----------------------------------------- | ------------- |
| `source` (default) | Primary questions in the foreign language | Pytania       |
| `transcription`    | Romanized rendering                       | Transkrypcja  |
| `translation`      | Polish translation of the questions       | Tłumaczenie   |

For non-Latin sources, mirror the questions block with a
transcription and a Polish translation, in the same way you mirror
the source `<Text>`.

## Rules

- Always wrap the questions in an ordered list (`1.`, `2.`, …) — not
  paragraphs and not a bullet list.
- Blank lines around the `<Questions>` open/close tags.
- One question per list item. Don't split a single question across
  multiple items.
- Keep questions short. If a prompt needs context, put the context in
  the preceding `<Text>`, not inside the question.
- For non-Latin source scripts, add a `<Questions as="transcription">`
  mirror block (with `script="latn"` and a `system` attribute) and a
  `<Questions as="translation">` mirror block (with `lang="pol"
  script="latn"`).

## Example (Polish source)

```mdx
<Questions lang="pol" script="latn">

1. Co było pierwsze, jajko czy kura?
2. Kto nie ma zeszytu?
3. Z kim wita się Jan?

</Questions>
```

## Example (Arabic source with mirror blocks)

```mdx
<Questions lang="arb" script="arab">

1. ما اسمك؟
2. من أين أنت؟

</Questions>

<Questions as="transcription" lang="arb" script="latn" system="DIN 31635">

1. Mā ismuka?
2. Min ayna anta?

</Questions>

<Questions as="translation" lang="pol" script="latn">

1. Jak masz na imię?
2. Skąd jesteś?

</Questions>
```

## When to use `<Questions>` vs `<Exercise type="open-answer">`

| Use `<Questions>` when…                                  | Use `<Exercise type="open-answer">` when…             |
| --------------------------------------------------------- | ------------------------------------------------------ |
| You want unstructured comprehension prompts.              | You want graded production practice.                   |
| The reader thinks but doesn't necessarily write.          | The reader writes full-sentence answers.               |
| You don't want hints, instructions, or exercise framing.  | You want `<Hint>` slots and a Polish `<Instruction>`.  |
| You want a transcription/translation mirror naturally.    | The exercise is monolingual.                           |
