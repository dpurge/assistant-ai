---
name: phraseforge-lang-hrv
description: Croatian (Hrvatski, ISO 639-3 hrv) language conventions for PhraseForge lessons. Codes, vocabulary shape (no article + gender/animate), verb aspect tags, and notes. Load whenever a PhraseForge lesson targets Croatian.
---

# Croatian (hrv) language conventions

## Codes

- `lang`: `hrv`
- `script`: `latn`

## Transcription

Not needed. Croatian uses Latin script. Preserve diacritics: `č c d s z` with caron and the digraph `dz`: `č ć dž đ š ž`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Croatian-specific rules:

- **Nouns:** no articles; mark gender and animate/inanimate for masculines: `{N m an}`, `{N m in}`, `{N f}`, `{N n}`.
- **Verbs:** infinitive form. Mark aspect: `{V impf}` / `{V pf}`. Add `irreg` for irregular.
- **Adjectives:** masculine singular nominative, tag `{Adj}`.

```
pas {N m an} = pies
kuca {N f} = dom
grad {N m in} = miasto
dijete {N n} = dziecko

govoriti {V impf} = mowic
vidjeti {V impf irreg} = widziec
biti {V irreg} = byc
imati {V irreg} = miec

mali {Adj} = maly
brzo {Adv} = szybko
```

## Declension tables (B1+)

Croatian has 7 cases. Show paradigms when relevant. Stress accent (pitch accent) can be noted for advanced learners.

## Translation

Translate to Polish (`pol`). Croatian `ti` → informal; `vi` (formal address) → `Pan`/`Pani`.
