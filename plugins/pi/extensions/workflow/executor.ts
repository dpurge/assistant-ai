/**
 * executor.ts — the deterministic, offline StepExecutor.
 *
 * PURE (no Pi/LLM imports). Returns canned values keyed by markers in the
 * request prompt, so workflows run and can be verified with no API key. It
 * ignores tools and skills — the real, model-backed executor (pi-executor.ts)
 * handles those. Add a case when a new model step needs an offline answer.
 */

import type { StepExecutor, StepRequest } from "./engine.ts";

type Result = { ok: true; value: unknown } | { ok: false; message: string };

export class SimulatedExecutor implements StepExecutor {
  async run(req: StepRequest): Promise<Result> {
    const p = req.prompt;

    // design workflow
    if (p.includes("Extract requirements")) {
      return { ok: true, value: ["Users can log in", "Users can reset password", "Admins manage users"] };
    }
    if (p.includes("Design architecture")) {
      return { ok: true, value: { modules: ["API", "Authentication", "Database"] } };
    }
    if (p.includes("Implementation plan")) {
      return { ok: true, value: ["Create API", "Create Auth", "Create DB"] };
    }

    return { ok: false, message: `SimulatedExecutor has no canned answer for: ${p.slice(0, 60)}…` };
  }
}
