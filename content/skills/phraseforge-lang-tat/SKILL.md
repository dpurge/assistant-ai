---
name: phraseforge-lang-tat
description: Tatar (Tatar tele, ISO 639-3 tat) language conventions for PhraseForge lessons — Cyrillic script variant as in phraseforge-data. Codes, vocabulary shape (agglutinative, no gender), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Tatar.
---

# Tatar (tat) language conventions

## Codes

- `lang`: `tat`
- `script`: `cyrl`

Note: Tatar uses Cyrillic in Tatarstan/Russia. A Latin-based alphabet exists but is not official.

## Transcription

Not required by default (Cyrillic excluded from transcription block).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Tatar-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`.
- **Verbs:** infinitive (ending `-у`/`-ү`). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
эт {N} = pies
өй {N} = dom
хатын {N} = kobieta
бала {N} = dziecko

сөйләшергә {V} = mowic; rozmawiac
күрергә {V} = widziec
булырга {V} = byc
булырга {V} = miec (posiadanie)

кечкенә {Adj} = maly
тиз {Adv} = szybko
```

## Grammar notes (B1+)

- **Agglutinative SOV** with front/back vowel harmony. Closely related to Bashkir.
- 6 cases. No grammatical gender.
- The Cyrillic Tatar alphabet includes `ә ө ү ж ң`.

## Translation

Translate to Polish (`pol`). Tatar `син` → informal; `сез` → formal/plural (`Pan`/`Pani`/`wy`).
