# eSmart Systems GTM Playbook

**Purpose:** Enable Matt and the eSmart team to operate and scale the Texas utilities workflow independently.

**Audience:** Matt Rilling Smith, Josh Allison, eSmart sales team

**Created:** January 30, 2026

---

## 1. Overview

### What We Built Together

An end-to-end outbound automation system for targeting Texas electric cooperatives. The system uses AI-powered deep research agents to generate consultant-quality intelligence and persona-tailored messaging at scale.

**The Core Innovation:**
Instead of generic outbound, we built a workflow that:
- Researches each utility like a consultant would (financials, regulations, risks)
- Generates KPMG-style reports with citations
- Tailors messaging by persona (CEO gets different content than Operations)
- Maintains quality at scale (not spray-and-pray)

### The End Result

| What You Get | Details |
|--------------|---------|
| Target Accounts | 18 vetted Texas utilities |
| Enriched Contacts | 221 contacts mapped to personas |
| Deep Research | Financial analysis, regulatory context, risk assessments per account |
| Personalized Emails | Tailored by persona, referencing specific findings |
| Execution Platform | Apollo sequences with HubSpot reporting |

### Why This Approach Works

Traditional outbound: "Hi, we help utilities with infrastructure inspection..."

Our approach: "Based on your 2025 annual report showing $2.3M in vegetation management costs and your exposure to HB 144 compliance requirements, here's how Grid Vision addresses your specific situation..."

The difference: **Specificity creates credibility.**

---

## 2. The Texas Workflow - Step by Step

### Tech Stack

| Tool | Purpose |
|------|---------|
| **Make.com** | Automation orchestration |
| **Apollo** | List building, contact enrichment, email generation (AI columns), sequencing |
| **Perplexity** | Deep research (2 agents) |
| **ChatGPT** | Summarization, KPMG consultant analysis |
| **Google Docs** | Research output storage |
| **HubSpot** | CRM, activity tracking, reporting |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAKE.COM SCENARIO                           │
│            "eSmart Deep Account Research"                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [Apollo: Search accounts by list ID]                          │
│         │                                                       │
│         ▼                                                       │
│   [Iterator] ─── loops through each account                     │
│         │                                                       │
│         ▼                                                       │
│   [Perplexity: Sonar-Deep-Research: TX Utility]                 │
│         │                                                       │
│         ▼                                                       │
│   [Google Docs: Create Deep Research document]                  │
│         │                                                       │
│         ▼                                                       │
│   [Google Docs: Get Content of Document]                        │
│         │                                                       │
│         ▼                                                       │
│   [Router] ─── splits into 3 parallel branches                  │
│         │                                                       │
│         ├──► Branch 1: SUMMARY                                  │
│         │    [ChatGPT: Summary of research (600 chars)]         │
│         │         │                                             │
│         │         ▼                                             │
│         │    [Apollo: Update with Summary + GDoc link]          │
│         │                                                       │
│         ├──► Branch 2: KPMG REPORT                              │
│         │    [ChatGPT: KPMG consultant agent]                   │
│         │         │                                             │
│         │         ▼                                             │
│         │    [Google Docs: Create Consultant output]            │
│         │         │                                             │
│         │         ▼                                             │
│         │    [Apollo: Update with KPMG GDoc link]               │
│         │                                                       │
│         └──► Branch 3: FINANCIAL RESEARCH                       │
│              [Perplexity: Financial Deep Research]              │
│                   │                                             │
│                   ▼                                             │
│              [Google Docs: Create Financial Health Analysis]    │
│                   │                                             │
│                   ▼                                             │
│              [Apollo: Update with Financial GDoc link]          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    APOLLO EMAIL GENERATION                      │
│              (AI Columns on Contact Lists)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CAMPAIGN 1: Legislative Focus (4-step sequence)               │
│   ├── Column 1: HB 144 Email                                    │
│   ├── Column 2: HB 145 Email                                    │
│   ├── Column 3: Tension/Pain Points Email                       │
│   └── Column 4: Reflection Email                                │
│                                                                 │
│   CAMPAIGN 2: Executive Financial (4-step sequence)             │
│   ├── Column 1: Financial Email (cross-ref job title + financials)│
│   ├── Column 2: [Email 2]                                       │
│   ├── Column 3: [Email 3]                                       │
│   └── Column 4: [Email 4]                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Future Optimization

