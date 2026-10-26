# Creating and Maintaining Instructions

- Keep source instructions platform-agnostic Markdown in `./instructions/`; use a verb-first, hyphen-separated filename ending in `.agent.md`.
- Keep each instruction focused on one workflow; use concise, actionable bullets and split unrelated concerns into separate files.
- Add every available instruction to `./instructions/main.agent.md` with a relative link, one-line purpose, and useful trigger keywords; add a target glob when the instruction is file-specific.
- Read existing instructions and entry points before editing; preserve useful content and fix stale catalog links rather than leaving references to missing files.
- Treat `./instructions/main.agent.md` as the routing catalog, not as a substitute for loading the relevant instruction in full.
- Keep platform-specific setup in thin wrappers that point to the canonical instruction instead of duplicating its content.
- For VS Code with GitHub Copilot, use `.github/copilot-instructions.md` as the workspace entry point, place slash-command wrappers in `.github/prompts/`, and enable instruction-file support in `.vscode/settings.json`.
- Avoid enabling unrelated broad tool access or adding workspace settings that are not needed for instruction discovery.
- When installing instruction infrastructure, verify that every catalog link resolves, wrappers reference existing files, and required frontmatter or JSON parses correctly.
- Use instruction files for prose workflows; use a skill when the workflow requires reusable scripts, references, or other bundled assets.
- Consult the source workflow when changing this setup: [Creating Instructions](https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/creating-instructions.agent.md).
