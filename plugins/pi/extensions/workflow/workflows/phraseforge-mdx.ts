/**
 * phraseforge-mdx.ts — production workflow: source URL/file → PhraseForge MDX lesson.
 *
 * Built for a small local model (Gemma via Ollama): every step is focused —
 * it reads only the context it needs (`reads`), injects the language-specific
 * skill only where it matters, uses small schemas, and prose steps return raw
 * text (more reliable than JSON for small models). The final `save` step renders
 * via mdx-export.py, whose Pydantic validation is the deterministic gate.
 *
 * Steps: read → clean → detect → [transcribe] → translate → vocabulary → models
 *        → grammar → questions → exercises → save
 */

import type { ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { isAbsolute, join } from "node:path";

import { type RetryableContext, type Runtime, type WorkflowStep } from "../engine.ts";
import { PiStepExecutor } from "../pi-executor.ts";
import { loadSkill, shell } from "../shell.ts";
import { runWithUi } from "../harness.ts";
import type { WorkflowDefinition } from "../registry.ts";

const MDX_TOOL = "skills/phraseforge-web/tools/mdx-export.py";
const TRANSLITERATED = new Set(["latn", "cyrl", "grek"]); // scripts that need NO transcription
const MAX_SOURCE_CHARS = 8000;

interface SourceRef {
  kind: "url" | "file";
  value: string;
}

interface PhraseCtx extends RetryableContext {
  input: string;
  cwd: string;
  sourceRef: SourceRef;
  level: string;
  source?: string;
  text?: string;
  language?: string;
  script?: string;
  title?: string;
  transcription?: string;
  translation?: string;
  vocabulary?: unknown;
  models?: unknown;
  grammar?: string;
  questions?: unknown;
  exercises?: unknown;
  outPath?: string;
}

/** Map the detected language (+script for Mandarin) to its phraseforge-lang skill. */
function langSkill(ctx: PhraseCtx): string[] {
  const l = ctx.language;
  if (!l) return [];
  if (l === "cmn") return [`phraseforge-lang-cmn-${ctx.script === "hant" ? "hant" : "hans"}`];
  return [`phraseforge-lang-${l}`];
}

// --- Steps -----------------------------------------------------------------

const read: WorkflowStep<PhraseCtx> = {
  id: "read",
  kind: "action",
  async action(ctx) {
    const { kind, value } = ctx.sourceRef;
    let raw: string;
    let isHtml: boolean;
    if (kind === "url") {
      const resp = await fetch(value);
      if (!resp.ok) throw new Error(`fetch failed: ${resp.status} ${resp.statusText}`);
      raw = await resp.text();
      isHtml = /text\/html/i.test(resp.headers.get("content-type") ?? "") || /<\/?[a-z][\s\S]*>/i.test(raw);
    } else {
      raw = await readFile(value, "utf8");
      isHtml = value.toLowerCase().endsWith(".html");
    }
    const text = (isHtml ? htmlToText(raw) : raw).slice(0, MAX_SOURCE_CHARS);
    return { source: text };
  },
  validate(ctx) {
    return ctx.source?.trim() ? { ok: true } : { ok: false, message: "source text is empty." };
  },
  next() {
    return "clean";
  },
};

const clean: WorkflowStep<PhraseCtx> = {
  id: "clean",
  kind: "model",
  system: "Clean the given source into simple, readable Markdown. Keep only the main body text; drop navigation, ads, and boilerplate. Output Markdown only.",
  reads: ["source"],
  prompt: (v) => `Source:\n\n${v.source}`,
  produces: "text",
  validate(ctx) {
    return (ctx.text as string)?.trim() ? { ok: true } : { ok: false, message: "cleaned text is empty." };
  },
  next() {
    return "detect";
  },
};

const detect: WorkflowStep<PhraseCtx> = {
  id: "detect",
  kind: "model",
  system: "Identify the language of the text. Return JSON only.",
  reads: ["text"],
  prompt: (v) =>
    `Text:\n${(v.text ?? "").slice(0, 1200)}\n\n` +
    `Return the ISO 639-3 language code, the ISO 15924 script code (lowercase), and a short lesson title.`,
  outputSchema: Type.Object({
    language: Type.String({ description: "ISO 639-3, e.g. deu, arb, cmn" }),
    script: Type.String({ description: "ISO 15924 lowercase, e.g. latn, arab, hans" }),
    title: Type.String(),
  }),
  // no `produces` → merge {language, script, title} into ctx
  validate(ctx) {
    if (!/^[a-z]{3}$/.test(ctx.language ?? "")) return { ok: false, message: "language must be ISO 639-3 (3 letters)." };
    if (!/^[a-z]{4}$/.test(ctx.script ?? "")) return { ok: false, message: "script must be ISO 15924 (4 letters, lowercase)." };
    return { ok: true };
  },
  // Branch: skip transcription for scripts that don't need it (transcription stays undefined).
  next(ctx) {
    return TRANSLITERATED.has(ctx.script ?? "") ? "translate" : "transcribe";
  },
};

const transcribe: WorkflowStep<PhraseCtx> = {
  id: "transcribe",
  kind: "model",
  system: "Romanize the text using the transcription system specified by the language skill. Output the transcription only.",
  reads: ["text", "language", "script"],
  skills: langSkill,
  prompt: (v) => `Transcribe this ${v.language} text:\n\n${v.text}`,
  produces: "transcription",
  validate(ctx) {
    return ctx.transcription?.trim() ? { ok: true } : { ok: false, message: "transcription is empty." };
  },
  next() {
    return "translate";
  },
};

const translate: WorkflowStep<PhraseCtx> = {
  id: "translate",
  kind: "model",
  system: "Translate the text into natural Polish prose. Output the Polish translation only.",
  reads: ["text"],
  prompt: (v) => `Translate to Polish:\n\n${v.text}`,
  produces: "translation",
  validate(ctx) {
    return ctx.translation?.trim() ? { ok: true } : { ok: false, message: "translation is empty." };
  },
  next() {
    return "vocabulary";
  },
};

const vocabulary: WorkflowStep<PhraseCtx> = {
  id: "vocabulary",
  kind: "model",
  system:
    "Extract a vocabulary list from the text following the language skill's rules for headword shape and grammar tags. " +
    "Each entry: headword (dictionary form), grammar tag, Polish translation (multiple senses joined with '; '), " +
    "and transcription for non-Latin scripts. Aim for 15–40 entries by level. Return JSON only.",
  reads: ["text", "transcription", "translation", "language", "script"],
  skills: langSkill,
  prompt: (v) => `Build vocabulary from this ${v.language} text:\n\n${v.text}`,
  outputSchema: Type.Array(
    Type.Object({
      headword: Type.String(),
      grammar: Type.Optional(Type.String()),
      transcription: Type.Optional(Type.String()),
      translation: Type.Optional(Type.String()),
      notes: Type.Optional(Type.String()),
    }),
  ),
  produces: "vocabulary",
  validate(ctx) {
    const n = (ctx.vocabulary as unknown[])?.length ?? 0;
    return n >= 10 ? { ok: true } : { ok: false, message: `need ≥10 vocabulary entries, got ${n}.` };
  },
  next() {
    return "models";
  },
};

const models: WorkflowStep<PhraseCtx> = {
  id: "models",
  kind: "model",
  system:
    "Build 3–6 model phrase patterns that illustrate constructions from the text, each building toward a full sentence. " +
    "Each: pattern (foreign), Polish translation (required), transcription for non-Latin scripts. Return JSON only.",
  reads: ["text", "transcription", "translation"],
  skills: langSkill,
  prompt: (v) => `Build model patterns from this text:\n\n${v.text}`,
  outputSchema: Type.Array(
    Type.Object({
      pattern: Type.String(),
      translation: Type.String(),
      transcription: Type.Optional(Type.String()),
      notes: Type.Optional(Type.String()),
    }),
  ),
  produces: "models",
  validate(ctx) {
    const n = (ctx.models as unknown[])?.length ?? 0;
    return n >= 3 && n <= 8 ? { ok: true } : { ok: false, message: `need 3–8 models, got ${n}.` };
  },
  next() {
    return "grammar";
  },
};

const grammar: WorkflowStep<PhraseCtx> = {
  id: "grammar",
  kind: "model",
  system:
    "Write a short grammar block in Polish Markdown explaining the key grammar the text exercises, " +
    "using the language skill's grammar notes. Keep it focused (a few paragraphs and/or a small table). Output Markdown only.",
  reads: ["text", "language", "script"],
  skills: langSkill,
  prompt: (v) => `Explain the key grammar in this ${v.language} text, in Polish:\n\n${v.text}`,
  produces: "grammar",
  validate(ctx) {
    return ctx.grammar?.trim() ? { ok: true } : { ok: false, message: "grammar block is empty." };
  },
  next() {
    return "questions";
  },
};

const questions: WorkflowStep<PhraseCtx> = {
  id: "questions",
  kind: "model",
  system: "Write 3–6 short, open-ended comprehension questions IN THE LESSON'S LANGUAGE. Return a JSON array of strings.",
  reads: ["text", "language"],
  prompt: (v) => `Write comprehension questions in ${v.language} for this text:\n\n${v.text}`,
  outputSchema: Type.Array(Type.String()),
  produces: "questions",
  validate(ctx) {
    const n = (ctx.questions as unknown[])?.length ?? 0;
    return n >= 3 && n <= 8 ? { ok: true } : { ok: false, message: `need 3–8 questions, got ${n}.` };
  },
  next() {
    return "exercises";
  },
};

const ALLOWED_EXERCISES = new Set([
  "translation",
  "fill-gaps",
  "word-order",
  "multiple-choice",
  "matching",
  "true-false",
  "open-answer",
]);

const exercises: WorkflowStep<PhraseCtx> = {
  id: "exercises",
  kind: "model",
  system:
    "Create 4–6 exercises mixing types. Always include translation, fill-gaps, word-order, and multiple-choice. " +
    "Each: {type, instruction (Polish), items (array of strings)}. Return JSON only.",
  reads: ["text", "vocabulary"],
  prompt: (v) => `Create exercises based on this text:\n\n${v.text}`,
  outputSchema: Type.Array(
    Type.Object({
      type: Type.String(),
      instruction: Type.Optional(Type.String()),
      items: Type.Array(Type.String()),
    }),
  ),
  produces: "exercises",
  validate(ctx) {
    const ex = (ctx.exercises as Array<{ type: string }>) ?? [];
    if (ex.length < 3 || ex.length > 6) return { ok: false, message: `need 3–6 exercises, got ${ex.length}.` };
    const bad = ex.find((e) => !ALLOWED_EXERCISES.has(e.type));
    return bad ? { ok: false, message: `unsupported exercise type "${bad.type}".` } : { ok: true };
  },
  next() {
    return "save";
  },
};

const save: WorkflowStep<PhraseCtx> = {
  id: "save",
  kind: "action",
  async action(ctx, io) {
    const date = new Date().toISOString().slice(0, 10);
    const lesson: Record<string, unknown> = {
      version: 1,
      title: ctx.title,
      lang: ctx.language,
      script: ctx.script,
      translation_lang: "pol",
      translation_script: "latn",
      level: ctx.level,
      date,
      vocabulary: ctx.vocabulary,
      models: ctx.models,
      source: { kind: "text", content: ctx.text },
      translation: ctx.translation,
      grammar: ctx.grammar,
      questions: ctx.questions,
      exercises: ctx.exercises,
    };
    if (ctx.transcription) lesson.transcription = ctx.transcription;

    const dir = join(ctx.cwd, "docs", String(ctx.language), String(ctx.level));
    await mkdir(dir, { recursive: true });
    const outPath = join(dir, `${date}-${await nextSeq(dir, date)}.mdx`);

    const res = await io.shell.runTool(MDX_TOOL, ["--out", outPath], { stdin: JSON.stringify(lesson) });
    if (res.code !== 0) throw new Error(res.stderr.trim() || `mdx-export exited ${res.code}`);
    return { outPath };
  },
  next() {
    return null;
  },
};

/** Next free per-day sequence letter (a, b, c, …) in the level directory. */
async function nextSeq(dir: string, date: string): Promise<string> {
  let taken: string[] = [];
  try {
    taken = (await readdir(dir))
      .filter((f) => f.startsWith(`${date}-`) && f.endsWith(".mdx"))
      .map((f) => f.slice(date.length + 1, -4));
  } catch {
    /* dir doesn't exist yet */
  }
  let seq = "a";
  while (taken.includes(seq)) seq = String.fromCharCode(seq.charCodeAt(0) + 1);
  return seq;
}

// --- Definition ------------------------------------------------------------

export const phraseforgeMdxWorkflow: WorkflowDefinition = {
  name: "phraseforge-mdx",
  description: "Build a PhraseForge MDX lesson from a URL or file (message also carries the CEFR level)",
  async execute(input, ctx: ExtensionCommandContext) {
    const sourceRef = parseSource(input);
    const level = (input.match(/\b([abc][12])\b/i)?.[1] ?? "").toLowerCase();
    if (!sourceRef || !level) {
      ctx.ui.notify("Usage: /workflow phraseforge-mdx <url|file> <level a1..c2>", "warning");
      return;
    }
    const runtime: Runtime<PhraseCtx> = {
      executor: new PiStepExecutor(ctx),
      io: { shell },
      loadSkill,
    };
    const graph = {
      read, clean, detect, transcribe, translate,
      vocabulary, models, grammar, questions, exercises, save,
    };
    const wfctx: PhraseCtx = { input, cwd: ctx.cwd, sourceRef, level };
    const result = await runWithUi(ctx, graph, "read", wfctx, runtime);
    if (result?.outPath) ctx.ui.notify(`Lesson written → ${result.outPath}`, "info");
  },
};

/** Extract a URL or a local file path from the message (level is parsed separately). */
function parseSource(raw: string): SourceRef | undefined {
  const tokens = raw.trim().split(/\s+/).filter(Boolean);
  const url = tokens.find((t) => /^https?:\/\//i.test(t));
  if (url) return { kind: "url", value: url };
  const file = tokens.find((t) => !/^[abc][12]$/i.test(t) && /[./\\]/.test(t));
  if (file) return { kind: "file", value: isAbsolute(file) ? file : file };
  return undefined;
}

/** Crude but dependency-free HTML→text: drop scripts/styles/tags, decode common entities. */
function htmlToText(s: string): string {
  return s
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}