The Financial Deep Research branch will be separated into its own Make scenario to avoid timeout issues.

---

### Step 1: Account List (Apollo)

**What:** Start with your target account list in Apollo - one state, ~10-20 utilities.

**Texas Example:**
- 18 electric cooperatives
- Criteria: Size, regulatory exposure, infrastructure age
- Stored as an Apollo account list

**Key Fields per Account (Apollo Custom Fields):**
| Field | Purpose |
|-------|---------|
| Company Name | Identification |
| Domain | For enrichment |
| Summary | 600-character account synopsis (populated by Make) |
| Deep Research GDoc | Link to Perplexity research output |
| KPMG Report GDoc | Link to consultant-style analysis |
| Financial Analysis GDoc | Link to financial deep research |

---

### Step 2: Deep Research (Make.com + Perplexity + ChatGPT)

**What:** A Make.com scenario that runs deep research on each account and stores outputs in Google Docs + Apollo.

**The Make Scenario: "eSmart Deep Account Research"**

#### Step 2a: Trigger
- **Module:** Apollo - Search accounts by list ID
- **What it does:** Pulls all accounts from your target list

#### Step 2b: Iterator
- **Module:** Iterator
- **What it does:** Loops through each account one by one

#### Step 2c: Perplexity Deep Research
- **Module:** Perplexity - Sonar-Deep-Research: TX Utility
- **What it does:** Researches the utility (regulatory context, wildfire mitigation, infrastructure)
- **Output:** Comprehensive research on the account

#### Step 2d: Save to Google Docs
- **Module:** Google Docs - Create a Document
- **What it does:** Saves the Perplexity output as a Google Doc for reference

#### Step 2e: Router (3 Parallel Branches)

**Branch 1: Summary**
- ChatGPT summarizes the research into 600 characters
- Apollo is updated with the summary text + link to the full Google Doc

**Branch 2: KPMG Consultant Report**
- ChatGPT analyzes the research and generates a KPMG-style risk assessment
- Output saved to a new Google Doc
- Apollo is updated with link to the KPMG report

**Branch 3: Financial Deep Research**
- A separate Perplexity agent runs financial-specific research
- Output saved to a new Google Doc (Financial Health Analysis)
- Apollo is updated with link to the financial report

**Design Principles:**
- Every claim needs a source citation
- Prompts tell AI to find data that substantiates known challenges (not infer challenges)
- All outputs stored in Google Docs for easy access and sharing
- Apollo custom fields hold links for quick reference

---

### Step 3: Contact Enrichment (Apollo)

**What:** Pull and validate contacts for each target account.

**Process:**
1. In Apollo, search contacts by account/company
2. Filter by relevant titles
3. Apollo validates email addresses automatically
4. Segment into lists by persona

**Texas Results:** 221 contacts across 18 utilities

---

### Step 4: Persona Segmentation (Apollo Lists)

**What:** Group contacts by role so messaging can be tailored.

**Our Segments:**

| Persona | Titles | Campaign |
|---------|--------|----------|
| Executive/Financial | CEO, CFO, VP Finance | Campaign 2 (Financial) |
| Operations & Asset | VP Ops, Asset Manager | Campaign 1 (Legislative) |
| Risk & Compliance | Risk Manager, Compliance | Campaign 1 (Legislative) |
| Mid-Level | Directors, Managers | Campaign 1 (Legislative) |

