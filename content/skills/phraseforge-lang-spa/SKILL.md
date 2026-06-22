---
name: phraseforge-lang-spa
description: Spanish (Español, ISO 639-3 spa) language conventions for PhraseForge lessons. Defines codes, transcription (none — Latin script), vocabulary entry shape (article + gender), verb conjugation patterns, and formality conventions. Load whenever a PhraseForge lesson targets Spanish.
---

# Spanish (spa) language conventions

## Codes

- `lang`: `spa`
- `script`: `latn`

## Transcription

Not needed. Spanish uses Latin script. Render `ñ`, accented vowels (`á é í ó ú`), inverted punctuation (`¿ ¡`), and `ü` (as in `pingüino`) as-is.

## Vocabulary format

Nouns: definite article + headword + grammar tag + Polish gloss:

```
el perro {N m sg}   — pies
la gata {N f sg}    — kotka
los niños {N m pl}  — dzieci
las casas {N f pl}  — domy
```

Verbs by infinitive ending (`-ar`, `-er`, `-ir`):

```
hablar {V}  — mówić
comer {V}   — jeść
vivir {V}   — żyć
ser {V}     — być
```

Adjectives in masculine singular form (the standard dictionary form):

```
pequeño {Adj} — mały
feliz {Adj}   — szczęśliwy
```

**Multiple senses** in the Polish translation are separated by `; ` (semicolon + space):

```
bueno  — dobry; smaczny
casa   — dom; mieszkanie
```

In the JSON contract this is just the `translation` string for that entry: `"translation": "dobry; smaczny"`.

See `phraseforge-core/references/vocabulary.md` for grammar-tag conventions; this skill specifies the Spanish-specific shape.

## Conjugation tables (optional, B1+)

For irregular verbs. Use a Markdown table — columns = subject pronouns (yo, tú, él/ella/usted, nosotros, vosotros, ellos/ellas/ustedes), rows = tense (presente, pretérito indefinido, imperfecto, futuro…).

## Translation

Translate to Polish (`pol`). Handle formality:
- `tú` / `vosotros` → informal Polish (`ty` / `wy`).
- `usted` / `ustedes` → formal Polish (`Pan` / `Pani` / `Państwo`).

## Regional variants

Default to peninsular Spanish (the `vosotros` form exists). If the source is clearly Latin American — uses `ustedes` for all 2nd-person plural, has voseo (`vos` instead of `tú`), or has regional vocabulary (`carro` for car instead of `coche`) — note the variant in the lesson description and adapt vocabulary accordingly.

## Stub

Conjugation-table templates and exercise tweaks specific to Spanish still TBD.
