---
name: phraseforge-lang-heb
description: Hebrew (Ivrit, ISO 639-3 heb) language conventions for PhraseForge lessons. Codes, RTL Hebrew script, SBL transcription, vocabulary shape (gender, no indefinite article, definite ha-), and notes. Load whenever a PhraseForge lesson targets Hebrew.
---

# Hebrew (heb) language conventions

## Codes

- `lang`: `heb`
- `script`: `hebr`

## Transcription

Required (non-Latin script). Use **SBL Hebrew** (Society of Biblical Literature) transliteration for modern Hebrew. System attribute: `SBL`.

Key correspondences (simplified for modern Hebrew):
| Hebrew | SBL | | Hebrew | SBL |
|--------|-----|-|--------|-----|
| א | ʾ / silent | | ל | l |
| ב | v / b | | מ | m |
| ג | g | | נ | n |
| ד | d | | ס | s |
| ה | h | | ע | ʿ / silent |
| ו | v / u / o | | פ | f / p |
| ז | z | | צ | ts |
| ח | ḥ | | ק | q |
| ט | t | | ר | r |
| י | y / i | | ש | sh / s |
| כ | kh / k | | ת | t |

Vowels: standard Israeli pronunciation. Long vowels `ā ē ī ō ū` where relevant.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Hebrew-specific rules:

- **Nouns:** mark gender: `{N m}` / `{N f}`. No indefinite article in Hebrew; the definite article is the prefix `ה` (`ha-`). Use bare form as headword.
- **Verbs:** infinitive (with `ל`-prefix: `לכתוב`), or root form. Tag `{V}`. Mark binyan (verb pattern) when helpful: `{V qal}`, `{V piel}`, `{V hifil}`, etc.
- **Adjectives:** masculine singular form, tag `{Adj}`.

```
כלב {N m} = pies
בית {N m} = dom
אישה {N f} = kobieta
ילד {N m} = dziecko

לדבר {V piel} = mowic
לראות {V qal} = widziec
להיות {V qal irreg} = byc
להיות ל {Phrase} = miec

קטן {Adj} = maly
מהר {Adv} = szybko
```

Transcriptions: `kelev`, `bayit`, `ʾishāh`, `yéled`, `ledaber`, `lirʾot`, `lihyot`, `qatan`, `mahēr`.

## Grammar notes (B1+)

- Hebrew root (shoresh) system: 3-letter roots generate families of related words via binyanim (verb patterns) and mishkalim (noun patterns). Note the 3-letter root for each verb.
- Gender agreement: adjectives and verbs agree with the subject in gender and number.

## Translation

Translate to Polish (`pol`). Modern Hebrew has informal `אתה`/`את` (you m./f.) and no formal T-V distinction.

## Notes

- Hebrew script is **right-to-left**. Pointed text (with nikud vowel marks) is used in textbooks and recommended for A1–B1 learners.
- Biblical Hebrew vs. Modern Hebrew differ significantly; note which register the source uses.
