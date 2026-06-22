# assistant-ai build/install/uninstall recipes.
# Requires `just` (https://github.com/casey/just) and `uv` (https://github.com/astral-sh/uv).

# Show available recipes
default:
    @just --list

# Build distributable zip files for all targets into dist/
build:
    uv run scripts/build.py

# Build the target's zip then unpack it into the install directory
# target: claude | opencode | pi
install target:
    uv run scripts/install.py {{target}}

# Remove the install directory for the named target
# target: claude | opencode | pi
uninstall target:
    uv run scripts/uninstall.py {{target}}

# Remove dist/
clean:
    uv run scripts/clean.py

# Run the pytest suite over the export tools and shared schema.
test:
    uv run --with pytest pytest tests/ -v

# Bump the version in plugin.json (accepts `0.2.0` or `v0.2.0`).
# Prints the git commit/tag/push commands to follow.
bump-version new_version:
    uv run scripts/bump_version.py {{new_version}}
