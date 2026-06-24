---
name: phraseforge-lang-lat
description: Latin (Latina, ISO 639-3 lat) language conventions for PhraseForge lessons. Codes, vocabulary shape (dictionary form + gender), verb conjugation class tags, and notes. Load whenever a PhraseForge lesson targets Latin.
---

# Latin (lat) language conventions

## Codes

- `lang`: `lat`
- `script`: `latn`

## Transcription

Not needed. Latin uses Latin script. Macrons (ā ē ī ō ū) are optional but recommended for A1–B1 learners to show vowel length.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Latin-specific rules:

- **Nouns:** nominative singular as headword; mark gender: `{N m}` / `{N f}` / `{N n}`. Optionally add declension class: `{N f 1}` (1st), `{N m 2}` (2nd), `{N f 3}` (3rd), etc.
- **Verbs:** first-person present active indicative as headword (dictionary form). Tag with conjugation class: `{V 1}` (1st), `{V 2}` (2nd), `{V 3}` (3rd), `{V 4}` (4th). Add `irreg` for irregular.
- **Adjectives:** masculine nominative singular (2-1-2 or 3rd declension), tag `{Adj}`.

```
rana {N f} = zaba
aqua {N f} = woda
ripa {N f} = brzeg
puer {N m} = chlopiec
templum {N n} = swiatynia

amare {V 1} = kochac
videre {V 2} = widziec
esse {V irreg} = byc
ire {V irreg} = isc

magnus {Adj} = wielki
parvus {Adj} = maly
```

## Declension tables (B1+)

Show noun declension tables (Nom/Gen/Dat/Acc/Abl/Voc × sg/pl) for irregular or difficult words. Verb conjugation tables: 6 persons × 6 tenses (active/passive where relevant).

## Translation

Translate to Polish (`pol`). Latin has no articles; Polish translation uses articles where natural.

## Notes

- Classical Latin (CL) by default. Note Ecclesiastical Latin pronunciation variants when relevant (e.g. `c` before `e`/`i` → /tʃ/).
- Macrons should be consistent: either use them throughout a lesson or not at all.
