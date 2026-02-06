---
name: COMPETITOR_CUSTOMER_TARGETING
description: Use case for identifying and targeting competitor customers
domain: messaging
node_type: concept
status: emergent
last_updated: 2026-01-28
tags:
  - messaging
  - value-prop
  - use-case
topics:
  - competitive-displacement
  - prospecting
  - outbound
related_concepts:
  - "[[enterprise-developer-tools]]"
  - "[[clay-workflow-service]]"
  - "[[deep-research-agents]]"
---

# Competitor Customer Targeting

A use case where you help clients identify companies using competitor products and build targeted outreach to displace them.

## What It Is

Using data enrichment and research to:
1. Identify companies using a competitor's product
2. Find the right contacts at those companies
3. Build messaging that speaks to switching triggers
4. Execute targeted outreach

## How It Works in Clay

```
Competitor signal sources:
- Technographics (BuiltWith, Wappalyzer, HG Insights)
- Job postings mentioning competitor tools
- LinkedIn profiles with competitor skills
- GitHub repos using competitor SDKs
- G2/Capterra reviews

→ Enrich with contact data
→ Score by switching likelihood
→ Personalize messaging to pain points
→ Push to outbound sequence
```

## Messaging Angles

For competitor displacement, focus on:
- What's broken with the current solution
- Migration path (easy vs hard)
- Proof from similar switchers
- Timing triggers (contract renewal, new leadership)

## Evidence

> "Wso2 will consider leveraging Clay for advanced data enrichment, outbound automation, and intent-based prospecting, especially to target competitors' customers"
> [VERIFIED: WSO2 call, Jan 2026]

## Who Buys This

- Companies in competitive markets with clear alternatives
- Enterprise software with switching costs (need to justify the effort)
- Sales teams struggling to break into accounts

## How It Relates

- [[enterprise-developer-tools]] - ICP that specifically asked for this
- [[clay-workflow-service]] - How we deliver it
- [[deep-research-agents]] - Can layer in for account-level intel

---

**Status:** Emergent - WSO2 expressed interest, not yet delivered
**Next:** Build POC for WSO2 if they engage, then templatize
