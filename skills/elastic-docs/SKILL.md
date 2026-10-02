---
name: elastic-docs
description: >
  Research Elastic product topics using the elastic-docs MCP (elastic.co/docs).
  Returns claim bundles with verbatim quotes, doc URLs, and version context for
  Elasticsearch, Kibana, Fleet, APM, Logstash, Beats, Elastic Security,
  Observability, Cloud, and Agent. Use before drafting any Elastic-focused
  write-up, and whenever verifying Elastic defaults, APIs, or field names.
user-invokable: true
argument-hint: "[topic]"
allowed-tools:
  - Read
  - WebFetch
  - Task
  - mcp__elastic-docs__search_docs
  - mcp__elastic-docs__get_document_by_url
  - mcp__elastic-docs__find_related_docs
  - mcp__elastic-docs__find_docs_inconsistencies
  - mcp__elastic-docs__analyze_document_structure
  - mcp__elastic-docs__check_docs_coherence
---

# Elastic Docs — Authoritative Product Research

Use this skill whenever the writing topic touches Elastic products. Training data
for Elasticsearch configs and defaults is often stale. Official docs win.

## MCP requirement

This plugin ships `.mcp.json` with:

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

If MCP tools are unavailable, stop research and tell the user to enable the
plugin MCP (restart Claude Code after install, or confirm `elastic-docs` appears
in connected MCP servers). Do not invent Elastic field defaults.

## Workflow

1. Spawn the `elastic-docs-researcher` agent (`model: sonnet`) **or** call MCP tools directly for a small lookup.
2. Search with `search_docs`, expand with `find_related_docs`, pull pages with `get_document_by_url`.
3. Return a claim bundle:

```markdown
## Claim Bundle: [Topic]

### Key Facts
| Fact | Verbatim Quote / Value | Doc URL | Version |
|------|------------------------|---------|---------|
| | | | |

### Verified API / Config Defaults
| Field / Parameter | Default | Doc URL |
|-------------------|---------|---------|

### Version-Specific Flags
- 

### Adjacent Docs
- 

### Not Found in Docs
- 
```

4. Hand the bundle to `writer-draft` / `blog-write`. Figures that show Elastic
   labels must use only strings from this bundle.

## Rules

- Never invent defaults.
- Prefer version-accurate URLs on elastic.co/docs.
- Flag preview vs GA and cross-version conflicts.
- No editorializing — facts and quotes only.
