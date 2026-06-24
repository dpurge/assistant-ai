---
name: phraseforge-lang-hin
description: Hindi (Hindi, ISO 639-3 hin) language conventions for PhraseForge lessons. Codes, Devanagari script, IAST transcription, vocabulary shape (gender, postpositions, verb forms), and notes. Load whenever a PhraseForge lesson targets Hindi.
---

# Hindi (hin) language conventions

## Codes

- `lang`: `hin`
- `script`: `deva`

## Transcription

Required (non-Latin script). Use **IAST** (International Alphabet of Sanskrit Transliteration), which is also standard for modern Hindi. System attribute: `IAST`.

Key IAST correspondences:
| Devanagari | IAST | | Devanagari | IAST |
|------------|------|-|------------|------|
| अ | a | | ट | ṭ |
| आ | ā | | ठ | ṭh |
| इ | i | | ड | ḍ |
| ई | ī | | ढ | ḍh |
| उ | u | | ण | ṇ |
| ऊ | ū | | त | t |
| ए | e | | थ | th |
| ऐ | ai | | द | d |
| ओ | o | | ध | dh |
| औ | au | | न | n |
| क | k | | प | p |
| ख | kh | | फ | ph |
| ग | g | | ब | b |
| घ | gh | | भ | bh |
| च | c | | म | m |
| छ | ch | | य | y |
| ज | j | | र | r |
| झ | jh | | ल | l |
| श | ś | | व | v |
| ष | ṣ | | स | s |
| ह | h | | ं | ṃ (anusvara) |

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Hindi-specific rules:

- **Nouns:** mark gender: `{N m}` / `{N f}`. No definite/indefinite articles. Plural and case are formed by suffixes and postpositions.
- **Verbs:** infinitive form (ending `-nā`). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** masculine direct case (uninflected `-ā` form), tag `{Adj}`. Note: adjectives ending in `-ā` inflect; those ending in a consonant do not.

```
कुत्ता {N m} = pies
घर {N m} = dom
औरत {N f} = kobieta
बच्चा {N m} = dziecko

बोलना {V} = mowic
देखना {V} = widziec
होना {V irreg} = byc
रखना {V} = miec; trzymac

छोटा {Adj} = maly
जल्दी {Adv} = szybko
```

IAST transcriptions: `kuttā`, `ghar`, `aurat`, `baccā`, `bolnā`, `dekhnā`, `honā`, `rakhnā`, `choṭā`, `jaldī`.

## Grammar notes (B1+)

- Hindi word order is **SOV**. Postpositions follow nouns (unlike European prepositions).
- Verb agreement is primarily with the object (in perfective aspect) or subject; depends on tense/aspect.
- Oblique case: nouns change form before postpositions.

## Translation

Translate to Polish (`pol`). Hindi `तुम` (`tum`) → informal; `आप` (`āp`) → formal (`Pan`/`Pani`).

## Notes

- Hindi and Urdu are mutually intelligible at the colloquial level but diverge in formal/literary vocabulary (Hindi draws on Sanskrit, Urdu on Persian/Arabic).
- Devanagari is written left-to-right.
