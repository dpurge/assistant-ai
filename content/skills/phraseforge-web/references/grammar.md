# Grammar block

The optional `grammar` lesson field holds a short grammar explanation as **Markdown prose, written
in the translation language** (Polish by default). It renders as a `## Gramatyka` section, placed
after the translation block and before questions.

- Source the content from the language skill's "Grammar notes" guidance
  (`phraseforge-lang-<iso>/SKILL.md`) — e.g. case/conjugation tables, aspect particles, measure
  words — tailored to the lesson's CEFR level.
- Keep it focused: a few short paragraphs and/or a small Markdown table. It explains the grammar the
  source text exercises; it is not a full reference.
- Omit the field entirely when there is nothing useful to say (the section then does not render).

Example:

```json
{ "grammar": "## Rodzaj rzeczownika\n\nW języku niemieckim rzeczownik ma rodzaj…\n\n| przypadek | rodzajnik |\n|---|---|\n| Nom | der |\n| Akk | den |" }
```
