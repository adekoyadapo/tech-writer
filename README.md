# Technical Writer

A **Claude Code** plugin for drafting blogs and other technical writing forms with:

- A **samples-first gate** (your voice and templates before drafting)
- **Model-routed agents** (Haiku / Sonnet / pinned Opus 5.5)
- Ported **blog** skills (write, rewrite, SEO, GEO, schema, …)
- **Elastic docs MCP** research for Elastic-focused posts
- **Opus 5.5 figures** as SVG stills or short GIFs (no Gemini API key)

Skill commands are namespaced: `/technical-writer:<skill>`.

## Requirements

- [Claude Code](https://code.claude.com/docs) (current)
- Python 3.11+ (quality scoring script; figure helper)
- Optional for raster/GIF: `librsvg` or ImageMagick, and `pip install pillow`
- Network access for the public Elastic docs MCP (`https://www.elastic.co/docs/_mcp/`)

## Install

Clone this repository, then choose a scope.

### Global (all your projects)

```bash
git clone https://github.com/adekoyadapo/tech-writer.git
cd tech-writer
./scripts/install.sh --global
```

This symlinks the plugin to `~/.claude/skills/technical-writer`. Claude Code auto-loads plugins that live under your personal skills directory.

### Project (one content repo)

```bash
cd /path/to/your-content-repo
/path/to/technical-writer/scripts/install.sh --project --path .
```

This creates `.claude/skills/technical-writer` → the plugin. Start Claude Code from that repo root, then accept workspace trust if prompted.

### Try without installing

```bash
claude --plugin-dir /path/to/technical-writer
```

Restart Claude Code or run `/reload-plugins` after install.

### Older `/blog` skills

If you already have `blog*` skills in `~/.claude/skills`, they keep answering `/blog` until you remove or rename them. This plugin’s commands are under `/technical-writer:…` and do not delete the old copies.

## First-run setup (do this before writing)

In the **content project** where you will write:

```text
/technical-writer:writer setup
```

That creates:

```text
.writer/
  samples/      ← put 1–3 of your past posts or docs here
  templates/    ← starter structures (edit freely)
  style.example.json
```

Then:

1. Copy your own writing into `.writer/samples/`.
2. Adjust `.writer/templates/` to match how you structure docs.
3. Build a style profile:

```text
/technical-writer:writer-style build
```

This writes `.writer/style.json`, which drafts must follow.

### Skip setup

You can say **skip** / run `/technical-writer:writer skip-setup` for a single session. Stock templates are used as a fallback. Skipping is explicit — the skill should not silently invent your voice.

## Everyday usage

| Goal | Command |
|------|---------|
| Write | `/technical-writer:writer write <topic>` |
| Rewrite | `/technical-writer:writer rewrite <file>` |
| Outline / brief | `/technical-writer:writer outline\|brief <topic>` |
| Score a draft | `/technical-writer:writer analyze <file>` |
| Blog-specific SEO/GEO/schema | `/technical-writer:blog-seo-check`, `blog-geo`, `blog-schema`, … |
| Elastic research | `/technical-writer:elastic-docs <topic>` |
| Figure / GIF | `/technical-writer:blog-image generate\|gif <idea>` |
| Style from samples | `/technical-writer:writer-style build` |

### Forms covered

Blog posts, how-tos, tutorials, runbooks, ADRs, troubleshooting guides, release notes, and reference-style write-ups. Blog forms reuse the full blog skill suite; other forms use the same agents with technical templates and skip SEO/GEO unless you ask.

### Elastic topics

Anything about Elasticsearch, Kibana, Fleet, APM, Logstash, Beats, Elastic Security, Observability, Cloud, or Agent must run through **elastic-docs** research first. Claims keep doc URL, version, and a verbatim quote. The plugin registers:

```json
{
  "mcpServers": {
    "elastic-docs": {
      "type": "http",
      "url": "https://www.elastic.co/docs/_mcp/"
    }
  }
}
```

### Figures (Opus 5.5)

`writer-image` is pinned to **`claude-opus-5-5`**. Opus writes SVG (or SVG frames). `scripts/render_figure.py` produces PNG/WebP or GIF when a local rasterizer is available:

```bash
brew install librsvg    # or imagemagick
pip install pillow      # GIF assembly
```

Photoreal covers still use Unsplash / Pixabay / Pexels. This plugin does not call Gemini.

## Agent model map

| Agent | Model | Role |
|-------|-------|------|
| `writer-research` | haiku | Non-Elastic research |
| `writer-seo` | haiku | On-page SEO checklist |
| `writer-factcheck` | haiku | Claim verification |
| `writer-draft` | sonnet | Drafting |
| `writer-review` | sonnet | 100-point quality score |
| `elastic-docs-researcher` | sonnet | Elastic.co docs research |
| `writer-image` | `claude-opus-5-5` | SVG / GIF figures |
| `writer-final` | `claude-opus-5-5` | Optional publish review |

Bump the Opus model ID in agent frontmatter when Anthropic ships the next Opus.

## Layout

```text
.claude-plugin/plugin.json
.mcp.json
CLAUDE.md
skills/           # writer, writer-style, elastic-docs, blog*
agents/           # model-pinned subagents
assets/writer-starter/
scripts/install.sh
scripts/render_figure.py
```

## License

MIT. Blog skill suite portions derive from AgriciDaniel’s MIT-licensed blog engine; see `LICENSE`.
