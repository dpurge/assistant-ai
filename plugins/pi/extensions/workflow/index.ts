/**
 * index.ts — the Pi adapter and single dispatcher.
 *
 * Registers ONE command, `/workflow`, that dispatches on its first argument to a
 * named workflow from the registry. This keeps the command surface small while
 * the registry holds arbitrarily many workflows.
 *
 *   /workflow                         list available workflows
 *   /workflow <name> <input…>         run a workflow
 *   /workflow design                run the offline, deterministic demo workflow
 *
 * All per-workflow logic (services, gates, output) lives in workflows/*.ts;
 * this file is pure routing + discoverability (name autocompletion).
 */

import type { ExtensionAPI, ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { REGISTRY, findWorkflow } from "./registry.ts";

function listText(): string {
  return ["Available workflows:", ...REGISTRY.map((w) => `  ${w.name} — ${w.description}`)].join("\n");
}

export default function (pi: ExtensionAPI) {
  pi.registerCommand("workflow", {
    description: "Run a named workflow (no name lists them): design | phraseforge-mdx | …",
    getArgumentCompletions: (prefix: string) =>
      REGISTRY.filter((w) => w.name.startsWith(prefix)).map((w) => ({
        value: w.name,
        label: w.name,
        description: w.description,
      })),
    handler: async (args: string, ctx: ExtensionCommandContext) => {
      const trimmed = args.trim();
      if (!trimmed) {
        ctx.ui.notify(listText(), "info");
        return;
      }

      const [name, ...restTokens] = trimmed.split(/\s+/);
      const def = findWorkflow(name);
      if (!def) {
        ctx.ui.notify(`Unknown workflow "${name}".\n${listText()}`, "warning");
        return;
      }

      await def.execute(restTokens.join(" "), ctx, pi);
    },
  });
}
