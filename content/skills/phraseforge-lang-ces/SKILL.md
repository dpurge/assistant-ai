---
name: phraseforge-lang-ces
description: Czech (Cestina, ISO 639-3 ces) language conventions for PhraseForge lessons. Codes, vocabulary shape (no article + gender/animate), verb aspect tags, and notes. Load whenever a PhraseForge lesson targets Czech.
---

# Czech (ces) language conventions

## Codes

- `lang`: `ces`
- `script`: `latn`

## Transcription

Not needed. Czech uses Latin script. Preserve diacritics: `á c d e é i n o r s t u y z` with háček or čárka: `á č ď é ě í ň ó ř š ť ú ů ý ž`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Czech-specific rules:

- **Nouns:** no articles; mark gender and animate/inanimate for masculines: `{N m an}` (masculine animate), `{N m in}` (masculine inanimate), `{N f}`, `{N n}`.
- **Verbs:** infinitive form. Czech verbs have **aspect pairs** (imperfective/perfective); list both when relevant: `delat {V impf}` / `udelat {V pf}`. Tag `irreg` if irregular.
- **Adjectives:** masculine singular nominative, tag `{Adj}`.

```
pes {N m an} = pies
dum {N m in} = dom
zena {N f} = kobieta
mesto {N n} = miasto

mluvit {V impf} = mowic
videt {V impf irreg} = widziec
byt {V irreg} = byc
mit {V irreg} = miec

maly {Adj} = maly
rychle {Adv} = szybko
```

## Declension tables (B1+)

Czech has 7 cases. Show declension paradigms for nouns/adjectives when relevant.

## Translation

Translate to Polish (`pol`). Czech `ty` → informal; `vy` (capital `Vy` when formal address) → formal Polish (`Pan`/`Pani`).

## Notes

- Czech and Polish are mutually intelligible to a fair degree; note false friends when they appear.
