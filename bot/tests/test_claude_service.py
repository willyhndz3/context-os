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
