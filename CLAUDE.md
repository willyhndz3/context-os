# GTM Context OS - Navigation Guide

**Purpose:** Centralized go-to-market intelligence that compounds over time.

---

## What Is This?

This is your **GTM Context Operating System** - a structured knowledge graph where:
- AI compounds intelligence over time
- Knowledge persists across sessions
- Concepts link to each other

**Philosophy:** Your GTM context is primary. System structures and compounds it.

---

## Directory Structure

```
gtm-context-os/
├── CLAUDE.md                   # <- YOU ARE HERE
├── _inbox/                     # Drop raw transcripts here for processing
├── _archive/                   # Processed transcripts (optional)
├── accounts/                   # All account-related content
│   ├── [Company Name]/
│   │   ├── account.md          # Main account file
│   │   ├── briefings/          # Call prep documents
│   │   │   └── YYYY-MM-DD-briefing.md
│   │   └── diagrams/           # Architecture diagrams
│   │       └── [workflow-name].md
│   └── _templates/
│       └── account_template.md
├── partners/                   # Vendor & technology partner relationships
│   ├── [Partner Name]/
│   │   └── partner.md          # Main partner file
│   └── _templates/
│       └── partner_template.md
├── knowledge_base/             # Cross-account concepts
│   ├── icp/                    # Ideal Customer Profiles
│   ├── messaging/              # Value props, taglines, narratives
│   ├── methodology/            # Frameworks and patterns
│   ├── positioning/            # Market position, differentiation
│   ├── competitive/            # Competitor intel, battlecards
│   └── objections/             # Common objections and responses
├── 00_foundation/              # Layer 2: Operational Docs
│   ├── strategy/               # GTM strategy documents
│   ├── messaging/              # Master messaging docs
│   └── _synthesis/             # Summary documents
└── _system/
    └── knowledge_graph/
        ├── taxonomy.yaml       # Blessed tags
        └── ontology.yaml       # Relationship rules
```

---

## How to Use This System

### Finding Information

1. **Start with synthesis docs** - Check `_synthesis/` folders first
2. **Then atomic concepts** - Read specific nodes in knowledge_base/
3. **Follow wiki-links** - [[concept-name]] links to related ideas

### Adding Information

**Option 1: From Clarify (fast, for most calls)**
"Process my call with [person] from [company] into the knowledge base"

Claude will query Clarify, pull the meeting summary, and extract insights.

**Option 2: From transcript file (deep, for key calls)**
1. Download transcript from Clarify
2. Drop it in `_inbox/` folder
3. "Process the transcript in inbox"

Claude will read the full transcript and extract richer detail including exact quotes.

**When to use each:**
- Routine calls → Clarify (summaries are good enough)
- Won deals, breakthrough insights, new objections → Full transcript

The system will:
- Extract concepts
- Create structured nodes
- Link to related concepts
- Move processed files to `_archive/` (optional)

### Common GTM Queries

- "What's our positioning against [competitor]?"
- "What are the top objections from [ICP segment]?"
- "Generate messaging for [use case]"
- "What proof points support [claim]?"
- "Show me all deals in [stage]"
- "What did we learn from [account]?"
- "Which accounts validated [concept]?"

---

## Quality Standards

**Every concept should have:**
- Structured frontmatter (tags, status, relationships)
- At least 3 links to related concepts
- Clear source attribution

**Evidence format:**
- [VERIFIED: source:line] - Direct evidence
- [INFERRED: logic] - Deduced from evidence
- [UNVERIFIABLE] - Cannot confirm

---

## GTM Concept Lifecycle

1. **Emergent** - Captured from transcript/doc, not yet validated
2. **Validated** - Confirmed in 1+ customer conversations
3. **Canonical** - Proven messaging, referenced 2+ times

---

**Created:** 2026-01-28
**Status:** Active
