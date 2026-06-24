---
name: phraseforge-lang-yid
description: Yiddish (Yidish, ISO 639-3 yid) language conventions for PhraseForge lessons. Codes, RTL Hebrew script, YIVO transcription, vocabulary shape (Germanic grammar in Hebrew letters, gender), and notes. Load whenever a PhraseForge lesson targets Yiddish.
---

# Yiddish (yid) language conventions

## Codes

- `lang`: `yid`
- `script`: `hebr`

## Transcription

Required (non-Latin script). Use **YIVO** standard romanization. System attribute: `YIVO`.

Key YIVO correspondences:
| Yiddish | YIVO | | Yiddish | YIVO |
|---------|------|-|---------|------|
| א | a | | ס | s |
| אַ | a | | ע | e |
| אָ | o | | פ | p / f |
| ב | b / v | | צ | ts |
| ג | g | | ק | k |
| ד | d | | ר | r |
| ה | h | | ש | sh |
| ו | v / u | | ת | t / s |
| ז | z | | יי | ay |
| ח | kh | | וו | v |
| י | y / i | | ײ | ey |
| כ | kh | | אי | i |
| ל | l | | | |
| מ | m | | | |
| נ | n | | | |

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Yiddish-specific rules (grammar is Germanic, written in Hebrew letters):

- **Nouns:** Yiddish has 3 genders: `m`, `f`, `n`. Include the **definite article** (`דער`/`der` m., `די`/`di` f., `דאָס`/`dos` n.) in the headword. Mark gender: `{N m}` / `{N f}` / `{N n}`.
- **Verbs:** infinitive (ending `-n` or `-en`), tag `{V}`.
- **Adjectives:** uninflected predicative form, tag `{Adj}`.

```
דער הונט {N m} = pies
דאָס הויז {N n} = dom
די פרוי {N f} = kobieta
דאָס קינד {N n} = dziecko

רעדן {V} = mowic
זען {V irreg} = widziec
זיין {V irreg} = byc
האָבן {V irreg} = miec

קלײן {Adj} = maly
גיך {Adv} = szybko
```

YIVO transcriptions: `der hunt`, `dos hoyz`, `di froy`, `dos kind`, `redn`, `zen`, `zayn`, `hobn`, `kleyn`, `gikh`.

## Grammar notes (B1+)

- Yiddish grammar closely follows German; 4 cases (Nominative, Accusative, Dative, Genitive — genitive is archaic). Article and adjective endings follow German patterns.
- Extensive Hebrew/Aramaic component: many learned/religious terms come from Hebrew.

## Translation

Translate to Polish (`pol`). Yiddish `du` → informal; `ir` (formal/plural) → `Pan`/`Pani`/`wy`.

## Notes

- Yiddish script is **right-to-left** and uses Hebrew letters but represents a Germanic language.
- Two major dialect groups: Ashkenazic Eastern Yiddish (YIVO standard) and Western Yiddish (nearly extinct). Default to YIVO Eastern.
