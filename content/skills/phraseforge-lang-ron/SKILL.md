---
name: phraseforge-lang-ron
description: Romanian (Română, ISO 639-3 ron) language conventions for PhraseForge lessons. Codes, vocabulary shape (postpositional article + gender), verb tags, and notes. Load whenever a PhraseForge lesson targets Romanian.
---

# Romanian (ron) language conventions

## Codes

- `lang`: `ron`
- `script`: `latn`

## Transcription

Not needed. Romanian uses Latin script. Preserve special characters: `ă â î ș ț`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Romanian-specific rules:

- **Nouns:** Romanian has three genders (m/f/n) and a **postpositional definite article** (suffixed: `-ul`, `-a`, `-le`). Show the indefinite form as headword; mark gender. `{N m}` / `{N f}` / `{N n}`.
- **Verbs:** infinitive (short form without `a`), tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** masculine singular, tag `{Adj}`.

```
caine {N m} = pies
casa {N f} = dom
copil {N n} = dziecko

a vorbi {V} = mowic
a fi {V irreg} = byc
a avea {V irreg} = miec

mic {Adj} = maly
repede {Adv} = szybko
```

## Grammar notes (B1+)

Romanian has preserved the Latin vocative and some case distinctions (nominative/accusative vs. genitive/dative via article forms). Note case endings for nouns when relevant.

## Translation

Translate to Polish (`pol`).

## Cultural notes

- Romanian is the only major Romance language in Eastern Europe; note Slavic and Hungarian loanwords when they appear.
