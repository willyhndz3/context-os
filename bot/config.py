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
