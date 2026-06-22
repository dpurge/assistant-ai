---
name: research-web
description: Render a research report (produced by research-core) as a Docusaurus MDX page. The output filename and path are arguments the caller supplies — no hardcoded local-clone path. Targets the dpurge/dpurge.github.io site by convention but works against any stock Docusaurus site. Use when the user asks for a research report written to a markdown/MDX file, or mentions Docusaurus, a personal site, or dpurge.github.io.
user-invocable: true
---

# Research → Docusaurus page

Render a research report (produced by `research-core`) as a single MDX page suitable for inclusion in a Docusaurus site.

This skill owns the **target-system specifics** for stock Docusaurus pages. The default integration is **dpurge/dpurge.github.io**, but the skill does **not** hardcode a local-clone path — the caller passes the output filename/path as an argument.

## Skeleton (fill in the placeholders)

```markdown
---
title: <Short declarative title>
description: <One sentence>
tags: [<tag1>, <tag2>]
---

<One-paragraph summary, ~60–100 words.>

## <First section heading>

<Prose paragraphs with inline citations like ([Knuth 1997](https://...)) or
footnotes[^k1].>

### <Optional subsection>

<More prose.>

## Open questions

- <Thing sources disagreed on or didn't cover.>

## References

- [Knuth 1997] Knuth, D. *TAOCP Vol 3.* Addison-Wesley, 1997. ISBN ...
- [arXiv:2401.12345] Author. "Title." arXiv:2401.12345, 2024.
- [MDN: CSS-Grid] MDN Web Docs. Retrieved 2026-06-22.

[^k1]: <Footnote text if using the footnote citation style.>
```

Pick **one** citation style per page (inline links OR footnotes); don't mix.

## When invoked

1. Confirm the **output path** with the user — the full path to the destination `.mdx` (or `.md`) file. There is no default location.
2. Use `research-core` for the report content.
3. Render the report per `references/docusaurus-conventions.md`:
   - Frontmatter: `title`, `description`, optional `sidebar_position`, `tags`.
   - Use H2/H3 for sections (the H1 comes from frontmatter).
   - Inline citations rendered as Docusaurus footnotes or markdown links — whichever the user's site supports.
   - References section at the bottom.
4. Write the file via the `Write` tool. Don't print the report content back to the user.
5. Confirm with a one-line message naming the file written.

## Constraints

- Use only **stock Docusaurus** features: standard markdown, admonitions (`:::note`, `:::tip`, `:::warning`, `:::danger`), tabs (only if the site has the tabs plugin enabled — confirm before using).
- **Do not** use any phraseforge-web custom components (`<Text>`, `<Exercise>`, `<Questions>`, `<L>`, `<N>`, etc.) — those are specific to phraseforge-web and won't render on a stock Docusaurus site.
- Check whether the target file already exists before writing; if it does, ask before overwriting.

## References

- `references/docusaurus-conventions.md` — frontmatter, sidebar/category, admonitions, image handling.
