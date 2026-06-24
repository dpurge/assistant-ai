---
name: phraseforge-lang-tur
description: Turkish (Turkce, ISO 639-3 tur) language conventions for PhraseForge lessons. Codes, vocabulary shape (agglutinative, no gender, vowel harmony), verb/noun tags, and notes. Load whenever a PhraseForge lesson targets Turkish.
---

# Turkish (tur) language conventions

## Codes

- `lang`: `tur`
- `script`: `latn`

## Transcription

Not needed. Turkish uses Latin script (reformed 1928). Preserve special characters: `ç ğ ı İ ö ş ü`. Note: `I` (capital ı) and `İ` (capital i) are distinct letters.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Turkish-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`. Mark plural when it appears in the source (suffix varies by vowel harmony: `-lar`/`-ler`).
- **Verbs:** infinitive form (ending `-mak`/`-mek`). Tag `{V}`. Add `irreg` for irregular.
- **Adjectives:** uninflected form, tag `{Adj}`.

```
kopek {N} = pies
ev {N} = dom
kadin {N} = kobieta
cocuk {N} = dziecko

konusmak {V} = mowic
gormek {V} = widziec
olmak {V} = byc
sahip olmak {V} = miec

kucuk {Adj} = maly
hizli {Adv} = szybko
```

(Actual headwords with Turkish characters: `köpek`, `ev`, `kadın`, `çocuk`, `konuşmak`, `görmek`, `olmak`, `küçük`, `hızlı`.)

## Grammar notes (B1+)

- **Agglutinative SOV** language: suffixes stack for case (`-ı/i/u/ü`, `-a/e`, `-da/de`, `-dan/den`, `-ın/in`), number, possessive, tense, person.
- **Vowel harmony**: front/back and rounded/unrounded vowels — suffixes must match the last vowel in the stem.
- No copula in present tense (`ben öğrenciyim` = I am a student).

## Translation

Translate to Polish (`pol`). Turkish `sen` → informal; `siz` (formal/plural) → `Pan`/`Pani`/`wy`.