**Segmentation Rules:**
- Executives/Financial → Campaign 2 (leverages financial research)
- Everyone else → Campaign 1 (legislative focus: HB 144/145)
- C-Level and VP → High-touch, inline edits before sending
- Director and below → Template-driven, less customization

---

### Step 5: Email Generation (Apollo AI Columns)

**What:** Apollo AI columns generate persona-specific emails using the research outputs.

**Campaign 1: Legislative Focus (4-step sequence)**

| Column | Email Purpose |
|--------|---------------|
| HB 144 Email | References HB 144 wildfire legislation requirements |
| HB 145 Email | References HB 145 compliance requirements |
| Tension/Pain Points | Surfaces specific challenges based on research |
| Reflection Email | Follow-up that reflects on their situation |

**Campaign 2: Executive Financial (4-step sequence)**

| Column | Email Purpose |
|--------|---------------|
| Financial Email 1 | Cross-references job title + financial research findings |
| Financial Email 2 | Deeper dive on financial implications |
| Financial Email 3 | ROI/business case angle |
| Financial Email 4 | Final outreach with clear CTA |

**How It Works:**
- Apollo AI columns read from the account's custom fields (Summary, GDoc links)
- Each column has a prompt that generates a specific email type
- The contact's job title determines which campaign they're in
- Emails are used in 4-step Apollo sequences

**Email Design Principles:**
- Less robotic, more human/colloquial
- Minimize links and images (deliverability)
- Reference specific findings from research
- Always cite sources ("per your 2025 annual report...")

---

### Step 6: Sequences + HubSpot Reporting

**What:** Execute outreach via Apollo sequences, track in HubSpot.

**Apollo Sequences:**
- Campaign 1: Legislative sequence (4 emails)
- Campaign 2: Executive Financial sequence (4 emails)
- 40 emails/day cap (quality over quantity)

**HubSpot Integration:**
- Contacts sync from Apollo
- Activity tracking (opens, replies, meetings)
- Simple dashboards for reporting

**Metrics to Track:**
| Metric | Target |
|--------|--------|
| Open Rate | >40% |
| Reply Rate | >5% |
| Meeting Book Rate | >1% |
| Positive Reply Rate | Track sentiment |

---

## 3. Using the Standalone Components

### Overview

The system has three main components that can be understood and modified independently:

1. **Make.com Scenario** - Orchestrates the research automation
2. **Google Docs** - Stores research outputs
3. **Apollo AI Columns** - Generates emails from research

### Component 1: Make.com Scenario

**Name:** "eSmart Deep Account Research: Apollo <> Perplexity <> GDocs <> Make"

**What It Does:** Takes an Apollo account list, runs deep research on each account, and stores outputs back in Apollo.

#### How to Run the Scenario

1. Open Make.com
2. Find the "eSmart Deep Account Research" scenario
3. Verify the Apollo list ID is correct (or update it)
4. Click "Run once" to test on one account
5. Once validated, schedule or run the full batch

#### How to Modify the Scenario

**To change the Perplexity research prompt:**
1. Open the scenario in Make.com
2. Click the "Sonar-Deep-Research: TX Utility" module
3. Edit the prompt in the chat completion settings
4. Save and test on 1-2 accounts

**To change the ChatGPT summarization:**
1. Click the "Summary of research (600 characters)" module
2. Edit the prompt
3. Adjust character limit if needed

**To change the KPMG consultant analysis:**
1. Click the "KPMG consultant agent" module
2. Edit the prompt to adjust tone, structure, or focus areas

**To change the Financial Deep Research:**
1. Click the "Financial Deep Research" module
2. Edit the Perplexity prompt for different financial metrics

#### Key Module Settings

| Module | Key Settings |
|--------|--------------|
| Perplexity (TX Utility) | Prompt, model selection, search depth |
| ChatGPT (Summary) | Prompt, max tokens (600 chars ≈ 150 tokens) |
| ChatGPT (KPMG) | Prompt, tone instructions, output structure |
| Perplexity (Financial) | Prompt, recency filter, citation requirements |
| Google Docs | Folder location, naming convention |
| Apollo | List ID, custom field mappings |

