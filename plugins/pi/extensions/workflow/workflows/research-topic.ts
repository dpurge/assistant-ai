/**
 * research-topic.ts — production: topic description → sourced Markdown report.
 *
 * Engine-driven multi-source pipeline (deterministic searches; the small model
 * only integrates). For each source the engine runs the Python search tool once
 * per topic (a search ACTION), then a focused model step folds the raw results
 * into a running list of cited paragraphs:
 *
 *   topics → [web → wiki → arxiv → rag] (each: search action + integrate model)
 *          → draft → review → save
 *
 * Each paragraph carries a `source` citation; the draft assembles a report per
 * research-core/references/report-shape.md, and review tightens it.
 */

import type { ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join } from "node:path";

import { type RetryableContext, type Runtime, type WorkflowStep } from "../engine.ts";
import { PiStepExecutor } from "../pi-executor.ts";
import { loadSkill, shell } from "../shell.ts";
import { runWithUi } from "../harness.ts";
import type { WorkflowDefinition } from "../registry.ts";

interface Paragraph {
  text: string;
  source: string;
}

interface ResearchCtx extends RetryableContext {
  input: string;
  cwd: string;
  outFile?: string;
  topic: string;
  topics?: string[];
  paragraphs?: Paragraph[];
  raw_web?: unknown;
  raw_wiki?: unknown;
  raw_arxiv?: unknown;
  raw_rag?: unknown;
  report?: string;
  outPath?: string;
}

const PARA = Type.Object({ text: Type.String(), source: Type.String() });
const TOOLS = "skills/research-core/tools";

interface Source {
  id: string;
  name: string;
  tool: string;
  args: (topic: string) => string[];
  rawKey: keyof ResearchCtx;
  cite: string;
  ragOk?: boolean; // rag-query.py exits 1 for "no hits" (not an error)
}

const SOURCES: Source[] = [
  { id: "web", name: "Web", tool: `${TOOLS}/web-search.py`, args: (t) => [t, "--limit", "5"], rawKey: "raw_web", cite: "web:<url>" },
  { id: "wiki", name: "Wikipedia", tool: `${TOOLS}/wikipedia-search.py`, args: (t) => [t], rawKey: "raw_wiki", cite: "wiki:<url>" },
  { id: "arxiv", name: "arXiv", tool: `${TOOLS}/arxiv-search.py`, args: (t) => [t], rawKey: "raw_arxiv", cite: "arxiv:<id>" },
  { id: "rag", name: "local knowledge base", tool: `${TOOLS}/rag-query.py`, args: (t) => [t], rawKey: "raw_rag", cite: "local:<file>", ragOk: true },
];

/** Trim long string fields so raw results don't overwhelm a small model. */
function compact(hits: unknown[]): unknown[] {
  return hits.slice(0, 5).map((h) => {
    if (h && typeof h === "object") {
      const o: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(h)) o[k] = typeof v === "string" && v.length > 300 ? v.slice(0, 300) : v;
      return o;
    }
    return h;
  });
}

const topics: WorkflowStep<ResearchCtx> = {
  id: "topics",
  kind: "model",
  system: "Propose the subtopics a report on the given topic should cover. Return a JSON array of 3–8 short strings.",
  reads: ["topic"],
  prompt: (v) => `Topic: ${v.topic}`,
  outputSchema: Type.Array(Type.String()),
  produces: "topics",
  validate(ctx) {
    const n = ctx.topics?.length ?? 0;
    return n >= 3 && n <= 8 ? { ok: true } : { ok: false, message: `need 3–8 subtopics, got ${n}.` };
  },
  next() {
    return "web-search";
  },
};

/** Build the (search action, integrate model) pair for one source. */
function searchPair(src: Source, nextId: string): WorkflowStep<ResearchCtx>[] {
  const search: WorkflowStep<ResearchCtx> = {
    id: `${src.id}-search`,
    kind: "action",
    async action(ctx, io) {
      const raw: Array<{ topic: string; hits: unknown[] }> = [];
      for (const t of (ctx.topics ?? []).slice(0, 8)) {
        const res = await io.shell.runTool(src.tool, src.args(t));
        let hits: unknown[] = [];
        if (res.code === 0 || (src.ragOk && res.code === 1)) {
          try {
            hits = JSON.parse(res.stdout || "[]");
          } catch {
            hits = [];
          }
        }
        raw.push({ topic: t, hits: compact(Array.isArray(hits) ? hits : []) });
      }
      return { [src.rawKey]: raw } as Partial<ResearchCtx>;
    },
    next() {
      return `${src.id}-integrate`;
    },
  };

  const isWeb = src.id === "web";
  const integrate: WorkflowStep<ResearchCtx> = {
    id: `${src.id}-integrate`,
    kind: "model",
    system:
      `Integrate ${src.name} search results into the running list of report paragraphs. ` +
      `Each paragraph is a short Markdown passage with a 'source' citation of the form "${src.cite}". ` +
      `Drop unreliable or duplicate content, add new well-supported facts, keep every paragraph cited. ` +
      `Return JSON only.` +
      (isWeb ? " Also return a possibly-revised list of subtopics." : ""),
    reads: (isWeb ? ["topic", "topics", "paragraphs", src.rawKey] : ["topic", "paragraphs", src.rawKey]) as (keyof ResearchCtx)[],
    prompt: (v) =>
      `Topic: ${v.topic}\n\nCurrent paragraphs:\n${JSON.stringify((v as ResearchCtx).paragraphs ?? [])}\n\n` +
      `${src.name} results:\n${JSON.stringify((v as Record<string, unknown>)[src.rawKey] ?? [])}`,
    outputSchema: isWeb
      ? Type.Object({ topics: Type.Array(Type.String()), paragraphs: Type.Array(PARA) })
      : Type.Array(PARA),
    produces: isWeb ? undefined : "paragraphs", // web merges {topics, paragraphs}
    validate(ctx) {
      return (ctx.paragraphs?.length ?? 0) > 0 ? { ok: true } : { ok: false, message: "no paragraphs after integration." };
    },
    next() {
      return nextId;
    },
  };

  return [search, integrate];
}

