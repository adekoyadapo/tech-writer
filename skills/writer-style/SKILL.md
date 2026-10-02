---
name: writer-style
description: >
  Build and update a writing style profile from the user's sample documents.
  Reads .writer/samples/, interviews for missing tone dimensions when needed,
  and writes .writer/style.json used by the writer and blog skills. Use when
  the user says writing style, voice, persona, tone, brand voice, or after
  they add samples during setup.
user-invokable: true
argument-hint: "[build|show|update] [optional-sample-path]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Writer Style — Samples to Style Profile

Turn the user's own writing into a reusable baseline for new drafts.

## Commands

| Command | Purpose |
|---------|---------|
| `build` | Analyze `.writer/samples/` and write `.writer/style.json` |
| `show` | Print the current `.writer/style.json` |
| `update` | Re-analyze samples and merge into the existing profile |

## Prerequisites

- `.writer/samples/` must contain at least one sample file, or the user must
  point at sample paths in the request.
- If samples are missing, stop and send them to `/technical-writer:writer setup`.

## Build Workflow

1. Glob `.writer/samples/**/*.{md,mdx,txt,html}`.
2. Read up to 5 representative samples (prefer recent / longest).
3. Derive:
   - Tone on the NNGroup 4 axes (funny–serious, formal–casual, respectful–irreverent, enthusiastic–matter-of-fact)
   - Average and max sentence length
   - Contraction frequency
   - Preferred summary-box label (Key Takeaways, TL;DR, etc.)
   - Banned openers and filler phrases observed as absent (or asked)
   - Domain vocabulary notes
4. Ask at most 2 clarifying questions if tone is ambiguous.
5. Write `.writer/style.json` using this shape (see also `assets/writer-starter/style.example.json`):

```json
{
  "name": "string",
  "role": "string",
  "tone": {
    "funny_to_serious": "string",
    "formal_to_casual": "string",
    "respectful_to_irreverent": "string",
    "enthusiastic_to_matter_of_fact": "string"
  },
  "voice_rules": ["string"],
  "banned_openers": ["string"],
  "readability": {
    "flesch_ease_target": "string",
    "avg_sentence_words": 18,
    "max_sentence_words": 25
  },
  "summary_box_label": "Key Takeaways",
  "source_samples": ["relative/paths"]
}
```

6. Confirm the path and a short voice summary to the user.

## Usage Rule for Downstream Skills

When `.writer/style.json` exists, `writer-draft` and blog write/rewrite must load it
and enforce `voice_rules` and `banned_openers`. Prefer it over any plugin-bundled persona.
