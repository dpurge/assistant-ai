# Report shape

Abstract structure of a report produced by `research-core`. Each output skill renders it differently — what's described here is the conceptual layout.

## Sections

1. **Title** — short, declarative; the answer to "what is this about?"
2. **Summary** — one paragraph (~60–100 words). State the main finding(s) plainly. No padding.
3. **Body** — H2 sections, one per sub-topic. Each H2 holds:
   - Plain-prose paragraphs (not bullet lists by default; use bullets only for genuine enumerations).
   - **Claims with inline citations.** Citation format below.
4. **Open questions** — explicitly enumerate things sources disagreed on or did not cover.
5. **References** — full citation list at the end.

## Citation format

Inline citation key in square brackets:

    ... uses bitwise tricks for fast hashing [Knuth1997].

Each key is resolved in the references list at the bottom of the report:

    [Knuth1997] Knuth, D. *The Art of Computer Programming, Vol 3.* Addison-Wesley, 1997. ISBN 0-201-89685-0.
    [arXiv:2401.12345] Author A, Author B. "Title." arXiv:2401.12345, 2024.
    [MDN:CSS-Grid] MDN Web Docs. "CSS Grid Layout." Retrieved 2026-06-22.

Every reference must include either a URL or a DOI/ISBN. Web references include the retrieval date — content rots.

## Length

- **Quick read:** ~500–1000 words. Default if the user doesn't specify.
- **Background:** ~1500–3000 words.
- **Deep dive:** 3000+ words.

If the user doesn't specify, ask before going long.
