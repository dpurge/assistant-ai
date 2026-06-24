---
name: phraseforge-lang-arb
description: Modern Standard Arabic (al-arabiyya al-fusha, ISO 639-3 arb) language conventions for PhraseForge lessons. Codes, RTL script, DIN 31635 transcription, vocabulary shape (root-pattern morphology, gender, nunation), and notes. Load whenever a PhraseForge lesson targets Modern Standard Arabic.
---

# Modern Standard Arabic (arb) language conventions

## Codes

- `lang`: `arb`
- `script`: `arab`

## Transcription

Required (non-Latin script). Use **DIN 31635** romanization system. System attribute: `DIN31635`.

Key correspondences:
| Arabic | DIN 31635 | | Arabic | DIN 31635 |
|--------|-----------|-|--------|-----------|
| ب | b | | ظ | ẓ |
| ت | t | | ع | ʿ |
| ث | ṯ | | غ | ġ |
| ج | ǧ | | ف | f |
| ح | ḥ | | ق | q |
| خ | ḫ | | ك | k |
| د | d | | ل | l |
| ذ | ḏ | | م | m |
| ر | r | | ن | n |
| ز | z | | ه | h |
| س | s | | و | w / ū |
| ش | š | | ي | y / ī |
| ص | ṣ | | ء | ʾ |
| ض | ḍ | | ى/ا | ā |

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Arabic-specific rules:

- **Nouns:** mark gender: `{N m}` / `{N f}`. For paradigm pairs (singular + broken plural), list both with `sg`/`pl`: `{N m sg}` / `{N m pl}`.
- **Verbs:** third-person masculine singular perfect (dictionary form). Tag `{V}`.
- **Adjectives:** masculine singular indefinite, tag `{Adj}`.
- Short vowels (harakat) should be included in headwords for learners at A1–B1.

```
كَلْبٌ {N m sg} = pies
كِلَابٌ {N m pl} = psy
بَيْتٌ {N m sg} = dom
اِمْرَأَةٌ {N f sg} = kobieta

كَتَبَ {V} = pisal; napisac
كَانَ {V irreg} = byl; byc
رَأَى {V irreg} = widziec

كَبِيرٌ {Adj} = duzy; wielki
صَغِيرٌ {Adj} = maly
```

Transcription examples: `kalbun`, `kilābun`, `baytun`, `imraʾatun`, `kataba`, `kāna`, `raʾā`, `kabīrun`, `ṣaġīrun`.

## Grammar notes (B1+)

- Root-pattern (trilateral root) morphology: note the 3-letter root for each verb and key derived nouns.
- Dual and plural agreement rules differ from European languages; note broken plural patterns.
- Verbs agree in gender and number with subject.

## Translation

Translate to Polish (`pol`).

## Notes

- Modern Standard Arabic (fusha) is used in formal writing and media. Distinguish from spoken dialects (apc — Levantine, arz — Egyptian) when the source uses colloquial forms.
- Arabic script is **right-to-left**; vocabulary and dialog entries are RTL.
