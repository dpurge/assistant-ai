---
name: phraseforge-lang-fin
description: Finnish (Suomi, ISO 639-3 fin) language conventions for PhraseForge lessons. Codes, vocabulary shape (no gender, 15 cases, no articles), verb conjugation class tags, and notes. Load whenever a PhraseForge lesson targets Finnish.
---

# Finnish (fin) language conventions

## Codes

- `lang`: `fin`
- `script`: `latn`

## Transcription

Not needed. Finnish uses Latin script. Preserve: `ä ö å` (the last used mainly in Swedish loanwords).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Finnish-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`. Plural formed by vowel lengthening + `-t` (partitive plural `-a`/`-ä`).
- **Verbs:** infinitive form (ending `-a`/`-ä`, `-da`/`-dä`, or `-la`/`-la`). Tag `{V}`. Mark conjugation type (1–6): `{V 1}` through `{V 6}`. Add `irreg` for irregular.
- **Adjectives:** uninflected basic form, tag `{Adj}`.

```
koira {N} = pies
talo {N} = dom
nainen {N} = kobieta
lapsi {N} = dziecko

puhua {V 1} = mowic
nahda {V 4 irreg} = widziec
olla {V irreg} = byc
omistaa {V 1} = miec; posiadac

pieni {Adj} = maly
nopeasti {Adv} = szybko
```

(With macrons: `nähdä`, `omistaa`; diacritics: `puhua`, `koira`, `nainen`, `pieni`.)

## Grammar notes (B1+)

- Finnish has 15 grammatical cases — all expressed by suffixes. The most important: nominative, partitive, genitive, accusative, locative cases (3 pairs: `ssa/ssa`, `sta/sta`, `lle`/`lla`/`lta` etc.).
- **Vowel harmony**: suffixes use front vowels (`ä`, `ö`, `y`) with front-vowel stems and back vowels (`a`, `o`, `u`) with back-vowel stems.
- Verb conjugation depends on type class; negative verb is a separate auxiliary (`en`, `et`, `ei`, …).

## Translation

Translate to Polish (`pol`). Finnish `sinä` → informal; `te` (formal/plural) → `Pan`/`Pani`/`wy`.
