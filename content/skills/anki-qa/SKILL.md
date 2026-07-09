---
name: anki-qa
description: Generate and review Anki-style flashcards stored as a YAML file of Q/A/Code/Notes records, one file per topic. Use when the user invokes /anki-qa, asks to create or expand flashcards for a topic, or wants to review/improve an existing flashcard YAML file for learning something from scratch on a smartphone.
---

# Anki Q&A flashcard generator

Produce and maintain concise flashcards for learning a topic from scratch, stored as YAML records appended to a file.

## Invocation

The user passes a filename and a topic description (topic may also just be given in the prompt, e.g. as a follow-up expanding a topic already in the file). If no filename is given, ask for one before doing anything else.

## File format

Each file is a YAML list. Each record:

```yaml
- Q: |
    <question, markdown, concise>
  A: |
    <answer, markdown, concise>
  C: |
    <code snippet, only if the card is about a command/code>
  N: |
    <notes, only if extra criteria/context is needed to fully answer>
```

- `Q` and `A` are mandatory.
- `C` (code) and `N` (notes) are optional — add only when they genuinely add value, not by default.
- Every field is markdown. Keep fields short (ideally one paragraph) — cards are reviewed on a smartphone.
- `N` is for extra criteria the answer should cover, or context that clarifies scope. `C` is for actual code/commands/snippets, not prose.

## Workflow

1. Resolve the filename (ask if missing) and the topic (from the prompt, or ask if unclear).
2. If the file exists, read it fully first — new cards must not duplicate existing ones, and should fit the existing coverage/progression.
3. Thoroughly research the topic (use available skills/tools — web search, docs, codebase — as appropriate) before drafting cards. Do not invent facts.
4. Identify the important facts/concepts a learner needs, from fundamentals up, and plan a logical learning progression (basics before edge cases, prerequisites before dependents).
5. Draft cards:
   - One clear, atomic fact or concept per card — don't cram multiple ideas into one Q/A.
   - Write questions that are answerable from the answer alone (no hidden context).
   - Keep answers short; push supporting detail into `N` only if it's needed to grade/complete the answer, not as padding.
   - Use `C` for anything the learner would type or read as code/commands.
6. Append new cards to the end of the file (existing cards are never reordered or rewritten unless the user asks for a review pass). Create the file if it doesn't exist yet.
7. When asked to review/improve rather than add: read the whole file, then propose concrete edits (fix ambiguous questions, split overloaded cards, cut fluff, correct errors) and apply them — don't just add more cards on top of a flawed base.
8. Topics are expected to be expanded over multiple follow-up messages — treat each invocation as either growing coverage of the topic or improving what's already there, not a one-shot dump.
