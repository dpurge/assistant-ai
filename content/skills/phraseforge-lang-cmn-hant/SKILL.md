---
name: phraseforge-lang-cmn-hant
description: Mandarin Chinese Traditional (Putonghua, ISO 639-3 cmn, Traditional script hant) language conventions for PhraseForge lessons. Codes, Pinyin transcription, vocabulary shape (measure words, no gender/articles), and notes. Load whenever a PhraseForge lesson targets Mandarin in Traditional Chinese.
---

# Mandarin Chinese — Traditional (cmn, hant) language conventions

## Codes

- `lang`: `cmn`
- `script`: `hant`

## Transcription

Required (non-Latin script). Use **Pinyin** with tone marks. System attribute: `Pinyin`.

(Traditional Chinese is used in Taiwan, Hong Kong, and Macau. The spoken language is the same as Simplified; only the written characters differ.)

## Vocabulary format

Identical to `phraseforge-lang-cmn-hans` — use the same tag conventions, measure-word notation, and grammar guidance. Write all headwords in **Traditional** characters.

```
狗 {N cl zhi} = pies
房子 {N cl ge} = dom
女人 {N cl ge} = kobieta
孩子 {N cl ge} = dziecko

說話 {V} = mowic
看見 {V} = widziec
是 {V} = byc
有 {V} = miec

小 {Adj} = maly
快 {Adv} = szybko
```

Pinyin: `gǒu`, `fángzi`, `nǚrén`, `háizi`, `shuōhuà`, `kànjiàn`, `shì`, `yǒu`, `xiǎo`, `kuài`.

## Notes

- Most characters are identical between Simplified and Traditional; differences concentrate in a few hundred high-frequency characters (e.g., 说 → 說, 见 → 見).
- In Taiwan, the standard romanization is **Zhuyin** (bopomofo) in primary education, but Pinyin is widely understood and used here.
- TOCFL vocabulary levels can be noted as notes when helpful.
