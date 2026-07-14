---
name: anki-qa
description: Generate and review Anki-style flashcards stored as YAML files of Q/A/C/N records, organized as a deck manifest (flashcard.yml) referencing one *.yml file per subtopic. Use when the user invokes /anki-qa, asks to create or expand flashcards for a topic, or wants to review/improve an existing flashcard deck for learning something from scratch on a smartphone.
---

# Anki Q&A flashcard generator

Produce and maintain concise flashcards for learning a topic from scratch, stored as YAML records split across subtopic files and tied together by a deck manifest, `flashcard.yml`.

## Invocation

The user passes a directory (or an existing `flashcard.yml`/topic file inside one) and a topic description (topic may also just be given in the prompt, e.g. as a follow-up expanding a topic already in the deck). If no directory is given, ask before doing anything else.

## Directory layout

A deck lives in its own directory, e.g. `dat/comp/rust/`:

```
dat/comp/rust/
  flashcard.yml     <- deck manifest (see below)
  ownership.yml      <- card records for the "ownership" subtopic
  traits.yml          <- card records for the "traits" subtopic
  ...                 <- one *.yml per subtopic, named after it
```

Card data is never dumped into one giant file. Split the material into coherent subtopics (e.g. for a language: basics, ownership, types, traits, concurrency, tooling) and give each its own `*.yml`. This keeps individual files reviewable, lets a topic be extended in isolation, and avoids one file growing unbounded as coverage deepens over many sessions.

## `flashcard.yml`: the deck manifest

`flashcard.yml` itself holds no cards. It is boilerplate that:
- names the Anki deck (`deck.name`, using `::` for subdecks, e.g. `'Computer::Rust'`)
- points at the shared card model/templates (copy this block verbatim from an existing `flashcard.yml` in a sibling directory, or from `dat/comp/_template`/`dat/comp/_model` if this is the very first deck)
- lists every subtopic file under `data`, each tagged with its subtopic name

```yaml
deck:
  name: 'Computer::Rust'

model:
  name: Computer QA
  kind: normal
  style:
    css: ../_model/comp-qa.css
  templates:
    - name: Computer QA
      qfmt: ../_model/comp-qfmt.html
      afmt: ../_model/comp-afmt.html
  fields:
    - name: Q
      template: ../_template/Question.txt
      index: true
      format: markdown
      description: Question
    - name: A
      template: ../_template/Answer.txt
      format: markdown
      description: Answer
    - name: C
      template: ../_template/Code.txt
      description: Code
    - name: N
      template: ../_template/Notes.txt
      format: markdown
      description: Notes

data:
  - filename: ./ownership.yml
    tags: ['ownership']
  - filename: ./traits.yml
    tags: ['traits']
```

- Every subtopic file must have an entry under `data`, `filename` pointing at it and `tags` set to a single-element array naming the subtopic (used for Anki tag filtering — keep it lowercase, hyphenated, matching the filename stem).
- When adding a new subtopic file, add its `data` entry in the same edit — a topic file with no manifest entry is invisible to the deck.
- Never put `Q`/`A`/`C`/`N` records inside `flashcard.yml` itself — that file's shape is fixed (deck/model/data), and cards always live in the subtopic files it references.

## Subtopic file format

Each subtopic `*.yml` is a plain YAML list of card records:

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

1. Resolve the deck directory (ask if missing) and the topic (from the prompt, or ask if unclear).
2. If the deck already exists, read `flashcard.yml` first to see which subtopic files exist and what each covers.
3. Decide which subtopic file the new material belongs in:
   - If it clearly extends an existing subtopic's coverage, read that file fully first — new cards must not duplicate existing ones, and should fit the existing coverage/progression.
   - If it's a new coherent subtopic not yet represented, create a new `*.yml` file for it and add a corresponding `data` entry (with `tags`) to `flashcard.yml` in the same turn.
   - Don't create a new file for one or two stray facts that clearly belong in an existing subtopic file instead — reserve new files for genuinely distinct subtopics.
4. Thoroughly research the topic (use available skills/tools — web search, docs, codebase — as appropriate) before drafting cards. Do not invent facts.
5. Identify the important facts/concepts a learner needs, from fundamentals up, and plan a logical learning progression (basics before edge cases, prerequisites before dependents).
6. Draft cards:
   - One clear, atomic fact or concept per card — don't cram multiple ideas into one Q/A.
   - Write questions that are answerable from the answer alone (no hidden context).
   - Keep answers short; push supporting detail into `N` only if it's needed to grade/complete the answer, not as padding.
   - Use `C` for anything the learner would type or read as code/commands.
7. Append new cards to the end of the relevant subtopic file (existing cards are never reordered or rewritten unless the user asks for a review pass). Create the file (and its `flashcard.yml` entry) if it doesn't exist yet.
8. When asked to review/improve rather than add: read the whole subtopic file (or the whole deck), then propose concrete edits (fix ambiguous questions, split overloaded cards, cut fluff, correct errors, split an overgrown file into subtopics) and apply them — don't just add more cards on top of a flawed base.
9. Topics are expected to be expanded over multiple follow-up messages — treat each invocation as either growing coverage of an existing subtopic, adding a new subtopic file, or improving what's already there, not a one-shot dump.
