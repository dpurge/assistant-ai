---
name: phraseforge-lang-kaz
description: Kazakh (Qazaq tili, ISO 639-3 kaz) language conventions for PhraseForge lessons — Cyrillic script variant as in phraseforge-data. Codes, vocabulary shape (agglutinative, no gender), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Kazakh.
---

# Kazakh (kaz) language conventions

## Codes

- `lang`: `kaz`
- `script`: `cyrl`

Note: Kazakhstan is transitioning to Latin script; phraseforge-data uses `kaz-cyrl`. This skill covers the Cyrillic variant.

## Transcription

Not required by default (Cyrillic excluded from transcription block per `phraseforge-web` convention).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Kazakh-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`.
- **Verbs:** infinitive (ending `-у`/`-ю` in Cyrillic, equivalent to `-w` stem). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
ит {N} = pies
үй {N} = dom; mieszkanie
әйел {N} = kobieta
бала {N} = dziecko

сөйлеу {V} = mowic
көру {V} = widziec
болу {V} = byc
болу {V} = miec (kontekst posiadania)

кішкентай {Adj} = maly
тез {Adv} = szybko
```

## Grammar notes (B1+)

- **Agglutinative SOV** with vowel harmony (front/back).
- 7 cases (nominative, genitive, dative, accusative, locative, ablative, instrumental).
- Extensive system of verbal nouns (masdar), participles, and converbs.

## Translation

Translate to Polish (`pol`). Kazakh `сен` → informal; `сіз` → formal/plural (`Pan`/`Pani`/`wy`).
