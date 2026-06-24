---
name: phraseforge-lang-epo
description: Esperanto (Esperanto, ISO 639-3 epo) language conventions for PhraseForge lessons. Codes, vocabulary shape (systematic morphology, no irregular forms), tag conventions, and notes. Load whenever a PhraseForge lesson targets Esperanto.
---

# Esperanto (epo) language conventions

## Codes

- `lang`: `epo`
- `script`: `latn`

## Transcription

Not needed. Esperanto uses Latin script with a circumflex supersign: `ĉ ĝ ĥ ĵ ŝ ŭ`. Always preserve these characters (do not substitute `ch`, `gh`, etc.).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Esperanto-specific rules:

- **Gender:** grammatically genderless by default; feminine marked by suffix `-ino`. Use `{N}` for default nouns; `{N f}` for explicitly feminine forms (with `-ino`).
- **Systematic word endings:** `-o` (noun), `-a` (adjective), `-e` (adverb), `-i` (verb infinitive). All regular: no irregular conjugation, no irregular plural (always `-j`), no irregular accusative (always `-n`).
- **Verbs:** infinitive (ending `-i`). Tag `{V}`. There are no irregular verbs.
- **Adjectives:** basic form (ending `-a`), tag `{Adj}`.

```
hundo {N} = pies
domo {N} = dom
virino {N f} = kobieta
infano {N} = dziecko

paroli {V} = mowic
vidi {V} = widziec
esti {V} = byc
havi {V} = miec

malgranda {Adj} = maly
rapide {Adv} = szybko
```

## Grammar notes

- Esperanto has 2 grammatical cases: nominative (unchanged) and accusative (suffix `-n`). No other cases — prepositions handle all other relationships.
- Verb tenses: `-as` (present), `-is` (past), `-os` (future), `-us` (conditional), `-u` (subjunctive/jussive).
- The regularity of Esperanto makes grammar tags minimal — virtually nothing is irregular.

## Translation

Translate to Polish (`pol`). Esperanto `vi` covers both singular polite and plural you → `Pan`/`Pani`/`wy` depending on context; `ci` (rarely used, informal singular) → `ty`.
