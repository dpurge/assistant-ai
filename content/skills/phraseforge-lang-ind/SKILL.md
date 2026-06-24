---
name: phraseforge-lang-ind
description: Indonesian (Bahasa Indonesia, ISO 639-3 ind) language conventions for PhraseForge lessons. Codes, vocabulary shape (no gender, no articles, minimal inflection), verb affixation tags, and notes. Load whenever a PhraseForge lesson targets Indonesian.
---

# Indonesian (ind) language conventions

## Codes

- `lang`: `ind`
- `script`: `latn`

## Transcription

Not needed. Indonesian uses Latin script. No special characters beyond standard ASCII (no diacritics in modern orthography).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Indonesian-specific rules:

- **No grammatical gender, no articles, no case inflection.** All nouns take `{N}`. Plural is formed by reduplication (`anjing-anjing` = dogs) — note it only when explicitly in the source.
- **Verbs:** base (root) form or the prefixed active form (`me-` prefix family). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
anjing {N} = pies
rumah {N} = dom
perempuan {N} = kobieta
anak {N} = dziecko

berbicara {V} = mowic; rozmawiac
melihat {V} = widziec
adalah {V} = byc (kopula)
ada {V} = byc; istniec
mempunyai {V} = miec; posiadac

kecil {Adj} = maly
cepat {Adv} = szybko; predko
```

## Grammar notes (B1+)

- Indonesian is largely **isolating/analytic**: meaning is expressed by word order and separate words rather than inflection.
- Verb affixes: `me-` (active transitive), `di-` (passive), `ber-` (intransitive/stative), `ter-` (involuntary/superlative). Note the relevant prefix when the vocabulary item is a derived form.
- **SVO** word order as default; topicalization is flexible.

## Translation

Translate to Polish (`pol`). Indonesian `kamu`/`Anda` — `kamu` informal, `Anda` formal-neutral (`Pan`/`Pani` in Polish).
