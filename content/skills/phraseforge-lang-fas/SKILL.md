---
name: phraseforge-lang-fas
description: Persian/Farsi (Farsi, ISO 639-3 fas) language conventions for PhraseForge lessons. Codes, RTL Arabic script, DIN 31635 transcription, vocabulary shape (no grammatical gender, SOV order), and notes. Load whenever a PhraseForge lesson targets Persian.
---

# Persian / Farsi (fas) language conventions

## Codes

- `lang`: `fas`
- `script`: `arab`

## Transcription

Required (non-Latin script). Use **DIN 31635** (adapted for Persian). System attribute: `DIN31635`.

Persian-specific letters beyond the Arabic set:
| Persian | Transcription |
|---------|--------------|
| پ | p |
| چ | č |
| ژ | ž |
| گ | g |

Short vowels: `a` (fatha-equivalent), `e` (kasra-equivalent), `o` (damma-equivalent). Long vowels: `ā`, `i`, `u`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Persian-specific rules:

- **No grammatical gender.** All nouns take `{N}`.
- **Nouns:** bare form as headword, no articles. Plural formed by `ها-` (`-hā`) suffix.
- **Verbs:** infinitive form (ending in `-an`/`-dan`). Tag `{V}`. Add `irreg` for irregular stems.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
سگ {N} = pies
خانه {N} = dom
زن {N} = kobieta
بچه {N} = dziecko

حرف زدن {V} = mowic
دیدن {V} = widziec
بودن {V irreg} = byc
داشتن {V irreg} = miec

کوچک {Adj} = maly
سریع {Adv} = szybko
```

Transcription examples: `sag`, `xāne`, `zan`, `baḥče`, `ḥarf zadan`, `dīdan`, `budan`, `dāštan`, `kūčak`, `sarīʿ`.

## Grammar notes (B1+)

- Persian word order is **SOV** (Subject–Object–Verb).
- The **ezafe** construction (`-e`) links nouns to modifiers: `خانه‌ی بزرگ` (`xāne-ye bozorg` = the big house).
- Verb conjugation is regular for most verbs; the present stem (vs. infinitive) must be learned.

## Translation

Translate to Polish (`pol`).

## Notes

- Persian script is **right-to-left**; inherits Arabic letters with 4 additional letters (پ چ ژ گ).
- Persian is not a Semitic language (it is Indo-Iranian); do not assume Arabic root morphology applies.
