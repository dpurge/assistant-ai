---
name: phraseforge-lang-deu
description: German (Deutsch, ISO 639-3 deu) language conventions for PhraseForge lessons. Defines codes, transcription (none — Latin script), vocabulary entry shape (article + gender/number), verb/adjective format, and inflection table conventions. Load whenever a PhraseForge lesson targets German.
---

# German (deu) language conventions

## Codes

- `lang`: `deu`
- `script`: `latn`

## Transcription

Not needed. German uses Latin script. Render `ä`, `ö`, `ü`, `ß` as-is; do **not** transliterate to `ae`, `oe`, `ue`, `ss` unless the source explicitly does.

## Vocabulary format

Each noun entry takes the **definite article** + headword + grammar tag + Polish gloss:

```
der Hund {N m sg}   — pies
die Katze {N f sg}  — kot
das Kind {N n sg}   — dziecko
die Bücher {N n pl} — książki
```

Verbs as the bare infinitive (no `zu`):

```
gehen {V}   — iść
fahren {V}  — jechać
sein {V}    — być
```

Adjectives in the uninflected (predicate) form:

```
klein {Adj} — mały
gut {Adj}   — dobry
```

Separable-prefix verbs: show the unseparated infinitive but mark the prefix split:

```
aufstehen {V sep}   — wstawać
```

**Multiple senses** in the Polish translation are separated by `; ` (semicolon + space):

```
alle     — wszyscy; wszystkie
angenehm — miły; przyjemny
```

In the JSON contract this is just the `translation` string for that entry: `"translation": "wszyscy; wszystkie"`.

See `phraseforge-core/references/vocabulary.md` for the underlying grammar-tag conventions; this skill only specifies German-specific shape.

## Inflection tables (optional, B1+)

Use for irregular verbs and strong/mixed noun declensions. Use a Markdown table — columns = case (Nom, Akk, Dat, Gen), rows = number (sg, pl) or person (ich/du/er…).

## Translation

Translate to Polish (`pol`). Match register: `Sie` → formal Polish; `du` → informal. Default to `Sie` unless the source is clearly informal (children's text, casual dialogue).

## Cultural / dialectal notes

- Default to standard high German (Hochdeutsch). Note Austrian / Swiss variants only if they appear in the source.

## Stub

Inflection-table templates and exercise tweaks specific to German still TBD.
