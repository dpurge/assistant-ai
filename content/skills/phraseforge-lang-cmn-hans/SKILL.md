---
name: phraseforge-lang-cmn-hans
description: Mandarin Chinese Simplified (Putonghua, ISO 639-3 cmn, Simplified script hans) language conventions for PhraseForge lessons. Codes, Pinyin transcription, vocabulary shape (measure words, no gender/articles), and notes. Load whenever a PhraseForge lesson targets Mandarin in Simplified Chinese.
---

# Mandarin Chinese — Simplified (cmn, hans) language conventions

## Codes

- `lang`: `cmn`
- `script`: `hans`

## Transcription

Required (non-Latin script). Use **Pinyin** with tone marks. System attribute: `Pinyin`.

Tones: 1st (ā), 2nd (á), 3rd (ǎ), 4th (à), neutral/5th (a, unmarked).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Mandarin-specific rules:

- **No grammatical gender, no articles, no inflection.** All nouns take `{N}`.
- **Measure words (classifiers):** note the primary measure word for countable nouns: `{N cl ge}` (general 个), `{N cl ben}` (books 本), `{N cl zhi}` (animals 只), etc.
- **Verbs:** uninflected stem, tag `{V}`. Add `irreg` for the handful of irregular forms.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
狗 {N cl zhi} = pies
房子 {N cl ge} = dom
女人 {N cl ge} = kobieta
孩子 {N cl ge} = dziecko

说话 {V} = mowic
看见 {V} = widziec
是 {V} = byc (jest)
有 {V} = miec

小 {Adj} = maly
快 {Adv} = szybko
```

Pinyin: `gǒu`, `fángzi`, `nǚrén`, `háizi`, `shuōhuà`, `kànjiàn`, `shì`, `yǒu`, `xiǎo`, `kuài`.

## Grammar notes (B1+)

- Chinese is **tonal** (4 tones + neutral); tone is part of the pronunciation of every syllable.
- **Topic-prominent** and **SOV/SVO** word order depending on construction.
- Aspect particles (了 `le`, 过 `guò`, 着 `zhe`) mark perfectivity, experience, ongoing state — not tense.
- Measure words are mandatory between a numeral and a noun.

## Translation

Translate to Polish (`pol`). Chinese `你` (`nǐ`) → informal; `您` (`nín`) → formal (`Pan`/`Pani`).

## Notes

- Use Simplified characters (mainland China standard). For Traditional, see `phraseforge-lang-cmn-hant`.
- HSK vocabulary levels (HSK 1–9) can be noted in parentheses as notes when helpful.
