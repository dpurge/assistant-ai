---
name: phraseforge-lang-lit
description: Lithuanian (Lietuviu, ISO 639-3 lit) language conventions for PhraseForge lessons. Codes, vocabulary shape (no article + gender), verb class tags, and notes. Load whenever a PhraseForge lesson targets Lithuanian.
---

# Lithuanian (lit) language conventions

## Codes

- `lang`: `lit`
- `script`: `latn`

## Transcription

Not needed. Lithuanian uses Latin script. Preserve diacritics: `ą č ę ė į š ų ū ž`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Lithuanian-specific rules:

- **Nouns:** no articles; mark gender: `{N m}` / `{N f}`. Lithuanian has 5 noun declension classes — note the class when relevant: `{N m 1}` … `{N m 5}`.
- **Verbs:** infinitive (ending in `-ti`), tag `{V}`. Mark conjugation class optionally: `{V 1}` (I-class), `{V 2}` (II-class), `{V 3}` (III-class). Add `irreg` for irregular.
- **Adjectives:** masculine singular nominative, tag `{Adj}`.

```
suo {N m} = pies
namas {N m} = dom
moteris {N f} = kobieta
vaikas {N m} = dziecko

kalbeti {V 2} = mowic
matyti {V 2} = widziec
buti {V irreg} = byc
tureti {V 2} = miec

mazas {Adj} = maly
greitai {Adv} = szybko
```

## Declension tables (B1+)

Lithuanian has 7 cases. Show paradigms when relevant. Lithuanian preserves pitch accent — note for advanced learners.

## Translation

Translate to Polish (`pol`). Lithuanian `tu` → informal; `jus` (formal/plural) → `Pan`/`Pani`/`wy`.

## Notes

- Lithuanian is one of the most archaic living Indo-European languages; vocabulary contains many Baltic cognates with no Slavic equivalent. Explain loanword sources when helpful.
