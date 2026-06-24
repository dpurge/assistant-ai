---
name: phraseforge-lang-dan
description: Danish (Dansk, ISO 639-3 dan) language conventions for PhraseForge lessons. Codes, vocabulary shape (indefinite article + gender), verb tags, and notes. Load whenever a PhraseForge lesson targets Danish.
---

# Danish (dan) language conventions

## Codes

- `lang`: `dan`
- `script`: `latn`

## Transcription

Not needed. Danish uses Latin script. Preserve: `æ ø å`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Danish-specific rules:

- **Nouns:** Danish has two genders: common (`c`) and neuter (`n`). Include the **indefinite article** (`en` for common, `et` for neuter) in the headword. Mark gender: `{N c}` / `{N n}`.
- **Verbs:** infinitive form (bare, without `at`), tag `{V}`.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
en hund {N c} = pies
et hus {N n} = dom
bornen {N c pl} = dzieci

tale {V} = mowic
vaere {V irreg} = byc
have {V irreg} = miec

lille {Adj} = maly
hurtigt {Adv} = szybko
```

## Grammar notes

- Definite article is **postpositional** (suffixed): `hunden` (the dog), `huset` (the house).
- Nouns take `-er` or `-e` plural endings (often irregular).

## Translation

Translate to Polish (`pol`). Danish `du` → informal Polish; `De` (archaic formal) → `Pan`/`Pani` if encountered.
