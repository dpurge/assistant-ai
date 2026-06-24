---
name: phraseforge-lang-rus
description: Russian (Russkiy, ISO 639-3 rus) language conventions for PhraseForge lessons. Codes, vocabulary shape (no article + gender/animate), verb aspect tags, and notes. Load whenever a PhraseForge lesson targets Russian.
---

# Russian (rus) language conventions

## Codes

- `lang`: `rus`
- `script`: `cyrl`

## Transcription

Not required by default (Cyrillic is excluded from the transcription block per `phraseforge-web` convention). For advanced learners, phonetic hints or stress marks can be added inline in parentheses.

## Vocabulary format

Tag conventions follow `phraseforge-core/references/vocabulary.md`. Russian-specific rules:

- **Nouns:** no articles; mark gender: `{N m}` / `{N f}` / `{N n}`. Add `an` for animate masculines: `{N m an}`.
- **Verbs:** infinitive form. Mark aspect: `{V impf}` / `{V pf}`. Add `irreg` for irregular.
- **Adjectives:** masculine singular nominative short/long form — use long: `{Adj}`.

```
sobaka {N f} = pies
dom {N m} = dom
zhenshchina {N f} = kobieta
rebyonok {N m an} = dziecko

govorit {V impf} = mowic
uvidet {V pf} = zobaczyc
byt {V irreg} = byc
imet {V impf} = miec

malenkiy {Adj} = maly
bystro {Adv} = szybko
```

(Write headwords in Cyrillic: `собака`, `дом`, `женщина`, `ребёнок`, `говорить`, `увидеть`, `быть`, `иметь`, `маленький`, `быстро`.)

## Declension tables (B1+)

Russian has 6 cases. Show noun/adjective paradigms when relevant.

## Translation

Translate to Polish (`pol`). Russian `ты` → informal; `вы` (formal/plural) → `Pan`/`Pani`/`wy`.

## Cultural notes

- Note Soviet vs. contemporary vocabulary differences when relevant.
- Stress (ударение) can shift between forms; mark with an acute accent (`о́`) in vocabulary when important.
