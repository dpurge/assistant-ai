---
name: phraseforge-lang-grc
description: Ancient Greek (Hellenike, ISO 639-3 grc) language conventions for PhraseForge lessons. Codes, Greek script (no transcription needed), vocabulary shape (gender + articles, 5 cases), verb principal parts, and notes. Load whenever a PhraseForge lesson targets Ancient Greek.
---

# Ancient Greek (grc) language conventions

## Codes

- `lang`: `grc`
- `script`: `grek`

## Transcription

Not required. Greek script is excluded from transcription block per `phraseforge-web` convention.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Ancient Greek-specific rules:

- **Nouns:** include the **definite article** (ὁ/m, ἡ/f, τό/n) and the genitive ending as headword — standard dictionary format: `λόγος, -ου, ὁ`. Mark gender: `{N m}` / `{N f}` / `{N n}`. Add declension: `{N m 2}` (2nd), `{N f 1}` (1st), `{N m 3}` (3rd), etc.
- **Verbs:** first-person singular present active indicative (1pp). Tag `{V}`. Note the conjugation class when useful (thematic / athematic / contract).
- **Adjectives:** masculine singular nominative, tag `{Adj}`.

```
ὁ κύων, κυνός {N m 3} = pies
ἡ οἰκία, -ας {N f 1} = dom
ἡ γυνή, γυναικός {N f 3 irreg} = kobieta
τὸ παιδίον, -ου {N n 2} = dziecko

λέγω {V} = mowic
ὁράω {V contract} = widziec
εἰμί {V irreg} = byc
ἔχω {V} = miec

μικρός {Adj} = maly
ταχέως {Adv} = szybko
```

## Principal parts (B1+)

Greek verbs have up to 6 principal parts (present, future, aorist active, perfect active, perfect passive, aorist passive). List relevant principal parts in the `notes` field for irregular verbs.

## Grammar notes (B1+)

Ancient Greek has 5 cases (nominative, genitive, dative, accusative, vocative) and 3 numbers (singular, dual, plural). Verb system encodes tense/aspect, mood (indicative, subjunctive, optative, imperative, infinitive, participle), voice (active, middle, passive), person, and number.

## Translation

Translate to Polish (`pol`).

## Notes

- Ancient Greek refers here to Classical Attic (5th–4th century BCE) as the default. Distinguish from Homeric Greek, Hellenistic Koine, or Byzantine Greek if the source uses a different register.
- Accents (acute, grave, circumflex) and breathings (rough, smooth) are part of the orthography and must be preserved.
