# GTM Context OS Telegram Bot -- Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Telegram bot that provides mobile two-way access to the GTM Context OS -- query the knowledge base, capture new contacts/insights, and get call prep briefings from your phone.

**Architecture:** Python FastAPI app on Railway receives Telegram webhook messages, reads/writes GTM Context OS files from a GitHub repo clone, calls Claude Sonnet for reasoning, and syncs contact data to Clarify via REST API.

**Tech Stack:** Python 3.12, FastAPI, python-telegram-bot 22.6, Anthropic SDK, Clarify REST API, Railway, GitHub

---

## Prerequisites (Manual Steps -- Do Before Starting)

These are things Willy needs to do in browser/phone before we write code:

- [ ] **Telegram bot token**: Message @BotFather on Telegram, run `/newbot`, save the token
- [ ] **Anthropic API key**: Go to console.anthropic.com, add billing, generate a new key (do NOT paste it in chat)
- [ ] **Clarify API key**: Go to Clarify workspace settings, generate an API key. Also note your workspace slug (visible in the URL when logged in)
- [ ] **Railway account**: Sign up at railway.com, select Hobby plan ($5)

---

## Task 1: Initialize Git Repo and Push to GitHub

**Files:**
- Create: `.gitignore`
- Modify: existing GTM Context OS directory

**Step 1: Create .gitignore**

```
.obsidian/
.env
__pycache__/
*.pyc
.DS_Store
```

**Step 2: Initialize git and push to GitHub**

```bash
cd /Users/willyhernandez/claude-code-setup/gtm-context-os
git init
git add .
git commit -m "Initial commit: GTM Context OS knowledge base"
```

**Step 3: Push to existing GitHub repo**

The repo https://github.com/willyhndz3/context-os already exists but is outdated. We'll force-push the current state (after Willy confirms this is okay since it replaces old content).

```bash
git remote add origin https://github.com/willyhndz3/context-os.git
git branch -M main
git push -u origin main --force
```

**Step 4: Verify on GitHub**

Open https://github.com/willyhndz3/context-os and confirm all files are there.

**Step 5: Commit**

Already committed in Step 2.

---

## Task 2: Create Bot Project Structure

**Files:**
- Create: `bot/main.py`
- Create: `bot/config.py`
- Create: `bot/requirements.txt`
- Create: `bot/Procfile`
- Create: `bot/.gitignore`
- Create: `bot/.env.example`

This is a separate project directory inside the GTM Context OS repo. The bot lives alongside the knowledge base.

**Step 1: Create project skeleton**

Create `bot/` directory with the following files:

`bot/requirements.txt`:
```
python-telegram-bot==22.6
anthropic>=0.78.0
fastapi>=0.115.0
uvicorn>=0.34.0
httpx>=0.27.0
```

`bot/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

`bot/.env.example`:
```
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
ANTHROPIC_API_KEY=sk-ant-your-key-here
WEBHOOK_SECRET=some-random-secret-string
CLARIFY_API_KEY=your-clarify-api-key
CLARIFY_WORKSPACE_SLUG=your-workspace-slug
GITHUB_TOKEN=your-github-personal-access-token
GITHUB_REPO=willyhndz3/context-os
```

`bot/.gitignore`:
```
.env
__pycache__/
*.pyc
.venv/
```

`bot/config.py`:
```python
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "change-me")
CLARIFY_API_KEY = os.environ.get("CLARIFY_API_KEY", "")
CLARIFY_WORKSPACE_SLUG = os.environ.get("CLARIFY_WORKSPACE_SLUG", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "willyhndz3/context-os")

RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
WEBHOOK_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else ""

PORT = int(os.environ.get("PORT", "8000"))

