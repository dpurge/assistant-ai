# Exercises

Each lesson has 4–7 `<Exercise>` blocks. Every block declares its
`type=` plus `lang` and `script`.

## The Exercise wrapper

```mdx
<Exercise type="<type>" lang="<lang3>" script="<script>">

<Instruction><Polish instruction sentence.></Instruction>

<...type-specific body...>

</Exercise>
```

- `<Instruction>` is the **first child** of every Exercise and is in
  **Polish**. The Polish text inside `<Instruction>` always renders
  Latin LTR even when the rest of the Exercise body renders in a
  non-Latin script.
- Inside `<Instruction>`, wrap foreign-language fragments in `<L>`:
  `<L>سوريا</L>` keeps them in the target script.
- Blank lines around `<Instruction>` and the body are required so MDX
  parses things correctly.

## Helper components used in exercise bodies

| Component       | Use                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------- |
| `<Instruction>` | First paragraph of every Exercise — Polish instructions, Latin LTR.                      |
| `<L>`           | Inline wrapper for **foreign** fragments inside `<Instruction>` (Polish-context).        |
| `<N>`           | Inline wrapper for **Polish** fragments inside the Exercise body (foreign-script context). Used for multiple-choice prompts. |
| `<Hint>`        | Inline supplementary aside in the foreign script — for open-answer hints.                |
| `<WordBank>`    | Block — comma-separated foreign words rendered as a row of chips. For `fill-gaps`.       |
| `<Match>`       | Block — 2-column grid for `matching`.                                                    |
| `<Column>`      | Block — one column inside `<Match>`, optionally with its own `lang`/`script` override.   |

## Which exercises to include

Always:
- one `translation`
- one `fill-gaps`
- one `word-order`
- one `multiple-choice`

Optionally, when the text supports them:
- `matching` (e.g., for vocabulary review)
- `true-false` (for reading comprehension)
- `open-answer` (for production practice)

Total 4–7 exercises per lesson.

## Per-type structures

### `translation`

Numbered list of sentences. Direction depends on language.

```mdx
<Exercise type="translation" lang="arb" script="arab">

<Instruction>Przetłumacz następujące zdania na język polski.</Instruction>

1. لماذا فاض نهر الفرات في سوريا؟
2. قال إن المنطقة تجاوزت مرحلة الخطر.

</Exercise>
```

For Polish → Foreign translation:

```mdx
<Exercise type="translation" lang="arb" script="arab">

<Instruction>Przetłumacz następujące zdania na język arabski.</Instruction>

1. Dlaczego wezbrała rzeka Eufrat?
2. Powiedział, że region minął etap zagrożenia.

</Exercise>
```

### `fill-gaps`

`<WordBank>` (comma-separated foreign words) above the numbered
sentences. Sentences use `___` (3 or more underscores) for blanks.

```mdx
<Exercise type="fill-gaps" lang="arb" script="arab">

<Instruction>Uzupełnij luki w zdaniach słowami z ramki.</Instruction>

<WordBank>سوريا, فاض, المنطقة, الأمطار</WordBank>

1. لماذا ______ نهر الفرات في ______؟
2. قال إن ______ تجاوزت مرحلة الخطر.

</Exercise>
```

### `word-order`

Each item is a list of word fragments separated by ` / ` (slash with
spaces around it).

```mdx
<Exercise type="word-order" lang="arb" script="arab">

<Instruction>Ułóż poprawne zdania z podanych słów.</Instruction>

1. في / الفرات / نهر / سوريا / فاض / لماذا / ؟
2. إن / قال / الخطر / تجاوزت / المنطقة / مرحلة /.

</Exercise>
```

### `multiple-choice`

Each item: a Polish prompt wrapped in `<N>`, followed by indented
`a) / b) / c)` options in the foreign language.

```mdx
<Exercise type="multiple-choice" lang="arb" script="arab">

<Instruction>Wybierz poprawne tłumaczenie podanego słowa lub frazy.</Instruction>

1. <N>dlaczego</N>

   a) كيف
   b) لماذا
   c) أين

2. <N>rzeka Eufrat</N>

   a) نهر النيل
   b) نهر دجلة
   c) نهر الفرات

</Exercise>
```

Always 3 options labelled `a)`, `b)`, `c)`. Indent options by 3 spaces.

### `matching`

`<Match>` with two `<Column>` children. The second column overrides
`lang` and `script` so it renders in Polish (Latin) instead of the
Exercise's script.

```mdx
<Exercise type="matching" lang="cmn" script="hans">

<Instruction>Dopasuj chińskie zwroty do ich polskich znaczeń.</Instruction>

<Match>
<Column>

- A. 航天领域
- B. 重要目标
- C. 实现目标

</Column>
<Column lang="pol" script="latn">

1. dziedzina astronautyki
2. osiągnąć cele
3. ważne cele

</Column>
</Match>

</Exercise>
```

- Blank lines around `<Column>` opening and closing tags are required.
- Left column: foreign script, label items with `A.`, `B.`, `C.`…
- Right column: Polish, label items with `1.`, `2.`, `3.`…

### `true-false`

Numbered statements, each ending with `(Правда / Неправда)`-style
options written in the foreign language.

```mdx
<Exercise type="true-false" lang="ukr" script="cyrl">

<Instruction>Przeczytaj zdania i zdecyduj, czy są prawdziwe (Правда) czy fałszywe (Неправда).</Instruction>

1. FlixBus запустив маршрут до польського курортного міста. (Правда / Неправда)
2. Релігійні групи виступали проти поєднання номера 666 з назвою Гель. (Правда / Неправда)

</Exercise>
```

The `(true / false)` words in parentheses should be in the foreign
language so the student answers in that language.

### `open-answer`

Numbered foreign-language questions. Optional `<Hint>` after each with
target-language phrases the student should use.

```mdx
<Exercise type="open-answer" lang="cmn" script="hans">

<Instruction>Odpowiedz na pytania pełnymi zdaniami.</Instruction>

1. 为什么在火星上长期居住对于人类来说很重要？ <Hint>对于...非常重要, 生育</Hint>

2. 在太空中怀孕会带来哪些风险？ <Hint>受到辐射, 太空辐射, 胎儿</Hint>

</Exercise>
```

`<Hint>` content stays in the foreign language. Don't translate it.
