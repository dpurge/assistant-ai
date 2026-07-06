import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const PROMPT = String.raw`Say "Hello" in following languages:

- Arabic
- Chinese
- Greek
- Polish

Do not use web search, respond from your own knowledge.
`;

export default function (pi: ExtensionAPI) {
  pi.registerCommand("example", {
    description: "Test whether I can define a command",
    handler: async (args: any, ctx: any) => {
        // await ctx.waitForIdle();
        // pi.sendUserMessage(PROMPT);
    
       const prompt = args?.trim()
        ? `${PROMPT}\n\nAdditional instructions from the user:\n${args.trim()}`
        : PROMPT;
      
        if (ctx.isIdle()) {
            pi.sendUserMessage(prompt);
        } else {
            pi.sendUserMessage(prompt, { deliverAs: "followUp" });
            ctx.ui.notify("Queued /example as a follow-up", "info");
        }
    },
  });
}