KNOWLEDGE_BASE_PATH = os.environ.get("KNOWLEDGE_BASE_PATH", "/app/knowledge")
```

**Step 2: Commit**

```bash
git add bot/
git commit -m "feat: add bot project skeleton"
```

---

## Task 3: Build the Knowledge Base Reader

This module clones the GitHub repo on startup and provides functions to find and read relevant files.

**Files:**
- Create: `bot/knowledge.py`
- Create: `bot/tests/test_knowledge.py`

**Step 1: Write the failing test**

`bot/tests/__init__.py`: (empty)

`bot/tests/test_knowledge.py`:
```python
import os
import tempfile
import pytest
from knowledge import KnowledgeBase


@pytest.fixture
def sample_kb(tmp_path):
    """Create a minimal knowledge base structure for testing."""
    # Create directory structure
    (tmp_path / "accounts" / "Acme-Corp").mkdir(parents=True)
    (tmp_path / "knowledge_base" / "icp").mkdir(parents=True)
    (tmp_path / "knowledge_base" / "objections").mkdir(parents=True)
    (tmp_path / "_system" / "knowledge_graph").mkdir(parents=True)

    # Create sample account file
    (tmp_path / "accounts" / "Acme-Corp" / "account.md").write_text(
        "---\nname: ACME_CORP\nstatus: prospect\n---\n# Acme Corp\nA test account."
    )

    # Create sample knowledge base node
    (tmp_path / "knowledge_base" / "objections" / "pricing-objection.md").write_text(
        "---\nname: PRICING_OBJECTION\ndomain: objections\n---\n# Pricing Objection\nRate too high."
    )

    # Create taxonomy
    (tmp_path / "_system" / "knowledge_graph" / "taxonomy.yaml").write_text(
        "domains:\n  blessed:\n    - icp\n    - objections\n"
    )

    return KnowledgeBase(str(tmp_path))


def test_find_account(sample_kb):
    files = sample_kb.find_relevant_files("What do we know about Acme Corp?")
    paths = [f["path"] for f in files]
    assert any("Acme-Corp" in p for p in paths)


def test_find_objection(sample_kb):
    files = sample_kb.find_relevant_files("pricing objection")
    paths = [f["path"] for f in files]
    assert any("pricing-objection" in p for p in paths)


def test_list_accounts(sample_kb):
    accounts = sample_kb.list_accounts()
    assert "Acme-Corp" in accounts


def test_get_account(sample_kb):
    content = sample_kb.get_account("Acme-Corp")
    assert "Acme Corp" in content
```

**Step 2: Run tests to verify they fail**

```bash
cd bot && python -m pytest tests/test_knowledge.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'knowledge'`

**Step 3: Write the implementation**

`bot/knowledge.py`:
```python
import os
import subprocess
from pathlib import Path


