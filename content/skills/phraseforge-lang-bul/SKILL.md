---
name: phraseforge-lang-bul
description: Bulgarian (Bulgarski, ISO 639-3 bul) language conventions for PhraseForge lessons. Codes, vocabulary shape (no inflectional case + postpositional article + gender), verb tags, and notes. Load whenever a PhraseForge lesson targets Bulgarian.
---

# Bulgarian (bul) language conventions

## Codes

- `lang`: `bul`
- `script`: `cyrl`

## Transcription

Not required by default (Cyrillic excluded from transcription block).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Bulgarian-specific rules:

- **Nouns:** Bulgarian has **lost case inflection** (like Romanian and Macedonian among Slavic languages) but retains gender and a **postpositional definite article** (suffixed). Use the indefinite (bare) form as headword; mark gender: `{N m}` / `{N f}` / `{N n}`.
- **Verbs:** first-person singular present as headword (dictionary form). Tag `{V}`. Mark aspect: `{V impf}` / `{V pf}`. Add `irreg` for irregular.
- **Adjectives:** masculine singular short form, tag `{Adj}`.

```
куче {N n} = pies
сграда {N f} = dom; budynek
жена {N f} = kobieta
дете {N n} = dziecko

говоря {V impf} = mowic
видя {V pf} = zobaczyc
съм {V irreg} = byc
имам {V irreg} = miec

малък {Adj} = maly
бързо {Adv} = szybko
```

## Translation

Translate to Polish (`pol`). Bulgarian `ти` → informal; `вие` (formal/plural) → `Pan`/`Pani`/`wy`.

## Notes

- Bulgarian uses a definite postpositional article: `куче` (dog) → `кучето` (the dog).
- Bulgarian has re-developed a future tense particle `ще` and compound past. Note these constructions in models.
