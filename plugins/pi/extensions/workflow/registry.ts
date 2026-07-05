/**
 * registry.ts — the single source of truth for named workflows.
 *
 * Each workflow is a self-contained WorkflowDefinition that owns its steps,
 * services, and output. The dispatcher (index.ts) only looks one up by name and
 * calls execute(). Add a workflow by appending to REGISTRY.
 */

import type { ExtensionAPI, ExtensionCommandContext } from "@earendil-works/pi-coding-agent";

import { SimulatedExecutor } from "./executor.ts";
import type { Runtime, StepIO } from "./engine.ts";
import { runWithUi } from "./harness.ts";
import { buildDesignWorkflow, makeContext, renderMarkdown, type WorkflowContext } from "./workflows/design.ts";

import { phraseforgeMdxWorkflow } from "./workflows/phraseforge-mdx.ts";
import { researchTopicWorkflow } from "./workflows/research-topic.ts";
import { workflow as phraseforgeText } from "./workflows/phraseforge-text.ts";

export interface WorkflowDefinition {
  /** Dispatch key and command argument, e.g. "phraseforge-mdx". */
  name: string;
  /** One-line summary shown by the list command and autocomplete. */
  description: string;
  /** Run end-to-end: build the graph, pick services, render/emit output, report via ctx.ui. */
  execute(input: string, ctx: ExtensionCommandContext, pi: ExtensionAPI): Promise<void>;
}

/** Offline, deterministic demo of the harness itself (no model, no tools). */
const designWorkflow: WorkflowDefinition = {
  name: "design",
  description: "Demo: design a system via a validated state machine (offline, deterministic)",
  async execute(input, ctx, pi) {
    const io: StepIO = { shell: { async runTool() { throw new Error("design demo uses no shell"); } } };
    const runtime: Runtime<WorkflowContext> = { executor: new SimulatedExecutor(), io };
    const { graph, startId } = buildDesignWorkflow();
    const seed = input || "Build an authentication system";
    const result = await runWithUi(ctx, graph, startId, makeContext(seed), runtime);
    if (result) {
      pi.sendMessage({ customType: "workflow_result", content: renderMarkdown(result), display: true });
    }
  },
};

export const REGISTRY: WorkflowDefinition[] = [
  designWorkflow,
  phraseforgeMdxWorkflow,
  researchTopicWorkflow,
  phraseforgeText,
];

export function findWorkflow(name: string): WorkflowDefinition | undefined {
  return REGISTRY.find((w) => w.name === name);
}