class KnowledgeBase:
    def __init__(self, path: str):
        self.path = Path(path)

    @classmethod
    def clone_from_github(cls, repo: str, token: str, dest: str) -> "KnowledgeBase":
        """Clone or pull the knowledge base from GitHub."""
        if os.path.exists(os.path.join(dest, ".git")):
            subprocess.run(["git", "-C", dest, "pull"], check=True, capture_output=True)
        else:
            url = f"https://x-access-token:{token}@github.com/{repo}.git"
            subprocess.run(["git", "clone", url, dest], check=True, capture_output=True)
        return cls(dest)

    def pull(self):
        """Pull latest changes from GitHub."""
        subprocess.run(
            ["git", "-C", str(self.path), "pull"],
            check=True, capture_output=True
        )

    def commit_and_push(self, message: str):
        """Commit all changes and push to GitHub."""
        subprocess.run(["git", "-C", str(self.path), "add", "."], check=True, capture_output=True)
        result = subprocess.run(
            ["git", "-C", str(self.path), "diff", "--cached", "--quiet"],
            capture_output=True
        )
        if result.returncode != 0:  # There are staged changes
            subprocess.run(
                ["git", "-C", str(self.path), "commit", "-m", message],
                check=True, capture_output=True
            )
            subprocess.run(
                ["git", "-C", str(self.path), "push"],
                check=True, capture_output=True
            )

    def list_accounts(self) -> list[str]:
        """List all account directory names."""
        accounts_dir = self.path / "accounts"
        if not accounts_dir.exists():
            return []
        return [
            d.name for d in accounts_dir.iterdir()
            if d.is_dir() and d.name != "_templates"
        ]

    def get_account(self, name: str) -> str:
        """Get account.md content by company name (case-insensitive match)."""
        accounts_dir = self.path / "accounts"
        for d in accounts_dir.iterdir():
            if d.is_dir() and d.name.lower() == name.lower():
                account_file = d / "account.md"
                if account_file.exists():
                    return account_file.read_text()
        return ""

    def get_briefings(self, account_name: str) -> list[dict]:
        """Get all briefings for an account."""
        accounts_dir = self.path / "accounts"
        for d in accounts_dir.iterdir():
            if d.is_dir() and d.name.lower() == account_name.lower():
                briefings_dir = d / "briefings"
                if not briefings_dir.exists():
                    return []
                return [
                    {"path": str(f.relative_to(self.path)), "content": f.read_text()}
                    for f in sorted(briefings_dir.glob("*.md"), reverse=True)
                ]
        return []

    def find_relevant_files(self, query: str) -> list[dict]:
        """Find files relevant to a query using keyword matching."""
        query_lower = query.lower()
        results = []

        # Search accounts
        for account_dir in (self.path / "accounts").iterdir():
            if not account_dir.is_dir() or account_dir.name == "_templates":
                continue
            if account_dir.name.lower().replace("-", " ") in query_lower or \
               query_lower in account_dir.name.lower().replace("-", " "):
                account_file = account_dir / "account.md"
                if account_file.exists():
                    results.append({
                        "path": str(account_file.relative_to(self.path)),
                        "content": account_file.read_text()
                    })

        # Search knowledge base
        kb_dir = self.path / "knowledge_base"
        if kb_dir.exists():
            for md_file in kb_dir.rglob("*.md"):
                filename = md_file.stem.replace("-", " ")
                content = md_file.read_text()
                if filename in query_lower or any(
                    word in content.lower() for word in query_lower.split() if len(word) > 3
                ):
                    results.append({
                        "path": str(md_file.relative_to(self.path)),
                        "content": content
                    })

        # Always include taxonomy for context
        taxonomy = self.path / "_system" / "knowledge_graph" / "taxonomy.yaml"
        if taxonomy.exists():
            results.append({
                "path": str(taxonomy.relative_to(self.path)),
                "content": taxonomy.read_text()
            })

        return results

    def get_all_context(self) -> str:
        """Get a summary of all accounts and knowledge base nodes for broad queries."""
        parts = []
        parts.append("## Accounts\n")
        for name in self.list_accounts():
            content = self.get_account(name)
            # Just grab the first few lines for summary
            lines = content.split("\n")[:15]
            parts.append(f"### {name}\n" + "\n".join(lines) + "\n")

        parts.append("## Knowledge Base Nodes\n")
        kb_dir = self.path / "knowledge_base"
        if kb_dir.exists():
            for md_file in kb_dir.rglob("*.md"):
                content = md_file.read_text()
                lines = content.split("\n")[:10]
                parts.append(f"### {md_file.stem}\n" + "\n".join(lines) + "\n")

        return "\n".join(parts)

    def write_file(self, relative_path: str, content: str):
        """Write content to a file in the knowledge base."""
        full_path = self.path / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
```

**Step 4: Run tests to verify they pass**

```bash
cd bot && python -m pytest tests/test_knowledge.py -v
```

Expected: All 4 tests PASS.

**Step 5: Commit**

```bash
git add bot/knowledge.py bot/tests/
git commit -m "feat: add knowledge base reader with file search"
```

---

## Task 4: Build the Claude Sonnet Service

This module wraps the Anthropic SDK and provides specialized prompts for query, capture, and prep modes.

**Files:**
- Create: `bot/claude_service.py`
- Create: `bot/tests/test_claude_service.py`

**Step 1: Write the failing test**

`bot/tests/test_claude_service.py`:
```python
import pytest
from claude_service import build_query_prompt, build_capture_prompt, build_prep_prompt


