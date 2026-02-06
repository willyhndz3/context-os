from anthropic import AsyncAnthropic
from config import ANTHROPIC_API_KEY

client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are the GTM Context OS assistant. You help with go-to-market intelligence.

You have access to a structured knowledge base with:
- Account records (companies, contacts, deal status)
- ICP definitions (ideal customer profiles)
- Messaging and positioning (value props, narratives)
- Methodology (frameworks, patterns)
- Objections and responses
- Competitive intelligence

Keep responses concise and mobile-friendly (the user is reading on their phone).
Use bullet points. No walls of text. Max 2-3 short paragraphs."""

CAPTURE_SYSTEM_PROMPT = """You are the GTM Context OS assistant processing a capture from the field.

Extract structured data from the user's message and return a JSON response with:
{
  "account_name": "Company Name",
  "account_dir_name": "Company-Name",
  "contact": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1-555-1234",
    "title": "Job Title"
  },
  "notes": "Key insights, interests, context from the interaction",
  "icp_match": ["gtm-automation-buyer", "enterprise-developer-tools"],
  "related_concepts": ["clay-workflow-service"],
  "account_md": "Full markdown content for account.md following the template format",
  "is_new_account": true
}

Rules:
- account_dir_name uses hyphens, no spaces
- Only include fields that were mentioned (null for missing)
- icp_match should reference existing ICPs if they fit
- related_concepts should reference existing knowledge base nodes if relevant
- account_md should follow the account template format with YAML frontmatter
- Set status to "prospect" and stage to "discovery" for new accounts"""


def build_query_prompt(question: str, context_files: list[dict]) -> str:
    """Build prompt for query mode."""
    parts = ["Here are the relevant files from the GTM knowledge base:\n"]
    for f in context_files:
        parts.append(f"--- {f['path']} ---\n{f['content']}\n")
    parts.append(f"\nQuestion: {question}")
    return "\n".join(parts)


def build_capture_prompt(raw_text: str) -> str:
    """Build prompt for capture mode."""
    return f"Process this field capture into structured data:\n\n{raw_text}"


def build_prep_prompt(
    account_name: str,
    account_content: str,
    briefings: list[dict],
    kb_nodes: list[dict],
) -> str:
    """Build prompt for prep mode."""
    parts = [f"Prepare a concise call briefing for {account_name}.\n"]
    parts.append(f"--- Account Record ---\n{account_content}\n")

    if briefings:
        parts.append("--- Previous Briefings ---\n")
        for b in briefings:
            parts.append(f"{b['path']}:\n{b['content']}\n")

    if kb_nodes:
        parts.append("--- Related Knowledge ---\n")
        for node in kb_nodes:
            parts.append(f"{node['path']}:\n{node['content']}\n")

    parts.append("""
Format the briefing for mobile reading:
1. Company snapshot (2-3 bullets)
2. Key contacts and roles
3. Where we left off
4. Their pain points / what they need
5. Our relevant services / positioning
6. Watch out for (objections, risks)
7. Suggested talking points""")

    return "\n".join(parts)


async def ask_claude(prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """Send a prompt to Claude Sonnet and return the response."""
    message = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


async def query(question: str, context_files: list[dict]) -> str:
    """Answer a question using knowledge base context."""
    prompt = build_query_prompt(question, context_files)
    return await ask_claude(prompt)


async def capture(raw_text: str) -> str:
    """Process a field capture and return structured JSON."""
    prompt = build_capture_prompt(raw_text)
    return await ask_claude(prompt, system=CAPTURE_SYSTEM_PROMPT)


async def prep(
    account_name: str,
    account_content: str,
    briefings: list[dict],
    kb_nodes: list[dict],
) -> str:
    """Generate a call prep briefing."""
    prompt = build_prep_prompt(account_name, account_content, briefings, kb_nodes)
    return await ask_claude(prompt)
