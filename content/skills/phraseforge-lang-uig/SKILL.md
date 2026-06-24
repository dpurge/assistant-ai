---
name: phraseforge-lang-uig
description: Uyghur (Uyghurche, ISO 639-3 uig) language conventions for PhraseForge lessons — Arabic script (Uyghur Perso-Arabic alphabet, standard in Xinjiang). Codes, RTL script, ULY/Chagatai-Latin transcription, agglutinative vocabulary shape, and notes. Load whenever a PhraseForge lesson targets Uyghur.
---

# Uyghur (uig) language conventions

## Codes

- `lang`: `uig`
- `script`: `arab`

Note: phraseforge-data stores Uyghur in `uig-cyrl` (Cyrillic); the canonical literary script and the script of this skill is the **Uyghur Arabic alphabet** (Perso-Arabic, RTL). If the source file uses Cyrillic, adapt accordingly and note the script in the lesson description.

## Transcription

Required (non-Latin script). Use **ULY** (Uyghur Latin Yéziqi) — the standardized Latin romanization:

| Arabic | ULY | | Arabic | ULY |
|--------|-----|-|--------|-----|
| ئا | a | | ئو | o |
| ئە | e | | ئۇ | u |
| ئى | i | | ئۆ | ö |
| ئې | é | | ئۈ | ü |
| ب | b | | پ | p |
| ت | t | | ج | j |
| چ | ch | | خ | x |
| د | d | | ر | r |
| ز | z | | ژ | zh |
| س | s | | ش | sh |
| ف | f | | غ | gh |
| ق | q | | ك | k |
| گ | g | | ڭ | ng |
| ل | l | | م | m |
| ن | n | | ھ | h |
| ۋ | w | | ي | y |

System attribute: `ULY`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Uyghur-specific rules:

- **No grammatical gender.** All nouns take `{N}`. Plural is formed with `لار-` / `لەر-` (`-lar`/`-lär`) suffix (vowel harmony).
- **Verbs:** infinitive/dictionary form (verb stem + `-maq`/`-mäk`), tag `{V}`.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
ئىت {N} = pies
öy {N} = dom (transcription: öy)
ئايال {N} = kobieta
بالا {N} = dziecko

سۆزلىمەك {V} = mowic
كۆرمەك {V} = widziec
بولماق {V} = byc
بارماق {V} = isc

كىچىك {Adj} = maly
تېز {Adv} = szybko
```

ULY transcriptions: `it`, `öy`, `ayal`, `bala`, `sözlimäk`, `körmäk`, `bolmaq`, `barmaq`, `kichik`, `téz`.

## Grammar notes (B1+)

- **Agglutinative SOV** language. Suffixes stack: case, plural, possessive, verb tense/aspect/person are all expressed by suffixes.
- **Vowel harmony**: suffixes alternate based on the last vowel of the stem (front/back).
- Verb tenses: present-future (`-idu`), past definite (`-di`), past evidential (`-ptiman`), etc.

## Translation

Translate to Polish (`pol`).

## Notes

- Uyghur is a Turkic language closely related to Uzbek. It uses the Perso-Arabic script (RTL) in China and Central Asia; a Cyrillic variant exists in former Soviet states.
- The Arabic-script Uyghur alphabet uses a full set of vowel letters (unlike Arabic proper, where short vowels are often omitted).
