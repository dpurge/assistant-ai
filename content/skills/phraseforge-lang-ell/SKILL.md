---
name: phraseforge-lang-ell
description: Modern Greek (Neoelliniki, ISO 639-3 ell) language conventions for PhraseForge lessons. Codes, Greek script (no transcription needed), vocabulary shape (gender + articles), verb conjugation class tags, and notes. Load whenever a PhraseForge lesson targets Modern Greek.
---

# Modern Greek (ell) language conventions

## Codes

- `lang`: `ell`
- `script`: `grek`

## Transcription

Not required. Greek script is excluded from transcription block per `phraseforge-web` convention. Preserve polytonic characters if the source uses them (modern Greek is monotonic — single accent mark).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Modern Greek-specific rules:

- **Nouns:** include the **definite article** (`ο`/`m`, `η`/`f`, `το`/`n`) in the headword. Mark gender: `{N m}` / `{N f}` / `{N n}`.
- **Verbs:** first-person singular present (dictionary form). Tag `{V}`. Two conjugation classes: `-ω` (type A) and `-άω`/`-ώ` (type B): `{V A}` / `{V B}`. Add `irreg` for irregular.
- **Adjectives:** masculine singular nominative, tag `{Adj}`.

```
ο σκύλος {N m} = pies
το σπίτι {N n} = dom
η γυναίκα {N f} = kobieta
το παιδί {N n} = dziecko

μιλώ {V B} = mowic
βλέπω {V A} = widziec
είμαι {V irreg} = byc
έχω {V A} = miec

μικρός {Adj} = maly
γρήγορα {Adv} = szybko
```

## Declension tables (B1+)

Modern Greek has 4 cases (nominative, genitive, accusative, vocative). Show paradigms for difficult nouns.

## Translation

Translate to Polish (`pol`). Modern Greek `εσύ` → informal; `εσείς` (formal/plural) → `Pan`/`Pani`/`wy`.

## Notes

- Modern Greek (Demotic/Dhimotiki) is the standard. Distinguish from Katharevousa (archaic formal) if it appears in the source.
