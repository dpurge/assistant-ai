---
name: phraseforge-lang-kor
description: Korean (Hangugeo, ISO 639-3 kor) language conventions for PhraseForge lessons. Codes, Hangul script, Revised Romanization transcription, vocabulary shape (no gender/articles, honorific levels), and notes. Load whenever a PhraseForge lesson targets Korean.
---

# Korean (kor) language conventions

## Codes

- `lang`: `kor`
- `script`: `kore`

## Transcription

Required (non-Latin script). Use **Revised Romanization of Korean** (RR, official South Korean standard). System attribute: `RR`.

Key RR rules:
- Vowels: `a`, `ae`, `ya`, `yae`, `eo`, `e`, `yeo`, `ye`, `o`, `wa`, `wae`, `oe`, `yo`, `u`, `wo`, `we`, `wi`, `yu`, `eu`, `ui`, `i`.
- Initial consonants: `g`, `kk`, `n`, `d`, `tt`, `r/l`, `m`, `b`, `pp`, `s`, `ss`, `(silent)`, `j`, `jj`, `ch`, `k`, `t`, `p`, `h`.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Korean-specific rules:

- **No grammatical gender, no articles.** All nouns take `{N}`. Sino-Korean (`{N sino}`) vs. native Korean (`{N native}`) origin can be noted.
- **Verbs:** dictionary form (ending `-다`), tag `{V}`. Mark formality if the source is specifically formal/informal: `{V formal}` / `{V informal}`.
- **Adjectives:** dictionary form (ending `-다`), tag `{Adj}`.

```
개 {N native} = pies
집 {N native} = dom
여자 {N sino} = kobieta
아이 {N native} = dziecko

말하다 {V} = mowic
보다 {V} = widziec
이다 {V} = byc (kopula)
있다 {V} = miec; byc; istniec

작다 {Adj} = byc malym
빠르다 {Adj} = byc szybkim
```

RR transcriptions: `gae`, `jip`, `yeoja`, `ai`, `malhada`, `boda`, `ida`, `itda`, `jakda`, `ppareuda`.

## Grammar notes (B1+)

- Korean word order is **SOV**. Postpositions (subject marker `-이/가`, object marker `-을/를`, topic marker `-은/는`, etc.) mark grammatical roles.
- **Speech levels** (honorifics) are grammatically encoded; verbs change form based on the relationship between speaker and listener. Standard polite: `-아요/어요`; formal polite: `-(스)ㅂ니다`.
- Sino-Korean vocabulary (from Chinese) coexists with native Korean; Sino-Korean numbers vs. native Korean numbers are used in different contexts.

## Translation

Translate to Polish (`pol`). Korean `너` (`neo`) → informal; `당신` (`dangsin`) or honorific forms → `Pan`/`Pani`.

## Notes

- Hangul is a phonemic alphabet arranged in syllabic blocks — it is relatively easy to learn to read (~1–2 days for the alphabet).
- TOPIK vocabulary levels (1–6) can be noted in the `notes` field.