def test_build_query_prompt():
    context = [{"path": "accounts/Acme/account.md", "content": "# Acme\nA company."}]
    prompt = build_query_prompt("What do we know about Acme?", context)
    assert "Acme" in prompt
    assert "account.md" in prompt


def test_build_capture_prompt():
    prompt = build_capture_prompt("Met Jake from Acme, jake@acme.com, likes Clay workflows")
    assert "Jake" in prompt
    assert "jake@acme.com" in prompt


def test_build_prep_prompt():
    account_content = "# WSO2\nDeveloper tools company."
    briefings = [{"path": "briefings/2026-01-28.md", "content": "Call prep notes."}]
    kb_nodes = [{"path": "kb/icp/dev-tools.md", "content": "# Dev Tools ICP"}]
    prompt = build_prep_prompt("WSO2", account_content, briefings, kb_nodes)
    assert "WSO2" in prompt
    assert "briefing" in prompt.lower() or "prep" in prompt.lower()
```

**Step 2: Run tests to verify they fail**

```bash
cd bot && python -m pytest tests/test_claude_service.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write the implementation**

`bot/claude_service.py`:
```python
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
```

**Step 4: Run tests to verify they pass**

```bash
cd bot && python -m pytest tests/test_claude_service.py -v
```

Expected: All 3 tests PASS (these test prompt building, not the API call).

**Step 5: Commit**

```bash
git add bot/claude_service.py bot/tests/test_claude_service.py
git commit -m "feat: add Claude Sonnet service with query, capture, and prep prompts"
```

---

## Task 5: Build the Clarify CRM Client

**Files:**
- Create: `bot/clarify_client.py`
- Create: `bot/tests/test_clarify_client.py`

**Step 1: Write the failing test**

`bot/tests/test_clarify_client.py`:
```python
import pytest
from clarify_client import ClarifyClient


def test_client_init():
    client = ClarifyClient("test-slug", "test-key")
    assert client.base_url == "https://api.clarify.ai/v1/workspaces/test-slug"


def test_headers():
    client = ClarifyClient("test-slug", "test-key")
    assert client.headers["Authorization"] == "api-key test-key"
    assert client.headers["Content-Type"] == "application/json"


def test_person_payload():
    client = ClarifyClient("test-slug", "test-key")
    payload = client._build_person_payload("Jane Smith", "jane@acme.com", title="VP Sales")
    assert payload["data"]["attributes"]["name"] == "Jane Smith"
    assert payload["data"]["attributes"]["email_addresses"] == ["jane@acme.com"]
    assert payload["data"]["attributes"]["title"] == "VP Sales"


def test_company_payload():
    client = ClarifyClient("test-slug", "test-key")
    payload = client._build_company_payload("Acme Corp", "acme.com")
    assert payload["data"]["attributes"]["name"] == "Acme Corp"
    assert payload["data"]["attributes"]["domains"] == ["acme.com"]
```

**Step 2: Run tests to verify they fail**

```bash
cd bot && python -m pytest tests/test_clarify_client.py -v
```

Expected: FAIL

**Step 3: Write the implementation**

