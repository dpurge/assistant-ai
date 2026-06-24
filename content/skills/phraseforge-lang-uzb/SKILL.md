---
name: phraseforge-lang-uzb
description: Uzbek (Ozbek tili, ISO 639-3 uzb) language conventions for PhraseForge lessons — Latin script variant. Codes, vocabulary shape (agglutinative, no gender), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Uzbek.
---

# Uzbek (uzb) language conventions

## Codes

- `lang`: `uzb`
- `script`: `latn`

Note: Uzbek uses Latin script in Uzbekistan (official since 1993) and Cyrillic in older materials. phraseforge-data uses `uzb-latn`.

## Transcription

Not needed. Uzbek uses Latin script. Preserve: `g' o' sh ch ng`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Uzbek-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`.
- **Verbs:** infinitive (ending `-moq`). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
it {N} = pies
uy {N} = dom; mieszkanie
ayol {N} = kobieta
bola {N} = dziecko

gapirmoq {V} = mowic
ko'rmoq {V} = widziec
bo'lmoq {V} = byc
ega bo'lmoq {V} = miec; posiadac

kichik {Adj} = maly
tez {Adv} = szybko
```

## Grammar notes (B1+)

- **Agglutinative SOV** language with vowel harmony (less strict than Turkish/Azerbaijani — Uzbek has largely lost rounded vowel harmony).
- 6 cases, expressed by suffixes.
- No copula in present tense (as in Turkish).

## Translation

Translate to Polish (`pol`). Uzbek `sen` → informal; `siz` → formal/plural (`Pan`/`Pani`/`wy`).
