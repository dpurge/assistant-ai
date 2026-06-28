/**
 * design.ts — a SAMPLE workflow in the declarative step model.
 *
 * Illustrates the shape, not the domain: each model step declares its own
 * focused prompt, a `reads` visibility allow-list (so the model sees ONLY what
 * it needs), and an output schema; `architecture` branches. Schemas here are
 * plain JSON-Schema literals (not typebox) so this file stays dependency-free
 * and the `import.meta.main` self-demo runs head-less under `deno`.
 */

import {
  type RetryableContext,
  type Runtime,
  type StepIO,
  type WorkflowStep,
  runWorkflow,
} from "../engine.ts";
import { SimulatedExecutor } from "../executor.ts";

export interface WorkflowContext extends RetryableContext {
  seed: string;
  goal?: string;
  requirements?: string[];
  architecture?: { modules: string[] };
  implementationPlan?: string[];
}

export function makeContext(seed: string): WorkflowContext {
  return { seed };
}

const goal: WorkflowStep<WorkflowContext> = {
  id: "goal",
  kind: "action",
  async action(ctx) {
    return { goal: ctx.seed.trim() };
  },
  validate(ctx) {
    return ctx.goal ? { ok: true } : { ok: false, message: "Goal cannot be empty." };
  },
  next() {
    return "requirements";
  },
};

const requirements: WorkflowStep<WorkflowContext> = {
  id: "requirements",
  kind: "model",
  system: "You extract concise software requirements.",
  reads: ["goal"],
  prompt: (v) => `Extract requirements.\nGoal:\n${v.goal}`,
  outputSchema: { type: "array", items: { type: "string" } },
  produces: "requirements",
  validate(ctx) {
    return ctx.requirements?.length ? { ok: true } : { ok: false, message: "Need at least one requirement." };
  },
  next() {
    return "architecture";
  },
};

const architecture: WorkflowStep<WorkflowContext> = {
  id: "architecture",
  kind: "model",
  system: "You design a minimal module architecture.",
  reads: ["requirements"],
  prompt: (v) => `Design architecture.\nRequirements:\n${(v.requirements ?? []).join("\n")}`,
  outputSchema: {
    type: "object",
    required: ["modules"],
    properties: { modules: { type: "array", items: { type: "string" } } },
  },
  produces: "architecture",
  validate(ctx) {
    return (ctx.architecture?.modules.length ?? 0) >= 2
      ? { ok: true }
      : { ok: false, message: "Need at least two modules." };
  },
  // Branch: only plan an implementation when there's an API to build.
  next(ctx) {
    return ctx.architecture!.modules.includes("API") ? "implementation" : "render";
  },
};

const implementation: WorkflowStep<WorkflowContext> = {
  id: "implementation",
  kind: "model",
  system: "You produce a short, ordered implementation plan.",
  reads: ["architecture"],
  prompt: (v) => `Implementation plan.\nArchitecture:\n${(v.architecture?.modules ?? []).join(", ")}`,
  outputSchema: { type: "array", items: { type: "string" } },
  produces: "implementationPlan",
  validate(ctx) {
    return ctx.implementationPlan?.length ? { ok: true } : { ok: false, message: "Implementation plan is empty." };
  },
  next() {
    return "render";
  },
};

// Terminal action; the caller renders the markdown so the graph stays I/O-free.
const render: WorkflowStep<WorkflowContext> = {
  id: "render",
  kind: "action",
  async action() {
    return {};
  },
  next() {
    return null;
  },
};

export function buildDesignWorkflow(): {
  graph: Record<string, WorkflowStep<WorkflowContext>>;
  startId: string;
} {
  return {
    graph: { goal, requirements, architecture, implementation, render },
    startId: "goal",
  };
}

export function renderMarkdown(ctx: WorkflowContext): string {
  const lines = [`# ${ctx.goal}`, "", "## Requirements", ""];
  lines.push(...(ctx.requirements ?? []).map((r) => `- ${r}`));
  lines.push("", "## Architecture", "");
  lines.push(...(ctx.architecture?.modules ?? []).map((m) => `- ${m}`));
  if (ctx.implementationPlan?.length) {
    lines.push("", "## Implementation", "");
    lines.push(...ctx.implementationPlan.map((s) => `- ${s}`));
  }
  return lines.join("\n");
}

// ---------------------------------------------------------------------------
// Self-demo: `deno run plugins/pi/extensions/workflow/workflows/design.ts`
// Dormant under Pi (jiti loads index.ts as the entry, so this is never main).
// ---------------------------------------------------------------------------
async function demo(): Promise<void> {
  const io: StepIO = { shell: { async runTool() { throw new Error("no shell in demo"); } } };
  const runtime: Runtime<WorkflowContext> = { executor: new SimulatedExecutor(), io };
  const { graph, startId } = buildDesignWorkflow();
  const log = (msg: string) => console.log(msg);

  log("=== Scenario 1: happy path (branches into implementation) ===");
  const ctx = await runWorkflow(graph, startId, makeContext("Build an authentication system"), runtime, {
    onStep: (e) => log(`  [${e.state}] attempt=${e.attempt} ${e.phase}${e.message ? `: ${e.message}` : ""}`),
  });
  log("\n--- Final output ---\n" + renderMarkdown(ctx) + "\n");

  log("=== Scenario 2: failing gate (empty goal) shows retry + WorkflowError ===");
  try {
    await runWorkflow(graph, startId, makeContext("   "), runtime, {
      maxAttempts: 2,
      onStep: (e) => log(`  [${e.state}] attempt=${e.attempt} ${e.phase}${e.message ? `: ${e.message}` : ""}`),
    });
  } catch (err) {
    log(`  caught ${(err as Error).name}: ${(err as Error).message}`);
  }
}

if (import.meta.main) {
  await demo();
}
