/**
 * engine.ts — a declarative, context-isolated workflow harness.
 *
 * This is the lesson, and it is PURE: it imports nothing from Pi, typebox, or
 * the filesystem, so it type-checks and runs anywhere. A workflow is a graph of
 * {@link WorkflowStep}s. There are two kinds:
 *
 *   • ModelStep  — declares WHAT the model sees and may do: a focused prompt, a
 *                  visibility allow-list (`reads`), skills to inject, tools it may
 *                  call, and an output schema. The engine builds a FRESH request
 *                  from the projected context only — no session history, no
 *                  sibling-step data — so small models stay focused.
 *   • ActionStep — deterministic local work (e.g. write a file). No model tokens.
 *
 * Every step has a validation gate; a step only advances once its gate passes.
 * All I/O (model calls, tool execution, skill loading) is delegated to an
 * injected {@link Runtime}, which is what keeps the engine pure and testable.
 */

/** Result of a validation gate. */
export type ValidationResult = { ok: true } | { ok: false; message: string };

/** A tool the model may call during a model step. The engine runs the loop. */
export interface ToolSpec {
  name: string;
  description: string;
  parameters: object; // typebox schema or plain JSON Schema (opaque here)
  execute(args: unknown): Promise<string>; // returns tool-result text
}

/** A single, self-contained model request — built fresh per step, no history. */
export interface StepRequest {
  system: string; // step role + injected skills + schema instruction
  prompt: string; // the sole user message (rendered from the projected context)
  tools?: ToolSpec[];
  outputSchema?: object; // when present, the executor must return validated JSON
  model?: string;
  effort?: string;
}

/** Performs a single model step. Implemented by Simulated and Pi executors. */
export interface StepExecutor {
  run(req: StepRequest): Promise<{ ok: true; value: unknown } | { ok: false; message: string }>;
}

/** Minimal shell surface action steps depend on (kept narrow for testing). */
export interface ShellRunner {
  runTool(
    toolRelPath: string,
    args: string[],
    opts?: { stdin?: string },
  ): Promise<{ code: number; stdout: string; stderr: string }>;
}

/** Services available to action steps. */
export interface StepIO {
  shell: ShellRunner;
}

/** Everything the engine needs from the outside world. */
export interface Runtime<Ctx> {
  executor: StepExecutor;
  io: StepIO;
  /** Returns a skill's SKILL.md text (Pi side reads the filesystem). */
  loadSkill?(name: string): Promise<string>;
}

export interface ModelStep<Ctx> {
  id: string;
  kind: "model";
  /** Focused role/system instruction for THIS step. */
  system?: string;
  /** Context keys visible to the model this step (projection allow-list). */
  reads?: (keyof Ctx)[];
  /** Render the user prompt from ONLY the projected context. */
  prompt(view: Partial<Ctx>): string;
  /**
   * Skill names whose SKILL.md is injected into this step's system prompt.
   * A function form lets a step pick skills from ctx (e.g. the detected language).
   */
  skills?: string[] | ((ctx: Ctx) => string[]);
  /** Tools the model may call this step. */
  tools?: ToolSpec[];
  /** Expected output schema; when set, the executor returns validated JSON. */
  outputSchema?: object;
  /** Override the model for this step (e.g. "anthropic/claude-haiku-4-5-20251001"). */
  model?: string;
  /** Effort level hint passed to the executor (e.g. "low" | "medium" | "high"). */
  effort?: string;
  /**
   * Context key under which the produced value is stored. Omit to MERGE the
   * produced object into ctx (`{...ctx, ...value}`) — handy when a step returns
   * several fields at once (e.g. {language, script, title}).
   */
  produces?: keyof Ctx;
  /** Extra deterministic gate beyond schema validation (e.g. shell a validator). */
  validate?(ctx: Ctx): ValidationResult | Promise<ValidationResult>;
  next(ctx: Ctx): string | null;
}

export interface ActionStep<Ctx> {
  id: string;
  kind: "action";
  /** Deterministic, non-model work; returns a partial context patch. */
  action(ctx: Ctx, io: StepIO): Promise<Partial<Ctx>>;
  validate?(ctx: Ctx): ValidationResult | Promise<ValidationResult>;
  next(ctx: Ctx): string | null;
}

export type WorkflowStep<Ctx> = ModelStep<Ctx> | ActionStep<Ctx>;

/** Emitted as the engine progresses; the engine's only output channel. */
export interface StepEvent {
  state: string;
  attempt: number;
  phase: "run" | "pass" | "retry" | "done";
  message?: string;
}

