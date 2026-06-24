---
name: phraseforge-lang-jpn
description: Japanese (Nihongo, ISO 639-3 jpn) language conventions for PhraseForge lessons. Codes, mixed Japn script, Hepburn transcription, vocabulary shape (no gender/articles, JLPT levels as notes), politeness levels, and notes. Load whenever a PhraseForge lesson targets Japanese.
---

# Japanese (jpn) language conventions

## Codes

- `lang`: `jpn`
- `script`: `japn`

## Transcription

Required (non-Latin script). Use **Hepburn** romanization (modified Hepburn). System attribute: `Hepburn`.

Key Hepburn rules:
- Long vowels: `ā ī ū ē ō` (macrons) — or double vowel `aa`, `uu`, `oo` when macrons are unavailable.
- `ん` before `b/m/p` → `m`: `shinbun` → `shimbun`.
- `っ` → doubled consonant: `kitte`.
- Particles: `は` = `wa`, `を` = `o`, `へ` = `e` (pronunciation-based romanization).

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Japanese-specific rules:

- **No grammatical gender, no articles, minimal inflection** (for nouns). All nouns take `{N}`.
- **Verbs:** dictionary form (plain non-past). Tag `{V}`. Mark verb group: `{V 1}` (Group 1 / godan, end in u-row consonant), `{V 2}` (Group 2 / ichidan, end in -iru/-eru), `{V irreg}` (する, くる).
- **Adjectives:** two classes — i-adjectives (`{Adj i}`) and na-adjectives (`{Adj na}`).
- **JLPT level** can be noted in `notes` field (e.g. `N5`, `N4`, …).

```
犬 {N} = pies
家 {N} = dom
女性 {N} = kobieta
子供 {N} = dziecko

話す {V 1} = mowic
見る {V 2} = widziec
だ {V irreg} = byc (kopula, styl nieformalny)
ある {V 1} = byc; istniec (rzeczy nieozywione)
いる {V 2} = byc; istniec (rzeczy ozywione)

小さい {Adj i} = maly
速い {Adj i} = szybki
きれいな {Adj na} = ladny; czysty
```

Hepburn: `inu`, `ie`, `josei`, `kodomo`, `hanasu`, `miru`, `da`, `aru`, `iru`, `chiisai`, `hayai`, `kirei na`.

## Grammar notes (B1+)

- Japanese word order is **SOV**. Postpositions (particles) mark grammatical roles.
- Verb conjugation distinguishes politeness level (plain vs. masu-form). Default to masu-form in lesson examples unless the source is colloquial.
- Honorific speech (keigo): sonkeigo, kenjōgo, teineigo — note level in advanced lessons.

## Translation

Translate to Polish (`pol`). Japanese `あなた` (`anata`) → general "you"; polite register defaults to `Pan`/`Pani` in Polish.

## Notes

- Japanese uses three writing systems simultaneously: **hiragana** (syllabary, native grammar), **katakana** (loanwords, emphasis), **kanji** (Chinese-derived ideographs).
- Furigana (small hiragana above kanji) can be included for A1–B1 learners; write as `漢字[かんじ]` in the source text if the MDX parser supports it, otherwise transcribe.
