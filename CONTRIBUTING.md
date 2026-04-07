# Contributing to the Settings Vault

Thank you for considering contributing to this personal macOS setup guide! This vault is a personal reference for setting up a new Mac from scratch.

## How to Contribute

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the existing conventions
3. **Ensure your changes follow the formatting rules** in [AGENTS.md](AGENTS.md)
4. **Submit a pull request** with a clear description of your changes

## Conventions to Follow

### Documentation Style
- Be concise. One sentence descriptions are preferred over paragraphs.
- Commands should be copy-pasteable as-is.
- Do not add excessive commentary or caveats.
- Target: **macOS on Apple Silicon** (M-series). Note Intel differences only when significant.

### File Structure
- Folders are strictly numbered (00 - Setup, 01 - Terminal, etc.)
- Always place new files in the most appropriate existing folder
- Do not create new top-level folders without being asked

### Page Types
Refer to [AGENTS.md](AGENTS.md) for the two distinct page layouts:
1. **Single-tool page** (for pages focused on one tool or category)
2. **Multi-tool listing page** (for pages that catalogue multiple related tools)

### Formatting Rules
- Every tool entry must include: installation command, basic configuration step, and startup/usage command
- Use YAML frontmatter with appropriate tags
- Use Obsidian wikilinks: `[[Page Name]]` when referencing other pages
- Use GitHub avatar URLs for icons: `<img src="https://github.com/<org>.png" width="24" style="vertical-align: middle; border-radius: 4px;" />`

### Code Blocks
- Use ```shell for all terminal commands
- Add # comments above non-obvious commands
- Prefer real, runnable commands over pseudocode

## Getting Help

If you have questions about contributing, please refer to the existing files in the repository for examples of the expected format and style.

Thank you for your contribution!