---
name: phraseforge-lang-arz
description: Egyptian Arabic (ISO 639-3 arz) — colloquial Egyptian Arabic — language conventions for PhraseForge lessons. Load whenever a PhraseForge lesson targets Egyptian Arabic.
---

# Egyptian Arabic (arz) language conventions

## Codes

- `lang`: `arz`
- `script`: `arab`

## Transcription

Required (non-Latin script). Use **DIN 31635** romanization (see `phraseforge-lang-arb` for the full table). System attribute: `DIN31635`.

Egyptian-specific: `ǧ` is pronounced /g/ (hard g) — a distinctive feature of Egyptian Arabic.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md` and `phraseforge-lang-arb`. Egyptian-specific notes:

- **Nouns:** mark gender: `{N m}` / `{N f}`. Broken plurals listed separately.
- **Verbs:** third-person masculine singular perfect, tag `{V}`.
- Definite article: `il-` / `el-` (assimilates to sun letters).
- Egyptian uses `b-` prefix for habitual present: `بيتكلم` (he speaks regularly).

```
كلب {N m sg} = pies
بيت {N m sg} = dom
ست {N f sg} = kobieta; pani

اتكلم {V impf} = mowic
شاف {V} = widziec
كان {V irreg} = byl; byc
عنده {Phrase} = ma

كبير {Adj} = duzy
صغير {Adj} = maly
```

## Translation

Translate to Polish (`pol`).

## Notes

- Egyptian Arabic is the most widely understood Arabic dialect due to Egyptian cinema and television.
- Avoid mixing with MSA (`arb`) or other dialects in a single lesson.
