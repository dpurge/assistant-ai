---
name: phraseforge-lang-fra
description: French (Français, ISO 639-3 fra) language conventions for PhraseForge lessons. Codes, vocabulary shape (definite article + gender), verb group tags, and formality rules. Load whenever a PhraseForge lesson targets French.
---

# French (fra) language conventions

## Codes

- `lang`: `fra`
- `script`: `latn`

## Transcription

Not needed. French uses Latin script. Preserve all accents and special characters: `é à â ç è ê î ï ô ù û ü ÿ œ æ`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. French-specific rules:

- **Nouns:** include the **definite article** (`le`, `la`, `l'`, `les`) in the headword to show gender. Mark gender: `{N m}` / `{N f}`.
- **Verbs:** infinitive form. Tag with verb group: `{V er}` (-er), `{V ir}` (-ir), `{V re}` (-re). Add `irreg` for irregular verbs.
- **Adjectives:** masculine singular form, tag `{Adj}`.

```
le chien {N m} = pies
la maison {N f} = dom
les enfants {N m pl} = dzieci

parler {V er} = mowic
finir {V ir} = konczyc
prendre {V re irreg} = brac
etre {V irreg} = byc
avoir {V irreg} = miec

petit {Adj} = maly
vite {Adv} = szybko
```

**Multiple senses** separated by `; `:
```
sauver {V er} = ratowac; zbawiac
```

## Conjugation tables (optional, B1+)

For irregular verbs. Markdown table: columns = subject (je, tu, il/elle, nous, vous, ils/elles), rows = tense (présent, passé composé, imparfait, futur…).

## Translation

Translate to Polish (`pol`). Formality:
- `tu` — informal Polish (`ty`).
- `vous` (formal/plural) — `Pan`/`Pani`/`Państwo` (formal) or `wy` (plural informal).

## Cultural notes

- Distinguish Parisian French from Canadian (québécois) or Belgian variants when they appear in the source.
- Note liaisons and elisions in pronunciation hints if relevant.
