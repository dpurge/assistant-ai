---
name: phraseforge-lang-ita
description: Italian (Italiano, ISO 639-3 ita) language conventions for PhraseForge lessons. Codes, vocabulary shape (definite article + gender), verb group tags, and formality rules. Load whenever a PhraseForge lesson targets Italian.
---

# Italian (ita) language conventions

## Codes

- `lang`: `ita`
- `script`: `latn`

## Transcription

Not needed. Italian uses Latin script. Preserve accents: `à è é ì î ò ó ù`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Italian-specific rules:

- **Nouns:** include the **definite article** (`il`, `lo`, `la`, `l'`, `i`, `gli`, `le`) in the headword. Mark gender: `{N m}` / `{N f}`.
- **Verbs:** infinitive form. Tag with verb class: `{V are}`, `{V ere}`, `{V ire}`. Add `irreg` for irregular verbs.
- **Adjectives:** masculine singular form, tag `{Adj}`.

```
il cane {N m} = pies
la casa {N f} = dom
gli amici {N m pl} = przyjaciele

parlare {V are} = mowic
vedere {V ere irreg} = widziec
dormire {V ire} = spac
essere {V irreg} = byc
avere {V irreg} = miec

piccolo {Adj} = maly
veloce {Adj} = szybki
bene {Adv} = dobrze
```

## Conjugation tables (optional, B1+)

For irregular verbs. Markdown table: columns = subject (io, tu, lui/lei, noi, voi, loro), rows = tense (presente, passato prossimo, imperfetto, futuro…).

## Translation

Translate to Polish (`pol`). Formality:
- `tu` — informal Polish.
- `Lei` (formal singular) — `Pan`/`Pani`.
- `voi` (plural) — `wy`.

## Cultural notes

- Default to standard Italian. Note regional variants (Sicilian, Venetian, etc.) only if they appear in the source.
