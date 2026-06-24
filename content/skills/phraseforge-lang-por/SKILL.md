---
name: phraseforge-lang-por
description: Portuguese (Português, ISO 639-3 por) language conventions for PhraseForge lessons. Codes, vocabulary shape (definite article + gender), verb group tags, and formality rules. Load whenever a PhraseForge lesson targets Portuguese.
---

# Portuguese (por) language conventions

## Codes

- `lang`: `por`
- `script`: `latn`

## Transcription

Not needed. Portuguese uses Latin script. Preserve accents and special characters: `á â ã à é ê í ó ô õ ú ç`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Portuguese-specific rules:

- **Nouns:** include the **definite article** (`o`, `a`, `os`, `as`) in the headword. Mark gender: `{N m}` / `{N f}`.
- **Verbs:** infinitive form. Tag with verb class: `{V ar}`, `{V er}`, `{V ir}`. Add `irreg` for irregular verbs.
- **Adjectives:** masculine singular form, tag `{Adj}`.

```
o cachorro {N m} = pies
a casa {N f} = dom
os amigos {N m pl} = przyjaciele

falar {V ar} = mowic
comer {V er} = jesc
partir {V ir} = odchodzic
ser {V irreg} = byc
ter {V irreg} = miec

pequeno {Adj} = maly
rapido {Adj} = szybki
```

## Conjugation tables (optional, B1+)

For irregular verbs. Markdown table: columns = subject (eu, tu, ele/ela/você, nós, vós, eles/elas), rows = tense (presente, pretérito perfeito, imperfeito, futuro…).

## Translation

Translate to Polish (`pol`). Formality: `você` (European formal or Brazilian standard) → `Pan`/`Pani`; `tu` (European informal / Brazilian informal) → `ty`.

## Regional variants

Note whether the source is European Portuguese (EP) or Brazilian Portuguese (BP) — vocabulary, spelling, and pronunciation differ. Default to EP unless context indicates BP.
