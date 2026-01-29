# Context OS Navigation Guide

This is the AI navigation guide for the Context OS knowledge base.

## Structure

```
context-os/
├── CLAUDE.md           # You are here
├── knowledge_base/     # Atomic knowledge nodes
│   ├── gtm/            # Go-to-market knowledge
│   ├── product/        # Product knowledge
│   └── research/       # Research and insights
├── _inbox/             # Unprocessed content (needs triage)
├── exports/            # External data exports
├── taxonomy.yaml       # Blessed tags
└── ontology.yaml       # Relationship rules
```

## How to Navigate

### Finding Information

1. **Search by topic** - Look in the appropriate subdirectory
2. **Search by tag** - Check frontmatter for matching tags
3. **Follow links** - Knowledge nodes link to related concepts

### Knowledge Base Conventions

Each node in `knowledge_base/` follows this format:

```yaml
---
title: Node Title
tags: [tag1, tag2]
created: 2025-01-29
updated: 2025-01-29
related: [[other-node]]
---

# Content

The actual knowledge content in markdown.
```

### Taxonomy

Use tags from `taxonomy.yaml`. Common tags:
- `discovery` - Customer discovery insights
- `objection` - Objection handling
- `competitor` - Competitive intelligence
- `pricing` - Pricing strategies
- `technical` - Technical details
- `process` - Internal processes

### Relationships

See `ontology.yaml` for how concepts connect:
- `addresses` - Solution addresses problem
- `competes_with` - Competitive relationship
- `requires` - Dependency relationship
- `supports` - Supporting evidence

## For AI Assistants

When answering questions:

1. **Search first** - Look for existing knowledge before generating
2. **Cite sources** - Reference the specific file path
3. **Use taxonomy** - Tag new content with blessed tags
4. **Link concepts** - Connect related knowledge nodes
5. **Inbox unprocessed** - Put uncertain content in `_inbox/`

## Quick Lookups

| Question Type | Where to Look |
|--------------|---------------|
| Pricing | `knowledge_base/gtm/pricing/` |
| Objections | `knowledge_base/gtm/objections/` |
| Product features | `knowledge_base/product/` |
| Competitor info | `knowledge_base/gtm/competitors/` |
| Meeting insights | `_inbox/` or `knowledge_base/research/` |
