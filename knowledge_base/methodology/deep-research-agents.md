---
name: DEEP_RESEARCH_AGENTS
description: AI-powered research workflows for account intelligence
domain: methodology
node_type: pattern
status: validated
last_updated: 2026-01-28
tags:
  - methodology
  - pattern
  - ai-research
topics:
  - account-intelligence
  - personalization
  - automation
related_concepts:
  - "[[clay-workflow-service]]"
  - "[[three-pillars-gtm-engineering]]"
---

# Deep Research Agents

Automated AI workflows that generate account-level intelligence for highly personalized outreach. A differentiating capability for enterprise and complex sales motions.

## What It Does

Uses AI (Claude, GPT, Perplexity) within Clay to:
- Analyze annual reports and financial filings
- Extract regulatory and compliance insights
- Generate consultant-style research briefs
- Surface account-specific talking points

## Use Case: eSmart Systems / Texas Utilities

Built deep research agents to analyze Texas electric cooperative annual reports:

**Inputs:**
- Company name and domain
- Annual report PDFs or URLs
- Target persona (CEO, CFO, Operations)

**Outputs:**
- Financial analysis (revenue trends, capital investments)
- Regulatory context (ERCOT, legislation)
- Consultant-style recommendations
- Persona-tailored email drafts

## Architecture

```
Account List → Perplexity Research → Financial Analysis →
Persona Segmentation → Email Agent → Apollo/HubSpot
```

## Key Design Decisions

1. **Recency filter** - Only cite reports within 24 months
2. **Citation required** - Every claim needs source reference
3. **Persona variation** - Different angles for CEO vs CFO vs Ops
4. **Tone calibration** - Less robotic, more consultant-style

## Evidence

> "Email agents will be updated to reference specific sections of consultant reports (e.g., KPMG) and surface actionable, utility-specific findings for each persona."
> [VERIFIED: eSmart Systems meeting 2026-01-26]

> "The workflow will focus on 18 vetted Texas utility accounts, with enrichment and deep research agents generating financial, regulatory, and consultant-style insights."
> [VERIFIED: eSmart Systems meeting 2026-01-26]

## When to Use

- **Enterprise accounts** with public financials
- **Long sales cycles** requiring differentiated outreach
- **Complex buying committees** needing persona-specific messaging
- **Regulated industries** (utilities, healthcare, finance)

## How It Relates

- [[clay-workflow-service]] - Advanced capability within core service
- [[persona-segmented-messaging]] - Feeds into personalization
- [[three-pillars-methodology]] - Spans Building and Executing pillars

---

**Status:** Validated - Proven with eSmart Systems engagement
**Next:** Templatize for other verticals (healthcare, finance)
