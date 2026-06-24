---
name: phraseforge-lang-eng
description: English (ISO 639-3 eng) language conventions for PhraseForge lessons. Codes, vocabulary shape (no articles/gender in headwords), verb and noun tags. Load whenever a PhraseForge lesson targets English.
---

# English (eng) language conventions

## Codes

- `lang`: `eng`
- `script`: `latn`

## Transcription

Not needed. English uses Latin script.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. English-specific rules:

- **Nouns:** no articles in headword; no grammatical gender. Use `{N}`. Mark `pl` for plural-only nouns.
- **Verbs:** base (infinitive) form without `to`; tag `{V}`. Add `irreg` for irregular past tense.
- **Adjectives:** uninflected form, tag `{Adj}`.
- **Phrasal verbs:** include particle(s) in headword: `give up {V}`, `look after {V}`.

```
dog {N} = pies
house {N} = dom
children {N pl} = dzieci

run {V} = biec; biegac
take {V irreg} = brac
give up {V} = rezygnowac

small {Adj} = maly
quickly {Adv} = szybko
```

## Grammar notes

English has no case inflection, no grammatical gender, and minimal agreement. Grammar tags are intentionally minimal.

## Translation

Translate to Polish (`pol`). English does not distinguish formality via pronouns (`you` covers both). Render as informal Polish by default unless the source register is clearly formal.
