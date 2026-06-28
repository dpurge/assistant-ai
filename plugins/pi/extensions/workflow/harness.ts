/**
 * harness.ts — shared Pi rendering glue.
 *
 * Wraps runWorkflow with a standard progress renderer (ctx.ui) and uniform
 * WorkflowError handling, so each workflow's execute() stays focused on its
 * steps, services, and output rather than repeating UI plumbing.
 */

import type { ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import {
  type RetryableContext,
  type Runtime,
  type WorkflowStep,
  WorkflowError,
  runWorkflow,
} from "./engine.ts";

/** Run a graph with standard ctx.ui progress + error reporting. Returns null on failure. */
export async function runWithUi<Ctx extends RetryableContext>(
  ctx: ExtensionCommandContext,
  graph: Record<string, WorkflowStep<Ctx>>,
  startId: string,
  wfctx: Ctx,
  runtime: Runtime<Ctx>,
  opts: { maxAttempts?: number } = {},
): Promise<Ctx | null> {
  try {
    return await runWorkflow(graph, startId, wfctx, runtime, {
      maxAttempts: opts.maxAttempts,
      onStep: (e) => {
        if (e.phase === "run") ctx.ui.setStatus("workflow", `▶ ${e.state} (try ${e.attempt})`);
        else if (e.phase === "retry") ctx.ui.notify(`↻ ${e.state}: ${e.message}`, "warning");
        else if (e.phase === "done") ctx.ui.setStatus("workflow", undefined);
      },
    });
  } catch (err) {
    ctx.ui.setStatus("workflow", undefined);
    const msg = err instanceof WorkflowError ? `[${err.state}] ${err.message}` : String(err);
    ctx.ui.notify(`Workflow failed: ${msg}`, "error");
    return null;
  }
}
