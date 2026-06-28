/**
 * shell.ts — the TS↔Python bridge + skill loader.
 *
 * Content workflows reuse the repo's Python export tools (lesson_schema +
 * exporters) as their validate/render backend instead of reimplementing them.
 * `runTool` invokes one via `uv run --script`, feeding JSON on stdin and
 * capturing stdout/stderr + exit code (a non-zero exit becomes a failed gate).
 * `loadSkill` reads a skill's SKILL.md for per-step injection.
 *
 * Paths resolve relative to the Pi agent base. After `just install pi` both this
 * extension and the skills live under ~/.pi/agent/, so a tool ships at
 * ~/.pi/agent/skills/<skill>/tools/<tool>.py and this file sits at
 * ~/.pi/agent/extensions/workflow/shell.ts — i.e. two levels up.
 */

import { spawn } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

import type { ShellRunner } from "./engine.ts";

export interface ShellResult {
  code: number;
  stdout: string;
  stderr: string;
}

/** Pi agent base dir: ASSISTANT_PI_DIR override, else two levels up from this file. */
function agentBase(): string {
  const override = process.env.ASSISTANT_PI_DIR;
  if (override) return resolve(override);
  const here = dirname(fileURLToPath(import.meta.url)); // …/extensions/workflow
  return resolve(here, "..", "..");
}

/** Default runner: `uv run --script <agentBase>/<toolRelPath> <args…>`. */
export const shell: ShellRunner = {
  runTool(toolRelPath, args, opts = {}) {
    const toolPath = join(agentBase(), toolRelPath);
    return new Promise<ShellResult>((resolvePromise, rejectPromise) => {
      const child = spawn("uv", ["run", "--script", toolPath, ...args], {
        stdio: ["pipe", "pipe", "pipe"],
      });
      let stdout = "";
      let stderr = "";
      child.stdout.on("data", (d) => (stdout += d));
      child.stderr.on("data", (d) => (stderr += d));
      child.on("error", rejectPromise); // e.g. uv not installed
      child.on("close", (code) => resolvePromise({ code: code ?? -1, stdout, stderr }));
      child.stdin.end(opts.stdin ?? "");
    });
  },
};

/** Read a skill's SKILL.md text for per-step injection; "" if not found. */
export async function loadSkill(name: string): Promise<string> {
  try {
    return await readFile(join(agentBase(), "skills", name, "SKILL.md"), "utf8");
  } catch {
    return "";
  }
}
