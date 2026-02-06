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
