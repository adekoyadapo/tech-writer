# Technical Writer plugin (Claude Code)

This repository is a Claude Code plugin. Prefer the `/technical-writer:*` skills.

## Before any write

1. Check for `.writer/samples/` and `.writer/templates/` in the content project.
2. If missing, run `/technical-writer:writer setup` and ask the user to add samples —
   unless they explicitly skip setup.
3. Load `.writer/style.json` when present.

## Routing

- Elastic product topics → `elastic-docs` / agent `elastic-docs-researcher` (sonnet) before drafting.
- Figures → `blog-image` / agent `writer-image` with model `claude-opus-5-5` (SVG → local render).
- Do not call Gemini/nanobanana from this plugin.
- Do not override agent `model` frontmatter when spawning Task agents.

## Model map

| Agent | Model |
|-------|-------|
| writer-research, writer-seo, writer-factcheck | haiku |
| writer-draft, writer-review, elastic-docs-researcher | sonnet |
| writer-image, writer-final | claude-opus-5-5 |

## MCP

Plugin `.mcp.json` registers public `elastic-docs` at `https://www.elastic.co/docs/_mcp/`.