#### Timeout Considerations

The current scenario runs all branches in one execution. For large lists, you may hit Make.com timeout limits.

**Future optimization:** Separate the Financial Deep Research into its own scenario that triggers after the main research completes.

---

### Component 2: Apollo AI Columns (Email Generation)

**What They Do:** Generate persona-specific emails using the research stored in Apollo custom fields.

#### Your AI Column Inventory

**Campaign 1 - Legislative Focus:**
| Column Name | Purpose | Inputs Referenced |
|-------------|---------|-------------------|
| HB 144 Email | Wildfire legislation angle | Summary, Deep Research GDoc |
| HB 145 Email | Compliance requirements | Summary, Deep Research GDoc |
| Tension Email | Surface pain points | Summary, KPMG Report |
| Reflection Email | Follow-up reflection | Summary, previous emails |

**Campaign 2 - Executive Financial:**
| Column Name | Purpose | Inputs Referenced |
|-------------|---------|-------------------|
| Financial Email 1 | Financial-focused opener | Job Title, Financial Analysis GDoc |
| Financial Email 2 | Deeper financial dive | Job Title, Financial Analysis GDoc |
| Financial Email 3 | ROI/business case | Job Title, Financial Analysis GDoc |
| Financial Email 4 | Final CTA | Job Title, Summary |

#### How to Modify Apollo AI Columns

1. Go to your contact list in Apollo
2. Click on the column header for the AI column you want to edit
3. Select "Edit AI prompt"
4. Modify the prompt
5. Test by running on 2-3 contacts
6. Review outputs before running on full list

#### Common Modifications

| Change | How to Do It |
|--------|--------------|
| Adjust tone | Add tone instructions: "Write in a conversational, peer-to-peer tone..." |
| Add personalization | Reference additional fields: "Use their {job_title} to tailor..." |
| Change email length | Add constraint: "Keep the email under 150 words..." |
| Reference different research | Point to different custom field: "Using the {Financial Analysis GDoc}..." |

---

### Component 3: Google Docs (Research Storage)

**What They Store:**
- Deep Research output (one doc per account)
- KPMG Consultant Report (one doc per account)
- Financial Health Analysis (one doc per account)

#### Folder Structure

```
Google Drive/
└── eSmart Research/
   ├── Deep Research/
   │   ├── [Utility Name] - Deep Research.gdoc
   │   └── ...
   ├── KPMG Reports/
   │   ├── [Utility Name] - KPMG Analysis.gdoc
   │   └── ...
   └── Financial Analysis/
      ├── [Utility Name] - Financial Health.gdoc
      └── ...
```

#### How to Access

- Direct links are stored in Apollo custom fields
- Click the link in Apollo to open the full research
- Share links with team members as needed

---

## 4. Self-Sufficiency Checklist

### Matt Can Do Independently

**Apollo:**
- [ ] Add new utilities to account lists
- [ ] Run contact searches and build contact lists
- [ ] Modify AI column prompts (email generation)
- [ ] Adjust persona segments / list filters
- [ ] Add/remove contacts from sequences
- [ ] Monitor sequence performance
- [ ] Pause/resume sequences
- [ ] A/B test email variations

**Make.com:**
- [ ] Run existing scenario on new account lists
- [ ] Update Apollo list ID in the scenario
- [ ] Minor prompt tweaks in Perplexity/ChatGPT modules

**HubSpot:**
- [ ] Pull activity reports
- [ ] Monitor deal pipeline
- [ ] Track engagement metrics

**Google Docs:**
- [ ] Access and review research outputs
- [ ] Share docs with team members

### May Need Support For