const draft: WorkflowStep<ResearchCtx> = {
  id: "draft",
  kind: "model",
  system:
    "Write a Markdown research report following the report shape: Title, Summary (~80 words), Body " +
    "(H2 per subtopic, prose with inline [Key] citations), Open questions, References (resolve every " +
    "citation key, one per paragraph source). Output Markdown only.",
  reads: ["topic", "topics", "paragraphs"],
  skills: ["research-core"],
  prompt: (v) =>
    `Topic: ${v.topic}\nSubtopics: ${(v.topics ?? []).join(", ")}\n\n` +
    `Cited paragraphs:\n${JSON.stringify(v.paragraphs ?? [])}`,
  produces: "report",
  validate(ctx) {
    return ctx.report?.trim() ? { ok: true } : { ok: false, message: "empty draft." };
  },
  next() {
    return "review";
  },
};

const review: WorkflowStep<ResearchCtx> = {
  id: "review",
  kind: "model",
  system:
    "Revise the report: shorten where possible, improve readability, and remove claims not backed by " +
    "a cited source. Keep the References section intact. Output the revised Markdown only.",
  reads: ["report"],
  prompt: (v) => `${v.report}`,
  produces: "report",
  validate(ctx) {
    return ctx.report?.trim() ? { ok: true } : { ok: false, message: "empty review." };
  },
  next() {
    return "save";
  },
};

const save: WorkflowStep<ResearchCtx> = {
  id: "save",
  kind: "action",
  async action(ctx) {
    const date = new Date().toISOString().slice(0, 10);
    const slug = ctx.topic.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40);
    const rel = ctx.outFile ?? `reports/${date}-${slug}.md`;
    const outPath = isAbsolute(rel) ? rel : join(ctx.cwd, rel);
    await mkdir(dirname(outPath), { recursive: true });
    await writeFile(outPath, String(ctx.report), "utf8");
    return { outPath };
  },
  next() {
    return null;
  },
};

export const researchTopicWorkflow: WorkflowDefinition = {
  name: "research-topic",
  description: "Research a topic across web + Wikipedia + arXiv + local RAG → sourced Markdown report (out: <file>.md)",
  async execute(input, ctx: ExtensionCommandContext) {
    const { outFile, topic } = parseInput(input);
    if (!topic) {
      ctx.ui.notify("Usage: /workflow research-topic <topic description> <output.md>", "warning");
      return;
    }

    // Chain the source pairs: topics → web → wiki → arxiv → rag → draft.
    const pairs: WorkflowStep<ResearchCtx>[] = [];
    SOURCES.forEach((src, i) => {
      const nextId = i + 1 < SOURCES.length ? `${SOURCES[i + 1].id}-search` : "draft";
      pairs.push(...searchPair(src, nextId));
    });
    const graph: Record<string, WorkflowStep<ResearchCtx>> = { topics, draft, review, save };
    for (const step of pairs) graph[step.id] = step;

    const runtime: Runtime<ResearchCtx> = { executor: new PiStepExecutor(ctx), io: { shell }, loadSkill };
    const wfctx: ResearchCtx = { input, cwd: ctx.cwd, outFile, topic };
    const result = await runWithUi(ctx, graph, "topics", wfctx, runtime);
    if (result?.outPath) ctx.ui.notify(`Report written → ${result.outPath}`, "info");
  },
};

/** A trailing `*.md` token (or `--out <file>`) is the output; the rest is the topic. */
function parseInput(raw: string): { outFile?: string; topic: string } {
  const tokens = raw.trim().split(/\s+/).filter(Boolean);
  let outFile: string | undefined;
  const rest: string[] = [];
  for (let i = 0; i < tokens.length; i++) {
    if (tokens[i] === "--out") outFile = tokens[++i];
    else if (/\.md$/i.test(tokens[i]) && !outFile) outFile = tokens[i];
    else rest.push(tokens[i]);
  }
  return { outFile, topic: rest.join(" ") };
}
