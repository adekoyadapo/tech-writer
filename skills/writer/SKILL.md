---
name: writer
description: >
  Universal technical writing front door for Claude Code. Routes write, rewrite,
  outline, brief, analyze, and audit requests across blog posts, how-tos, tutorials,
  runbooks, ADRs, release notes, and troubleshooting guides. Enforces a samples and
  templates setup gate before drafting (unless the user skips). Routes Elastic product
  topics through elastic-docs research and figures through Opus 5.5 SVG/GIF generation.
  Use when the user says write, draft, rewrite, outline, brief, analyze, technical
  writing, blog, docs, runbook, ADR, release notes, or documentation.
user-invokable: true
argument-hint: "[write|rewrite|outline|brief|analyze|audit|setup|skip-setup] [topic-or-file]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - Task
---

# Writer — Universal Writing Front Door

Route every writing request through this skill. Prefer this over calling blog
sub-skills directly so the samples gate, model routing, and Elastic research rules apply.

## Commands

| Command | Action |
|---------|--------|
| `/technical-writer:writer write <topic>` | Draft new content |
| `/technical-writer:writer rewrite <file>` | Rewrite or refresh existing content |
| `/technical-writer:writer outline <topic>` | Outline only |
| `/technical-writer:writer brief <topic>` | Content brief |
| `/technical-writer:writer analyze <file>` | Quality score |
| `/technical-writer:writer audit [dir]` | Batch health check |
| `/technical-writer:writer setup` | Create `.writer/` from starter assets |
| `/technical-writer:writer skip-setup` | Proceed without samples for this session |

Bare `/technical-writer:writer` without a subcommand: ask which action they need.

## Setup Gate (required before write or rewrite)

Before drafting, check the **content project** (cwd / repo root):

1. `.writer/samples/` — at least one prior writing sample (`.md`, `.mdx`, `.txt`, `.html`)
2. `.writer/templates/` — at least one structure template the user wants followed
3. `.writer/style.json` — optional but preferred; create via `writer-style` after samples exist

### If samples or templates are missing

Stop. Do not draft yet. Tell the user:

1. Copy starter assets: run `/technical-writer:writer setup`, or manually copy from this plugin's `assets/writer-starter/` into the project's `.writer/`.
2. Add 1–3 of their own posts/docs into `.writer/samples/`.
3. Adjust or replace templates in `.writer/templates/`.
4. Optionally run `/technical-writer:writer-style` to build `.writer/style.json`.

Then ask whether to proceed with setup, or to **skip** for this session.

### Skip

Only continue without samples when the user explicitly says skip, `skip-setup`,
or equivalent. After skip, use stock templates from `assets/writer-starter/templates/`
and the plugin blog templates. Never silently substitute stock voice for the user's.

### Setup command

When the user runs setup:

```bash
mkdir -p .writer/samples .writer/templates
# Copy from the plugin's assets/writer-starter/ (locate via this skill's plugin root)
cp -R <plugin-root>/assets/writer-starter/templates/* .writer/templates/
cp <plugin-root>/assets/writer-starter/style.example.json .writer/style.example.json
```

Leave `.writer/samples/` empty for the user to fill. Remind them to add samples.

## Form Detection

Pick a form from topic + context:

| Signals | Form | Delegation |
|---------|------|------------|
| blog, post, SEO, GEO, listicle, pillar | blog | `blog-write` / `blog-rewrite` / related blog skills |
| how-to, tutorial, walkthrough | how-to / tutorial | blog templates `how-to-guide` / `tutorial`, or `.writer/templates/` |
| runbook, playbook, on-call | runbook | `.writer/templates/runbook.md` |
| ADR, architecture decision | adr | `.writer/templates/adr.md` |
| troubleshooting, debug, incident | troubleshooting | `.writer/templates/troubleshooting.md` |
| release notes, changelog | release-notes | short structured bullets; skip SEO unless asked |
| reference, API, config | reference | technical sections; skip SEO unless asked |

For **blog** forms: load and follow the matching `skills/blog-*` skill after the gate passes.
For **non-blog** forms: use the same agents below with the chosen template; skip SEO/GEO
unless the user asks.

## Agent and Model Routing

Spawn Task agents. Do **not** override the agent's frontmatter `model`.

| Stage | Agent file | Model | When |
|-------|------------|-------|------|
| Elastic research | `elastic-docs-researcher` | sonnet | Any Elasticsearch, Kibana, Fleet, APM, Logstash, Beats, Security, Observability, Cloud, Agent topic |
| General research | `writer-research` | haiku | Non-Elastic topics |
| Draft | `writer-draft` | sonnet | After research / outline |
| Figures | `writer-image` | `claude-opus-5-5` | Diagrams, stills, GIFs (not photoreal covers) |
| SEO check | `writer-seo` | haiku | Blog / SEO requested |
| Fact-check | `writer-factcheck` | haiku | After draft |
| Quality score | `writer-review` | sonnet | Before deliver |
| Publish review | `writer-final` | `claude-opus-5-5` | Only if user asks |

### Elastic rule

If the topic touches Elastic products, spawn `elastic-docs-researcher` **before** draft.
Pass its claim bundle into the draft agent. Do not invent Elastic defaults from training data.

### Figure rule

For technical diagrams and short motion explainers, spawn `writer-image` (Opus 5.5).
Photographic covers: use Unsplash/Pixabay/Pexels stock URLs from visual-media guidance.
Never call Gemini/nanobanana from this plugin.

## Standard Write Flow

1. **Gate** — samples/templates present or skip confirmed
2. **Style** — load `.writer/style.json` if present
3. **Parse** — form, platform (md/mdx/html), template
4. **Research** — Elastic agent or writer-research
5. **Outline** — from template + research gaps
6. **Draft** — writer-draft
7. **Figures** — writer-image when diagrams/GIFs needed
8. **Checks** — factcheck; SEO if blog
9. **Review** — writer-review scorecard
10. **Deliver** — file path, scorecard, open fixes

## Blog Sub-Skill Map

When form is blog, after the gate, route to:

- write → `blog-write`
- rewrite / update → `blog-rewrite`
- analyze → `blog-analyze`
- brief → `blog-brief`
- calendar → `blog-calendar`
- strategy → `blog-strategy`
- outline → `blog-outline`
- seo-check → `blog-seo-check`
- schema → `blog-schema`
- repurpose → `blog-repurpose`
- geo → `blog-geo`
- audit → `blog-audit`
- cannibalization → `blog-cannibalization`
- factcheck → `blog-factcheck`
- persona → `blog-persona` (prefer `.writer/style.json` via writer-style)
- taxonomy → `blog-taxonomy`
- image / figure → `blog-image` (Opus 5.5 SVG/GIF path)

Keep using relative references under `../blog/references/` from those skills.
