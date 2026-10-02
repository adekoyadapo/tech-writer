---
name: blog-image
description: >
  Technical figure generation for blog and docs content using Claude Opus 5.5.
  Authors self-contained SVG stills or short SVG-frame GIFs, then renders locally
  with scripts/render_figure.py (PNG/WebP/GIF). No Gemini, nanobanana, or image
  API keys. Use for hero diagrams, inline architecture figures, process GIFs,
  and OG-style technical cards. Photoreal covers stay on Unsplash/Pixabay/Pexels.
  Use when user says blog image, generate figure, diagram, GIF, hero diagram,
  architecture figure, or illustration.
user-invokable: true
argument-hint: "[generate|gif|setup] [description]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
license: MIT
metadata:
  version: "2.0.0"
  engine: "claude-opus-5-5 + local SVG render"
---

# Blog Image — Opus 5.5 Figures (SVG / GIF)

Claude Opus 5.5 authors figures as SVG text. Local tooling turns them into
PNG, WebP, or GIF. This skill does **not** call Gemini or any image MCP.

## Commands

| Command | What it does |
|---------|--------------|
| `generate <idea>` | Still figure (SVG + optional PNG/WebP) |
| `gif <idea>` | Short looping GIF from SVG frames |
| `setup` | Explain optional rasterizer installs |

## When to use still vs GIF

| Need | Output |
|------|--------|
| Architecture, UI sketch, sequence, component map | still SVG (+ WebP/PNG) |
| Short process (4–12 steps), highlight flow | GIF |
| Photoreal cover / lifestyle photo | Unsplash/Pixabay/Pexels — do not use Opus |

## Workflow

1. Clarify use case: hero, inline, OG card, or process GIF.
2. Collect exact labels. For Elastic topics, labels must come from the
   `elastic-docs-researcher` claim bundle.
3. Spawn the `writer-image` agent (`model: claude-opus-5-5`). Do not override the model.
4. Agent writes SVG (or frame set) under the content project's asset path, e.g.
   `public/blog/<slug>/` or `.writer/figures/<slug>/`.
5. Run the renderer from the plugin root:

```bash
# Still
python3 <plugin-root>/scripts/render_figure.py still \
  --input path/to/figure.svg --out-dir path/to/out --format webp --width 1200

# GIF
python3 <plugin-root>/scripts/render_figure.py gif \
  --frames-dir path/to/frames --out-dir path/to/out --width 800 --duration-ms 400
```

6. Deliver SVG path, raster/GIF path (or SVG-only note), and alt text.

## Setup (optional rasterizers)

Opus always produces SVG. Raster/GIF extras:

```bash
brew install librsvg          # preferred: rsvg-convert
# or
brew install imagemagick
pip install pillow            # required for GIF assembly
pip install cairosvg          # optional Python fallback
```

If no rasterizer is present, return the SVG and name one install. Do not fail
the parent write workflow.

## Internal API (blog-write / blog-rewrite / writer)

**Input:** `image_type` (hero|inline|og|gif), `topic`, `section_context`, `labels`, `output_dir`  
**Output:** SVG path, optional raster/GIF path, alt text  

Graceful fallback: if render fails, keep SVG and continue the article.

## Alt text

- One descriptive sentence, 10–125 characters
- Topic keywords natural
- For GIFs: describe the process shown

## Anti-patterns

| Do not | Why |
|--------|-----|
| Call nanobanana / Gemini | Out of scope for this plugin |
| Invent Elastic UI chrome or field names | Breaks fact-check |
| Emit huge GIFs (>2MB) | Slow pages |
| Skip SVG source | SVG is the editable source of truth |
