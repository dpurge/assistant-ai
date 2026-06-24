---
name: phraseforge-lang-nld
description: Dutch (Nederlands, ISO 639-3 nld) language conventions for PhraseForge lessons. Codes, vocabulary shape (de/het article + gender), verb tags, and notes. Load whenever a PhraseForge lesson targets Dutch.
---

# Dutch (nld) language conventions

## Codes

- `lang`: `nld`
- `script`: `latn`

## Transcription

Not needed. Dutch uses Latin script. Preserve: `é è ë ij/ij`. Note that `ij` is a digraph treated as a single letter.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Dutch-specific rules:

- **Nouns:** Dutch has two article types — `de` (common gender, covering former masculine and feminine) and `het` (neuter). Include the article in the headword. Mark: `{N de}` / `{N het}`.
- **Verbs:** infinitive form, tag `{V}`. Separable verbs: `{V sep}`. Add `irreg` for irregular.
- **Adjectives:** uninflected stem form, tag `{Adj}`.

```
de hond {N de} = pies
het huis {N het} = dom
de kinderen {N de pl} = dzieci

praten {V} = mowic
zien {V irreg} = widziec
opstaan {V sep} = wstawac
zijn {V irreg} = byc
hebben {V irreg} = miec

klein {Adj} = maly
snel {Adv} = szybko
```

## Grammar notes

- `de`/`het` must be learned per word — there is no simple gender rule.
- Diminutives always take `het`: `het hondje` (the little dog).

## Translation

Translate to Polish (`pol`). Dutch `jij`/`je` → informal; `u` → formal (`Pan`/`Pani`).
