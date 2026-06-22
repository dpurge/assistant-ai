# Dialog section

For conversation-based lessons (dialogues, interviews, drama), use the
`dialog` code fence **instead of** `<Text>`. The fence captures
speaker turns as structured units, which renders with speaker labels
and gives downstream tooling (exercises, i18n, translation) something
real to hook into.

When the source is plain prose, keep using `<Text>`.

## Shape

````mdx
```dialog lang=<lang3> script=<script>
# <Optional title in the foreign language>

<Optional narration paragraphs.>

@<Speaker>:
  <First line of speaker's turn.>
  <Second line — joined into one paragraph with the first.>

  <Second paragraph of the same turn — separated by a blank line.>

@<Other speaker>:
  <Their turn.>

--:
  <Anonymous turn — no speaker label, e.g. stage direction, off-screen voice.>
```
````

## Parsing rules

These are enforced by the remark plugin at build time:

1. **Title** (optional). The first non-blank line, if it starts with
   `# `, becomes the dialog title. Lifted into a `title` attribute on
   the rendered Dialog. Subsequent `#` lines are not treated as titles.
2. **Speaker turn header**. A non-indented line matching `@<Name>:`
   starts a named turn. Speaker names can contain spaces, diacritics,
   hyphens — anything except `:`.
3. **Anonymous turn header**. A non-indented line equal to `--:` starts
   a turn with no speaker label (renders an em-dash in the speaker
   column).
4. **Turn body**. Lines indented with 2 spaces, 4 spaces, or a tab
   belong to the most recent turn. The indent is stripped before
   parsing. Inside the body:
   - Consecutive non-blank lines join into one paragraph (newlines
     collapse to spaces).
   - A blank line separates paragraphs within the turn.
   - Body text is parsed as Markdown — `**bold**`, `*italic*`,
     `` `code` ``, `[link](url)` all work.
5. **Body termination**. A non-indented non-blank line ends the
   current turn. It then starts a new turn header (if it matches) or
   becomes a narration paragraph.
6. **Narration paragraph**. A non-indented non-blank line that is not
   a title or turn header becomes a top-level narration paragraph
   between turns. Also Markdown.

## Rules

- `lang` and `script` are required meta attributes on the code fence,
  same convention as `vocabulary` / `models`.
- Title goes inside the fence body on its own line (`# ...`). Don't
  put the title as a fence meta attribute.
- Use a consistent indent (2 spaces is recommended) for all turn
  bodies in a file.
- Don't nest `dialog` inside another lesson block.
- MDX JSX inside turn bodies (`<L>`, `<N>`) is **not** supported in
  the first release. Use plain Markdown only for now.

## The `as` attribute

Like `<Text>`, the `dialog` fence carries an `as` meta attribute that
marks the role the block plays in the lesson:

| `as` value      | Role                                                    | Default |
| --------------- | ------------------------------------------------------- | ------- |
| `source`        | Primary foreign-language dialog                         | yes     |
| `transcription` | Romanized/transliterated rendering (non-Latin sources)  | —       |
| `translation`   | Polish translation of the dialog                        | —       |

Omit `as` for the primary dialog. For transcription and translation,
write the same dialog structure (title, narration, turns) in the
target script/language — the turn shapes stay parallel across the
three fences so the reader can compare them line-for-line.

````mdx
```dialog lang=arb script=arab
# مكالمة قصيرة

@أحمد:
  مرحبا!
  كيف حالك؟

@فاطمة:
  بخير، شكرا.
```

```dialog as=transcription lang=arb script=latn system="DIN 31635"
# Mukālamatun qaṣīratun

@Aḥmad:
  Marḥabā!
  Kayfa ḥāluka?

@Fāṭima:
  Bi-ḫair, šukran.
```

```dialog as=translation lang=pol script=latn
# Krótka rozmowa

@Ahmed:
  Cześć!
  Jak się masz?

@Fatima:
  Dobrze, dziękuję.
```
````

A `transcription` dialog should mirror the source paragraph-for-paragraph
and turn-for-turn. A `translation` dialog should preserve speaker
labels (translated where appropriate, e.g. Arabic أحمد → Polish Ahmed).

## Example

````mdx
```dialog lang=pol script=latn
# Przykładowa rozmowa

Jan wita się z Martą na ulicy.

@Jan:
  Cześć!
  Gdzie idziesz?

@Marta:
  Cześć, **Jan**!
  Idę do szkoły.

  Jutro mamy *egzamin*.

--:
  W tle słychać muzykę.
```
````

renders as:

- A "Dialog" panel with title "Przykładowa rozmowa".
- A narration paragraph: "Jan wita się z Martą na ulicy."
- Turn 1: speaker "Jan", body "Cześć! Gdzie idziesz?"
- Turn 2: speaker "Marta", first paragraph "Cześć, **Jan**! Idę do
  szkoły." (with Markdown bold rendered), second paragraph "Jutro
  mamy *egzamin*." (with italic rendered).
- Turn 3: anonymous (em-dash), body "W tle słychać muzykę."

## When to use a dialog fence

Use `dialog` instead of `<Text>` whenever the source is a
conversation, interview, drama, or any speaker-attributed text.
Within a dialog lesson, every content role is a `dialog` fence with
the appropriate `as`:

1. `vocabulary` code fence
2. `models` code fence
3. `dialog` code fence (no `as`, or `as=source`) — primary content
4. `dialog as=transcription` — only when script is not `latn` / `cyrl` / `grek`
5. `dialog as=translation` — Polish translation, structured as a dialog
6. Exercises

You can also mix: a primary `dialog` fence followed by a Polish
`<Text as="translation">` if you prefer the translation rendered as
flat prose rather than turns. The two styles are interchangeable.