- [ ] Building new Make.com scenarios from scratch
- [ ] Adding new modules/integrations to Make
- [ ] Separating Financial Research into its own scenario
- [ ] Complex prompt engineering overhauls
- [ ] Troubleshooting API/integration issues
- [ ] Setting up new state (first-time replication)
- [ ] Apollo AI column architecture changes

### Quick Reference: Where Things Live

| What | Where |
|------|-------|
| Account lists | Apollo → Lists |
| Account custom fields | Apollo → Account record |
| Contact lists | Apollo → Lists |
| Email AI prompts | Apollo → AI Columns on contact lists |
| Sequences | Apollo → Sequences |
| Research automation | Make.com → "eSmart Deep Account Research" scenario |
| Research outputs | Google Drive → eSmart Research folder |
| CRM / Reporting | HubSpot |
| Perplexity prompts | Make.com → Perplexity modules |
| ChatGPT prompts | Make.com → ChatGPT modules |

---

## 5. Scaling to Other Reps

### The Repeatable Pattern

```
1 State + ~10-20 Utilities + Quality Contacts + Personalized Messages
```

This is the formula. Each rep owns a state (or region) and runs the same workflow.

### To Replicate for Another Rep

#### Phase 1: Setup (Do Once Per Rep)

1. **Pick the state**
- Start with one state per rep
- Consider: regulatory environment, market size, existing relationships

2. **Build account list in Apollo**
- Create new account list for the state
- Add ~10-20 utilities
- Ensure custom fields are set up (Summary, GDoc links)

3. **Clone the Make.com scenario**
- Duplicate "eSmart Deep Account Research" scenario
- Rename for the new state (e.g., "eSmart Deep Account Research - Florida")
- Update Apollo list ID to point to new list

#### Phase 2: Customize

4. **Adjust prompts for state context**

**In Make.com (Perplexity/ChatGPT modules):**
| What Changes | Texas → [New State] |
|--------------|---------------------|
| Regulatory references | HB 144/145 → [State equivalent legislation] |
| Regional terms | ERCOT → [Regional grid operator: PJM, MISO, etc.] |
| Risk factors | Wildfire → [State-specific risks: hurricanes, ice storms, etc.] |

**In Apollo (AI columns):**
| What Changes | Texas → [New State] |
|--------------|---------------------|
| Legislative email prompts | HB 144/145 references → State equivalent |
| Regional context | Texas-specific language → State-specific |

5. **Run the Make scenario**
- Execute on new account list
- Review Google Doc outputs for quality
- Verify Apollo custom fields are populated

6. **Build contact lists in Apollo**
- Search contacts by account
- Filter by relevant titles
- Create segmented lists (Executive, Operations, etc.)

#### Phase 3: Launch

7. **Generate emails via Apollo AI columns**
- Run AI enrichment on contact lists
- Review high-priority contacts (C-level) before sending

8. **Create sequences in Apollo**
- Clone existing sequences or create new
- Assign contacts to sequences
- Set daily send limits

9. **Train rep on execution**
- How to monitor sequences in Apollo
- How to handle replies
- How to update HubSpot
- When to escalate

### What Changes Per State

| Element | Changes? | Where to Change |
|---------|----------|-----------------|
| Account list | Yes | Apollo - new list |
| Make scenario | Clone + update list ID | Make.com |
| Perplexity prompts | Update regulatory refs | Make.com modules |
| ChatGPT prompts | Update state context | Make.com modules |
| Apollo AI columns | Update legislative refs | Apollo column prompts |
| Sequences | Clone or reuse | Apollo |
| Google Drive | New folder for state | Google Drive |

### What Stays the Same

- Overall workflow architecture
- Make.com scenario structure
- Persona segmentation logic
- Quality standards (citations, recency)
- Email design principles
- HubSpot reporting structure

### Estimated Effort Per New State

