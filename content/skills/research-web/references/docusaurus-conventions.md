# Docusaurus conventions

Conventions for rendering a research report as a stock Docusaurus page (https://docusaurus.io). No project-specific custom components.

## Frontmatter

```yaml
---
title: <Short declarative title>
description: <One sentence — also used as the <meta description>>
sidebar_position: 10        # optional; numeric sort within the category
tags: [<tag>, <tag>, ...]   # optional
---
```

`title` becomes the page H1; do **not** also write `# Title` at the top of the body.

## Section headings

- `##` for top-level sections.
- `###` for subsections.
- Avoid going deeper than `###` except in rare cases.

## Admonitions

```
:::note
A neutral aside.
:::

:::tip
A non-obvious recommendation.
:::

:::warning
A pitfall or caveat.
:::

:::danger
A footgun the reader should not ignore.
:::
```

## Citations

Two acceptable styles — pick one per page and stay consistent:

**Footnotes** (Docusaurus + remark-footnotes):

    The algorithm runs in linear time[^knuth].

    [^knuth]: Knuth, D. *TAOCP Vol 3*, 1997.

**Inline markdown links**:

    The algorithm runs in linear time ([Knuth 1997](https://...)).

## Images

Place files under `static/img/` in the Docusaurus site and reference with `![alt](/img/file.png)`. Inline base64 or external URLs are discouraged for built pages.

## What NOT to use

- `<Text>`, `<Exercise>`, `<Questions>`, `<L>`, `<N>`, `<Hint>`, `<WordBank>`, `<Match>`, `<Column>` — phraseforge-web's custom components.
- The `vocabulary`, `models`, and `dialog` code fences — also phraseforge-web specific.
- React/JSX inside MDX without a plugin enabling it on the target site.

## Verification

Suggest to the user: `npm run start` in the Docusaurus repo locally to preview before pushing.