`bot/clarify_client.py`:
```python
import httpx
import logging

logger = logging.getLogger(__name__)


class ClarifyClient:
    def __init__(self, workspace_slug: str, api_key: str):
        self.base_url = f"https://api.clarify.ai/v1/workspaces/{workspace_slug}"
        self.headers = {
            "Authorization": f"api-key {api_key}",
            "Content-Type": "application/json",
        }
        self.enabled = bool(workspace_slug and api_key)

    def _build_person_payload(self, name: str, email: str, **extra) -> dict:
        attrs = {"name": name, "email_addresses": [email]}
        if "phone" in extra and extra["phone"]:
            attrs["phone_numbers"] = [extra["phone"]]
        if "title" in extra and extra["title"]:
            attrs["title"] = extra["title"]
        return {"data": {"type": "person", "attributes": attrs}}

    def _build_company_payload(self, name: str, domain: str, **extra) -> dict:
        attrs = {"name": name, "domains": [domain]}
        return {"data": {"type": "company", "attributes": attrs}}

    async def create_person(self, name: str, email: str, **extra) -> dict | None:
        """Create or upsert a person in Clarify. Returns response or None on failure."""
        if not self.enabled:
            logger.warning("Clarify not configured, skipping person creation")
            return None
        payload = self._build_person_payload(name, email, **extra)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/objects/person/records",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify create_person failed: {resp.status_code} {resp.text}")
                return None
            return resp.json()

    async def create_company(self, name: str, domain: str) -> dict | None:
        """Create or upsert a company in Clarify. Returns response or None on failure."""
        if not self.enabled:
            logger.warning("Clarify not configured, skipping company creation")
            return None
        payload = self._build_company_payload(name, domain)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/objects/company/records",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify create_company failed: {resp.status_code} {resp.text}")
                return None
            return resp.json()

    async def link_person_to_company(self, person_id: str, company_id: str) -> bool:
        """Link a person to a company. Returns True on success."""
        if not self.enabled:
            return False
        payload = {"data": [{"id": company_id, "type": "company"}]}
        async with httpx.AsyncClient() as client:
            resp = await client.patch(
                f"{self.base_url}/objects/person/records/{person_id}/relationships/company",
                headers=self.headers,
                json=payload,
            )
            if resp.status_code >= 400:
                logger.error(f"Clarify link failed: {resp.status_code} {resp.text}")
                return False
            return True
```

**Step 4: Run tests to verify they pass**

```bash
cd bot && python -m pytest tests/test_clarify_client.py -v
```

Expected: All 4 tests PASS.

**Step 5: Commit**

```bash
git add bot/clarify_client.py bot/tests/test_clarify_client.py
git commit -m "feat: add Clarify CRM client for person/company creation"
```

---

## Task 6: Build the Telegram Handlers

**Files:**
- Create: `bot/handlers.py`

**Step 1: Write the handlers**

