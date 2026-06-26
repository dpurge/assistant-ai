# Workflow example

Slash command with parameters
State graph (not just a linear workflow)
Shared context object
Each state mutates the context
Validation after every state
Automatic retry until validation succeeds
Conditional branching
Final output either to the terminal or to a file

```ts
/**
 * workflow-example.ts
 *
 * A self-contained example of a graph-based workflow for a Pi coding agent.
 *
 * Concepts demonstrated:
 *
 * ✓ Slash command entry point
 * ✓ Shared context object
 * ✓ Graph of states
 * ✓ Validation after every state
 * ✓ Retry until validation succeeds
 * ✓ Branching
 * ✓ Markdown rendering
 * ✓ Optional file output
 *
 * Replace FakePi with the real Pi API later.
 */

import * as fs from "fs/promises";

/* ============================================================
 * Context
 * ============================================================
 */

interface WorkflowContext {
    command: string;
    args: string[];

    goal?: string;

    requirements?: string[];

    architecture?: {
        modules: string[];
    };

    implementationPlan?: string[];

    outputMode: "terminal" | "file";

    outputFile?: string;

    validationMessage?: string;
}

/* ============================================================
 * Validation
 * ============================================================
 */

type ValidationResult =
    | { ok: true }
    | { ok: false; message: string };

/* ============================================================
 * Pi interface
 * ============================================================
 */

interface Pi {

    ask<T>(prompt: string): Promise<T>;

    markdown(markdown: string): Promise<void>;

}

/* ============================================================
 * Fake Pi implementation
 *
 * Replace this class with the real Pi API.
 * ============================================================
 */

class FakePi implements Pi {

    async ask<T>(prompt: string): Promise<T> {

        console.log("\n==============================");
        console.log(prompt);
        console.log("==============================");

        if (prompt.includes("Extract requirements")) {

            return [
                "Users can log in",
                "Users can reset password",
                "Admins manage users"
            ] as T;

        }

        if (prompt.includes("Design architecture")) {

            return {
                modules: [
                    "API",
                    "Authentication",
                    "Database"
                ]
            } as T;

        }

        if (prompt.includes("Implementation plan")) {

            return [
                "Create API",
                "Create Auth",
                "Create DB"
            ] as T;

        }

        throw new Error("Unknown prompt");
    }

    async markdown(markdown: string) {

        console.log(markdown);

    }

}

/* ============================================================
 * State interface
 * ============================================================
 */

interface State {

    id: string;

    run(
        pi: Pi,
        ctx: WorkflowContext
    ): Promise<WorkflowContext>;

    validate(
        ctx: WorkflowContext
    ): Promise<ValidationResult>;

    next(
        ctx: WorkflowContext
    ): string | null;

}

/* ============================================================
 * States
 * ============================================================
 */

const GoalState: State = {

    id: "goal",

    async run(pi, ctx) {

        return {

            ...ctx,

            goal: ctx.args.join(" ")

        };

    },

    async validate(ctx) {

        if (!ctx.goal?.trim()) {

            return {
                ok: false,
                message: "Goal cannot be empty."
            };

        }

        return { ok: true };

    },

    next() {

        return "requirements";

    }

};

const RequirementsState: State = {

    id: "requirements",

    async run(pi, ctx) {

        const requirements =
            await pi.ask<string[]>(`

Extract requirements.

Goal:

${ctx.goal}

Validation feedback:

${ctx.validationMessage ?? "None"}

`);

        return {
            ...ctx,
            requirements
        };

    },

    async validate(ctx) {

        if (!ctx.requirements?.length) {

            return {

                ok: false,

                message:
                    "Need at least one requirement."

            };

        }

        return { ok: true };

    },

    next() {

        return "architecture";

    }

};

const ArchitectureState: State = {

    id: "architecture",

    async run(pi, ctx) {

        const architecture =
            await pi.ask<{ modules: string[] }>(`

Design architecture.

Requirements:

${ctx.requirements?.join("\n")}

`);

        return {

            ...ctx,

            architecture

        };

    },

    async validate(ctx) {

        if (
            !ctx.architecture ||
            ctx.architecture.modules.length < 2
        ) {

            return {

                ok: false,

                message:
                    "Need at least two modules."

            };

        }

        return { ok: true };

    },

    next(ctx) {

        if (
            ctx.architecture!.modules.includes("API")
        ) {

            return "implementation";

        }

        return "render";

    }

};

const ImplementationState: State = {

    id: "implementation",

    async run(pi, ctx) {

        const plan =
            await pi.ask<string[]>(`

Implementation plan.

Architecture:

${ctx.architecture?.modules.join(", ")}

`);

        return {

            ...ctx,

            implementationPlan: plan

        };

    },

    async validate(ctx) {

        if (!ctx.implementationPlan?.length) {

            return {

                ok: false,

                message:
                    "Implementation plan empty."

            };

        }

        return { ok: true };

    },

    next() {

        return "render";

    }

};

const RenderState: State = {

    id: "render",

    async run(pi, ctx) {

        const markdown = renderMarkdown(ctx);

        if (ctx.outputMode === "terminal") {

            await pi.markdown(markdown);

        } else {

            await fs.writeFile(

                ctx.outputFile ?? "plan.md",

                markdown

            );

            console.log(
                `Written to ${ctx.outputFile ?? "plan.md"}`
            );

        }

        return ctx;

    },

    async validate() {

        return { ok: true };

    },

    next() {

        return null;

    }

};

/* ============================================================
 * Graph
 * ============================================================
 */

const graph: Record<string, State> = {

    goal: GoalState,

    requirements: RequirementsState,

    architecture: ArchitectureState,

    implementation: ImplementationState,

    render: RenderState

};

/* ============================================================
 * Workflow engine
 * ============================================================
 */

async function executeWorkflow(

    pi: Pi,

    ctx: WorkflowContext

) {

    let current = "goal";

    while (current) {

        const state = graph[current];

        console.log(
            `\n--- STATE: ${state.id} ---`
        );

        while (true) {

            ctx = await state.run(pi, ctx);

            const validation =
                await state.validate(ctx);

            if (validation.ok) {

                break;

            }

            console.log(
                "Validation failed:",
                validation.message
            );

            ctx.validationMessage =
                validation.message;

        }

        current = state.next(ctx);

    }

}

/* ============================================================
 * Markdown renderer
 * ============================================================
 */

function renderMarkdown(
    ctx: WorkflowContext
) {

    return `# ${ctx.goal}

## Requirements

${ctx.requirements?.map(x => `- ${x}`).join("\n")}

## Architecture

${ctx.architecture?.modules
    .map(x => `- ${x}`)
    .join("\n")}

## Implementation

${ctx.implementationPlan
    ?.map(x => `- ${x}`)
    .join("\n")}
`;

}

/* ============================================================
 * Slash command simulation
 * ============================================================
 */

async function main() {

    const pi = new FakePi();

    const slashCommand = "/design";

    const args = [
        "Build",
        "an",
        "authentication",
        "system"
    ];

    const context: WorkflowContext = {

        command: slashCommand,

        args,

        outputMode: "terminal"

        // Change to:

        // outputMode: "file",
        // outputFile: "plan.md"

    };

    await executeWorkflow(
        pi,
        context
    );

}

main().catch(console.error);
```
