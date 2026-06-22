# Models block

A fenced code block with info string `models lang=<lang3> script=<script>`.

Models show **phrase patterns and progressively built example sentences**
that combine the vocabulary into usable chunks. Each line is one entry,
syntactically the same as a vocabulary line **but without grammar marks**:

```
<phrase> = <Polish translation>
<phrase> [<transcription>] = <Polish translation>
```

- Transcription brackets `[…]` are required for non-Latin scripts.
- No `{grammar marks}`.

## Pattern

Build up from short pieces to a full sentence, like this Arabic example:

````mdx
```models lang=arb script=arab
لماذا [limaḏā] = dlaczego
فاض [fāḍa] = wezbrał (o rzece)
نهر الفرات [nahru al-Furāt] = rzeka Eufrat
في سوريا [fī Sūriyā] = w Syrii
لماذا فاض نهر الفرات؟ [limaḏā fāḍa nahru al-Furāt?] = Dlaczego wezbrała rzeka Eufrat?
لماذا فاض نهر الفرات في سوريا؟ [limaḏā fāḍa nahru al-Furāt fī Sūriyā?] = Dlaczego wezbrała rzeka Eufrat w Syrii?
```
````

Blank lines separate groups of related entries (one group per
sentence/idea). Each group should culminate in a full sentence from the
text.

## How many groups

3–6 groups, each covering one important sentence or construction from
the text. Aim for 20–60 lines total.

## Latin-script example (German)

````mdx
```models lang=deu script=latn
das Haus = dom
mein Haus = mój dom
in meinem Haus = w moim domu
Ich wohne in meinem Haus. = Mieszkam w moim domu.

ein Buch = książka
ein gutes Buch = dobra książka
Sie liest ein gutes Buch. = Ona czyta dobrą książkę.
```
````