`bot/handlers.py`:
```python
import json
import logging
from telegram import Update
from telegram.ext import ContextTypes

import claude_service
from knowledge import KnowledgeBase
from clarify_client import ClarifyClient
from config import (
    CLARIFY_API_KEY,
    CLARIFY_WORKSPACE_SLUG,
    GITHUB_TOKEN,
    GITHUB_REPO,
    KNOWLEDGE_BASE_PATH,
)

logger = logging.getLogger(__name__)

# Initialize on first use
_kb: KnowledgeBase | None = None
_clarify: ClarifyClient | None = None


def get_kb() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase.clone_from_github(GITHUB_REPO, GITHUB_TOKEN, KNOWLEDGE_BASE_PATH)
    return _kb


def get_clarify() -> ClarifyClient:
    global _clarify
    if _clarify is None:
        _clarify = ClarifyClient(CLARIFY_WORKSPACE_SLUG, CLARIFY_API_KEY)
    return _clarify


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language queries (default message handler)."""
    question = update.message.text
    await update.message.reply_text("Looking that up...")

    kb = get_kb()
    kb.pull()

    relevant_files = kb.find_relevant_files(question)
    if not relevant_files:
        # Broad query -- give overview context
        overview = kb.get_all_context()
        relevant_files = [{"path": "overview", "content": overview}]

    response = await claude_service.query(question, relevant_files)

    # Telegram has a 4096 char limit per message
    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i:i + 4000])
    else:
        await update.message.reply_text(response)


async def handle_capture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /capture command -- process field notes into the knowledge base."""
    raw_text = " ".join(context.args) if context.args else ""
    if not raw_text:
        await update.message.reply_text(
            "Usage: /capture Met Jake from Acme Corp, jake@acme.com, interested in Clay workflows"
        )
        return

    await update.message.reply_text("Processing capture...")

    kb = get_kb()
    kb.pull()

    # Get Claude to extract structured data
    response = await claude_service.capture(raw_text)

    try:
        # Parse the JSON from Claude's response
        # Claude might wrap it in markdown code blocks
        json_str = response
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]

        data = json.loads(json_str.strip())

        actions = []

        # Write account file
        if data.get("account_md") and data.get("account_dir_name"):
            dir_name = data["account_dir_name"]
            kb.write_file(f"accounts/{dir_name}/account.md", data["account_md"])
            # Create empty subdirectories
            kb.write_file(f"accounts/{dir_name}/briefings/.gitkeep", "")
            kb.write_file(f"accounts/{dir_name}/diagrams/.gitkeep", "")
            actions.append(f"Created account: {data.get('account_name', dir_name)}")

        # Sync to Clarify
        contact = data.get("contact", {})
        if contact.get("email"):
            clarify = get_clarify()

            # Create company if we have a domain from the email
            company_id = None
            email_domain = contact["email"].split("@")[1] if "@" in contact["email"] else None
            if email_domain and data.get("account_name"):
                company_resp = await clarify.create_company(data["account_name"], email_domain)
                if company_resp:
                    company_id = company_resp.get("data", {}).get("id")
                    actions.append(f"Synced company to Clarify: {data['account_name']}")

            # Create person
            person_resp = await clarify.create_person(
                name=contact.get("name", ""),
                email=contact["email"],
                phone=contact.get("phone"),
                title=contact.get("title"),
            )
            if person_resp:
                person_id = person_resp.get("data", {}).get("id")
                actions.append(f"Synced contact to Clarify: {contact.get('name', contact['email'])}")

                # Link person to company
                if company_id and person_id:
                    await clarify.link_person_to_company(person_id, company_id)

        # Commit and push
        kb.commit_and_push(f"capture: {data.get('account_name', 'field notes')}")

        summary = "Done! Here's what I did:\n" + "\n".join(f"- {a}" for a in actions)
        await update.message.reply_text(summary)

    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to parse capture response: {e}\nResponse: {response}")
        await update.message.reply_text(
            f"I captured the info but had trouble structuring it. Here's what I got:\n\n{response}"
        )


async def handle_prep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /prep command -- generate a call briefing."""
    account_name = " ".join(context.args) if context.args else ""
    if not account_name:
        await update.message.reply_text("Usage: /prep <company name>")
        return

    await update.message.reply_text(f"Preparing briefing for {account_name}...")

    kb = get_kb()
    kb.pull()

    account_content = kb.get_account(account_name)
    if not account_content:
        # Try fuzzy match
        accounts = kb.list_accounts()
        matches = [a for a in accounts if account_name.lower() in a.lower()]
        if matches:
            account_name = matches[0]
            account_content = kb.get_account(account_name)
        else:
            await update.message.reply_text(
                f"No account found for '{account_name}'.\n\n"
                f"Available accounts:\n" + "\n".join(f"- {a}" for a in accounts)
            )
            return

    briefings = kb.get_briefings(account_name)
    related_files = kb.find_relevant_files(account_name)
    # Filter out the account file itself from related files
    kb_nodes = [f for f in related_files if "knowledge_base" in f["path"]]

    response = await claude_service.prep(account_name, account_content, briefings, kb_nodes)

    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i:i + 4000])
    else:
        await update.message.reply_text(response)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command -- welcome message."""
    await update.message.reply_text(
        "GTM Context OS Bot\n\n"
        "Just send me a message to query the knowledge base.\n\n"
        "Commands:\n"
        "/capture <notes> -- Capture contacts and insights\n"
        "/prep <company> -- Get a call briefing\n"
        "/accounts -- List all accounts"
    )


async def handle_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /accounts command -- list all tracked accounts."""
    kb = get_kb()
    kb.pull()
    accounts = kb.list_accounts()
    if accounts:
        await update.message.reply_text(
            "Tracked accounts:\n" + "\n".join(f"- {a}" for a in sorted(accounts))
        )
    else:
        await update.message.reply_text("No accounts found.")
```

