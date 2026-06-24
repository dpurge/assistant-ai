---
name: phraseforge-lang-aze
description: Azerbaijani (Azerbeycan dili, ISO 639-3 aze) language conventions for PhraseForge lessons — Latin script variant. Codes, vocabulary shape (agglutinative, no gender, vowel harmony), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Azerbaijani.
---

# Azerbaijani (aze) language conventions

## Codes

- `lang`: `aze`
- `script`: `latn`

Note: Azerbaijani uses Latin script in Azerbaijan (since 1991) and Cyrillic in Russia. phraseforge-data uses `aze-latn`. This skill covers the Latin variant.

## Transcription

Not needed. Azerbaijani uses Latin script. Preserve: `ç ğ ı İ ö ş ü ə`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Azerbaijani-specific rules closely follow Turkish (the two languages are closely related):

- **No grammatical gender, no articles.** All nouns take `{N}`.
- **Verbs:** infinitive (ending `-maq`/`-mək`). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
it {N} = pies
ev {N} = dom
qadin {N} = kobieta
usaq {N} = dziecko

danismaq {V} = mowic
gormek {V} = widziec
olmaq {V} = byc
sahib olmaq {V} = miec

kicik {Adj} = maly
tez {Adv} = szybko
```

(Actual headwords: `it`, `ev`, `qadın`, `uşaq`, `danışmaq`, `görmək`, `olmaq`, `kiçik`, `tez`.)

## Grammar notes (B1+)

- **Agglutinative SOV** with vowel harmony (back/front, rounded/unrounded), closely parallel to Turkish.
- Azerbaijani has 6 cases (nominative, genitive, dative, accusative, locative, ablative).

## Translation

Translate to Polish (`pol`). Azerbaijani `sən` → informal; `siz` → formal/plural (`Pan`/`Pani`/`wy`).