export class WorkflowError extends Error {
  constructor(
    public readonly state: string,
    message: string,
  ) {
    super(message);
    this.name = "WorkflowError";
  }
}

/** Contexts carry a slot the engine uses to feed validation feedback into retries. */
export interface RetryableContext {
  validationMessage?: string;
}

export interface RunOptions {
  maxAttempts?: number;
  onStep?: (event: StepEvent) => void;
}

/** Project only the allow-listed keys of ctx into a fresh view object. */
function project<Ctx>(ctx: Ctx, reads?: (keyof Ctx)[]): Partial<Ctx> {
  if (!reads) return {};
  const view: Partial<Ctx> = {};
  for (const key of reads) view[key] = ctx[key];
  return view;
}

/** Assemble a step's system prompt: role + injected skills + schema instruction. */
async function buildSystem<Ctx>(step: ModelStep<Ctx>, ctx: Ctx, runtime: Runtime<Ctx>): Promise<string> {
  const parts: string[] = [];
  if (step.system) parts.push(step.system);
  const skillNames = typeof step.skills === "function" ? step.skills(ctx) : step.skills ?? [];
  for (const name of skillNames) {
    const text = runtime.loadSkill ? await runtime.loadSkill(name) : "";
    if (text) parts.push(`# Skill: ${name}\n${text}`);
  }
  if (step.outputSchema) {
    parts.push(
      "Respond with ONLY a JSON value matching this JSON Schema, no prose, no code fences:\n" +
        JSON.stringify(step.outputSchema),
    );
  }
  return parts.join("\n\n");
}

/** Run one model step's request and surface the outcome as a gate result. */
async function runModelStep<Ctx extends RetryableContext>(
  step: ModelStep<Ctx>,
  ctx: Ctx,
  runtime: Runtime<Ctx>,
): Promise<{ ok: true; ctx: Ctx } | { ok: false; message: string }> {
  const view = project(ctx, step.reads);
  const feedback = ctx.validationMessage ? `\n\nPrevious attempt failed: ${ctx.validationMessage}` : "";
  const req: StepRequest = {
    system: await buildSystem(step, ctx, runtime),
    prompt: step.prompt(view) + feedback,
    tools: step.tools,
    outputSchema: step.outputSchema,
    model: step.model,
    effort: step.effort,
  };
  const res = await runtime.executor.run(req);
  if (!res.ok) return res;
  // produces set → store under that key; omitted → merge the produced object.
  const next = step.produces
    ? { ...ctx, [step.produces]: res.value }
    : { ...ctx, ...(res.value as object) };
  return { ok: true, ctx: next as Ctx };
}

/**
 * Drive a workflow graph from `startId` until a step returns next() === null.
 * The loop gates every transition; failures retry with feedback, then throw.
 */
export async function runWorkflow<Ctx extends RetryableContext>(
  graph: Record<string, WorkflowStep<Ctx>>,
  startId: string,
  ctx: Ctx,
  runtime: Runtime<Ctx>,
  opts: RunOptions = {},
): Promise<Ctx> {
  const maxAttempts = opts.maxAttempts ?? 3;
  const onStep = opts.onStep ?? (() => {});

  let currentId: string | null = startId;

  while (currentId !== null) {
    const step: WorkflowStep<Ctx> = graph[currentId];
    if (!step) throw new WorkflowError(currentId, `no step registered for id "${currentId}"`);

    let passed = false;
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      onStep({ state: step.id, attempt, phase: "run" });

      if (step.kind === "model") {
        const out = await runModelStep(step, ctx, runtime);
        if (!out.ok) {
          ctx.validationMessage = out.message;
          onStep({ state: step.id, attempt, phase: "retry", message: out.message });
          continue;
        }
        ctx = out.ctx;
      } else {
        ctx = { ...ctx, ...(await step.action(ctx, runtime.io)) };
      }

      const gate = step.validate ? await step.validate(ctx) : ({ ok: true } as ValidationResult);
      if (gate.ok) {
        ctx.validationMessage = undefined;
        onStep({ state: step.id, attempt, phase: "pass" });
        passed = true;
        break;
      }
      ctx.validationMessage = gate.message;
      onStep({ state: step.id, attempt, phase: "retry", message: gate.message });
    }

    if (!passed) {
      throw new WorkflowError(
        step.id,
        `failed after ${maxAttempts} attempt(s): ${ctx.validationMessage}`,
      );
    }

    currentId = step.next(ctx);
  }

  onStep({ state: startId, attempt: 0, phase: "done" });
  return ctx;
}