| Task | Effort |
|------|--------|
| Build account list in Apollo | 2-4 hours |
| Clone Make scenario + update | 1 hour |
| Customize Perplexity/ChatGPT prompts | 2-3 hours |
| Run Make scenario | 1-2 hours (mostly automated) |
| Build contact lists in Apollo | 2-3 hours |
| Update Apollo AI column prompts | 1-2 hours |
| Generate emails (run AI columns) | 1 hour (automated) |
| QA and review | 2-3 hours |
| Rep training | 1-2 hours |
| **Total** | **~15-20 hours** |

---

## 6. Resources & Support

### Documentation

- **This playbook** (Notion)
- **Make.com scenario** (cloneable for new states)
- **Apollo AI column prompts** (in your contact list columns)
- **Google Docs research outputs** (shared folder)

### Key Links

| Resource | Link |
|----------|------|
| Make.com workspace | [link] |
| Apollo | [link] |
| HubSpot | [link] |
| Perplexity | [link] |
| Google Drive (Research folder) | [link] |
| ChatGPT (if separate account) | [link] |

### Training Materials

- [ ] Recorded walkthrough: [to be created]
- [ ] Make.com scenario walkthrough: [to be created]
- [ ] Apollo AI columns guide: [Section 3 above]
- [ ] Troubleshooting FAQ: [to be created]

### Support Channels

| Type | Contact |
|------|---------|
| General questions | willy@thegtmfactory.com |
| Urgent issues | [phone/text] |
| Slack | [if applicable] |

### When to Reach Out

**Definitely reach out if:**
- Make.com scenario errors or timeouts
- Apollo AI column failures
- Need to add new capability
- Scaling to new state (first time)
- Performance issues (low reply rates, deliverability)
- Integration breaks (Apollo ↔ HubSpot, Make ↔ Apollo)

**Try self-service first:**
- Minor prompt tweaks (Make.com or Apollo)
- Adding/removing contacts from lists
- Sequence adjustments in Apollo
- HubSpot report questions
- Accessing Google Docs research

---

## 7. Next Steps

### Immediate (This Week)

- [ ] Matt reviews this playbook
- [ ] Walkthrough call to answer questions
- [ ] Identify first state for replication (if scaling)

### Short-Term (Next 2-4 Weeks)

- [ ] Complete Texas campaign execution
- [ ] Gather performance data
- [ ] Refine based on what's working
- [ ] Scope scaling engagement (how many states/reps?)

### Longer-Term

- [ ] Replicate to additional states
- [ ] Train additional reps
- [ ] Build internal documentation for eSmart team
- [ ] Transition to full self-sufficiency

---

## Appendix: Key Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Dec 17, 2025 | 3 research focus areas: utility overview, legislative impact, wildfire mitigation | Cover key research areas for Texas utilities |
| Jan 8, 2026 | Quality over quantity, 40 emails/day cap | High-touch approach works better for enterprise |
| Jan 12, 2026 | Modular architecture: Make.com for research, Apollo for emails | Easier to iterate and debug each component |
| Jan 15, 2026 | Consultant-style reports (KPMG-like) via ChatGPT | Differentiate from generic outbound |
| Jan 21, 2026 | Use Make.com to orchestrate Perplexity + ChatGPT + Google Docs | Flexible automation with multiple AI providers |
| Jan 22, 2026 | A/B test direct vs. consultative email styles | Determine what resonates |
| Jan 23, 2026 | 24-month recency filter on Perplexity research | Credibility requires recent data |
| Jan 26, 2026 | 18 vetted accounts, segment contacts by persona | Focus resources on best targets |
| Jan 27, 2026 | C-level/VP get inline edits, others templated | Balance quality with efficiency |
| Jan 27, 2026 | Separate Financial Deep Research as its own Perplexity call | Different research focus than main utility research |
| Future | Separate Financial Research into own Make scenario | Avoid timeout issues on large lists |

---

**Document Version:** 1.0
**Last Updated:** January 30, 2026
**Owner:** Willy Hernandez, The GTM Factory
