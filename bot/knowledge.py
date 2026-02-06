import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class KnowledgeBase:
    def __init__(self, path: str, token: str = "", repo: str = ""):
        self.path = Path(path)
        self.token = token
        self.repo = repo

    @classmethod
    def clone_from_github(cls, repo: str, token: str, dest: str) -> "KnowledgeBase":
        """Clone or pull the knowledge base from GitHub."""
        if os.path.exists(os.path.join(dest, ".git")):
            subprocess.run(["git", "-C", dest, "pull"], check=True, capture_output=True)
        else:
            url = f"https://x-access-token:{token}@github.com/{repo}.git"
            subprocess.run(["git", "clone", url, dest], check=True, capture_output=True)
        # Configure git identity for commits from the bot
        subprocess.run(["git", "-C", dest, "config", "user.name", "GTM Context Bot"], capture_output=True)
        subprocess.run(["git", "-C", dest, "config", "user.email", "bot@gtm-context-os.local"], capture_output=True)
        # Ensure remote URL has auth token for pushing
        auth_url = f"https://x-access-token:{token}@github.com/{repo}.git"
        subprocess.run(["git", "-C", dest, "remote", "set-url", "origin", auth_url], capture_output=True)
        return cls(dest, token=token, repo=repo)

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
            push_result = subprocess.run(
                ["git", "-C", str(self.path), "push"],
                capture_output=True
            )
            if push_result.returncode != 0:
                logger.error(f"Git push failed: {push_result.stderr.decode()}")
                logger.error(f"Git push stdout: {push_result.stdout.decode()}")

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
