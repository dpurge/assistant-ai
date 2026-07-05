import type { ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import { dirname, isAbsolute, join } from "node:path";
import { Type } from "typebox";

import { type RetryableContext, type Runtime, type WorkflowStep } from "../engine.ts";
import { PiStepExecutor } from "../pi-executor.ts";
import { loadSkill, shell } from "../shell.ts";
import { runWithUi } from "../harness.ts";
import type { WorkflowDefinition } from "../registry.ts";

// I N T E R F A C E S

interface WorkflowContext extends RetryableContext {
  source: string;
  output: string | undefined;
  raw?: string;
  language?: string;
  script?: string;
  text?: string;
  transcription?: string;
  translation?: string;
  vocabulary?: string;
}

// H E L P E R S

// scripts that need NO transcription
const TRANSLITERATED = new Set(["latn", "cyrl", "grek"]);

/** Map the detected language (+script for Mandarin) to its phraseforge-lang skill. */
function langSkill(ctx: WorkflowContext): string[] {
  const language = ctx.language;
  if (!language) return [];
  if (language === "cmn") return [`phraseforge-lang-cmn-${ctx.script === "hant" ? "hant" : "hans"}`];
  return ["phraseforge-core", `phraseforge-lang-${language}`];
}

// S T E P S

const read: WorkflowStep<WorkflowContext> = {
  id: "read",
  kind: "action",

  async action(ctx) {
    const source = ctx.source;

    let raw: string;
    let isHtml: boolean;

    if (source.startsWith('http://') || source.startsWith('https://')) {
      const response = await fetch(source);
      if (!response.ok) throw new Error(`fetch failed: ${response.status} ${response.statusText}`);
      raw = await response.text();
      isHtml = /text\/html/i.test(response.headers.get("content-type") ?? "") || /<\/?[a-z][\s\S]*>/i.test(raw);
    } else {
      raw = await readFile(source, "utf8");
      isHtml = source.toLowerCase().endsWith(".html");
    }
    raw = (isHtml ? htmlToText(raw) : raw);
    return { raw };
  },

  validate(ctx) {
    return ctx.raw?.trim() ? { ok: true } : { ok: false, message: "raw text is empty." };
  },

  next() {
    return "clean";
  },
};


const clean: WorkflowStep<WorkflowContext> = {
  id: "clean",
  kind: "model",

  system:
    "Convert RAW TEXT between <BEGIN_RAW_TEXT> and <END_RAW_TEXT> into clean Markdown." +
    
    "Rules:" +
    "- Do not explain." +
    "- Do not analyze." +
    "- Do not describe the HTML." +
    "- Output only Markdown." +
    "- Preserve the text content." +
    "- Remove scripts, styles, and navigation." +
    "- If something cannot be represented in Markdown, use plain text." +

    "Keep:" +
    "- The article title." +
    "- The main article body." +
    "- Headings, paragraphs, lists, blockquotes, and tables." +

    "Remove:" +
    "- Image captions." +
    "- Image credits." +
    "- Image attribution (e.g. \"Image source\", \"Getty Images\")." +
    "- Figure descriptions (\"Caption\")." +
    "- Author information." +
    "- Publication date." +
    "- Reading time." +
    "- Article metadata." +
    "- Navigation." +
    "- Social sharing buttons." +
    "- Related articles." +
    "- Advertisements." +
    "- Footer and header." +
    "- Any boilerplate not part of the article text." +
    
    "Output only the cleaned Markdown.",

  reads: ["raw"],
  // skills: ["research-core"],

  prompt: (v) =>
    "\n<BEGIN_RAW_TEXT>\n" + v.raw + "\n<END_RAW_TEXT>\n",
  
  produces: "text",

  validate(ctx) {
    return ctx.text?.trim() ? { ok: true } : { ok: false, message: "empty text." };
  },

  next() {
    return "detect";
  },
};

const detect: WorkflowStep<WorkflowContext> = {
  id: "detect",
  kind: "model",

  system: "Identify the language and the script of the text. Return JSON only.",

  reads: ["text"],

  prompt: (v) =>
    `Text:\n${(v.text ?? "").slice(0, 1200)}\n\n` +
    `Return the ISO 639-3 language code, the ISO 15924 script code (lowercase).` +
    "\n<START_TEXT>\n" + v.text + "\n<END_TEXT>\n",
  
  outputSchema: Type.Object({
    language: Type.String({ description: "ISO 639-3, e.g. deu, arb, cmn" }),
    script: Type.String({ description: "ISO 15924 lowercase, e.g. latn, arab, hans, hant, grek, cyrl, hebr" }),
  }),
  
  validate(ctx) {
    if (!/^[a-z]{3}$/.test(ctx.language ?? "")) return { ok: false, message: "language must be ISO 639-3 (3 lowercase letters)." };
    if (!/^[a-z]{4}$/.test(ctx.script ?? "")) return { ok: false, message: "script must be ISO 15924 (4 lowercase letters)." };
    return { ok: true };
  },
  
  next(ctx) {
    return TRANSLITERATED.has(ctx.script ?? "") ? "translate" : "transcribe";
  },
};


const transcribe: WorkflowStep<WorkflowContext> = {
  id: "transcribe",
  kind: "model",

  system:
    "Romanize the text between <START_TEXT> and <END_TEXT> using the transcription system specified by the language skill." +
    "Output the transcription only.",

  reads: ["text", "language", "script"],

  skills: langSkill,

  prompt: (v) => 
    `Transcribe this ${v.language} text:` +
    "\n<START_TEXT>\n" + v.text + "\n<END_TEXT>\n",

  produces: "transcription",

  validate(ctx) {
    return ctx.transcription?.trim() ? { ok: true } : { ok: false, message: "transcription is empty." };
  },

  next() {
    return "translate";
  },
};

const translate: WorkflowStep<WorkflowContext> = {
  id: "translate",
  kind: "model",

  system: "Translate the text between <START_TEXT> and <END_TEXT> into natural Polish prose. Output the Polish translation only.",

  reads: ["text"],

  prompt: (v) =>
    `Translate to Polish:` +
    "\n<START_TEXT>\n" + v.text + "\n<END_TEXT>\n",

  produces: "translation",

  validate(ctx) {
    return ctx.translation?.trim() ? { ok: true } : { ok: false, message: "translation is empty." };
  },

  next() {
    return "vocabulary";
  },
};


const vocabulary: WorkflowStep<WorkflowContext> = {
  id: "vocabulary",
  kind: "model",

  system:
    "Extract a vocabulary list from the text between <START_TEXT> and <END_TEXT> following the language skill's rules. " +
    "Each entry: headword (dictionary form), grammar tag, Polish translation (multiple senses joined with '; '), " +
    "and transcription for non-Latin scripts." +
    "Aim for 15–40 entries by level.",

  reads: ["text", "transcription", "translation", "language", "script"],

  skills: langSkill,

  prompt: (v) => 
    `Build vocabulary from this ${v.language} text.` +
    `You MUST use phraseforge-core and phraseforge-lang-${v.language} skills.` +
    "\n<START_TEXT>\n" + v.text + "\n<END_TEXT>\n" +
    "\n<START_TRANSLATION>\n" + v.translation + "\n<END_TRANSLATION>\n" +
    "\n<START_TRANSCRIPTION>\n" + v.transcription + "\n<END_TRANSCRIPTION>\n",

  // outputSchema: Type.Array(
  //   Type.Object({
  //     headword: Type.String(),
  //     grammar: Type.Optional(Type.String()),
  //     transcription: Type.Optional(Type.String()),
  //     translation: Type.Optional(Type.String()),
  //     notes: Type.Optional(Type.String()),
  //   }),
  // ),

  produces: "vocabulary",

  validate(ctx) {
    // ctx.vocabulary = (ctx.vocabulary as string)
    //   .trim()
    //   .replace(/^```(?:json)?\s*/i, "")
    //   .replace(/\s*```$/, "");
    // const n = ctx.vocabulary.length ?? 0;
    // return n >= 10 ? { ok: true } : { ok: false, message: `need ≥10 vocabulary entries, got ${n}.` };

    return ctx.vocabulary?.trim() ? { ok: true } : { ok: false, message: "vocabulary is empty." };
  },

  next() {
    return "save";
  },
};



const save: WorkflowStep<WorkflowContext> = {
  id: "save",
  kind: "action",

  async action(ctx, io) {
    const date = new Date().toISOString().slice(0, 10);
    const output = ctx.output ?? `${date}.md`;
    await mkdir(dirname(output), { recursive: true });
    await writeFile(
      output,
      String(ctx.text) + "\n\n" +
      `${ctx.language}-${ctx.script}` + "\n\n" +
      String(ctx.transcription) + "\n\n" +
      String(ctx.translation) + "\n\n" +
      String(ctx.vocabulary),
      "utf8");
    return { output };
  },

  next() {
    return null;
  },
};

// W O R K F L O W

function parameters(raw: string): {
  message: string;
  source?: string;
  output?: string
} {
  const tokens = raw.trim().split(/\s+/).filter(Boolean);

  let source: string | undefined;
  let output: string | undefined;

  const rest: string[] = [];

  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] === "--source") source = tokens[++i];
    else if (tokens[i] === "--output") output = tokens[++i];
    else rest.push(tokens[i]);
  }

  return {
    message: rest.join(" "),
    source,
    output,
  };
}

export const workflow: WorkflowDefinition = {
  name: "phraseforge-text",
  description: "Read text and format it as markdown with transcription and translation",
  async execute(input, ctx: ExtensionCommandContext) {
    const { message, source, output } = parameters(input);

    if (!source) {
      ctx.ui.notify("Usage: /workflow phraseforge-text --source <file or url> [--output <report.md>]", "warning");
      return;
    }

    const graph = {
      read,
      clean,
      detect,
      transcribe,
      translate,
      vocabulary,
      save,
    };

    const runtime: Runtime<WorkflowContext> = {
      executor: new PiStepExecutor(ctx),
      io: { shell },
      loadSkill,
    };

    const wfctx: WorkflowContext = {
      source: source,
      output: output,
      // raw: undefined,
      // language: undefined,
      // script: undefined,
      // text: undefined,
      // transcription: undefined,
      // translation: undefined,
    };

    const result = await runWithUi(ctx, graph, "read", wfctx, runtime);

    if (result?.output) ctx.ui.notify(`File written → ${result.output}`, "info");
  }
}

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