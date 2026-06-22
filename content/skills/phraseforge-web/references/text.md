# Text section

`<Text>` is the unified component for any prose content in a lesson —
the original foreign-language text, a romanized transliteration of
it, and the Polish translation. One component, one set of rules. An
`as` attribute marks the role the block plays:

| `as` value         | Role                                                          | Default |
| ------------------ | ------------------------------------------------------------- | ------- |
| `source`           | Primary foreign-language text                                 | yes     |
| `transcription`    | Romanized/transliterated rendering (only for non-Latin scripts) | —     |
| `translation`      | Polish translation                                            | —       |

Omit `as` for the primary text — `<Text lang="…" script="…">` is the
same as `<Text as="source" lang="…" script="…">`.

For conversation content, use the `dialog` code fence — it supports
the same `as` attribute. See `references/dialog.md`.

## Shape

```mdx
<Text lang="<lang3>" script="<script>">

## <Foreign-language heading>

<First foreign-language paragraph.>

<Second foreign-language paragraph.>

</Text>

<Text as="transcription" lang="<lang3>" script="<script>" system="<system name>">

## <Transliterated heading>

<Transliterated paragraphs.>

</Text>

<Text as="translation" lang="pol" script="latn">

## <Polish heading>

<Polish paragraphs.>

</Text>
```

## Rules — applies to every `<Text>`

- Always start the body with a level-2 Markdown heading `## <title>`
  matching the role (foreign-language heading for source, transliterated
  heading for transcription, Polish heading for translation).
- Prose paragraphs separated by blank lines.
- **Blank lines must surround the `<Text>` opening and closing tags**
  so MDX parses the inside as Markdown.
- Don't put bullet lists or tables inside `<Text>` unless the source
  text actually has them.
- Use the language's native quotation marks (e.g. `„...”` for Polish,
  `"..."` or `« ... »` for others).
- Don't mix roles in one block — keep source, transcription, and
  translation as separate `<Text>` blocks.

## `as="source"` — primary text

The adapted foreign-language source. This is the default.

```mdx
<Text lang="deu" script="latn">

## Warum lernt jeder Deutsch?

Deutsch ist eine wichtige Sprache in Europa. Viele Menschen lernen
Deutsch, weil sie in Deutschland arbeiten möchten.

Andere lernen die Sprache, weil sie deutsche Bücher lesen wollen.

</Text>
```

```mdx
<Text lang="arb" script="arab">

## لماذا فاض نهر الفرات في سوريا؟

فايز عباس، رئيس لجنة الطوارئ في دير الزور، قال إن المنطقة تجاوزت
مرحلة الخطر بعد ارتفاع مياه نهر الفرات.

</Text>
```

## `as="transcription"` — romanized text

Include **only** when the script is not `latn`, `cyrl`, or `grek`.
Latin, Cyrillic, and Greek scripts are read directly — no
transcription needed.

The transcription should mirror the source paragraph-for-paragraph,
heading-for-heading. The `system` prop names the transliteration
scheme (badge in the Shell header).

```mdx
<Text as="transcription" lang="arb" script="latn" system="DIN 31635">

## Limaḏā fāḍa nahru al-Furāt fī Sūriyā?

Fāyiz ʿAbbās, raʾīsu laǧnati aṭ-Ṭawāriʾ fī Dair az-Zūr, qāla inna
al-minṭaqata taǧāwazat marḥalata al-ḫaṭari baʿda irtifāʿi miyāhi nahri
al-Furāt.

</Text>
```

Note: `script="latn"` because the **rendered** transliteration is in
Latin script, even though the source script is `arab`.

### Transcription system per source script

| Source script | `system` attribute       | Notes                            |
| ------------- | ------------------------ | -------------------------------- |
| `arab`        | `"DIN 31635"`            | Standard German DIN romanization |
| `hebr`        | `"ISO 259"`              | ISO 259 academic transliteration |
| `syrc`        | `"ALA-LC"`               | ALA-LC romanization              |
| `hans`        | `"Hanyu Pinyin"`         | Pinyin with tone marks           |
| `hant`        | `"Hanyu Pinyin"`         | Pinyin with tone marks           |
| `jpan`        | `"Hepburn"`              | Modified Hepburn                 |
| `kore`        | `"Revised Romanization"` | Official South-Korean RR         |
| `armn`        | `"BGN/PCGN"`             | BGN/PCGN romanization            |
| `geor`        | `"National"`             | Georgian National                |
| `mong`        | `"VPMC"`                 | Vertical Pre-Modern Cyrillic     |

If unsure, use the most common Western academic system for that script.

## `as="translation"` — Polish translation

Always `lang="pol" script="latn"` for the default Polish locale of
the repo. For the English mirror file you write `lang="eng"
script="latn"` — see `references/english-i18n.md`.

- Translate paragraph-for-paragraph. Same number and order of
  paragraphs as the source `<Text>`.
- The heading translates the source heading.
- Use real Polish letters: `ą ę ć ł ń ó ś ź ż`. Don't strip
  diacritics.
- Use Polish-style quotation marks `„...”` for direct quotes.
- Keep proper nouns spelled correctly in Polish (transliterate from
  the source script when necessary).
- Don't add commentary or notes that aren't in the source.

```mdx
<Text as="translation" lang="pol" script="latn">

## Dlaczego wezbrała rzeka Eufrat w Syrii?

Fāyiz ʿAbbās, przewodniczący komisji ds. sytuacji nadzwyczajnych w
Dajr az-Zaur, powiedział, że region minął etap zagrożenia po
podniesieniu się poziomu wód w rzece Eufrat.

</Text>
```
