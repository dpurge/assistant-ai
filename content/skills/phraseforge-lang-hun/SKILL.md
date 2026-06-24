---
name: phraseforge-lang-hun
description: Hungarian (Magyar, ISO 639-3 hun) language conventions for PhraseForge lessons. Codes, vocabulary shape (no gender, agglutinative, vowel harmony, no articles for headwords), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Hungarian.
---

# Hungarian (hun) language conventions

## Codes

- `lang`: `hun`
- `script`: `latn`

## Transcription

Not needed. Hungarian uses Latin script. Preserve diacritics: `á é í ó ö ő ú ü ű`. Note double-length vowels: `ő` (long ö) and `ű` (long ü).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Hungarian-specific rules:

- **No grammatical gender, no articles in headwords.** All nouns take `{N}`. Indefinite article `egy`; definite `a`/`az` — not part of headword.
- **Verbs:** third-person singular present (dictionary form). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
kutya {N} = pies
ház {N} = dom
nő {N} = kobieta
gyerek {N} = dziecko

beszél {V} = mowic
lát {V} = widziec
van {V irreg} = byc
van neki {Phrase} = miec

kicsi {Adj} = maly
gyorsan {Adv} = szybko
```

## Grammar notes (B1+)

- **Agglutinative** language with extensive suffixation: case endings, possessive suffixes, and verb conjugation for person/number/definiteness all expressed by suffixes.
- Hungarian distinguishes **definite** and **indefinite** verb conjugation (the verb changes form depending on whether the object is definite).
- **Vowel harmony**: suffixes alternate based on the dominant vowel of the stem (front/back, with a special class for `i`-dominant stems).
- 18 cases (nominative + 17 oblique forms), although most are spatial/locative cases.

## Translation

Translate to Polish (`pol`). Hungarian `te` → informal; `ön` (formal/singular) or `önök` (formal/plural) → `Pan`/`Pani`/`Państwo`.
