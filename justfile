# assistant-ai build/install/uninstall recipes.
# Requires `just` (https://github.com/casey/just) and `uv` (https://github.com/astral-sh/uv).

# Use cmd.exe on Windows so no sh/Git-Bash dependency is required.
set windows-shell := ["cmd", "/c"]

# Show available recipes
default:
    @just --list

# Build distributable zip files for all targets into dist/
build:
    uv run --script scripts/build.py

# Build the target's zip then unpack it into the install directory
# target: claude | opencode | pi
install target:
    uv run --script scripts/install.py {{target}}

# Remove the install directory for the named target
# target: claude | opencode | pi
uninstall target:
    uv run --script scripts/uninstall.py {{target}}

# Remove dist/
clean:
    uv run --script scripts/clean.py

# Run the pytest suite over the export tools and shared schema.
test:
    uv run --with pytest --with pydantic pytest tests/ -v

# Evaluate skill prompt quality against any OpenAI-compatible model.
# model: model name string, e.g. "gemma2:2b" or "claude-haiku-4-5-20251001"
# base-url: base URL for OpenAI-compat API (default: local Ollama)
# api-key: API key (any non-empty value works for local Ollama)
eval-skills model="gemma2:2b" base-url="http://localhost:11434/v1" api-key="ollama":
    uv run --script scripts/eval_skills.py --model {{model}} --base-url {{base-url}} --api-key {{api-key}}

# Bump the version in plugin.json (accepts `0.2.0` or `v0.2.0`).
# Prints the git commit/tag/push commands to follow.
bump-version new_version:
    uv run --script scripts/bump_version.py {{new_version}}