**Step 2: Commit**

```bash
git add bot/handlers.py
git commit -m "feat: add Telegram handlers for query, capture, prep, and accounts"
```

---

## Task 7: Build main.py -- Wire Everything Together

**Files:**
- Create: `bot/main.py`

**Step 1: Write main.py**

`bot/main.py`:
```python
import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET
from handlers import handle_query, handle_capture, handle_prep, handle_start, handle_accounts

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Build PTB application (no updater -- webhook mode)
ptb = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)

# Register handlers
ptb.add_handler(CommandHandler("start", handle_start))
ptb.add_handler(CommandHandler("capture", handle_capture))
ptb.add_handler(CommandHandler("prep", handle_prep))
ptb.add_handler(CommandHandler("accounts", handle_accounts))
ptb.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"Setting webhook to {WEBHOOK_URL}")
    await ptb.bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def telegram_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    data = await request.json()
    update = Update.de_json(data, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Step 2: Commit**

```bash
git add bot/main.py
git commit -m "feat: add main.py wiring FastAPI + Telegram webhook"
```

---

## Task 8: Deploy to Railway

**Step 1: Configure Railway to use the bot/ subdirectory**

Create `bot/railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Step 2: Push all code to GitHub**

```bash
git add .
git commit -m "feat: add Railway config"
git push
```

**Step 3: Set up Railway (in browser)**

1. Go to railway.com dashboard
2. Click "New Project" > "Deploy from GitHub repo"
3. Select `willyhndz3/context-os`
4. In service settings, set **Root Directory** to `bot/`
5. Go to **Variables** tab and add:
   - `TELEGRAM_BOT_TOKEN` = (from BotFather)
   - `ANTHROPIC_API_KEY` = (from console.anthropic.com)
   - `WEBHOOK_SECRET` = (any random string)
   - `CLARIFY_API_KEY` = (from Clarify settings)
   - `CLARIFY_WORKSPACE_SLUG` = (from Clarify URL)
   - `GITHUB_TOKEN` = (GitHub personal access token with repo scope)
   - `GITHUB_REPO` = `willyhndz3/context-os`
   - `KNOWLEDGE_BASE_PATH` = `/app/knowledge`
6. Go to **Settings** > **Networking** > Click "Generate Domain"
7. Railway will auto-deploy

**Step 4: Verify webhook is set**

Visit in browser: `https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo`

Should show your Railway domain as the webhook URL.

**Step 5: Test the bot**

Open Telegram on your phone, find your bot, and send:
- "Hello" -- should respond
- "/accounts" -- should list accounts
- "/prep WSO2" -- should generate a briefing
- "/capture Met test person, test@example.com" -- should process and sync

---

## Task 9: Set Up Obsidian Git Sync

**Step 1: Install Obsidian Git plugin**

1. Open Obsidian
2. Settings > Community Plugins > Browse
3. Search "Obsidian Git" and install
4. Enable the plugin

**Step 2: Configure auto-pull**

In Obsidian Git settings:
- Auto pull interval: 5 minutes
- Auto commit and push: disabled (we'll do this manually or via Claude Code)
- Pull on startup: enabled

**Step 3: Verify sync**

Send a `/capture` via Telegram, wait 5 minutes, confirm the new account appears in Obsidian.

---

## Summary

| Task | What It Does |
|------|-------------|
| 1 | Initialize git, push GTM Context OS to GitHub |
| 2 | Create bot project skeleton (config, requirements, Procfile) |
| 3 | Build knowledge base reader (find files, read accounts) |
| 4 | Build Claude Sonnet service (query, capture, prep prompts) |
| 5 | Build Clarify CRM client (create person, company, link) |
| 6 | Build Telegram handlers (wire modes to services) |
| 7 | Build main.py (FastAPI + webhook) |
| 8 | Deploy to Railway + configure env vars |
| 9 | Set up Obsidian Git sync |

Total: ~400 lines of Python across 5 files + config.
