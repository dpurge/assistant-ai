/**
 * pi-executor.ts — the real, model-backed StepExecutor.
 *
 * Builds a fresh, single-message Context per step (so no session history leaks
 * in), runs a bounded tool-execution loop (complete() returns tool calls but
 * does not execute them — we do), then parses + typebox-validates the final
 * reply against the step's outputSchema. Isolated here so the engine and the
 * Simulated executor stay import-clean and head-less-testable.
 *
 * NOTE: the exact pi-ai Message / tool-result shapes can't be type-checked
 * locally (the package isn't installed in this repo). Reviewed against the
 * documented API; adjust the toolResult construction if Pi's shape differs.
 */

import type { ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import type { StepExecutor, StepRequest, ToolSpec } from "./engine.ts";

const MAX_TOOL_TURNS = 4;

type Result = { ok: true; value: unknown } | { ok: false; message: string };

export class PiStepExecutor implements StepExecutor {
  constructor(private readonly ctx: ExtensionCommandContext) {}

  async run(req: StepRequest): Promise<Result> {
    const { complete, getModel } = await import("@earendil-works/pi-ai/compat");
    const { Value } = await import("typebox/value");

    const resolvedModel = (() => {
      if (req.model != null) {
        const slash = req.model.indexOf("/");
        return slash !== -1
          ? getModel(req.model.slice(0, slash), req.model.slice(slash + 1))
          : getModel("anthropic", req.model);
      }
      return this.ctx.model ?? getModel("anthropic", "claude-haiku-4-5-20251001");
    })();
    const model = resolvedModel;
    const auth = await this.ctx.modelRegistry.getApiKeyAndHeaders(model);
    const authOpts = { apiKey: auth.apiKey, headers: auth.headers, env: auth.env };
    const tools = (req.tools ?? []).map((t) => ({
      name: t.name,
      description: t.description,
      parameters: t.parameters,
    }));

    // Fresh context: ONLY this step's prompt — no history.
    const messages: any[] = [{ role: "user", content: [{ type: "text", text: req.prompt }] }];

    let finalText = "";
    for (let turn = 0; turn <= MAX_TOOL_TURNS; turn++) {
      const resp = await complete(
        model,
        {
          systemPrompt: req.system,
          messages,
          tools: tools.length ? tools : undefined,
          ...(req.effort != null ? { effort: req.effort } : {}),
        },
        authOpts,
      );

      const calls = (resp.content ?? []).filter((c: { type: string }) => c.type === "toolCall");
      if (calls.length === 0) {
        finalText = textOf(resp);
        break;
      }
      if (turn === MAX_TOOL_TURNS) {
        return { ok: false, message: `tool loop exceeded ${MAX_TOOL_TURNS} turns` };
      }

      messages.push(resp);
      for (const call of calls) {
        const spec = req.tools?.find((t) => t.name === call.name);
        const out = spec
          ? await safeExec(spec, call.arguments)
          : `error: unknown tool "${call.name}"`;
        messages.push({
          role: "toolResult",
          toolCallId: call.id,
          content: [{ type: "text", text: out }],
        });
      }
    }

    // Raw text result when the step declares no schema (e.g. a Markdown report).
    if (!req.outputSchema) return { ok: true, value: finalText };

    let parsed: unknown;
    try {
      parsed = JSON.parse(stripFences(finalText));
    } catch (e) {
      return { ok: false, message: `reply was not valid JSON: ${(e as Error).message}` };
    }
    if (!Value.Check(req.outputSchema as any, parsed)) {
      const errs = [...Value.Errors(req.outputSchema as any, parsed)]
        .slice(0, 5)
        .map((e: any) => `${e.path}: ${e.message}`)
        .join("; ");
      return { ok: false, message: `output did not match schema: ${errs}` };
    }
    return { ok: true, value: parsed };
  }
}

async function safeExec(spec: ToolSpec, args: unknown): Promise<string> {
  try {
    return await spec.execute(args);
  } catch (e) {
    return `error: ${(e as Error).message}`;
  }
}

function textOf(resp: { content?: Array<{ type: string; text?: string }> }): string {
  return (resp.content ?? [])
    .filter((c): c is { type: "text"; text: string } => c.type === "text" && typeof c.text === "string")
    .map((c) => c.text)
    .join("\n");
}

/** Tolerate models that wrap JSON in ```json fences despite instructions. */
export function stripFences(text: string): string {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  return (fenced ? fenced[1] : text).trim();
}
