---
name: phraseforge-lang-apc
description: North Levantine Arabic (ISO 639-3 apc) — Syrian/Lebanese colloquial Arabic — language conventions for PhraseForge lessons. Load whenever a PhraseForge lesson targets Levantine Arabic.
---

# North Levantine Arabic (apc) language conventions

## Codes

- `lang`: `apc`
- `script`: `arab`

## Transcription

Required (non-Latin script). Use **DIN 31635** romanization (see `phraseforge-lang-arb` for the full table). System attribute: `DIN31635`.

Levantine-specific sounds: emphatic `q` is often pronounced as a glottal stop (ʾ) in urban speech; `ǧ` is /ʒ/ in Syrian and /dʒ/ in Lebanese.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md` and `phraseforge-lang-arb`. Levantine-specific notes:

- **Nouns:** mark gender: `{N m}` / `{N f}`. Broken plurals listed separately with `{N m pl}` / `{N f pl}`.
- **Verbs:** third-person masculine singular perfect (dictionary form), tag `{V}`.
- Definite article: `l-` / `il-` (assimilates to sun letters).

```
كلب {N m sg} = pies
بيت {N m sg} = dom
ست {N f sg} = kobieta; pani

حكى {V} = mowic
شاف {V} = widziec
كان {V irreg} = byl; byc
عنده {Phrase} = ma (on ma)
```

## Translation

Translate to Polish (`pol`).

## Notes

- Levantine Arabic differs significantly from MSA (`arb`) in phonology, morphology, and vocabulary. Avoid mixing the two in a single lesson.
- Distinguish Syrian (`apc`) from Lebanese colloquial when relevant; they share most features.
