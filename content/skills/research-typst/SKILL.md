---
name: research-typst
description: Generate a Typst source file (.typ) from a research report, suitable for `typst compile` to PDF. Use when the user mentions Typst, PDF, printable report, or asks for a research write-up as PDF.
user-invocable: true
---

# Research → Typst (PDF source)

Render a research report (produced by `research-core`) as a Typst `.typ` source file. Pair with `typst compile report.typ report.pdf` (Typst is Apache-2.0, open source — https://github.com/typst/typst).

## Status

Stub. The tool driver is `tools/typst-export.py` (not yet implemented). Invoke it as:

```
uv run --script tools/typst-export.py <report.md|report.mdx> [--out report.typ]
```

`uv run --script` honors the tool's PEP-723 inline dependency block (see [PEP 723](https://peps.python.org/pep-0723/)); the current stub uses stdlib only. Template + style in `references/typst-format.md`.

## Planned behavior

**Inputs:** a research report (text or file path).

**Outputs:** a `.typ` file. Run `typst compile report.typ report.pdf` to render PDF.

## References

- `references/typst-format.md` — Typst template + style conventions for research reports.
