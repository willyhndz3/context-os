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
