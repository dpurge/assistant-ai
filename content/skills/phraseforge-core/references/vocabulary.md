# Vocabulary grammar tag conventions

Grammar tags appear inside `{}` in the vocabulary code fence:

```
headword {grammar tag} [transcription] = translation (notes)
```

Tags are **not yet finalised** — real source data (phraseforge-data) may use a different
notation and will be normalised later. Use the canonical tags below when the AI generates
lesson content. When parsing real `.ff` files, preserve whatever tags are already there.

## Canonical tag format

```
{POS [gender] [number] [modifier ...]}
```

All parts are **space-separated**. Each individual token must contain **only alphanumeric characters** (`A–Z`, `a–z`, `0–9`) — no dashes, dots, slashes, or other punctuation. Tags are **case-sensitive**: `N` (noun) and `n` (neuter gender) are distinct. POS is required; everything else is optional and language-dependent.

### Part-of-speech base tags

| Tag | Part of speech | Example headword |
|-----|---------------|------------------|
| `N` | noun | `der Hund {N m}` |
| `V` | verb | `gehen {V}` |
| `Adj` | adjective | `klein {Adj}` |
| `Adv` | adverb | `schnell {Adv}` |
| `Pron` | pronoun | `ich {Pron}` |
| `Prep` | preposition | `auf {Prep}` |
| `Conj` | conjunction | `und {Conj}` |
| `Num` | numeral | `zwei {Num}` |
| `Part` | particle | `doch {Part}` |
| `Interj` | interjection | `ach {Interj}` |
| `Phrase` | fixed phrase / idiom | `Guten Morgen {Phrase}` |

### Gender modifiers (nouns)

| Tag | Gender |
|-----|--------|
| `m` | masculine |
| `f` | feminine |
| `n` | neuter |

### Number modifiers

Include `sg` / `pl` only when listing paradigm pairs (e.g. Arabic broken plurals or
German plural-only nouns). Omit for standard dictionary headwords in singular.

| Tag | Number |
|-----|--------|
| `sg` | singular |
| `pl` | plural |

### Verb modifiers

| Tag | Meaning |
|-----|---------|
| `sep` | separable prefix (German: `aufstehen {V sep}`) |
| `refl` | reflexive (`sich freuen {V refl}`) |
| `tr` | transitive |
| `intr` | intransitive |

### Adjective modifiers

| Tag | Meaning |
|-----|---------|
| `comp` | comparative form |
| `sup` | superlative form |

## Full examples

```
der Hund {N m} = pies
die Katze {N f} = kot
das Kind {N n} = dziecko
die Hunde {N m pl} = psy

gehen {V} = iść
aufstehen {V sep} = wstawać
sich freuen {V refl} = cieszyć się

klein {Adj} = mały
schnell {Adv} = szybko
ich {Pron} = ja
und {Conj} = i
```

Arabic paradigm pair (both sg and pl listed separately):
```
كَبِيرٌ {N m sg} = duży
كِبَارٌ {N m pl} = duzi
```

## What the per-language skills add

Each `phraseforge-lang-<iso>` skill specifies:
- Whether gender is relevant and how to mark it.
- Whether articles are part of the headword (German `der/die/das`, Spanish `el/la`).
- Any language-specific tags beyond the above (e.g. Spanish `{V ar}` / `{V er}` / `{V ir}` verb class — no dashes).
- Whether number should appear on standard headwords (usually no).
